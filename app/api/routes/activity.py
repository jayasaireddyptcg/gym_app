from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.activity import ActivityLog
from app.schemas.activity import ActivityCreate
from app.api.deps import get_current_user
from app.models.user import User
from datetime import date, timedelta

router = APIRouter()

@router.post("/log")
async def log_activity(
    payload: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ActivityLog).where(
            ActivityLog.user_id == current_user.id,
            ActivityLog.date == payload.date
        )
    )

    existing = result.scalar_one_or_none()

    if existing:
        existing.steps = payload.steps
        existing.calories = payload.calories
        existing.distance = payload.distance
    else:
        new_log = ActivityLog(
            user_id=current_user.id,
            date=payload.date,
            steps=payload.steps,
            calories=payload.calories,
            distance=payload.distance
        )
        db.add(new_log)

    await db.commit()

    return {"success": True}

@router.get("/today")
async def get_today_activity(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    result = await db.execute(
        select(ActivityLog).where(
            ActivityLog.user_id == current_user.id,
            ActivityLog.date == today
        )
    )

    log = result.scalar_one_or_none()

    if not log:
        return {"success": True, "data": None}

    return {
        "success": True,
        "data": {
            "steps": log.steps,
            "calories": log.calories,
            "distance": log.distance
        }
    }

@router.get("/weekly")
async def weekly_activity(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    start = today - timedelta(days=7)

    result = await db.execute(
        select(ActivityLog).where(
            ActivityLog.user_id == current_user.id,
            ActivityLog.date >= start
        )
    )

    logs = result.scalars().all()

    data = [
        {
            "date": log.date,
            "steps": log.steps,
            "calories": log.calories,
            "distance": log.distance
        }
        for log in logs
    ]

    return {"success": True, "data": data}
