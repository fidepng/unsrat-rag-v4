# PROJECT REQUIREMENTS & SPECIFICATION DOCUMENT (PRD + SRS)

## Sistem Chatbot Informasi Akademik UNSRAT Berbasis RAG

**Nama Mahasiswa:** Teofide W. K. Pangemanan
**NIM:** 220211060317
**Program Studi:** Informatika / Ilmu Komputer
**Universitas:** Universitas Sam Ratulangi (UNSRAT) Manado

---

## KONTROL DOKUMEN

| Versi   | Tanggal     | Perubahan                                                                                                                                                                                                                                                                                                                            |
| ------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | 2025-12     | Draft awal                                                                                                                                                                                                                                                                                                                           |
| 2.0     | 2026-01     | Revisi arsitektur                                                                                                                                                                                                                                                                                                                    |
| 3.0     | 2026-05     | Revisi komprehensif (PRD)                                                                                                                                                                                                                                                                                                            |
| 4.0     | 2026-05     | Integrasi YAML Standard v2, perbaikan bug kritis, tambahan SRS                                                                                                                                                                                                                                                                       |
| 5.0     | 2026-05     | Tambah Config C (BM25), 5 metrik Ragas, pengukuran latensi, UI model switcher, uji Wilcoxon, analisis kegagalan, mitigasi self-eval bias, Section 19 Rencana Analisis Bab IV                                                                                                                                                         |
| 6.0     | 2026-05     | Sinkronisasi penuh dengan codebase aktual: migrasi FastAPI+SPA, hapus category UI, tambah logging terpusat, inline citation, git workflow, context7, revisi model evaluator                                                                                                                                                          |
| 7.0     | 2026-05     | \*\*Revisi arsitektur komprehensif: klarifikasi bug citation parsing, fix konflik MAX_RETRIES, klarifikasi retrieved_contexts vs citation_sources untuk Ragas, tambah provider alternatif (Ollama/NIM), upgrade skema log, hapus referensi usang Streamlit/PNG-UI, tambah Section 20 (Biaya Evaluasi & Provider Switching)           |
| **8.0** | **2026-05** | **Bug fix NIM integration (max_tokens & base_url), tambah Chart.js ke tech stack, klarifikasi memory stateless frontend, tambah panduan NIM embedding, tambah interpretasi skor BM25 vs cosine, tambah gap evaluasi (resume, threshold validation, urutan config), fix prompt engineering, klarifikasi 02-unsrat-red-variants.html** |
| **9.0** | **2026-05** | **Brainstorming refinement (Socratic): hapus summary chunk (D-B1), slim REQUIRED_YAML_FIELDS ke 3 field (D-B2), hapus priority+chunk_type dari ChromaDB (D-B3), hapus /api/log_transaction (D-B4), ganti reinitialize_llm() dengan _get_llm() stateless (D-B5), panduan ground_truth natural language (D-B6), wajib kalibrasi threshold empiris (D-B7)** |
| **10.0** | **2026-06** | **Optimalisasi logging dengan rotasi file log otomatis (RotatingFileHandler), penambahan middleware penanganan error global di app.py, modularisasi direktori tests/ dengan mock fixture conftest.py, dan penulisan test suite unit & integrasi lengkap.** |

> **PERINGATAN:** Dokumen ini adalah Sumber Kebenaran Tunggal (Single Source of Truth). Setiap
> keputusan teknis, nama file, nama variabel, dan nilai parameter yang tercantum di sini adalah
> STANDAR MUTLAK. Tidak boleh ada deviasi tanpa revisi tertulis pada dokumen ini terlebih dahulu.

---

## DAFTAR ISI

**BAGIAN A — PRD (Product Requirements Document)**

1. Ringkasan Eksekutif & Konteks
2. Filosofi Pengembangan
3. Tech Stack & Versi
4. Struktur Folder (Canonical)
5. Spesifikasi Corpus & Standar YAML
6. Arsitektur Sistem & Alur Kerja
7. Spesifikasi Konfigurasi & Parameter
8. Spesifikasi File `.env`
9. Format Data Evaluasi
10. Spesifikasi API Backend (FastAPI)
11. Spesifikasi UI (SPA Frontend)
12. Spesifikasi Pipeline Evaluasi Ragas
13. Spesifikasi Logging Terpusat
14. Aturan Kode & Hard Constraints
15. Spesifikasi Error Handling
16. Panduan Setup & Git Workflow
17. Daftar Keputusan Arsitektur (Decision Log)
18. Strategi Mitigasi Biaya Evaluasi & Provider Alternatif

**BAGIAN B — SRS (Software Requirements Specification)**

19. Functional Requirements (FR)
20. Non-Functional Requirements (NFR)
21. Constraints & Assumptions
22. Rencana Analisis Hasil (Template Bab IV)

---

# BAGIAN A — PRD

---

## 1. RINGKASAN EKSEKUTIF & KONTEKS

### 1.1 Deskripsi & Tujuan

Sistem tanya-jawab (Question-Answering) berbasis RAG untuk menjawab pertanyaan civitas akademika
UNSRAT tentang:

- Sejarah, profil, visi-misi, identitas institusi
- Peraturan Akademik resmi (Peraturan Rektor No. 01 Tahun 2025)
- Kalender Akademik Semester Genap 2025/2026
- Frequently Asked Questions dalam lingkungan Universitas (Status: Pending, setelah file tersedia)
- Informasi Umum Lainnya (Status: Pending)

**Sifat Proyek:** Prototipe penelitian Tugas Akhir/Skripsi. BUKAN sistem produksi.
**Fokus Penelitian:** Implementasi RAG + evaluasi kinerja _dua dimensi_:
(1) **Kualitas jawaban** — diukur via Ragas (faithfulness, answer_relevancy, context_precision, context_recall).
(2) **Performa sistem** — diukur via latensi respons (`response_time_seconds`).
**Metode Ilmiah:** Studi komparasi tiga konfigurasi:

- Config A: RAG chunking kecil (500 char)
- Config B: RAG chunking besar (2000 char) — _kandidat terbaik_
- Config C: BM25 murni (keyword search, tanpa embedding) — _baseline komparasi_

### 1.2 Batasan Masalah (Scope)

**DALAM RUANG LINGKUP:**

- Sistem tanya-jawab berbasis dokumen yang sudah tersedia
- Implementasi dan perbandingan dua strategi chunking (Config A vs B)
- Perbandingan RAG vs keyword search murni (Config B vs C)
- Evaluasi kuantitatif menggunakan framework Ragas
- API backend berbasis FastAPI dengan frontend SPA kustom

**DI LUAR RUANG LINGKUP (DILARANG):**

- Fitur transaksional (pengisian KRS, pendaftaran, dsb.)
- Manajemen akun / sistem login
- Integrasi dengan sistem informasi akademik UNSRAT yang ada
- Deployment ke server publik / production environment
- Fitur Reranking (Cohere, Jina, dsb.)
- Google Search Grounding / web browsing
- Metadata pre-filtering pada ChromaDB (lihat D-A2)

---

## 2. FILOSOFI PENGEMBANGAN

> **Prinsip Utama:** Setiap keputusan teknis harus melewati filter ini:
> _"Apakah kompleksitas tambahan ini secara langsung meningkatkan kualitas penelitian atau
> kemudahan debugging? Jika tidak, jangan tambahkan."_

| Fitur                        | Status           | Alasan                                                             |
| ---------------------------- | ---------------- | ------------------------------------------------------------------ |
| Reranking (Cohere/Jina)      | ❌ Tidak dipakai | Overkill untuk < 100 halaman                                       |
| Hybrid BM25 + Vector         | ❌ Tidak dipakai | Masing-masing sebagai config terpisah lebih bersih ilmiah          |
| **BM25 murni (Config C)**    | **✅ Dipakai**   | **Baseline komparasi ilmiah. Chunk size identik Config B**         |
| Category pre-filter ChromaDB | ❌ Dihapus       | Risiko false negative pada kueri singkat; embedding semantik cukup |
| Category badge di UI         | ❌ Dihapus       | Tidak ada nilai tambah sejak filter tidak digunakan (D-A2)         |
| Persistent user sessions     | ❌ Tidak dipakai | Fokus evaluasi RAG, bukan UX                                       |
| Database SQL chat history    | ❌ Tidak dipakai | In-memory sudah cukup                                              |
| Google Search Grounding      | ❌ Dilarang      | Biaya tambahan + keluar dari scope RAG                             |
| Multi-language support       | ❌ Tidak dipakai | Fokus Bahasa Indonesia                                             |
| Streamlit UI                 | ❌ Digantikan    | FastAPI + SPA memberikan kontrol DOM penuh dan tidak re-run script |
| Tiktoken (estimasi token)    | ✅ Dipakai       | Estimasi token offline tanpa API call tambahan (D-A5)              |
| Ollama / NVIDIA NIM          | ✅ Opsional      | Alternatif cost-free untuk skenario evaluasi; lihat Section 18     |

---

## 3. TECH STACK & VERSI

### 3.1 Runtime & Environment

| Komponen        | Spesifikasi                | Catatan                          |
| --------------- | -------------------------- | -------------------------------- |
| Bahasa          | Python 3.11                | Wajib 3.11                       |
| Package Manager | Conda (Miniconda/Anaconda) | BUKAN venv atau pip global       |
| Nama Conda Env  | `unsrat-rag`               | Nama standar, tidak boleh diubah |
| OS Pengembangan | Windows 11 Home 64-bit     |                                  |
| RAM             | 16 GB                      |                                  |
| GPU             | NVIDIA RTX 3050 Laptop     | Tidak dipakai (semua via API)    |

### 3.2 Library Python (`environment.yml`)

```yaml
name: unsrat-rag
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - pip:
      - langchain>=0.3.0
      - langchain-google-genai>=2.0.0
      - langchain-chroma>=0.1.0
      - langchain-community>=0.3.0 # Dibutuhkan untuk OllamaLLM (opsional, Section 18)
      - langchain-core>=0.3.0
      - langchain-ollama>=0.1.0 # Opsional: integrasi Ollama (Section 18)
      - chromadb>=0.5.0
      - ragas>=0.4.0 # Verifikasi API dengan `use context7` sebelum implementasi
      - fastapi>=0.100.0
      - uvicorn>=0.20.0
      - python-dotenv>=1.0.0
      - python-frontmatter>=1.0.0
      - pandas>=2.0.0
      - pyyaml>=6.0
      - matplotlib>=3.8.0
      - google-generativeai>=0.8.0
      - rank-bm25>=0.2.2 # Config C: BM25 pure keyword search baseline; digunakan LANGSUNG di src/bm25_retriever.py (bukan via LangChain wrapper) — D-A6
      - scipy>=1.11.0 # Uji signifikansi Wilcoxon signed-rank
      - tiktoken>=0.5.0 # Estimasi token offline
      - openai>=1.0.0 # Opsional: diperlukan untuk NVIDIA NIM via OpenAI-compatible endpoint (Section 18)
```

> **CATATAN RAGAS:** Sebelum mengimplementasikan `evaluation.py`, wajib menjalankan
> `use context7` untuk mendapatkan dokumentasi API Ragas versi yang terinstall.
> Nama class, cara instansiasi metrik, dan signature `evaluate()` berubah antar versi minor.
> Jangan asumsikan nama import dari memori.

> **CATATAN `use context7`:** Gunakan perintah `use context7` kapanpun membutuhkan
> informasi terkini tentang versi, dokumentasi, fungsi, atau cara import library apapun
> dalam proyek ini. Ini berlaku untuk semua library: LangChain, ChromaDB, Ragas,
> FastAPI, rank-bm25, tiktoken, langchain-ollama, openai (untuk NIM), dan lainnya.

### 3.3 Frontend Dependencies (CDN — Tidak Perlu Install)

| Library  | Versi | Digunakan Di       | Catatan                                              |
| -------- | ----- | ------------------ | ---------------------------------------------------- |
| Chart.js | 4.x   | `static/js/app.js` | Grouped bar chart komparasi 3 config di Tab Evaluasi |

