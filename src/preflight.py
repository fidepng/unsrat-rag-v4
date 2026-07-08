# src/preflight.py — Preflight API Readiness Health Check
# PRD Reference: Task 2 - UNSRAT RAG System Hardening

import os
import time

from src.config import (
    EMBEDDING_MODEL_NAME,
    GOOGLE_API_KEY,
    LLM_MODEL_NAME,
    EVALUATOR_MODEL_NAME,
    NVIDIA_NIM_API_KEY,
)
from src.logger_manager import get_logger

logger = get_logger("preflight")


def test_google_embedding() -> dict:
    """Uji konektivitas & kesiapan Google Embedding API."""
    start_time = time.time()
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        from src.config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID
        
        kwargs = {"model": EMBEDDING_MODEL_NAME}
        if GOOGLE_APPLICATION_CREDENTIALS:
            from google.oauth2 import service_account
            kwargs["credentials"] = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            kwargs["project"] = GCP_PROJECT_ID
        else:
            kwargs["google_api_key"] = GOOGLE_API_KEY

        embeddings = GoogleGenerativeAIEmbeddings(**kwargs)
        embeddings.embed_query("test preflight")
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Preflight test_google_embedding BERHASIL ({latency_ms} ms)")
        return {"ok": True, "latency_ms": latency_ms, "error": None}
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        err_msg = str(e)
        logger.warning(f"Preflight test_google_embedding GAGAL ({latency_ms} ms): {err_msg}")
        return {"ok": False, "latency_ms": latency_ms, "error": err_msg}


def _resolve_nim_model_name(model_name: str) -> str:
    """Petakan model_name lokal ke endpoint name NVIDIA NIM."""
    if "/" in model_name:
        return model_name
    mapping = {
        "gemma-4-31b-it": "google/gemma-4-31b-it",
        "llama-3.3-nemotron-super-49b-v1.5": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "llama-3.1-nemotron-nano-8b-v1": "nvidia/llama-3.1-nemotron-nano-8b-v1",
        "llama-3.1-70b-instruct": "meta/llama-3.1-70b-instruct",
        "llama-3.1-8b-instruct": "meta/llama-3.1-8b-instruct",
        "deepseek-v4-flash": "deepseek-ai/deepseek-v4-flash",
        "deepseek-v4-pro": "deepseek-ai/deepseek-v4-pro",
    }
    return mapping.get(model_name, model_name)


