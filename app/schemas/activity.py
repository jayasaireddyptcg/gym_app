from pydantic import BaseModel, Field
from datetime import date as dt_date


class ActivityCreate(BaseModel):
    # Avoid name clash between the field `date` and the imported type `date` (Pydantic v2).
    date: dt_date = Field(default_factory=dt_date.today)
    steps: int = 0
    calories: int = 0
    distance: float = 0.0
