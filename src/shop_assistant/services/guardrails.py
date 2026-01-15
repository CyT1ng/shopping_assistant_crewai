from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailResult:
    ok: bool
    reason: str | None = None


# Keep this list strict: the assistant should avoid facilitating age-restricted / regulated goods.
DISALLOWED_KEYWORDS = {
    # age-restricted / regulated
    "alcohol", "beer", "wine", "vodka", "whiskey",
    "cigarette", "cigarettes", "vape", "nicotine", "tobacco",
    # weapons
    "gun", "firearm", "ammunition", "ammo", "silencer",
    "switchblade", "brass knuckles", "taser",
    # illicit drugs
    "weed", "marijuana", "thc", "cbd", "magic mushrooms",
}


def validate_user_query(query: str) -> GuardrailResult:
    q = query.lower()
    for kw in DISALLOWED_KEYWORDS:
        if kw in q:
            return GuardrailResult(
                ok=False,
                reason=(
                    "I can't help shop for age-restricted or regulated items. "
                    "Try a different product category."
                ),
            )
    return GuardrailResult(ok=True)


def validate_inputs(inputs: dict) -> dict:
    # Called pre-kickoff. Raise early for unsupported categories.
    query = str(inputs.get("query", "")).strip()
    if not query:
        raise ValueError("Missing required input: query")

    gr = validate_user_query(query)
    if not gr.ok:
        raise ValueError(gr.reason or "Query blocked by guardrails.")
    return inputs
