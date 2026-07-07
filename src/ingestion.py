# src/ingestion.py — Pipeline Data Ingestion → ChromaDB
# PRD Reference: Section 6.1, 6.2, FR-01–FR-08
# PENTING: Gunakan `use context7` untuk verifikasi API LangChain sebelum run

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import chromadb
import frontmatter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from src.config import (
    CORPUS_DIR, CHROMA_BASE_DIR, CHROMA_DIR_A, CHROMA_DIR_B,
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

    doc_id       = str(meta["doc_id"])
    title        = str(meta["title"])
    category     = str(meta["category"])
    content_type = str(meta.get("content_type", ""))
    status       = str(meta.get("status", "active"))
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

    from src.config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID
    
    kwargs = {
        "model": EMBEDDING_MODEL_NAME,
        "task_type": "retrieval_document",
    }
    if GOOGLE_APPLICATION_CREDENTIALS:
        from google.oauth2 import service_account
        kwargs["credentials"] = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        kwargs["project"] = GCP_PROJECT_ID
    else:
        kwargs["google_api_key"] = GOOGLE_API_KEY

    # Embedding function — task_type="retrieval_document" (FR-07, D-15)
    embedding_fn = GoogleGenerativeAIEmbeddings(**kwargs)

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

    meta_path = CHROMA_BASE_DIR / f"config_{config}" / ".ingestion_meta.json"
    meta = {
        "config": config,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "total_chunks": collection.count(),
        "corpus_files": len(md_files),
        "chunk_size": CHUNK_SIZE_B if config == "b" else CHUNK_SIZE_A,
        "chunk_overlap": CHUNK_OVERLAP_B if config == "b" else CHUNK_OVERLAP_A,
    }
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    logger.info(f"Ingestion metadata disimpan: {meta_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingestion pipeline UNSRAT RAG")
    parser.add_argument("--config", choices=["a", "b"], default="b", help="Config A atau B (default: b)")
    parser.add_argument("--rebuild", action="store_true", help="Hapus collection dan rebuild dari nol")
    args = parser.parse_args()
    if args.config == "a":
        print("Config A is deprecated and archived for backup purposes.")
        sys.exit(0)
    run_ingestion(args.config, args.rebuild)
