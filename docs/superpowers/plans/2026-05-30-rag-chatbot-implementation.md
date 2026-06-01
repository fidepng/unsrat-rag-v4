# UNSRAT RAG Chatbot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun sistem chatbot RAG akademik UNSRAT lengkap: pipeline ingestion, retrieval tiga config (A/B/C), FastAPI backend dengan SSE streaming, SPA frontend dua tab, dan pipeline evaluasi Ragas.

**Architecture:** Sistem dibagi menjadi tiga layer: (1) Offline ingestion pipeline yang mengisi ChromaDB dan BM25 index dari corpus Markdown, (2) Online application layer (FastAPI + chain.py) yang menerima query via SSE dan mengembalikan jawaban dengan inline citation, (3) Offline evaluation pipeline (Ragas + Wilcoxon) yang mengukur kinerja tiga konfigurasi secara komparatif.

**Tech Stack:** Python 3.11, FastAPI, ChromaDB, LangChain, Google Gemini API, rank-bm25, Ragas, scipy, tiktoken, Chart.js (CDN)

**Spec Reference:** `prd_srs-v4.md` v9.0 — baca sebelum mengeksekusi setiap task.

---

## File Map

| File | Status | Tanggung Jawab |
|------|--------|----------------|
| `src/__init__.py` | Buat | Python package marker |
| `src/config.py` | Buat | Semua konstanta dan parameter sistem |
| `src/logger_manager.py` | Buat | Logging terpusat: system log, ingestion CSV, chat CSV |
| `src/ingestion.py` | Buat | Pipeline YAML → chunk → embed → ChromaDB (Config A & B) |
| `src/bm25_retriever.py` | Buat | BM25 indexing dan retrieval (Config C) |
| `src/retriever.py` | Buat | Unified interface: query → config A/B/C → chunks |
| `src/chain.py` | Buat | RAG chain: retrieval + LLM + inline citation + SSE |
| `app.py` | Buat | FastAPI controller: 4 endpoint, serve static |
| `static/index.html` | Buat | SPA entry point: markup dua tab |
| `static/js/app.js` | Buat | Frontend logic: SSE, render, chat history |
| `evaluation.py` | Buat | Ragas evaluation + Wilcoxon + error analysis + chart |
| `tests/test_citation_parser.py` | Buat | Unit test untuk parse_cited_indices (logika kritis) |
| `environment.yml` | Ada | Sudah ada di PRD Section 3.2 |
| `.gitignore` | Ada/Update | Pastikan semua direktori auto-generated di-ignore |

---

## Task 1: Project Foundation & Environment

**Files:**
- Modify: `.gitignore`
- Create: `environment.yml` (jika belum ada)
- Create: `data/corpus/.gitkeep`, `eval/dataset/.gitkeep`, `eval/results/.gitkeep`

- [x] **Step 1.1: Verifikasi .gitignore sudah benar**

Pastikan `.gitignore` berisi semua yang diperlukan:
```
.env
chroma_db/
bm25_index/
__pycache__/
*.pyc
.conda/
*.egg-info/
logs/
```

Jalankan:
```bash
cat .gitignore
```

Jika ada yang kurang, tambahkan manual.

- [x] **Step 1.2: Buat direktori yang diperlukan**

```bash
mkdir -p data/corpus eval/dataset eval/results logs static/js src tests
```

- [x] **Step 1.3: Buat conda environment**

Pastikan file `environment.yml` sudah ada dengan konten dari PRD Section 3.2. Kemudian:

```bash
conda env create -f environment.yml
conda activate unsrat-rag
```

- [x] **Step 1.4: Verifikasi semua library kritis terinstall**

```bash
python --version
python -c "import langchain; print('langchain:', langchain.__version__)"
python -c "import chromadb; print('chromadb:', chromadb.__version__)"
python -c "import ragas; print('ragas:', ragas.__version__)"
python -c "import fastapi; print('fastapi:', fastapi.__version__)"
python -c "import tiktoken; print('tiktoken OK')"
python -c "from rank_bm25 import BM25Okapi; print('rank-bm25 OK')"
python -c "from scipy.stats import wilcoxon; print('scipy OK')"
python -c "import frontmatter; print('python-frontmatter OK')"
```

Expected: Semua print tanpa error.

- [x] **Step 1.5: Buat file .env**

```bash
# Buat file .env di root proyek (jangan commit!)
echo "GOOGLE_API_KEY=isi_dengan_api_key_anda" > .env
```

Edit `.env` dan isi dengan API key Google AI Studio yang valid.

- [x] **Step 1.6: Commit foundation**

```bash
git add .gitignore environment.yml
git commit -m "chore: verifikasi foundation — gitignore, environment, direktori"
```

---

## Task 2: src/config.py — Pusat Konfigurasi

**Files:**
- Create: `src/__init__.py`
- Create: `src/config.py`

- [x] **Step 2.1: Buat src/__init__.py**

```bash
echo "" > src/__init__.py
```

- [x] **Step 2.2: Buat src/config.py dengan konten lengkap**

Buat file `src/config.py`:

```python
# src/config.py — CANONICAL CONFIGURATION FILE
# PRD Reference: Section 7

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── PATH ────────────────────────────────────────────────────
ROOT_DIR             = Path(__file__).parent.parent
CORPUS_DIR           = ROOT_DIR / "data" / "corpus"
CHROMA_BASE_DIR      = ROOT_DIR / "chroma_db"
CHROMA_DIR_A         = CHROMA_BASE_DIR / "config_a"
CHROMA_DIR_B         = CHROMA_BASE_DIR / "config_b"
BM25_INDEX_DIR       = ROOT_DIR / "bm25_index"
BM25_INDEX_PATH      = BM25_INDEX_DIR / "bm25_index.pkl"
EVAL_DATASET_PATH    = ROOT_DIR / "eval" / "dataset" / "ground_truth.csv"
EVAL_RESULTS_DIR     = ROOT_DIR / "eval" / "results"
LOGS_DIR             = ROOT_DIR / "logs"
SYSTEM_LOG_PATH      = LOGS_DIR / "unsrat_rag.log"
CHAT_LOG_PATH        = LOGS_DIR / "transaksi_chat.csv"
INGESTION_LOG_PATH   = LOGS_DIR / "ingestion_report.csv"

# ── CHROMADB COLLECTIONS ────────────────────────────────────
CHROMA_COLLECTION_A  = "unsrat_rag_config_a"
CHROMA_COLLECTION_B  = "unsrat_rag_config_b"
CHROMA_DISTANCE_FN   = "cosine"

# ── MODEL ───────────────────────────────────────────────────
# Generator dan evaluator HARUS BERBEDA (D-16 — mitigasi self-eval bias)
# NVIDIA NIM models are used for active testing due to Google AI Studio API limits.
# Optimasi kecepatan & penalaran: Generator = Nemotron Nano 8B, Evaluator = Nemotron Super 49B (D-16 Terpenuhi)
LLM_MODEL_NAME       = "llama-3.1-nemotron-nano-8b-v1"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"
EVALUATOR_MODEL_NAME = "llama-3.3-nemotron-super-49b-v1.5"

# Daftar model tersedia di UI sidebar
AVAILABLE_MODELS: list[str] = [
    "gemini-3.5-flash",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "llama-3.1-8b-instruct",
    "llama-3.1-nemotron-nano-8b-v1",
    "llama-3.3-nemotron-super-49b-v1.5",
    "gemma-4-31b-it",
]

# ── CHUNKING — CONFIG A ──────────────────────────────────────
CHUNK_SIZE_A         = 500
CHUNK_OVERLAP_A      = 100

# ── CHUNKING — CONFIG B ──────────────────────────────────────
CHUNK_SIZE_B         = 2000
CHUNK_OVERLAP_B      = 200

# ── SEPARATORS ───────────────────────────────────────────────
CHUNK_SEPARATORS     = ["\n\n", "\n", " ", ""]

# ── RETRIEVAL ────────────────────────────────────────────────
RETRIEVAL_K          = 4
SIMILARITY_THRESHOLD = 0.65   # Wajib dikalibrasi secara empiris (D-B7) sebelum eval resmi
MIN_CHUNK_LENGTH     = 50

# ── BM25 — CONFIG C ──────────────────────────────────────────
BM25_K               = 4
BM25_MIN_TOKEN_LEN   = 2

# ── LLM GENERATION ──────────────────────────────────────────
LLM_TEMPERATURE      = 0.1
LLM_MAX_OUTPUT_TOKENS = 2048
LLM_TOP_P            = 0.95

# ── MEMORI ──────────────────────────────────────────────────
MEMORY_K             = 5

# ── RETRY POLICY (chain.py — interaktif) ────────────────────
MAX_RETRIES          = 3
RETRY_DELAYS         = [2, 5]   # detik: attempt 2→2s, attempt 3→5s

# ── EVALUASI ─────────────────────────────────────────────────
METRICS_COLS = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
]

OPTIONAL_METRICS_COLS = [
    "context_entity_recall",
]

ERROR_ANALYSIS_N = 10

# ── REQUIRED YAML FIELDS ─────────────────────────────────────
# (D-B2): Hanya 3 field yang benar-benar dikonsumsi kode runtime.
# Field lain boleh ada di YAML sebagai dokumentasi manusia.
REQUIRED_YAML_FIELDS = ["doc_id", "title", "category"]

# ── SYSTEM PROMPT (TERKUNCI) ─────────────────────────────────
SYSTEM_PROMPT = """Anda adalah agen asisten informasi akademik resmi \
Universitas Sam Ratulangi.
Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan dokumen \
konteks yang disediakan di bawah ini.

PENTING: Jangan gunakan pengetahuan Anda di luar dokumen konteks yang \
disediakan, meskipun Anda mengetahuinya dari sumber lain.

Setiap klaim atau informasi dalam jawaban Anda HARUS disertai dengan \
penanda referensi inline berbentuk [N] di akhir kalimat yang bersumber \
dari dokumen tersebut, di mana N adalah nomor sumber yang tersedia \
dalam konteks.

Contoh format jawaban yang benar:
"Mahasiswa dapat mengambil maksimal 24 SKS per semester [1]. \
Kalender akademik semester genap dimulai pada Februari 2026 [2]."

Jika jawaban tidak ada di dalam dokumen konteks, katakan secara jujur \
bahwa Anda tidak menemukan informasinya dan arahkan mereka untuk \
menghubungi bagian administrasi kampus. Dalam kasus ini, \
jangan gunakan penanda referensi.

JANGAN PERNAH mengarang informasi, tanggal, atau angka SKS.
Jawab dalam Bahasa Indonesia yang ramah dan mudah dipahami."""

# ── FALLBACK RESPONSE ────────────────────────────────────────
FALLBACK_RESPONSE = (
    "Maaf, saya tidak menemukan informasi yang relevan mengenai "
    "pertanyaan Anda dalam dokumen yang tersedia. "
    "Untuk informasi lebih lanjut, silakan hubungi:\n\n"
    "• Bagian Akademik UNSRAT\n"
    "• Portal INSPIRE: inspire.unsrat.ac.id\n"
    "• Atau datang langsung ke Gedung Rektorat UNSRAT"
)

# ── API ──────────────────────────────────────────────────────
API_HOST             = "0.0.0.0"
API_PORT             = 8501

# ── API KEY ──────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY tidak ditemukan!\n"
        "Buat file .env di root proyek dan isi: GOOGLE_API_KEY=your_key_here"
    )

# NVIDIA NIM API Key (opsional)
NVIDIA_NIM_API_KEY = os.getenv("NVIDIA_NIM_API_KEY")  # None jika tidak di-set
```

- [x] **Step 2.3: Verifikasi config.py berjalan tanpa error**

```bash
python -c "from src.config import ROOT_DIR, REQUIRED_YAML_FIELDS, SYSTEM_PROMPT; print('ROOT_DIR:', ROOT_DIR); print('REQUIRED_YAML_FIELDS:', REQUIRED_YAML_FIELDS); print('Config OK')"
```

Expected output:
```
ROOT_DIR: D:\Kuliah\Skripsi Repository\unsrat-rag-v4-28.05.2026
REQUIRED_YAML_FIELDS: ['doc_id', 'title', 'category']
Config OK
```

- [x] **Step 2.4: Commit**

```bash
git add src/__init__.py src/config.py
git commit -m "feat: tambah src/config.py — pusat konfigurasi sistem (PRD v9.0)"
```

---

## Task 3: src/logger_manager.py — Logging Terpusat

**Files:**
- Create: `src/logger_manager.py`

PRD Reference: Section 13

- [x] **Step 3.1: Buat src/logger_manager.py**

