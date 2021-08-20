from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

from app.config import settings

# ============== Connection PostgreSQL DB ====================
engine = create_engine(settings.POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============== Connection Mongo DB =========================
client = MongoClient(settings.MONGO_DATABASE_URL)

mongo_db = client['operations']
