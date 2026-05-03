def parse_intent(question: str) -> dict:
    q = question.lower()
    intent: dict[str, str] = {}

    if "top" in q and "product" in q:
        intent["type"] = "top_n_products"
    elif "orders" in q or "transactions" in q:
        intent["type"] = "orders_summary"
    else:
        intent["type"] = "generic"

    if "last month" in q:
        intent["time_range"] = "last_month"
    elif "this week" in q:
        intent["time_range"] = "this_week"

    return intent