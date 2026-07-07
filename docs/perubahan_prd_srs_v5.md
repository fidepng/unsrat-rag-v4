# Dokumen Poin-Poin Perubahan Penyusunan PRD-SRS v5
**Sistem Chatbot Informasi Akademik UNSRAT Berbasis RAG**

Dokumen ini merinci seluruh poin perubahan dari spesifikasi PRD-SRS versi v4 menuju versi v5 berdasarkan kondisi riil dan keputusan pengembangan terbaru pada codebase proyek saat ini. Format dokumen ini disusun secara paralel mengikuti struktur daftar isi dari dokumen PRD-SRS v4 asli.

---

## BAGIAN A — PRD (PRODUCT REQUIREMENTS DOCUMENT)

### 1. RINGKASAN EKSEKUTIF & KONTEKS
*   **Pergeseran Fokus Komparatif**: Fokus penelitian riset skripsi diubah dari membandingkan pengaruh ukuran chunk (Config A vs Config B) menjadi membandingkan pendekatan teknologi pencarian/retrieval (Config B: Dense Semantic Vector Search vs Config C: Sparse Keyword Okapi BM25). 
*   **Bypass Config A**: Config A (Vector search dengan chunk 500) secara resmi dinonaktifkan secara halus (*soft-disabled/archived*) dan diarsipkan untuk kebutuhan cadangan saja. Evaluasi kuantitatif sepenuhnya difokuskan pada perbandingan Config B vs Config C.

### 2. FILOSOFI PENGEMBANGAN
*   **Prinsip Netralitas Evaluasi (*Evaluation Neutrality*)**: Ditambahkan prinsip pengujian adil di mana chatbot harus menghasilkan jawaban fallback yang tidak mengandung klaim faktual positif agar tidak memicu bias penilaian metrik Ragas Faithfulness pada kueri Out-of-Domain (OOD).
*   **Standar Bahasa Indonesia Alami (*Natural Language Standard*)**: Ground truth beralih sepenuhnya menggunakan Bahasa Indonesia alami formal dan semi-formal. Pendekatan penerjemahan dialek/slang Manado resmi tidak lagi digunakan dalam dataset evaluasi demi mengisolasi variabel performa mesin pencari dari variabel translasi bahasa daerah.

### 3. TECH STACK & VERSI
*   **Integrasi NVIDIA NIM**: Ditambahkan provider **NVIDIA NIM (OpenAI-compatible API)** sebagai opsi utama untuk generator dan evaluator aktif guna mengatasi batasan rate-limit kuota Google AI Studio.
*   **Model Aktif Teruji**:
    *   **Generator**: `llama-3.1-nemotron-nano-8b-v1` (diakses via OpenAI compatible endpoint atau dipetakan dari model lokal `llama-3.1-8b-instruct`).
    *   **Evaluator**: `llama-3.3-nemotron-super-49b-v1.5` (diakses via OpenAI compatible endpoint atau dipetakan dari model lokal `qwen/qwen3-next-80b-a3b-instruct`). Hal ini memenuhi aturan **D-16** di mana model generator dan evaluator wajib berbeda demi menghindari bias evaluasi mandiri (*self-evaluation bias*).
    *   **Embedding**: Tetap menggunakan Google `models/gemini-embedding-001`.

### 4. STRUKTUR FOLDER (CANONICAL)
*   **Modul Tambahan**:
    *   `backup_original/`: Menyimpan salinan file asli v4 sebelum implementasi refaktor v5.
    *   `static/dev.html` & `static/js/dev.js`: Menampung antarmuka panel pengujian developer yang disajikan via route `/dev`.
    *   `.understand-anything/`: Folder cache visualisasi arsitektur kode.
*   **Tanggung Jawab File**: File `evaluation.py` dan `src/ingestion.py` diperbarui untuk memuat interceptor pemblokiran terhadap pemanggilan Config A.

