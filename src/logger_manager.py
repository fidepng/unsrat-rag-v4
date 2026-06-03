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

    from logging.handlers import RotatingFileHandler

    # File handler — semua level dengan rotasi file (max 5MB, keep 3 backups)
    fh = RotatingFileHandler(
        SYSTEM_LOG_PATH,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
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
