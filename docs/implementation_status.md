# 📊 Status Implementasi Proyek: UNSRAT RAG Chatbot

Laporan ini merinci kemajuan implementasi sistem **UNSRAT RAG Chatbot v4** per **1 Juni 2026**. Proyek saat ini telah menyelesaikan seluruh Phase 1 (Task 1 hingga Task 10) dengan lengkap dan teruji secara menyeluruh. Sistem kini siap untuk masuk ke Phase 2 (Kalibrasi Threshold & Ekspansi Data Evaluasi).

---

## 🗺️ Peta Kemajuan (Progress Matrix)

Sistem dibagi menjadi 13 Task utama sesuai dengan rencana implementasi (`docs/superpowers/plans/2026-05-30-rag-chatbot-implementation.md`).

| Task | Komponen / File | Status | Keterangan |
| :--- | :--- | :--- | :--- |
| **Task 1** | **Project Foundation & Environment** | ✅ **SELESAI** | Folder terstruktur, `.gitignore` dikonfigurasi, conda environment `unsrat-rag` aktif. |
| **Task 2** | **`src/config.py` — Pusat Konfigurasi** | ✅ **SELESAI** | Semua konstanta (chunk size, model, prompt, parameter) tersentralisasi. |
| **Task 3** | **`src/logger_manager.py` — Logging** | ✅ **SELESAI** | Logging terpusat: system log, audit ingestion CSV, dan audit chat CSV. |
| **Task 4** | **`src/ingestion.py` — Ingestion Pipeline** | ✅ **SELESAI** | Dua-tahap chunking, embedding Google GenAI dengan retry eksponensial. Ingestion berhasil dijalankan. |
| **Task 5** | **`src/bm25_retriever.py` — BM25 Index** | ✅ **SELESAI** | Indeks keyword search Okapi BM25 untuk Config C berhasil dibangun di atas potongan chunk Config B. |
| **Task 6** | **`src/retriever.py` — Unified Retriever** | ✅ **SELESAI** | Interface tunggal untuk memanggil Config A (Vector 500), Config B (Vector 2000) dan Config C (BM25). |
| **Task 7** | **`src/chain.py` — RAG Chain & SSE** | ✅ **SELESAI** | RAG Generation, parsing sitasi `[N]`, streaming SSE, memori chat, dan penanganan rate limit. |
| **Task 8** | **`app.py` — FastAPI Backend** | ✅ **SELESAI** | Endpoint SSE `/api/chat` (streaming), server static UI, dan stateless model list `/api/models`. |
| **Task 9** | **`static/` — SPA Frontend** | ✅ **SELESAI** | UI Web dua tab (Chat RAG & Visualisasi Evaluasi Ragas) dengan indikator thinking. |
| **Task 10**| **`evaluation.py` — Pipeline Evaluasi** | ✅ **SELESAI** | Batch evaluation menggunakan Ragas, analisis statistik Wilcoxon, & ekspor Chart.js/visualisasi. |
| **Task 11**| **Kalibrasi Threshold Empiris** | ⏳ *BERIKUTNYA* | Pengujian presisi threshold retrieval (`D-B7`) sebelum evaluasi resmi. |
| **Task 12**| **Persiapan Ground Truth** | ⏳ *BERIKUTNYA* | dataset evaluasi (NL) dari file peraturan akademik (`D-B6`). |
| **Task 13**| **Evaluasi Resmi & Validasi Akhir** | 📋 Terencana | Pengujian performa komparatif tiga konfigurasi dengan visualisasi performa. |

---

## 📈 Status Data Ingestion & Indexing
Pipeline ingestion telah berhasil dieksekusi untuk kedua konfigurasi vektor dan keyword search dengan hasil sebagai berikut (tercatat di [ingestion_report.csv](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/logs/ingestion_report.csv)):

1. **Config B (Vektor - Chunk 2000)**:
   * **File diproses**: 9 file Markdown corpus
   * **Total chunk ter-ingest**: **179 chunks** disimpan di ChromaDB (`unsrat_rag_config_b`)
   * **Kepatuhan Schema (D-B3)**: 100% mematuhi aturan (bebas dari field `priority` dan `chunk_type` di metadata).

2. **Config A (Vektor - Chunk 500)**:
   * **File diproses**: 9 file Markdown corpus
   * **Total chunk ter-ingest**: **430 chunks** disimpan di ChromaDB (`unsrat_rag_config_a`)

3. **Config C (Keyword - BM25 Okapi)**:
   * **Total chunk terindeks**: **179 chunks** disimpan di pickle file ([bm25_index.pkl](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/bm25_index/bm25_index.pkl)) untuk perbandingan baseline yang adil dengan Config B.

---

## 🛠️ Modul Pengujian & Verifikasi yang Tersedia

Beberapa script verifikasi mandiri telah dibuat untuk menguji sistem secara aman dan andal:
* **Verifikasi Ingestion**: [verify_ingestion.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/verify_ingestion.py) — Menguji jumlah chunk ChromaDB dan kepatuhan format metadata (PRD Section D-B3).
* **Verifikasi Retriever**: [verify_retriever.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/verify_retriever.py) — Menguji fungsionalitas retrieval Config A, B, dan C dengan query sampel dan threshold filter.
* **Verifikasi NVIDIA NIM API & Rate Limit**: [test_nvidia_nim_api.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/test_nvidia_nim_api.py) — Menguji keandalan pemanggilan model generator dan evaluator NVIDIA NIM dengan pembatasan RPM secara otomatis.
* **Unit Tests Terpadu**: Diuji menggunakan `pytest` untuk parser sitasi dan SPA serving (`tests/test_citation_parser.py`, `tests/test_spa_serving.py`).

---

## 🎯 Langkah Selanjutnya (Next Steps)
Fokus berikutnya adalah **Task 11 (Kalibrasi Threshold D-B7)** dan **Task 12 (Persiapan Ground Truth D-B6)**:
1. Menyusun berkas kalibrasi empiris (`tests/calibrate_threshold.py`) untuk menganalisis akurasi retrieval pada threshold kesamaan berbeda.
2. Memperluas `eval/dataset/ground_truth.csv` dari 3 pasang data uji menjadi 30–50 pertanyaan-jawaban alami untuk evaluasi ilmiah naskah skripsi.
