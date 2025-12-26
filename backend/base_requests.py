from typing import List, Dict, Any
from pydantic import BaseModel, Field, field_validator


# Existing: generic content request/response (you can keep for future)
class GenerateContentRequest(BaseModel):
    """Request model for generic content generation."""
    question: str = Field(..., description="question for content generation")
    local_llm: bool = Field(False, description="Whether to use a local LLM (default: False)")

    @field_validator("question")
    def validate_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question cannot be empty")
        return value.strip()


class GenerateContentResponse(BaseModel):
    """Response model for content generation."""
    status: str
    message: str
    data: str

    @field_validator("data")
    def validate_data(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Generated content cannot be empty")
        return value.strip()


# NEW: Schema endpoint response (renamed field to avoid shadowing)
class SchemaResponse(BaseModel):
    schema_text: str = Field(..., description="Database schema metadata as text")


# NEW: Generate-SQL endpoint
class GenerateSQLRequest(BaseModel):
    question: str = Field(..., description="Natural language question to convert to SQL")

    @field_validator("question")
    def validate_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question cannot be empty")
        return value.strip()


class GenerateSQLResponse(BaseModel):
    originalQuestion: str
    generatedSQL: str


# NEW: Execute-SQL endpoint
class ExecuteSQLRequest(BaseModel):
    originalQuestion: str
    generatedSQL: str


class ExecuteSQLResponse(BaseModel):
    originalQuestion: str
    generatedSQL: str
    rows: List[Dict[str, Any]]
