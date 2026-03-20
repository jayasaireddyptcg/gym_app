from sqlalchemy import Column, Integer, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import uuid

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    date = Column(Date)
    steps = Column(Integer, default=0)
    calories = Column(Integer, default=0)
    distance = Column(Float, default=0)

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="unique_user_date"),
    )