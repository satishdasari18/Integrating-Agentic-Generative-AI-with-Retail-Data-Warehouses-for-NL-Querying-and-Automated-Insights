from app.nl2sql import generate_sql

q = "What are the top 5 most viewed products last month?"
sql = generate_sql(q)
print("Generated SQL:\n", sql)