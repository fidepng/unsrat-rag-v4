import sys
import os
import pickle
import argparse

# Fallback dummy module untuk rank_bm25 jika dijalankan di luar venv (saat load pickle)
try:
    import rank_bm25
except ImportError:
    import types
    rank_bm25_dummy = types.ModuleType('rank_bm25')
    class DummyBM25Okapi: pass
    rank_bm25_dummy.BM25Okapi = DummyBM25Okapi
    sys.modules['rank_bm25'] = rank_bm25_dummy

# Lakukan guard import untuk chromadb agar script tidak crash saat start jika di luar venv
try:
    import chromadb
except ImportError:
    chromadb = None

# Konfigurasi Path
ROOT_DIR = Path(__file__).parent.parent if 'Path' in globals() else None
if not ROOT_DIR:
    from pathlib import Path
    ROOT_DIR = Path(__file__).parent.parent

sys.path.append(str(ROOT_DIR))
from src.config import CHROMA_DIR_B, CHROMA_COLLECTION_B, BM25_INDEX_PATH

def get_chroma_chunks(chunk_ids):
    """Mengambil chunk dari ChromaDB (Config B)."""
    if not chunk_ids:
        return {}

    if chromadb is None:
        print("[!] Error: Library 'chromadb' tidak terinstal.")
        print("    Jalankan perintah ini di dalam virtual environment Conda Anda.")
        return {}

    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR_B))
        collection = client.get_collection(CHROMA_COLLECTION_B)
        results = collection.get(ids=chunk_ids)
        
        chunks_data = {}
        if results and results.get("ids"):
            for i, chunk_id in enumerate(results["ids"]):
                meta = results["metadatas"][i] if results.get("metadatas") else {}
                content = results["documents"][i] if results.get("documents") else ""
                chunks_data[chunk_id] = {
                    "doc_id": meta.get("doc_id", "N/A"),
                    "title": meta.get("title", "Tidak ada judul"),
                    "bab": meta.get("bab", "N/A"),
                    "bagian": meta.get("bagian", "N/A"),
                    "pasal": meta.get("pasal", "N/A"),
                    "content": content
                }
        return chunks_data
    except Exception as e:
        print(f"[!] Gagal mengambil chunk dari ChromaDB: {e}")
        return {}

def get_bm25_chunks(chunk_ids):
    """Mengambil chunk dari BM25 Pickle (Config C)."""
    if not chunk_ids:
        return {}

    if not BM25_INDEX_PATH.exists():
        print(f"[!] File indeks BM25 tidak ditemukan di: {BM25_INDEX_PATH}")
        return {}

    try:
        with open(BM25_INDEX_PATH, "rb") as f:
            data = pickle.load(f)

        all_chunks = data.get("chunks", [])
        chunks_data = {}

        for chunk_id in chunk_ids:
            try:
                # Parsing ID (bisa berupa "bm25_91" atau langsung angka "91")
                if "_" in str(chunk_id):
                    idx = int(str(chunk_id).split("_")[1])
                else:
                    idx = int(chunk_id)
                
                if 0 <= idx < len(all_chunks):
                    chunk = all_chunks[idx]
                    chunks_data[chunk_id] = {
                        "doc_id": chunk.get("doc_id", "N/A"),
                        "title": chunk.get("title", "Tidak ada judul"),
                        "bab": chunk.get("bab", "N/A"),
                        "bagian": chunk.get("bagian", "N/A"),
                        "pasal": chunk.get("pasal", "N/A"),
                        "content": chunk.get("content", "")
                    }
                else:
                    print(f"[!] Indeks BM25 di luar batas jangkauan (0 - {len(all_chunks)-1}): {chunk_id}")
            except (IndexError, ValueError):
                print(f"[!] Format ID BM25 tidak valid: {chunk_id}")

        return chunks_data
    except Exception as e:
        print(f"[!] Gagal membaca indeks BM25: {e}")
        return {}

def lihat_chunks(target_ids):
    if not target_ids:
        print("[!] Tidak ada ID chunk yang dimasukkan.")
        return

    # Routing otomatis berdasarkan Prefix ID
    bm25_ids = []
    chroma_ids = []
    
    for cid in target_ids:
        cid_str = str(cid).strip()
        if cid_str.startswith("bm25_") or cid_str.isdigit():
            bm25_ids.append(cid_str)
        else:
            chroma_ids.append(cid_str)
  
    results = {}
    results.update(get_chroma_chunks(chroma_ids))
    results.update(get_bm25_chunks(bm25_ids))

    # Tampilkan Hasil dengan formatting yang rapi
    for chunk_id in target_ids:
        chunk_id_str = str(chunk_id).strip()
        print("\n" + "="*70)
        print(f"🔖 CHUNK ID   : {chunk_id_str}")

        if chunk_id_str in results:
            data = results[chunk_id_str]
            print(f"📄 SUMBER DOC : {data['doc_id']} - {data['title']}")
            print(f"📌 LOKASI     : Bab {data['bab']}, Bagian {data['bagian']}, Pasal {data['pasal']}")
            print("-"*70)
            print(data['content'])
        else:
            print("❌ Chunk tidak ditemukan di database/indeks.")
        print("="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Tool Verifikasi & Inspeksi Isi Chunk RAG (ChromaDB / BM25)")
    parser.add_argument("chunk_ids", nargs="*", help="Satu atau lebih ID chunk (bisa dipisah spasi, koma, atau | jika di-quote)")
    args = parser.parse_args()

    # Jika tidak ada arguments, gunakan default fallback list
    if not args.chunk_ids:
        print("[*] Menjalankan dengan mode default (fallback test IDs)...")
        print("    Tips: Anda bisa memasukkan ID chunk langsung lewat argumen CLI:")
        print("          python scripts/lihat_chunk.py bm25_91 bm25_57")
        print("          python scripts/lihat_chunk.py \"id1|id2|id3\" (gunakan tanda kutip ganda)")
        default_ids = ["bm25_91", "bm25_57"]
        lihat_chunks(default_ids)
    else:
        # Proses semua argument untuk memecah separator seperti |, koma, semicolon
        processed_ids = []
        for arg in args.chunk_ids:
            # Ganti koma, semicolon, dan pipe dengan spasi, lalu split
            cleaned_arg = str(arg).replace(",", " ").replace("|", " ").replace(";", " ")
            parts = cleaned_arg.split()
            processed_ids.extend([p.strip() for p in parts if p.strip()])
            
        lihat_chunks(processed_ids)

if __name__ == "__main__":
    main()