Dimuat via CDN di `static/index.html`:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
```

> Tidak perlu diinstall ke conda environment. Tidak ada build step.
> use context7 untuk mendapatkan dokumentasi terbaru

### 3.4 Model AI

#### 3.4.1 Provider Utama & Core Demo (Google AI Studio — CANONICAL CORE)
> **INTEGRITAS JUDUL SKRIPSI:** Sistem RAG ini secara kanonik dirancang dan berjudul dengan menggunakan **Google Gemini** sebagai generator utama. Untuk keperluan demo akhir, sidang skripsi, dan rilis produksi, **Google Gemini (Google AI Studio) adalah Provider Utama yang wajib digunakan**.
> 
> Saat ini, generator utama kanonik adalah `gemini-3.5-flash` dan evaluator utama kanonik adalah `gemini-2.5-flash`.

| Komponen                    | Model Kanonik          | Provider Kanonik | Catatan Utama                          |
| --------------------------- | ---------------------- | ---------------- | -------------------------------------- |
| LLM Utama (RAG Generation)  | `gemini-3.5-flash`     | Google AI Studio | Generator Core Demo Akhir (Kanonik)   |
| Embedding                   | `gemini-embedding-001` | Google AI Studio | Embeddings Core (Kanonik)              |
| LLM Evaluator (Ragas Judge) | `gemini-2.5-flash`     | Google AI Studio | Evaluator Core (Mitigasi bias D-16)    |

#### 3.4.2 Provider Active Testing & Prototyping (NVIDIA NIM — Solusi Limit Kuota)
> **CATATAN TESTING:** Selama fase pengembangan, pengujian berulang (prototyping), dan evaluasi batch skripsi, model alternatif dari **NVIDIA NIM dapat digunakan secara aktif sebagai default pengujian** untuk mengatasi keterbatasan kuota Google AI Studio. 
> 
> Model pengujian aktif dikonfigurasi secara berbeda untuk **tetap mematuhi aturan D-16 (Self-Evaluation Bias Mitigation)** serta dioptimalkan untuk kecepatan dan efisiensi penalaran:

| Komponen                    | Model Pengujian Active                 | Provider   | Catatan Testing                        |
| --------------------------- | -------------------------------------- | ---------- | -------------------------------------- |
| LLM Utama (RAG Generation)  | `llama-3.1-nemotron-nano-8b-v1`        | NVIDIA NIM | Active Generator (Ultra-Cepat / Edge)  |
| LLM Evaluator (Ragas Judge) | `llama-3.3-nemotron-super-49b-v1.5`    | NVIDIA NIM | Active Evaluator (D-16 Terpenuhi)      |
| LLM Evaluator (Premium)          | `gemma-4-31b-it`                       | NVIDIA NIM | Reasoning kuat, alternatif evaluator   |
| LLM Utama (Standard)             | `llama-3.1-nemotron-nano-8b-v1`        | NVIDIA NIM | Model generator aktif                  |
| LLM Lokal (gratis, tanpa kuota)  | Model tersedia di Ollama               | Ollama     | Cocok untuk evaluasi batch             |

> **PERINGATAN KOMPARABILITAS:** Jika model evaluator diganti (misalnya dari `gemini-2.5-flash`
> ke `llama-3.3-nemotron-super-49b-v1.5`), hasil evaluasi Ragas TIDAK DAPAT dibandingkan secara
> apples-to-apples. Dokumentasikan secara eksplisit provider dan versi model yang digunakan
> untuk setiap sesi evaluasi di jurnal penelitian.

### 3.5 Keamanan Biaya

- **Budget Alert:** $50 (peringatan), $250 (kritis)
- **Hard Cap:** $280 (sisakan $20 buffer)
- **Dilarang:** Google Search Grounding ($14/1000 req)
- **Strategi efisiensi evaluasi:** Lihat Section 18 untuk opsi Ollama dan NVIDIA NIM

---

## 4. STRUKTUR FOLDER (CANONICAL)

```
unsrat-rag/                          ← Root folder proyek (git repository)
│
├── data/                            ← Semua aset data
│   └── corpus/                      ← File Markdown knowledge base
│       ├── 01_sejarah.md
│       ├── 02_visi_misi.md
│       ├── 03_tujuan_sasaran_strategi.md
│       ├── 04_lambang.md
│       ├── 05_bendera.md
│       ├── 06_mars_hymne.md
│       ├── 07_akreditasi.md
│       ├── Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md
│       ├── Kalender_Akademik_UNSRAT_Genap_2025-2026.md
│       └── [PENDING] faq.md
│
├── chroma_db/                       ← Database ChromaDB (auto-generated, di-gitignore)
│   ├── config_a/
│   └── config_b/
│
├── bm25_index/                      ← Indeks BM25 (auto-generated, di-gitignore)
│   └── bm25_index.pkl
│
├── eval/                            ← Semua aset evaluasi penelitian
│   ├── dataset/
│   │   └── ground_truth.csv
│   └── results/
│       ├── hasil_config_a.csv
│       ├── hasil_config_b.csv
│       ├── hasil_config_c.csv
│       ├── statistical_test.csv
│       ├── error_analysis_config_a.csv
│       ├── error_analysis_config_b.csv
│       └── perbandingan_visual.png   ← Output untuk lampiran skripsi/laporan (BUKAN dibaca UI runtime)
│
├── logs/                            ← Log sistem (auto-generated, di-gitignore)
│   ├── unsrat_rag.log               ← Log sistem lengkap (semua level)
│   ├── ingestion_report.csv         ← Laporan ingestion per run
│   └── transaksi_chat.csv           ← Audit trail setiap query (untuk debugging)
│
├── static/                          ← Aset frontend SPA
│   ├── index.html                   ← Entry point UI (SPA)
│   └── js/
│       └── app.js                   ← Logika frontend (fetch, SSE, render)
│
├── src/                             ← Source code modular (framework-agnostic)
│   ├── __init__.py
│   ├── config.py                    ← SEMUA parameter konfigurasi terpusat
│   ├── ingestion.py                 ← Pipeline data ingestion → ChromaDB
│   ├── retriever.py                 ← Unified retrieval interface (A/B/C)
│   ├── bm25_retriever.py            ← BM25 indexing & retrieval (Config C)
│   ├── chain.py                     ← Logika RAG (retriever + LLM + inline citation)
│   └── logger_manager.py            ← Logging terpusat (file + CSV audit)
│
├── tests/                           ← Modul pengujian terpadu (Pytest)
│   ├── unit/                        ← Pengujian unit (logger, ingestion, retriever, dll.)
│   ├── integration/                 ← Pengujian integrasi (FastAPI Chat API & SPA Serving)
│   ├── scripts/                     ← Skrip verifikasi mandiri (NIM, ingestion, retriever)
│   └── conftest.py                  ← Fixture mock global (ChromaDB, Gemini, NIM)
│
├── .env                             ← API Keys (TIDAK di-commit)
├── .gitignore
├── environment.yml
├── pytest.ini                       ← Konfigurasi penanda pengujian (offline/online)
├── app.py                           ← FastAPI backend (API Controller + Error Middleware)
└── evaluation.py                    ← Pipeline evaluasi Ragas (CLI)
```

### 4.1 Tanggung Jawab Tiap File

| File                    | Tanggung Jawab Tunggal                                      | Dipanggil Oleh              |
| ----------------------- | ----------------------------------------------------------- | --------------------------- |
| `src/config.py`         | Menyimpan SEMUA parameter & konstanta                       | Semua file                  |
| `src/ingestion.py`      | Baca .md → chunk → embed → ChromaDB (Config A & B)          | CLI langsung                |
| `src/retriever.py`      | Unified interface: Query → Config A/B/C → return chunks     | `src/chain.py`              |
| `src/bm25_retriever.py` | BM25 indexing & retrieval (Config C)                        | `src/retriever.py`          |
| `src/chain.py`          | RAG chain: retrieval + LLM + format inline citation         | `app.py`, `evaluation.py`   |
| `src/logger_manager.py` | Logging terpusat: system log, ingestion report, audit trail | Semua file yang butuh log   |
| `app.py`                | FastAPI controller: route HTTP request ke `src/chain.py`    | Uvicorn                     |
| `evaluation.py`         | Load CSV, evaluasi Ragas, statistik, simpan hasil           | CLI langsung                |
| `static/index.html`     | Entry point SPA: markup HTML dasar                          | Browser (via FastAPI serve) |
| `static/js/app.js`      | Frontend logic: fetch API, SSE stream, render UI            | Browser                     |
| `tests/conftest.py`     | Fixture mock global (Chroma, LLM, Embedding)                | Pytest                      |
| `tests/unit/`           | Suite pengujian unit modular offline                        | Pytest / CLI langsung       |
| `tests/integration/`    | Suite pengujian integrasi (API & SPA Serving)               | Pytest / CLI langsung       |
| `tests/scripts/`        | Skrip verifikasi mandiri (NIM, ingestion, retriever)        | CLI langsung                |

> **Prinsip Modularitas Backend:** Semua logika bisnis (RAG, retrieval, LLM) WAJIB ada
> di dalam `src/`. File `app.py` hanya boleh berisi route handler dan response formatting.
> Ini memungkinkan penggantian framework tanpa menyentuh kode inti.

---

## 5. SPESIFIKASI CORPUS & STANDAR YAML

### 5.1 Daftar Dokumen (Corpus Master List)

| #   | Nama File                                       | doc_id                  | category            | content_type | Priority | Status     |
| --- | ----------------------------------------------- | ----------------------- | ------------------- | ------------ | -------- | ---------- |
| 1   | `01_sejarah.md`                                 | UNSRAT-PROFILE-2020-001 | institution_profile | narrative    | 4        | ✅ Siap    |
| 2   | `02_visi_misi.md`                               | UNSRAT-PROFILE-2020-002 | institution_profile | narrative    | 4        | ✅ Siap    |
| 3   | `03_tujuan_sasaran_strategi.md`                 | UNSRAT-PROFILE-2020-003 | institution_profile | narrative    | 4        | ✅ Siap    |
| 4   | `04_lambang.md`                                 | UNSRAT-PROFILE-2020-004 | institution_profile | narrative    | 4        | ✅ Siap    |
| 5   | `05_bendera.md`                                 | UNSRAT-PROFILE-2020-005 | institution_profile | narrative    | 4        | ✅ Siap    |
| 6   | `06_mars_hymne.md`                              | UNSRAT-PROFILE-2020-006 | institution_profile | narrative    | 4        | ✅ Siap    |
| 7   | `07_akreditasi.md`                              | UNSRAT-PROFILE-2020-007 | institution_profile | narrative    | 3        | ✅ Siap    |
| 8   | `Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md` | UNSRAT-REG-2025-001     | academic            | regulation   | 1        | ✅ Siap    |
| 9   | `Kalender_Akademik_UNSRAT_Genap_2025-2026.md`   | UNSRAT-CAL-2026-001     | calendar            | calendar     | 2        | ✅ Siap    |
| 10+ | `faq.md`                                        | UNSRAT-FAQ-001          | faq                 | guide        | 2        | ⏳ PENDING |

> **Catatan:** Field `category` digunakan sebagai metadata di ChromaDB untuk
> keperluan audit dan filtering pada `error_analysis`. Ia TIDAK digunakan sebagai
> pre-filter saat retrieval runtime (lihat D-A2).

### 5.2 Standar YAML Frontmatter v2.0

Setiap file corpus WAJIB memiliki YAML frontmatter. Field kritis yang WAJIB terisi:

| Field               | Wajib? | Catatan                                                          |
| ------------------- | ------ | ---------------------------------------------------------------- |
| `doc_id`            | ✅     | Format: `UNSRAT-{TYPE}-{YYYY}-{NNN}`                             |
| `title`             | ✅     | Sama persis dengan judul di dokumen asli                         |
| `category`          | ✅     | Metadata ChromaDB; digunakan untuk error analysis post-hoc       |
| `content_type`      | ⬜     | Opsional — metadata ChromaDB; tidak dipakai untuk filter runtime |
| `valid_from`        | ⬜     | Opsional — dokumentasi tanggal berlaku dokumen                   |
| `status`            | ⬜     | Opsional — file yang ada di `data/corpus/` dianggap aktif        |
| `retrieval_summary` | ⬜     | Opsional — catatan dokumentasi manusia; tidak dibuat chunk       |
| `chunk_strategy`    | ⬜     | Opsional — dokumentasi metodologi (tidak runtime, D-A1)          |
| `last_updated`      | ⬜     | Opsional — tidak disimpan di ChromaDB                            |

**Contoh lengkap (field wajib + kritis):**

```yaml
---
doc_id: "UNSRAT-REG-2025-001"
title: "Peraturan Rektor UNSRAT Nomor 01 Tahun 2025 tentang Peraturan Akademik"
version: "1.0"
language_primary: "id"
institution: "Universitas Sam Ratulangi"
unit_penerbit: "Rektorat"
content_type: "regulation"
category: "academic"
subcategory:
  - "perkuliahan"
  - "evaluasi"
  - "wisuda"
audience:
  - "mahasiswa_s1"
  - "dosen"
access_level: "public"
nomor_sk: "01/2025"
tanggal_penetapan: "2025-02-13"
pejabat_penandatangan: "Oktovian Berty Alexander Sompie, Rektor UNSRAT"
source_document: "Peraturan-Rektor-Unsrat-Nomor-1-tahun-2025.pdf"
valid_from: "2025-02-13"
valid_until: null
status: "active"
last_updated: "2025-12-16"
last_verified: "2025-12-16"
retrieval_summary: "Peraturan Rektor UNSRAT Nomor 01 Tahun 2025 mengatur
  seluruh aspek akademik program sarjana di Universitas Sam Ratulangi,
  mencakup sistem kredit semester (SKS), pengisian KRS, evaluasi, cuti
  akademik, yudisium, dan wisuda. Berlaku bagi seluruh mahasiswa S1 dan
  dosen mulai Februari 2025."
chunk_strategy: "by_section"
chunk_notes: "Unit atomik adalah Pasal. Jangan memotong di tengah Pasal."
embedding_model: "gemini-embedding-001"
priority: 1
related_docs:
  - "UNSRAT-CAL-2026-001"
tags:
  - peraturan_akademik
  - kelulusan
  - wisuda
keywords:
  - "SKS"
  - "KRS"
  - "IPK"
  - "yudisium"
entities:
  - "Oktovian Berty Alexander Sompie"
  - "Portal INSPIRE"
---
```

---

## 6. ARSITEKTUR SISTEM & ALUR KERJA

### 6.1 Gambaran Keseluruhan

```
[File .md + YAML Frontmatter]
          │
          ▼
┌─────────────────────────────────────────────────┐
│  PIPELINE INGESTION (src/ingestion.py)          │
│  Dijalankan SEKALI per config via CLI           │
│                                                 │
│  1. Parse YAML frontmatter → ekstrak metadata   │
│  2. Buat "summary chunk" dari retrieval_summary │
│  3. MarkdownHeaderTextSplitter (struktural)     │
│  4. RecursiveCharacterTextSplitter (ukuran)     │
│  5. Filter: buang chunk < MIN_CHUNK_LENGTH      │
│  6. Cek hash per chunk → skip jika duplikat     │
│  7. Embed via gemini-embedding-001              │
│     (task_type = "retrieval_document")          │
│  8. Simpan ke ChromaDB collection terpisah      │
│  9. Log progress ke logger_manager              │
└─────────────────────────────────────────────────┘
          │
          ▼
  [chroma_db/config_a/ atau chroma_db/config_b/]
          │
          ▼
┌──────────────────────────────────────────────────────┐
│  PIPELINE RAG (src/chain.py)                         │
│  Dipanggil oleh app.py per request                   │
│                                                      │
│  Input: query + chat_history (list)                  │
│       │                                              │
│       ▼                                              │
│  [retriever.py: similarity search global k=4]        │
│  (task_type = "retrieval_query" untuk embed)         │
│       │                                              │
│  ┌────┴──────────────────────────────────────────┐   │
│  │ Tidak ada chunk lolos threshold?              │   │
│  │ → Return FALLBACK_RESPONSE tanpa panggil LLM  │   │
│  └───────────────────────────────────────────────┘   │
│       │ Ada chunk yang lolos                         │
│       ▼                                              │
│  [Format konteks + trim chat_history (MEMORY_K)]     │
│  [Kirim ke Gemini dengan SYSTEM_PROMPT inline cite]  │
│  [Parse response → ekstrak inline citations [N]]     │
│  [Return: response + citation_sources + found]       │
│  [Log ke logger_manager: query, answer, tokens]      │
└──────────────────────────────────────────────────────┘
```

### 6.2 Strategi Chunking (Two-Stage Hybrid Splitter)

Two-stage hybrid splitter adalah pendekatan optimal untuk corpus berbasis Markdown terstruktur (dokumen dengan BAB, Bagian, Pasal). Alasannya: Stage pertama menjamin batas chunk mengikuti batas logis dokumen (tidak memotong di tengah pasal peraturan), sementara Stage kedua menjamin tidak ada chunk yang terlalu besar untuk embedding API maupun terlalu kecil untuk memberikan konteks yang cukup.

**Tahap 1 — Structural Split (MarkdownHeaderTextSplitter):**

```python
headers_to_split_on = [
    ("#",    "header_1"),
    ("##",   "bab"),
    ("###",  "bagian"),
    ("####", "pasal"),
]
```

**Tahap 2 — Size Normalization (RecursiveCharacterTextSplitter):**

|                     | Config A              | Config B              | Config C (BM25)      |
| ------------------- | --------------------- | --------------------- | -------------------- |
| `chunk_size`        | 500                   | 2000                  | 2000 (sama dgn B)    |
| `chunk_overlap`     | 100                   | 200                   | 200 (sama dgn B)     |
| Metode retrieval    | Vector similarity     | Vector similarity     | BM25 keyword         |
| ChromaDB collection | `unsrat_rag_config_a` | `unsrat_rag_config_b` | Tidak pakai ChromaDB |
| Index               | `chroma_db/config_a/` | `chroma_db/config_b/` | `bm25_index.pkl`     |

> **CATATAN Config C:** BM25 mengindeks chunk berukuran 2000 char (identik Config B)
> bukan dokumen utuh. Ini wajib agar perbandingan RAG vs BM25 bersifat _apples-to-apples_ —
> variabel yang dibandingkan adalah teknik retrieval (vector vs keyword), bukan ukuran teks.
> Lihat D-A3.

> **CATATAN chunk_strategy:** Field `chunk_strategy` dan `chunk_notes` di YAML adalah
> metadata dokumentasi penelitian, bukan instruksi runtime. Pipeline selalu menggunakan
> two-stage splitter yang sama untuk semua dokumen. Lihat D-A1.

> **CATATAN retrieval_summary (D-B1):** Field ini TIDAK lagi digunakan untuk membuat
> summary chunk. Ia diturunkan menjadi field opsional untuk catatan dokumentasi manusia.
> Summary chunk telah dihapus dari pipeline — corpus < 100 halaman dengan two-stage
> chunking yang terstruktur sudah cukup tanpa mekanisme tambahan ini.

### 6.3 Metadata yang Disimpan per Chunk di ChromaDB

```python
{
    "doc_id":       str,   # "UNSRAT-REG-2025-001"
    "title":        str,   # Judul dokumen
    "category":     str,   # "academic", "calendar", dll. (metadata saja, bukan filter)
    "content_type": str,   # "regulation", "calendar"
    "bab":          str,   # Nama BAB
    "bagian":       str,   # Nama Bagian/Pasal
    "pasal":        str,   # Sub-pasal
    "chunk_id":     str,   # MD5 hash dari doc_id + content
    "status":       str,   # "active" (default; nilai tidak dicek runtime — D-B2)
}
```

> **CATATAN (D-B3):** Field `priority` dan `chunk_type` telah dihapus dari schema ini.
> `priority` tidak pernah dibaca oleh kode retrieval manapun (tidak ada reranking/pre-filter).
> `chunk_type` hanya relevan untuk summary chunk yang sudah dihapus (D-B1).

### 6.4 Strategi Retrieval — Global Similarity Search

**Metode:** ChromaDB similarity search tanpa metadata pre-filter.

Tidak ada category pre-filtering (lihat D-A2). Semua query mencari di seluruh collection.

**Similarity Threshold:**

- ChromaDB distance function: **cosine**
- Nilai mendekati 0 = lebih mirip, mendekati 2 = tidak mirip
- `SIMILARITY_THRESHOLD = 0.3` — buang chunk dengan distance > 0.3 (Hasil kalibrasi empiris)

### 6.5 Inline Citation — Mekanisme & Spesifikasi Parsing

Sistem menggunakan inline citation untuk mengidentifikasi bagian jawaban LLM yang bersumber dari dokumen tertentu, bukan sekadar menampilkan semua chunk yang di-retrieve.

**Alur:**

1. `chain.py` memformat konteks dengan penanda sumber: `[Sumber 1: judul — bab]`, `[Sumber 2: ...]`
2. `SYSTEM_PROMPT` menginstruksikan LLM untuk menyisipkan `[1]`, `[2]` di dalam teks jawaban pada bagian yang bersumber dari dokumen tersebut
3. `chain.py` mem-parsing response untuk mengekstrak referensi mana saja yang benar-benar dikutip
4. Hanya chunk yang dikutip (ada nomor referensinya dalam teks) yang dikembalikan sebagai `citation_sources`

**Contoh output jawaban LLM:**

```
Mahasiswa program sarjana dapat mengambil maksimal 24 SKS per semester [1].
Namun jika IPS semester sebelumnya kurang dari 2.00, beban maksimal adalah 18 SKS [1].
Semester genap 2025/2026 dimulai pada tanggal 3 Februari 2026 [2].
```

Dari contoh di atas, hanya chunk dari Sumber 1 dan Sumber 2 yang muncul di citation panel — bukan semua chunk yang di-retrieve.

**Spesifikasi Parsing Wajib (Resistansi terhadap Ketidakpatuhan LLM):**

LLM tidak selalu menghasilkan format marker yang sempurna. Parser HARUS diimplementasikan dengan aturan berikut untuk menghindari silent failure:

```python
import re

