from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, equipment, food, activity, exercise
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

app.include_router(auth.router, prefix="/auth")
app.include_router(equipment.router, prefix="/equipment")
app.include_router(food.router, prefix="/food")
app.include_router(activity.router, prefix="/activity")
app.include_router(exercise.router, prefix="/exercises")