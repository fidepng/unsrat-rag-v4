# Panduan Onboarding Developer - unsrat-rag

Selamat datang di proyek **unsrat-rag**! Panduan ini dirancang untuk membantu Anda memahami arsitektur, struktur kode, alur kerja, dan konsep-konsep utama dalam Sistem Chatbot Informasi Akademik UNSRAT Berbasis RAG (Retrieval-Augmented Generation).

Proyek ini merupakan penelitian skripsi yang membandingkan performa tiga konfigurasi RAG (Config A, Config B, dan Config C) dalam menjawab pertanyaan seputar regulasi dan kalender akademik Universitas Sam Ratulangi (UNSRAT).

---

## 1. Gambaran Umum Proyek (Project Overview)

- **Nama Proyek:** unsrat-rag
- **Bahasa Pemrograman:** Python (Backend & Evaluasi), JavaScript (Frontend SPA), HTML/CSS (Interface), YAML (Conda Env), CSV (Dataset & Analisis).
- **Kerangka Kerja & Pustaka Utama:**
  - **FastAPI & Uvicorn:** Penyedia server web dan API backend.
  - **LangChain:** Orkestrasi alur RAG (Retrieval-Augmented Generation) dan integrasi LLM.
  - **ChromaDB:** Database vektor (Vector Store) untuk penyimpanan embedding dokumen akademik.
  - **Ragas:** Framework evaluasi performa RAG secara otomatis (faithfulness, answer relevance, dll.).
  - **rank-bm25:** Algoritma pencarian leksikal untuk Config C.
  - **google-generativeai:** Integrasi dengan API Gemini (sebagai generator/evaluator).
- **Deskripsi Singkat:** Chatbot berbasis RAG untuk membantu mahasiswa dan staf akademik UNSRAT mencari informasi regulasi kampus secara akurat. Chatbot ini menyajikan jawaban streaming secara real-time yang disertai dengan pencantuman sitasi inline dari dokumen sumber.

---

## 2. Lapisan Arsitektur (Architecture Layers)

Sistem ini dibagi menjadi 6 lapisan logis untuk menjaga pemisahan tanggung jawab (separation of concerns):

| Lapisan | Deskripsi | Berkas/Direktori Utama |
| :--- | :--- | :--- |
| **Lapisan Korpus & Data** | Berisi dokumen akademik resmi UNSRAT format Markdown dan berkas evaluasi CSV. | `data/corpus/`, `eval/dataset/`, `eval/results/` |
| **Lapisan Utama & Layanan** | Komponen inti RAG (ingestion, retrieval, konfigurasi, chain logic, dan logger terpusat). | `src/config.py`, `src/ingestion.py`, `src/retriever.py`, `src/chain.py`, `src/logger_manager.py` |
| **Lapisan API & Controller** | Server backend FastAPI yang mengelola request chat SSE dan visualisasi data hasil pengujian. | `app.py` |
| **Lapisan Antarmuka Pengguna** | Aplikasi satu halaman (SPA) front-end dengan visualisasi metrik performa. | `static/index.html`, `static/js/app.js` |
| **Lapisan Pengujian & Evaluasi** | Suite evaluasi menggunakan Ragas, uji statistik Wilcoxon, dan pengujian unit offline (pytest). | `evaluation.py`, `tests/conftest.py`, `tests/unit/`, `tests/integration/` |
| **Lapisan Dokumentasi & Rencana** | Spesifikasi kebutuhan perangkat lunak (PRD + SRS), rencana kerja, dan dokumentasi kemajuan. | `prd_srs.md`, `docs/implementation_status.md`, `docs/todo.md` |

---

## 3. Konsep & Keputusan Desain Utama (Key Concepts)

