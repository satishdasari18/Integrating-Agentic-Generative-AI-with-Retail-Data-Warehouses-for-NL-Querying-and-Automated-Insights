from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .config import DB_URL

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def run_query(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()
    return cols, rows