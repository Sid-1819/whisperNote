from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes.note import router as note_router
from fastapi_utils.tasks import repeat_every
from app.utils.cleanup import delete_expired_notes
from datetime import datetime
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.note import Note
from app.core.logging_config import setup_logging
from app.core.metrics import REQUEST_COUNT, start_metrics_server
import threading
import time

setup_logging()
app = FastAPI(title=settings.PROJECT_NAME)
start_metrics_server(8001)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(endpoint=request.url.path, method=request.method).inc()
    return response

def start_cleanup_task():
    def task():
        while True:
            try:
                db = SessionLocal()
                delete_expired_notes(db)
            finally:
                db.close()
            time.sleep(60)  # run every 60 seconds
    thread = threading.Thread(target=task, daemon=True)
    thread.start()

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