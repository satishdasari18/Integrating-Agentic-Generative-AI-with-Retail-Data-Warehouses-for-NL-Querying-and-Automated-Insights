from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from .agent import run_agentic_query
from .answer_gen import generate_answer
from .logger import log_query

app = FastAPI(title="Retail NL-to-SQL Agent")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    sql: str
    columns: list[str]
    rows: list[list]
    answer: str
    attempts: int
    latency_sec: float

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    start = time.time()
    try:
        final_sql, cols, rows, attempts = run_agentic_query(
            req.question,
            max_retries=3,
        )
        answer = generate_answer(req.question, cols, rows)
        latency = time.time() - start

        # Log to CSV
        log_query(
            question=req.question,
            sql=final_sql,
            columns=cols,
            rows=rows,
            attempts=attempts,
            latency_sec=latency,
            source="api",
        )

        return QueryResponse(
            question=req.question,
            sql=final_sql,
            columns=cols,
            rows=rows,
            answer=answer,
            attempts=attempts,
            latency_sec=latency,
        )

    except Exception as e:
        # even failed queries can be logged if you want; for now just raise
        raise HTTPException(status_code=400, detail=str(e))