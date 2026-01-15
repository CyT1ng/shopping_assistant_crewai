from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class RecommendedItem(BaseModel):
    rank: int = Field(..., ge=1)
    title: str
    why: list[str]
    estimated_total: float | None = None
    currency: str = "USD"
    best_link: HttpUrl | None = None
    tradeoffs: list[str] = Field(default_factory=list)


class RecommendationOutput(BaseModel):
    summary: str
    recommendations: list[RecommendedItem]
    follow_up_questions: list[str] = Field(default_factory=list)
