from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import router

app = FastAPI(title="WhisperNote")

# Create tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "WhisperNote API is running"}
