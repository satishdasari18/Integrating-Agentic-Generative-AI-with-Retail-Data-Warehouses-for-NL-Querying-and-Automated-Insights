import time

from app.agent import run_agentic_query
from app.answer_gen import generate_answer
from app.logger import log_query

def pretty_print_table(columns, rows, max_rows=10):
    cols = list(columns)
    sample = rows[:max_rows]

    # simple column-width calculation
    widths = [len(str(c)) for c in cols]
    for row in sample:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    # header
    header = " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cols))
    sep = "-+-".join("-" * widths[i] for i in range(len(cols)))
    print(header)
    print(sep)
    for row in sample:
        print(" | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row)))

def main():
    print("Retail NL-to-SQL CLI (type 'exit' to quit)")
    while True:
        question = input("\nQuestion> ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break

        start = time.time()
        try:
            sql, cols, rows, attempts = run_agentic_query(question, max_retries=3)
            latency = time.time() - start
            answer = generate_answer(question, cols, rows)

            print("\nGenerated SQL:")
            print(sql)
            print(f"\nAttempts: {attempts}, Latency: {latency:.3f} s")
            print("\nResult preview:")
            if rows:
                pretty_print_table(cols, rows)
            else:
                print("(no rows)")

            print("\nNarrative:")
            print(answer)

            # log
            log_query(
                question=question,
                sql=sql,
                columns=cols,
                rows=rows,
                attempts=attempts,
                latency_sec=latency,
                source="cli",
            )

        except Exception as e:
            print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()