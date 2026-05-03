from .db import run_query
from .validator import validate_sql

def execute_safe(sql: str, limit: int = 100):
    """
    Validate and execute SQL, adding a LIMIT if missing.
    Returns (final_sql, columns, rows).
    """
    # 1) Basic validation
    sql = validate_sql(sql)

    low = sql.lower()
    # 2) Add LIMIT for safety if not present
    if "limit" not in low:
        sql = sql.rstrip(" ;") + f" LIMIT {limit};"

    # 3) Execute against PostgreSQL
    cols, rows = run_query(sql)
    return sql, cols, rows