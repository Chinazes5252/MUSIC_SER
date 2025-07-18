import yt_dlp
from typing import Dict
from config import settings

class YouTubeClient:
    def __init__(self):
        self.key = settings.YOUTUBE_KEY

    async def search(self, q: str) -> dict:
        import aiohttp
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'q': q,
            'key': self.key,
            'part': 'snippet',
            'maxResults': 15,
            'type': 'video',
            'videoCategoryId': '10'
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, params=params) as r:
                data = await r.json()
        return [
            {'id': i['id']['videoId'], 'title': i['snippet']['title'], 'channel': i['snippet']['channelTitle'], 'thumbnail': i['snippet']['thumbnails']['high']['url']}
            for i in data.get('items', [])
        ]

    async def get_stream_url(self, video_id: str) -> str:
        opts = {'format':'bestaudio/best','quiet':True,'noplaylist':True}
        def extract():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(f'https://youtu.be/{video_id}', download=False)
                return info['url']
        import asyncio
        return await asyncio.to_thread(extract)