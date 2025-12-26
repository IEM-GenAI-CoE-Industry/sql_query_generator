# backend/sql_execution_service.py
from typing import List, Dict, Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from db import engine


FORBIDDEN_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
]


def validate_select_only(sql: str) -> None:
    """
    Raises ValueError if the SQL is not a pure SELECT query.
    """
    lower_sql = sql.strip().lower()
    if not lower_sql.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    for kw in FORBIDDEN_KEYWORDS:
        if kw in lower_sql:
            raise ValueError(f"Query contains forbidden keyword: {kw}")


def execute_sql_query(sql: str) -> List[Dict[str, Any]]:
    """
    Executes a validated SQL query and returns list of row dicts.
    """
    validate_select_only(sql)

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = [dict(row._mapping) for row in result]
            return rows
    except SQLAlchemyError as e:
        # Reraise with clean message for API
        raise RuntimeError(f"Database error while executing query: {str(e)}") from e