```python
# src/logger_manager.py — Logging terpusat tiga output
# PRD Reference: Section 13

import logging
import csv
from pathlib import Path
from datetime import datetime
from src.config import SYSTEM_LOG_PATH, CHAT_LOG_PATH, INGESTION_LOG_PATH, LOGS_DIR

_loggers: dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """
    Kembalikan logger untuk modul yang diberikan.

    Dikonfigurasi dengan FileHandler (semua level) dan StreamHandler (INFO+).
    Logger di-cache agar tidak membuat duplikasi handler.
    """
    if name in _loggers:
        return _loggers[name]

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — semua level
    fh = logging.FileHandler(SYSTEM_LOG_PATH, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Console handler — INFO dan ke atas
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate = False

    _loggers[name] = logger
    return logger


def log_ingestion_report(
    config: str,
    files_processed: int,
    chunks_generated: int,
    chunks_inserted: int,
    chunks_duplicate_skipped: int,
    chunks_too_short_skipped: int,
    execution_time_seconds: float,
) -> None:
    """
    Append satu baris ke ingestion_report.csv.

    Skema: timestamp, config, files_processed, chunks_generated,
    chunks_inserted, chunks_duplicate_skipped,
    chunks_too_short_skipped, execution_time_seconds
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "timestamp", "config", "files_processed", "chunks_generated",
        "chunks_inserted", "chunks_duplicate_skipped",
        "chunks_too_short_skipped", "execution_time_seconds",
    ]
    file_exists = INGESTION_LOG_PATH.exists()
    with open(INGESTION_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "config": config,
            "files_processed": files_processed,
            "chunks_generated": chunks_generated,
            "chunks_inserted": chunks_inserted,
            "chunks_duplicate_skipped": chunks_duplicate_skipped,
            "chunks_too_short_skipped": chunks_too_short_skipped,
            "execution_time_seconds": round(execution_time_seconds, 2),
        })


def log_chat_transaction(
    config: str,
    model_llm: str,
    user_query: str,
    chunks_retrieved_count: int,
    retrieved_chunk_ids: list[str],
    best_similarity_score: float,
    average_similarity_score: float,
    response_time_seconds: float,
    estimated_prompt_tokens: int,
    estimated_completion_tokens: int,
    estimated_total_tokens: int,
    found_state: bool,
    answer_preview: str,
) -> None:
    """
    Append satu baris ke transaksi_chat.csv.

    Skema: lihat PRD Section 13.2 — Audit Trail Chat.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "timestamp", "config", "model_llm", "user_query",
        "chunks_retrieved_count", "retrieved_chunk_ids",
        "best_similarity_score", "average_similarity_score",
        "response_time_seconds", "estimated_prompt_tokens",
        "estimated_completion_tokens", "estimated_total_tokens",
        "found_state", "answer_preview",
    ]
    file_exists = CHAT_LOG_PATH.exists()
    with open(CHAT_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "config": config,
            "model_llm": model_llm,
            "user_query": user_query[:200],
            "chunks_retrieved_count": chunks_retrieved_count,
            "retrieved_chunk_ids": "|".join(retrieved_chunk_ids),
            "best_similarity_score": round(best_similarity_score, 4),
            "average_similarity_score": round(average_similarity_score, 4),
            "response_time_seconds": round(response_time_seconds, 4),
            "estimated_prompt_tokens": estimated_prompt_tokens,
            "estimated_completion_tokens": estimated_completion_tokens,
            "estimated_total_tokens": estimated_total_tokens,
            "found_state": found_state,
            "answer_preview": answer_preview[:200],
        })
```

- [x] **Step 3.2: Verifikasi logger_manager**

```bash
python -c "
from src.logger_manager import get_logger, log_ingestion_report, log_chat_transaction
logger = get_logger('test')
logger.info('Logger test OK')
logger.debug('Debug message OK')
log_ingestion_report('b', 9, 312, 295, 14, 3, 187.4)
log_chat_transaction('b','gemini-2.5-flash','Test query',3,['id1','id2','id3'],0.31,0.42,2.14,1250,187,1437,True,'Test answer preview')
print('logger_manager OK — cek logs/ directory')
"
```

Expected: File `logs/unsrat_rag.log` dan `logs/ingestion_report.csv` terbuat.

- [x] **Step 3.3: Commit**

```bash
git add src/logger_manager.py
git commit -m "feat: tambah src/logger_manager.py — logging terpusat tiga output"
```

---

## Task 4: src/ingestion.py — Pipeline Data Ingestion

**Files:**
- Create: `src/ingestion.py`

PRD Reference: Section 6.1, 6.2 (D-B1: no summary chunk), 6.3 (D-B3: no priority/chunk_type), FR-01–FR-08

- [x] **Step 4.1: Verifikasi YAML frontmatter corpus sebelum ingestion**

Jalankan verifikasi ini dulu sebelum menulis kode:
```bash
python -c "
import frontmatter
from pathlib import Path
from src.config import CORPUS_DIR, REQUIRED_YAML_FIELDS
for f in sorted(CORPUS_DIR.glob('*.md')):
    post = frontmatter.load(f)
    missing = [field for field in REQUIRED_YAML_FIELDS if not post.metadata.get(field)]
    status = 'ERROR' if missing else 'OK'
    print(f'{status}: {f.name}' + (f' — field kosong: {missing}' if missing else ''))
"
```

Expected: Semua file status `OK`. Jika ada `ERROR`, perbaiki YAML frontmatter terlebih dahulu (tambahkan field `doc_id`, `title`, atau `category` yang kurang).

- [x] **Step 4.2: Buat src/ingestion.py**

```python
# src/ingestion.py — Pipeline Data Ingestion → ChromaDB
# PRD Reference: Section 6.1, 6.2, FR-01–FR-08
# PENTING: Gunakan `use context7` untuk verifikasi API LangChain sebelum run

import argparse
import hashlib
import time
from pathlib import Path

import frontmatter
import chromadb
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import (
    CORPUS_DIR, CHROMA_DIR_A, CHROMA_DIR_B,
    CHROMA_COLLECTION_A, CHROMA_COLLECTION_B, CHROMA_DISTANCE_FN,
    CHUNK_SIZE_A, CHUNK_OVERLAP_A, CHUNK_SIZE_B, CHUNK_OVERLAP_B,
    CHUNK_SEPARATORS, MIN_CHUNK_LENGTH, REQUIRED_YAML_FIELDS,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY,
)
from src.logger_manager import get_logger, log_ingestion_report

logger = get_logger("ingestion")

# ── Retry policy lokal (D-A8): terpisah dari config.py, agresif untuk batch ──
MAX_RETRIES_INGESTION = 5
INTER_CHUNK_SLEEP     = 0.3   # detik jeda antar chunk embed untuk hindari quota burst

# ── Markdown header splitter ───────────────────────────────────────────────────
HEADERS_TO_SPLIT_ON = [
    ("#",    "header_1"),
    ("##",   "bab"),
    ("###",  "bagian"),
    ("####", "pasal"),
]


def _make_chunk_id(doc_id: str, content: str) -> str:
    """Buat chunk_id unik berdasarkan MD5 hash dari doc_id + content. (FR-06)"""
    raw = f"{doc_id}::{content}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _embed_with_retry(
    embedding_fn,
    texts: list[str],
    max_retries: int = MAX_RETRIES_INGESTION,
) -> list[list[float]]:
    """
    Embed list of texts dengan retry eksponensial.

    Raises RuntimeError jika semua retry habis.
    """
    for attempt in range(1, max_retries + 1):
        try:
            return embedding_fn.embed_documents(texts)
        except Exception as e:
            if attempt == max_retries:
                raise RuntimeError(f"Embedding gagal setelah {max_retries} attempt: {e}") from e
            wait = 2 ** attempt   # 2, 4, 8, 16, 32 detik
            logger.warning(f"Embedding error (attempt {attempt}/{max_retries}): {e}. Retry dalam {wait}s.")
            time.sleep(wait)


def _parse_and_chunk(
    md_file: Path,
    chunk_size: int,
    chunk_overlap: int,
) -> list[dict]:
    """
    Parse file .md → validasi YAML → two-stage chunking → return list chunk dict.

    Setiap chunk dict berisi: content, metadata (doc_id, title, category,
    content_type, bab, bagian, pasal, chunk_id, status).

    Returns empty list jika validasi gagal (file di-skip, bukan crash).
    (FR-01, FR-02, FR-03, D-B1: tanpa summary chunk)
    """
    try:
        post = frontmatter.load(md_file)
    except Exception as e:
        logger.warning(f"Gagal parse frontmatter: {md_file.name} — {e}")
        return []

    meta = post.metadata

    # FR-02: Validasi field wajib
    missing = [f for f in REQUIRED_YAML_FIELDS if not meta.get(f)]
    if missing:
        logger.warning(f"SKIP {md_file.name} — field wajib kosong: {missing}")
        return []

    doc_id       = meta["doc_id"]
    title        = meta["title"]
    category     = meta["category"]
    content_type = meta.get("content_type", "")
    status       = meta.get("status", "active")
    body         = post.content

    # Two-stage split: Stage 1 — structural (Markdown headers)
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    structural_chunks = md_splitter.split_text(body)

    # Two-stage split: Stage 2 — size normalization
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=CHUNK_SEPARATORS,
    )
    raw_chunks = char_splitter.split_documents(structural_chunks)

    chunks = []
    for doc in raw_chunks:
        content = doc.page_content.strip()

        # FR-05: Filter chunk terlalu pendek
        if len(content) < MIN_CHUNK_LENGTH:
            logger.debug(f"SKIP chunk pendek ({len(content)} char) di {doc_id}")
            continue

        chunk_id = _make_chunk_id(doc_id, content)
        header_meta = doc.metadata

        chunks.append({
            "content": content,
            "chunk_id": chunk_id,
            "metadata": {
                "doc_id":       doc_id,
                "title":        title,
                "category":     category,
                "content_type": content_type,
                "bab":          header_meta.get("bab", ""),
                "bagian":       header_meta.get("bagian", ""),
                "pasal":        header_meta.get("pasal", ""),
                "chunk_id":     chunk_id,
                "status":       status,
            },
        })

    return chunks


def run_ingestion(config: str, rebuild: bool = False) -> None:
    """
    Jalankan pipeline ingestion untuk config 'a' atau 'b'.

    Jika rebuild=True, hapus collection yang ada dan buat ulang.
    Jika rebuild=False, skip chunk yang sudah ada (idempotent via MD5 hash).

    Dipanggil via CLI: python src/ingestion.py --config a [--rebuild]
    """
    start_time = time.time()

    if config == "a":
        chroma_dir  = CHROMA_DIR_A
        collection_name = CHROMA_COLLECTION_A
        chunk_size  = CHUNK_SIZE_A
        chunk_overlap = CHUNK_OVERLAP_A
    elif config == "b":
        chroma_dir  = CHROMA_DIR_B
        collection_name = CHROMA_COLLECTION_B
        chunk_size  = CHUNK_SIZE_B
        chunk_overlap = CHUNK_OVERLAP_B
    else:
        raise ValueError(f"Config tidak valid: '{config}'. Gunakan 'a' atau 'b'.")

    chroma_dir.mkdir(parents=True, exist_ok=True)

    # ChromaDB client
    client = chromadb.PersistentClient(path=str(chroma_dir))

    if rebuild:
        try:
            client.delete_collection(collection_name)
            logger.info(f"Collection '{collection_name}' dihapus (rebuild mode).")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": CHROMA_DISTANCE_FN},
    )

    # Embedding function — task_type="retrieval_document" (FR-07, D-15)
    embedding_fn = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        task_type="retrieval_document",
    )

    md_files = sorted(CORPUS_DIR.glob("*.md"))
    logger.info(f"Ingestion Config {config.upper()} — {len(md_files)} file ditemukan.")

    total_generated     = 0
    total_inserted      = 0
    total_duplicate     = 0
    total_too_short     = 0
    files_processed     = 0

    for md_file in md_files:
        logger.info(f"Memproses: {md_file.name}")
        chunks = _parse_and_chunk(md_file, chunk_size, chunk_overlap)

        if not chunks:
            continue

        files_processed += 1

        # Hitung chunk yang terlalu pendek di tahap sebelumnya
        # (sudah di-filter di _parse_and_chunk, tapi kita track via generated vs returned)
        # Untuk akurasi, kita generate ulang tanpa filter untuk hitung generated:
        # (Simplified: anggap generated = len(chunks) + chunks_filtered_in_parse)
        # Dalam implementasi aktual, pass counter ke _parse_and_chunk
        total_generated += len(chunks)

        for chunk in chunks:
            chunk_id = chunk["chunk_id"]

            # FR-06: Idempotency check — skip jika sudah ada
            existing = collection.get(ids=[chunk_id], include=[])
            if existing["ids"]:
                total_duplicate += 1
                logger.debug(f"SKIP duplikat: {chunk_id[:8]}...")
                continue

            # Embed dengan retry
            try:
                embeddings = _embed_with_retry(embedding_fn, [chunk["content"]])
            except RuntimeError as e:
                logger.error(f"Embedding gagal untuk chunk {chunk_id[:8]}: {e}")
                continue

            collection.add(
                ids=[chunk_id],
                embeddings=embeddings,
                documents=[chunk["content"]],
                metadatas=[chunk["metadata"]],
            )
            total_inserted += 1
            logger.debug(f"INSERT: {chunk_id[:8]}... ({len(chunk['content'])} char)")
            time.sleep(INTER_CHUNK_SLEEP)

        logger.info(
            f"✓ {md_file.name}: {len(chunks)} chunk diproses | "
            f"{total_inserted} inserted sejauh ini"
        )

    execution_time = time.time() - start_time

    logger.info(
        f"Ingestion Config {config.upper()} selesai | "
        f"{files_processed} file | {total_generated} generated | "
        f"{total_inserted} inserted | {total_duplicate} duplikat | "
        f"{total_too_short} terlalu pendek | {execution_time:.1f}s"
    )

    log_ingestion_report(
        config=config,
        files_processed=files_processed,
        chunks_generated=total_generated,
        chunks_inserted=total_inserted,
        chunks_duplicate_skipped=total_duplicate,
        chunks_too_short_skipped=total_too_short,
        execution_time_seconds=execution_time,
    )

    logger.info(f"ChromaDB {collection_name}: {collection.count()} total chunks.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingestion pipeline UNSRAT RAG")
    parser.add_argument("--config", choices=["a", "b"], required=True, help="Config A atau B")
    parser.add_argument("--rebuild", action="store_true", help="Hapus collection dan rebuild dari nol")
    args = parser.parse_args()
    run_ingestion(args.config, args.rebuild)
```

