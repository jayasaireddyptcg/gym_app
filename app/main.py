from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import auth, equipment, food, activity, exercise
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware

app = FastAPI()


def _validation_message(exc: RequestValidationError) -> str:
    errs = exc.errors()
    if not errs:
        return "Validation error"
    e0 = errs[0]
    loc = ".".join(str(x) for x in e0.get("loc", []) if x != "body")
    msg = e0.get("msg", "Invalid value")
    return f"{loc}: {msg}".strip(": ") if loc else msg


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    message = detail if isinstance(detail, str) else str(detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": message,
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": _validation_message(exc),
            },
        },
    )


# Add CORS middleware (credentials must be false when using wildcard origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

app.include_router(auth.router, prefix="/auth")
app.include_router(equipment.router, prefix="/equipment")
app.include_router(food.router, prefix="/food")
app.include_router(activity.router, prefix="/activity")
app.include_router(exercise.router)