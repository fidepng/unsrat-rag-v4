# src/bm25_retriever.py — BM25 Indexing & Retrieval (Config C)
# PRD Reference: FR-19, FR-20, D-A3, D-A6
# rank-bm25 digunakan LANGSUNG, bukan via LangChain wrapper (D-A6)

import argparse
import pickle
import re
from pathlib import Path

import frontmatter
from rank_bm25 import BM25Okapi
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from src.config import (
    CORPUS_DIR, BM25_INDEX_DIR, BM25_INDEX_PATH,
    CHUNK_SIZE_B, CHUNK_OVERLAP_B, CHUNK_SEPARATORS,
    MIN_CHUNK_LENGTH, BM25_K, BM25_MIN_TOKEN_LEN,
    REQUIRED_YAML_FIELDS,
)
from src.logger_manager import get_logger

logger = get_logger("bm25_retriever")

# ── Stemmer & stopword remover Bahasa Indonesia (Sastrawi) ─────────────────
# CATATAN (fix fairness B vs C): BM25 murni cocok token literal, sehingga
# variasi imbuhan ("mengambil" vs "diambil" vs "pengambilan") tidak akan
# match tanpa stemming. Dibuat sebagai module-level singleton (bukan
# per-panggilan) agar tidak membangun factory berulang kali — satu-satunya
# pertimbangan performa yang relevan di sini, tidak ada tuning tambahan lain.
_stemmer = StemmerFactory().create_stemmer()
_stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

HEADERS_TO_SPLIT_ON = [
    ("#",    "header_1"),
    ("##",   "bab"),
    ("###",  "bagian"),
    ("####", "pasal"),
]


def _tokenize(text: str) -> list[str]:
    """
    Tokenisasi Bahasa Indonesia untuk BM25: stopword removal → stemming →
    lowercase → hapus tanda baca → filter token pendek.

    Dipakai identik saat indexing (per chunk) dan saat query, sehingga
    representasi token pada kedua sisi tetap konsisten (D-A6 tetap berlaku:
    rank-bm25 dipakai langsung, hanya preprocessing teks yang berubah).

    Min token length dari BM25_MIN_TOKEN_LEN (default: 2 karakter).
    """
    cleaned = _stopword_remover.remove(text)
    stemmed = _stemmer.stem(cleaned)
    tokens = re.findall(r'\b\w+\b', stemmed.lower())
    return [t for t in tokens if len(t) >= BM25_MIN_TOKEN_LEN]


def _load_all_chunks() -> list[dict]:
    """
    Load semua file corpus, chunk dengan parameter identik Config B (D-A3).

    Returns list of chunk dicts: {content, doc_id, title, category,
    content_type, bab, bagian, pasal}
    """
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE_B,
        chunk_overlap=CHUNK_OVERLAP_B,
        separators=CHUNK_SEPARATORS,
    )

    all_chunks = []
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        try:
            post = frontmatter.load(md_file)
        except Exception as e:
            logger.warning(f"Gagal parse {md_file.name}: {e}")
            continue

        meta = post.metadata
        missing = [f for f in REQUIRED_YAML_FIELDS if not meta.get(f)]
        if missing:
            logger.warning(f"SKIP {md_file.name} — field kosong: {missing}")
            continue

        structural = md_splitter.split_text(post.content)
        raw_chunks = char_splitter.split_documents(structural)

        for doc in raw_chunks:
            content = doc.page_content.strip()
            if len(content) < MIN_CHUNK_LENGTH:
                continue
            all_chunks.append({
                "content":      content,
                "doc_id":       meta["doc_id"],
                "title":        meta["title"],
                "category":     meta["category"],
                "content_type": meta.get("content_type", ""),
                "bab":          doc.metadata.get("bab", ""),
                "bagian":       doc.metadata.get("bagian", ""),
                "pasal":        doc.metadata.get("pasal", ""),
            })

    logger.info(f"BM25: {len(all_chunks)} chunk dimuat dari corpus.")
    return all_chunks


def build_index(rebuild: bool = False) -> None:
    """
    Bangun BM25 index dari corpus dan simpan ke bm25_index.pkl.

    Dipanggil via: python src/bm25_retriever.py --rebuild
    """
    if BM25_INDEX_PATH.exists() and not rebuild:
        logger.info("BM25 index sudah ada. Gunakan --rebuild untuk membangun ulang.")
        return

    BM25_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    chunks = _load_all_chunks()

    if not chunks:
        raise RuntimeError("Tidak ada chunk yang bisa diindeks. Periksa corpus.")

    tokenized = [_tokenize(c["content"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks, "tokenized": tokenized}, f)

    logger.info(f"BM25 index disimpan: {BM25_INDEX_PATH} ({len(chunks)} chunks)")


def _load_index() -> tuple[BM25Okapi, list[dict]]:
    """Load BM25 index dari pickle. Raise RuntimeError jika tidak ada."""
    if not BM25_INDEX_PATH.exists():
        raise RuntimeError(
            f"BM25 index tidak ditemukan: {BM25_INDEX_PATH}\n"
            "Jalankan: python src/bm25_retriever.py --rebuild"
        )
    with open(BM25_INDEX_PATH, "rb") as f:
        data = pickle.load(f)
    return data["bm25"], data["chunks"]


def retrieve_chunks_bm25(query: str) -> list[dict]:
    """
    Retrieve BM25_K chunk teratas untuk query yang diberikan.

    Returns list[dict] kompatibel dengan format unified retriever:
    {content, doc_id, title, category, content_type, bab, bagian, pasal,
     score, chunk_id}

    BM25 score BUKAN cosine distance — nilainya tidak dinormalisasi [0,1].
    (FR-20)
    """
    bm25, chunks = _load_index()
    query_tokens  = _tokenize(query)

    if not query_tokens:
        logger.warning(f"Query tokenisasi kosong untuk: '{query}'")
        return []

    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:BM25_K]

    results = []
    for idx in top_indices:
        if scores[idx] <= 0:
            continue   # Skip chunk dengan score 0 (tidak relevan sama sekali)
        chunk = chunks[idx].copy()
        chunk["score"]    = float(scores[idx])
        chunk["chunk_id"] = f"bm25_{idx}"   # pseudo-ID untuk audit log
        results.append(chunk)

    logger.debug(f"BM25 retrieved {len(results)} chunks untuk '{query[:50]}'")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BM25 index builder (Config C)")
    parser.add_argument("--rebuild", action="store_true", help="Bangun ulang index dari nol")
    args = parser.parse_args()
    build_index(rebuild=args.rebuild)