# app.py — FastAPI Backend Controller
# PRD Reference: Section 10, FR-27
# PENTING: Gunakan `use context7` untuk verifikasi API FastAPI sebelum run

import json
import os
import shutil
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.config import (
    API_HOST, API_PORT, AVAILABLE_MODELS, LLM_MODEL_NAME,
    EVALUATOR_MODEL_NAME, EMBEDDING_MODEL_NAME, GOOGLE_API_KEY,
    NVIDIA_NIM_API_KEY, ROOT_DIR, CHROMA_DIR_B, CHROMA_COLLECTION_B,
    BM25_INDEX_PATH, EVAL_RESULTS_DIR, SYSTEM_LOG_PATH,
)
from src.chain import get_response
from src.logger_manager import get_logger
from src.preflight import preflight_check

logger = get_logger("app")

app = FastAPI(title="UNSRAT RAG Chatbot API", version="1.0.0")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(f"Unhandled exception occurred during request to {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Terjadi kesalahan internal pada server. Silakan hubungi administrator."}
    )


# ── Helper Functions ──────────────────────────────────────────────────────────

def _load_manifest() -> dict:
    """
    Muat run_manifest.json dari EVAL_RESULTS_DIR / "archive".
    Buat direktori jika belum ada. Jika file belum ada, return {"runs": []}.
    """
    archive_dir = EVAL_RESULTS_DIR / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = archive_dir / "run_manifest.json"

    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Gagal membaca manifest file: {e}")
            return {"runs": []}
    return {"runs": []}


def _save_manifest(manifest: dict) -> None:
    """
    Tulis JSON ke EVAL_RESULTS_DIR / "archive" / "run_manifest.json" secara atomik dengan indentasi.
    """
    archive_dir = EVAL_RESULTS_DIR / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = archive_dir / "run_manifest.json"
    tmp_path = archive_dir / "run_manifest.json.tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    tmp_path.replace(manifest_path)


def tail_log_file(filepath: Path, n_lines: int = 50) -> list[str]:
    """
    Membaca file dari akhir secara efisien menggunakan binary seek pointer (4KB chunks)
    dan mengembalikan N baris terakhir sebagai list of string.
    Mengembalikan [] jika file tidak ada.
    """
    if not filepath.exists() or not filepath.is_file():
        return []

    chunk_size = 4096
    lines: list[str] = []
    buffer = ""

    try:
        with open(filepath, "rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size

            while pointer > 0 and len(lines) < n_lines:
                read_size = min(chunk_size, pointer)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size).decode("utf-8", errors="replace")
                buffer = chunk + buffer

                split_lines = buffer.splitlines(keepends=False)
                if pointer > 0:
                    buffer = split_lines[0]
                    lines = split_lines[1:] + lines
                else:
                    lines = split_lines + lines

            if len(lines) > n_lines:
                lines = lines[-n_lines:]
            return lines
    except Exception as e:
        logger.error(f"Gagal membaca tail log file {filepath}: {e}")
        return []


# ── Request/Response Models ────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Request body untuk endpoint /api/chat."""
    query:        str
    config:       str = "b"    # default Config B
    chat_history: list[dict] = []
    model:        str = LLM_MODEL_NAME


class ActivateRunRequest(BaseModel):
    """Request body untuk endpoint /api/dev/runs/activate."""
    run_id: str


class ModelTestRequest(BaseModel):
    model_name: str


class ModelSetRequest(BaseModel):
    model_name: str


