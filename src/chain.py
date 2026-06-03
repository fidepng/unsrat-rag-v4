# src/chain.py — RAG Chain: retrieval + LLM + inline citation + SSE streaming
# PRD Reference: Section 6.5, 6.6, 6.7, 6.8, FR-12, FR-26, D-B5
# PENTING: Gunakan `use context7` untuk verifikasi API LangChain dan Gemini sebelum run

import re
import time
import tiktoken
from typing import Any, Generator

from src.config import (
    LLM_TEMPERATURE, LLM_MAX_OUTPUT_TOKENS, LLM_TOP_P,
    MEMORY_K, MAX_RETRIES, RETRY_DELAYS,
    SYSTEM_PROMPT, FALLBACK_RESPONSE, GOOGLE_API_KEY,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.retriever import retrieve_chunks
from src.logger_manager import get_logger, log_chat_transaction

logger = get_logger("chain")

# ── Tiktoken untuk estimasi token offline (D-A5) ──────────────────────────────
_enc = tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    """Estimasi jumlah token menggunakan tiktoken cl100k_base (proxy untuk Gemini)."""
    return len(_enc.encode(text))


# ── Stateless LLM cache (D-B5) ───────────────────────────────────────────────
_llm_cache: dict[str, Any] = {}


def _get_llm(model_name: str) -> Any:
    """
    Kembalikan LLM instance untuk model_name. Cache per model, tidak ada global mutation.

    Stateless per-request — konsisten dengan arsitektur backend (D-B5, Section 6.7).
    """
    if model_name not in _llm_cache:
        import os
        nvidia_api_key = os.getenv("NVIDIA_NIM_API_KEY")
        if nvidia_api_key and ("llama" in model_name or "qwen" in model_name or "nvidia" in model_name or "gemma" in model_name or os.getenv("FORCE_NIM_GENERATOR") == "true"):
            logger.info(f"Menggunakan NVIDIA NIM untuk generator model: {model_name}")
            from langchain_openai import ChatOpenAI
            
            nim_model = model_name
            if model_name == "gemma-4-31b-it":
                nim_model = "google/gemma-4-31b-it"
            elif model_name == "llama-3.3-nemotron-super-49b-v1.5":
                nim_model = "nvidia/llama-3.3-nemotron-super-49b-v1.5"
            elif model_name == "llama-3.1-nemotron-nano-8b-v1":
                nim_model = "nvidia/llama-3.1-nemotron-nano-8b-v1"
            elif model_name == "llama-3.1-70b-instruct":
                nim_model = "meta/llama-3.1-70b-instruct"
            elif model_name == "llama-3.1-8b-instruct":
                nim_model = "meta/llama-3.1-8b-instruct"
                
            _llm_cache[model_name] = ChatOpenAI(
                model=nim_model,
                api_key=nvidia_api_key,
                openai_api_base="https://integrate.api.nvidia.com/v1",
                temperature=LLM_TEMPERATURE,
                max_tokens=LLM_MAX_OUTPUT_TOKENS,
            )
        else:
            logger.info(f"Menggunakan Google Gemini untuk generator model: {model_name}")
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
                "content": chunk["content"],
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


def run_rag_chain(
    query: str,
    config_choice: str = "b",
    model_name: str = "nvidia/llama-3.1-nemotron-nano-8b-v1"
) -> dict:
    """
    Orchestrate retrieve + prompt + generation sync for unit test/mock matching.
    """
    res = get_response(
        query=query,
        config=config_choice,
        chat_history=[],
        model_name=model_name,
        streaming=False
    )
    return {
        "answer": res["answer"],
        "sources": res["citation_sources"],
        "found_state": res["found"],
    }
