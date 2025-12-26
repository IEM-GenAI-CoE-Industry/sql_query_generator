from fastapi import APIRouter, HTTPException, status
import logging

from base_requests import (
    GenerateContentRequest,
    GenerateContentResponse,
    SchemaResponse,
    GenerateSQLRequest,
    GenerateSQLResponse,
    ExecuteSQLRequest,
    ExecuteSQLResponse,
)
from test_run import generate_summary  # optional, for old /generate
from schema_service import get_schema_metadata, get_table_names
from nl2sql_service import generate_sql_from_question
from sql_execution_service import execute_sql_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter(tags=["SQG API Services"])


# --- Legacy endpoint: generic content (optional) ---
@api_router.post(
    "/generate",
    response_model=GenerateContentResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def generate_content(request: GenerateContentRequest) -> GenerateContentResponse:
    """
    Legacy endpoint: generic content generation (summary).
    Not required by the new spec but kept for compatibility.
    """
    try:
        logger.info("Generating generic content for question")
        summary = generate_summary(text=request.question, local_llm=request.local_llm)

        if summary is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to generate content",
            )

        return GenerateContentResponse(
            status="success",
            message="Content generated successfully",
            data=summary,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}",
        )
    




# --- 1) GET /schema ---

@api_router.get(
    "/tables",
    status_code=status.HTTP_200_OK,
)
async def list_tables():
    """
    Returns list of available database tables.
    """
    try:
        tables = get_table_names()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@api_router.get(
    "/schema",
    response_model=SchemaResponse,
    status_code=status.HTTP_200_OK,
)
async def get_schema() -> SchemaResponse:
    """
    Returns schema metadata for the database.
    """
    try:
        schema_text = get_schema_metadata()
        return SchemaResponse(schema_text=schema_text)

    except Exception as e:
        logger.error(f"Error fetching schema: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching schema: {str(e)}",
        )


# --- 2) POST /generate-sql ---
@api_router.post(
    "/generate-sql",
    response_model=GenerateSQLResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_sql_endpoint(
    request: GenerateSQLRequest,
) -> GenerateSQLResponse:
    """
    Takes a natural-language question and returns a SQL query using Gemini + schema.
    """
    try:
        logger.info(f"Generating SQL for question: {request.question!r}")
        sql = generate_sql_from_question(request.question)
        return GenerateSQLResponse(
            originalQuestion=request.question,
            generatedSQL=sql,
        )
    except Exception as e:
        logger.error(f"Error generating SQL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating SQL: {str(e)}",
        )


# --- 3) POST /execute-sql ---
@api_router.post(
    "/execute-sql",
    response_model=ExecuteSQLResponse,
    status_code=status.HTTP_200_OK,
)
async def execute_sql_endpoint(
    request: ExecuteSQLRequest,
) -> ExecuteSQLResponse:
    """
    Validates and executes the provided SQL query, returning result rows.
    """
    try:
        logger.info("Executing SQL query")
        rows = execute_sql_query(request.generatedSQL)
        return ExecuteSQLResponse(
            originalQuestion=request.originalQuestion,
            generatedSQL=request.generatedSQL,
            rows=rows,
        )
    except ValueError as ve:
        # validation error (non-SELECT)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )
    except RuntimeError as re:
        # DB error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(re),
        )
    except Exception as e:
        logger.error(f"Unexpected error executing SQL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
    
#Health Check Endpoint
@api_router.get("/health", tags=["SQG API Services"])
async def health_check():
    return {"status": "UP"}

