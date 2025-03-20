from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "nowotwor_user"
DB_PASSWORD = "nowotwor_eiti"
DB_HOST = "localhost"
DB_SERVICE = "XEPDB1"

DATABASE_URL = f"oracle+cx_oracle://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:1521/?service_name={DB_SERVICE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
