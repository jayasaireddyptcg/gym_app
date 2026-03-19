from sqlalchemy import Column, String, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import uuid

class EquipmentScan(Base):
    __tablename__ = "equipment_scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    equipment_id = Column(String)
    confidence = Column(Float)

    muscles = Column(JSON)
    instructions = Column(String)