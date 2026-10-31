from pydantic import BaseModel, Field
from typing import Any


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)


class QuestionResponse(BaseModel):
    success: bool
    question: str
    intent: str
    result: Any = None
    message: str = ""