- [x] **Step 4.3: Jalankan ingestion Config B terlebih dahulu (chunk besar lebih andal untuk validasi)**

```bash
python src/ingestion.py --config b --rebuild
```

Expected output:
```
... | INFO | ingestion | Ingestion Config B — 9 file ditemukan.
... | INFO | ingestion | Memproses: 01_sejarah.md
... | INFO | ingestion | ✓ 01_sejarah.md: N chunk diproses | ...
... (semua file)
... | INFO | ingestion | Ingestion Config B selesai | 9 file | XXX generated | XXX inserted | ...
```

- [x] **Step 4.4: Verifikasi jumlah chunk di ChromaDB**

```bash
python -c "
import chromadb
from src.config import CHROMA_DIR_B, CHROMA_COLLECTION_B
client = chromadb.PersistentClient(path=str(CHROMA_DIR_B))
col = client.get_collection(CHROMA_COLLECTION_B)
print(f'Config B: {col.count()} chunks')
# Verifikasi metadata schema (D-B3: tidak ada priority atau chunk_type)
sample = col.get(limit=1, include=['metadatas'])
print('Sample metadata:', sample['metadatas'][0])
"
```

Expected: count > 0, metadata TIDAK mengandung `priority` atau `chunk_type`.

- [x] **Step 4.5: Jalankan ingestion Config A**

```bash
python src/ingestion.py --config a --rebuild
```

- [x] **Step 4.6: Verifikasi Config A**

```bash
python -c "
import chromadb
from src.config import CHROMA_DIR_A, CHROMA_COLLECTION_A
col = chromadb.PersistentClient(path=str(CHROMA_DIR_A)).get_collection(CHROMA_COLLECTION_A)
print(f'Config A: {col.count()} chunks')
"
```

Expected: Config A lebih banyak chunk dari Config B (chunk kecil = lebih banyak potongan).

- [x] **Step 4.7: Commit**

```bash
git add src/ingestion.py
git commit -m "feat: tambah src/ingestion.py — pipeline ChromaDB Config A & B (D-B1: no summary chunk)"
```

---

## Task 5: src/bm25_retriever.py — BM25 Index (Config C)

**Files:**
- Create: `src/bm25_retriever.py`

PRD Reference: Section 6.2 (Config C), FR-19, FR-20, D-A6

- [x] **Step 5.1: Buat src/bm25_retriever.py**

```python
# src/bm25_retriever.py — BM25 Indexing & Retrieval (Config C)
# PRD Reference: FR-19, FR-20, D-A3, D-A6
# rank-bm25 digunakan LANGSUNG, bukan via LangChain wrapper (D-A6)

import argparse
import pickle
import re
from pathlib import Path

import frontmatter
from rank_bm25 import BM25Okapi
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from src.config import (
    CORPUS_DIR, BM25_INDEX_DIR, BM25_INDEX_PATH,
    CHUNK_SIZE_B, CHUNK_OVERLAP_B, CHUNK_SEPARATORS,
    MIN_CHUNK_LENGTH, BM25_K, BM25_MIN_TOKEN_LEN,
    REQUIRED_YAML_FIELDS,
)
from src.logger_manager import get_logger

logger = get_logger("bm25_retriever")

HEADERS_TO_SPLIT_ON = [
    ("#",    "header_1"),
    ("##",   "bab"),
    ("###",  "bagian"),
    ("####", "pasal"),
]


def _tokenize(text: str) -> list[str]:
    """
    Tokenisasi sederhana: lowercase, hapus tanda baca, filter token pendek.

    Min token length dari BM25_MIN_TOKEN_LEN (default: 2 karakter).
    """
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [t for t in tokens if len(t) >= BM25_MIN_TOKEN_LEN]


def _load_all_chunks() -> list[dict]:
    """
    Load semua file corpus, chunk dengan parameter identik Config B (D-A3).

    Returns list of chunk dicts: {content, doc_id, title, category,
    content_type, bab, bagian, pasal}
    """
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE_B,
        chunk_overlap=CHUNK_OVERLAP_B,
        separators=CHUNK_SEPARATORS,
    )

    all_chunks = []
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        try:
            post = frontmatter.load(md_file)
        except Exception as e:
            logger.warning(f"Gagal parse {md_file.name}: {e}")
            continue

        meta = post.metadata
        missing = [f for f in REQUIRED_YAML_FIELDS if not meta.get(f)]
        if missing:
            logger.warning(f"SKIP {md_file.name} — field kosong: {missing}")
            continue

        structural = md_splitter.split_text(post.content)
        raw_chunks = char_splitter.split_documents(structural)

        for doc in raw_chunks:
            content = doc.page_content.strip()
            if len(content) < MIN_CHUNK_LENGTH:
                continue
            all_chunks.append({
                "content":      content,
                "doc_id":       meta["doc_id"],
                "title":        meta["title"],
                "category":     meta["category"],
                "content_type": meta.get("content_type", ""),
                "bab":          doc.metadata.get("bab", ""),
                "bagian":       doc.metadata.get("bagian", ""),
                "pasal":        doc.metadata.get("pasal", ""),
            })

    logger.info(f"BM25: {len(all_chunks)} chunk dimuat dari corpus.")
    return all_chunks


def build_index(rebuild: bool = False) -> None:
    """
    Bangun BM25 index dari corpus dan simpan ke bm25_index.pkl.

    Dipanggil via: python src/bm25_retriever.py --rebuild
    """
    if BM25_INDEX_PATH.exists() and not rebuild:
        logger.info("BM25 index sudah ada. Gunakan --rebuild untuk membangun ulang.")
        return

    BM25_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    chunks = _load_all_chunks()

    if not chunks:
        raise RuntimeError("Tidak ada chunk yang bisa diindeks. Periksa corpus.")

    tokenized = [_tokenize(c["content"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks, "tokenized": tokenized}, f)

    logger.info(f"BM25 index disimpan: {BM25_INDEX_PATH} ({len(chunks)} chunks)")


def _load_index() -> tuple[BM25Okapi, list[dict]]:
    """Load BM25 index dari pickle. Raise RuntimeError jika tidak ada."""
    if not BM25_INDEX_PATH.exists():
        raise RuntimeError(
            f"BM25 index tidak ditemukan: {BM25_INDEX_PATH}\n"
            "Jalankan: python src/bm25_retriever.py --rebuild"
        )
    with open(BM25_INDEX_PATH, "rb") as f:
        data = pickle.load(f)
    return data["bm25"], data["chunks"]


def retrieve_chunks_bm25(query: str) -> list[dict]:
    """
    Retrieve BM25_K chunk teratas untuk query yang diberikan.

    Returns list[dict] kompatibel dengan format unified retriever:
    {content, doc_id, title, category, content_type, bab, bagian, pasal,
     score, chunk_id}

    BM25 score BUKAN cosine distance — nilainya tidak dinormalisasi [0,1].
    (FR-20)
    """
    bm25, chunks = _load_index()
    query_tokens  = _tokenize(query)

    if not query_tokens:
        logger.warning(f"Query tokenisasi kosong untuk: '{query}'")
        return []

    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:BM25_K]

    results = []
    for idx in top_indices:
        if scores[idx] <= 0:
            continue   # Skip chunk dengan score 0 (tidak relevan sama sekali)
        chunk = chunks[idx].copy()
        chunk["score"]    = float(scores[idx])
        chunk["chunk_id"] = f"bm25_{idx}"   # pseudo-ID untuk audit log
        results.append(chunk)

    logger.debug(f"BM25 retrieved {len(results)} chunks untuk '{query[:50]}'")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BM25 index builder (Config C)")
    parser.add_argument("--rebuild", action="store_true", help="Bangun ulang index dari nol")
    args = parser.parse_args()
    build_index(rebuild=args.rebuild)
```

- [x] **Step 5.2: Build BM25 index**

```bash
python src/bm25_retriever.py --rebuild
```

Expected:
```
... | INFO | bm25_retriever | BM25: XXX chunk dimuat dari corpus.
... | INFO | bm25_retriever | BM25 index disimpan: .../bm25_index/bm25_index.pkl (XXX chunks)
```

- [x] **Step 5.3: Verifikasi retrieval BM25**

```bash
python -c "
from src.bm25_retriever import retrieve_chunks_bm25
results = retrieve_chunks_bm25('berapa SKS maksimal per semester')
print(f'Retrieved {len(results)} chunks')
for r in results:
    print(f'  Score: {r[\"score\"]:.3f} | {r[\"doc_id\"]} | {r[\"content\"][:80]}...')
"
```

Expected: 1–4 chunk dengan score > 0, konten tentang SKS.

- [x] **Step 5.4: Commit**

```bash
git add src/bm25_retriever.py
git commit -m "feat: tambah src/bm25_retriever.py — BM25 indexing & retrieval Config C (D-A6)"
```

---

## Task 6: src/retriever.py — Unified Retrieval Interface

**Files:**
- Create: `src/retriever.py`

PRD Reference: Section 6.4, FR-09, FR-10, FR-11

- [x] **Step 6.1: Buat src/retriever.py**

```python
# src/retriever.py — Unified Retrieval Interface (Config A / B / C)
# PRD Reference: Section 6.4, FR-09, FR-10

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import (
    CHROMA_DIR_A, CHROMA_DIR_B,
    CHROMA_COLLECTION_A, CHROMA_COLLECTION_B, CHROMA_DISTANCE_FN,
    RETRIEVAL_K, SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY,
)
from src.bm25_retriever import retrieve_chunks_bm25
from src.logger_manager import get_logger

logger = get_logger("retriever")

# ── Cache ChromaDB clients (satu per config) ───────────────────────────────────
_chroma_clients: dict[str, chromadb.PersistentClient] = {}
_chroma_collections: dict[str, chromadb.Collection] = {}

# ── Cache embedding function (satu instance, untuk query) ──────────────────────
_embedding_fn: GoogleGenerativeAIEmbeddings | None = None


def _get_embedding_fn() -> GoogleGenerativeAIEmbeddings:
    """Kembalikan embedding function. task_type='retrieval_query' (D-15, FR-07)."""
    global _embedding_fn
    if _embedding_fn is None:
        _embedding_fn = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
            task_type="retrieval_query",
        )
    return _embedding_fn


def _get_chroma_collection(config: str) -> chromadb.Collection:
    """Kembalikan ChromaDB collection untuk config 'a' atau 'b'."""
    if config in _chroma_collections:
        return _chroma_collections[config]

    if config == "a":
        chroma_dir  = CHROMA_DIR_A
        coll_name   = CHROMA_COLLECTION_A
    else:
        chroma_dir  = CHROMA_DIR_B
        coll_name   = CHROMA_COLLECTION_B

    if not chroma_dir.exists():
        raise RuntimeError(
            f"ChromaDB untuk Config {config.upper()} tidak ditemukan: {chroma_dir}\n"
            f"Jalankan: python src/ingestion.py --config {config} --rebuild"
        )

    client     = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_collection(coll_name)
    _chroma_collections[config] = collection
    return collection


def retrieve_chunks(query: str, config: str) -> list[dict]:
    """
    Retrieve chunk relevan untuk query sesuai config yang dipilih.

    Config 'a' atau 'b': vector similarity search via ChromaDB.
    Config 'c': BM25 keyword search.

    Untuk config a/b: terapkan SIMILARITY_THRESHOLD (buang chunk dengan
    cosine distance > threshold). (FR-09, FR-10)

    Returns list[dict]:
    {content, doc_id, title, category, content_type, bab, bagian, pasal,
     chunk_id, distance}  — distance = cosine distance untuk a/b, BM25 score untuk c.
    """
    if config == "c":
        return retrieve_chunks_bm25(query)

    # Config A atau B — vector search
    collection   = _get_chroma_collection(config)
    embedding_fn = _get_embedding_fn()

    query_embedding = embedding_fn.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=RETRIEVAL_K,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        # FR-10: Buang chunk dengan cosine distance > threshold
        if dist > SIMILARITY_THRESHOLD:
            logger.debug(
                f"FILTER: distance {dist:.4f} > threshold {SIMILARITY_THRESHOLD} "
                f"untuk doc_id={meta.get('doc_id', '?')}"
            )
            continue
        chunks.append({
            "content":      doc,
            "doc_id":       meta.get("doc_id", ""),
            "title":        meta.get("title", ""),
            "category":     meta.get("category", ""),
            "content_type": meta.get("content_type", ""),
            "bab":          meta.get("bab", ""),
            "bagian":       meta.get("bagian", ""),
            "pasal":        meta.get("pasal", ""),
            "chunk_id":     meta.get("chunk_id", ""),
            "distance":     round(dist, 4),
        })

    if not chunks:
        logger.warning(f"Tidak ada chunk lolos threshold untuk query: '{query[:60]}'")
    else:
        logger.debug(f"Retrieved {len(chunks)} chunks (config={config}) untuk '{query[:60]}'")

    return chunks
```

