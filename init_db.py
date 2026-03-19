import asyncio
from app.core.database import engine
from app.models.base import Base

# import all models so metadata loads
from app.models import user, activity, equipment_scan, food_scan

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