def parse_cited_indices(answer_text: str, max_source_index: int) -> list[int]:
    """
    Ekstrak nomor sumber yang dikutip LLM dari teks jawaban.

    Hanya mengenali format [N] (bracket dengan angka). Mengabaikan marker
    di luar range valid. Mengembalikan list kosong jika tidak ada kutipan
    yang valid — TIDAK crash.

    Args:
        answer_text: Teks jawaban dari LLM.
        max_source_index: Jumlah maksimum sumber yang tersedia (= jumlah chunk lolos threshold).

    Returns:
        List integer unik dan terurut dari nomor sumber yang dikutip.
    """
    raw_indices = re.findall(r'\[(\d+)\]', answer_text)
    valid_indices = []
    for idx_str in raw_indices:
        idx = int(idx_str)
        if 1 <= idx <= max_source_index:
            if idx not in valid_indices:
                valid_indices.append(idx)
        else:
            # Log warning jika LLM mengutip nomor di luar range
            logger.warning(f"LLM mengutip [{ idx }] tapi hanya ada {max_source_index} sumber tersedia. Diabaikan.")
    return sorted(valid_indices)
```

> **RULE:** Jika `parse_cited_indices()` mengembalikan list kosong (LLM tidak menggunakan
> marker sama sekali atau semua marker di luar range), sistem tetap mengembalikan jawaban
> teks dengan `citation_sources = []` dan `cited_indices = []`. JANGAN crash atau hapus
> jawaban. Catat di log level DEBUG.

### 6.6 Perbedaan Kritis: `retrieved_contexts` vs `citation_sources`

> **⚠️ INI KRITIS — JANGAN SALAH IMPLEMENTASI**

Dua konsep ini memiliki tujuan yang berbeda dan TIDAK boleh dicampur:

| Konsep               | Isi                                               | Digunakan Untuk                        | Bias Jika Salah                         |
| -------------------- | ------------------------------------------------- | -------------------------------------- | --------------------------------------- |
| `retrieved_contexts` | **Semua K chunk yang lolos similarity threshold** | Input ke `ragas.evaluate()` (WAJIB)    | `context_recall` bias tinggi artifisial |
| `citation_sources`   | Hanya chunk yang dikutip LLM dalam jawaban        | Tampilan UI citation panel + audit log | —                                       |

**Aturan definitif:**

- Untuk kolom `retrieved_contexts` di `hasil_config_*.csv` yang dikirim ke `ragas.evaluate()`, yang dimasukkan adalah **SEMUA chunk yang lolos threshold** (opsi a), bukan hanya `citation_sources`.
- `context_recall` mengukur apakah _semua_ informasi relevan berhasil diambil — metrik ini harus melihat seluruh konteks yang disediakan ke LLM, bukan hanya subset yang dikutip. Jika hanya cited chunks yang dilaporkan, `context_recall` akan bias ke atas secara artifisial dan tidak valid sebagai metrik ilmiah.
- `citation_sources` hanya untuk konsumsi UI dan audit trail `transaksi_chat.csv`.

### 6.7 Manajemen Memori Percakapan

```python
MEMORY_K = 5   # Simpan 5 pasang Q&A terakhir (= 10 pesan dalam list)
```

- Memori dikelola sebagai Python list biasa (BUKAN LangChain memory class — lihat D-04)
- List di-trim ke `MEMORY_K * 2` pesan sebelum dikirim ke LLM
- Memori hidup di memori aplikasi selama server berjalan; di frontend disimpan per-sesi
- Tidak pernah disimpan ke database

> **ARSITEKTUR STATELESS:** Backend (`chain.py` dan `app.py`) adalah **stateless per-request**.
> `chat_history` tidak disimpan di server — ia dikirim oleh frontend sebagai bagian dari
> setiap request body ke `/api/chat`. Ini berarti:
>
> - Setiap tab browser memiliki sesi memori yang independen (by design)
> - Server restart tidak butuh notifikasi khusus — history sudah ada di frontend
> - Tombol "Reset Percakapan" cukup mengosongkan array `chatHistory` di JavaScript frontend
>   dan tidak perlu memanggil endpoint backend apapun
>
> Implikasi untuk `evaluation.py`: karena stateless, cukup kirim `chat_history=[]` pada
> setiap call (FR-14) — tidak ada state yang perlu di-clear di sisi server.

### 6.8 Return Type Formal dari `chain.py`

```python
# Tipe data yang dikembalikan get_response() — mode non-streaming:
{
    "answer":            str,          # Teks jawaban dari LLM (atau pesan fallback)
    "citation_sources":  List[Dict],   # Hanya chunk yang dikutip LLM dalam jawaban (bisa [])
    "retrieved_contexts": List[str],   # SEMUA chunk yang lolos threshold — untuk Ragas evaluate()
    "found":             bool,         # True jika ada chunk yang lolos threshold
    "cited_indices":     List[int],    # Indeks sumber yang dikutip (misal [1, 2]); [] jika tidak ada
}

# Setiap item dalam "citation_sources":
{
    "index":    int,   # Nomor urut sumber (1-based, sesuai [N] dalam teks)
    "doc_id":   str,
    "title":    str,
    "bab":      str,
    "bagian":   str,
    "pasal":    str,
    "preview":  str,   # 150 karakter pertama isi chunk
    "content":  str,   # Full text chunk (untuk Ragas — meski digunakan via retrieved_contexts)
}
```

---

## 7. SPESIFIKASI KONFIGURASI & PARAMETER

Semua parameter sistem wajib didefinisikan di `src/config.py`.
**Tidak boleh ada angka "ajaib" (magic number) di dalam file lain.**

```python
# src/config.py — CANONICAL CONFIGURATION FILE

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── PATH ────────────────────────────────────────────────────
ROOT_DIR          = Path(__file__).parent.parent
CORPUS_DIR        = ROOT_DIR / "data" / "corpus"
CHROMA_BASE_DIR   = ROOT_DIR / "chroma_db"
CHROMA_DIR_A      = CHROMA_BASE_DIR / "config_a"
CHROMA_DIR_B      = CHROMA_BASE_DIR / "config_b"
BM25_INDEX_DIR    = ROOT_DIR / "bm25_index"
BM25_INDEX_PATH   = BM25_INDEX_DIR / "bm25_index.pkl"
EVAL_DATASET_PATH = ROOT_DIR / "eval" / "dataset" / "ground_truth.csv"
EVAL_RESULTS_DIR  = ROOT_DIR / "eval" / "results"
LOGS_DIR          = ROOT_DIR / "logs"
SYSTEM_LOG_PATH      = LOGS_DIR / "unsrat_rag.log"
CHAT_LOG_PATH        = LOGS_DIR / "transaksi_chat.csv"
INGESTION_LOG_PATH   = LOGS_DIR / "ingestion_report.csv"

# ── CHROMADB COLLECTIONS ────────────────────────────────────
CHROMA_COLLECTION_A = "unsrat_rag_config_a"
CHROMA_COLLECTION_B = "unsrat_rag_config_b"
CHROMA_DISTANCE_FN  = "cosine"

# ── MODEL ───────────────────────────────────────────────────
# Generator dan evaluator HARUS BERBEDA (D-16 — mitigasi self-eval bias)
# NVIDIA NIM Llama models are used for active testing due to Google AI Studio API limits.
LLM_MODEL_NAME       = "llama-3.1-nemotron-nano-8b-v1"
EMBEDDING_MODEL_NAME = "models/gemini-embedding-001"
EVALUATOR_MODEL_NAME = "llama-3.3-nemotron-super-49b-v1.5"

# Daftar model yang bisa dipilih di UI sidebar
# Catatan: model NVIDIA NIM menggunakan provider "openai_compatible" (lihat Section 18)
AVAILABLE_MODELS: list[str] = [
    "gemini-3.5-flash",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "llama-3.1-nemotron-nano-8b-v1",
    "llama-3.3-nemotron-super-49b-v1.5",
]

# ── CHUNKING — CONFIG A ──────────────────────────────────────
CHUNK_SIZE_A    = 500
CHUNK_OVERLAP_A = 100

# ── CHUNKING — CONFIG B ──────────────────────────────────────
CHUNK_SIZE_B    = 2000
CHUNK_OVERLAP_B = 200

# ── SEPARATORS ───────────────────────────────────────────────
CHUNK_SEPARATORS = ["\n\n", "\n", " ", ""]

# ── REQUIRED YAML FIELDS ─────────────────────────────────────────────
REQUIRED_YAML_FIELDS = [
    "doc_id", "title", "category",
    # CATATAN (D-B2): Hanya 3 field yang benar-benar dikonsumsi kode runtime.
    # Field lain (content_type, valid_from, status, retrieval_summary,
    # chunk_strategy, last_updated) tetap BOLEH ada di YAML sebagai dokumentasi,
    # tapi tidak divalidasi. File di data/corpus/ dianggap aktif by convention.
]

# ── RETRIEVAL ────────────────────────────────────────────────
RETRIEVAL_K          = 4
SIMILARITY_THRESHOLD = 0.3
MIN_CHUNK_LENGTH     = 50

# ── BM25 — CONFIG C ──────────────────────────────────────────
BM25_K             = 4
BM25_MIN_TOKEN_LEN = 2

# ── LLM GENERATION ──────────────────────────────────────────
LLM_TEMPERATURE       = 0.1
LLM_MAX_OUTPUT_TOKENS = 2048
LLM_TOP_P             = 0.95

# ── MEMORI ──────────────────────────────────────────────────
MEMORY_K = 5

# ── RETRY POLICY ────────────────────────────────────────────
# CATATAN: Dua policy berbeda untuk dua konteks berbeda.
# chain.py (interaktif, user menunggu) — policy ringan:
MAX_RETRIES  = 3
RETRY_DELAYS = [2, 5]   # detik: attempt 2 tunggu 2 detik, attempt 3 tunggu 5 detik

# ingestion.py (batch, rate-limit sensitif) — menggunakan konstanta LOKAL di ingestion.py:
# MAX_RETRIES_INGESTION = 5 dengan exponential backoff hingga 50 detik
# Didefinisikan di src/ingestion.py agar tidak mencemari namespace chain.py
# INTER_CHUNK_SLEEP = 0.2  # jeda antar chunk untuk menghindari quota burst

# ── EVALUASI ─────────────────────────────────────────────────
# Metrik wajib yang selalu dijalankan:
METRICS_COLS = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
]

# Metrik opsional — tidak dijalankan secara default karena butuh LLM call tambahan.
# Kode evaluation.py harus siap menerima metrik ini via flag --extra-metrics.
# context_entity_recall: mengukur apakah entitas penting (nama pasal, angka SKS,
# tanggal) tercantum dalam konteks yang diambil — sangat relevan untuk domain akademik.
# Aktifkan dengan: python evaluation.py --config a --extra-metrics context_entity_recall
OPTIONAL_METRICS_COLS = [
    "context_entity_recall",
    # Tambahkan metrik opsional lain di sini di masa depan
]

ERROR_ANALYSIS_N = 10

# ── REQUIRED YAML FIELDS — dikelola di atas (D-B2) ──────────

# ── SYSTEM PROMPT (TERKUNCI) ─────────────────────────────────
# CATATAN INLINE CITATION: Prompt ini menginstruksikan LLM untuk menyisipkan
# [1], [2], dst. di dalam teks jawaban pada bagian yang bersumber dari
# dokumen. chain.py akan mem-parsing marker ini untuk menghasilkan
# citation_sources yang akurat. Lihat Section 6.5 untuk spesifikasi parsing lengkap.
SYSTEM_PROMPT = """Anda adalah agen asisten informasi akademik resmi \
Universitas Sam Ratulangi.
Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan dokumen \
konteks yang disediakan di bawah ini.

PENTING: Jangan gunakan pengetahuan Anda di luar dokumen konteks yang \
disediakan, meskipun Anda mengetahuinya dari sumber lain.

Setiap klaim atau informasi dalam jawaban Anda HARUS disertai dengan \
penanda referensi inline berbentuk [N] di akhir kalimat yang bersumber \
dari dokumen tersebut, di mana N adalah nomor sumber yang tersedia \
dalam konteks.

Contoh format jawaban yang benar:
"Mahasiswa dapat mengambil maksimal 24 SKS per semester [1]. \
Kalender akademik semester genap dimulai pada Februari 2026 [2]."

Jika jawaban tidak ada di dalam dokumen konteks, katakan secara jujur \
bahwa Anda tidak menemukan informasinya dan arahkan mereka untuk \
menghubungi bagian administrasi kampus. Dalam kasus ini, \
jangan gunakan penanda referensi.

JANGAN PERNAH mengarang informasi, tanggal, atau angka SKS.
Jawab dalam Bahasa Indonesia yang ramah dan mudah dipahami."""

# ── FALLBACK RESPONSE ────────────────────────────────────────
FALLBACK_RESPONSE = (
    "Maaf, saya tidak menemukan informasi yang relevan mengenai "
    "pertanyaan Anda dalam dokumen yang tersedia. "
    "Untuk informasi lebih lanjut, silakan hubungi:\n\n"
    "• Bagian Akademik UNSRAT\n"
    "• Portal INSPIRE: inspire.unsrat.ac.id\n"
    "• Atau datang langsung ke Gedung Rektorat UNSRAT"
)

