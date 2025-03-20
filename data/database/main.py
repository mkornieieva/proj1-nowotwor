from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from services import get_image_by_id
import models
# Tworzenie tabeli w bazie (jeśli nie istnieje)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Funkcja do pobierania sesji bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/images/{image_id}")
def read_image(image_id: int, db: Session = Depends(get_db)):
    image_record = get_image_by_id(db, image_id)
    if not image_record:
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image_record.image_data, media_type="image/png")