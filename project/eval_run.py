import time
import csv
from pathlib import Path

from app.nl2sql import generate_sql
from app.executor import execute_safe
from app.agent import run_agentic_query
from app.db import run_query  # for gold SQL execution

EVAL_INPUT = Path("data/eval/questions_gold.csv")
EVAL_OUTPUT = Path("data/eval/eval_results_v2.csv")

def exec_gold(sql: str):
    cols, rows = run_query(sql)
    return cols, rows

def main():
    rows_out = []

    with EVAL_INPUT.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        questions = list(reader)

    for q in questions:
        qid = q["id"]
        question = q["question"]
        gold_sql = q["gold_sql"]

        print(f"Evaluating {qid}: {question}")

        # 1) Gold SQL
        try:
            gold_cols, gold_rows = exec_gold(gold_sql)
            gold_success = True
        except Exception as e:
            print(f"  GOLD ERROR: {e}")
            gold_cols, gold_rows = [], []
            gold_success = False

        # 2) Baseline
        baseline_success = False
        baseline_match = False
        baseline_latency = None
        baseline_sql = ""

        start = time.time()
        try:
            baseline_sql = generate_sql(question)
            _, b_cols, b_rows = execute_safe(baseline_sql)
            baseline_success = True
            baseline_match = gold_success and len(b_rows) == len(gold_rows)
        except Exception as e:
            print(f"  BASELINE ERROR: {e}")
        end = time.time()
        baseline_latency = end - start

        # 3) Agentic
        agent_success = False
        agent_match = False
        agent_latency = None
        agent_sql = ""
        agent_attempts = 0

        start = time.time()
        try:
            agent_sql, a_cols, a_rows, agent_attempts = run_agentic_query(
                question,
                max_retries=3,
            )
            agent_success = True
            agent_match = gold_success and len(a_rows) == len(gold_rows)
        except Exception as e:
            print(f"  AGENTIC ERROR: {e}")
        end = time.time()
        agent_latency = end - start

        rows_out.append({
            "id": qid,
            "question": question,
            "category": q.get("category", ""),
            "difficulty": q.get("difficulty", ""),
            "gold_success": gold_success,
            "baseline_success": baseline_success,
            "baseline_match": baseline_match,
            "baseline_latency": f"{baseline_latency:.3f}" if baseline_latency is not None else "",
            "agent_success": agent_success,
            "agent_match": agent_match,
            "agent_latency": f"{agent_latency:.3f}" if agent_latency is not None else "",
            "agent_attempts": agent_attempts,
            "baseline_sql": baseline_sql,
            "agent_sql": agent_sql,
        })

    fieldnames = list(rows_out[0].keys()) if rows_out else []
    EVAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with EVAL_OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\nSaved evaluation results to {EVAL_OUTPUT}")

if __name__ == "__main__":
    main()