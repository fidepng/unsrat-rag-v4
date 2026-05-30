# src/retriever.py — Unified Retrieval Interface (Config A / B / C)
# PRD Reference: Section 6.4, FR-09, FR-10

import chromadb

from src.config import (
    CHROMA_DIR_A, CHROMA_DIR_B,
    CHROMA_COLLECTION_A, CHROMA_COLLECTION_B, CHROMA_DISTANCE_FN,
    RETRIEVAL_K, SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY,
)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
