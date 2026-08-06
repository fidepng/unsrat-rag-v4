# scripts/calibrate_threshold_final.py
# Kalibrasi empiris SIMILARITY_THRESHOLD — versi FINAL (D-B7 revisi)
#
# Perbedaan dari versi lama (calibrate_threshold.py):
#   1. Sumber data: eval/dataset/calibration_dataset_final.csv (20 relevan + 20 irrelevant),
#      bukan 5+5 query hardcoded di dalam script.
#   2. Set ini terverifikasi TIDAK overlap dengan eval/dataset/ground_truth.csv
#      (dicek manual dengan difflib sebelum file ini dibuat — lihat catatan di README kalibrasi).
#   3. Distance diambil top-1 SAMPAI top-K (bukan cuma top-1), karena RETRIEVAL_K
#      chunk semuanya disaring oleh threshold yang sama di produksi.
#   4. Metode threshold sweep (precision/recall/F1 di banyak titik), bukan formula
#      margin tunggal (max_relevan + 0.01) — lebih tahan terhadap outlier pada n kecil.
#   5. Definisi keputusan per query: "lolos" jika MINIMAL 1 dari K chunk berjarak
#      <= threshold (persis logika retrieval produksi: fallback dipicu hanya jika
#      SEMUA kandidat tersaring).
#
# Jalankan: python scripts/calibrate_threshold_final.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import chromadb
from chromadb.config import Settings
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import (
    CHROMA_DIR_B, CHROMA_COLLECTION_B,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, RETRIEVAL_K, SIMILARITY_THRESHOLD,
    GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID
)
from src.logger_manager import get_logger

logger = get_logger("calibrate_threshold_final")

CALIBRATION_DATASET_PATH = Path("eval/dataset/calibration_dataset_final.csv")
SWEEP_OUTPUT_PATH        = Path("eval/results/threshold_sweep_report.csv")
SWEEP_MIN, SWEEP_MAX, SWEEP_STEP = 0.25, 0.42, 0.01
RECALL_FLOOR = 0.95  # ambang recall minimum yang ingin dijaga (lihat justifikasi di bagian akhir)

print(f"\n{'='*70}")
print("       SIMILARITY THRESHOLD CALIBRATOR (FINAL) — CONFIG B")
print(f"       Threshold Aktif Saat Ini di config.py: {SIMILARITY_THRESHOLD}")
print(f"{'='*70}")
logger.info("Memulai kalibrasi threshold versi final (sweep precision/recall/F1)")

# ── 1. Load calibration dataset ──────────────────────────────────────
if not CALIBRATION_DATASET_PATH.exists():
    print(f"[FATAL ERROR] File tidak ditemukan: {CALIBRATION_DATASET_PATH}")
    logger.error(f"File kalibrasi tidak ditemukan: {CALIBRATION_DATASET_PATH}")
    sys.exit(1)

cal_df = pd.read_csv(CALIBRATION_DATASET_PATH)
required_cols = {"query", "label"}
if not required_cols.issubset(cal_df.columns):
    print(f"[FATAL ERROR] Kolom wajib {required_cols} tidak lengkap di {CALIBRATION_DATASET_PATH}")
    sys.exit(1)

cal_df["label"] = cal_df["label"].str.strip().str.lower()
n_relevant = (cal_df["label"] == "relevant").sum()
n_irrelevant = (cal_df["label"] == "irrelevant").sum()
print(f"Dataset kalibrasi dimuat: {n_relevant} relevan, {n_irrelevant} irrelevant "
      f"(total {len(cal_df)})")
logger.info(f"Dataset kalibrasi: {n_relevant} relevan, {n_irrelevant} irrelevant")

if n_relevant < 10 or n_irrelevant < 10:
    print("[WARN] Jumlah sampel per kelas < 10 — hasil sweep berisiko kurang stabil. "
          "Tetap dilanjutkan, tapi laporkan keterbatasan ini di metodologi skripsi.")
    logger.warning("Sample size per kelas kurang dari 10.")

