from __future__ import annotations

import json
import os
import re
from typing import Any

import requests
from crewai.tools import tool


SERPER_SHOPPING_ENDPOINT = "https://google.serper.dev/shopping"

_PRICE_RE = re.compile(r"[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?|[-+]?\d+(?:\.\d+)?")


def _parse_price_to_float(price: Any) -> float | None:
    """Best-effort parse of a price field returned by Serper."""
    if price is None:
        return None
    if isinstance(price, (int, float)):
        return float(price)
    s = str(price)
    m = _PRICE_RE.search(s.replace(" ", ""))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _serper_api_key() -> str:
    key = os.getenv("SERPER_API_KEY") or os.getenv("SERPER_APIKEY") or os.getenv("SERPER_KEY")
    if not key:
        raise RuntimeError("Missing SERPER_API_KEY. Put it in your .env (see .env.example).")
    return key


def _post_serper_shopping(payload: dict[str, Any]) -> dict[str, Any]:
    headers = {"X-API-KEY": _serper_api_key(), "Content-Type": "application/json"}
    resp = requests.post(SERPER_SHOPPING_ENDPOINT, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


@tool("Google Shopping Candidates (Serper)")
def serper_shopping_candidates(
    query: str,
    num: int = 10,
    gl: str = "us",
    hl: str = "en",
    location: str | None = None,
) -> str:
    """Search Google Shopping via Serper and return normalized candidates as JSON.

    Output JSON:
    {
      "query": "...",
      "count": N,
      "candidates": [
        {
          "title": "...",
          "price": 123.45,
          "currency": "USD",
          "source": "Walmart",
          "link": "https://...",
          "rating": 4.6,
          "review_count": 1200,
          "delivery": "...",
          "imageUrl": "https://..."
        }
      ],
      "raw_keys": ["...", "..."]
    }

    Notes:
    - Serper's exact fields can vary; this tool is defensive and best-effort.
    - Adjust parsing/mapping as you observe your own Serper responses.
    """
    payload: dict[str, Any] = {"q": query, "num": max(1, min(int(num), 50)), "gl": gl, "hl": hl}
    if location:
        payload["location"] = location

    data = _post_serper_shopping(payload)

    items = data.get("shopping") or data.get("shoppingResults") or data.get("shopping_results") or []
    normalized: list[dict[str, Any]] = []

    for it in items:
        title = it.get("title") or it.get("name")
        link = it.get("link") or it.get("productLink") or it.get("url")
        source = it.get("source") or it.get("merchant") or it.get("store")
        price_raw = it.get("price") or it.get("priceValue") or it.get("extracted_price")
        rating = it.get("rating") or it.get("stars")
        review_count = it.get("reviewCount") or it.get("reviews") or it.get("ratingCount")
        delivery = it.get("delivery") or it.get("shipping") or it.get("deliveryTime")
        image_url = it.get("imageUrl") or it.get("thumbnailUrl") or it.get("image")

        # rating/review_count sometimes come as strings; do best-effort conversions
        rating_f = None
        if rating is not None:
            try:
                rating_f = float(str(rating).strip())
            except ValueError:
                rating_f = None

        review_i = None
        if review_count is not None:
            try:
                review_i = int(str(review_count).strip().replace(",", ""))
            except ValueError:
                review_i = None

        normalized.append(
            {
                "title": title,
                "price": _parse_price_to_float(price_raw),
                "currency": "USD",
                "source": source,
                "link": link,
                "rating": rating_f,
                "review_count": review_i,
                "delivery": delivery,
                "imageUrl": image_url,
            }
        )

    return json.dumps(
        {"query": query, "count": len(normalized), "candidates": normalized, "raw_keys": sorted(list(data.keys()))},
        ensure_ascii=False,
        indent=2,
    )
