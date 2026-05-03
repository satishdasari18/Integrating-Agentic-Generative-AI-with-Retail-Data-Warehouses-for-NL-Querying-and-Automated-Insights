from app.db import run_query

cols, rows = run_query("SELECT 1;")
print(cols, rows)