### 5. SPESIFIKASI CORPUS & STANDAR YAML
*   **Penyederhanaan Validasi Frontmatter (D-B2)**: Konfirmasi runtime bahwa hanya field `doc_id`, `title`, dan `category` yang divalidasi secara ketat oleh parser ingestion. Field metadata lain (misalnya `valid_from`, `status`, `retrieval_summary`) diperbolehkan tetap ada di file `.md` sebagai dokumentasi pasif tetapi tidak diuji oleh parser guna menjaga kecepatan eksekusi.

### 6. ARSITEKTUR SISTEM & ALUR KERJA
*   **Penghentian Alur Config A**: Seluruh alur data chunking, indexing, dan retrieval untuk Config A dihentikan pada pipeline operasional.
*   **Pembersihan Data OOD**: Deteksi Out-of-Domain (OOD) dipisahkan dari evaluasi kuantitatif Ragas dan diperlakukan sebagai fitur chatbot murni berbasis threshold kesamaan (*similarity threshold*).
*   **Manajemen Memori Percakapan**: Penegasan alur stateless per-request pada `src/chain.py` dengan pembatasan memori hingga `MEMORY_K = 5` putaran percakapan terakhir secara dinamis tanpa mutasi state global backend.

### 7. SPESIFIKASI KONFIGURASI & PARAMETER
*   **Bypass Konstanta Config A**: Parameter `CHUNK_SIZE_A`, `CHUNK_OVERLAP_A`, `CHROMA_DIR_A`, dan `CHROMA_COLLECTION_A` di dalam `src/config.py` ditandai secara eksplisit dengan komentar `[BACKUP/DEPRECATED - ARCHIVED]`.
*   **Netralisasi Fallback Response**: `FALLBACK_RESPONSE` diubah menjadi pesan claim-free yang netral: *"Maaf, saya tidak menemukan informasi yang relevan mengenai pertanyaan Anda dalam dokumen regulasi yang tersedia."* Seluruh tautan dinamis atau referensi kontak dipindahkan ke static asset UI.
*   **Pemberlakuan Delay Evaluasi**: Penambahan parameter interval delay query `EVAL_QUERY_DELAY_NIM = 1.5` detik dan `EVAL_QUERY_DELAY_GOOGLE = 15.0` detik untuk menjaga kepatuhan batas RPM provider.

### 8. SPESIFIKASI FILE `.env`
*   **Variabel Tambahan**: Penambahan variabel lingkungan `NVIDIA_NIM_API_KEY` (opsional, hanya diisi jika menggunakan model NIM) untuk mendampingi `GOOGLE_API_KEY` (wajib).

### 9. FORMAT DATA EVALUASI
*   **Dataset Ground Truth Bersih**: File `eval/dataset/ground_truth.csv` dibersihkan dari 3 pertanyaan OOD (menyisakan total 30 kueri in-domain formal) dan seluruh teks pertanyaan dialek Manado diganti dengan kalimat Bahasa Indonesia alami formal yang merepresentasikan kebutuhan informasi mahasiswa secara akurat.
*   **Eksklusi File Hasil Config A**: Pipeline evaluasi tidak lagi menghasilkan file `hasil_config_a.csv` dan `error_analysis_config_a.csv`. Proses ekspor difokuskan ke Config B dan C.

### 10. SPESIFIKASI API BACKEND (FASTAPI)
*   **Filter `/api/config`**: Endpoint dikonfigurasi untuk hanya mengembalikan list konfigurasi aktif `["b", "c"]`.
*   **Endpoint Developer Baru**:
    *   `GET /dev`: Menyajikan halaman panel dasbor developer (`static/dev.html`).
    *   `GET /api/dev/status`: Memberikan informasi status database ChromaDB, status index BM25, serta ketersediaan API key.
    *   `GET /api/dev/preflight`: Menjalankan pengujian konektivitas real-time ke Google Embedding API, NIM Generator, dan NIM Evaluator.
    *   `GET /api/dev/runs`: Mengembalikan riwayat hasil pengujian dari `run_manifest.json`.
    *   `POST /api/dev/runs/activate`: Mengaktifkan data visualisasi dari arsip run evaluasi tertentu.
    *   `GET /api/dev/log/tail`: Membaca baris log sistem terakhir secara efisien melalui pencarian pointer biner.

