from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="admin",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("database connection was successful")
except Exception as e:
    print("Error in connecting database ")
    print("Error : ", e)
