# evaluation.py — Pipeline Evaluasi Ragas + Wilcoxon + Error Analysis + Chart
# PRD Reference: Section 12, FR-15–FR-17, FR-21–FR-25, FR-31


import argparse
import csv
import time
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon as scipy_wilcoxon

from src.config import (
    EVAL_DATASET_PATH, EVAL_RESULTS_DIR,
    METRICS_COLS, OPTIONAL_METRICS_COLS, ERROR_ANALYSIS_N,
    EVALUATOR_MODEL_NAME, LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, GOOGLE_API_KEY,
)
# Ragas imports — VERIFIKASI dengan `use context7` sebelum implementasi
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

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

        # NVIDIA NIM Rate Limit Compliance (40 RPM limit)
        # 1.5 seconds delay between requests prevents quota exhaustion on NIM integrate endpoints.
        if any(m in LLM_MODEL_NAME.lower() for m in ["llama", "qwen", "gemma"]):
            logger.info("Jeda 1.5s untuk mematuhi rate limit NVIDIA NIM (40 RPM)...")
            time.sleep(1.5)

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

    # Initialize custom LLM and Embeddings wrappers for Gemini / NVIDIA NIM
    import os
    nvidia_api_key = os.getenv("NVIDIA_NIM_API_KEY")
    if nvidia_api_key:
        evaluator_model = EVALUATOR_MODEL_NAME
        if evaluator_model == "gemma-4-31b-it":
            evaluator_model = "google/gemma-4-31b-it"
        elif evaluator_model == "llama-3.3-nemotron-super-49b-v1.5":
            evaluator_model = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
        elif evaluator_model == "llama-3.1-nemotron-nano-8b-v1":
            evaluator_model = "nvidia/llama-3.1-nemotron-nano-8b-v1"
        elif evaluator_model == "llama-3.1-70b-instruct":
            evaluator_model = "meta/llama-3.1-70b-instruct"
        elif evaluator_model == "llama-3.1-8b-instruct":
            evaluator_model = "meta/llama-3.1-8b-instruct"
        logger.info(f"NVIDIA_NIM_API_KEY ditemukan. Menggunakan NVIDIA NIM ({evaluator_model}) sebagai evaluator.")
        from langchain_openai import ChatOpenAI
        evaluator_llm = LangchainLLMWrapper(ChatOpenAI(
            model=evaluator_model,
            api_key=nvidia_api_key,
            openai_api_base="https://integrate.api.nvidia.com/v1",
            temperature=0.0,
            max_tokens=1024,
        ))
        logger.info("Menggunakan Google Gemini (models/gemini-embedding-001) sebagai evaluator embeddings untuk menghindari error 500 NIM.")
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        evaluator_embeddings = LangchainEmbeddingsWrapper(GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
        ))
    else:
        logger.info(f"NVIDIA_NIM_API_KEY tidak ditemukan. Menggunakan Google Gemini ({EVALUATOR_MODEL_NAME}) sebagai evaluator.")
        evaluator_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(
            model=EVALUATOR_MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.0,
        ))
        evaluator_embeddings = LangchainEmbeddingsWrapper(GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
        ))

    # Assign custom LLM and Embeddings to each metric
    for metric in base_metrics:
        if hasattr(metric, "llm"):
            metric.llm = evaluator_llm
        if hasattr(metric, "embeddings"):
            metric.embeddings = evaluator_embeddings

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
    for metric in METRICS_COLS + ["response_time_seconds"]:
        if metric not in df_a.columns or metric not in df_b.columns:
            continue
        scores_a = df_a[metric].dropna()
        scores_b = df_b[metric].dropna()

        try:
            stat, p_value = scipy_wilcoxon(scores_a, scores_b)
            significant = p_value < 0.05
            winner = None
            if significant:
                if metric == "response_time_seconds":
                    winner = "Config B" if scores_b.mean() < scores_a.mean() else "Config A"
                else:
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