### 11. SPESIFIKASI UI (SPA FRONTEND)
*   **Penyembunyian Config A**: Opsi selector Config A dikomentari pada `static/index.html`.
*   **Penghapusan Watchdog Klien**: Watchdog timer keras selama 30 detik pada JavaScript dihapus untuk mengakomodasi stream respons yang panjang dan latency LLM NIM.
*   **Mekanisme Manual Abort UX**: Memakai flag `isUserAborted` di mana jika stream diputus pengguna melalui tombol Stop, teks respons parsial tetap dipertahankan dan ditambahkan pesan peringatan: `⚠️ [Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap.]`.
*   **Pembaruan Chart Evaluasi**: Grafik Chart.js disesuaikan untuk hanya membandingkan performa metrik Config B vs Config C (menghapus dataset Config A).

### 12. SPESIFIKASI PIPELINE EVALUASI RAGAS
*   **Intersepsi Evaluasi Config A**: Jika CLI dijalankan dengan perintah `python evaluation.py --config a`, sistem akan mencetak pesan *"Config A is deprecated and archived for backup purposes."* dan keluar dengan bersih tanpa crash.
*   **Pengarsipan Uji Wilcoxon**: Flag `--stats` diblokir dan tidak lagi menjalankan uji Wilcoxon (A vs B) karena perbandingan bergeser ke B vs C (uji non-parametrik dua sampel berpasangan tidak relevan jika membandingkan dua metode dengan baseline chunk yang berbeda).
*   **Visualisasi Komparatif**: Output visualisasi diagram batang `perbandingan_visual.png` disesuaikan untuk membandingkan secara berdampingan Config B vs Config C.

### 13. SPESIFIKASI LOGGING TERPUSAT
*   **Ukuran Log Terkendali**: Log sistem utama `unsrat_rag.log` dibatasi ukuran rotasinya maksimal 5MB dengan mempertahankan maksimal 3 file backup untuk efisiensi penyimpanan lokal.

### 14. ATURAN KODE & HARD CONSTRAINTS
*   **Larangan Kritis Baru**:
    *   ❌ **DILARANG**: Menjalankan pipeline evaluasi kuantitatif menggunakan data kueri dialek daerah/Manado (karena ground truth telah distandardisasi).
    *   ❌ **DILARANG**: Menyertakan link eksternal atau klaim informasi faktual di dalam `FALLBACK_RESPONSE` di `src/config.py`.
    *   ❌ **DILARANG**: Memunculkan menu pilihan Config A atau Uji Wilcoxon di dashboard UI pengguna umum.
*   **Kewajiban Baru**:
    *   ✅ **WAJIB**: Mendukung parameter override model generator (`--model`) dan evaluator (`--evaluator`) dari command line pada `evaluation.py`.

### 15. SPESIFIKASI ERROR HANDLING
*   **SSE Error Event**: Jika API generator mengalami error di tengah streaming SSE, endpoint FastAPI harus me-yield event type `"error"` berisi pesan ramah pengguna dan menutup koneksi SSE dengan bersih agar status UI kembali ke `Ready`.

### 16. PANDUAN SETUP & GIT WORKFLOW
*   **Fokus Pipeline Ingestion**: Ingestion difokuskan hanya untuk Config B (`python src/ingestion.py --config b --rebuild`) dan BM25 Indexing (`python src/bm25_retriever.py --rebuild`). Pipeline Config A dilewati.