### A. Tiga Konfigurasi RAG yang Dibandingkan (Config A, B, dan C)
Penelitian ini membandingkan kinerja tiga metode pencarian informasi yang berbeda:
1. **Config A (Pencarian Vektor Semantik - Chunk Kecil):** Memotong dokumen dengan ukuran **500 karakter** (overlap 50), di-embed dengan `GoogleGenAIEmbeddings` (`text-embedding-004`), disimpan di ChromaDB, dan diambil menggunakan Similarity Search.
2. **Config B (Pencarian Vektor Semantik - Chunk Besar):** Memotong dokumen dengan ukuran **2000 karakter** (overlap 200), dengan sisa proses yang sama seperti Config A.
3. **Config C (Pencarian Leksikal BM25):** Menggunakan pencarian berbasis kata kunci murni (`rank-bm25`) tanpa menggunakan embedding vektor.

### B. Alur Evaluasi Ragas & Wilcoxon
Evaluasi dilakukan menggunakan dataset ground truth yang dikumpulkan dalam `eval/dataset/ground_truth.csv`. Metrik yang diukur meliputi:
- **Faithfulness:** Seberapa setia jawaban generator terhadap konteks yang ditemukan.
- **Answer Relevance:** Seberapa relevan jawaban terhadap pertanyaan kueri.
- **Context Recall:** Seberapa lengkap konteks yang ditemukan dibanding jawaban ideal.
- **Context Precision:** Seberapa presisi urutan konteks yang ditemukan.
- **Response Time:** Latensi waktu respons dalam hitungan detik.

Hasil pengujian Config A vs Config B diuji secara statistik dengan **Wilcoxon Signed-Rank Test** untuk menguji apakah ada perbedaan performa yang signifikan secara statistik.

### C. Sistem Sitasi Inline dan Streaming SSE
- Generator (LLM) diinstruksikan untuk menyisipkan referensi bernomor seperti `[1]`, `[2]`, dst. di dalam jawabannya.
- Logika di klien (`app.js`) dan parser sitasi di backend (`chain.py`) memetakan nomor-nomor tersebut secara dinamis ke potongan dokumen sumber asli yang relevan, sehingga pengguna dapat melihat teks asal referensi tersebut secara terpisah di UI.
- Jawaban dikirim dari FastAPI menggunakan Server-Sent Events (SSE) streaming untuk meningkatkan kenyamanan visual pengguna.

### D. Sistem Logging Terpusat & Exception Middleware
- Transaksi chat dicatat ke dalam berkas CSV (`logs/chat_transactions.csv`) untuk audit trail, sementara peristiwa sistem dicatat ke log harian (`logs/system.log`).
- Digunakan `RotatingFileHandler` dengan kapasitas maksimal 5MB per berkas dan 3 cadangan (backups) guna mencegah konsumsi memori/penyimpanan berlebih.
- Middleware penanganan exception terpusat di FastAPI (`app.py`) menangkap semua kesalahan runtime tidak terduga dan mengembalikan respons JSON terstandarisasi.

---

## 4. Tur Terpandu (Guided Tour)

Untuk mempelajari sistem ini secara bertahap, silakan ikuti tur berikut:

