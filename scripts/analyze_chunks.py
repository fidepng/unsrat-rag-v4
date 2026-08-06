import sys
import json
import pickle
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime

# Fallback dummy module untuk rank_bm25 jika dijalankan di luar venv (saat load pickle)
try:
    import rank_bm25
except ImportError:
    import types
    rank_bm25_dummy = types.ModuleType('rank_bm25')
    class DummyBM25Okapi: pass
    rank_bm25_dummy.BM25Okapi = DummyBM25Okapi
    sys.modules['rank_bm25'] = rank_bm25_dummy

try:
    import frontmatter
    from langchain_text_splitters import MarkdownHeaderTextSplitter
except ImportError:
    frontmatter = None
    MarkdownHeaderTextSplitter = None

# Konfigurasi Path
ROOT_DIR = Path(__file__).parent.parent
CORPUS_DIR = ROOT_DIR / "data" / "corpus"
BM25_INDEX_PATH = ROOT_DIR / "bm25_index" / "bm25_index.pkl"
REPORT_PATH = ROOT_DIR / "docs" / "reports" / "statistik_chunk_analisis.json"

HEADERS_TO_SPLIT_ON = [
    ("#",    "header_1"),
    ("##",   "bab"),
    ("###",  "bagian"),
    ("####", "pasal"),
]

def calculate_stats(lengths, chunk_metadata=None):
    if not lengths:
        return None
    lengths_arr = np.array(lengths)
    n = len(lengths_arr)
    max_idx = np.argmax(lengths_arr)
    
    # Dapatkan top 5 chunk terbesar (outliers) untuk audit kualitas data
    sorted_indices = np.argsort(lengths_arr)[::-1]
    top_n = min(5, len(sorted_indices))
    top_outliers = []
    
    for idx in sorted_indices[:top_n]:
        outlier = {
            "length": int(lengths_arr[idx])
        }
        if chunk_metadata and idx < len(chunk_metadata):
            outlier.update(chunk_metadata[idx])
        top_outliers.append(outlier)
    
    stats = {
        "total_sections": n,
        "min_len": int(np.min(lengths_arr)),
        "mean_len": float(np.mean(lengths_arr)),
        "median_len": float(np.median(lengths_arr)),
        "p75": float(np.percentile(lengths_arr, 75)),
        "p90": float(np.percentile(lengths_arr, 90)),
        "p95": float(np.percentile(lengths_arr, 95)),
        "p99": float(np.percentile(lengths_arr, 99)),
        "max_len": int(np.max(lengths_arr)),
        "under_2000": int(np.sum(lengths_arr <= 2000)),
        "pct_under_2000": float((np.sum(lengths_arr <= 2000) / n) * 100),
        "mean_no_outlier": float(np.mean(np.delete(lengths_arr, max_idx))) if n > 1 else None,
        "top_outliers": top_outliers
    }
        
    return stats

def run_structural_analysis():
    if frontmatter is None or MarkdownHeaderTextSplitter is None:
        print("[!] Warning: 'python-frontmatter' dan 'langchain' tidak terdeteksi.")
        print("    Jalankan di dalam virtual environment (.venv) untuk analisis struktural.")
        return None
        
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )

    lengths = []
    chunk_metadata = []
    
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        try:
            post = frontmatter.load(md_file)
            body = post.content
            
            structural_chunks = md_splitter.split_text(body)
            for doc in structural_chunks:
                content = doc.page_content.strip()
                if len(content) >= 50: # Filter MIN_CHUNK_LENGTH = 50
                    lengths.append(len(content))
                    meta = doc.metadata.copy()
                    meta['file_name'] = md_file.name
                    chunk_metadata.append(meta)
        except Exception as e:
            print(f"Error memproses {md_file.name}: {e}")
            
    return calculate_stats(lengths, chunk_metadata)

def run_index_analysis():
    if not BM25_INDEX_PATH.exists():
        print(f"[!] Index BM25 tidak ditemukan di: {BM25_INDEX_PATH}")
        return None
        
    try:
        with open(BM25_INDEX_PATH, 'rb') as f:
            data = pickle.load(f)
            
        chunks = data.get("chunks", [])
        lengths = [len(chunk.get("content", "").strip()) for chunk in chunks]
        
        chunk_metadata = []
        for chunk in chunks:
            chunk_metadata.append({
                "doc_id": chunk.get("doc_id"),
                "title": chunk.get("title"),
                "pasal": chunk.get("pasal", "N/A")
            })
            
        return calculate_stats(lengths, chunk_metadata)
    except Exception as e:
        print(f"Error membaca index BM25: {e}")
        return None

def print_summary_table(source_stats, index_stats):
    print("="*65)
    print(f"{'METRIK STATISTIK CHUNK':<25} | {'KORPUS SUMBER':<16} | {'INDEKS RUNTIME*':<16}")
    print("="*65)
    
    metrics = [
        ("Total Sections/Chunks", "total_sections", "{:.0f}"),
        ("Panjang Minimum", "min_len", "{:.0f}"),
        ("Rata-rata (Mean)", "mean_len", "{:.1f}"),
        ("Median (P50)", "median_len", "{:.1f}"),
        ("Persentil 75 (P75)", "p75", "{:.1f}"),
        ("Persentil 90 (P90)", "p90", "{:.1f}"),
        ("Persentil 95 (P95)", "p95", "{:.1f}"),
        ("Persentil 99 (P99)", "p99", "{:.1f}"),
        ("Panjang Maksimum", "max_len", "{:.0f}"),
        ("Rata-rata tanpa max", "mean_no_outlier", "{:.1f}"),
    ]
    
    for label, key, fmt in metrics:
        src_val = fmt.format(source_stats[key]) if (source_stats and source_stats.get(key) is not None) else "N/A"
        idx_val = fmt.format(index_stats[key]) if (index_stats and index_stats.get(key) is not None) else "N/A"
        print(f"{label:<25} | {src_val:>16} | {idx_val:>16}")
        
    print("-"*65)
    src_under = f"{source_stats['under_2000']} ({source_stats['pct_under_2000']:.1f}%)" if source_stats else "N/A"
    idx_under = f"{index_stats['under_2000']} ({index_stats['pct_under_2000']:.1f}%)" if index_stats else "N/A"
    print(f"{'Section <= 2000 Karakter':<25} | {src_under:>16} | {idx_under:>16}")
    print("="*65)
    print("*) Catatan: Statistik Indeks Runtime berlaku identik untuk:")
    print("   - Config B (ChromaDB Vector Store)")
    print("   - Config C (BM25 Index)")
    print("   karena keduanya berbagi pipeline ingestion & text splitting yang sama.")
    print("="*65)

def main():
    parser = argparse.ArgumentParser(description="Analisis Statistik Karakter Chunk RAG")
    parser.add_argument("--source-only", action="store_true", help="Hanya analisis dokumen korpus asli")
    parser.add_argument("--index-only", action="store_true", help="Hanya analisis index runtime BM25")
    args = parser.parse_args()
    
    source_stats = None
    index_stats = None
    
    print(f"Menjalankan analisis statistik chunk... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    
    if not args.index_only:
        source_stats = run_structural_analysis()
        
    if not args.source_only:
        index_stats = run_index_analysis()
        
    if source_stats or index_stats:
        print("\n")
        print_summary_table(source_stats, index_stats)
        
        # Simpan laporan terpadu ke JSON
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "source_corpus": source_stats,
            "runtime_index": index_stats
        }
        
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        print(f"\n[+] Laporan JSON berhasil disimpan di: {REPORT_PATH}")

if __name__ == "__main__":
    main()