def test_nim_generator(model_name: str | None = None) -> dict:
    """Uji konektivitas LLM Generator terhadap NVIDIA NIM endpoint (atau Gemini jika model Gemini)."""
    start_time = time.time()
    target_model = model_name or LLM_MODEL_NAME

    try:
        if "gemini" in target_model.lower():
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import HumanMessage

            from src.config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID
            kwargs = {
                "model": target_model,
                "temperature": 0.0,
                "max_output_tokens": 1,
                "max_retries": 1,
                "timeout": 15,
            }
            if GOOGLE_APPLICATION_CREDENTIALS:
                from google.oauth2 import service_account
                kwargs["credentials"] = service_account.Credentials.from_service_account_file(
                    GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                kwargs["project"] = GCP_PROJECT_ID
            else:
                kwargs["google_api_key"] = GOOGLE_API_KEY
                
            llm = ChatGoogleGenerativeAI(**kwargs)
            llm.invoke([HumanMessage(content="hi")])
        else:
            api_key = NVIDIA_NIM_API_KEY or os.getenv("NVIDIA_NIM_API_KEY")
            if not api_key:
                raise ValueError("NVIDIA_NIM_API_KEY tidak ditemukan di environment.")

            nim_model = _resolve_nim_model_name(target_model)
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage

            llm = ChatOpenAI(
                model=nim_model,
                api_key=api_key,
                openai_api_base="https://integrate.api.nvidia.com/v1",
                temperature=0.0,
                max_tokens=1,
                max_retries=1,
                timeout=15,
            )
            llm.invoke([HumanMessage(content="hi")])

        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Preflight test_nim_generator ({target_model}) BERHASIL ({latency_ms} ms)")
        return {"ok": True, "latency_ms": latency_ms, "error": None}
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        err_msg = str(e)
        logger.warning(f"Preflight test_nim_generator ({target_model}) GAGAL ({latency_ms} ms): {err_msg}")
        return {"ok": False, "latency_ms": latency_ms, "error": err_msg}


def test_ragas_evaluator(evaluator_model: str | None = None) -> dict:
    """Uji kesiapan Ragas evaluator dengan 1 prompt tes ringan."""
    start_time = time.time()
    target_evaluator = evaluator_model or EVALUATOR_MODEL_NAME

    try:
        api_key = NVIDIA_NIM_API_KEY or os.getenv("NVIDIA_NIM_API_KEY")
        if api_key and ("gemini" not in target_evaluator.lower()):
            nim_model = _resolve_nim_model_name(target_evaluator)
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(
                model=nim_model,
                api_key=api_key,
                openai_api_base="https://integrate.api.nvidia.com/v1",
                temperature=0.0,
                max_tokens=10,
                timeout=5,
                max_retries=1,
            )
        else:
            from langchain_google_genai import ChatGoogleGenerativeAI

            from src.config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID
            kwargs = {
                "model": target_evaluator,
                "temperature": 0.0,
                "max_output_tokens": 10,
                "max_retries": 1,
                "timeout": 15,
            }
            if GOOGLE_APPLICATION_CREDENTIALS:
                from google.oauth2 import service_account
                kwargs["credentials"] = service_account.Credentials.from_service_account_file(
                    GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                kwargs["project"] = GCP_PROJECT_ID
            else:
                kwargs["google_api_key"] = GOOGLE_API_KEY
                
            llm = ChatGoogleGenerativeAI(**kwargs)

        resp = llm.invoke("Test evaluator API connection")
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Preflight test_ragas_evaluator ({target_evaluator}) BERHASIL ({latency_ms} ms)")
        return {"ok": True, "latency_ms": latency_ms, "error": None}
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        err_msg = str(e)
        logger.warning(f"Preflight test_ragas_evaluator ({target_evaluator}) GAGAL ({latency_ms} ms): {err_msg}")
        return {"ok": False, "latency_ms": latency_ms, "error": err_msg}


def preflight_check(
    require_google: bool = True,
    require_nim: bool = False,
    generator_model: str | None = None,
    evaluator_model: str | None = None,
) -> dict:
    """
    Jalankan preflight check untuk memastikan ketersediaan API Google, Generator, dan Evaluator.

    Returns dict terstruktur:
    {
        "overall_ok": bool,
        "services": {
            "google_embedding": {"ok": bool, "latency_ms": float, "error": str|None},
            "generator": {"ok": bool, "latency_ms": float, "error": str|None},
            "evaluator": {"ok": bool, "latency_ms": float, "error": str|None}
        }
    }
    """
    logger.info("=== Menjalankan Pre-flight Health Check ===")

    services = {}

    try:
        # 1. Google Embedding
        if require_google:
            emb_res = test_google_embedding()
        else:
            emb_res = {"ok": True, "latency_ms": 0.0, "error": None}
        services["google_embedding"] = emb_res

        # 2. Generator
        gen_model_to_test = generator_model or LLM_MODEL_NAME
        gen_res = test_nim_generator(gen_model_to_test)
        services["generator"] = gen_res

        # 3. Evaluator
        eval_model_to_test = evaluator_model or EVALUATOR_MODEL_NAME
        eval_res = test_ragas_evaluator(eval_model_to_test)
        services["evaluator"] = eval_res

    except Exception as e:
        logger.error(f"Kesalahan tak terduga dalam preflight_check: {e}")

    overall_ok = len(services) == 3 and all(svc.get("ok", False) for svc in services.values())

    if overall_ok:
        logger.info("=== Pre-flight Health Check: SEMUA LAYANAN OK ===")
    else:
        logger.warning(f"=== Pre-flight Health Check: ADA KENDALA pada layanan (overall_ok={overall_ok}) ===")

    return {
        "overall_ok": overall_ok,
        "services": services,
    }
