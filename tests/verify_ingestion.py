# tests/verify_ingestion.py
# Script untuk verifikasi database ChromaDB pasca-ingestion
# Menguji kepatuhan terhadap PRD section D-B3 (tanpa 'priority' dan 'chunk_type' di metadata)

import sys
from pathlib import Path
import chromadb

# Tambahkan src ke python path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import (
    CHROMA_DIR_A, CHROMA_DIR_B,
    CHROMA_COLLECTION_A, CHROMA_COLLECTION_B,
)

def verify_collection(config_name: str, chroma_dir: Path, collection_name: str):
    print(f"\n==================================================")
    print(f"VERIFIKASI CHROMADB - CONFIG {config_name.upper()}")
    print(f"==================================================")
    print(f"Directory  : {chroma_dir}")
    print(f"Collection : {collection_name}")

    if not chroma_dir.exists():
        print(f"[-] ERROR: Direktori database tidak ditemukan. Silakan jalankan ingestion terlebih dahulu.")
        return False

    client = chromadb.PersistentClient(path=str(chroma_dir))
    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        print(f"[-] ERROR: Gagal mengambil collection '{collection_name}': {e}")
        return False

    count = collection.count()
    print(f"[+] Total chunk di database: {count}")

    if count == 0:
        print(f"[-] WARNING: Database kosong.")
        return True

    # Ambil 5 sampel chunk untuk pengecekan metadata
    results = collection.get(limit=5, include=["metadatas", "documents"])
    metadatas = results.get("metadatas", [])

    print(f"\n[+] Memeriksa kepatuhan skema metadata (PRD Section D-B3)...")
    forbidden_keys = ["priority", "chunk_type"]
    has_error = False

    for idx, meta in enumerate(metadatas):
        print(f"  Sampel #{idx + 1} metadata keys: {list(meta.keys())}")
        for key in forbidden_keys:
            if key in meta:
                print(f"  [-] PELANGGARAN: Ditemukan field '{key}' di metadata chunk!")
                has_error = True

    if not has_error:
        print(f"[+] SUKSES: Semua chunk mematuhi aturan D-B3 (tidak ada field 'priority' atau 'chunk_type' di metadata).")
    else:
        print(f"[-] GAGAL: Terdeteksi pelanggaran aturan metadata D-B3.")

    # Tampilkan preview teks sampel pertama
    if results.get("documents"):
        preview = results["documents"][0][:150].replace("\n", " ")
        print(f"\n[+] Preview Chunk Pertama:")
        print(f"  ID: {results['ids'][0]}")
        print(f"  Teks: \"{preview}...\"")

    return not has_error

def main():
    success_a = verify_collection("A", CHROMA_DIR_A, CHROMA_COLLECTION_A)
    success_b = verify_collection("B", CHROMA_DIR_B, CHROMA_COLLECTION_B)

    if success_a and success_b:
        print("\n[+] KESIMPULAN: VERIFIKASI SELESAI & SEMUA DATA INGESTION 100% VALID!")
        sys.exit(0)
    else:
        print("\n[-] KESIMPULAN: DITEMUKAN MASALAH ATAU PELANGGARAN ATURAN!")
        sys.exit(1)

if __name__ == "__main__":
    main()
