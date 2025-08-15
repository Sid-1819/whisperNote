from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteOut
from app.utils.encryption import encrypt_text, decrypt_text

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    encrypted_content = encrypt_text(note.content)
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=note.expire_after_minutes)

    db_note = Note(content=encrypted_content, expiry_time=expiry_time)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@router.get("/{note_id}")
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    now_utc = datetime.now(timezone.utc)

    # Ensure expiry_time is timezone-aware
    expiry_time = db_note.expiry_time
    if expiry_time.tzinfo is None:
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)

    # Check expiry
    if now_utc > expiry_time:
        db.delete(db_note)
        db.commit()
        raise HTTPException(status_code=410, detail="Note expired")

    # Decrypt and delete (self-destruct)
    content = decrypt_text(db_note.content)
    db.delete(db_note)
    db.commit()
    return {"content": content}
