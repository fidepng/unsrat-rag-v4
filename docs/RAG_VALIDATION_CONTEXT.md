# Konteks Validasi Chunking — Proyek RAG UNSRAT

## 1. Strategi Chunking (WAJIB)
- Two-stage:
  1. MarkdownHeaderTextSplitter — split di setiap level heading (#, ##, ###, ####)
     → menghasilkan metadata: header_1, bab, bagian, pasal
  2. RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
     separators = ["\n\n", "\n", " ", ""]
- Config aktif: **Config B** (2000/200). Config A (500/100) sudah deprecated/archived.
- MIN_CHUNK_LENGTH = 50 karakter (chunk lebih pendek dari ini di-skip)
- chunk_id = MD5(doc_id + content) → dipakai untuk cek duplikat/idempotency

## 2. Field YAML Wajib (frontmatter)
- doc_id, title, category  (hanya 3 ini yang divalidasi runtime)
- Field lain (content_type, valid_from, status, retrieval_summary,
  chunk_strategy, last_updated) boleh ada tapi tidak divalidasi kode.
- Jika field wajib kosong → seluruh file di-SKIP saat ingestion (bukan crash).

## 3. Retrieval (untuk konteks, bukan chunking)
- RETRIEVAL_K = 4 (top-k=4)
- SIMILARITY_THRESHOLD = 0.32 (cosine distance, buang jika > threshold)
- Config C = BM25 (tidak pakai threshold di atas)

## 4. Aturan Umum yang Wajib Dipatuhi
- Tabel jadwal TIDAK BOLEH terpotong dari heading induknya (per chunk_notes YAML dokumen)
- Tidak boleh ada halusinasi/penambahan info yang tidak ada di dokumen sumber
- Jika perlu koreksi data sumber (typo dsb.), harus didisclose eksplisit
  di dalam file (bukan silent-edit)