_ACTIVE_DEV_MODEL = None


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
        # Config A is archived for backup. Restricting API output to B and C.
        "configs":          ["b", "c"],
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

    Mengembalikan mean, std per metrik per config beserta metadata parameter uji.
    """
    from datetime import datetime

    result = {"configs": {}, "wilcoxon": {}, "metadata": {}}

    # Ekstrak data metadata parameter pengujian untuk laporan skripsi
    dataset_size = 0
    from src.config import EVAL_DATASET_PATH
    if EVAL_DATASET_PATH.exists():
        try:
            df_gt = pd.read_csv(EVAL_DATASET_PATH)
            dataset_size = len(df_gt)
        except Exception:
            pass

    last_run = "-"
    last_run_b = "-"
    last_run_c = "-"
    latest_mtime = 0.0

    # Config B timestamp
    path_b = EVAL_RESULTS_DIR / "hasil_config_b.csv"
    if path_b.exists():
        try:
            mtime_b = os.path.getmtime(path_b)
            last_run_b = datetime.fromtimestamp(mtime_b).strftime("%Y-%m-%d %H:%M")
            if mtime_b > latest_mtime:
                latest_mtime = mtime_b
        except Exception:
            pass

    # Config C timestamp
    path_c = EVAL_RESULTS_DIR / "hasil_config_c.csv"
    if path_c.exists():
        try:
            mtime_c = os.path.getmtime(path_c)
            last_run_c = datetime.fromtimestamp(mtime_c).strftime("%Y-%m-%d %H:%M")
            if mtime_c > latest_mtime:
                latest_mtime = mtime_c
        except Exception:
            pass

    if latest_mtime > 0:
        last_run = datetime.fromtimestamp(latest_mtime).strftime("%Y-%m-%d %H:%M")

    result["metadata"] = {
        "last_run":        last_run,
        "last_run_b":      last_run_b,
        "last_run_c":      last_run_c,
        "dataset_size":    f"{dataset_size} Pertanyaan",
        "generator_model":  LLM_MODEL_NAME,
        "evaluator_model":  EVALUATOR_MODEL_NAME,
        "embedding_model":  EMBEDDING_MODEL_NAME
    }

    for config_label in ["a", "b", "c"]:
        csv_path = EVAL_RESULTS_DIR / f"hasil_config_{config_label}.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "response_time_seconds"]
            stats = {}
            for m in metrics:
                if m in df.columns:
                    mean_val = df[m].mean()
                    std_val = df[m].std()
                    min_val = df[m].min()
                    max_val = df[m].max()
                    
                    stats[m] = {
                        "mean": None if pd.isna(mean_val) else round(mean_val, 4),
                        "std":  None if pd.isna(std_val) else round(std_val, 4),
                        "min":  None if pd.isna(min_val) else round(min_val, 4),
                        "max":  None if pd.isna(max_val) else round(max_val, 4),
                    }
            result["configs"][config_label] = stats

    # Wilcoxon results
    wilcoxon_path = EVAL_RESULTS_DIR / "statistical_test.csv"
    if wilcoxon_path.exists():
        df_w = pd.read_csv(wilcoxon_path)
        for _, row in df_w.iterrows():
            stat_val = row.get("wilcoxon_statistic")
            p_val = row.get("p_value")
            winner_val = row.get("winner")
            sig_val = row.get("significant_at_0.05")
            
            result["wilcoxon"][row["metric"]] = {
                "statistic": None if pd.isna(stat_val) else stat_val,
                "p_value":   None if pd.isna(p_val) else p_val,
                "significant": False if pd.isna(sig_val) else bool(sig_val),
                "winner":    "Tidak signifikan" if pd.isna(winner_val) or winner_val == "Tidak signifikan" else winner_val,
            }

    # Audit log (5 transaksi terakhir)
    from src.config import CHAT_LOG_PATH
    if CHAT_LOG_PATH.exists():
        df_audit = pd.read_csv(CHAT_LOG_PATH)
        # Mengganti NaN dengan None agar tidak merusak serialisasi JSON (D-A7)
        df_audit = df_audit.astype(object).where(pd.notnull(df_audit), None)
        result["audit_log"] = df_audit.tail(5).to_dict(orient="records")
    else:
        result["audit_log"] = []

    # Consistency warning check
    manifest = _load_manifest()
    runs = manifest.get("runs", [])
    active_b = next((r for r in runs if r.get("is_active") and str(r.get("config", "")).lower() == "b"), None)
    active_c = next((r for r in runs if r.get("is_active") and str(r.get("config", "")).lower() == "c"), None)

    consistency_warning = {
        "has_warning": False,
        "message": "",
        "details": []
    }

    if active_b and active_c:
        diff_details = []
        if active_b.get("generator_model") != active_c.get("generator_model"):
            diff_details.append(
                f"Model generator berbeda: Config B ({active_b.get('generator_model')}) vs Config C ({active_c.get('generator_model')})"
            )
        if active_b.get("evaluator_model") != active_c.get("evaluator_model"):
            diff_details.append(
                f"Model evaluator berbeda: Config B ({active_b.get('evaluator_model')}) vs Config C ({active_c.get('evaluator_model')})"
            )
        if active_b.get("ground_truth_hash") != active_c.get("ground_truth_hash"):
            diff_details.append(
                f"Ground truth hash berbeda: Config B ({active_b.get('ground_truth_hash')}) vs Config C ({active_c.get('ground_truth_hash')})"
            )

        if diff_details:
            consistency_warning["has_warning"] = True
            consistency_warning["message"] = "Model generator/evaluator atau dataset ground truth antara Config B dan C tidak identik. Perbandingan mungkin tidak sebanding secara ilmiah."
            consistency_warning["details"] = diff_details

    result["consistency_warning"] = consistency_warning

    return JSONResponse(result)


@app.get("/dev", response_class=HTMLResponse)
async def dev_page():
    dev_html = ROOT_DIR / "static" / "dev.html"
    if not dev_html.exists():
        raise HTTPException(status_code=404, detail="Dev page not found")
    return HTMLResponse(content=dev_html.read_text(encoding="utf-8"))



# ── Developer Endpoints ────────────────────────────────────────────────────────

@app.get("/api/dev/status")
async def dev_status():
    """
    Kembalikan status sistem developer (models, API keys, index status).
    """
    google_key_present = bool(GOOGLE_API_KEY)
    nim_key_present = bool(NVIDIA_NIM_API_KEY or os.getenv("NVIDIA_NIM_API_KEY"))

    chromadb_config_b_chunks = 0
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(CHROMA_DIR_B))
        collection = client.get_collection(name=CHROMA_COLLECTION_B)
        chromadb_config_b_chunks = collection.count()
    except Exception as e:
        logger.warning(f"Gagal membaca ChromaDB collection count: {e}")
        chromadb_config_b_chunks = 0

    meta_path = CHROMA_DIR_B / ".ingestion_meta.json"
    chromadb_config_b_meta = None
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                chromadb_config_b_meta = json.load(f)
        except Exception as e:
            logger.warning(f"Gagal membaca .ingestion_meta.json: {e}")
            chromadb_config_b_meta = None

    bm25_present = BM25_INDEX_PATH.exists()

    global _ACTIVE_DEV_MODEL
    return JSONResponse({
        "available_models": AVAILABLE_MODELS,
        "active_generator": _ACTIVE_DEV_MODEL if _ACTIVE_DEV_MODEL else LLM_MODEL_NAME,
        "active_evaluator": EVALUATOR_MODEL_NAME,
        "active_embedding": EMBEDDING_MODEL_NAME,
        "google_api_key_present": google_key_present,
        "nvidia_nim_api_key_present": nim_key_present,
        "chromadb_config_b_chunks": chromadb_config_b_chunks,
        "chromadb_config_b_meta": chromadb_config_b_meta,
        "bm25_index_present": bm25_present,
    })


@app.get("/api/dev/preflight")
def dev_preflight():
    """
    Menjalankan preflight check untuk memastikan ketersediaan API Google, Generator, dan Evaluator.
    """
    res = preflight_check(
        require_google=True,
        require_nim=False,
        generator_model=LLM_MODEL_NAME,
        evaluator_model=EVALUATOR_MODEL_NAME,
    )
    return JSONResponse(res)


@app.get("/api/dev/runs")
async def dev_runs():
    """
    Membaca dan mengembalikan daftar riwayat pengujian dari run_manifest.json.
    """
    manifest = _load_manifest()
    return JSONResponse(manifest)


@app.post("/api/dev/runs/activate")
async def dev_activate_run(request: ActivateRunRequest):
    """
    Mengaktifkan hasil pengujian tertentu dari arsip manifest.
    """
    manifest = _load_manifest()
    runs = manifest.get("runs", [])

    target_run = None
    for run in runs:
        if run.get("run_id") == request.run_id:
            target_run = run
            break

    if not target_run:
        raise HTTPException(
            status_code=404,
            detail=f"Run ID '{request.run_id}' tidak ditemukan di manifest."
        )

    archive_rel_path = target_run.get("archive_file")
    if not archive_rel_path:
        raise HTTPException(
            status_code=404,
            detail=f"Run ID '{request.run_id}' tidak memiliki file arsip."
        )

    archive_file_path = Path(archive_rel_path)
    if not archive_file_path.is_absolute():
        archive_file_path = ROOT_DIR / archive_file_path

    if not archive_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File arsip tidak ditemukan: {archive_file_path}"
        )

    config = target_run.get("config", "b")
    dest_file = EVAL_RESULTS_DIR / f"hasil_config_{config}.csv"

    try:
        shutil.copy2(archive_file_path, dest_file)
    except Exception as e:
        logger.error(f"Gagal menyalin file arsip {archive_file_path} ke {dest_file}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Gagal mengaktifkan hasil pengujian: {e}"
        )

    for run in runs:
        if run.get("config") == config:
            if run.get("run_id") == request.run_id:
                run["is_active"] = True
            else:
                run["is_active"] = False

    _save_manifest(manifest)

    return JSONResponse({
        "status": "success",
        "activated_run": target_run,
    })


@app.get("/api/dev/logs")
async def dev_logs(lines: int = Query(default=50, ge=1)):
    """
    Membaca N baris terakhir dari log sistem (unsrat_rag.log).
    """
    log_lines = tail_log_file(SYSTEM_LOG_PATH, n_lines=lines)
    return JSONResponse({
        "log_path": str(SYSTEM_LOG_PATH),
        "total_lines_returned": len(log_lines),
        "lines": log_lines,
    })


@app.post("/api/dev/test_model")
async def dev_test_model(request: ModelTestRequest):
    """Test model dengan get_response dan ukur latency."""
    import time
    start = time.time()
    try:
        res = get_response(
            query="Halo, ini tes.",
            config="b",
            chat_history=[],
            model_name=request.model_name,
            streaming=False
        )
        res_text = res.get("answer", "")
    except Exception as e:
        logger.error(f"Error dev_test_model: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    latency_ms = int((time.time() - start) * 1000)
    return JSONResponse({
        "model": request.model_name,
        "response": res_text,
        "latency_ms": latency_ms
    })


@app.post("/api/dev/set_model")
async def dev_set_model(request: ModelSetRequest):
    """Set active dev model di memory (app.py)."""
    global _ACTIVE_DEV_MODEL
    _ACTIVE_DEV_MODEL = request.model_name
    logger.info(f"Set active dev model to: {_ACTIVE_DEV_MODEL}")
    return JSONResponse({"status": "success", "active_model": _ACTIVE_DEV_MODEL})


@app.get("/api/dev/chunks")
async def dev_chunks(index: int = 1, config: str = "b"):
    """Lihat raw chunk dari ChromaDB atau BM25."""
    import pickle
    if index < 1:
        raise HTTPException(status_code=400, detail="Index must be >= 1")
        
    if config == "b":
        try:
            import chromadb
            client = chromadb.PersistentClient(path=str(CHROMA_DIR_B))
            collection = client.get_collection(name=CHROMA_COLLECTION_B)
            # Deterministic ordering by sorting IDs
            all_ids = collection.get(include=[])["ids"]
            sorted_ids = sorted(all_ids, key=lambda x: int(x.split('_')[-1]) if '_' in x and x.split('_')[-1].isdigit() else x)
            if index > len(sorted_ids):
                raise HTTPException(status_code=404, detail="Chunk not found")
            
            target_id = sorted_ids[index-1]
            results = collection.get(ids=[target_id])
            
            if not results["documents"]:
                raise HTTPException(status_code=404, detail="Chunk not found")
            return JSONResponse({
                "index": index,
                "content": results["documents"][0],
                "metadata": results["metadatas"][0] if results["metadatas"] else {}
            })
        except Exception as e:
            logger.error(f"Error fetching chunk from ChromaDB: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    elif config == "c":
        try:
            if not BM25_INDEX_PATH.exists():
                raise HTTPException(status_code=404, detail="BM25 index not found")
            with open(BM25_INDEX_PATH, "rb") as f:
                data = pickle.load(f)
            chunks = data.get("chunks", [])
            if index > len(chunks):
                raise HTTPException(status_code=404, detail="Chunk not found")
            chunk = chunks[index-1]
            return JSONResponse({
                "index": index,
                "content": chunk.get("content", ""),
                "metadata": {k: v for k, v in chunk.items() if k != "content"}
            })
        except Exception as e:
            logger.error(f"Error fetching chunk from BM25: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid config. Use 'b' or 'c'.")


@app.get("/api/dev/retrieval_test")
async def dev_retrieval_test(query: str, config: str = "b"):
    """Coba fungsi retrieval tanpa memanggil LLM."""
    from src.retriever import retrieve_chunks
    try:
        chunks = retrieve_chunks(query, config)
        return JSONResponse({
            "query": query,
            "config": config,
            "results": chunks
        })
    except Exception as e:
        logger.error(f"Error dev_retrieval_test: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Static Files & Root ────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve demo UNSRAT replica homepage."""
    index_path = Path("static/demo/index.html")
    if not index_path.exists():
        return HTMLResponse("<h1>Frontend demo belum tersedia. Buat static/demo/index.html.</h1>")
    return FileResponse(index_path, media_type="text/html")


@app.get("/testing")
async def testing():
    """Serve initial SPA frontend for testing & debugging."""
    testing_path = Path("static/index.html")
    if not testing_path.exists():
        return HTMLResponse("<h1>Frontend testing tidak ditemukan di static/index.html.</h1>")
    return FileResponse(testing_path, media_type="text/html")


@app.get("/evaluation")
async def evaluation():
    """Serve standalone RAGAS evaluation page."""
    eval_path = Path("static/demo/evaluation.html")
    if not eval_path.exists():
        return HTMLResponse("<h1>Halaman evaluasi belum tersedia. Buat static/demo/evaluation.html.</h1>")
    return FileResponse(eval_path, media_type="text/html")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Memulai server UNSRAT RAG di http://{API_HOST}:{API_PORT}")
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=False)

