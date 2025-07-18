from urllib.parse import quote
import aiohttp
from config import settings

class LastFMClient:
    def __init__(self):
        self.key = settings.LASTFM_KEY

    async def recommendations(self, artist: str, track: str) -> list:
        url = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'track.getsimilar',
            'artist': artist,
            'track': track,
            'api_key': self.key,
            'format': 'json'
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, params=params) as r:
                data = await r.json()
        return data.get('similartracks', {}).get('track', [])