# ── 2. Koneksi ChromaDB ──────────────────────────────────────────────
try:
    if not CHROMA_DIR_B.exists():
        raise FileNotFoundError(f"Direktori database '{CHROMA_DIR_B}' tidak ditemukan.")
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR_B),
        settings=Settings(anonymized_telemetry=False)
    )
    collection = client.get_collection(CHROMA_COLLECTION_B)
    if collection.count() == 0:
        raise ValueError(f"Koleksi '{CHROMA_COLLECTION_B}' kosong (0 chunks).")
    logger.info(f"Koneksi ChromaDB berhasil. Jumlah chunk terdaftar: {collection.count()}")
except Exception as e:
    print(f"\n[FATAL ERROR] Gagal menghubungkan ke ChromaDB!\nDetail: {str(e)}\n"
          f"Jalankan dulu: python src/ingestion.py\n")
    logger.error(f"Koneksi ChromaDB Gagal: {str(e)}", exc_info=True)
    sys.exit(1)

# ── 3. Inisialisasi embedding model ──────────────────────────────────
try:
    gemini_emb_kwargs = {"model": EMBEDDING_MODEL_NAME, "task_type": "retrieval_query"}
    if GOOGLE_APPLICATION_CREDENTIALS:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        gemini_emb_kwargs["credentials"] = creds
        gemini_emb_kwargs["project"] = GCP_PROJECT_ID
    else:
        gemini_emb_kwargs["google_api_key"] = GOOGLE_API_KEY
    embedding_fn = GoogleGenerativeAIEmbeddings(**gemini_emb_kwargs)
except Exception as e:
    print(f"\n[FATAL ERROR] Gagal menginisialisasi embedding model!\nDetail: {str(e)}\n")
    logger.error(f"Inisialisasi Embeddings Gagal: {str(e)}", exc_info=True)
    sys.exit(1)

# ── 4. Ambil distance top-K untuk semua query ────────────────────────
print(f"\n>>> Mengambil distance top-{RETRIEVAL_K} untuk {len(cal_df)} query...")
records = []
for _, row in cal_df.iterrows():
    q, label = row["query"], row["label"]
    try:
        emb = embedding_fn.embed_query(str(q))
        res = collection.query(query_embeddings=[emb], n_results=RETRIEVAL_K, include=["distances"])
        dists = res["distances"][0]
        if not dists:
            print(f"  [WARN] Query tanpa hasil sama sekali: '{str(q)[:50]}...'")
            logger.warning(f"Query tanpa hasil: '{q}'")
            continue
        records.append({"query": q, "label": label, "distances": dists, "min_distance": min(dists)})
        logger.debug(f"'{q}' [{label}] -> {dists}")
    except Exception as e:
        print(f"  [ERROR] Gagal memproses query '{str(q)[:50]}...': {e}")
        logger.error(f"Gagal memproses query '{q}': {e}")

if not records:
    print("[FATAL ERROR] Tidak ada data distance yang berhasil dikumpulkan.")
    sys.exit(1)

result_df = pd.DataFrame(records)
print(f"Berhasil mengumpulkan distance untuk {len(result_df)}/{len(cal_df)} query.")

# ── 5. Threshold sweep: precision / recall / F1 ──────────────────────
# Definisi keputusan (identik dgn logika retrieval produksi):
#   Query "lolos" pada suatu threshold T jika MINIMAL 1 dari K chunk berjarak <= T.
#   TP = relevan & lolos | FN = relevan & tidak lolos (-> fallback, seharusnya jawab)
#   FP = irrelevant & lolos (-> retrieval "salah nyambung")  | TN = irrelevant & tidak lolos
print(f"\n>>> Menjalankan threshold sweep ({SWEEP_MIN}–{SWEEP_MAX}, step {SWEEP_STEP})...")

thresholds = [round(SWEEP_MIN + i * SWEEP_STEP, 3)
              for i in range(int(round((SWEEP_MAX - SWEEP_MIN) / SWEEP_STEP)) + 1)]

