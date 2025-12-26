# backend/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from langchain_community.utilities import SQLDatabase

from config import settings

# SQLAlchemy base + engine
Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_sql_database() -> SQLDatabase:

    return SQLDatabase.from_uri(
        settings.DATABASE_URL,
        sample_rows_in_table_info=0,  # <-- focus on schema only
    )
