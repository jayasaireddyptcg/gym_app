from sqlalchemy import Column, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import uuid

class FoodScan(Base):
    __tablename__ = "food_scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    items = Column(JSON)
    total_calories = Column(Integer)