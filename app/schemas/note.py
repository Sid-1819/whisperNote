from pydantic import BaseModel, validator
from datetime import datetime, timezone

class NoteCreate(BaseModel):
    content: str
    expire_after_minutes: int

class NoteOut(BaseModel):
    id: int
    expiry_time: datetime

    class Config:
        orm_mode = True

    @validator("expiry_time", pre=True)
    def ensure_timezone(cls, value):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