1. **Spesifikasi & Kebutuhan Sistem:** Pelajari [prd_srs.md](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/prd_srs.md) untuk memahami tujuan akademis, skema komparasi RAG, dan batasan penelitian.
2. **Data Pengetahuan Utama (Knowledge Base):** Baca [Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/data/corpus/Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md) and [Kalender_Akademik_UNSRAT_Genap_2025-2026.md](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/data/corpus/Kalender_Akademik_UNSRAT_Genap_2025-2026.md) untuk memahami format penulisan dokumen regulasi kampus yang diproses oleh RAG.
3. **Infrastruktur Log Sistem:** Buka [src/logger_manager.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/logger_manager.py) untuk melihat penyiapan log terpusat dengan rotasi file otomatis sebelum modul logika utama berjalan.
4. **Pipeline Ingestion data:** Buka [src/ingestion.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/ingestion.py) untuk melihat bagaimana file markdown dibersihkan, dipotong berdasarkan heading, dihitung tokennya, dan disimpan ke ChromaDB.
5. **Modul Retrieval:** Pelajari [src/bm25_retriever.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/bm25_retriever.py) (pencarian leksikal kata kunci) dan [src/retriever.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/retriever.py) (pencarian terpadu yang memadukan pencarian ChromaDB dan BM25 dengan penyaringan threshold relevansi).
6. **Rantai Utama RAG (RAG Chain):** Baca [src/chain.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/chain.py) untuk memahami proses orkestrasi pemanggilan retriever, penyusunan prompt instruksi, interaksi LLM Gemini/NIM, parser sitasi, dan stream generator.
7. **Entry Point Backend (FastAPI Server):** Buka [app.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/app.py) untuk mempelajari konfigurasi API endpoints `/api/chat` (SSE Streaming), `/api/evaluation` (memuat data hasil pengujian Ragas), dan middleware penanganan error global.
8. **Antarmuka Klien SPA:** Telusuri [static/index.html](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/static/index.html) dan [static/js/app.js](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/static/js/app.js) untuk melihat antarmuka Maroon Klasik, integrasi Chart.js untuk visualisasi grafik perbandingan performa Ragas, serta ekspor CSV log chat.
9. **Pipeline Evaluasi Skripsi:** Buka [evaluation.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/evaluation.py) untuk memahami bagaimana model evaluator memproses dataset acuan, menghitung rata-rata metrik kualitas jawaban, dan melakukan uji statistik Wilcoxon.
10. **Suite Pengujian Modular:** Pelajari berkas di folder `tests/` seperti [tests/conftest.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/conftest.py) (mock ChromaDB dan LLM API) dan [tests/unit/test_ingestion.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/unit/test_ingestion.py) guna memahami cara menjalankan pengujian unit dan integrasi secara offline untuk menjamin stabilitas fungsionalitas sistem.

---

## 5. Peta Berkas Utama (File Map)

Berikut adalah ringkasan fungsionalitas dari berkas-berkas penting proyek:

### Lapisan Utama & Layanan (`src/`)
- **[config.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/config.py) (Konfigurasi Utama):** Berisi semua konstanta konfigurasi, nama koleksi ChromaDB, model generator (`nvidia/llama-3.1-nemotron-nano-8b-v1`), model evaluator (`nvidia/llama-3.3-nemotron-super-49b-v1.5`), konfigurasi chunking, prompt sistem akademik UNSRAT, dan pesan fallback.
- **[logger_manager.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/logger_manager.py) (Log Manager):** Menyediakan logging terpusat dengan `RotatingFileHandler` untuk file log harian (`system.log`) dan log transaksi obrolan (`chat_transactions.csv`).
- **[ingestion.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/ingestion.py) (Data Ingest):** Memotong berkas Markdown korpus dengan heading-based chunking, menyaring data yaml yang tidak valid, membuat embedding, dan mendaftarkannya ke database vektor ChromaDB.
- **[bm25_retriever.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/bm25_retriever.py) (Retriever BM25):** Mengindeks kata kunci dokumen secara leksikal untuk kueri pencarian leksikal murni (Config C).
- **[retriever.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/retriever.py) (Unified Retriever):** Gerbang tunggal untuk mencari potongan dokumen yang relevan dari ChromaDB (Config A/B) maupun BM25 (Config C), lengkap dengan filter similarity threshold.
- **[chain.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/chain.py) (Orkestrator RAG):** Menggabungkan retrieval dan generasi LLM (Gemini/NIM API), menyaring kueri kosong, memproses sitasi, dan mengembalikan teks secara streaming.

### Lapisan API & Controller (`root`)
- **[app.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/app.py) (Server FastAPI):** Berkas inisialisasi aplikasi backend yang menyediakan rute obrolan `/api/chat` via SSE, rute pembacaan data evaluasi `/api/evaluation`, penyajian berkas statis frontend SPA, serta exception handler middleware global.

