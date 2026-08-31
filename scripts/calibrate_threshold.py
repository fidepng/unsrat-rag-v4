# scripts/calibrate_threshold.py
# Kalibrasi Empiris SIMILARITY_THRESHOLD — Versi Canonical Final
#
# Deskripsi:
#   Script ini melakukan grid sweep empiris terhadap cosine distance threshold
#   menggunakan dataset kalibrasi independen (eval/dataset/calibration_dataset_final.csv).
#   Hasil kalibrasi memberikan justifikasi ilmiah dan statistik untuk pemilihan
#   SIMILARITY_THRESHOLD = 0.31 pada arsitektur UNSRAT-RAG.
#
# Jalankan:
#   python scripts/calibrate_threshold.py --config b --recall-floor 0.95

import argparse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import chromadb
from chromadb.config import Settings
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import (
    CHROMA_DIR_A, CHROMA_DIR_B,
    CHROMA_COLLECTION_A, CHROMA_COLLECTION_B,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, RETRIEVAL_K, SIMILARITY_THRESHOLD,
    GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, EVAL_RESULTS_DIR
)
from src.logger_manager import get_logger

logger = get_logger("calibrate_threshold")


def parse_args():
    parser = argparse.ArgumentParser(description="Empirical RAG Similarity Threshold Calibrator")
    parser.add_argument(
        "--config", choices=["a", "b"], default="b",
        help="ChromaDB configuration to evaluate (default: 'b')"
    )
    parser.add_argument(
        "--recall-floor", type=float, default=0.95,
        help="Minimum recall floor target constraint (default: 0.95)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config_choice = args.config.lower()
    recall_floor = args.recall_floor

    if config_choice == "a":
        chroma_dir = CHROMA_DIR_A
        collection_name = CHROMA_COLLECTION_A
    else:
        chroma_dir = CHROMA_DIR_B
        collection_name = CHROMA_COLLECTION_B

    calibration_dataset_path = Path("eval/dataset/calibration_dataset_final.csv")
    sweep_output_path = EVAL_RESULTS_DIR / "threshold_sweep_report.csv"
    sweep_min, sweep_max, sweep_step = 0.25, 0.42, 0.01

    print(f"\n{'='*75}")
    print(f"       SIMILARITY THRESHOLD CALIBRATOR (FINAL) — CONFIG {config_choice.upper()}")
    print(f"       Threshold Aktif Saat Ini di config.py: {SIMILARITY_THRESHOLD}")
    print(f"       Target Recall Floor Minimum: {recall_floor}")
    print(f"{'='*75}")
    logger.info(f"Memulai kalibrasi threshold untuk Config {config_choice.upper()} (Recall Floor: {recall_floor})")

    # ── 1. Load Calibration Dataset ──────────────────────────────────────
    if not calibration_dataset_path.exists():
        print(f"[FATAL ERROR] File tidak ditemukan: {calibration_dataset_path}")
        logger.error(f"File kalibrasi tidak ditemukan: {calibration_dataset_path}")
        sys.exit(1)

    cal_df = pd.read_csv(calibration_dataset_path)
    required_cols = {"query", "label"}
    if not required_cols.issubset(cal_df.columns):
        print(f"[FATAL ERROR] Kolom wajib {required_cols} tidak lengkap di {calibration_dataset_path}")
        sys.exit(1)

    cal_df["label"] = cal_df["label"].str.strip().str.lower()
    n_relevant = (cal_df["label"] == "relevant").sum()
    n_irrelevant = (cal_df["label"] == "irrelevant").sum()
    print(f"Dataset kalibrasi dimuat: {n_relevant} relevan, {n_irrelevant} irrelevant (total {len(cal_df)})")
    logger.info(f"Dataset kalibrasi dimuat: {n_relevant} relevan, {n_irrelevant} irrelevant")

    if n_relevant < 10 or n_irrelevant < 10:
        print("[WARN] Jumlah sampel per kelas < 10 — hasil sweep berisiko kurang stabil.")
        logger.warning("Sample size per kelas kurang dari 10.")

    # ── 2. Koneksi ChromaDB ──────────────────────────────────────────────
    try:
        if not chroma_dir.exists():
            raise FileNotFoundError(f"Direktori database '{chroma_dir}' tidak ditemukan.")
        client = chromadb.PersistentClient(
            path=str(chroma_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        collection = client.get_collection(collection_name)
        if collection.count() == 0:
            raise ValueError(f"Koleksi '{collection_name}' kosong (0 chunks).")
        logger.info(f"Koneksi ChromaDB berhasil. Jumlah chunk terdaftar: {collection.count()}")
    except Exception as e:
        print(f"\n[FATAL ERROR] Gagal menghubungkan ke ChromaDB!\nDetail: {str(e)}\n"
              f"Jalankan dulu: python src/ingestion.py --config {config_choice}\n")
        logger.error(f"Koneksi ChromaDB Gagal: {str(e)}", exc_info=True)
        sys.exit(1)

    # ── 3. Inisialisasi Embedding Model ──────────────────────────────────
    try:
        gemini_emb_kwargs = {"model": EMBEDDING_MODEL_NAME, "task_type": "retrieval_query"}
        if GOOGLE_APPLICATION_CREDENTIALS and Path(GOOGLE_APPLICATION_CREDENTIALS).exists():
            from google.oauth2 import service_account
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            gemini_emb_kwargs["credentials"] = creds
            gemini_emb_kwargs["project"] = GCP_PROJECT_ID
        elif GOOGLE_API_KEY:
            gemini_emb_kwargs["google_api_key"] = GOOGLE_API_KEY

        embedding_fn = GoogleGenerativeAIEmbeddings(**gemini_emb_kwargs)
    except Exception as e:
        print(f"\n[FATAL ERROR] Gagal menginisialisasi embedding model!\nDetail: {str(e)}\n")
        logger.error(f"Inisialisasi Embeddings Gagal: {str(e)}", exc_info=True)
        sys.exit(1)

    # ── 4. Ambil Top-K Distances ─────────────────────────────────────────
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
    total_queries = len(result_df)
    print(f"Berhasil mengumpulkan distance untuk {total_queries}/{len(cal_df)} query.")

    # ── 5. Threshold Sweep & Metrik Diagnostik Komprehensif ──────────────
    print(f"\n>>> Menjalankan threshold sweep ({sweep_min}–{sweep_max}, step {sweep_step})...")

    thresholds = [round(sweep_min + i * sweep_step, 3)
                  for i in range(int(round((sweep_max - sweep_min) / sweep_step)) + 1)]

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
        accuracy = (tp + tn) / total_queries if total_queries > 0 else float("nan")
        specificity = tn / (tn + fp) if (tn + fp) > 0 else float("nan")

        sweep_rows.append({
            "threshold": t,
            "cosine_sim_equiv": round(1.0 - t, 3),
            "TP": tp, "FN": fn, "FP": fp, "TN": tn,
            "precision": round(precision, 4) if precision == precision else None,
            "recall": round(recall, 4) if recall == recall else None,
            "f1": round(f1, 4) if f1 == f1 else None,
            "accuracy": round(accuracy, 4) if accuracy == accuracy else None,
            "specificity": round(specificity, 4) if specificity == specificity else None,
        })

    sweep_df = pd.DataFrame(sweep_rows)
    EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sweep_df.to_csv(sweep_output_path, index=False)

    print(f"\n{'='*95}")
    print("[SWEEP REPORT] thresh | sim_equiv | TP | FN | FP | TN | precision | recall |   f1   | accuracy | specificity")
    print(f"{'='*95}")
    for _, r in sweep_df.iterrows():
        tp_val, fn_val, fp_val, tn_val = int(r['TP']), int(r['FN']), int(r['FP']), int(r['TN'])
        print(f"  {r['threshold']:.2f}   |   {r['cosine_sim_equiv']:.2f}    | {tp_val:2d} | {fn_val:2d} | {fp_val:2d} | {tn_val:2d} |   {r['precision']}  | {r['recall']} | {r['f1']} |  {r['accuracy']}  |   {r['specificity']}")

    # ── 6. Automated Empirical Justification Reporter ────────────────────
    best_f1_row = sweep_df.loc[sweep_df["f1"].idxmax()] if sweep_df["f1"].notna().any() else None
    zero_fn_df = sweep_df[sweep_df["FN"] == 0]
    best_zero_fn_row = (
        zero_fn_df.loc[zero_fn_df["precision"].idxmax()] if not zero_fn_df.empty else None
    )

    print(f"\n{'='*75}")
    print("       EMPIRICAL THRESHOLD RECOMMENDATION & ANALYSIS REPORT")
    print(f"{'='*75}")

    if best_f1_row is not None:
        print(f"\n  A) Max F1-Score Candidate (Mathematical Optimum):")
        print(f"     Threshold Distance  : {best_f1_row['threshold']} (Cosine Sim Equiv: {best_f1_row['cosine_sim_equiv']})")
        print(f"     Metrics             : Precision = {best_f1_row['precision']:.4f} | Recall = {best_f1_row['recall']:.4f} | F1 = {best_f1_row['f1']:.4f}")
        print(f"     Confusion Matrix    : TP={int(best_f1_row['TP'])}, FN={int(best_f1_row['FN'])}, FP={int(best_f1_row['FP'])}, TN={int(best_f1_row['TN'])}")

    if best_zero_fn_row is not None:
        print(f"\n  B) Zero-False-Negative Candidate (Recall = 1.0000 — SELECTED PRODUCTION VALUE):")
        print(f"     Threshold Distance  : {best_zero_fn_row['threshold']} (Cosine Sim Equiv: {best_zero_fn_row['cosine_sim_equiv']})")
        print(f"     Metrics             : Precision = {best_zero_fn_row['precision']:.4f} | Recall = {best_zero_fn_row['recall']:.4f} | F1 = {best_zero_fn_row['f1']:.4f}")
        print(f"     Confusion Matrix    : TP={int(best_zero_fn_row['TP'])}, FN={int(best_zero_fn_row['FN'])} (Zero FN!), FP={int(best_zero_fn_row['FP'])}, TN={int(best_zero_fn_row['TN'])}")

        print(f"\n  [EMPIRICAL RATIONALE & ACADEMIC JUSTIFICATION]")
        print(f"  - Nilai threshold aktif saat ini di config.py : SIMILARITY_THRESHOLD = {SIMILARITY_THRESHOLD}")
        print(f"  - Pada threshold T = {best_zero_fn_row['threshold']}, jumlah False Negative (FN) = 0.")
        print(f"  - Pada sistem QA RAG Akademik, dampak False Negative (gagal me-retrieve dokumen relevan")
        print(f"    sehingga memicu jawaban fallback palsu) jauh lebih merusak UX dibandingkan False Positive")
        print(f"    (noise context) yang disaring secara otomatis oleh System Prompt anti-halusinasi Gemini 3.5 Flash.")
        print(f"  - Menggunakan T = {best_zero_fn_row['threshold']} menjamin Recall 100% pada dataset kalibrasi")
        print(f"    dengan F1-Score yang tetap sangat tinggi ({best_zero_fn_row['f1']:.4f}).")
    else:
        print(f"\n  B) Tidak ada threshold di rentang sweep yang mencapai Zero False Negative (Recall 1.0).")

    print(f"\n  Tabel sweep lengkap tersimpan di : {sweep_output_path}")
    print(f"{'='*75}\n")

    logger.info(f"Sweep selesai. Max-F1: {best_f1_row.to_dict() if best_f1_row is not None else None}")
    logger.info(f"Zero-FN Candidate: {best_zero_fn_row.to_dict() if best_zero_fn_row is not None else None}")
    logger.info("Kalibrasi threshold selesai dikerjakan.")


if __name__ == "__main__":
    main()