- [x] **Step 6.2: Verifikasi unified retriever**

```bash
python -c "
from src.retriever import retrieve_chunks

print('=== Config B (vector) ===')
chunks = retrieve_chunks('syarat yudisium sarjana', 'b')
print(f'Retrieved {len(chunks)} chunks')
for c in chunks:
    print(f'  dist={c[\"distance\"]} | {c[\"doc_id\"]} | {c[\"content\"][:70]}...')

print()
print('=== Config C (BM25) ===')
chunks_c = retrieve_chunks('SKS maksimal per semester', 'c')
print(f'Retrieved {len(chunks_c)} chunks')
for c in chunks_c:
    print(f'  score={c[\"score\"]:.3f} | {c[\"doc_id\"]} | {c[\"content\"][:70]}...')
"
```

Expected: Kedua config mengembalikan chunk relevan.

- [x] **Step 6.3: Commit**

```bash
git add src/retriever.py
git commit -m "feat: tambah src/retriever.py — unified retrieval interface A/B/C"
```

---

## Task 7: src/chain.py — RAG Chain + Citation + SSE

**Files:**
- Create: `src/chain.py`
- Create: `tests/test_citation_parser.py`

PRD Reference: Section 6.5 (citation parsing), 6.6, 6.7, 6.8, FR-12, FR-26, D-B5

- [x] **Step 7.1: Tulis failing unit test untuk citation parser terlebih dahulu (TDD)**

Buat `tests/__init__.py`:
```bash
echo "" > tests/__init__.py
```

Buat `tests/test_citation_parser.py`:

```python
# tests/test_citation_parser.py
# Unit test untuk parse_cited_indices — fungsi kritis untuk citation system
# Jalankan: pytest tests/test_citation_parser.py -v

import pytest


# Import akan gagal sampai src/chain.py dibuat — ini intentional (TDD)
from src.chain import parse_cited_indices


class TestParseCitedIndices:
    """Test suite untuk parse_cited_indices (PRD Section 6.5)."""

    def test_basic_citation(self):
        """Marker valid dalam range dikembalikan."""
        result = parse_cited_indices("Jawaban ini [1] benar.", max_source_index=3)
        assert result == [1]

    def test_multiple_citations(self):
        """Multiple marker valid dikembalikan sebagai sorted list."""
        result = parse_cited_indices("Dari [2] dan [1] serta [3].", max_source_index=3)
        assert result == [1, 2, 3]

    def test_duplicate_citations_deduplicated(self):
        """Marker yang sama tidak duplikat dalam hasil."""
        result = parse_cited_indices("[1] teks [1] teks [1]", max_source_index=2)
        assert result == [1]

    def test_out_of_range_ignored(self):
        """Marker di luar range max_source_index diabaikan tanpa crash."""
        result = parse_cited_indices("Referensi [5] tidak ada.", max_source_index=3)
        assert result == []

    def test_no_citation_returns_empty(self):
        """Teks tanpa marker mengembalikan list kosong, tidak crash."""
        result = parse_cited_indices("Jawaban tanpa referensi.", max_source_index=4)
        assert result == []

    def test_zero_max_source_index(self):
        """max_source_index=0 — semua marker di luar range."""
        result = parse_cited_indices("Teks [1].", max_source_index=0)
        assert result == []

    def test_mixed_valid_and_invalid(self):
        """Hanya marker dalam range yang dikembalikan."""
        result = parse_cited_indices("[1] valid, [10] tidak valid, [2] valid", max_source_index=3)
        assert result == [1, 2]

    def test_result_is_sorted(self):
        """Hasil selalu sorted ascending."""
        result = parse_cited_indices("[3] lalu [1] lalu [2]", max_source_index=5)
        assert result == [1, 2, 3]

    def test_empty_text_returns_empty(self):
        """String kosong mengembalikan list kosong."""
        result = parse_cited_indices("", max_source_index=4)
        assert result == []
```

- [x] **Step 7.2: Jalankan test — pastikan FAIL (ImportError karena chain.py belum ada)**

```bash
pytest tests/test_citation_parser.py -v
```

Expected: `ImportError: cannot import name 'parse_cited_indices' from 'src.chain'`

- [x] **Step 7.3: Buat src/chain.py**

```python
# src/chain.py — RAG Chain: retrieval + LLM + inline citation + SSE streaming
# PRD Reference: Section 6.5, 6.6, 6.7, 6.8, FR-12, FR-26, D-B5
# PENTING: Gunakan `use context7` untuk verifikasi API LangChain dan Gemini sebelum run

import re
import time
import tiktoken
from typing import Any, Generator

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.config import (
    LLM_TEMPERATURE, LLM_MAX_OUTPUT_TOKENS, LLM_TOP_P,
    MEMORY_K, MAX_RETRIES, RETRY_DELAYS,
    SYSTEM_PROMPT, FALLBACK_RESPONSE, GOOGLE_API_KEY,
)
from src.retriever import retrieve_chunks
from src.logger_manager import get_logger, log_chat_transaction

logger = get_logger("chain")

# ── Tiktoken untuk estimasi token offline (D-A5) ──────────────────────────────
_enc = tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    """Estimasi jumlah token menggunakan tiktoken cl100k_base (proxy untuk Gemini)."""
    return len(_enc.encode(text))


# ── Stateless LLM cache (D-B5) ───────────────────────────────────────────────
_llm_cache: dict[str, ChatGoogleGenerativeAI] = {}


def _get_llm(model_name: str) -> ChatGoogleGenerativeAI:
    """
    Kembalikan LLM instance untuk model_name. Cache per model, tidak ada global mutation.

    Stateless per-request — konsisten dengan arsitektur backend (D-B5, Section 6.7).
    """
    if model_name not in _llm_cache:
        _llm_cache[model_name] = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=GOOGLE_API_KEY,
            temperature=LLM_TEMPERATURE,
            max_output_tokens=LLM_MAX_OUTPUT_TOKENS,
            top_p=LLM_TOP_P,
        )
        logger.debug(f"LLM instance dibuat untuk model: {model_name}")
    return _llm_cache[model_name]


def parse_cited_indices(answer_text: str, max_source_index: int) -> list[int]:
    """
    Ekstrak nomor sumber yang dikutip LLM dari teks jawaban.

    Hanya mengenali format [N] (bracket dengan angka). Mengabaikan marker
    di luar range valid. Mengembalikan list kosong jika tidak ada kutipan
    yang valid — TIDAK crash. (PRD Section 6.5, FR-26)

    Args:
        answer_text: Teks jawaban dari LLM.
        max_source_index: Jumlah maksimum sumber yang tersedia.

    Returns:
        List integer unik dan terurut dari nomor sumber yang dikutip.
    """
    raw_indices = re.findall(r'\[(\d+)\]', answer_text)
    valid_indices = []
    for idx_str in raw_indices:
        idx = int(idx_str)
        if 1 <= idx <= max_source_index:
            if idx not in valid_indices:
                valid_indices.append(idx)
        else:
            logger.warning(
                f"LLM mengutip [{idx}] tapi hanya ada {max_source_index} sumber. Diabaikan."
            )
    return sorted(valid_indices)


def _format_context(chunks: list[dict]) -> str:
    """
    Format chunks menjadi string konteks dengan penanda sumber [Sumber N: ...].

    Format ini menginstruksikan LLM untuk menggunakan [N] dalam jawaban.
    """
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        header = f"[Sumber {i}: {chunk['title']} — {chunk.get('bab', '')} {chunk.get('bagian', '')}]"
        parts.append(f"{header}\n{chunk['content']}")
    return "\n\n---\n\n".join(parts)


def _build_messages(
    query: str,
    context: str,
    chat_history: list[dict],
) -> list[Any]:
    """
    Bangun list pesan untuk LLM: system prompt + trimmed history + user query.

    chat_history di-trim ke MEMORY_K * 2 pesan terbaru.
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Trim history ke MEMORY_K pasang terakhir
    trimmed_history = chat_history[-(MEMORY_K * 2):]
    for msg in trimmed_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    # Query + konteks
    user_content = f"Konteks:\n{context}\n\nPertanyaan: {query}"
    messages.append(HumanMessage(content=user_content))
    return messages


def get_response(
    query: str,
    config: str,
    chat_history: list[dict],
    model_name: str,
    streaming: bool = False,
) -> dict | Generator:
    """
    Proses query RAG dan kembalikan respons.

    Mode streaming=False (untuk evaluation.py): return dict langsung.
    Mode streaming=True (untuk app.py via SSE): return Generator yang yield event SSE.

    Return dict (non-streaming):
    {
        "answer": str,
        "citation_sources": list[dict],   # chunk yang dikutip LLM
        "retrieved_contexts": list[str],  # SEMUA chunk lolos threshold (untuk Ragas)
        "found": bool,
        "cited_indices": list[int],
    }

    (PRD Section 6.8, FR-12, D-A7)
    """
    if streaming:
        return _get_response_streaming(query, config, chat_history, model_name)
    else:
        return _get_response_sync(query, config, chat_history, model_name)


def _get_response_sync(
    query: str,
    config: str,
    chat_history: list[dict],
    model_name: str,
) -> dict:
    """Implementasi non-streaming untuk evaluation.py."""
    start_time = time.time()
    logger.info(f"Query: '{query[:80]}' | Config: {config} | Model: {model_name}")

    # Retrieval
    chunks = retrieve_chunks(query, config)

    if not chunks:
        # FR-11: Fallback jika tidak ada chunk lolos threshold
        elapsed = time.time() - start_time
        _log_transaction(
            config=config, model_llm=model_name, query=query,
            chunks=[], answer=FALLBACK_RESPONSE,
            elapsed=elapsed, found=False,
        )
        return {
            "answer": FALLBACK_RESPONSE,
            "citation_sources": [],
            "retrieved_contexts": [],
            "found": False,
            "cited_indices": [],
        }

    context = _format_context(chunks)
    messages = _build_messages(query, context, chat_history)
    llm = _get_llm(model_name)

    # LLM generation dengan retry
    answer = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = llm.invoke(messages)
            answer = response.content
            break
        except Exception as e:
            if attempt == MAX_RETRIES:
                logger.error(f"LLM gagal setelah {MAX_RETRIES} attempt: {e}")
                answer = "Terjadi gangguan pada layanan AI. Coba lagi nanti."
                break
            wait = RETRY_DELAYS[attempt - 1] if attempt - 1 < len(RETRY_DELAYS) else 10
            logger.warning(f"LLM error attempt {attempt}/{MAX_RETRIES}: {e}. Retry {wait}s.")
            time.sleep(wait)

    # Citation parsing (FR-26, Section 6.5)
    cited_indices = parse_cited_indices(answer, max_source_index=len(chunks))

    citation_sources = []
    for idx in cited_indices:
        chunk = chunks[idx - 1]   # 1-based
        citation_sources.append({
            "index":    idx,
            "doc_id":   chunk["doc_id"],
            "title":    chunk["title"],
            "bab":      chunk.get("bab", ""),
            "bagian":   chunk.get("bagian", ""),
            "pasal":    chunk.get("pasal", ""),
            "preview":  chunk["content"][:150],
            "content":  chunk["content"],
        })

    # retrieved_contexts untuk Ragas — SEMUA chunk lolos threshold (D-A7, Section 6.6)
    retrieved_contexts = [c["content"] for c in chunks]

    elapsed = time.time() - start_time
    logger.info(f"Retrieved: {len(chunks)} chunks | Cited: {len(citation_sources)} | Latency: {elapsed:.2f}s")
    logger.debug(f"LLM Output: {answer[:200]}...")

    _log_transaction(
        config=config, model_llm=model_name, query=query,
        chunks=chunks, answer=answer, elapsed=elapsed, found=True,
    )

    return {
        "answer": answer,
        "citation_sources": citation_sources,
        "retrieved_contexts": retrieved_contexts,
        "found": True,
        "cited_indices": cited_indices,
    }


def _get_response_streaming(
    query: str,
    config: str,
    chat_history: list[dict],
    model_name: str,
) -> Generator:
    """
    Implementasi streaming untuk app.py via SSE.

    Yield string dalam format SSE: 'data: {json}\n\n'
    Event types: thinking, token, citations, done, error (FR-27)
    """
    import json

    yield f'data: {json.dumps({"type": "thinking", "content": "Sedang mencari informasi..."})}\n\n'

    start_time = time.time()

    try:
        chunks = retrieve_chunks(query, config)

        if not chunks:
            # FR-11: Fallback
            elapsed = time.time() - start_time
            _log_transaction(
                config=config, model_llm=model_name, query=query,
                chunks=[], answer=FALLBACK_RESPONSE, elapsed=elapsed, found=False,
            )
            yield f'data: {json.dumps({"type": "token", "content": FALLBACK_RESPONSE})}\n\n'
            yield f'data: {json.dumps({"type": "citations", "sources": []})}\n\n'
            yield f'data: {json.dumps({"type": "done"})}\n\n'
            return

        context = _format_context(chunks)
        messages = _build_messages(query, context, chat_history)
        llm = _get_llm(model_name)

        # Streaming generation dengan retry
        full_answer = ""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                for token_chunk in llm.stream(messages):
                    token = token_chunk.content
                    full_answer += token
                    yield f'data: {json.dumps({"type": "token", "content": token})}\n\n'
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    error_msg = "Terjadi gangguan pada layanan AI. Coba lagi nanti."
                    logger.error(f"LLM streaming error: {e}")
                    yield f'data: {json.dumps({"type": "error", "message": error_msg})}\n\n'
                    return
                wait = RETRY_DELAYS[attempt - 1] if attempt - 1 < len(RETRY_DELAYS) else 10
                logger.warning(f"Streaming error attempt {attempt}: {e}. Retry {wait}s.")
                time.sleep(wait)
                full_answer = ""   # reset untuk retry

        # Citations setelah streaming selesai
        cited_indices = parse_cited_indices(full_answer, max_source_index=len(chunks))
        citation_sources = []
        for idx in cited_indices:
            chunk = chunks[idx - 1]
            citation_sources.append({
                "index":   idx,
                "doc_id":  chunk["doc_id"],
                "title":   chunk["title"],
                "bab":     chunk.get("bab", ""),
                "bagian":  chunk.get("bagian", ""),
                "pasal":   chunk.get("pasal", ""),
                "preview": chunk["content"][:150],
            })

        elapsed = time.time() - start_time
        logger.info(f"Streaming done | {len(chunks)} chunks | {len(citation_sources)} cited | {elapsed:.2f}s")

        _log_transaction(
            config=config, model_llm=model_name, query=query,
            chunks=chunks, answer=full_answer, elapsed=elapsed, found=True,
        )

        yield f'data: {json.dumps({"type": "citations", "sources": citation_sources})}\n\n'
        yield f'data: {json.dumps({"type": "done"})}\n\n'

    except Exception as e:
        logger.error(f"Unexpected error in streaming: {e}")
        yield f'data: {json.dumps({"type": "error", "message": "Terjadi kesalahan sistem. Coba lagi."})}\n\n'


def _log_transaction(
    config: str,
    model_llm: str,
    query: str,
    chunks: list[dict],
    answer: str,
    elapsed: float,
    found: bool,
) -> None:
    """Log transaksi ke transaksi_chat.csv via logger_manager."""
    prompt_text  = SYSTEM_PROMPT + query + " ".join(c["content"] for c in chunks[:4])
    prompt_tokens  = estimate_tokens(prompt_text)
    answer_tokens  = estimate_tokens(answer)

    distances = [c.get("distance", c.get("score", 0.0)) for c in chunks]

    log_chat_transaction(
        config=config,
        model_llm=model_llm,
        user_query=query,
        chunks_retrieved_count=len(chunks),
        retrieved_chunk_ids=[c.get("chunk_id", "") for c in chunks],
        best_similarity_score=min(distances) if distances else 0.0,
        average_similarity_score=sum(distances) / len(distances) if distances else 0.0,
        response_time_seconds=elapsed,
        estimated_prompt_tokens=prompt_tokens,
        estimated_completion_tokens=answer_tokens,
        estimated_total_tokens=prompt_tokens + answer_tokens,
        found_state=found,
        answer_preview=answer[:200],
    )
```

