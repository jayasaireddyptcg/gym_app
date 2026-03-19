from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = round((time.time() - start) * 1000, 2)

        logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} time={duration}ms"
        )

        return response
