from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User's question about uploaded documents."
    )

    session_id: str = Field(
        default="default",
        min_length=1,
        description="Unique conversation session identifier."
    )


class SourceReference(BaseModel):
    source: str
    page: int
    chunk: int


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceReference]