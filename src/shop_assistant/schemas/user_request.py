from __future__ import annotations

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    query: str = Field(..., description="What the user wants to buy.")
    budget: float | None = Field(None, description="Max budget (numeric).")
    currency: str = Field("USD", description="Currency code, e.g., USD.")
    region: str = Field("US", description="Shopping region, e.g., US.")
    must_haves: list[str] = Field(default_factory=list, description="Hard constraints.")
    nice_to_haves: list[str] = Field(default_factory=list, description="Soft preferences.")
    max_results: int = Field(10, ge=3, le=50, description="How many candidates to consider.")
