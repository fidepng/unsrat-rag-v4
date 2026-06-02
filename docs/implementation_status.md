# 📊 Status Implementasi Proyek: UNSRAT RAG Chatbot

Laporan ini merinci kemajuan implementasi sistem **UNSRAT RAG Chatbot v4** per **3 Juni 2026**. Proyek saat ini telah menyelesaikan seluruh Phase 1 (Task 1 hingga Task 10) serta Task 11 (Kalibrasi Threshold Empiris) dari Phase 2 dengan lengkap dan teruji secara menyeluruh. Sistem kini berada pada tahap persiapan akhir evaluasi resmi (Task 12 dan Task 13).

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
| **Task 11**| **Kalibrasi Threshold Empiris** | ✅ **SELESAI** | Kalibrasi empiris menggunakan `calibrate_threshold.py` selesai. Threshold `0.3` divalidasi sangat optimal (gap 0.117, midpoint 0.291). |
| **Task 12**| **Persiapan Ground Truth** | ⏳ *BERIKUTNYA* | Ekspansi dataset evaluasi (NL) dari minimal 3 pertanyaan menjadi 30–50 pasang Q&A (`D-B6`). |
| **Task 13**| **Evaluasi Resmi & Validasi Akhir** | 📋 Terencana | Pengujian performa komparatif tiga konfigurasi dengan visualisasi performa. |

---

## 📈 Status Data Ingestion & Indexing
Pipeline ingestion telah berhasil dieksekusi untuk kedua konfigurasi vektor dan keyword search dengan hasil sebagai berikut (tercatat di [ingestion_report.csv](../logs/ingestion_report.csv)):

1. **Config B (Vektor - Chunk 2000)**:
   * **File diproses**: 9 file Markdown corpus
   * **Total chunk ter-ingest**: **179 chunks** disimpan di ChromaDB (`unsrat_rag_config_b`)
   * **Kepatuhan Schema (D-B3)**: 100% mematuhi aturan (bebas dari field `priority` dan `chunk_type` di metadata).

2. **Config A (Vektor - Chunk 500)**:
   * **File diproses**: 9 file Markdown corpus
   * **Total chunk ter-ingest**: **430 chunks** disimpan di ChromaDB (`unsrat_rag_config_a`)

3. **Config C (Keyword - BM25 Okapi)**:
   * **Total chunk terindeks**: **179 chunks** disimpan di pickle file ([bm25_index.pkl](../bm25_index/bm25_index.pkl)) untuk perbandingan baseline yang adil dengan Config B.

---

## ⚡ Optimasi UI & Robustness (Phase 2)
Sebagai bagian dari penyempurnaan keandalan sistem di Phase 2, optimasi berikut telah diterapkan pada frontend chatbot:
* **Penghapusan Watchdog Timer**: Client-side watchdog timer keras selama 30 detik dihapus sepenuhnya untuk mendukung dokumen/konteks berukuran besar dan memastikan model generator NVIDIA NIM dapat menyelesaikan stream respons secara utuh tanpa interupsi sepihak dari klien.
* **Peningkatan UX Manual Abort**: Mengenalkan state flag `isUserAborted` untuk mengelola event penghentian stream secara presisi. Jika stream berhenti secara alami, respons ditutup dengan bersih tanpa memicu peringatan. Jika dihentikan secara manual melalui tombol Stop, teks respons yang parsial dipertahankan, ditambahkan catatan kaki peringatan `⚠️ [Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap.]`, dan aplikasi kembali ke status `Ready` seketika.

---

## 🛠️ Modul Pengujian & Verifikasi yang Tersedia

Beberapa script verifikasi mandiri telah dibuat untuk menguji sistem secara aman dan andal:
* **Kalibrasi Threshold**: [calibrate_threshold.py](../scripts/calibrate_threshold.py) — Menganalisis gap keputusan cosine distance antara kueri relevan dan tidak relevan untuk menentukan threshold optimal.
* **Verifikasi Ingestion**: [verify_ingestion.py](../tests/verify_ingestion.py) — Menguji jumlah chunk ChromaDB dan kepatuhan format metadata (PRD Section D-B3).
* **Verifikasi Retriever**: [verify_retriever.py](../tests/verify_retriever.py) — Menguji fungsionalitas retrieval Config A, B, dan C dengan query sampel dan threshold filter.
* **Verifikasi NVIDIA NIM API & Rate Limit**: [test_nvidia_nim_api.py](../tests/test_nvidia_nim_api.py) — Menguji keandalan pemanggilan model generator dan evaluator NVIDIA NIM dengan pembatasan RPM secara otomatis.
* **Unit Tests Terpadu**: Diuji menggunakan `pytest` untuk parser sitasi dan SPA serving (`tests/test_citation_parser.py`, `tests/test_spa_serving.py`).

---

## 🎯 Langkah Selanjutnya (Next Steps)
Fokus berikutnya adalah **Task 12 (Persiapan Ground Truth D-B6)** dan **Task 13 (Evaluasi Resmi & Validasi Akhir)**:
1. Memperluas `eval/dataset/ground_truth.csv` dari 3 pasang data uji menjadi 30–50 pertanyaan-jawaban alami untuk evaluasi ilmiah naskah skripsi.
2. Melakukan pengujian resmi untuk tiga konfigurasi (Config A, Config B, Config C) dengan menjalankan `evaluation.py`.
3. Menganalisis hasil evaluasi secara statistik menggunakan uji Wilcoxon signed-rank (`python evaluation.py --stats`) dan membuat visualisasi bar chart perbandingan (`python evaluation.py --visualize`).
