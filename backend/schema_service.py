# backend/schema_service.py

from db import get_sql_database


def get_schema_metadata() -> str:
   
    
    db = get_sql_database()
    return db.get_table_info()

from sqlalchemy import text
from db import get_sql_database


def get_table_names() -> list[str]:
    """
    Returns all table names from the public schema.
    """
    engine = get_sql_database()

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE';
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        tables = [row[0] for row in result]

    return tables

