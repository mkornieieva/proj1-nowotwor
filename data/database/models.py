from sqlalchemy import Column, Integer, LargeBinary
from database import Base

class ProcessedImage(Base):
    __tablename__ = "ProcessedImages"

    proc_image_id = Column(Integer, primary_key=True, index=True)
    image_data = Column(LargeBinary, nullable=False)
