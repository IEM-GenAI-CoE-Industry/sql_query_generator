import requests

from config import settings
from schema_service import get_schema_metadata

# 👉 Paste one of the names you saw from list_models.py, e.g.:
# MODEL_NAME = "models/gemini-2.5-flash"
MODEL_NAME = "models/gemini-2.5-flash"  # <-- change this to whatever you actually have

# Build endpoint directly from the full model name
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent"

SQL_GENERATION_PROMPT = """
You are a SQL query generator. Return ONLY a SQL query.

Rules:
- Only SELECT queries (no UPDATE/DELETE/INSERT/ALTER/DROP/TRUNCATE).
- Use ONLY the provided schema; do not invent tables or columns.
- Output SQL only. No explanation, no comments, no markdown fences.

Schema:
{schema_metadata}

User query:
{user_input}
"""


def _call_gemini(prompt: str) -> str:
    params = {"key": settings.GOOGLE_API_KEY}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    resp = requests.post(GEMINI_ENDPOINT, params=params, json=payload, timeout=60)
    try:
        resp.raise_for_status()
    except Exception as e:
        try:
            error_json = resp.json()
        except Exception:
            error_json = resp.text
        raise RuntimeError(f"Gemini HTTP error: {e} | Response: {error_json}")

    data = resp.json()
    # candidates[0].content.parts[0].text is the usual text output
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response format: {data}") from e

    return text.strip()


def generate_sql_from_question(user_input: str) -> str:
    schema_metadata = get_schema_metadata()

    prompt = SQL_GENERATION_PROMPT.format(
        schema_metadata=schema_metadata,
        user_input=user_input,
    )

    raw_sql = _call_gemini(prompt)

    # Just in case the model ignores "no markdown" rule
    if raw_sql.startswith("```"):
        parts = raw_sql.split("```")
        if len(parts) >= 2:
            raw_sql = parts[1].strip()

    if not raw_sql.endswith(";"):
        raw_sql = raw_sql.rstrip() + ";"

    return raw_sql
