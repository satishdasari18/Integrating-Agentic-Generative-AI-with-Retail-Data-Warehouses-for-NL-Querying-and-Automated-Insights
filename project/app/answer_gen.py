from collections import Counter
from .llm_client import call_llm

def generate_answer(question: str, columns, rows, max_preview: int = 5) -> str:
    # 1) No data case: be honest and don't hallucinate
    if not rows:
        return (
            "No matching data was found in the database for this question and "
            "time range. You may want to broaden the filters or check if the "
            "dataset contains events for that period."
        )

    # 2) Prepare a small preview for the LLM
    preview_rows = rows[:max_preview]
    col_list = list(columns)

    # 3) Detect if we only have IDs as labels (e.g., item_id) and no names
    lower_cols = [c.lower() for c in col_list]
    has_item_id = "item_id" in lower_cols
    has_product_name = "product_name" in lower_cols

    # Simple heuristic description of the primary entity
    if has_product_name:
        entity_label = "products"
    elif has_item_id:
        entity_label = "items (identified by item_id only, no names)"
    else:
        entity_label = "rows"

    system_msg = (
        "You are a data analyst. "
        "Given a question and a small sample of SQL query results, "
        "write a concise 2-3 sentence business summary that reflects ONLY the data shown. "
        "If there are no clear product names, refer to them as items by ID. "
        "Do not invent product names or values that are not in the result."
    )

    prompt = f"""
Question:
{question}

Entity type (for wording):
{entity_label}

Columns:
{col_list}

Sample rows (up to {max_preview}):
{preview_rows}

Write a concise, business-friendly summary of the main insight.
Do not mention SQL or database internals.
Do not make up product names or categories that are not present in the sample rows.
"""

    return call_llm(prompt, temperature=0.2, system=system_msg).strip()