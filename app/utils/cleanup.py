from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.note import Note

def delete_expired_notes(db: Session):
    now = datetime.now(timezone.utc)
    expired_notes = db.query(Note).filter(Note.expiry_time < now).all()
    for note in expired_notes:
        db.delete(note)
    db.commit()
