from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    content: str
    expire_after_minutes: int

class NoteOut(BaseModel):
    id: int
    expiry_time: datetime

    class Config:
        orm_mode = True