# ── API ──────────────────────────────────────────────────────
API_HOST = "0.0.0.0"
API_PORT = 8501

# ── API KEY ──────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY tidak ditemukan!\n"
        "Buat file .env di root proyek dan isi: GOOGLE_API_KEY=your_key_here"
    )

# NVIDIA NIM API Key (opsional — hanya dibutuhkan jika menggunakan provider NIM)
NVIDIA_NIM_API_KEY = os.getenv("NVIDIA_NIM_API_KEY")  # None jika tidak di-set, tidak crash
```

---

## 8. SPESIFIKASI FILE `.env`

```bash
# File: .env (di root proyek, sejajar dengan app.py)
# JANGAN commit file ini ke Git!

# API Key Google AI Studio (wajib)
GOOGLE_API_KEY=isi_dengan_api_key_anda_di_sini

# API Key NVIDIA NIM (opsional — hanya jika menggunakan provider NIM untuk evaluasi)
# Daftar di: https://build.nvidia.com/
# NVIDIA_NIM_API_KEY=nvapi-xxxxxxxxxxxxxxxx
```

File `.gitignore` WAJIB berisi:

```
.env
chroma_db/
bm25_index/
__pycache__/
*.pyc
.conda/
*.egg-info/
logs/
```

---

## 9. FORMAT DATA EVALUASI

### 9.1 Ground Truth (`eval/dataset/ground_truth.csv`)

**Format:** CSV UTF-8 (dengan BOM untuk kompatibilitas Excel)
**Jumlah baris:** 30-50 pasang data (target minimum 30)

```csv
user_input,reference,category,source_doc,notes
"Apa syarat yudisium program sarjana?","Mahasiswa dapat mengikuti yudisium...","academic","Peraturan_Akademik_UNSRAT_2025","Pasal 45"
```

**Distribusi yang direkomendasikan:**

- 40% → Peraturan Akademik (`academic`)
- 30% → Kalender Akademik (`calendar`)
- 20% → Profil institusi (`institution_profile`)
- 10% → FAQ (`faq`, setelah file tersedia)

### 9.2 Skema CSV Hasil (`eval/results/hasil_config_*.csv`)

```csv
user_input,reference,response,retrieved_contexts,citation_sources_count,faithfulness,answer_relevancy,context_precision,context_recall,response_time_seconds
```

> **CATATAN KRITIS — `retrieved_contexts`:**
> Kolom `retrieved_contexts` berisi **SEMUA** chunk yang lolos similarity threshold
> (bukan hanya yang dikutip LLM). Ini adalah input yang benar untuk `ragas.evaluate()`
> agar `context_recall` dapat diukur secara valid tanpa bias ke atas.
> `citation_sources_count` (jumlah chunk yang dikutip LLM) dicatat terpisah untuk audit,
> tapi TIDAK dikirim ke Ragas sebagai `retrieved_contexts`.
> Lihat Section 6.6 untuk penjelasan lengkap.

> **CATATAN `context_entity_recall`:** Kolom ini tidak ada di skema default. Jika evaluasi
> dijalankan dengan flag `--extra-metrics context_entity_recall`, kolom ini ditambahkan
> secara otomatis ke CSV hasil. Kode `evaluation.py` harus mengecek keberadaan kolom ini
> sebelum memproses (graceful degradation jika tidak ada).

### 9.3 Skema CSV Uji Statistik (`statistical_test.csv`)

```csv
metric,wilcoxon_statistic,p_value,significant_at_0.05,winner
faithfulness,12.0,0.031,True,Config B
```

### 9.4 Skema CSV Analisis Kegagalan (`error_analysis_config_*.csv`)

```csv
rank,user_input,reference,response,avg_metric_score,failure_type,failure_notes
```

`failure_type` diisi manual: `retrieval_failure` | `generation_failure` | `chunking_failure`

---

## 10. SPESIFIKASI API BACKEND (FASTAPI)

### 10.1 Deskripsi Umum

`app.py` adalah FastAPI application yang berjalan via Uvicorn pada port 8501.
Ia juga menyajikan file statis frontend (`static/`) sebagai SPA.

### 10.2 Endpoint

| Method | Path              | Deskripsi                                        |
| ------ | ----------------- | ------------------------------------------------ |
| GET    | `/`               | Sajikan `static/index.html`                      |
| GET    | `/api/config`     | Kembalikan daftar config dan model yang tersedia |
| POST   | `/api/chat`       | Proses query, kembalikan SSE stream              |
| GET    | `/api/evaluation` | Baca dan kembalikan statistik dari CSV hasil eval |

> **CATATAN (D-B4):** Endpoint `POST /api/log_transaction` telah dihapus. Semua logging
> ke `transaksi_chat.csv` dilakukan sepenuhnya di dalam `chain.py` via `logger_manager`
> setelah streaming selesai. Backend sudah memiliki semua data yang dibutuhkan; endpoint
> terpisah hanya menambah round-trip HTTP yang tidak perlu.

### 10.3 Spesifikasi `/api/chat`

**Request body:**

```json
{
    "query":        "string",
    "config":       "a" | "b" | "c",
    "chat_history": [{"role": "user"|"assistant", "content": "string"}],
    "model":        "string"
}
```

**Response:** `text/event-stream` (SSE)

Format setiap event:

```
data: {"type": "thinking", "content": "Sedang mencari informasi..."}

data: {"type": "token", "content": "teks jawaban token per token"}

data: {"type": "citations", "sources": [{"index": 1, "title": "...", "bab": "...", "pasal": "...", "preview": "..."}]}

data: {"type": "done"}

data: {"type": "error", "message": "Pesan error dalam Bahasa Indonesia"}
```

> **CATATAN Event `thinking`:** Dikirim SEBELUM token pertama untuk memberi feedback
> visual kepada pengguna bahwa sistem sedang memproses. Frontend harus menampilkan
> indikator "sedang berpikir" (typing indicator) saat menerima event ini.

> **CATATAN Event `citations`:** Dikirim SETELAH seluruh token selesai, berisi HANYA
> chunk yang benar-benar dikutip LLM (bukan semua top-K yang di-retrieve).

> **CATATAN Event `error`:** Dikirim alih-alih `token` jika terjadi error yang tidak
> bisa di-recover (setelah semua retry habis). Pesan error harus dalam Bahasa Indonesia
> dan dapat dimengerti pengguna (misalnya: "Batas kuota API tercapai. Coba lagi nanti."
> bukan stack trace teknis).

### 10.4 Spesifikasi `/api/config`

**Response body:**

```json
{
    "available_models": ["gemini-3.5-flash", ...],
    "active_model":     "gemini-3.5-flash",
    "configs":          ["a", "b", "c"]
}
```

---

## 11. SPESIFIKASI UI (SPA FRONTEND)

### 11.1 Prinsip UI

- `static/index.html` dan `static/js/app.js` adalah adapter UI murni
- Semua data berasal dari API call ke `app.py` — tidak ada logika bisnis di frontend
- Desain menggunakan skema warna Maroon Klasik UNSRAT sebagai referensi utama
  (file referensi: `02-unsrat-red-variants.html`, Variant 1: Maroon Klasik)

### 11.2 Komponen Utama (Dua Tab)

**Tab 1: 💬 Chatbot**

- Header identitas sistem (nama sistem, institusi)
- Sidebar: pilih Config (A / B / C), pilih Model dari `AVAILABLE_MODELS`, tombol Reset Percakapan
- Area chat (bubble pengguna + bubble asisten)
- Indikator "Sedang berpikir..." (thinking indicator) saat event `thinking` diterima — wajib, lihat 11.5
- Streaming response token per token via SSE
- Efek mengetik (typing animation) pada teks yang sedang di-stream — lihat 11.5
- Panel citation inline (lihat 11.3)
- Tampilan error yang jelas jika menerima event `error` — beda visual dari "tidak ada jawaban"
- Disclaimer penelitian

**Tab 2: 📊 Evaluasi Ragas**

- Tabel agregasi hasil (mean ± std) per config
- Tabel uji Wilcoxon (A vs B)
- Bar chart perbandingan 3 config (di-render via JavaScript dari data API — BUKAN membaca file PNG)
- Tabel live audit log (5 transaksi terakhir dari `transaksi_chat.csv`)
- Instruksi CLI jika belum ada hasil evaluasi

> **CATATAN `perbandingan_visual.png`:** File ini TETAP dihasilkan oleh
> `python evaluation.py --visualize` untuk keperluan lampiran skripsi dan laporan.
> Namun UI Tab 2 TIDAK membacanya — UI me-render grafik secara langsung dari data
> yang di-return oleh `/api/evaluation`. Ini menghilangkan dependensi UI pada file statis.

### 11.3 Citation Panel

Setelah streaming response selesai, frontend menerima event `citations` berisi array sumber yang dikutip. Panel citation menampilkan:

- Nomor referensi `[N]` sesuai yang muncul dalam teks jawaban
- Judul dokumen, nama BAB/Pasal
- Preview 150 karakter teks asli chunk

> Detail estetika (warna, animasi, layout spesifik) diserahkan ke desainer/developer.
> Yang wajib: nomor referensi harus konsisten antara `[N]` dalam teks dan item di panel citation.

### 11.4 Model Switcher

Selectbox di sidebar mengirim model baru ke `/api/chat` sebagai field `model` di request
body. Backend (`app.py`) meneruskan `model_name` ke `get_response()` di `chain.py`,
yang memanggil `_get_llm(model_name)` secara stateless.

```python
# chain.py — pattern stateless (D-B5), tidak ada global state mutation
_llm_cache: dict[str, Any] = {}

def _get_llm(model_name: str):
    """Kembalikan LLM instance. Cache per model name; tidak ada global mutation."""
    if model_name not in _llm_cache:
        _llm_cache[model_name] = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=LLM_TEMPERATURE,
            max_output_tokens=LLM_MAX_OUTPUT_TOKENS,
            top_p=LLM_TOP_P,
        )
    return _llm_cache[model_name]
```

> **CATATAN (D-B5):** `reinitialize_llm()` telah dihapus. Pendekatan `_get_llm()` sepenuhnya
> stateless per-request — konsisten dengan arsitektur backend (Section 6.7) dan mengeliminasi
> potensi race condition saat development/testing multi-tab.

### 11.5 Indikator Visual "Thinking" & Efek Mengetik

**Wajib diimplementasikan** untuk memberikan feedback bahwa sistem sedang aktif memproses, bukan hang.

**Thinking Indicator:**

- Ditampilkan saat SSE event `thinking` diterima (sebelum token pertama muncul)
- Visual: tiga titik animasi `( . . . )` atau teks _"Sedang mencari informasi..."_
- Hilang otomatis saat token pertama dari event `token` diterima

**Typing Animation:**

- Saat token di-stream satu per satu via SSE, teks muncul karakter demi karakter
- Efek ini sudah otomatis terjadi karena SSE streaming; pastikan tidak ada buffering berlebihan di frontend yang menumpuk token sebelum render

**Implementasi (JavaScript minimal):**

```javascript
// Saat menerima event type="thinking":
showThinkingIndicator(); // tampilkan animasi "..."

// Saat menerima event type="token" pertama:
hideThinkingIndicator(); // sembunyikan animasi
appendToken(content); // tambahkan teks ke bubble

// Saat menerima event type="error":
hideThinkingIndicator();
showErrorBubble(message); // tampilkan bubble error dengan warna/style berbeda
```

### 11.6 Akuntabilitas Elemen UI Tab Evaluasi

Setiap elemen di Tab Evaluasi harus dapat dipertanggungjawabkan sumber data dan dampak interpretasinya:

| Elemen UI                      | Sumber Data                         | Fungsi                                            | Dampak Interpretasi Jika Salah                                             |
| ------------------------------ | ----------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------- |
| Tabel mean ± std metrik        | `hasil_config_*.csv`                | Menunjukkan performa rata-rata per config         | Mean tanpa std menyembunyikan inkonsistensi sistem                         |
| Tabel Wilcoxon p-value         | `statistical_test.csv`              | Membuktikan perbedaan signifikan secara statistik | p-value tanpa konteks jumlah sampel bisa menyesatkan                       |
| Bar chart 3 config             | Data dari `/api/evaluation`         | Visualisasi komparasi cepat antar config          | Skala Y yang tidak dimulai dari 0 bisa memperbesar kesan perbedaan         |
| Audit log 5 transaksi terakhir | `transaksi_chat.csv`                | Debugging real-time dan monitoring sistem         | Bukan representasi statistik — hanya 5 transaksi terbaru                   |
| `context_recall` score         | Ragas evaluate (retrieved_contexts) | Mengukur apakah semua info relevan ter-retrieve   | BIAS ke atas jika hanya citation_sources yang dimasukkan ke Ragas          |
| `faithfulness` score           | Ragas evaluate                      | Mengukur apakah jawaban tidak mengarang           | Dipengaruhi kualitas model evaluator — dokumentasikan model yang digunakan |
| `response_time_seconds`        | `time.time()` di evaluation.py      | Mengukur latensi end-to-end                       | Termasuk latensi jaringan API — bukan murni komputasi lokal                |

---

## 12. SPESIFIKASI PIPELINE EVALUASI RAGAS

### 12.1 Metrik yang Diukur

> ⚠️ **WAJIB sebelum implementasi `evaluation.py`:** Jalankan `use context7` untuk
> mendapatkan dokumentasi API Ragas versi yang terinstall. Verifikasi nama class,
> cara instansiasi, dan signature `evaluate()`. Jangan tulis kode berdasarkan memori.

**Dimensi 1 — Kualitas Jawaban (via Ragas):**

| Metrik                  | Mengukur Apa                                                       | Target Min | Butuh `reference`? | Status      |
| ----------------------- | ------------------------------------------------------------------ | ---------- | ------------------ | ----------- |
| `faithfulness`          | Jawaban hanya dari dokumen, tidak mengarang                        | ≥ 0.90     | Tidak              | ✅ Wajib    |
| `answer_relevancy`      | Jawaban tepat sasaran terhadap pertanyaan                          | ≥ 0.85     | Tidak              | ✅ Wajib    |
| `context_precision`     | Chunk yang diambil relevan (tidak ada noise)                       | ≥ 0.80     | Ya                 | ✅ Wajib    |
| `context_recall`        | Semua informasi relevan berhasil diambil                           | ≥ 0.80     | Ya                 | ✅ Wajib    |
| `context_entity_recall` | Entitas penting (nama pasal, angka SKS, tanggal) ada dalam konteks | ≥ 0.75     | Ya                 | ⚙️ Opsional |

> **CATATAN `context_entity_recall`:** Metrik ini opsional dan tidak dijalankan secara default.
> Aktifkan dengan flag `--extra-metrics context_entity_recall`. Kode wajib disiapkan untuk
> menerimanya di masa depan — jangan hardcode daftar metrik tanpa mengecek `OPTIONAL_METRICS_COLS`
> dari `config.py`. Sangat relevan untuk domain akademik karena dokumen mengandung banyak entitas
> spesifik (nomor pasal, angka SKS, tanggal berlaku).

**Dimensi 2 — Performa Sistem:**

| Metrik                  | Mengukur Apa                 | Target     |
| ----------------------- | ---------------------------- | ---------- |
| `response_time_seconds` | Latensi end-to-end per query | Deskriptif |

### 12.2 Konfigurasi Ragas yang Direkomendasikan

Untuk menghindari kegagalan massal akibat rate limit Gemini (429):

```python
# Dalam evaluate() — konfigurasi sequential untuk stabilitas
run_config = RunConfig(
    max_workers=1,      # Sequential, bukan parallel
    timeout=300,        # 5 menit per metrik
    max_retries=10,
)
```

> **CATATAN:** `max_workers=1` secara drastis memperlambat evaluasi (30–50 sampel × 4 metrik
> bisa memakan 1–3 jam dengan provider Gemini). Ini trade-off yang disengaja antara kecepatan
> dan stabilitas. Lihat Section 18 untuk strategi mitigasi biaya dan waktu menggunakan
> Ollama atau NVIDIA NIM.

### 12.2b Protokol Evaluasi — Urutan dan Kontinuitas

**Aturan urutan config:**
Evaluasi ketiga config (A, B, C) **HARUS menggunakan model evaluator yang sama dalam satu
sesi penelitian berkesinambungan**.

### 12.3 Monkey Patch VertexAI (jika diperlukan)

Ragas versi terbaru mungkin mencoba mengimpor modul VertexAI pada runtime non-GCP.
Jika terjadi `ImportError` terkait VertexAI saat menjalankan `evaluation.py`, tambahkan
monkey patch di bagian paling atas file:

```python
# evaluation.py — baris paling atas, sebelum import lain
import sys
import types
# Bypass VertexAI import error pada runtime non-GCP
_mock_vertex = types.ModuleType("vertexai")
sys.modules.setdefault("vertexai", _mock_vertex)
```

> Ini adalah workaround yang diketahui valid untuk Ragas 0.4.x pada environment
> yang tidak memiliki Google Cloud SDK. Catat di jurnal penelitian.

### 12.4 Alur Kerja `evaluation.py`

```bash
# Evaluasi per config (termasuk latensi + error analysis otomatis)
python evaluation.py --config a
python evaluation.py --config b
python evaluation.py --config c   # BM25 baseline

