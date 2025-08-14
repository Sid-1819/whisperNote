from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import router
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from app.core.database import SessionLocal
from app.models.note import Note

app = FastAPI(title="WhisperNote")

# Create tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(router)

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