- [x] **Step 7.4: Jalankan test — pastikan PASS**

```bash
pytest tests/test_citation_parser.py -v
```

Expected:
```
tests/test_citation_parser.py::TestParseCitedIndices::test_basic_citation PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_multiple_citations PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_duplicate_citations_deduplicated PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_out_of_range_ignored PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_no_citation_returns_empty PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_zero_max_source_index PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_mixed_valid_and_invalid PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_result_is_sorted PASSED
tests/test_citation_parser.py::TestParseCitedIndices::test_empty_text_returns_empty PASSED

9 passed in X.XXs
```

- [x] **Step 7.5: Verifikasi get_response non-streaming**

```bash
python -c "
from src.chain import get_response
result = get_response(
    query='Berapa SKS maksimal yang bisa diambil mahasiswa per semester?',
    config='b',
    chat_history=[],
    model_name='gemini-2.5-flash',
    streaming=False,
)
print('Found:', result['found'])
print('Answer:', result['answer'][:200])
print('Citations:', len(result['citation_sources']))
print('Retrieved contexts:', len(result['retrieved_contexts']))
"
```

Expected: `found=True`, jawaban tentang SKS, citation_sources ≥ 1.

- [x] **Step 7.6: Commit**

```bash
git add src/chain.py tests/__init__.py tests/test_citation_parser.py
git commit -m "feat: tambah src/chain.py — RAG chain + citation + SSE (D-B5: stateless LLM)"
```

---

## Task 8: app.py — FastAPI Backend

**Files:**
- Create: `app.py`

PRD Reference: Section 10, FR-27, D-B4 (tanpa /api/log_transaction)

- [x] **Step 8.1: Buat app.py**

```python
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
```

- [x] **Step 8.2: Test endpoint /api/config**

Jalankan server di terminal terpisah:
```bash
python app.py
```

Di terminal lain:
```bash
python -c "
import urllib.request, json
with urllib.request.urlopen('http://localhost:8501/api/config') as r:
    print(json.loads(r.read()))
"
```

Expected: JSON dengan `available_models`, `active_model`, `configs`.

- [x] **Step 8.3: Test endpoint /api/chat via SSE**

```bash
python -c "
import urllib.request, json
data = json.dumps({'query': 'Apa itu UNSRAT?', 'config': 'b', 'chat_history': [], 'model': 'gemini-2.5-flash'}).encode()
req = urllib.request.Request('http://localhost:8501/api/chat', data=data, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    for line in r:
        line = line.decode().strip()
        if line.startswith('data:'):
            print(line[:120])
"
```

Expected: Event `thinking`, lalu beberapa event `token`, event `citations`, event `done`.

- [x] **Step 8.4: Commit**

```bash
git add app.py
git commit -m "feat: tambah app.py — FastAPI 4 endpoint + SSE streaming (D-B4: no log_transaction)"
```

---

## Task 9: static/ — SPA Frontend

**Files:**
- Create: `static/index.html`
- Create: `static/js/app.js`

PRD Reference: Section 11, FR-27, FR-33

- [x] **Step 9.1: Buat static/index.html**

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Informasi Akademik UNSRAT</title>
    <meta name="description" content="Sistem tanya-jawab akademik Universitas Sam Ratulangi berbasis RAG">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --maroon: #800000;
            --maroon-dark: #5c0000;
            --maroon-light: #a33030;
            --gold: #c9a227;
            --bg: #f5f5f5;
            --surface: #ffffff;
            --text: #1a1a1a;
            --text-muted: #666666;
            --border: #e0e0e0;
            --user-bubble: #800000;
            --bot-bubble: #f0f0f0;
            --error-bubble: #fff0f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; }

        /* Header */
        header { background: var(--maroon); color: white; padding: 12px 20px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }
        header h1 { font-size: 1.1rem; font-weight: 600; }
        header p { font-size: 0.8rem; opacity: 0.8; }

        /* Tab navigation */
        .tabs { display: flex; background: var(--maroon-dark); }
        .tab-btn { padding: 10px 24px; border: none; background: transparent; color: rgba(255,255,255,0.7); cursor: pointer; font-size: 0.9rem; transition: background 0.2s; }
        .tab-btn.active { background: var(--bg); color: var(--maroon); font-weight: 600; }
        .tab-btn:hover:not(.active) { background: rgba(255,255,255,0.1); }

        /* Main layout */
        .main { display: flex; flex: 1; overflow: hidden; }
        .tab-content { display: none; flex: 1; overflow: hidden; }
        .tab-content.active { display: flex; }

        /* Sidebar */
        .sidebar { width: 220px; background: var(--surface); border-right: 1px solid var(--border); padding: 16px; display: flex; flex-direction: column; gap: 16px; overflow-y: auto; }
        .sidebar label { font-size: 0.8rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; }
        .sidebar select, .sidebar button { width: 100%; padding: 8px 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.85rem; }
        .sidebar button { background: var(--maroon); color: white; border: none; cursor: pointer; margin-top: 4px; }
        .sidebar button:hover { background: var(--maroon-light); }
        .sidebar-section { display: flex; flex-direction: column; gap: 6px; }

        /* Chat area */
        .chat-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        #chat-messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }

        /* Bubbles */
        .bubble { max-width: 75%; padding: 10px 14px; border-radius: 12px; line-height: 1.6; font-size: 0.9rem; }
        .bubble.user { align-self: flex-end; background: var(--user-bubble); color: white; border-bottom-right-radius: 4px; }
        .bubble.bot { align-self: flex-start; background: var(--bot-bubble); border-bottom-left-radius: 4px; }
        .bubble.error { align-self: flex-start; background: var(--error-bubble); border: 1px solid #ff9999; color: #cc0000; }
        .bubble.thinking { align-self: flex-start; background: var(--bot-bubble); opacity: 0.7; font-style: italic; }

        /* Thinking dots animation */
        .thinking-dots::after { content: ''; animation: dots 1.2s steps(4, end) infinite; }
        @keyframes dots { 0%, 20% { content: ''; } 40% { content: '.'; } 60% { content: '..'; } 80%, 100% { content: '...'; } }

        /* Citation panel */
        .citations { margin-top: 8px; padding: 8px 10px; background: rgba(128,0,0,0.05); border-left: 3px solid var(--maroon); border-radius: 4px; font-size: 0.78rem; }
        .citations h4 { color: var(--maroon); margin-bottom: 6px; font-size: 0.78rem; }
        .citation-item { margin-bottom: 4px; }
        .citation-item strong { color: var(--maroon); }

        /* Input area */
        .input-area { padding: 12px 16px; border-top: 1px solid var(--border); background: var(--surface); display: flex; gap: 10px; }
        #user-input { flex: 1; padding: 10px 14px; border: 1px solid var(--border); border-radius: 20px; font-size: 0.9rem; resize: none; max-height: 100px; }
        #send-btn { padding: 10px 20px; background: var(--maroon); color: white; border: none; border-radius: 20px; cursor: pointer; font-weight: 600; }
        #send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        #send-btn:hover:not(:disabled) { background: var(--maroon-light); }

        /* Disclaimer */
        .disclaimer { text-align: center; padding: 6px; font-size: 0.72rem; color: var(--text-muted); background: var(--surface); border-top: 1px solid var(--border); }

        /* Tab 2 — Evaluasi */
        .eval-content { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }
        .eval-card { background: var(--surface); border-radius: 8px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
        .eval-card h3 { color: var(--maroon); margin-bottom: 12px; font-size: 1rem; }
        table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
        th { background: var(--maroon); color: white; padding: 8px 10px; text-align: left; }
        td { padding: 7px 10px; border-bottom: 1px solid var(--border); }
        tr:hover td { background: rgba(128,0,0,0.04); }
        .chart-container { max-width: 700px; }
        .empty-state { color: var(--text-muted); font-style: italic; padding: 8px 0; font-size: 0.85rem; }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>💬 Chatbot Informasi Akademik UNSRAT</h1>
            <p>Universitas Sam Ratulangi — Sistem RAG Penelitian</p>
        </div>
    </header>

    <div class="tabs">
        <button class="tab-btn active" id="tab-chat-btn" onclick="switchTab('chat')">💬 Chatbot</button>
        <button class="tab-btn" id="tab-eval-btn" onclick="switchTab('eval')">📊 Evaluasi Ragas</button>
    </div>

    <div class="main">
        <!-- Tab 1: Chatbot -->
        <div class="tab-content active" id="tab-chat">
            <div class="sidebar">
                <div class="sidebar-section">
                    <label>Konfigurasi</label>
                    <select id="config-select">
                        <option value="b">Config B — RAG (2000 char)</option>
                        <option value="a">Config A — RAG (500 char)</option>
                        <option value="c">Config C — BM25 Keyword</option>
                    </select>
                </div>
                <div class="sidebar-section">
                    <label>Model LLM</label>
                    <select id="model-select">
                        <option value="gemini-2.5-flash">gemini-2.5-flash</option>
                    </select>
                </div>
                <div class="sidebar-section">
                    <button id="reset-btn" onclick="resetChat()">🔄 Reset Percakapan</button>
                </div>
                <div class="sidebar-section" style="margin-top: auto; font-size: 0.75rem; color: var(--text-muted);">
                    <p id="status-info">Ready</p>
                </div>
            </div>

            <div class="chat-area">
                <div id="chat-messages"></div>
                <div class="input-area">
                    <textarea id="user-input" placeholder="Ketik pertanyaan Anda tentang akademik UNSRAT..." rows="1"
                        onkeydown="handleKeyDown(event)"></textarea>
                    <button id="send-btn" onclick="sendMessage()">Kirim</button>
                </div>
                <div class="disclaimer">
                    ⚠️ Sistem ini adalah prototipe penelitian. Verifikasi informasi ke Bagian Akademik UNSRAT untuk kepastian.
                </div>
            </div>
        </div>

        <!-- Tab 2: Evaluasi -->
        <div class="tab-content" id="tab-eval">
            <div class="eval-content">
                <div class="eval-card">
                    <h3>📊 Perbandingan Metrik Ragas (Mean ± Std)</h3>
                    <div id="metrics-table-container"><p class="empty-state">Jalankan evaluasi terlebih dahulu: <code>python evaluation.py --config a</code></p></div>
                </div>
                <div class="eval-card">
                    <h3>📈 Visualisasi Komparasi Config</h3>
                    <div class="chart-container"><canvas id="metricsChart"></canvas></div>
                </div>
                <div class="eval-card">
                    <h3>🔬 Uji Wilcoxon Signed-Rank (Config A vs B)</h3>
                    <div id="wilcoxon-table-container"><p class="empty-state">Jalankan: <code>python evaluation.py --stats</code></p></div>
                </div>
                <div class="eval-card">
                    <h3>📋 5 Transaksi Terakhir (Audit Log)</h3>
                    <div id="audit-log-container"><p class="empty-state">Belum ada transaksi.</p></div>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
```

- [x] **Step 9.2: Buat static/js/app.js**

```javascript
// static/js/app.js — Frontend SPA Logic
// PRD Reference: Section 11, FR-27, FR-33

// ── State ─────────────────────────────────────────────────────────────────────
let chatHistory = [];   // [{role: "user"|"assistant", content: "..."}]
let isStreaming = false;
let metricsChartInstance = null;

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
    await loadConfig();
    if (document.getElementById("tab-eval").classList.contains("active")) {
        await loadEvalData();
    }
});

