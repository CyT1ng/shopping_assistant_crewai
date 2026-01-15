from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class Offer(BaseModel):
    retailer: str
    price: float | None = None
    currency: str = "USD"
    shipping: float | None = None
    in_stock: bool | None = None
    url: HttpUrl | None = None


class Product(BaseModel):
    title: str
    brand: str | None = None
    model: str | None = None
    category: str | None = None
    offers: list[Offer] = Field(default_factory=list)
    rating: float | None = None
    review_count: int | None = None
    key_features: list[str] = Field(default_factory=list)