### 17. DAFTAR KEPUTUSAN ARSITEKTUR (DECISION LOG)
*   **Entri Keputusan Baru**:
    *   **D-B8 (24 Juni 2026)**: Pengarsipan Config A dan penonaktifkan Uji Wilcoxon guna memusatkan analisis skripsi pada performa Vector (Config B) vs BM25 (Config C).
    *   **D-B9 (4 Juli 2026)**: Netralisasi fallback response di `src/config.py` untuk menghilangkan bias matematika pada perhitungan metrik Faithfulness Ragas.
    *   **D-B10 (4 Juli 2026)**: Migrasi total ground truth ke Bahasa Indonesia alami/formal tanpa dialek Manado untuk memastikan validitas perbandingan retrieval.

### 18. STRATEGI MITIGASI BIAYA EVALUASI & PROVIDER ALTERNATIF
*   **Adopsi NVIDIA NIM**: Menjadikan OpenAI compatible endpoint NVIDIA NIM sebagai arsitektur default dalam script evaluasi offline, dengan penyesuaian delay dinamis agar tidak memicu pemblokiran koneksi API.

---

## BAGIAN B — SRS (SOFTWARE REQUIREMENTS SPECIFICATION)

### 19. FUNCTIONAL REQUIREMENTS (FR)
*   **FR-03 (Two-Stage Chunking)**: Dibatasi implementasinya hanya untuk Config B (Vektor 2000).
*   **FR-09 & FR-10 (Retrieval & Threshold)**: Diarahkan untuk mengembalikan chunk eksklusif dari Vektor Config B atau BM25 Config C.
*   **FR-22 (Uji Wilcoxon)**: ⚠️ **DIHAPUS/DIARSIPKAN** (Tidak dijalankan pada evaluasi B vs C).
*   **FR-25 (Config C Evaluation Support)**: Ditingkatkan menjadi kebutuhan fungsional utama yang sejajar dengan Config B.
*   **FR-37 (API Endpoint Status & Dev Dashboard)**: Kebutuhan fungsional baru untuk menyediakan dashboard `/dev` dan API endpoint preflight check untuk kelancaran debugging sistem.

### 20. NON-FUNCTIONAL REQUIREMENTS (NFR)
*   **NFR-13 (SSE Connection Resilience)**: Klien web harus mampu mengidentifikasi putusnya stream SSE secara prematur (misalnya karena crash backend) dan mengembalikan tombol UI ke kondisi "Ready" dengan menampilkan pesan error yang informatif.
*   **NFR-14 (Efficient Log Tail Reader)**: Pembacaan file log sistem dari browser developer (/dev) harus beroperasi dengan kompleksitas waktu O(1) menggunakan binary seek pointer tanpa me-load seluruh file log berukuran besar (>2MB) ke memori RAM backend.

### 21. CONSTRAINTS & ASSUMPTIONS
*   **Uptime Provider NIM**: Diasumsikan server NVIDIA NIM memiliki uptime yang tinggi selama proses running evaluasi massal (30 kueri berturut-turut).
*   **Ketersediaan API Key**: Diasumsikan key di dalam file `.env` telah dikonfigurasi dengan benar oleh peneliti sebelum aplikasi dinyalakan.

### 22. RENCANA ANALISIS HASIL (TEMPLATE BAB IV)
*   **Penyesuaian Matriks Komparasi**: Template Tabel 4.1 (Bab IV Skripsi) disesuaikan untuk hanya membandingkan dua kolom: **Config B (Vektor 2000)** dan **Config C (BM25 2000)** di bawah 4 metrik Ragas wajib (Faithfulness, Answer Relevancy, Context Precision, Context Recall).
*   **Fokus Pembahasan Kualitatif**: Diskusi difokuskan pada trade-off antara pencarian semantik (mampu menangkap sinonim formal) vs pencarian kata kunci leksikal (sangat presisi pada pencocokan singkatan regulasi atau nomor pasal spesifik).

### 23. SPESIFIKASI PENGUJIAN & VERIFIKASI (TESTING)
*   **Mock Global Config A**: Seluruh unit test pada `tests/` yang sebelumnya memverifikasi database Config A dinonaktifkan atau disesuaikan untuk memfokuskan verifikasi fungsionalitas retriever pada collections Config B dan BM25 Pickle Index.
