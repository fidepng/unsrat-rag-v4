# scripts/generate_chunk_report.py
import pickle
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).parent.parent
INDEX_PATH = ROOT_DIR / "bm25_index" / "bm25_index.pkl"
OUTPUT_PATH = ROOT_DIR / "docs" / "reports" / "laporan_seluruh_chunk.md"

def main():
    if not INDEX_PATH.exists():
        print(f"Error: File index tidak ditemukan di {INDEX_PATH}")
        return

    # Load chunks
    with open(INDEX_PATH, 'rb') as f:
        data = pickle.load(f)
        chunks = data.get("chunks", [])

    total_chunks = len(chunks)
    print(f"Membaca {total_chunks} chunks dari index...")

    # Buat konten markdown
    md_content = []
    md_content.append("# Laporan Seluruh Chunk Dokumen RAG UNSRAT")
    md_content.append(f"Dokumen ini berisi daftar lengkap **{total_chunks} chunk** hasil pemrosesan korpus akademik UNSRAT untuk diverifikasi secara manual.\n")
    md_content.append("---\n")

    for idx, chunk in enumerate(chunks, start=1):
        content = chunk.get('content', '').strip()
        length = len(content)
        
        md_content.append(f"## CHUNK {idx} dari {total_chunks}")
        md_content.append(f"* **ID Dokumen**: `{chunk.get('doc_id', 'N/A')}`")
        md_content.append(f"* **Judul**: {chunk.get('title', 'N/A')}")
        md_content.append(f"* **Kategori**: `{chunk.get('category', 'N/A')}`")
        if chunk.get('bab'):
            md_content.append(f"* **Bab**: {chunk.get('bab')}")
        if chunk.get('bagian'):
            md_content.append(f"* **Bagian**: {chunk.get('bagian')}")
        if chunk.get('pasal'):
            md_content.append(f"* **Pasal**: {chunk.get('pasal')}")
        md_content.append(f"* **Ukuran**: {length} karakter\n")
        
        md_content.append("### Konten:")
        md_content.append("```markdown")
        md_content.append(content)
        md_content.append("```")
        md_content.append("\n" + "-"*40 + "\n")

    # Tulis ke file
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))

    print(f"Sukses! Laporan berhasil disimpan ke: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
