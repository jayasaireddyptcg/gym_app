from pydantic import BaseModel
from datetime import date

class ActivityCreate(BaseModel):
    date: date
    steps: int = 0
    calories: int = 0
    distance: int = 0
