# bot/ytdownloader.py
import yt_dlp
from datetime import datetime
import os
from pathlib import Path

def download_youtube_audio(video_id: str) -> dict:
    filename = str(Path('audio_files') / f"music_{datetime.now().timestamp()}.mp3")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,  # Исключаем плейлисты
        'socket_timeout': 30  # Таймаут соединения
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not video_id.startswith('http'):
                video_id = f"ytsearch:{video_id}"
            
            info = ydl.extract_info(video_id, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            return {
                'title': info['title'],
                'artist': info.get('uploader', 'Unknown Artist'),
                'duration': info['duration'],
                'filepath': filename
            }
    except Exception as e:
        if Path(filename).exists():
            os.remove(filename)
        raise e