sweep_rows = []
for t in thresholds:
    tp = fn = fp = tn = 0
    for _, r in result_df.iterrows():
        passed = any(d <= t for d in r["distances"])
        if r["label"] == "relevant":
            if passed: tp += 1
            else: fn += 1
        else:
            if passed: fp += 1
            else: tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
    recall    = tp / (tp + fn) if (tp + fn) > 0 else float("nan")
    f1 = (2 * precision * recall / (precision + recall)
          if (precision == precision and recall == recall and (precision + recall) > 0)
          else float("nan"))

    sweep_rows.append({
        "threshold": t, "TP": tp, "FN": fn, "FP": fp, "TN": tn,
        "precision": round(precision, 4) if precision == precision else None,
        "recall": round(recall, 4) if recall == recall else None,
        "f1": round(f1, 4) if f1 == f1 else None,
    })

sweep_df = pd.DataFrame(sweep_rows)
SWEEP_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
sweep_df.to_csv(SWEEP_OUTPUT_PATH, index=False)

print(f"\n{'='*70}")
print("[SWEEP TABLE] threshold | precision | recall | f1")
print(f"{'='*70}")
for _, r in sweep_df.iterrows():
    print(f"  {r['threshold']:.2f}   |   {r['precision']}   |  {r['recall']}  |  {r['f1']}")

# ── 6. Rekomendasi: dua kandidat, dua justifikasi berbeda ────────────
best_f1_row = sweep_df.loc[sweep_df["f1"].idxmax()] if sweep_df["f1"].notna().any() else None

recall_ok = sweep_df[sweep_df["recall"] >= RECALL_FLOOR]
best_recall_constrained_row = (
    recall_ok.loc[recall_ok["precision"].idxmax()] if not recall_ok.empty else None
)

print(f"\n{'='*70}")
print("[RECOMMENDATION] DUA KANDIDAT THRESHOLD DENGAN JUSTIFIKASI BERBEDA")
print(f"{'='*70}")

if best_f1_row is not None:
    print(f"\n  A) Max F1 (keseimbangan precision & recall):")
    print(f"     threshold = {best_f1_row['threshold']}, "
          f"precision = {best_f1_row['precision']}, recall = {best_f1_row['recall']}, "
          f"f1 = {best_f1_row['f1']}")
else:
    print("\n  A) Max F1: tidak dapat dihitung (data precision/recall tidak lengkap).")

if best_recall_constrained_row is not None:
    print(f"\n  B) Recall-constrained (recall >= {RECALL_FLOOR}, precision setinggi mungkin):")
    print(f"     threshold = {best_recall_constrained_row['threshold']}, "
          f"precision = {best_recall_constrained_row['precision']}, "
          f"recall = {best_recall_constrained_row['recall']}, "
          f"f1 = {best_recall_constrained_row['f1']}")
    print(f"\n  [SARAN] Untuk sistem tanya-jawab akademik seperti UNSRAT-RAG, di mana fallback\n"
          f"          palsu (FN) berdampak lebih buruk ke pengalaman pengguna daripada retrieval\n"
          f"          noise (FP) yang masih bisa disaring LLM lewat SYSTEM_PROMPT anti-halusinasi,\n"
          f"          opsi B (recall-constrained) LEBIH DISARANKAN sebagai nilai final.")
else:
    print(f"\n  B) Tidak ada threshold di rentang sweep yang mencapai recall >= {RECALL_FLOOR}. "
          f"Pertimbangkan memperlebar SWEEP_MAX atau mengecek ulang kualitas embedding/corpus.")

print(f"\n  Nilai saat ini di config.py: SIMILARITY_THRESHOLD = {SIMILARITY_THRESHOLD}")
print(f"  Tabel sweep lengkap tersimpan di: {SWEEP_OUTPUT_PATH}")
print(f"{'='*70}\n")

logger.info(f"Sweep selesai. Kandidat max-F1: {best_f1_row.to_dict() if best_f1_row is not None else None}")
logger.info(f"Kandidat recall-constrained: "
            f"{best_recall_constrained_row.to_dict() if best_recall_constrained_row is not None else None}")
logger.info("Kalibrasi threshold (final) selesai dikerjakan.")