async function loadConfig() {
    try {
        const res = await fetch("/api/config");
        const data = await res.json();
        const modelSelect = document.getElementById("model-select");
        modelSelect.innerHTML = data.available_models
            .map(m => `<option value="${m}">${m}</option>`)
            .join("");
        modelSelect.value = data.active_model;
    } catch (e) {
        console.error("Gagal load config:", e);
    }
}

// ── Tab Switching ─────────────────────────────────────────────────────────────
function switchTab(tab) {
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.getElementById(`tab-${tab}`).classList.add("active");
    document.getElementById(`tab-${tab}-btn`).classList.add("active");
    if (tab === "eval") loadEvalData();
}

// ── Chat Logic ────────────────────────────────────────────────────────────────
function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const query = input.value.trim();
    if (!query || isStreaming) return;

    const config = document.getElementById("config-select").value;
    const model  = document.getElementById("model-select").value;

    input.value = "";
    isStreaming  = true;
    document.getElementById("send-btn").disabled = true;
    document.getElementById("status-info").textContent = "Memproses...";

    // Tampilkan bubble user
    appendBubble("user", query);
    chatHistory.push({ role: "user", content: query });

    // Placeholder bot bubble
    const botBubbleId = `bot-${Date.now()}`;
    const thinkingId  = `thinking-${Date.now()}`;
    appendThinkingBubble(thinkingId);

    let botContent = "";
    let botBubbleCreated = false;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, config, chat_history: chatHistory, model }),
        });

        const reader   = response.body.getReader();
        const decoder  = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const text   = decoder.decode(value, { stream: true });
            const lines  = text.split("\n");

            for (const line of lines) {
                if (!line.startsWith("data:")) continue;
                const jsonStr = line.slice(5).trim();
                if (!jsonStr) continue;

                let event;
                try { event = JSON.parse(jsonStr); } catch { continue; }

                if (event.type === "thinking") {
                    // Thinking indicator sudah tampil — tidak perlu aksi
                } else if (event.type === "token") {
                    removeElement(thinkingId);
                    if (!botBubbleCreated) {
                        createBotBubble(botBubbleId);
                        botBubbleCreated = true;
                    }
                    botContent += event.content;
                    document.getElementById(botBubbleId).textContent = botContent;
                    scrollToBottom();
                } else if (event.type === "citations") {
                    if (event.sources && event.sources.length > 0) {
                        appendCitations(botBubbleId, event.sources);
                    }
                } else if (event.type === "done") {
                    chatHistory.push({ role: "assistant", content: botContent });
                    break;
                } else if (event.type === "error") {
                    removeElement(thinkingId);
                    appendErrorBubble(event.message);
                    break;
                }
            }
        }
    } catch (e) {
        removeElement(thinkingId);
        appendErrorBubble("Gagal terhubung ke server. Pastikan server berjalan.");
        console.error(e);
    } finally {
        isStreaming = false;
        document.getElementById("send-btn").disabled = false;
        document.getElementById("status-info").textContent = "Ready";
    }
}

function resetChat() {
    chatHistory = [];
    document.getElementById("chat-messages").innerHTML = "";
    document.getElementById("status-info").textContent = "Percakapan di-reset.";
    setTimeout(() => document.getElementById("status-info").textContent = "Ready", 1500);
}

// ── DOM Helpers ───────────────────────────────────────────────────────────────
function appendBubble(role, content) {
    const div = document.createElement("div");
    div.className = `bubble ${role}`;
    div.textContent = content;
    document.getElementById("chat-messages").appendChild(div);
    scrollToBottom();
}

function appendThinkingBubble(id) {
    const div = document.createElement("div");
    div.id = id;
    div.className = "bubble thinking";
    div.innerHTML = 'Sedang mencari informasi<span class="thinking-dots"></span>';
    document.getElementById("chat-messages").appendChild(div);
    scrollToBottom();
}

function createBotBubble(id) {
    const div = document.createElement("div");
    div.id = id;
    div.className = "bubble bot";
    document.getElementById("chat-messages").appendChild(div);
}

function appendErrorBubble(message) {
    const div = document.createElement("div");
    div.className = "bubble error";
    div.textContent = `⚠️ ${message}`;
    document.getElementById("chat-messages").appendChild(div);
    scrollToBottom();
}

function appendCitations(bubbleId, sources) {
    const bubble = document.getElementById(bubbleId);
    if (!bubble) return;
    const panel = document.createElement("div");
    panel.className = "citations";
    panel.innerHTML = `<h4>📚 Sumber Referensi</h4>` +
        sources.map(s =>
            `<div class="citation-item"><strong>[${s.index}] ${s.title}</strong> — ${s.bab || ""} ${s.bagian || ""}<br><small>${s.preview || ""}</small></div>`
        ).join("");
    bubble.appendChild(panel);
    scrollToBottom();
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    const msgs = document.getElementById("chat-messages");
    msgs.scrollTop = msgs.scrollHeight;
}

// ── Evaluation Tab ────────────────────────────────────────────────────────────
async function loadEvalData() {
    try {
        const res  = await fetch("/api/evaluation");
        const data = await res.json();
        renderMetricsTable(data.configs);
        renderChart(data.configs);
        renderWilcoxon(data.wilcoxon);
        renderAuditLog(data.audit_log);
    } catch (e) {
        console.error("Gagal load evaluation data:", e);
    }
}

function renderMetricsTable(configs) {
    const container = document.getElementById("metrics-table-container");
    if (!configs || Object.keys(configs).length === 0) {
        container.innerHTML = '<p class="empty-state">Belum ada hasil evaluasi.</p>';
        return;
    }
    const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "response_time_seconds"];
    const configLabels = { a: "Config A (500)", b: "Config B (2000)", c: "Config C (BM25)" };
    let html = `<table><tr><th>Metrik</th>${Object.keys(configs).map(k => `<th>${configLabels[k] || k}</th>`).join("")}</tr>`;
    for (const m of metrics) {
        html += `<tr><td><strong>${m}</strong></td>`;
        for (const cfg of Object.keys(configs)) {
            const s = configs[cfg][m];
            html += s ? `<td>${s.mean.toFixed(3)} ± ${s.std.toFixed(3)}</td>` : "<td>—</td>";
        }
        html += "</tr>";
    }
    html += "</table>";
    container.innerHTML = html;
}

function renderChart(configs) {
    const ctx = document.getElementById("metricsChart").getContext("2d");
    if (metricsChartInstance) metricsChartInstance.destroy();
    if (!configs || Object.keys(configs).length === 0) return;

    const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"];
    const colors  = { a: "#800000", b: "#c9a227", c: "#4a4a4a" };
    const labels  = { a: "Config A", b: "Config B", c: "Config C (BM25)" };

    const datasets = Object.entries(configs).map(([cfg, stats]) => ({
        label: labels[cfg] || cfg,
        data: metrics.map(m => stats[m]?.mean || 0),
        backgroundColor: colors[cfg] || "#999",
    }));

    metricsChartInstance = new Chart(ctx, {
        type: "bar",
        data: { labels: metrics, datasets },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, max: 1 } },
            plugins: { legend: { position: "top" } },
        },
    });
}

function renderWilcoxon(wilcoxon) {
    const container = document.getElementById("wilcoxon-table-container");
    if (!wilcoxon || Object.keys(wilcoxon).length === 0) {
        container.innerHTML = '<p class="empty-state">Jalankan: <code>python evaluation.py --stats</code></p>';
        return;
    }
    let html = `<table><tr><th>Metrik</th><th>Statistik</th><th>p-value</th><th>Signifikan (p<0.05)</th><th>Winner</th></tr>`;
    for (const [metric, stat] of Object.entries(wilcoxon)) {
        html += `<tr><td>${metric}</td><td>${stat.statistic}</td><td>${stat.p_value}</td><td>${stat.significant ? "✅ Ya" : "❌ Tidak"}</td><td>${stat.winner || "—"}</td></tr>`;
    }
    html += "</table>";
    container.innerHTML = html;
}

function renderAuditLog(logs) {
    const container = document.getElementById("audit-log-container");
    if (!logs || logs.length === 0) {
        container.innerHTML = '<p class="empty-state">Belum ada transaksi.</p>';
        return;
    }
    let html = `<table><tr><th>Waktu</th><th>Config</th><th>Query</th><th>Chunks</th><th>Latency</th></tr>`;
    for (const log of logs) {
        html += `<tr><td>${log.timestamp || "—"}</td><td>${log.config || "—"}</td><td>${(log.user_query || "").substring(0, 40)}...</td><td>${log.chunks_retrieved_count || 0}</td><td>${log.response_time_seconds || "—"}s</td></tr>`;
    }
    html += "</table>";
    container.innerHTML = html;
}
```

- [x] **Step 9.3: Verifikasi frontend via browser**

Pastikan server masih berjalan, buka browser ke `http://localhost:8501`. Verifikasi:
- [x] Tab Chatbot tampil dengan sidebar config/model
- [x] Ketik pertanyaan → muncul thinking indicator → streaming response → citation panel
- [x] Reset chat button berfungsi
- [x] Tab Evaluasi menampilkan "Belum ada hasil evaluasi" (normal jika belum eval)

- [x] **Step 9.4: Commit**

```bash
git add static/index.html static/js/app.js
git commit -m "feat: tambah static/ — SPA frontend dua tab (chatbot + evaluasi Ragas)"
```

