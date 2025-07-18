from fastapi import Request, HTTPException
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings

class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Пропуск CORS preflight-запросов
        if request.method == 'OPTIONS' and request.url.path.startswith('/api'):
            return Response(status_code=200)

        # Проверяем заголовок X-Token для всех API-запросов
        if request.url.path.startswith('/api'):
            token = request.headers.get('X-Token')
            if token != settings.PUBLIC_TOKEN:
                raise HTTPException(status_code=401, detail='Unauthorized')

        # Передаём управление следующему обработчику
        return await call_next(request)