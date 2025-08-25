# app/main.py

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.config import settings
from app.api.routes import router as api_router
from app.db.session import engine


app = FastAPI(title="Amazon FBA Analytics API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _load_sql_statements(path: Path) -> list[str]:
    """
    Read a .sql file, strip out '--' comments, split on semicolons,
    and return individual statements (non-empty).
    """
    raw = path.read_text(encoding="utf-8")
    # remove line comments
    lines = []
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("--") or s == "":
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    # split on semicolons
    stmts = [s.strip() for s in cleaned.split(";") if s.strip()]
    return stmts

# Startup: run init.sql statements one by one
@app.on_event("startup")
async def startup() -> None:
    init_path = Path(__file__).parent / "db" / "init.sql"
    if init_path.exists():
        stmts = _load_sql_statements(init_path)
        async with engine.begin() as conn:
            for stmt in stmts:
                await conn.exec_driver_sql(stmt)
    else:
        print(f"[WARN] init.sql not found at {init_path} — skipping DB bootstrap")

# Shutdown: close DB engine
@app.on_event("shutdown")
async def shutdown() -> None:
    await engine.dispose()

# API routes
app.include_router(api_router, prefix="/api")