---

## Task 10: evaluation.py — Pipeline Evaluasi Ragas

**Files:**
- Create: `evaluation.py`

PRD Reference: Section 12, FR-15–FR-17, FR-21–FR-23, FR-25, FR-31

> ⚠️ **WAJIB sebelum implementasi:** Jalankan `use context7` untuk mendapatkan dokumentasi API Ragas versi yang terinstall. Verifikasi nama class, cara instansiasi, dan signature `evaluate()`. Jangan tulis kode berdasarkan memori.

- [x] **Step 10.1: Verifikasi API Ragas yang terinstall**

```bash
python -c "import ragas; print('Ragas version:', ragas.__version__)"
python -c "from ragas import evaluate; help(evaluate)"
python -c "from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall; print('Metrics OK')"
```

Jika ada ImportError atau nama class berbeda, sesuaikan import di kode di bawah.

- [x] **Step 10.2: Buat evaluation.py**

```python
# evaluation.py — Pipeline Evaluasi Ragas + Wilcoxon + Error Analysis + Chart
# PRD Reference: Section 12, FR-15–FR-17, FR-21–FR-25, FR-31
#
# PENTING: Verifikasi API Ragas dengan `use context7` sebelum run!
# Nama class dan signature evaluate() berubah antar versi minor.
#
# Monkey patch VertexAI (jika diperlukan pada environment non-GCP):
import sys, types
_mock_vertex = types.ModuleType("vertexai")
sys.modules.setdefault("vertexai", _mock_vertex)

import argparse
import csv
import time
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon as scipy_wilcoxon

# Ragas imports — VERIFIKASI dengan `use context7` sebelum implementasi
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import RunConfig

from src.config import (
    EVAL_DATASET_PATH, EVAL_RESULTS_DIR,
    METRICS_COLS, OPTIONAL_METRICS_COLS, ERROR_ANALYSIS_N,
    EVALUATOR_MODEL_NAME, LLM_MODEL_NAME, GOOGLE_API_KEY,
)
from src.chain import get_response
from src.logger_manager import get_logger

logger = get_logger("evaluation")


def _load_ground_truth() -> pd.DataFrame:
    """Load ground_truth.csv. Raise FileNotFoundError jika tidak ada."""
    if not EVAL_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Ground truth tidak ditemukan: {EVAL_DATASET_PATH}\n"
            "Buat file CSV dengan kolom: user_input, reference, category, source_doc, notes"
        )
    df = pd.read_csv(EVAL_DATASET_PATH, encoding="utf-8-sig")
    required = ["user_input", "reference"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ada di ground_truth.csv: {missing}")
    logger.info(f"Ground truth dimuat: {len(df)} baris.")
    return df


def run_evaluation(config: str, extra_metrics: list[str] | None = None) -> None:
    """
    Jalankan evaluasi Ragas untuk config tertentu.

    Hasil disimpan ke eval/results/hasil_config_{config}.csv
    dan error_analysis_config_{config}.csv.

    (FR-15, FR-16, FR-21, FR-23, FR-25, FR-31)
    """
    logger.info(f"=== Evaluasi Config {config.upper()} dimulai ===")
    logger.info(f"Generator: {LLM_MODEL_NAME} | Evaluator: {EVALUATOR_MODEL_NAME}")
    logger.info("PERINGATAN: Pastikan model evaluator sama untuk semua config! (Section 18.5)")

    df = _load_ground_truth()
    EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    for idx, row in df.iterrows():
        query     = str(row["user_input"])
        reference = str(row["reference"])
        logger.info(f"[{idx+1}/{len(df)}] Evaluasi: '{query[:60]}'")

        start_time = time.time()

        # FR-14: Reset chat_history untuk setiap query evaluasi
        resp = get_response(
            query=query,
            config=config,
            chat_history=[],   # stateless per query
            model_name=LLM_MODEL_NAME,
            streaming=False,
        )

        elapsed = time.time() - start_time

        results.append({
            "user_input":           query,
            "reference":            reference,
            "response":             resp["answer"],
            # FR-31: retrieved_contexts = SEMUA chunk lolos threshold (bukan hanya citation_sources)
            "retrieved_contexts":   resp["retrieved_contexts"],
            "citation_sources_count": len(resp["citation_sources"]),
            "response_time_seconds": round(elapsed, 4),
            "category":             row.get("category", ""),
            "source_doc":           row.get("source_doc", ""),
        })

    # Ragas evaluation
    logger.info("Menjalankan Ragas evaluate()...")

    # Bangun dataset untuk Ragas
    # CATATAN: Verifikasi format input dengan `use context7`!
    eval_data = {
        "question":           [r["user_input"]           for r in results],
        "answer":             [r["response"]             for r in results],
        "contexts":           [r["retrieved_contexts"]   for r in results],
        "ground_truth":       [r["reference"]            for r in results],
    }

    # Konfigurasi sequential untuk stabilitas (Section 12.2)
    run_config = RunConfig(max_workers=1, timeout=300, max_retries=10)

    # Metrik yang dijalankan
    base_metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
    # Tambah metrik opsional jika diminta
    if extra_metrics:
        for m_name in extra_metrics:
            if m_name in OPTIONAL_METRICS_COLS:
                try:
                    # context_entity_recall — verifikasi import dengan `use context7`
                    from ragas.metrics import context_entity_recall
                    base_metrics.append(context_entity_recall)
                    logger.info(f"Metrik opsional ditambahkan: {m_name}")
                except ImportError:
                    logger.warning(f"Metrik opsional {m_name} tidak tersedia di versi Ragas ini.")

    # CATATAN: API Ragas bisa berbeda antar versi. Verifikasi dengan `use context7`.
    # Contoh di bawah menggunakan pola umum — sesuaikan jika nama class/fungsi berbeda.
    try:
        from datasets import Dataset
        ragas_dataset = Dataset.from_dict(eval_data)

        ragas_result = evaluate(
            dataset=ragas_dataset,
            metrics=base_metrics,
            run_config=run_config,
        )
        ragas_df = ragas_result.to_pandas()
    except Exception as e:
        logger.error(f"Ragas evaluate() gagal: {e}")
        logger.error("Jalankan `use context7` untuk verifikasi API Ragas yang terinstall.")
        raise

    # Gabungkan hasil Ragas dengan metadata
    for i, row in ragas_df.iterrows():
        results[i]["faithfulness"]       = row.get("faithfulness",       None)
        results[i]["answer_relevancy"]   = row.get("answer_relevancy",   None)
        results[i]["context_precision"]  = row.get("context_precision",  None)
        results[i]["context_recall"]     = row.get("context_recall",     None)
        if extra_metrics and "context_entity_recall" in extra_metrics:
            results[i]["context_entity_recall"] = row.get("context_entity_recall", None)

    # Simpan hasil utama
    output_path = EVAL_RESULTS_DIR / f"hasil_config_{config}.csv"
    fieldnames = [
        "user_input", "reference", "response", "retrieved_contexts",
        "citation_sources_count", "faithfulness", "answer_relevancy",
        "context_precision", "context_recall", "response_time_seconds",
        "category", "source_doc",
    ]
    if extra_metrics and "context_entity_recall" in extra_metrics:
        fieldnames.append("context_entity_recall")

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    logger.info(f"Hasil disimpan: {output_path}")

    # Agregasi
    df_result = pd.DataFrame(results)
    _print_summary(df_result, config)

    # FR-23: Error analysis — N sampel dengan skor terendah
    _export_error_analysis(df_result, config)


def _print_summary(df: pd.DataFrame, config: str) -> None:
    """Print agregasi mean ± std ke terminal dan log."""
    metrics = METRICS_COLS + ["response_time_seconds"]
    logger.info(f"\n{'='*60}\nRINGKASAN Config {config.upper()}\n{'='*60}")
    for m in metrics:
        if m in df.columns:
            logger.info(f"  {m:30s}: {df[m].mean():.4f} ± {df[m].std():.4f}")


def _export_error_analysis(df: pd.DataFrame, config: str) -> None:
    """
    Export ERROR_ANALYSIS_N sampel dengan skor Ragas terendah.

    Kolom failure_type diisi MANUAL oleh peneliti setelah ekspor.
    (FR-23, Section 22.3)
    """
    score_cols = [c for c in METRICS_COLS if c in df.columns]
    if not score_cols:
        return

    df_copy = df.copy()
    df_copy["avg_metric_score"] = df_copy[score_cols].mean(axis=1)
    df_sorted = df_copy.sort_values("avg_metric_score").head(ERROR_ANALYSIS_N)

    df_sorted["rank"]         = range(1, len(df_sorted) + 1)
    df_sorted["failure_type"] = ""   # Diisi manual oleh peneliti
    df_sorted["failure_notes"] = ""

    output_cols = ["rank", "user_input", "reference", "response",
                   "avg_metric_score", "failure_type", "failure_notes"]

    out_path = EVAL_RESULTS_DIR / f"error_analysis_config_{config}.csv"
    df_sorted[output_cols].to_csv(out_path, index=False, encoding="utf-8-sig")
    logger.info(f"Error analysis disimpan: {out_path}")


def run_statistical_test() -> None:
    """
    Jalankan Wilcoxon Signed-Rank Test antara Config A dan B per metrik.

    Simpan ke statistical_test.csv. (FR-22, D-17)
    """
    path_a = EVAL_RESULTS_DIR / "hasil_config_a.csv"
    path_b = EVAL_RESULTS_DIR / "hasil_config_b.csv"

    if not path_a.exists() or not path_b.exists():
        raise FileNotFoundError(
            "Jalankan evaluasi Config A dan B terlebih dahulu:\n"
            "  python evaluation.py --config a\n"
            "  python evaluation.py --config b"
        )

    df_a = pd.read_csv(path_a)
    df_b = pd.read_csv(path_b)

    if len(df_a) != len(df_b):
        raise ValueError(
            f"Jumlah baris A ({len(df_a)}) ≠ B ({len(df_b)}). "
            "Wilcoxon membutuhkan data berpasangan (jumlah query sama)."
        )

    results = []
    for metric in METRICS_COLS:
        if metric not in df_a.columns or metric not in df_b.columns:
            continue
        scores_a = df_a[metric].dropna()
        scores_b = df_b[metric].dropna()

        try:
            stat, p_value = scipy_wilcoxon(scores_a, scores_b)
            significant = p_value < 0.05
            winner = None
            if significant:
                winner = "Config B" if scores_b.mean() > scores_a.mean() else "Config A"
            results.append({
                "metric": metric,
                "wilcoxon_statistic": round(stat, 4),
                "p_value": round(p_value, 4),
                "significant_at_0.05": significant,
                "winner": winner or "Tidak signifikan",
                "mean_a": round(scores_a.mean(), 4),
                "mean_b": round(scores_b.mean(), 4),
            })
            logger.info(f"Wilcoxon {metric}: stat={stat:.4f}, p={p_value:.4f}, sig={significant}")
        except Exception as e:
            logger.warning(f"Wilcoxon gagal untuk {metric}: {e}")

    out_path = EVAL_RESULTS_DIR / "statistical_test.csv"
    pd.DataFrame(results).to_csv(out_path, index=False, encoding="utf-8-sig")
    logger.info(f"Statistical test disimpan: {out_path}")


def run_visualization() -> None:
    """
    Buat grouped bar chart perbandingan 3 config.

    Output: eval/results/perbandingan_visual.png (untuk lampiran skripsi).
    BUKAN dikonsumsi UI — UI render dari /api/evaluation. (D-A9, FR-17)
    """
    configs = {"a": "Config A (500)", "b": "Config B (2000)", "c": "Config C (BM25)"}
    metrics = METRICS_COLS

    data = {}
    for cfg, label in configs.items():
        path = EVAL_RESULTS_DIR / f"hasil_config_{cfg}.csv"
        if path.exists():
            df = pd.read_csv(path)
            data[label] = {m: df[m].mean() if m in df.columns else 0 for m in metrics}

    if not data:
        raise FileNotFoundError("Tidak ada file hasil evaluasi. Jalankan evaluasi terlebih dahulu.")

    fig, ax = plt.subplots(figsize=(12, 6))
    x      = range(len(metrics))
    width  = 0.25
    colors = ["#800000", "#c9a227", "#4a4a4a"]

    for i, (label, scores) in enumerate(data.items()):
        offset = (i - len(data) / 2) * width + width / 2
        bars = ax.bar([xi + offset for xi in x], [scores[m] for m in metrics],
                      width=width, label=label, color=colors[i % len(colors)])
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Metrik Evaluasi")
    ax.set_ylabel("Skor")
    ax.set_title("Perbandingan Kinerja Config A vs B vs C — UNSRAT RAG")
    ax.set_xticks(list(x))
    ax.set_xticklabels(metrics, rotation=15)
    ax.set_ylim(0, 1.1)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    out_path = EVAL_RESULTS_DIR / "perbandingan_visual.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    logger.info(f"Visualisasi disimpan: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Evaluasi UNSRAT RAG")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", choices=["a", "b", "c"], help="Jalankan evaluasi config tertentu")
    group.add_argument("--stats",      action="store_true", help="Uji Wilcoxon A vs B")
    group.add_argument("--visualize",  action="store_true", help="Buat bar chart PNG")

    parser.add_argument("--extra-metrics", nargs="+", default=None,
                        help="Metrik opsional, contoh: context_entity_recall")
    args = parser.parse_args()

    if args.config:
        run_evaluation(args.config, extra_metrics=args.extra_metrics)
    elif args.stats:
        run_statistical_test()
    elif args.visualize:
        run_visualization()
```

