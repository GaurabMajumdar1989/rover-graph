from typing import List
from pydantic import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="Critque of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous.")

class AnswerQuestion(BaseModel):
    """Answer the question."""

    answer: str = Field(description="~200 words deatiled answer to the question.")
    reflection: str = Field(description="Your reflection on your initial answer.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )

class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""

    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )