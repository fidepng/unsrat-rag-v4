# Desain Optimalisasi Logging & Testing — unsrat-rag

Spesifikasi desain ini menjelaskan arsitektur dan strategi implementasi untuk meningkatkan sistem logging serta testing pada proyek `unsrat-rag`. Sesuai dengan filosofi pengembangan di [prd_srs-v4.md](file:///D:/Kuliah/Skripsi Repository/unsrat-rag-v4-28.05.2026/prd_srs-v4.md) (Section 13 dan Section 18), desain ini memprioritaskan kesederhanaan, performa, serta kemudahan debugging tanpa mengenalkan dependensi eksternal yang kompleks.

---

## 1. Optimalisasi Logging & Middleware

Tujuan optimalisasi logging adalah memastikan seluruh aktivitas sistem tercatat dengan andal, terstruktur, aman dari kebocoran ruang penyimpanan, serta mencatat kesalahan sistem yang tidak tertangani (unhandled exceptions).

### 1.1 Logger Terpusat dengan Rotasi File
Kita akan memperbarui `src/logger_manager.py` menggunakan `logging.handlers.RotatingFileHandler` untuk mencegah file log `logs/unsrat_rag.log` membengkak tanpa kendali di server produksi/pengembangan.

* **File Tujuan**: `logs/unsrat_rag.log`
* **Handler**: `RotatingFileHandler`
* **Ukuran Maksimal**: 5 MB (`maxBytes=5 * 1024 * 1024`)
* **Backup Count**: 3 file cadangan (`backupCount=3`)
* **Encoding**: UTF-8 (`encoding="utf-8"`)
* **Format Log**:
  ```text
  %(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s
  ```

### 1.2 FastAPI Exception Logging Middleware
Kita akan menambahkan middleware di `app.py` untuk menangkap kesalahan tidak terduga (unhandled exceptions) di level HTTP route, mencatatnya ke log dengan traceback lengkap, dan mengembalikan respons JSON ramah pengguna (misal: HTTP 500 dengan pesan kesalahan terstandar).

* **Alur Penanganan**:
  1. Request masuk -> Middleware memproses request.
  2. Jika terjadi exception yang tidak ditangkap oleh route handler:
     * Catch exception.
     * Log error menggunakan `logger.exception("Unhandled exception occurred during request: {request.url.path}")`.
     * Kembalikan `JSONResponse` dengan status `500 Internal Server Error` dan format:
       `{"detail": "Terjadi kesalahan internal pada server. Silakan hubungi administrator."}`

---

## 2. Struktur Baru Direktori Pengujian (Testing)

Untuk memisahkan pengujian yang cepat (offline) dari pengujian yang lambat/membutuhkan internet (online), kita membagi struktur direktori pengujian sebagai berikut:

```text
tests/
│
├── unit/                         # Unit Test (100% Offline, Menggunakan Mock)
│   ├── __init__.py
│   ├── test_logger_manager.py    # Baru: Uji rotasi log dan validasi format CSV
│   ├── test_ingestion.py         # Baru: Uji parsing metadata markdown & chunking
│   ├── test_bm25_retriever.py    # Baru: Uji tokenisasi, pembuatan & pencarian index BM25
│   ├── test_retriever.py         # Baru: Uji seleksi retriever, threshold & hybrid scoring logic
│   ├── test_citation_parser.py   # Uji parser sitasi (memindahkan test_citation_parser.py)
│   └── test_chain.py             # Baru: Uji RAG chain orchestration offline (mock API/DB)
│
├── integration/                  # Integration Test (Uji integrasi API & Server)
│   ├── __init__.py
│   ├── test_spa_serving.py       # Uji serving static HTML/JS (memindahkan test_spa_serving.py)
│   └── test_chat_api.py          # Baru: Uji endpoint /api/chat secara offline (mock API/DB)
│
├── scripts/                      # Script verifikasi manual (tidak di-run otomatis oleh pytest)
│   ├── verify_ingestion.py       # Dipindahkan dari tests/
│   ├── verify_retriever.py       # Dipindahkan dari tests/
│   └── test_nvidia_nim_api.py    # Dipindahkan dari tests/
│
├── conftest.py                   # Pytest global fixtures, setup, & teardown
└── pytest.ini                    # Konfigurasi penanda (custom markers)
```

---

## 3. Konfigurasi Penanda (Custom Markers)

Kita akan membuat file [pytest.ini](file:///D:/Kuliah/Skripsi Repository/unsrat-rag-v4-28.05.2026/pytest.ini) untuk mendefinisikan marker sehingga developer dapat memfilter pengujian dengan mudah:

```ini
[pytest]
markers =
    offline: Pengujian yang berjalan sepenuhnya offline tanpa koneksi internet atau database eksternal.
    online: Pengujian konektivitas eksternal (misal: verifikasi API key Google/NVIDIA NIM).
```

* **Cara Menjalankan Offline Test (Sangat Cepat)**:
  ```bash
  pytest -m offline
  ```
* **Cara Menjalankan Semua Test**:
  ```bash
  pytest
  ```

---

## 4. Strategi Mocking Dependensi (Mocking Strategy)

Semua dependensi eksternal (API LLM, API Embeddings, Database ChromaDB) akan di-mock di dalam file `tests/conftest.py` menggunakan `unittest.mock`. Hal ini menjamin pengujian unit dapat berjalan dengan cepat, terprediksi, dan 100% offline.

### 4.1 Mocking ChromaDB
Kita mem-mock fungsionalitas ChromaDB agar tidak perlu menyentuh disk/menulis file nyata ke folder `chroma_db/`:
* `chromadb.PersistentClient` di-mock untuk mengembalikan client tiruan.
* Collection ChromaDB di-mock sehingga metode `.get()` dan `.query()` mengembalikan struktur data JSON tiruan yang menyerupai respons asli ChromaDB (berisi `ids`, `documents`, `metadatas`, dan `distances`).

### 4.2 Mocking LangChain Google GenAI (Embedding & LLM)
* **GoogleGenerativeAIEmbeddings**: Metode `.embed_query()` and `.embed_documents()` di-mock agar langsung mengembalikan vektor dummy berisi deretan float (misal: `[0.1, 0.2, ...]`) dengan dimensi yang sesuai.
* **ChatGoogleGenerativeAI**: Metode `.invoke()` atau `.stream()` di-mock agar mengembalikan respons `AIMessage` tiruan yang berisi teks markdown berformat sitasi seperti `"Berdasarkan dokumen [1], syarat kelulusan adalah..."`.

### 4.3 Mocking NVIDIA NIM (ChatOpenAI)
* **ChatOpenAI**: Panggilan ke endpoint OpenAI kompatibel tiruan milik NVIDIA NIM di-mock agar mengembalikan respons instan tanpa melakukan koneksi HTTP asli.

---

## 5. Matriks Cakupan Unit & Integration Testing

Berikut adalah detail unit-unit sistem yang diuji beserta target pengujiannya:

| Modul | File Test | Target Pengujian | Skenario Uji |
| :--- | :--- | :--- | :--- |
| **Logger** | `tests/unit/test_logger_manager.py` | `logger_manager.py` | - Uji pembuatan direktori logs jika belum ada.<br>- Uji fungsionalitas `log_ingestion_report` menulis baris baru CSV secara valid.<br>- Uji fungsionalitas `log_chat_transaction` menulis baris baru CSV secara valid. |
| **Ingestion** | `tests/unit/test_ingestion.py` | `ingestion.py` | - Uji `_make_chunk_id` menghasilkan hash md5 yang konsisten.<br>- Uji `_parse_and_chunk` melewatkan file jika YAML header wajib kosong.<br>- Uji two-stage split (Markdown Header & Recursive) memecah teks dengan benar. |
| **BM25 Retriever** | `tests/unit/test_bm25_retriever.py` | `bm25_retriever.py` | - Uji tokenizer (`_tokenize`) membersihkan tanda baca dan huruf kapital.<br>- Uji load chunks dari corpus & build index BM25 Okapi.<br>- Uji retrieval query Config C mengembalikan skor pencarian yang relevan. |
| **Vector Retriever**| `tests/unit/test_retriever.py` | `retriever.py` | - Uji retrieval Config B (Vector search) dengan mock database ChromaDB.<br>- Uji threshold similarity (hanya mengembalikan chunk dengan distance <= threshold). |
| **Citation Parser**| `tests/unit/test_citation_parser.py` | `chain.py` (`parse_cited_indices`) | - Uji parsing berbagai bentuk penulisan sitasi `[1]`, `[2]`, `[1, 2]`.<br>- Uji pembuangan kutipan yang berada di luar range `max_source_index`. |
| **RAG Chain** | `tests/unit/test_chain.py` | `chain.py` | - Uji orkestrasi penuh: input query -> retriever -> LLM -> parse citation -> estimasi token -> log transaksi CSV.<br>- Uji estimasi token offline menggunakan tiktoken (`cl100k_base`). |
| **App Routing** | `tests/integration/test_spa_serving.py` | `app.py` | - Uji endpoint root (`/`) menyajikan file HTML SPA.<br>- Uji endpoint static (`/static/js/app.js`) menyajikan static JS. |
| **App Chat API** | `tests/integration/test_chat_api.py` | `app.py` | - Uji endpoint POST `/api/chat` mengembalikan respons JSON valid dengan mock RAG chain.<br>- Uji middleware menangkap unhandled exception di app API dan mencatat stacktrace ke log system. |

---

## 6. Kepatuhan Terhadap Filosofi Pengembangan

1. **Modularitas**: Kode testing dipisah secara rapi dalam sub-direktori `unit/` dan `integration/`. File `conftest.py` menampung semua mock logic terpusat.
2. **Tanpa Dependensi Tambahan**: Menggunakan framework bawaan Python (`unittest.mock`) untuk mocking dan standard library Python (`logging.handlers.RotatingFileHandler`) untuk log rotasi. Tidak memerlukan library eksternal baru selain yang didefinisikan di `environment.yml`.
3. **Tanpa Efek Samping (Non-intrusive)**: Pengujian unit tidak menulis ke file log asli atau memodifikasi database ChromaDB operasional. Semua data selama testing menggunakan memori/mock temporer.
