# app.py — FastAPI Backend Controller
# PRD Reference: Section 10, FR-27
# PENTING: Gunakan `use context7` untuk verifikasi API FastAPI sebelum run

import json
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.config import (
    API_HOST, API_PORT, AVAILABLE_MODELS, LLM_MODEL_NAME,
    EVAL_RESULTS_DIR,
)
from src.chain import get_response
from src.logger_manager import get_logger

logger = get_logger("app")

app = FastAPI(title="UNSRAT RAG Chatbot API", version="1.0.0")


# ── Request/Response Models ────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Request body untuk endpoint /api/chat."""
    query:        str
    config:       str = "b"    # default Config B
    chat_history: list[dict] = []
    model:        str = LLM_MODEL_NAME


# ── API Endpoints ──────────────────────────────────────────────────────────────

@app.get("/api/config")
async def get_config():
    """
    Kembalikan daftar config dan model yang tersedia.
    (PRD Section 10.4)
    """
    return JSONResponse({
        "available_models": AVAILABLE_MODELS,
        "active_model":     LLM_MODEL_NAME,
        "configs":          ["a", "b", "c"],
    })


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Proses query dan kembalikan SSE stream.

    Event types: thinking, token, citations, done, error.
    (PRD Section 10.3, FR-27)
    """
    logger.info(
        f"POST /api/chat | config={request.config} | model={request.model} | "
        f"query='{request.query[:60]}'"
    )

    def event_generator():
        yield from get_response(
            query=request.query,
            config=request.config,
            chat_history=request.chat_history,
            model_name=request.model,
            streaming=True,
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/evaluation")
async def get_evaluation():
    """
    Baca dan kembalikan statistik evaluasi dari CSV hasil.

    Mengembalikan mean, std per metrik per config.
    Data ini digunakan oleh Tab Evaluasi frontend untuk render Chart.js.
    """
    result = {"configs": {}, "wilcoxon": {}}

    for config_label in ["a", "b", "c"]:
        csv_path = EVAL_RESULTS_DIR / f"hasil_config_{config_label}.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "response_time_seconds"]
            stats = {}
            for m in metrics:
                if m in df.columns:
                    stats[m] = {
                        "mean": round(df[m].mean(), 4),
                        "std":  round(df[m].std(), 4),
                        "min":  round(df[m].min(), 4),
                        "max":  round(df[m].max(), 4),
                    }
            result["configs"][config_label] = stats

    # Wilcoxon results
    wilcoxon_path = EVAL_RESULTS_DIR / "statistical_test.csv"
    if wilcoxon_path.exists():
        df_w = pd.read_csv(wilcoxon_path)
        for _, row in df_w.iterrows():
            result["wilcoxon"][row["metric"]] = {
                "statistic": row.get("wilcoxon_statistic"),
                "p_value":   row.get("p_value"),
                "significant": row.get("significant_at_0.05"),
                "winner":    row.get("winner"),
            }

    # Audit log (5 transaksi terakhir)
    from src.config import CHAT_LOG_PATH
    if CHAT_LOG_PATH.exists():
        df_audit = pd.read_csv(CHAT_LOG_PATH)
        result["audit_log"] = df_audit.tail(5).to_dict(orient="records")
    else:
        result["audit_log"] = []

    return JSONResponse(result)


# ── Static Files & Root ────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve SPA frontend."""
    index_path = Path("static/index.html")
    if not index_path.exists():
        return HTMLResponse("<h1>Frontend belum tersedia. Buat static/index.html.</h1>")
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Memulai server UNSRAT RAG di http://{API_HOST}:{API_PORT}")
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=False)
