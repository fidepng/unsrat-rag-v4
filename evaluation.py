# evaluation.py — Pipeline Evaluasi Ragas + Wilcoxon + Error Analysis + Chart
# PRD Reference: Section 12, FR-15–FR-17, FR-21–FR-25, FR-31

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon as scipy_wilcoxon

from src.config import (
    ROOT_DIR, EVAL_DATASET_PATH, EVAL_RESULTS_DIR,
    METRICS_COLS, OPTIONAL_METRICS_COLS, ERROR_ANALYSIS_N,
    EVALUATOR_MODEL_NAME, LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, GOOGLE_API_KEY,
    GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID,
    EVAL_QUERY_DELAY_GOOGLE, EVAL_QUERY_DELAY_NIM,
)
# Ragas imports — VERIFIKASI dengan `use context7` sebelum implementasi
# --- BEGIN RAGAS COMPATIBILITY HACK ---
import sys, types
if 'langchain_community.chat_models' not in sys.modules:
    sys.modules['langchain_community.chat_models'] = types.ModuleType('langchain_community.chat_models')
if 'langchain_community.chat_models.vertexai' not in sys.modules:
    dummy_cv = types.ModuleType('langchain_community.chat_models.vertexai')
    dummy_cv.ChatVertexAI = None
    sys.modules['langchain_community.chat_models.vertexai'] = dummy_cv
if 'langchain_community.llms' not in sys.modules:
    dummy_llms = types.ModuleType('langchain_community.llms')
    dummy_llms.VertexAI = None
    sys.modules['langchain_community.llms'] = dummy_llms
# --- END RAGAS COMPATIBILITY HACK ---

from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas import RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src.chain import get_response
from src.logger_manager import get_logger
from src.preflight import preflight_check

logger = get_logger("evaluation")

NIM_MODEL_MAP = {
    "gemma-4-31b-it": "google/gemma-4-31b-it",
    "llama-3.3-nemotron-super-49b-v1.5": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "llama-3.1-nemotron-nano-8b-v1": "nvidia/llama-3.1-nemotron-nano-8b-v1",
    "llama-3.1-70b-instruct": "meta/llama-3.1-70b-instruct",
    "llama-3.1-8b-instruct": "meta/llama-3.1-8b-instruct",
    "deepseek-v4-flash": "deepseek-ai/deepseek-v4-flash",
    "deepseek-v4-pro": "deepseek-ai/deepseek-v4-pro",
}




def _backup_ground_truth() -> tuple[str, Path]:
    """
    Hitung hash SHA256 dari ground_truth.csv (12 karakter pertama).
    Simpan salinan ke eval/dataset/archive/ground_truth_{gt_hash}.csv jika belum ada.
    Return (gt_hash, archive_gt_path).
    """
    if not EVAL_DATASET_PATH.exists():
        raise FileNotFoundError(f"Ground truth tidak ditemukan: {EVAL_DATASET_PATH}")

    content = EVAL_DATASET_PATH.read_bytes()
    gt_hash = hashlib.sha256(content).hexdigest()[:12]

    archive_dir = EVAL_DATASET_PATH.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    archive_gt_path = archive_dir / f"ground_truth_{gt_hash}.csv"
    if not archive_gt_path.exists():
        archive_gt_path.write_bytes(content)
        logger.info(f"Ground truth di-backup ke {archive_gt_path}")

    return gt_hash, archive_gt_path


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
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            corrupt_path = archive_dir / f"run_manifest.json.corrupt_{timestamp}"
            try:
                shutil.copy2(manifest_path, corrupt_path)
            except Exception as copy_err:
                logger.error(f"Gagal membuat backup manifest corrupt: {copy_err}")
            logger.error(f"Gagal membaca manifest file: {e}. Backup dibuat di {corrupt_path}. Menggunakan manifest baru.")
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


def _slugify_model(model_name: str) -> str:
    name = model_name.split("/")[-1].lower()
    return re.sub(r'[^a-z0-9]', '', name)


