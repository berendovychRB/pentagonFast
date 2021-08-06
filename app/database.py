from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =============== For SQLITE DB ================================
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./data.db'
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# =================== FOR POSTGRESQL DB =========================
POSTGRES_DATABASE_URL = "postgresql://username:password@db:5432/api"
# POSTGRES_DATABASE_URL = "postgresql://root1:root@localhost/pentagon_db"

engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
