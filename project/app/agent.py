from typing import Tuple

from .nl2sql import generate_sql
from .executor import execute_safe
from .llm_client import call_llm

def refine_sql(question: str, prev_sql: str, error_msg: str) -> str:
    system_msg = (
        "You are an expert PostgreSQL SQL assistant. "
        "You fix SQL queries based on error messages without changing the user's intent."
    )

    prompt = f"""
The user asked this question:

{question}

You previously generated this SQL:

{prev_sql}

When executing it, the database returned this error:

{error_msg}

Task:
- Analyze the error and the original question.
- Generate a corrected PostgreSQL SELECT query that fixes the error.
- Do not change the meaning of the question.
- Use only the tables and columns that actually exist.
- Return ONLY the corrected SQL, with no explanation.
"""

    sql = call_llm(prompt, temperature=0.0, system=system_msg)
    sql = sql.strip()
    if sql.lower().startswith("```"):
        sql = sql.strip("`")
    return sql.strip()

def run_agentic_query(question: str, max_retries: int = 3) -> Tuple[str, list[str], list[list], int]:
    """
    Full agentic loop:
    - initial NL->SQL
    - execute
    - on error, refine SQL via LLM and retry
    Returns (final_sql, columns, rows, attempts_used).
    """
    current_sql = generate_sql(question)
    attempts = 0

    while True:
        attempts += 1
        try:
            final_sql, cols, rows = execute_safe(current_sql)
            return final_sql, list(cols), [list(r) for r in rows], attempts
        except Exception as e:
            if attempts > max_retries:
                # give up; re-raise last error
                raise e
            # refine SQL and try again
            current_sql = refine_sql(question, current_sql, str(e))