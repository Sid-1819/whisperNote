from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime, timedelta

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    expiry_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
