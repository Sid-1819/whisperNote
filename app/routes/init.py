from fastapi import APIRouter
from app.routes import note

router = APIRouter()
router.include_router(note.router)
