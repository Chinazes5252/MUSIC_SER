import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio, BotCommand, BotCommandScopeDefault
from telethon.tl.functions.bots import SetBotCommandsRequest
import logging
from config import settings
from database import Database
from youtube_api import YouTubeClient
from lastfm_api import LastFMClient
from auth import TokenAuthMiddleware
from ytdownloader import download_youtube_audio
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # теперь разрешены все origin
    allow_credentials=True,
    allow_methods=["*"],      # разрешены все HTTP-методы
    allow_headers=["*"],      # разрешены все заголовки
)
app.add_middleware(TokenAuthMiddleware)

db = Database()
yt_client = YouTubeClient()
lfm_client = LastFMClient()

@app.get('/api/search')
async def search(q: str, _=None):
    if len(q) < 2: return JSONResponse({'error':'Too short'}, status_code=400)
    return await yt_client.search(q)

@app.get('/api/stream')
async def stream(id: str):
    url = await yt_client.get_stream_url(id)
    return PlainTextResponse(url)

@app.get('/api/recommendations')
async def rec(track: str, artist: str):
    return await lfm_client.recommendations(artist, track)

@app.post('/api/save')
async def save(request: Request):
    data = await request.json()
    user_id = data.get('user_id'); vid = data.get('track_id')
    if not user_id or not vid: return JSONResponse({'error':'Invalid'},status_code=400)
    now = datetime.now();
    # rate limiting omitted for brevity
    info = await asyncio.to_thread(download_youtube_audio, vid)
    file_hash = os.popen(f"md5sum {info['filepath']}").read().split()[0]
    if not db.add_track(user_id, info['title'], info['artist'], int(info['duration']), info['filepath']):
        return {'status':'already_exists'}
    await bot.send_file(int(user_id), info['filepath'], attributes=[DocumentAttributeAudio(title=info['title'],duration=int(info['duration']),performer=info['artist'])])
    os.remove(info['filepath']);
    return {'status':'saved'}

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    if 'message' in data: upd = events.UpdateNewMessage.from_dict(data)
    else: upd = events.UpdateBotCallbackQuery.from_dict(data)
    await bot.process_updates([upd]); return {'ok':True}

# Health check
@app.get('/health')
async def health():
    return JSONResponse({'status':'ok'})

# Telethon startup
@app.on_event('startup')
async def start_bot():
    global bot
    bot = TelegramClient('bot', settings.API_ID, settings.API_HASH)
    await bot.start(bot_token=settings.BOT_TOKEN)
    await bot(SetBotCommandsRequest(scope=BotCommandScopeDefault(), lang_code='ru', commands=[
        BotCommand('start','Старт'),BotCommand('download','Моя музыка'),BotCommand('help','Помощь')
    ]))
    @bot.on(events.NewMessage(pattern='/start'))
    async def on_start(e):
        await e.respond(f"🎧 Добро пожаловать! {settings.WEBAPP_URL}")
    @bot.on(events.NewMessage(pattern='/download'))
    async def on_download(e):
        u=e.sender_id; tracks=db.get_user_tracks(u)
        for t,a,d,p in tracks: await e.respond(file=p, attributes=[DocumentAttributeAudio(title=t,duration=d,performer=a)])
    asyncio.create_task(bot.run_until_disconnected())

@app.on_event('shutdown')
async def shutdown():
    await bot.disconnect(); db.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)