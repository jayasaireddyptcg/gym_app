from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.core.logger import logger

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)

        except Exception as e:
            logger.error("Unhandled error", exc_info=True)

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "Something went wrong"
                    }
                }
            )