# Dengan metrik opsional:
python evaluation.py --config a --extra-metrics context_entity_recall

# Uji statistik (setelah Config A & B selesai)
python evaluation.py --stats      # Wilcoxon A vs B → statistical_test.csv

# Visualisasi untuk lampiran skripsi (setelah semua config selesai)
python evaluation.py --visualize  # Bar chart → eval/results/perbandingan_visual.png
```

### 12.5 Catatan Metodologi

**Self-evaluation bias:** Generator (`gemini-3.5-flash`) dan evaluator (`gemini-2.5-flash`)
menggunakan model berbeda. Dokumentasikan pasangan model di laporan untuk reproduktibilitas.

**Config C (BM25):** BM25 tidak memanggil LLM untuk retrieval, tapi LLM tetap dipakai
untuk generate jawaban dari teks BM25. `context_precision` dan `context_recall` mengukur
kualitas retrieval BM25 secara langsung.

**Uji Wilcoxon:** `scipy.stats.wilcoxon` antara skor per-query Config A vs B.
Threshold: p < 0.05. Jika p ≥ 0.05, perbedaan tidak signifikan — tetap valid sebagai
temuan ilmiah dan harus didiskusikan di Bab 5.

**Keterbatasan:** Ground truth dibuat manual; jumlah sampel 30–50 terbatas secara
statistik. Akui keduanya di Bab 5.

---

## 13. SPESIFIKASI LOGGING TERPUSAT

### 13.1 Tanggung Jawab `src/logger_manager.py`

Satu file ini bertanggung jawab atas semua logging sistem. File lain tidak boleh
membuat logger sendiri — cukup import dari `logger_manager`.

### 13.2 Tiga Output Log

**1. System Log (`logs/unsrat_rag.log`)**

Log teks terstruktur semua aktivitas sistem. Format:

```
2026-05-27 14:23:01 | INFO     | ingestion    | Memproses: Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md
2026-05-27 14:23:05 | INFO     | ingestion    | ✓ 47 di-insert | 0 duplikat | 2 terlalu pendek
2026-05-27 14:25:11 | INFO     | chain        | Query: "Berapa SKS maksimal?" | Config: b | Model: gemini-3.5-flash
2026-05-27 14:25:13 | INFO     | chain        | Retrieved: 3 chunks | Cited: 2 | Latency: 2.14s
2026-05-27 14:25:13 | DEBUG    | chain        | LLM Output: "Mahasiswa dapat mengambil maksimal 24 SKS [1]..."
2026-05-27 14:25:13 | DEBUG    | chain        | Prompt (500 chars): "Anda adalah agen... [Sumber 1: Peraturan Akademik..."
2026-05-27 14:25:13 | WARNING  | retriever    | Tidak ada chunk lolos threshold untuk query: "cuaca hari ini"
2026-05-27 14:25:13 | WARNING  | chain        | Citation parsing: LLM mengutip [5] tapi hanya 3 sumber tersedia. Diabaikan.
2026-05-27 14:25:14 | ERROR    | chain        | Gemini API timeout — attempt 2/3. Retry dalam 5 detik.
2026-05-27 14:25:14 | ERROR    | chain        | Gemini API rate limit (429). Pesan ke user: "Batas kuota API tercapai."
```

Level yang digunakan:

- `DEBUG` — output LLM lengkap, prompt (truncated 500 char), detail retrieval per chunk, citation parsing detail
- `INFO` — aktivitas normal: query masuk, chunk count, latensi, ingestion progress
- `WARNING` — kondisi yang perlu diperhatikan: tidak ada chunk lolos, retry API, citation marker di luar range
- `ERROR` — kegagalan yang ter-handle: API timeout, rate limit, file tidak ditemukan

**2. Ingestion Report (`logs/ingestion_report.csv`)**

Skema baru (per run, bukan per file):

```csv
timestamp,config,files_processed,chunks_generated,chunks_inserted,chunks_duplicate_skipped,chunks_too_short_skipped,execution_time_seconds
2026-05-27 14:23:01,b,9,312,295,14,3,187.4
```

| Kolom                      | Arti                                                        | Nilai Ekspektasi           |
| -------------------------- | ----------------------------------------------------------- | -------------------------- |
| `timestamp`                | Waktu mulai ingestion run                                   | ISO datetime               |
| `config`                   | Konfigurasi yang diproses: `a` atau `b`                     | `a` / `b`                  |
| `files_processed`          | Jumlah file .md yang berhasil diproses                      | = jumlah file di corpus    |
| `chunks_generated`         | Total chunk yang dihasilkan sebelum filter                  | > `chunks_inserted`        |
| `chunks_inserted`          | Chunk yang berhasil disimpan ke ChromaDB                    | Angka terbesar             |
| `chunks_duplicate_skipped` | Chunk yang di-skip karena hash sudah ada di DB (idempotent) | 0 jika run pertama         |
| `chunks_too_short_skipped` | Chunk yang di-skip karena panjang < `MIN_CHUNK_LENGTH`      | Biasanya kecil             |
| `execution_time_seconds`   | Durasi total ingestion run dalam detik                      | Berguna deteksi bottleneck |

**3. Audit Trail Chat (`logs/transaksi_chat.csv`)**

Skema baru (lebih komprehensif untuk debugging dan analisis):

```csv
timestamp,config,model_llm,user_query,chunks_retrieved_count,retrieved_chunk_ids,best_similarity_score,average_similarity_score,response_time_seconds,estimated_prompt_tokens,estimated_completion_tokens,estimated_total_tokens,found_state,answer_preview
2026-05-27 14:25:11,b,gemini-3.5-flash,"Berapa SKS maksimal?",3,"chunk_id_1|chunk_id_2|chunk_id_3",0.31,0.42,2.14,1250,187,1437,true,"Mahasiswa dapat mengambil maksimal 24 SKS..."
```

| Kolom                         | Arti                                                         | Catatan Implementasi                            |
| ----------------------------- | ------------------------------------------------------------ | ----------------------------------------------- | ------------------------------- |
| `timestamp`                   | Waktu query masuk                                            | ISO datetime                                    |
| `config`                      | Konfigurasi retrieval: `a`, `b`, atau `c`                    |                                                 |
| `model_llm`                   | Model LLM yang digunakan untuk generation                    | Dari request body `model`                       |
| `user_query`                  | Pertanyaan pengguna (raw)                                    | Truncate ke 200 char untuk CSV                  |
| `chunks_retrieved_count`      | Jumlah chunk yang lolos similarity threshold                 | 0 jika `found_state = false`                    |
| `retrieved_chunk_ids`         | ID chunk yang diambil, dipisahkan `                          | `                                               | Untuk cross-reference debugging |
| `best_similarity_score`       | Distance cosine terkecil (chunk paling relevan)              | Mendekati 0 = sangat relevan                    |
| `average_similarity_score`    | Rata-rata distance cosine semua chunk yang lolos             | Indikator kualitas retrieval keseluruhan        |
| `response_time_seconds`       | Latensi end-to-end: dari query masuk hingga token terakhir   | Diukur di `chain.py`                            |
| `estimated_prompt_tokens`     | Estimasi token prompt via tiktoken `cl100k_base`             | Proxy untuk cost estimasi                       |
| `estimated_completion_tokens` | Estimasi token output via tiktoken                           | Proxy untuk cost estimasi                       |
| `estimated_total_tokens`      | `prompt + completion`                                        | = `estimated_prompt + estimated_completion`     |
| `found_state`                 | `true` jika ada chunk lolos threshold, `false` jika fallback |                                                 |
| `answer_preview`              | 200 karakter pertama jawaban LLM                             | Full answer ada di `unsrat_rag.log` level DEBUG |

> `retrieved_chunk_ids` dipisahkan dengan `|` (bukan koma) untuk kompatibilitas CSV.
> Untuk BM25 (Config C), `best_similarity_score` dan `average_similarity_score` diisi
> dengan BM25 score tertinggi/rata-rata (bukan cosine distance).

### 13.3 Estimasi Token (Tiktoken)

Gunakan `tiktoken` dengan encoding `cl100k_base` untuk estimasi jumlah token secara
offline. Ini menghasilkan estimasi yang cukup akurat untuk Gemini tanpa API call tambahan.

```python
import tiktoken
_enc = tiktoken.get_encoding("cl100k_base")

def estimate_tokens(text: str) -> int:
    """Estimasi jumlah token untuk teks menggunakan tiktoken cl100k_base."""
    return len(_enc.encode(text))
```

### 13.4 Aturan Logging

- Semua file log berada di `logs/` yang ada di `.gitignore`
- Log tidak pernah berisi API key atau data sensitif
- `logs/transaksi_chat.csv` dibaca oleh dashboard evaluasi di Tab 2 UI
- Ukuran `unsrat_rag.log` dibatasi secara otomatis dengan `RotatingFileHandler` (maksimal 5MB, menyimpan 3 berkas backup) untuk mencegah pembengkakan log.

---

## 14. ATURAN KODE & HARD CONSTRAINTS

### 14.1 Hal yang TIDAK BOLEH Dilakukan

```python
# ❌ DILARANG: Hardcode API Key
GOOGLE_API_KEY = "AIza..."

# ❌ DILARANG: Magic number di luar config.py
results = vectorstore.similarity_search(query, k=4)  # k harus dari config!

# ❌ DILARANG: Logika RAG di dalam app.py
# app.py hanya boleh memanggil fungsi dari src/chain.py

# ❌ DILARANG: Google Search Grounding
# ❌ DILARANG: Import reranking library (cohere, jina)
# ❌ DILARANG: Hardcode path absolut
# ❌ DILARANG: Import rank_bm25 di luar src/bm25_retriever.py
# ❌ DILARANG: Membuat logger baru di luar src/logger_manager.py
# ❌ DILARANG: Category detection untuk pre-filter retrieval (telah dihapus — D-A2)
# ❌ DILARANG: Menampilkan semua top-K retrieved chunks di UI citation panel
#             (hanya tampilkan chunk yang benar-benar dikutip LLM — lihat Section 6.5)
# ❌ DILARANG: Mengirim citation_sources ke ragas.evaluate() sebagai retrieved_contexts
#             (lihat Section 6.6 — ini akan membuat context_recall bias ke atas)
# ❌ DILARANG: Crash saat citation parsing gagal — kembalikan citation_sources=[] (Section 6.5)
```

### 14.2 Hal yang WAJIB Dilakukan

```python
# ✅ Semua parameter dari config.py
from src.config import RETRIEVAL_K, SIMILARITY_THRESHOLD

# ✅ Setiap fungsi punya docstring
def get_response(query: str, ...) -> dict:
    """Dapatkan respons RAG untuk pertanyaan yang diberikan."""

# ✅ Memory reset saat evaluasi
chat_history = []  # Reset sebelum setiap pertanyaan evaluasi

# ✅ task_type berbeda untuk embed dokumen vs query
# Ingestion: task_type="retrieval_document"
# Query:     task_type="retrieval_query"

# ✅ Logging semua aktivitas via logger_manager
from src.logger_manager import get_logger
logger = get_logger(__name__)

# ✅ Gunakan `use context7` untuk verifikasi API library sebelum implementasi

# ✅ retrieved_contexts untuk Ragas = semua chunk lolos threshold (bukan citation_sources)
retrieved_contexts_for_ragas = [chunk["content"] for chunk in all_retrieved_chunks]

# ✅ Ingestion menggunakan konstanta lokal untuk retry (BUKAN MAX_RETRIES dari config.py)
# MAX_RETRIES_INGESTION = 5  # di dalam src/ingestion.py

# ✅ Citation parsing tidak crash — kembalikan [] jika tidak ada marker valid
cited_indices = parse_cited_indices(answer_text, max_source_index=len(retrieved_chunks))
```

### 14.3 Aturan Commit Git

Setiap commit HARUS menggunakan format pesan yang jelas:

```
<type>: <deskripsi singkat dalam bahasa Indonesia>

Tipe yang valid:
  feat     — fitur baru
  fix      — perbaikan bug
  refactor — refaktor kode tanpa mengubah fungsi
  docs     — perubahan dokumentasi
  chore    — setup, konfigurasi, tooling
  test     — penambahan atau perubahan test
  style    — formatting, tidak mengubah logika

Contoh:
  feat: tambah src/chain.py — RAG chain dengan inline citation
  fix: perbaiki double API call di get_response streaming mode
  chore: tambah .gitignore dan setup environment awal
  docs: update SYSTEM_PROMPT untuk instruksi inline citation [N]
```

---

## 15. SPESIFIKASI ERROR HANDLING

### 15.1 Tabel Error & Penanganannya

| Skenario                                  | Lokasi          | Penanganan                                                        | Pesan ke User (Bahasa Indonesia)                            |
| ----------------------------------------- | --------------- | ----------------------------------------------------------------- | ----------------------------------------------------------- |
| `GOOGLE_API_KEY` tidak ditemukan          | `config.py`     | `ValueError` dengan pesan jelas; log ERROR                        | — (crash sebelum server berjalan)                           |
| `chroma_db/config_[a\|b]/` tidak ada      | `retriever.py`  | `RuntimeError` + instruksi CLI                                    | — (crash sebelum request)                                   |
| `ground_truth.csv` tidak ditemukan        | `evaluation.py` | `FileNotFoundError` + path ditampilkan                            | — (CLI, bukan UI)                                           |
| File .md tidak punya frontmatter          | `ingestion.py`  | `ValueError` + nama file; skip & log WARNING                      | — (CLI, bukan UI)                                           |
| Field wajib frontmatter kosong            | `ingestion.py`  | `ValueError` + nama field + nama file; log WARNING                | — (CLI, bukan UI)                                           |
| Gemini API timeout (setelah semua retry)  | `chain.py`      | SSE event `error`                                                 | "Permintaan ke server AI timeout. Coba lagi beberapa saat." |
| Gemini API rate limit / quota habis (429) | `chain.py`      | Retry → jika gagal semua: SSE event `error`                       | "Batas kuota API tercapai. Coba lagi beberapa menit."       |
| Gemini API error umum (500, dll)          | `chain.py`      | Retry → jika gagal semua: SSE event `error`                       | "Terjadi gangguan pada layanan AI. Coba lagi nanti."        |
| Tidak ada chunk lolos threshold           | `chain.py`      | Return `{"found": False}` — BUKAN error, ini kondisi valid        | Gunakan `FALLBACK_RESPONSE` (pesan "tidak ada informasi")   |
| Chunk terlalu pendek                      | `ingestion.py`  | Log WARNING + skip                                                | — (CLI)                                                     |
| Chunk duplikat                            | `ingestion.py`  | Log INFO + skip (idempotent)                                      | — (CLI)                                                     |
| Citation marker di luar range             | `chain.py`      | Log WARNING; abaikan marker tersebut; jawaban tetap ditampilkan   | — (tidak perlu ditampilkan ke user)                         |
| Citation parsing gagal total              | `chain.py`      | Log DEBUG; kembalikan `citation_sources=[]`; jawaban tetap tampil | — (citation panel kosong adalah acceptable)                 |
| CSV hasil tidak ada saat `--visualize`    | `evaluation.py` | Error jelas: "Jalankan evaluasi terlebih dahulu"                  | — (CLI)                                                     |
| VertexAI import error (Ragas)             | `evaluation.py` | Monkey patch di baris paling atas (Section 12.3)                  | — (CLI)                                                     |

> **PRINSIP:** Error yang mempengaruhi user (terjadi saat user menunggu respons) HARUS
> dikomunikasikan via SSE event `error` dengan pesan Bahasa Indonesia yang jelas.
> Error yang terjadi di pipeline offline (ingestion, evaluation) cukup di-log ke terminal
> dan `unsrat_rag.log`.

### 15.2 Retry Policy

```python
# ── src/chain.py (interaktif, user menunggu) ──────────────────────────────
# Dari config.py — policy ringan agar user tidak menunggu terlalu lama:
MAX_RETRIES  = 3           # dari config.py
RETRY_DELAYS = [2, 5]      # detik: attempt 2 tunggu 2s, attempt 3 tunggu 5s

