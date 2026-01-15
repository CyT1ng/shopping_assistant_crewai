from __future__ import annotations

from typing import Any


def simple_score(candidate: dict[str, Any], budget: float | None) -> float:
    """A tiny baseline scorer you can replace with something smarter.

    candidate: a dict with keys like {title, price, rating, review_count, shipping}
    """
    price = candidate.get("price")
    rating = candidate.get("rating")
    reviews = candidate.get("review_count")

    score = 0.0
    if rating is not None:
        score += float(rating) * 2.0
    if reviews is not None:
        score += min(float(reviews), 5000.0) / 5000.0  # 0..1

    if price is not None:
        score += 1.0  # having a price is good
        if budget is not None:
            # Penalize going over budget
            over = float(price) - float(budget)
            if over > 0:
                score -= min(over / max(budget, 1.0), 2.0)

    return score


def rank_candidates(candidates: list[dict[str, Any]], budget: float | None) -> list[dict[str, Any]]:
    scored = []
    for c in candidates:
        c = dict(c)
        c["_score"] = simple_score(c, budget)
        scored.append(c)
    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored
