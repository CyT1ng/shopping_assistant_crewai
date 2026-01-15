from shop_assistant.services.guardrails import validate_user_query


def test_guardrails_allows_safe_query():
    assert validate_user_query("wireless keyboard").ok is True


def test_guardrails_blocks_restricted_query():
    assert validate_user_query("buy beer").ok is False
