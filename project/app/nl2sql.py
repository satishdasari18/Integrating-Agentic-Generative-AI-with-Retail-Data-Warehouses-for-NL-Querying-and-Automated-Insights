from .schema_metadata import SCHEMA_METADATA
from .intent_parser import parse_intent
from .llm_client import call_llm

FEW_SHOT = """
Example 1:
Question: What are the top 5 most viewed items overall?
SQL: SELECT i.item_id, COUNT(*) AS view_count
     FROM fact_events e
     JOIN dim_item i ON e.item_id = i.item_id
     WHERE e.event_type = 'view'
     GROUP BY i.item_id
     ORDER BY view_count DESC
     LIMIT 5;

Example 2:
Question: How many transactions happened last month?
SQL: SELECT COUNT(*) AS txn_count
     FROM fact_events
     WHERE event_type = 'transaction'
       AND event_time >= date_trunc('month', CURRENT_DATE - INTERVAL '1 month')
       AND event_time <  date_trunc('month', CURRENT_DATE);

Example 3:
Question: What is the total number of views per month over the last 6 months?
SQL: SELECT
         date_trunc('month', event_time) AS month,
         COUNT(*) AS view_count
     FROM fact_events
     WHERE event_type = 'view'
       AND event_time >= CURRENT_DATE - INTERVAL '6 months'
     GROUP BY month
     ORDER BY month;
"""

def generate_sql(question: str) -> str:
    intent = parse_intent(question)

    system_msg = (
        "You are an expert PostgreSQL SQL generator for a retail analytics data warehouse. "
        "Always return ONLY a valid SQL SELECT statement that can run on PostgreSQL. "
        "Do not include explanations, comments, or backticks."
    )

    prompt = f"""
Schema:
{SCHEMA_METADATA}

Use only the tables and columns from the schema.
Generate a single PostgreSQL SELECT statement for this question.

{FEW_SHOT}

Question: {question}
SQL:
"""

    sql = call_llm(prompt, temperature=0.0, system=system_msg)
    # Remove potential code fences
    sql = sql.strip()
    if sql.lower().startswith("```"):
        sql = sql.strip("`")
    return sql.strip()