### Lapisan Pengujian & Evaluasi (`tests/` & `root`)
- **[evaluation.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/evaluation.py) (Pipeline Evaluasi):** Memuat data ground truth, mengirimkan pertanyaan ke sistem RAG, mengumpulkan jawaban, menghitung metrik Ragas dengan LLM evaluator, dan menghasilkan uji statistik Wilcoxon Signed-Rank Test.
- **[tests/conftest.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/conftest.py) (Mocking Test):** Mempersiapkan isolasi pengujian secara offline dengan melakukan *mocking* pada database vektor ChromaDB dan API LLM.
- **[tests/unit/test_ingestion.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/unit/test_ingestion.py) (Unit Test Ingestion):** Memastikan parser markdown dan pembuat ID chunk unik bekerja dengan benar.
- **[tests/unit/test_retriever.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/unit/test_retriever.py) (Unit Test Retriever):** Menguji logika retrieval vector search dan filter threshold.
- **[tests/integration/test_chat_api.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/tests/integration/test_chat_api.py) (API Integration Test):** Menguji keandalan HTTP status code dan aliran SSE streaming pada server FastAPI.

---

## 6. Titik Hotspot Kompleksitas (Complexity Hotspots)

Beberapa area dalam codebase memiliki tingkat kompleksitas tinggi yang perlu didekati secara hati-hati oleh developer baru:

1. **Logika RAG Chain dan Sitasi ([src/chain.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/chain.py)):**
   Orkestrasi streaming asinkron dan ekspresi reguler untuk mengekstrak nomor sitasi (`parse_cited_indices`) di dalam teks streaming cukup sensitif. Kesalahan kecil di sini dapat merusak render sitasi di frontend atau memicu kegagalan aliran data (SSE stream).
2. **Pipeline Ingestion dan Chunking ([src/ingestion.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/src/ingestion.py)):**
   Menguraikan berkas Markdown secara rekursif berdasarkan tingkatan Heading (`#`, `##`, `###`) membutuhkan penanganan struktur Markdown yang presisi. Perhatikan aturan kepatuhan metadata (seperti `doc_id`, `category`, dan `title` wajib) untuk mencegah error validasi database ChromaDB.
3. **Pipeline Evaluasi Ragas & Wilcoxon ([evaluation.py](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/evaluation.py)):**
   Bagian ini melibatkan kalkulasi multi-thread metrik Ragas yang mengonsumsi token API dalam jumlah besar dan rentan terhadap pembatasan laju pemanggilan API (rate limiting). Modul ini juga menghitung uji Wilcoxon menggunakan statistik non-parametrik yang memerlukan format data input CSV yang sangat ketat.
4. **Logika SPA JavaScript ([static/js/app.js](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/static/js/app.js)):**
   Logika penanganan streaming SSE dari server FastAPI, rendering Markdown secara real-time di sisi klien menggunakan Marked.js, penanganan tombol penghentian streaming (abort controller), dan visualisasi grafik performa interaktif berbasis Chart.js.

---

## 7. Cara Memulai Pengembangan (Quick Start)

### Persiapan Lingkungan (Setup Env)
1. Pastikan Anda telah menginstal **Conda** (Miniconda/Anaconda).
2. Buat lingkungan virtual berbasis berkas konfigurasi `environment.yml`:
   ```bash
   conda env create -f environment.yml
   conda activate unsrat-rag
   ```
3. Salin file konfigurasi environment `.env` dan isi kunci API Google Gemini Anda:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   NVIDIA_API_KEY=your_nvidia_api_key_here
   ```

### Menjalankan Ingestion Data (Membangun Database Vektor)
Lakukan proses *ingest* berkas korpus akademik ke database vektor:
```bash
python -m src.ingestion
```

### Menjalankan Server Utama
Jalankan server backend FastAPI secara lokal (server akan melayani frontend SPA di port `8000`):
```bash
python app.py
```
Akses chatbot melalui peramban di `http://127.0.0.1:8000`.

### Menjalankan Suite Pengujian (Pytest)
Jalankan seluruh suite pengujian unit dan integrasi secara offline untuk memastikan tidak ada fitur yang rusak:
```bash
pytest
```
