from typing import Optional, Dict, Any
import json

from util.llm_factory import LLMFactory
from util.system_prompt import (
    prompt_generate_summary,
    prompt_sql_query_generator,
)


def generate_summary(text: str, local_llm: bool = False) -> Optional[str]:
    """
    Generates a summary of the given text using the LLM.
    """
    if not text or not text.strip():
        return None

    try:
        response = LLMFactory.invoke(
            system_prompt=prompt_generate_summary,
            human_message=text,
            temperature=0.7,
            local_llm=local_llm,
        )
        summary = response.content.strip()
        return summary
    except Exception as e:
        # Log the error appropriately
        print(f"Error generating summary: {e}")
        return None


def generate_sql_agent_output(
    question: str,
    schema: Optional[str] = None,
    local_llm: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Core SQL agent logic: calls LLM with SQL-specific system prompt and
    returns a parsed dict: {"sql": "...", "reasoning": "..."}.
    """
    if not question or not question.strip():
        return None

    # Build a human message including schema if provided
    if schema:
        human_message = (
            f"User question:\n{question}\n\n"
            f"Database schema:\n{schema}\n\n"
            "Generate ONLY the JSON object with 'sql' and 'reasoning'."
        )
    else:
        human_message = (
            f"User question:\n{question}\n\n"
            "Generate ONLY the JSON object with 'sql' and 'reasoning'."
        )

    try:
        response = LLMFactory.invoke(
            system_prompt=prompt_sql_query_generator,
            human_message=human_message,
            temperature=0.2,  # more deterministic for SQL
            local_llm=local_llm,
        )

        raw_text = response.content.strip()
        data = json.loads(raw_text)

        sql = data.get("sql", "").strip()
        reasoning = data.get("reasoning", "").strip()

        if not sql:
            raise ValueError("Model did not return a 'sql' field")

        return {
            "sql": sql,
            "reasoning": reasoning,
        }

    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None
