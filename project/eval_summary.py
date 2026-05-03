import csv
from pathlib import Path

EVAL_RESULTS = Path("data/eval/eval_results_v2.csv")

def parse_bool(v: str) -> bool:
    return str(v).strip().upper() == "TRUE"

def main():
    with EVAL_RESULTS.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No rows in eval_results.csv")
        return

    n = len(rows)

    gold_ok = sum(parse_bool(r["gold_success"]) for r in rows)

    baseline_ok = sum(parse_bool(r["baseline_success"]) for r in rows)
    baseline_match = sum(parse_bool(r["baseline_match"]) for r in rows)

    agent_ok = sum(parse_bool(r["agent_success"]) for r in rows)
    agent_match = sum(parse_bool(r["agent_match"]) for r in rows)

    # Latency averages (ignore empty values)
    baseline_latencies = [
        float(r["baseline_latency"])
        for r in rows
        if r.get("baseline_latency")
    ]
    agent_latencies = [
        float(r["agent_latency"])
        for r in rows
        if r.get("agent_latency")
    ]

    avg_baseline_lat = sum(baseline_latencies) / len(baseline_latencies) if baseline_latencies else 0.0
    avg_agent_lat = sum(agent_latencies) / len(agent_latencies) if agent_latencies else 0.0

    # Error reduction
    baseline_fail = n - baseline_ok
    agent_fail = n - agent_ok
    error_reduction = None
    if baseline_fail > 0:
        error_reduction = (baseline_fail - agent_fail) / baseline_fail

    print(f"Total questions: {n}")
    print(f"Gold SQL success: {gold_ok}/{n} ({gold_ok/n:.1%})")
    print()
    print("Baseline (single-pass NL->SQL):")
    print(f"  Execution success: {baseline_ok}/{n} ({baseline_ok/n:.1%})")
    print(f"  Result match (simple heuristic): {baseline_match}/{n} ({baseline_match/n:.1%})")
    print(f"  Avg latency: {avg_baseline_lat:.3f} s")
    print()
    print("Agentic (validation + refinement loop):")
    print(f"  Execution success: {agent_ok}/{n} ({agent_ok/n:.1%})")
    print(f"  Result match (simple heuristic): {agent_match}/{n} ({agent_match/n:.1%})")
    print(f"  Avg latency: {avg_agent_lat:.3f} s")
    if error_reduction is not None:
        print(f"  Error reduction vs. baseline (by execution failures): {error_reduction:.1%}")
    else:
        print("  Error reduction: N/A (no baseline failures)")

if __name__ == "__main__":
    main()