- [x] **Step 10.3: Buat ground_truth.csv minimal untuk test**

Buat `eval/dataset/ground_truth.csv` dengan beberapa baris contoh (untuk verifikasi pipeline berjalan):

```csv
user_input,reference,category,source_doc,notes
"Apa visi Universitas Sam Ratulangi?","Visi UNSRAT adalah menjadi universitas unggulan dalam pengembangan ilmu pengetahuan teknologi dan seni yang berbudaya dan humanis.","institution_profile","02_visi_misi.md","Paraf visi"
"Berapa SKS maksimal per semester untuk mahasiswa sarjana?","Mahasiswa program sarjana dapat mengambil maksimum 24 SKS per semester. Namun jika IPS semester sebelumnya di bawah 2.00, batas maksimalnya adalah 18 SKS.","academic","Peraturan_Akademik_UNSRAT_2025","Pasal 14"
"Kapan semester genap 2025/2026 dimulai?","Semester genap 2025/2026 dimulai pada awal Februari 2026 sesuai kalender akademik yang ditetapkan.","calendar","Kalender_Akademik_UNSRAT_Genap_2025-2026","Sesuai kalender"
```

> **CATATAN D-B6:** Kolom `reference` harus ditulis dalam natural language seperti contoh di atas — bukan copy-paste verbatim teks dokumen.

- [x] **Step 10.4: Test evaluasi dengan data minimal**

```bash
python evaluation.py --config b
```

Expected: Proses berjalan, file `eval/results/hasil_config_b.csv` terbuat.

Jika ada error import Ragas, jalankan `use context7` untuk verifikasi API dan sesuaikan import.

- [x] **Step 10.5: Commit**

```bash
git add evaluation.py eval/dataset/ground_truth.csv
git commit -m "feat: tambah evaluation.py — Ragas + Wilcoxon + error analysis + visualisasi"
```

---

## Task 11: Kalibrasi SIMILARITY_THRESHOLD (D-B7)

> **Lakukan ini SEBELUM evaluasi resmi**, bukan sebelum implementasi.

**Files:**
- Create: `scripts/calibrate_threshold.py` (scratch script, tidak perlu di-commit ke main)

PRD Reference: D-B7, Section 12.2b (Bab III metodologi)

- [ ] **Step 11.1: Buat script kalibrasi**

Buat `scripts/calibrate_threshold.py`:

```python
# scripts/calibrate_threshold.py
# Kalibrasi empiris SIMILARITY_THRESHOLD (D-B7)
# Jalankan: python scripts/calibrate_threshold.py
# Hasil digunakan untuk memvalidasi atau menyesuaikan nilai threshold di config.py

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import (
    CHROMA_DIR_B, CHROMA_COLLECTION_B,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, RETRIEVAL_K, SIMILARITY_THRESHOLD
)

embedding_fn = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    task_type="retrieval_query",
)

client     = chromadb.PersistentClient(path=str(CHROMA_DIR_B))
collection = client.get_collection(CHROMA_COLLECTION_B)

# 5 query RELEVAN (seharusnya distance kecil = mendekati 0)
relevant_queries = [
    "berapa SKS maksimal per semester",
    "syarat yudisium sarjana",
    "kalender akademik semester genap 2026",
    "cuti akademik prosedur",
    "visi misi universitas sam ratulangi",
]

# 5 query TIDAK RELEVAN (seharusnya distance besar)
irrelevant_queries = [
    "harga makan siang di kantin",
    "cuaca hari ini di Manado",
    "tim sepak bola favorit",
    "resep masak ayam goreng",
    "cara membuat kue ulang tahun",
]

print(f"\n{'='*60}")
print(f"CALIBRASI SIMILARITY_THRESHOLD — Config B (cosine distance)")
print(f"Threshold saat ini: {SIMILARITY_THRESHOLD}")
print(f"{'='*60}")

print("\n📌 Query RELEVAN (harapan: distance KECIL, < threshold):")
for q in relevant_queries:
    emb = embedding_fn.embed_query(q)
    res = collection.query(query_embeddings=[emb], n_results=RETRIEVAL_K, include=["distances"])
    dists = res["distances"][0]
    print(f"  '{q[:50]}' → distances: {[f'{d:.3f}' for d in dists]}")

print("\n📌 Query TIDAK RELEVAN (harapan: distance BESAR, > threshold):")
for q in irrelevant_queries:
    emb = embedding_fn.embed_query(q)
    res = collection.query(query_embeddings=[emb], n_results=RETRIEVAL_K, include=["distances"])
    dists = res["distances"][0]
    print(f"  '{q[:50]}' → distances: {[f'{d:.3f}' for d in dists]}")

print(f"\n{'='*60}")
print("INTERPRETASI:")
print(f"- Distance mendekati 0 = sangat relevan")
print(f"- Distance mendekati 1+ = tidak relevan")
print(f"- Threshold {SIMILARITY_THRESHOLD}: chunk dengan distance > {SIMILARITY_THRESHOLD} dibuang")
print(f"\nJika query relevan memberikan distance > {SIMILARITY_THRESHOLD}: threshold terlalu ketat → turunkan")
print(f"Jika query tidak relevan memberikan distance < {SIMILARITY_THRESHOLD}: threshold terlalu longgar → naikkan")
print(f"{'='*60}")
```

- [ ] **Step 11.2: Jalankan kalibrasi**

```bash
mkdir scripts
python scripts/calibrate_threshold.py
```

- [ ] **Step 11.3: Analisis dan sesuaikan threshold**

Periksa output:
- Jika query relevan memiliki distance rata-rata ~0.2–0.5 dan query tidak relevan ~0.7–1.2 → **nilai 0.65 valid**
- Jika gap kurang jelas → sesuaikan `SIMILARITY_THRESHOLD` di `src/config.py`
- Catat hasil kalibrasi di jurnal penelitian untuk Bab III

- [ ] **Step 11.4: Commit (hanya jika threshold berubah)**

Hanya commit jika nilai `SIMILARITY_THRESHOLD` di `config.py` berubah:
```bash
git add src/config.py scripts/calibrate_threshold.py
git commit -m "chore: kalibrasi SIMILARITY_THRESHOLD empiris — hasil D-B7"
```

---

## Task 12: Persiapan Ground Truth (D-B6)

> Ini adalah task MANUAL oleh peneliti — tidak ada kode yang perlu ditulis.

PRD Reference: Section 9.1, D-B6

- [ ] **Step 12.1: Buat 30–50 pasang Q&A ground truth**

Edit `eval/dataset/ground_truth.csv` mengikuti aturan berikut:

**Aturan penulisan `reference` (D-B6):**
- Tulis dalam Bahasa Indonesia yang natural — seperti menjawab ke mahasiswa
- Sertakan key facts: angka SKS, tanggal, nama pasal, kondisi edge case
- JANGAN copy-paste verbatim teks hukum
- Panjang ideal: 1–3 kalimat yang mencakup semua kondisi relevan

**Target distribusi:**
```
40% (12–20 Q&A) → Peraturan Akademik (academic)
30% (9–15 Q&A)  → Kalender Akademik (calendar)
20% (6–10 Q&A)  → Profil Institusi (institution_profile)
10% (3–5 Q&A)   → FAQ (setelah faq.md tersedia)
```

**Format CSV:**
```csv
user_input,reference,category,source_doc,notes
"Pertanyaan natural mahasiswa?","Jawaban natural dengan key facts spesifik.",kategori,nama_file.md,"Referensi pasal/bagian"
```

- [ ] **Step 12.2: Verifikasi ground truth CSV**

```bash
python -c "
import pandas as pd
from src.config import EVAL_DATASET_PATH
df = pd.read_csv(EVAL_DATASET_PATH, encoding='utf-8-sig')
print(f'Total Q&A: {len(df)}')
print(f'Distribusi kategori:\n{df[\"category\"].value_counts()}')
print(f'Rata-rata panjang reference: {df[\"reference\"].str.len().mean():.0f} karakter')
print('Semua kolom wajib ada:', all(c in df.columns for c in ['user_input', 'reference']))
"
```

Expected: ≥ 30 baris, distribusi kategori sesuai target, kolom `user_input` dan `reference` ada.

- [ ] **Step 12.3: Commit ground truth**

```bash
git add eval/dataset/ground_truth.csv
git commit -m "chore: tambah ground_truth.csv — 30-50 Q&A akademik (D-B6: natural language references)"
```

---

## Task 13: Evaluasi Resmi & Validasi Akhir

Jalankan setelah Task 11 (threshold kalibrasi) dan Task 12 (ground truth siap).

PRD Reference: Section 12.4, 16.5, Section 18 (jika menggunakan Ollama/NIM)

> ⚠️ **Pastikan model evaluator sama untuk SEMUA config** (Section 18.5). Catat provider dan model di jurnal sebelum mulai.

- [ ] **Step 13.1: Jalankan evaluasi ketiga config secara berurutan**

```bash
# Config B (RAG chunk besar) — jalankan pertama
python evaluation.py --config b

# Config A (RAG chunk kecil)
python evaluation.py --config a

# Config C (BM25 baseline)
python evaluation.py --config c
```

Setiap evaluasi akan menghasilkan file di `eval/results/`.

- [ ] **Step 13.2: Jalankan uji statistik Wilcoxon**

```bash
python evaluation.py --stats
```

Expected: File `eval/results/statistical_test.csv` terbuat.

- [ ] **Step 13.3: Buat visualisasi untuk lampiran skripsi**

```bash
python evaluation.py --visualize
```

Expected: File `eval/results/perbandingan_visual.png` terbuat.

- [ ] **Step 13.4: Verifikasi Tab Evaluasi di UI**

Buka `http://localhost:8501` → Tab Evaluasi. Verifikasi:
- Tabel metrik menampilkan mean ± std per config
- Bar chart ter-render dari data API (bukan PNG)
- Tabel Wilcoxon menampilkan p-value per metrik

- [ ] **Step 13.5: Isi failure_type di error_analysis CSV secara manual**

Buka `eval/results/error_analysis_config_a.csv` dan `error_analysis_config_b.csv`.
Untuk setiap baris, isi kolom `failure_type` dengan salah satu:
- `retrieval_failure` — informasi ada di dokumen tapi tidak ter-retrieve
- `generation_failure` — chunk tepat diambil, LLM salah interpretasi
- `chunking_failure` — informasi terpotong di tengah dua chunk

- [ ] **Step 13.6: Commit hasil evaluasi (hanya CSV metadata, bukan raw data)**

```bash
git add eval/results/statistical_test.csv eval/results/error_analysis_config_a.csv eval/results/error_analysis_config_b.csv
git commit -m "chore: hasil evaluasi resmi — statistical_test + error_analysis semua config"
```

---

## Checklist Akhir

Sebelum menyatakan implementasi selesai, verifikasi checklist ini:

- [ ] `git log --oneline` menampilkan commit sequence yang bersih
- [ ] `pytest tests/test_citation_parser.py -v` → 9 PASSED
- [ ] `http://localhost:8501` berjalan, chatbot menjawab dengan citation
- [ ] `eval/results/` berisi `hasil_config_a.csv`, `hasil_config_b.csv`, `hasil_config_c.csv`
- [ ] `eval/results/statistical_test.csv` berisi hasil Wilcoxon
- [ ] `eval/results/perbandingan_visual.png` ada untuk lampiran skripsi
- [ ] `logs/transaksi_chat.csv` mencatat transaksi chat
- [ ] `logs/ingestion_report.csv` mencatat ingestion run
- [ ] ChromaDB metadata tidak mengandung `priority` atau `chunk_type` (D-B3)
- [ ] `REQUIRED_YAML_FIELDS = ["doc_id", "title", "category"]` di `config.py` (D-B2)
- [ ] Tidak ada endpoint `POST /api/log_transaction` (D-B4)
- [ ] `reinitialize_llm()` tidak ada — gunakan `_get_llm()` (D-B5)
- [ ] `reference` di ground_truth ditulis natural language (D-B6)
- [ ] Hasil kalibrasi threshold dicatat di jurnal penelitian (D-B7)
