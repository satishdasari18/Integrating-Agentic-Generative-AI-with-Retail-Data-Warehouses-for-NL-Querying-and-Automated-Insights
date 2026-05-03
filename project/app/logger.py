import csv
import time
from pathlib import Path
from typing import List

LOG_PATH = Path("data/logs/query_log.csv")


def log_query(
    question: str,
    sql: str,
    columns: List[str],
    rows: List[List],
    attempts: int,
    latency_sec: float,
    source: str,
) -> None:
    """
    Append a single query run to CSV log.

    source: "api" or "cli" (or anything you like).
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "question": question,
        "sql": sql.replace("\n", " "),
        "columns": "|".join(columns),
        "row_count": len(rows),
        "attempts": attempts,
        "latency_sec": f"{latency_sec:.3f}",
    }

    write_header = not LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)