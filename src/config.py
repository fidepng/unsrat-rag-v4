# src/config.py — CANONICAL CONFIGURATION FILE

import os
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress library deprecation and future warnings from underlying SDKs
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

# ── PATH ────────────────────────────────────────────────────
ROOT_DIR          = Path(__file__).parent.parent
CORPUS_DIR        = ROOT_DIR / "data" / "corpus"
CHROMA_BASE_DIR   = ROOT_DIR / "chroma_db"
CHROMA_DIR_A      = CHROMA_BASE_DIR / "config_a"
CHROMA_DIR_B      = CHROMA_BASE_DIR / "config_b"
BM25_INDEX_DIR    = ROOT_DIR / "bm25_index"
BM25_INDEX_PATH   = BM25_INDEX_DIR / "bm25_index.pkl"
EVAL_DATASET_PATH = ROOT_DIR / "eval" / "dataset" / "ground_truth.csv"
EVAL_RESULTS_DIR  = ROOT_DIR / "eval" / "results"
LOGS_DIR          = ROOT_DIR / "logs"
SYSTEM_LOG_PATH      = LOGS_DIR / "unsrat_rag.log"
CHAT_LOG_PATH        = LOGS_DIR / "transaksi_chat.csv"
INGESTION_LOG_PATH   = LOGS_DIR / "ingestion_report.csv"

# ── CHROMADB COLLECTIONS ────────────────────────────────────
CHROMA_COLLECTION_A = "unsrat_rag_config_a"
CHROMA_COLLECTION_B = "unsrat_rag_config_b"
CHROMA_DISTANCE_FN  = "cosine"

# ── MODEL ───────────────────────────────────────────────────
# Generator dan evaluator HARUS BERBEDA (D-16 — mitigasi self-eval bias)
LLM_MODEL_NAME       = "llama-3.1-8b-instruct"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"
EVALUATOR_MODEL_NAME = "llama-3.1-8b-instruct"

# Daftar model yang bisa dipilih di UI sidebar
# Catatan: model NVIDIA NIM menggunakan provider "openai_compatible" (lihat Section 18)
AVAILABLE_MODELS: list[str] = [
    "gemini-3.5-flash",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "llama-3.1-8b-instruct",
]

# ── CHUNKING — CONFIG A ──────────────────────────────────────
CHUNK_SIZE_A    = 500
CHUNK_OVERLAP_A = 100

# ── CHUNKING — CONFIG B ──────────────────────────────────────
CHUNK_SIZE_B    = 2000
CHUNK_OVERLAP_B = 200

# ── SEPARATORS ───────────────────────────────────────────────
CHUNK_SEPARATORS = ["\n\n", "\n", " ", ""]

# ── REQUIRED YAML FIELDS ─────────────────────────────────────────────
REQUIRED_YAML_FIELDS = [
    "doc_id", "title", "category",
    # CATATAN (D-B2): Hanya 3 field yang benar-benar dikonsumsi kode runtime.
    # Field lain (content_type, valid_from, status, retrieval_summary,
    # chunk_strategy, last_updated) tetap BOLEH ada di YAML sebagai dokumentasi,
    # tapi tidak divalidasi. File di data/corpus/ dianggap aktif by convention.
]

# ── RETRIEVAL ────────────────────────────────────────────────
RETRIEVAL_K          = 4
SIMILARITY_THRESHOLD = 0.65
MIN_CHUNK_LENGTH     = 50

# ── BM25 — CONFIG C ──────────────────────────────────────────
BM25_K             = 4
BM25_MIN_TOKEN_LEN = 2

# ── LLM GENERATION ──────────────────────────────────────────
LLM_TEMPERATURE       = 0.1
LLM_MAX_OUTPUT_TOKENS = 2048
LLM_TOP_P             = 0.95

# ── MEMORI ──────────────────────────────────────────────────
MEMORY_K = 5

# ── RETRY POLICY ────────────────────────────────────────────
# CATATAN: Dua policy berbeda untuk dua konteks berbeda.
# chain.py (interaktif, user menunggu) — policy ringan:
MAX_RETRIES  = 3
RETRY_DELAYS = [2, 5]   # detik: attempt 2 tunggu 2 detik, attempt 3 tunggu 5 detik

# ingestion.py (batch, rate-limit sensitif) — menggunakan konstanta LOKAL di ingestion.py:
# MAX_RETRIES_INGESTION = 5 dengan exponential backoff hingga 50 detik
# Didefinisikan di src/ingestion.py agar tidak mencemari namespace chain.py
# INTER_CHUNK_SLEEP = 0.2  # jeda antar chunk untuk menghindari quota burst

# ── EVALUASI ─────────────────────────────────────────────────
# Metrik wajib yang selalu dijalankan:
METRICS_COLS = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
]

# Metrik opsional — tidak dijalankan secara default karena butuh LLM call tambahan.
# Kode evaluation.py harus siap menerima metrik ini via flag --extra-metrics.
# context_entity_recall: mengukur apakah entitas penting (nama pasal, angka SKS,
# tanggal) tercantum dalam konteks yang diambil — sangat relevan untuk domain akademik.
# Aktifkan dengan: python evaluation.py --config a --extra-metrics context_entity_recall
OPTIONAL_METRICS_COLS = [
    "context_entity_recall",
    # Tambahkan metrik opsional lain di sini di masa depan
]

ERROR_ANALYSIS_N = 10

# ── REQUIRED YAML FIELDS — dikelola di atas (D-B2) ──────────

# ── SYSTEM PROMPT (TERKUNCI) ─────────────────────────────────
# CATATAN INLINE CITATION: Prompt ini menginstruksikan LLM untuk menyisipkan
# [N] di dalam teks jawaban pada bagian yang bersumber dari
# dokumen. chain.py akan mem-parsing marker ini untuk menghasilkan
# citation_sources yang akurat. Lihat Section 6.5 untuk spesifikasi parsing lengkap.
SYSTEM_PROMPT = """Anda adalah agen asisten informasi akademik resmi Universitas Sam Ratulangi.
Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan dokumen konteks yang disediakan di bawah ini.

PENTING: Jangan gunakan pengetahuan Anda di luar dokumen konteks yang disediakan, meskipun Anda mengetahuinya dari sumber lain.

Setiap klaim atau informasi dalam jawaban Anda HARUS disertai dengan penanda referensi inline berbentuk [N] di akhir kalimat yang bersumber dari dokumen tersebut, di mana N adalah nomor sumber yang tersedia dalam konteks.

Contoh format jawaban yang benar:
"Mahasiswa dapat mengambil maksimal 24 SKS per semester [1]. Kalender akademik semester genap dimulai pada Februari 2026 [2]."

Jika jawaban tidak ada di dalam dokumen konteks, katakan secara jujur bahwa Anda tidak menemukan informasinya dan arahkan mereka untuk menghubungi bagian administrasi kampus. Dalam kasus ini, jangan gunakan penanda referensi.

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
API_HOST = "0.0.0.0"
API_PORT = 8501

# ── API KEY ──────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY tidak ditemukan!\n"
        "Buat file .env di root proyek dan isi: GOOGLE_API_KEY=your_key_here"
    )

# NVIDIA NIM API Key (opsional — hanya dibutuhkan jika menggunakan provider NIM)
NVIDIA_NIM_API_KEY = os.getenv("NVIDIA_NIM_API_KEY")  # None jika tidak di-set, tidak crash