# ── src/ingestion.py (batch, rate-limit sangat sensitif) ──────────────────
# KONSTANTA LOKAL di ingestion.py — BUKAN dari config.py:
MAX_RETRIES_INGESTION = 5
# Backoff eksponensial: 2s, 4s, 8s, 16s, 32s (maks ~50 detik per attempt)
# INTER_CHUNK_SLEEP = 0.2  # jeda antar chunk untuk menghindari quota burst

# ALASAN DUA POLICY BERBEDA:
# - ingestion.py: batch proses ratusan chunk sekaligus, sangat rentan 429.
#   Retry agresif lebih baik daripada ingestion gagal di tengah jalan.
# - chain.py: single-query interaktif. Pengguna tidak boleh menunggu >30 detik.
#   Jika 3x retry gagal, lebih baik tampilkan error + minta coba ulang.
```

### 15.3 Penanganan Kesalahan Global Backend (Middleware)

Aplikasi FastAPI (`app.py`) dilengkapi dengan handler eksepsi global menggunakan decorator `@app.exception_handler(Exception)` untuk menangkap seluruh pengecualian yang tidak tertangani selama runtime:

- **Logging**: Traceback kesalahan dicatat secara otomatis ke file log utama (`logs/unsrat_rag.log`) menggunakan `logger.exception()`.
- **Response**: Mengembalikan status HTTP 500 dengan pesan JSON seragam (bukan raw stack trace yang sensitif demi keamanan):
  ```json
  {"detail": "Terjadi kesalahan internal pada server. Silakan hubungi administrator."}
  ```

---

## 16. PANDUAN SETUP & GIT WORKFLOW

### 16.1 Inisialisasi Proyek (Sekali Saja)

```bash
# Langkah 1: Inisialisasi Git — WAJIB sebagai langkah pertama
git init
git add .gitignore environment.yml src/__init__.py
git commit -m "chore: inisialisasi proyek — git init, environment, gitignore"

# Catatan: remote GitHub ditambahkan manual oleh user setelah init lokal
git remote add origin https://github.com/fidepng/unsrat-rag-v4.git
```

### 16.2 Setup Environment

```bash
# Langkah 2: Buat environment
conda env create -f environment.yml
conda activate unsrat-rag

# Langkah 3: Verifikasi library kritis
python --version        # Harus: Python 3.11.x
python -c "import langchain; print('langchain:', langchain.__version__)"
python -c "import chromadb; print('chromadb:', chromadb.__version__)"
python -c "import ragas; print('ragas:', ragas.__version__)"
python -c "import fastapi; print('fastapi:', fastapi.__version__)"
python -c "import tiktoken; print('tiktoken OK')"
python -c "from rank_bm25 import BM25Okapi; print('rank-bm25 OK')"
python -c "from scipy.stats import wilcoxon; print('scipy OK')"
```

### 16.3 Ingestion & Build Index

```bash
# Langkah 4: Buat direktori yang diperlukan
mkdir -p data/corpus eval/dataset eval/results logs

# Langkah 5: Verifikasi YAML frontmatter corpus sebelum ingestion
python -c "
import frontmatter
from pathlib import Path
from src.config import CORPUS_DIR, REQUIRED_YAML_FIELDS
for f in sorted(CORPUS_DIR.glob('*.md')):
    post = frontmatter.load(f)
    missing = [field for field in REQUIRED_YAML_FIELDS if not post.metadata.get(field)]
    status = 'ERROR' if missing else 'OK'
    print(f'{status}: {f.name}' + (f' — field kosong: {missing}' if missing else ''))
"

# Langkah 6: Ingestion ChromaDB
python src/ingestion.py --config a --rebuild
python src/ingestion.py --config b --rebuild

# Langkah 7: Build BM25 index
python src/bm25_retriever.py --rebuild

# Langkah 8: Verifikasi database
python -c "
import chromadb
from src.config import CHROMA_DIR_A, CHROMA_DIR_B, CHROMA_COLLECTION_A, CHROMA_COLLECTION_B
ca = chromadb.PersistentClient(path=str(CHROMA_DIR_A)).get_collection(CHROMA_COLLECTION_A)
cb = chromadb.PersistentClient(path=str(CHROMA_DIR_B)).get_collection(CHROMA_COLLECTION_B)
print(f'Config A: {ca.count()} chunks')
print(f'Config B: {cb.count()} chunks')
"
```

### 16.4 Menjalankan Aplikasi

```bash
# Jalankan server FastAPI
python app.py
# atau: uvicorn app:app --host 0.0.0.0 --port 8501 --reload

# Buka browser: http://localhost:8501
```

### 16.5 Pipeline Evaluasi

```bash
# Setelah ground_truth.csv siap:
python evaluation.py --config a
python evaluation.py --config b
python evaluation.py --config c
python evaluation.py --stats        # Wilcoxon A vs B
python evaluation.py --visualize    # Bar chart → eval/results/perbandingan_visual.png (untuk lampiran skripsi)
```

### 16.6 Git Workflow Harian

```bash
# Setelah menyelesaikan satu task atau fitur:
git add <file-yang-berubah>
git commit -m "feat: deskripsi singkat apa yang ditambahkan/diubah"

# Contoh commit sequence yang baik:
git commit -m "chore: setup project foundation — environment, gitignore, src package"
git commit -m "feat: tambah src/config.py — pusat konfigurasi sistem"
git commit -m "feat: tambah src/logger_manager.py — logging terpusat tiga output"
git commit -m "feat: tambah src/ingestion.py — pipeline ChromaDB Config A & B"
git commit -m "feat: tambah src/bm25_retriever.py — BM25 chunk-based Config C"
git commit -m "feat: tambah src/retriever.py — unified retrieval interface A/B/C"
git commit -m "feat: tambah src/chain.py — RAG chain + inline citation + SSE streaming"
git commit -m "feat: tambah app.py — FastAPI backend dengan endpoint chat SSE"
git commit -m "feat: tambah static/ — SPA frontend dua tab"
git commit -m "feat: tambah evaluation.py — Ragas 0.4.x + Wilcoxon + chart"
```

---

## 17. DAFTAR KEPUTUSAN ARSITEKTUR (DECISION LOG)

| #     | Keputusan                                                                          | Pilihan Lain Ditolak              | Alasan                                                                                                        |
| ----- | ---------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| D-01  | Model: `gemini-3.5-flash`                                                          | gemini-2.0-flash                  | Rilis terbaru; fleksibel ganti via config dan UI model switcher                                               |
| D-02  | ChromaDB: Dua collection terpisah per config                                       | Satu collection, metadata filter  | Isolasi penuh data antar config; tidak saling timpa                                                           |
| D-03  | Retrieval: k=4, cosine distance threshold=0.3                                      | k=2, k=10 tanpa threshold         | Keseimbangan presisi-recall; threshold cegah halusinasi (Telah Dikalibrasi)                                    |
| D-04  | Memory: Manual history list                                                        | ConversationBufferWindowMemory    | Hindari deprecated LangChain API; lebih transparan untuk debugging                                            |
| D-05  | UI: FastAPI + Vanilla SPA                                                          | Streamlit, Chainlit, Gradio       | Kontrol DOM penuh, tidak re-run script saat widget berubah, SSE stabil                                        |
| D-06  | Ground truth: CSV UTF-8                                                            | Excel, JSON                       | Portabel, kompatibel Ragas, mudah diedit                                                                      |
| D-07  | BM25 chunk size = Config B (2000 char)                                             | Dokumen utuh tanpa chunking       | Fair comparison: variabel yang dibandingkan adalah teknik retrieval, bukan ukuran teks |
| ~~D-08~~ | ~~Summary chunk: dari retrieval_summary~~                                       | ~~Abaikan / di system prompt~~    | **DICABUT — D-B1:** Corpus < 100 hal; summary dibuat AI tanpa review; tidak ada bukti empiris manfaatnya; pipeline lebih sederhana tanpa ini |
| D-09  | Search: Pure vector tanpa pre-filter (Config A/B)                                  | Metadata pre-filter kategori      | False negative risk pada kueri singkat; embedding semantik sudah cukup representatif                          |
| D-09b | BM25 murni sebagai Config C (baseline terpisah)                                    | Tidak ada baseline                | Meningkatkan bobot ilmiah: klaim "RAG mengungguli keyword search" dapat dipertahankan                         |
| D-10  | Versioning library: >= (fleksibel)                                                 | Pin ketat ==                      | Kemudahan update; diimbangi `use context7` sebelum implementasi                                               |
| D-11  | Idempotency: Chunk hash (MD5)                                                      | Upsert ChromaDB                   | Transparan, mudah di-debug; tidak ada side effect                                                             |
| D-12  | Evaluasi agregasi: mean ± std                                                      | Mean saja                         | Std dev penting untuk menunjukkan konsistensi sistem                                                          |
| D-13  | Konversi manual PDF → Markdown                                                     | PyPDF2 otomatis                   | Kualitas teks lebih bersih; bagian valid metodologi                                                           |
| D-14  | Tidak ada reranking                                                                | Cohere Rerank, Jina               | Overkill untuk < 100 halaman                                                                                  |
| D-15  | `task_type` embedding berbeda (doc vs query)                                       | Satu task_type                    | Best practice Google Embedding API; kualitas lebih baik                                                       |
| D-16  | Generator ≠ Evaluator model                                                        | Model sama (self-evaluation)      | Eliminasi self-eval bias; generator=`gemini-3.5-flash`, evaluator=`gemini-2.5-flash`                          |
| D-17  | Wilcoxon Signed-Rank Test per-metrik (A vs B)                                      | t-test parametrik                 | Data skor Ragas tidak diasumsikan normal; Wilcoxon lebih tepat untuk sampel kecil                             |
| D-A1  | `chunk_strategy` & `chunk_notes` = metadata dokumentasi                            | Instruksi runtime                 | Pipeline selalu two-stage splitter; field ini untuk dokumentasi penelitian manusia                            |
| D-A2  | Hapus category pre-filter ChromaDB; hapus category badge UI                        | Category keyword matching filter  | False negative risk pada kueri singkat; embedding semantik sudah cukup representatif                          |
| D-A3  | BM25 chunk identik Config B (chunk_size=2000)                                      | Dokumen utuh                      | Fair comparison metodologi; variabel kontrol: teknik retrieval, bukan ukuran konteks                          |
| D-A4  | Hapus `SESSION_CHAT_HISTORY` sebagai konstanta terpisah                            | Key terpisah di session state     | History dikelola langsung dalam `messages` list; konstanta terpisah redundant                                 |
| D-A5  | Tiktoken offline untuk estimasi token                                              | API call token count              | Latensi 0 ms; Gemini API tidak return token count reliably di SSE stream                                      |
| D-A6  | `rank-bm25` digunakan langsung di `bm25_retriever.py`, bukan via wrapper LangChain | LangChain BM25Retriever           | Lebih ringan; tidak ada overhead wrapper; BM25 adalah satu-satunya tempat library ini dipakai                 |
| D-A7  | `retrieved_contexts` ke Ragas = semua chunk lolos threshold                        | Hanya `citation_sources`          | Menghindari bias `context_recall` ke atas secara artifisial; Section 6.6                                      |
| D-A8  | Retry policy `ingestion.py` terpisah dari `config.py`                              | Satu konstanta MAX_RETRIES global | Dua policy berbeda secara legitimate: batch vs interaktif; mencampur keduanya menyebabkan konflik             |
| D-A9  | `perbandingan_visual.png` untuk lampiran skripsi; UI render dari API               | UI baca PNG langsung              | UI tidak bergantung pada file statis; PNG tetap dihasilkan untuk dokumentasi laporan                          |
| D-A10 | `context_entity_recall` sebagai metrik opsional dengan `OPTIONAL_METRICS_COLS`     | Hardcode di METRICS_COLS          | Metrik ini butuh LLM call tambahan dan mahal; opsional agar tidak memaksa setiap run                          |
| D-A11 | Chart.js via CDN untuk visualisasi Tab Evaluasi                                    | D3.js, Plotly.js                  | Lightweight; tidak butuh bundler; cukup untuk grouped bar chart 3 config; zero install overhead               |
| D-A12 | Memory chat dikelola di frontend (stateless backend)                               | Server-side session               | Stateless backend lebih mudah di-debug; tidak ada state yang bisa corrupt di server; natural untuk SPA        |
| D-A13 | Celery/background worker ditolak untuk evaluasi                                    | Celery + Redis                    | Over-engineering untuk prototipe 1-user; evaluasi dijalankan maksimal 3x; Rich progress bar di terminal cukup |
| **D-B1** | **Hapus summary chunk dari pipeline ingestion**                                | Summary chunk tetap              | Corpus < 100 hal; summary AI tanpa review berisiko; YAGNI; pipeline lebih linear |
| **D-B2** | **REQUIRED_YAML_FIELDS = ["doc_id", "title", "category"] saja**               | Validasi 9 field                 | Hanya 3 field yang dikonsumsi runtime; field lain boleh ada sebagai dokumentasi |
| **D-B3** | **Hapus `priority` dan `chunk_type` dari ChromaDB metadata**                   | Simpan semua field               | `priority` tidak pernah dibaca kode; `chunk_type` redundan setelah D-B1 |
| **D-B4** | **Hapus endpoint `POST /api/log_transaction`**                                 | Endpoint terpisah                | Backend sudah punya semua data; endpoint terpisah = extra round-trip tanpa nilai tambah |
| **D-B5** | **Hapus `reinitialize_llm()`; gunakan `_get_llm(model_name)` stateless**       | Global LLM mutation              | Konsisten dengan stateless backend (Section 6.7); eliminasi potensi race condition |
| **D-B6** | **Ground truth `reference`: natural language dengan key facts**                 | Verbatim copy-paste dokumen      | Verbatim membuat context_recall trivial; natural language mengukur semantic recall |
| **D-B7** | **Kalibrasi empiris SIMILARITY_THRESHOLD sebelum evaluasi resmi**              | Pakai nilai tanpa validasi       | Selesai. Nilai 0.3 divalidasi sangat optimal dengan gap keputusan 0.117 |

---

## 18. STRATEGI MITIGASI BIAYA EVALUASI & PROVIDER ALTERNATIF

### 18.1 Konteks: Mengapa Evaluasi Ragas Mahal

Evaluasi Ragas dengan `max_workers=1` (sequential) untuk 4 metrik utama pada 30–50 sampel
dapat menghasilkan **300–500+ LLM API call** (setiap metrik membutuhkan multiple calls per sampel).
Dengan model Gemini, ini dapat:

- Mengonsumsi kuota harian dengan cepat (terutama tier gratis)
- Memerlukan waktu 1–3 jam per config
- Menghasilkan biaya yang signifikan jika melebihi free tier

**Strategi mitigasi yang tersedia:**

| Strategi                | Biaya    | Kecepatan           | Trade-off                                               |
| ----------------------- | -------- | ------------------- | ------------------------------------------------------- |
| Gemini (default)        | Berbayar | Sedang              | Kuota gratis terbatas; bisa kena 429                    |
| NVIDIA NIM (API gratis) | Gratis\* | Baik                | Kuota gratis terbatas; perlu daftar akun; model berbeda |
| Ollama (lokal)          | Gratis   | Bergantung hardware | Butuh RAM besar; kualitas tergantung model yang dipilih |

\*NVIDIA NIM memberikan kredit API gratis untuk pengembang saat pendaftaran.

### 18.2 Integrasi NVIDIA NIM

NVIDIA NIM menyediakan endpoint OpenAI-compatible, sehingga dapat diintegrasikan via library `openai`.

> **WAJIB sebelum implementasi:** Jalankan `use context7` untuk mendapatkan dokumentasi
> terkini tentang cara menggunakan NVIDIA NIM dengan LangChain atau Ragas. Konfigurasi
> endpoint dan nama model bisa berubah. Konfirmasi dokumentasi resmi di:
> `https://docs.nvidia.com/nim/`

