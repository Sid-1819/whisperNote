from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes.note import router as note_router
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.note import Note

app = FastAPI(title=settings.PROJECT_NAME)

# Create tables
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, replace with frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(note_router)

@app.get("/")
def root():
    return {"message": "WhisperNote API is running"}


@app.on_event("startup")
@repeat_every(seconds=60)  # runs every 1 minute
def cleanup_expired_notes():
    db = SessionLocal()
    db.query(Note).filter(Note.expiry_time < datetime.utcnow()).delete()
    db.commit()
    db.close()