FORBIDDEN_KEYWORDS = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create ",
    "grant",
    "revoke",
)

def validate_sql(sql: str) -> str:
    """
    Very simple validator: only allow SELECT queries and block DML/DDL.
    """
    low = sql.lower().strip()

    if not low.startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")

    if any(word in low for word in FORBIDDEN_KEYWORDS):
        raise ValueError("Unsafe SQL detected (DML/DDL not allowed).")

    return sql