```python
# Contoh integrasi NVIDIA NIM untuk evaluator Ragas (OpenAI-compatible endpoint)
# CATATAN: Verifikasi nama class dan import dengan `use context7` sebelum implementasi

from langchain_openai import ChatOpenAI  # Gunakan `use context7` untuk verifikasi import

def get_nim_evaluator_llm():
    """
    Inisialisasi LLM evaluator menggunakan NVIDIA NIM via OpenAI-compatible endpoint.

Model yang sudah diuji: llama-3.3-nemotron-super-49b-v1.5
    Endpoint: https://integrate.api.nvidia.com/v1

    PENTING: Konfirmasi nama model dan endpoint terbaru di:
    https://build.nvidia.com/explore/reasoning

    Returns:
        ChatOpenAI instance terkonfigurasi untuk NIM endpoint.
    """
    import os
    nvidia_api_key = os.getenv("NVIDIA_NIM_API_KEY")
    if not nvidia_api_key:
        raise ValueError("NVIDIA_NIM_API_KEY tidak ditemukan di .env")

    return ChatOpenAI(
        model=model_name,  # Verifikasi nama model terbaru
        api_key=nvidia_api_key,
        openai_api_base="https://integrate.api.nvidia.com/v1",
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_OUTPUT_TOKENS,
    )

# Model yang sudah diuji untuk evaluator Ragas:
# - nvidia/llama-3.3-nemotron-super-49b-v1.5 (direkomendasikan untuk evaluasi presisi tinggi)
# - nvidia/llama-3.1-nemotron-nano-8b-v1 (sangat direkomendasikan untuk uji coba cepat)
# Model yang sudah diuji untuk generator LLM:
# - nvidia/qwen3.5-397b-a17b (akurasi tinggi, namun antrean NIM lambat)
# - nvidia/llama-3.1-nemotron-nano-8b-v1 (sangat cepat, 1-2 detik per kueri)
# Model embedding yang sudah diuji untuk evaluator Ragas:
# - nvidia/nv-embedqa-e5-v5 (bebas dari issue rate-limit Gemini)
# KONFIRMASI nama model yang aktif di: https://build.nvidia.com/
```

### 18.3 Integrasi Ollama (Model Lokal)

Ollama memungkinkan menjalankan model LLM secara lokal tanpa biaya API.

> **WAJIB sebelum implementasi:** Jalankan `use context7` untuk mendapatkan dokumentasi
> terkini tentang `langchain-ollama` dan cara mengintegrasikannya dengan Ragas.
> Konfirmasi model yang tersedia dan ukuran RAM yang dibutuhkan di: `https://ollama.com/library`
>
> **Perhatikan spesifikasi hardware:** GPU RTX 3050 Laptop (4–8 GB VRAM) membatasi
> model yang dapat berjalan dengan baik. Rekomendasikan model ≤7B parameter untuk
> performa yang acceptable. Model 13B+ kemungkinan akan sangat lambat atau gagal.

```python
# Contoh integrasi Ollama untuk evaluator Ragas
# CATATAN: Verifikasi nama class dan import dengan `use context7` sebelum implementasi

from langchain_ollama import ChatOllama  # Gunakan `use context7` untuk verifikasi import

def get_ollama_evaluator_llm(model_name: str = "llama3.1:8b"):
    """
    Inisialisasi LLM evaluator menggunakan Ollama (model lokal, gratis).

    Prasyarat:
    1. Install Ollama: https://ollama.com/download
    2. Pull model: ollama pull llama3.1:8b
    3. Pastikan Ollama berjalan: ollama serve

    Model yang direkomendasikan untuk RTX 3050 Laptop (≤8GB VRAM):
    - llama3.1:8b  (~5 GB)
    - mistral:7b   (~4 GB)
    - gemma2:9b    (~6 GB)

    PENTING: Ganti model evaluator akan membuat hasil evaluasi TIDAK DAPAT
    dibandingkan dengan sesi evaluasi menggunakan Gemini. Dokumentasikan
    model yang digunakan di setiap sesi evaluasi.

    Args:
        model_name: Nama model Ollama yang sudah di-pull.

    Returns:
        ChatOllama instance terkonfigurasi.
    """
    return ChatOllama(
        model=model_name,
        temperature=0.1,
    )
```

### 18.4 Integrasi Embedding NVIDIA NIM (Opsional — Dampak Besar)

> **⚠️ PERINGATAN DAMPAK BESAR:** Mengganti model embedding jauh lebih berdampak
> daripada mengganti LLM generator atau evaluator. Jika embedding model diganti,
> **seluruh ChromaDB harus dihapus dan di-rebuild dari nol** karena dimensi dan
> ruang vektor berbeda antar model embedding yang berbeda.

Model embedding NVIDIA NIM yang tersedia dan telah diidentifikasi:

| Model NIM                           | Dimensi | Catatan                                                    |
| ----------------------------------- | ------- | ---------------------------------------------------------- |
| `nvidia/llama-nemotron-embed-1b-v2` | 4096    | https://build.nvidia.com/nvidia/llama-nemotron-embed-1b-v2 |
| `nvidia/nv-embedqa-e5-v5`           | 1024    | https://build.nvidia.com/nvidia/nv-embedqa-e5-v5           |

> **WAJIB sebelum implementasi:** Konfirmasi dimensi vektor, task_type yang didukung
> (retrieval_document vs retrieval_query), dan format API terbaru di halaman masing-masing
> model di build.nvidia.com. Jalankan `use context7` untuk verifikasi integrasi LangChain.

**Aturan jika ingin menggunakan NIM embedding:**

1. Catat model embedding yang digunakan di jurnal penelitian bersamaan dengan provider LLM
2. Jalankan `ingestion.py --rebuild` untuk kedua config setelah mengganti embedding model
3. Verifikasi dimensi vektor konsisten antara ingestion dan query di `chromadb` collection
4. Untuk komparabilitas penelitian: **jangan ganti embedding model di tengah siklus evaluasi**

### 18.5 Peringatan Komparabilitas Hasil Evaluasi

> **⚠️ KRITIS UNTUK METODOLOGI PENELITIAN**

Jika provider atau model evaluator diganti antar sesi evaluasi, hasil skor Ragas
**tidak dapat dibandingkan secara langsung**. Ini karena:

- Setiap LLM memiliki calibrasi dan standar penilaian yang berbeda
- `faithfulness` yang dinilai `gemini-2.5-flash` ≠ `faithfulness` yang dinilai `llama-3.3-nemotron-super-49b-v1.5`

**Aturan evaluasi:**

1. Pilih satu model evaluator sebelum memulai evaluasi seluruh config
2. Gunakan model evaluator yang **sama** untuk Config A, B, dan C dalam satu sesi penelitian
3. Catat provider, nama model, dan versi di jurnal penelitian dan di Bab IV laporan
4. Jika terpaksa ganti model evaluator, tandai hasilnya sebagai sesi evaluasi terpisah dan jangan gabungkan dalam tabel perbandingan yang sama

### 18.6 Panduan Memilih Provider untuk Evaluasi

```
Skenario 1: Evaluasi resmi (untuk skripsi)
→ Gunakan Gemini (gemini-2.5-flash) sebagai evaluator
→ Hasil paling konsisten dan mudah didokumentasikan

Skenario 2: Eksperimen / debugging metrik sebelum evaluasi resmi
→ Gunakan Ollama (lokal, gratis, tidak ada rate limit)
→ Cepat untuk iterasi; hasil tidak dimasukkan ke laporan utama

Skenario 3: Evaluasi resmi tapi quota Gemini hampir habis
→ Gunakan NVIDIA NIM (llama-3.3-nemotron-super-49b-v1.5)
→ Catat pergantian provider ini secara eksplisit di laporan
→ Diskusikan implikasi metodologisnya di Bab 5 (keterbatasan)
```

---

# BAGIAN B — SRS (SOFTWARE REQUIREMENTS SPECIFICATION)

---

## 19. FUNCTIONAL REQUIREMENTS (FR)

### FR-01: Parsing Corpus

Sistem HARUS dapat membaca semua file `.md` di `data/corpus/`, mem-parsing YAML frontmatter
menggunakan library `python-frontmatter`, dan mengekstrak metadata serta konten secara terpisah.

### FR-02: Validasi Frontmatter

Sistem HARUS memvalidasi bahwa setiap file memiliki field wajib sesuai `REQUIRED_YAML_FIELDS`.
File yang gagal validasi harus di-log (WARNING) dan di-skip tanpa menghentikan proses.

### FR-03: Two-Stage Chunking

Sistem HARUS memotong dokumen dalam dua tahap: (1) MarkdownHeaderTextSplitter berdasarkan
heading, (2) RecursiveCharacterTextSplitter untuk normalisasi ukuran. Parameter dari `config.py`.

### FR-04: ~~Summary Chunk Generation~~ — **DIHAPUS (D-B1)**

> Requirement ini telah dihapus. Summary chunk tidak diimplementasikan.
> Lihat D-B1 di Section 17 dan catatan di Section 6.2.

### FR-05: Chunk Filtering

Sistem HARUS membuang chunk yang panjangnya (setelah `.strip()`) kurang dari `MIN_CHUNK_LENGTH`.

### FR-06: Idempotent Ingestion

Sistem HARUS menghasilkan `chunk_id` unik per chunk berdasarkan MD5 hash dari
`f"{doc_id}::{chunk_content}"`. Chunk duplikat di-skip dan di-log (INFO).

### FR-07: Embedding dengan Task Type

Sistem HARUS menggunakan `task_type="retrieval_document"` saat ingestion dan
`task_type="retrieval_query"` saat query pengguna.

### FR-08: Dual Collection ChromaDB

Sistem HARUS menyimpan Config A dan Config B di collection ChromaDB yang berbeda.

### FR-09: Global Similarity Search (Tanpa Pre-Filter)

Sistem HARUS melakukan similarity search secara global di seluruh collection tanpa
metadata pre-filter kategori. Ini adalah keputusan arsitektur definitif (D-A2).

### FR-10: Similarity Threshold Filtering

Sistem HARUS membuang chunk dengan cosine distance > `SIMILARITY_THRESHOLD` sebelum
chunk dikirim ke LLM.

### FR-11: Fallback Response

Sistem HARUS mengembalikan `FALLBACK_RESPONSE` TANPA memanggil LLM jika tidak ada
satu pun chunk yang lolos threshold.

### FR-12: Dual-Mode Response

`get_response()` HARUS mendukung `streaming=True` (Generator untuk SSE) dan
`streaming=False` (dict untuk `evaluation.py`).

### FR-13: Manual Memory Management

Sistem HARUS mengelola chat history sebagai Python list biasa, di-trim ke `MEMORY_K * 2`
pesan sebelum dikirim ke LLM.

### FR-14: Evaluation Memory Reset

`evaluation.py` HARUS mereset `chat_history = []` sebelum setiap pertanyaan evaluasi.

### FR-15: Ragas Evaluation

Sistem HARUS menjalankan evaluasi menggunakan metrik dari `METRICS_COLS` (wajib) dan
mendukung metrik dari `OPTIONAL_METRICS_COLS` via flag `--extra-metrics`.

> Verifikasi API dengan `use context7` sebelum implementasi.

### FR-16: Evaluation Aggregation

Sistem HARUS menghitung dan menampilkan mean, std, min, max untuk setiap metrik + latensi.

### FR-17: Comparison Visualization

Sistem HARUS menghasilkan `eval/results/perbandingan_visual.png` (grouped bar chart 3 config +
latency line + p-value annotation) via flag `--visualize`. File ini untuk lampiran skripsi,
bukan dikonsumsi UI runtime.

### FR-18: API Retry

Semua panggilan ke Gemini API HARUS mengimplementasikan retry policy sesuai `MAX_RETRIES`
dan `RETRY_DELAYS` (untuk `chain.py`) atau `MAX_RETRIES_INGESTION` dengan exponential backoff
(untuk `ingestion.py`).

### FR-19: BM25 Indexing (Config C)

`src/bm25_retriever.py` HARUS membangun indeks BM25 dari chunk-chunk (chunk_size=2000,
identik Config B) menggunakan `rank-bm25` secara langsung (bukan via LangChain wrapper — D-A6)
dan menyimpannya sebagai `bm25_index.pkl`. Mendukung flag `--rebuild`.

### FR-20: BM25 Retrieval

`retrieve_chunks_bm25(query)` HARUS mengembalikan `BM25_K` chunk teratas dalam format
kompatibel dengan `get_response()`.

### FR-21: Latensi Per-Query

`evaluation.py` HARUS mengukur `response_time_seconds` per query via `time.time()`.

### FR-22: Uji Wilcoxon

`evaluation.py` HARUS menjalankan `scipy.stats.wilcoxon` antara skor per-query
Config A vs B, menyimpan ke `statistical_test.csv`.

### FR-23: Error Analysis Export

`evaluation.py` HARUS mengekspor `ERROR_ANALYSIS_N` sampel skor terendah ke
`error_analysis_config_[a|b].csv` dengan kolom rank, scores, failure_type (manual), notes.

### FR-24: Model Switcher UI & Backend

Frontend HARUS menyediakan selectbox model dari `AVAILABLE_MODELS`. Pilihan dikirim ke
backend via request body `/api/chat`, diteruskan ke `reinitialize_llm(model_name)` di `chain.py`.

### FR-25: Config C Evaluation Support

`evaluation.py` HARUS mendukung `--config c` yang menggunakan BM25 untuk retrieval
dan LLM yang sama untuk generation.

### FR-26: Inline Citation Generation dengan Robust Parsing

`chain.py` HARUS memformat konteks dengan penanda `[Sumber N: ...]`, menginstruksikan
LLM via `SYSTEM_PROMPT` untuk menyisipkan `[N]` di dalam teks jawaban, dan mem-parsing
response menggunakan `re.findall(r'\[(\d+)\]', answer_text)` untuk mengekstrak `citation_sources`
berisi HANYA chunk yang dikutip. Parser HARUS toleran terhadap ketidakpatuhan LLM:
marker di luar range valid diabaikan dengan log WARNING; parsing gagal total mengembalikan
`citation_sources = []` tanpa crash. Lihat Section 6.5 untuk spesifikasi lengkap.