def _make_model_slug(generator_model: str, evaluator_model: str) -> str:
    gen_slug = _slugify_model(generator_model)
    eval_slug = _slugify_model(evaluator_model)
    return f"{gen_slug}_{eval_slug}"


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


def run_evaluation(
    config: str,
    extra_metrics: list[str] | None = None,
    limit: int | None = None,
    generator_model: str | None = None,
    evaluator_model: str | None = None,
) -> None:
    """
    Jalankan evaluasi Ragas untuk config tertentu.

    Hasil disimpan ke eval/results/hasil_config_{config}.csv
    dan error_analysis_config_{config}.csv.

    (FR-15, FR-16, FR-21, FR-23, FR-25, FR-31)
    """
    llm_model = generator_model if generator_model else LLM_MODEL_NAME
    eval_model = evaluator_model if evaluator_model else EVALUATOR_MODEL_NAME

    # Preflight Health Check API Readiness
    pf_res = preflight_check(
        require_google=True,
        require_nim=False,
        generator_model=llm_model,
        evaluator_model=eval_model,
    )
    if not pf_res.get("overall_ok", False):
        print("\n" + "=" * 60)
        print("PERINGATAN PRE-FLIGHT HEALTH CHECK")
        print("=" * 60)
        for svc_name, status in pf_res.get("services", {}).items():
            if not status.get("ok"):
                print(f" - [{svc_name}]: GAGAL -> {status.get('error')}")
            else:
                print(f" - [{svc_name}]: OK ({status.get('latency_ms')} ms)")
        print("=" * 60)

        user_choice = input("PERINGATAN PRE-FLIGHT: Beberapa API mengalami kendala. Lanjutkan evaluasi? (y/n): ")
        if user_choice.strip().lower() != "y":
            logger.warning("Evaluasi dibatalkan oleh pengguna karena kendala pre-flight check.")
            sys.exit(1)

    logger.info(f"=== Evaluasi Config {config.upper()} dimulai ===")
    logger.info(f"Generator: {llm_model} | Evaluator: {eval_model}")
    logger.info("PERINGATAN: Pastikan model evaluator sama untuk semua config! (Section 18.5)")

    df = _load_ground_truth()
    if limit is not None:
        df = df.head(limit)
        logger.info(f"Evaluasi dibatasi ke {limit} baris pertama untuk pengujian.")
    EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    gt_hash, _ = _backup_ground_truth()

    start_dt = datetime.now(timezone.utc)
    run_id = f"{config}_{start_dt.strftime('%Y%m%d_%H%M%S')}"

    run_entry = {
        "run_id": run_id,
        "config": config,
        "timestamp_start": start_dt.isoformat(),
        "timestamp_end": None,
        "status": "running",
        "generator_model": llm_model,
        "generator_provider": "google" if "gemini" in llm_model.lower() else "nvidia_nim",
        "evaluator_model": eval_model,
        "evaluator_provider": "google" if "gemini" in eval_model.lower() else "nvidia_nim",
        "embedding_model": EMBEDDING_MODEL_NAME,
        "ground_truth_hash": gt_hash,
        "total_queries": len(df),
        "success_count": 0,
        "error_count": 0,
        "metrics": {},
        "archive_file": None,
        "is_active": False,
    }

    manifest = _load_manifest()
    manifest["runs"].append(run_entry)
    _save_manifest(manifest)

    try:
        results = []
        success_cnt = 0
        err_cnt = 0

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
                model_name=llm_model,
                streaming=False,
            )
            elapsed = time.time() - start_time

            answer_str = resp.get("answer", "")
            if "Terjadi gangguan" in answer_str:
                err_cnt += 1
            else:
                success_cnt += 1

            # Rate Limit Compliance (Dynamic delay based on generator model)
            if "gemini" in llm_model.lower():
                delay = EVAL_QUERY_DELAY_GOOGLE
            else:
                delay = EVAL_QUERY_DELAY_NIM

            logger.info(f"Jeda {delay:.1f}s untuk mematuhi rate limit model generator ({llm_model})...")
            time.sleep(delay)

            results.append({
                "user_input":           query,
                "reference":            reference,
                "response":             answer_str,
                # FR-31: retrieved_contexts = SEMUA chunk lolos threshold (bukan hanya citation_sources)
                "retrieved_contexts":   resp["retrieved_contexts"],
                "citation_sources_count": len(resp["citation_sources"]),
                "response_time_seconds": round(elapsed, 4),
                "category":             row.get("category", ""),
                "source_doc":           row.get("source_doc", ""),
            })

        # ── FR-CHECKPOINT: simpan hasil generasi SEBELUM Ragas evaluate() ──────
        # Rationale: fase generasi (get_response per query) mahal & rate-limited.
        # Jika ragas.evaluate() gagal (rate limit, parsing error, dsb.), hasil
        # generasi yang sudah didapat tidak boleh hilang begitu saja.
        checkpoint_path = EVAL_RESULTS_DIR / f"_checkpoint_config_{config}_{run_id}.csv"
        try:
            pd.DataFrame(results).to_csv(checkpoint_path, index=False, encoding="utf-8-sig")
            logger.info(f"Checkpoint hasil generasi disimpan: {checkpoint_path}")
        except Exception as e:
            # Kegagalan checkpoint tidak boleh menghentikan pipeline evaluasi,
            # tapi wajib dicatat sebagai warning karena mengurangi ketahanan run.
            logger.warning(f"Gagal menyimpan checkpoint hasil generasi: {e}")

        # Ragas evaluation
        logger.info("Menjalankan Ragas evaluate()...")

        # Konfigurasi Paralel yang Aman untuk Menghindari Timeout
        run_config = RunConfig(max_workers=4, timeout=600, max_retries=10)

        # Initialize custom LLM and Embeddings wrappers for Gemini / NVIDIA NIM
        # Siapkan kwargs untuk Gemini agar mendukung GOOGLE_APPLICATION_CREDENTIALS (GCP Billed)
        gemini_llm_kwargs = {
            "model": eval_model,
            "temperature": 0.0,
            "max_retries": 2,
            "timeout": 120,
        }
        gemini_emb_kwargs = {
            "model": EMBEDDING_MODEL_NAME,
            "max_retries": 2,
            "timeout": 60,
        }
        
        if GOOGLE_APPLICATION_CREDENTIALS:
            from google.oauth2 import service_account
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            gemini_llm_kwargs["credentials"] = creds
            gemini_llm_kwargs["project"] = GCP_PROJECT_ID
            gemini_emb_kwargs["credentials"] = creds
            gemini_emb_kwargs["project"] = GCP_PROJECT_ID
        else:
            gemini_llm_kwargs["google_api_key"] = GOOGLE_API_KEY
            gemini_emb_kwargs["google_api_key"] = GOOGLE_API_KEY

        import os
        nvidia_api_key = os.getenv("NVIDIA_NIM_API_KEY")
        if nvidia_api_key and ("gemini" not in eval_model.lower()):
            evaluator_model_name = NIM_MODEL_MAP.get(eval_model, eval_model)
            logger.info(f"NVIDIA_NIM_API_KEY ditemukan. Menggunakan NVIDIA NIM ({evaluator_model_name}) sebagai evaluator.")
            from langchain_openai import ChatOpenAI
            evaluator_llm = LangchainLLMWrapper(ChatOpenAI(
                model=evaluator_model_name,
                api_key=nvidia_api_key,
                openai_api_base="https://integrate.api.nvidia.com/v1",
                temperature=0.0,
                max_tokens=4096,
                max_retries=2,
                timeout=120,
            ))
            logger.info("Menggunakan Google Gemini (models/gemini-embedding-001) sebagai evaluator embeddings untuk menghindari error 500 NIM.")
            evaluator_embeddings = LangchainEmbeddingsWrapper(GoogleGenerativeAIEmbeddings(**gemini_emb_kwargs))
        else:
            logger.info(f"NVIDIA_NIM_API_KEY tidak ditemukan. Menggunakan Google Gemini ({eval_model}) sebagai evaluator.")
            evaluator_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(**gemini_llm_kwargs))
            evaluator_embeddings = LangchainEmbeddingsWrapper(GoogleGenerativeAIEmbeddings(**gemini_emb_kwargs))

        # Metrik yang dijalankan (Ragas v0.4 class-based initialization)
        base_metrics = [
            Faithfulness(llm=evaluator_llm),
            AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
            ContextPrecision(llm=evaluator_llm),
            ContextRecall(llm=evaluator_llm)
        ]
        
        # Tambah metrik opsional jika diminta
        if extra_metrics:
            for m_name in extra_metrics:
                if m_name in OPTIONAL_METRICS_COLS:
                    if m_name == "context_entity_recall":
                        try:
                            from ragas.metrics import ContextEntityRecall
                            base_metrics.append(ContextEntityRecall(llm=evaluator_llm))
                            logger.info(f"Metrik opsional ditambahkan: {m_name}")
                        except ImportError:
                            logger.warning(f"Metrik opsional {m_name} tidak tersedia di versi Ragas ini.")

        try:
            from ragas import EvaluationDataset, SingleTurnSample
            
            samples = []
            for r in results:
                sample = SingleTurnSample(
                    user_input=r["user_input"],
                    response=r["response"],
                    retrieved_contexts=r["retrieved_contexts"],
                    reference=r["reference"]
                )
                samples.append(sample)
                
            ragas_dataset = EvaluationDataset(samples=samples)

            ragas_result = evaluate(
                dataset=ragas_dataset,
                metrics=base_metrics,
                run_config=run_config,
            )
            ragas_df = ragas_result.to_pandas()
        except Exception as e:
            logger.error(f"Ragas evaluate() gagal: {e}")
            logger.error("Pastikan Ragas v0.4 terpasang. Error detail di atas.")
            raise

        # ── FR-NAN-AUDIT: laporkan evaluator failure rate per metrik ────────
        # Rationale: pd.DataFrame.mean() default skipna=True menyembunyikan
        # kegagalan parsing/judge Ragas secara diam-diam. Log eksplisit di sini
        # supaya jumlah NaN per metrik tercatat di log DAN manifest, bukan
        # cuma hilang dari rata-rata akhir.
        n_total = len(ragas_df)
        nan_summary = {}
        ragas_metric_cols = [c for c in METRICS_COLS if c in ragas_df.columns]
        if extra_metrics:
            ragas_metric_cols += [m for m in extra_metrics if m in ragas_df.columns]

        logger.info(f"{'='*60}\nEVALUATOR FAILURE RATE (NaN per metrik) — Config {config.upper()}\n{'='*60}")
        for m_col in ragas_metric_cols:
            n_nan = int(ragas_df[m_col].isna().sum())
            pct_nan = (n_nan / n_total * 100) if n_total else 0.0
            nan_summary[m_col] = {"n_nan": n_nan, "pct_nan": round(pct_nan, 2)}
            level = logger.warning if pct_nan > 0 else logger.info
            level(f"  {m_col:25s}: {n_nan}/{n_total} NaN ({pct_nan:.2f}%)")

        if any(v["n_nan"] > 0 for v in nan_summary.values()):
            logger.warning(
                "Sebagian skor Ragas gagal dihitung (NaN). Baris ini TETAP masuk "
                "hasil_config CSV, tapi diabaikan (skipna) saat menghitung mean "
                "agregat — lihat kolom individual di CSV untuk audit manual."
            )

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

        # Checkpoint sudah tidak diperlukan setelah hasil final tersimpan
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            logger.debug(f"Checkpoint dibersihkan: {checkpoint_path}")

        # Agregasi
        df_result = pd.DataFrame(results)
        _print_summary(df_result, config)

        # FR-23: Error analysis — N sampel dengan skor terendah
        _export_error_analysis(df_result, config)

        # Archive & Run Manifest recording
        slug = _make_model_slug(llm_model, eval_model)
        archive_dir = EVAL_RESULTS_DIR / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_csv_name = f"hasil_config_{config}_{start_dt.strftime('%Y%m%d_%H%M%S')}_{slug}.csv"
        archive_csv_path = archive_dir / archive_csv_name
        shutil.copy2(output_path, archive_csv_path)
        logger.info(f"Hasil evaluasi di-archive ke: {archive_csv_path}")

        # Compute mean of all available metrics columns from Ragas results
        mean_metrics_dict = {}
        possible_metrics = METRICS_COLS + (extra_metrics or []) + ["response_time_seconds"]
        for m_col in possible_metrics:
            if m_col in df_result.columns:
                mean_val = df_result[m_col].mean()
                if pd.notna(mean_val):
                    mean_metrics_dict[m_col] = round(float(mean_val), 4)

        manifest = _load_manifest()
        for r in manifest["runs"]:
            if r["run_id"] == run_id:
                r["status"] = "completed"
                r["timestamp_end"] = datetime.now(timezone.utc).isoformat()
                r["success_count"] = success_cnt
                r["error_count"] = err_cnt
                r["metrics"] = mean_metrics_dict
                r["nan_summary"] = nan_summary
                r["archive_file"] = archive_csv_path.relative_to(ROOT_DIR).as_posix()
                r["is_active"] = True
            elif r.get("config") == config:
                r["is_active"] = False

        _save_manifest(manifest)

    except BaseException as e:
        logger.error(f"Evaluasi run {run_id} gagal dengan error: {e}")
        logger.error(
            f"Hasil generasi (jika sempat di-checkpoint) tersedia di: "
            f"{EVAL_RESULTS_DIR / f'_checkpoint_config_{config}_{run_id}.csv'}"
        )
        manifest = _load_manifest()
        for r in manifest["runs"]:
            if r["run_id"] == run_id:
                r["status"] = "failed"
                r["timestamp_end"] = datetime.now(timezone.utc).isoformat()
        _save_manifest(manifest)
        raise


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
    Buat grouped bar chart perbandingan 2 config (Config B vs C).

    Output: eval/results/perbandingan_visual.png (untuk lampiran skripsi).
    BUKAN dikonsumsi UI — UI render dari /api/evaluation. (D-A9, FR-17)
    """
    # Config A is archived. Exclusively plotting Config B vs C.
    configs = {"b": "Config B", "c": "Config C"}
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
    width  = 0.35
    colors = ["#B63D3D", "#C2C8D3"]

    for i, (label, scores) in enumerate(data.items()):
        offset = (i - len(data) / 2) * width + width / 2
        bars = ax.bar([xi + offset for xi in x], [scores[m] for m in metrics],
                      width=width, label=label, color=colors[i % len(colors)])
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Metrik Evaluasi")
    ax.set_ylabel("Skor")
    ax.set_title("Perbandingan Config B vs C")
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
    parser.add_argument("--limit", type=int, default=None,
                        help="Batasi jumlah baris dataset yang dievaluasi")
    parser.add_argument("--model", type=str, default=None,
                        help="Override LLM generator model")
    parser.add_argument("--evaluator", type=str, default=None,
                        help="Override Ragas evaluator model")
    args = parser.parse_args()

    if args.config:
        if args.config == "a":
            print("Config A is deprecated and archived for backup purposes.")
            sys.exit(0)
        run_evaluation(
            args.config,
            extra_metrics=args.extra_metrics,
            limit=args.limit,
            generator_model=args.model,
            evaluator_model=args.evaluator,
        )
    elif args.stats:
        # --- ARCHIVED WILCOXON TEST ---
        print("Wilcoxon statistical test is deprecated and archived for backup purposes.")
        # run_statistical_test()
    elif args.visualize:
        run_visualization()