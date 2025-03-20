from sqlalchemy.orm import Session
from models import ProcessedImage

def get_image_by_id(db: Session, image_id: int):
    return db.query(ProcessedImage).filter(ProcessedImage.proc_image_id == image_id).first()