### FR-27: SSE Streaming dengan Empat Tipe Event

`app.py` HARUS mengirim SSE dengan empat tipe event:

- `thinking` — sebelum proses dimulai (feedback visual ke user)
- `token` — per token jawaban
- `citations` — setelah streaming selesai, berisi citation_sources
- `done` — penanda akhir stream
- `error` — jika terjadi error yang tidak bisa di-recover, berisi pesan Bahasa Indonesia

### FR-28: Centralized Logging

Semua aktivitas sistem HARUS di-log via `src/logger_manager.py` ke tiga output:
`unsrat_rag.log` (sistem), `ingestion_report.csv`, dan `transaksi_chat.csv`.
Output LLM dan prompt (truncated) HARUS di-log di level DEBUG.

### FR-29: Token Estimation

Sistem HARUS mengestimasi jumlah token prompt dan completion menggunakan `tiktoken`
(`cl100k_base`) secara offline dan mencatatnya di `transaksi_chat.csv`.

### FR-30: Git Initialization

Setiap proyek HARUS dimulai dengan `git init` sebagai langkah pertama. Setiap perubahan
signifikan HARUS di-commit dengan pesan yang jelas mengikuti format di Section 14.3.

### FR-31: Retrieved Contexts untuk Ragas

`evaluation.py` HARUS mengirim **semua chunk yang lolos similarity threshold** (bukan hanya
`citation_sources`) sebagai `retrieved_contexts` ke `ragas.evaluate()`. Lihat Section 6.6
dan D-A7.

### FR-32: Error Ditampilkan ke User via SSE

Semua error yang terjadi saat user menunggu respons (`chain.py`) HARUS dikomunikasikan via
SSE event `error` dengan pesan dalam Bahasa Indonesia. Frontend HARUS menampilkan error
bubble yang secara visual berbeda dari bubble "tidak ada jawaban".

### FR-33: Thinking & Typing Indicator UI

Frontend HARUS menampilkan thinking indicator saat SSE event `thinking` diterima dan
menyembunyikannya saat token pertama dari event `token` diterima. Lihat Section 11.5.

### FR-34: Opsional Metrics Support

`evaluation.py` HARUS membaca `OPTIONAL_METRICS_COLS` dari `config.py` dan mengaktifkan
metrik tersebut jika flag `--extra-metrics <nama_metrik>` diberikan. Kode HARUS disiapkan
untuk mengakomodasi `context_entity_recall` dan metrik opsional lain di masa depan.

---

## 20. NON-FUNCTIONAL REQUIREMENTS (NFR)

### NFR-01: Modularitas

Semua logika bisnis HARUS ada di `src/`. `app.py` hanya boleh berisi route handler.
Frontend hanya boleh berisi UI dan fetch call.

### NFR-02: Single Responsibility

Setiap file Python HARUS memiliki satu tanggung jawab utama (Section 4.1).

### NFR-03: No Magic Numbers

Semua angka konfigurasi HARUS berasal dari `src/config.py`.

### NFR-04: Secret Management

API Key HARUS dimuat dari `.env` via `python-dotenv`. Dilarang hardcode.

### NFR-05: Docstring

Setiap fungsi Python HARUS memiliki docstring minimal satu baris.

### NFR-06: Bahasa Pesan Error ke User

Semua pesan error yang ditampilkan ke pengguna (via SSE event `error` atau UI) HARUS
dalam Bahasa Indonesia yang jelas dan tidak mengandung stack trace teknis.

### NFR-07: Reproducibility

Evaluasi HARUS menghasilkan hasil konsisten untuk input sama. Dijamin oleh
`LLM_TEMPERATURE = 0.1` dan memory reset antar pertanyaan evaluasi.
Provider dan model evaluator HARUS didokumentasikan di setiap sesi evaluasi.

### NFR-08: Logging Coverage

`ingestion.py` HARUS mencetak progress ke terminal DAN menyimpan ke `ingestion_report.csv`.
`chain.py` HARUS menyimpan setiap transaksi ke `transaksi_chat.csv` termasuk output LLM.

### NFR-09: Graceful Degradation

Sistem HARUS tetap berjalan saat menghadapi error API yang bisa di-retry.
Crash hanya boleh terjadi untuk kondisi unrecoverable (API key tidak ada, database tidak ada).
Citation parsing gagal HARUS graceful: kembalikan `citation_sources=[]`, jangan crash.

### NFR-10: Konsistensi Citation

Nomor referensi `[N]` dalam teks jawaban HARUS konsisten dengan nomor `index` di array
`citation_sources`. Tidak boleh ada referensi dalam teks yang tidak punya source, atau
source yang tidak direferensikan dalam teks. Dijamin oleh parser `parse_cited_indices()`
di Section 6.5.

---

## 21. CONSTRAINTS & ASSUMPTIONS

### 21.1 Technical Constraints

- Model embedding **default** via Google AI Studio (`gemini-embedding-001`). Alternatif via NVIDIA NIM
  tersedia (lihat Section 18.4) tapi **mengharuskan rebuild ChromaDB penuh** dan harus dikonfirmasi
  kompatibilitas dimensi vektornya. Mengganti embedding model di tengah siklus penelitian dilarang.
- Corpus terbatas pada dokumen statis dalam format Markdown
- Tidak ada persistensi sesi percakapan antar restart server
- ChromaDB berjalan sebagai embedded database (bukan server terpisah)
- Sistem hanya berjalan di localhost (tidak ada deployment publik)
- Model LLM generator dan evaluator dapat menggunakan provider alternatif (Ollama/NIM) sesuai Section 18, tapi dengan konsekuensi komparabilitas yang harus didokumentasikan

### 21.2 Research Constraints

- Generator dan evaluator menggunakan model berbeda (D-16) — self-eval bias telah
  dimitigasi teknis; akui keterbatasan LLM-as-a-judge di Bab 5
- Ground truth dibuat manual oleh peneliti (bukan crowdsourced)
- Jumlah sampel evaluasi (30–50) terbatas — Wilcoxon valid untuk sampel kecil
  tapi power statistik terbatas; akui di Bab 5
- Config C (BM25) stateless per-query, konsisten dengan evaluasi Config A & B
- Jika provider evaluator diganti antar sesi, hasil tidak dapat dibandingkan langsung

### 21.3 Assumptions

- Semua file corpus tersedia dalam format Markdown yang bersih sebelum ingestion
- Koneksi internet tersedia saat sistem berjalan (akses ke Gemini API)
- Pengguna memiliki pemahaman dasar penggunaan browser
- Untuk opsi Ollama: Ollama terinstall dan berjalan di localhost:11434

---

## 22. RENCANA ANALISIS HASIL (TEMPLATE BAB IV)

### 22.1 Struktur Bab IV yang Direkomendasikan

```
Bab IV — Hasil dan Pembahasan
4.1 Hasil Evaluasi Kuantitatif
    4.1.1 Perbandingan Metrik Ragas (A vs B vs C)
    4.1.2 Perbandingan Latensi Sistem
    4.1.3 Uji Signifikansi Statistik (Wilcoxon A vs B)
4.2 Analisis Kegagalan Kualitatif
    4.2.1 Kasus Kegagalan Config A (10 sampel terburuk)
    4.2.2 Kasus Kegagalan Config B (10 sampel terburuk)
    4.2.3 Klasifikasi Penyebab Kegagalan
4.3 Diskusi Trade-off
    4.3.1 Chunk Size vs Token Consumption vs Latensi
    4.3.2 Chunk Size vs Kualitas Konteks
    4.3.3 RAG vs BM25 Baseline
4.4 Rekomendasi Konfigurasi
```

### 22.2 Template Tabel Komparasi Utama (Tabel 4.1)

| Metrik                    | Config A (500) | Config B (2000) | Config C (BM25) | Winner | p-value (A vs B) |
| ------------------------- | -------------- | --------------- | --------------- | ------ | ---------------- |
| Faithfulness              | X.XXX ± X.XXX  | X.XXX ± X.XXX   | X.XXX ± X.XXX   | ?      | p = X.XXX        |
| Answer Relevancy          | —              | —               | —               | ?      | p = X.XXX        |
| Context Precision         | —              | —               | —               | ?      | p = X.XXX        |
| Context Recall            | —              | —               | —               | ?      | p = X.XXX        |
| **Response Time (detik)** | X.XX ± X.XX    | X.XX ± X.XX     | X.XX ± X.XX     | ?      | —                |

> **CATATAN TABEL:** Pastikan semua metrik di tabel dihasilkan dari evaluator model yang **sama**
> untuk ketiga config. Jika ada perbedaan provider/model evaluator, buat tabel terpisah atau
> tambahkan footnote yang jelas.

### 22.3 Protokol Analisis Kegagalan Kualitatif

1. Buka `error_analysis_config_a.csv` dan `error_analysis_config_b.csv`
2. Untuk setiap sampel (rank 1–10), isi kolom `failure_type` secara manual:

| Kode                 | Definisi                                                              |
| -------------------- | --------------------------------------------------------------------- |
| `retrieval_failure`  | Chunk salah diambil; informasi ada di dokumen tapi tidak ter-retrieve |
| `generation_failure` | Chunk tepat diambil, tapi LLM salah interpretasi atau merangkum       |
| `chunking_failure`   | Informasi terpotong di antara dua chunk; tidak ada chunk yang lengkap |

3. Tulis narasi Bab IV 4.2 berdasarkan distribusi `failure_type`

### 22.4 Diskusi Trade-off yang Wajib Dibahas

**Chunk Size vs Token Consumption:** Config B (2000 char) mengonsumsi ~4× token input
lebih banyak dari Config A. Hitung biaya estimasi berdasarkan `estimated_prompt_tokens` di
`transaksi_chat.csv`.

**RAG vs BM25:** Jika selisih Config B vs Config C kecil, ini adalah temuan menarik
yang harus didiskusikan — seberapa jauh embedding vector search mengungguli keyword
matching sederhana?

### 22.5 Kriteria Rekomendasi Konfigurasi

Rekomendasikan Config X jika memenuhi ≥ 3 dari 4 kriteria:

| Kriteria                 | Threshold                       |
| ------------------------ | ------------------------------- |
| Faithfulness tertinggi   | Selisih ≥ 0.05 dari config lain |
| Context Recall tertinggi | Selisih ≥ 0.05 dari config lain |
| Latensi dapat diterima   | mean response_time < 10 detik   |
| Unggul vs BM25 baseline  | Semua metrik utama > Config C   |

---

## CHECKLIST SEBELUM MULAI CODING

- [ ] `git init` sudah dijalankan di root proyek
- [ ] File `.env` sudah dibuat dengan `GOOGLE_API_KEY` yang valid
- [ ] Conda environment `unsrat-rag` berhasil dibuat dan diaktifkan
- [ ] Semua file corpus `.md` ada di `data/corpus/` dengan YAML frontmatter yang benar
- [ ] GCP Budget Alert sudah diaktifkan ($50 dan $250)
- [ ] File `.gitignore` sudah berisi `.env`, `chroma_db/`, `bm25_index/`, `logs/`
- [ ] Dokumen ini dibaca dan dipahami sebelum mulai menulis kode
- [ ] `use context7` dijalankan untuk verifikasi API Ragas sebelum menulis `evaluation.py`
- [ ] `use context7` dijalankan untuk verifikasi API LangChain sebelum menulis `chain.py`
- [ ] `LLM_MODEL_NAME` ≠ `EVALUATOR_MODEL_NAME` di `config.py`
- [ ] Tidak ada hardcode model name di luar `config.py`
- [ ] Setiap commit menggunakan format pesan yang jelas (Section 14.3)
- [ ] Citation parser menggunakan `re.findall(r'\[(\d+)\]', ...)` dengan range validation (Section 6.5)
- [ ] `retrieved_contexts` ke Ragas = semua chunk lolos threshold, BUKAN hanya `citation_sources` (Section 6.6)
- [ ] `ingestion.py` menggunakan `MAX_RETRIES_INGESTION = 5` lokal, BUKAN `MAX_RETRIES` dari config (Section 15.2)
- [ ] `OPTIONAL_METRICS_COLS` didefinisikan di `config.py` untuk `context_entity_recall` (Section 7)
- [ ] Provider dan model evaluator yang digunakan untuk evaluasi resmi sudah dicatat di jurnal penelitian
- [ ] Validasi `SIMILARITY_THRESHOLD` dengan beberapa query manual sebelum evaluasi resmi (Section 12.2b)
- [ ] Provider + model evaluator sudah ditentukan dan dicatat SEBELUM menjalankan evaluasi Config A (Section 12.2b)
- [ ] `get_nim_evaluator_llm()` dipanggil dengan parameter `model_name` eksplisit (Section 18.2)
- [ ] Jika menggunakan NIM embedding, ChromaDB sudah di-rebuild setelah ganti model (Section 18.4)
- [ ] `Chart.js` sudah dimuat via CDN di `static/index.html` untuk Tab Evaluasi (Section 3.3)

---

## 23. SPESIFIKASI PENGUJIAN & VERIFIKASI (TESTING)

Sistem menggunakan framework `pytest` untuk melakukan pengujian unit dan integrasi secara modular. Pengujian dibagi menjadi mode **offline** (cepat, tanpa API call eksternal) dan mode **online** (memerlukan koneksi API riil).

### 23.1 Konfigurasi Penanda (pytest.ini)

Pembedaan pengujian diatur melalui penanda kustom di `pytest.ini`:
- `pytest -m offline`: Menjalankan suite pengujian offline menggunakan tiruan (mocking) untuk database ChromaDB, Gemini, dan NIM.
- `pytest -m online`: Menjalankan suite pengujian yang berinteraksi langsung dengan API eksternal (Google GenAI, NVIDIA NIM).

### 23.2 Mocking Global (tests/conftest.py)

Untuk mendukung pengujian offline yang cepat dan andal, `conftest.py` mendefinisikan fixture mock global yang di-patch secara otomatis ke seluruh berkas pengujian:
1. `mock_chroma`: Mem-patch `chromadb.PersistentClient` agar tidak membuat berkas database fisik.
2. `mock_embeddings`: Menyediakan mock untuk class embeddings dan mengembalikan vektor berdimensi statis.
3. `mock_google_llm` & `mock_nim_llm`: Menyimulasikan respons model Gemini dan NIM dengan teks akademik tiruan.

### 23.3 Skenario Pengujian Unit (tests/unit/)

Pengujian unit memverifikasi kebenaran logika logika modular program:
- `test_logger_manager.py`: Menguji rotasi log `RotatingFileHandler` dan format output CSV.
- `test_ingestion.py`: Memvalidasi parsing frontmatter Markdown, pembagian chunk, pembuatan hash ID, dan retry embedding.
- `test_bm25_retriever.py`: Memvalidasi logika tokenisasi dan pemfilteran kata dasar leksikal.
- `test_retriever.py`: Menguji fungsionalitas retrieval hibrida dan ambang batas filter similarity.
- `test_chain.py` & `test_citation_parser.py`: Menguji parsing tanda kurung sitasi `[N]` dan pembuatan struktur respons RAG.

### 23.4 Skenario Pengujian Integrasi (tests/integration/)

Pengujian integrasi memvalidasi interaksi antarmuka HTTP backend:
- `test_chat_api.py`: Menguji endpoint chat `/api/chat` dalam memancarkan event streaming SSE (thinking, token, citations, done) dan memvalidasi keandalan middleware eksepsi global.
- `test_spa_serving.py`: Memastikan API root FastAPI menyajikan file `index.html` dan statis assets JavaScript dengan tipe konten (`mime-type`) yang tepat.

---

_Dokumen terakhir direvisi: 4 Juni 2026 | Versi: 10.0_
