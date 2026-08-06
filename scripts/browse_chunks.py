import sys
import os
import pickle
import argparse
from pathlib import Path

# Fallback dummy untuk rank_bm25 jika dijalankan di luar venv (saat unpickling)
try:
    import rank_bm25
except ImportError:
    import types
    rank_bm25_dummy = types.ModuleType('rank_bm25')
    class DummyBM25Okapi: pass
    rank_bm25_dummy.BM25Okapi = DummyBM25Okapi
    sys.modules['rank_bm25'] = rank_bm25_dummy

# Tentukan path ke file index
ROOT_DIR = Path(__file__).parent.parent
INDEX_PATH = ROOT_DIR / "bm25_index" / "bm25_index.pkl"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    parser = argparse.ArgumentParser(description="Paginator Interaktif untuk Navigasi Chunk Indeks RAG")
    parser.add_argument("--start", type=int, default=1, help="Nomor chunk awal navigasi (1-based index)")
    args = parser.parse_args()

    if not INDEX_PATH.exists():
        print(f"[!] Error: File index tidak ditemukan di {INDEX_PATH}")
        print("    Silakan jalankan indexer/ingestion terlebih dahulu.")
        sys.exit(1)

    # Load chunks dari index pickle
    try:
        with open(INDEX_PATH, 'rb') as f:
            data = pickle.load(f)
            chunks = data.get("chunks", [])
    except Exception as e:
        print(f"[!] Error saat membaca file index: {e}")
        sys.exit(1)

    total_chunks = len(chunks)
    if total_chunks == 0:
        print("[!] Tidak ada chunk yang ditemukan di dalam index.")
        sys.exit(0)

    # Set indeks awal (convert 1-based ke 0-based index)
    current_index = max(0, min(args.start - 1, total_chunks - 1))

    while True:
        clear_screen()
        chunk = chunks[current_index]
        
        print("=" * 80)
        print(f" CHUNK {current_index + 1} dari {total_chunks} [Berlaku Identik untuk Config B & C]")
        print("=" * 80)
        print(f"Dokumen   : {chunk.get('title', 'N/A')} (ID: {chunk.get('doc_id', 'N/A')})")
        print(f"Kategori  : {chunk.get('category', 'N/A')}")
        if chunk.get('bab'):
            print(f"Bab       : {chunk.get('bab')}")
        if chunk.get('bagian'):
            print(f"Bagian    : {chunk.get('bagian')}")
        if chunk.get('pasal'):
            print(f"Pasal     : {chunk.get('pasal')}")
        print("-" * 80)
        print("ISI CHUNK:")
        print("-" * 80)
        print(chunk.get('content', ''))
        print("=" * 80)
        
        print("\nNavigasi:")
        print("  [Enter]  : Chunk berikutnya")
        print("  [b]      : Chunk sebelumnya")
        print("  [g <num>]: Pergi ke nomor chunk tertentu (contoh: g 10)")
        print("  [q]      : Keluar")
        print("-" * 80)
        
        choice = input("Pilihan Anda: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'b':
            if current_index > 0:
                current_index -= 1
            else:
                input("\n⚠️ Sudah berada di chunk pertama! (Tekan Enter untuk melanjutkan)")
        elif choice.startswith('g '):
            try:
                num = int(choice.split()[1]) - 1
                if 0 <= num < total_chunks:
                    current_index = num
                else:
                    input(f"\n⚠️ Nomor chunk harus di antara 1 dan {total_chunks}! (Tekan Enter untuk melanjutkan)")
            except (ValueError, IndexError):
                input("\n⚠️ Format salah! Gunakan 'g <nomor>' (contoh: g 45). (Tekan Enter untuk melanjutkan)")
        else:
            if current_index < total_chunks - 1:
                current_index += 1
            else:
                input("\n⚠️ Sudah berada di chunk terakhir! (Tekan Enter untuk melanjutkan)")

    print("\nTerima kasih!")

if __name__ == "__main__":
    main()
