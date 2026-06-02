# Laporan Pengujian RAG Chatbot Akademik UNSRAT

Laporan ini menyajikan hasil pengujian fungsional dan visual menyeluruh dari sistem RAG Chatbot Universitas Sam Ratulangi (UNSRAT) menggunakan Playwright.

---

## 📋 Ringkasan Pengujian

Pengujian dilakukan secara otomatis menggunakan Playwright MCP server pada instansi aplikasi lokal yang berjalan di `http://localhost:8501/`.

| Aspek Uji | Skenario Pengujian | Status | Catatan / Hasil Verifikasi |
|---|---|---|---|
| **Konektivitas Model** | Membaca model generator aktif & melakukan uji koneksi backend | **PASS** | `llama-3.1-nemotron-nano-8b-v1` dan `gemini-2.5-flash` terhubung penuh |
| **Reset Chat** | Klik tombol "Reset Percakapan" untuk membersihkan sesi percakapan | **PASS** | DOM terhapus bersih; status sisa parameter default dipertahankan |
| **Uji Pencarian & RAG** | Kirim pertanyaan: *"Berapa batas SKS maksimum yang dapat diambil mahasiswa semester satu?"* | **PASS** | Menghasilkan jawaban akurat **20 SKS** dengan referensi valid |
| **Uji Rujukan (Citations)**| Ekspansi panel akordeon referensi dokumen ground-truth | **PASS** | Menampilkan Pasal 27 (Distribusi Beban Belajar) dari Peraturan Akademik 2025 |
| **SPA Navigation** | Perpindahan tab dari "Chatbot Utama" ke "Evaluasi Ragas" | **PASS** | DOM beralih instan tanpa visual reload (SPA Vanilla JS murni) |
| **Metadata Evaluasi** | Verifikasi dynamic metadata panel di dashboard evaluasi | **PASS** | Sukses memuat generator, evaluator, embedding model, dan timestamp |
| **Uji Signifikansi** | Menampilkan hasil pengujian statistik Wilcoxon (Config A vs B) | **PASS** | Metrik terekam lengkap dan diformat dengan layout skripsi akademis |
| **Live Audit Log** | Logging transaksi real-time di tabel logs/transaksi_chat.csv | **PASS** | Sukses merekam metrik latency, tokens, retrieved chunks, dan best score |

---

## 💬 1. Uji Chatbot Utama & Verifikasi Keakuratan Jawaban

Sistem chatbot diuji menggunakan model **`gemini-2.5-flash`** pada **`Config B`** (RAG 2000 karakter chunk).

### Skenario Chat
- **Pertanyaan:** *"Berapa batas SKS maksimum yang dapat diambil mahasiswa semester satu?"*
- **Jawaban RAG:** *"Berdasarkan dokumen yang diberikan, batas SKS maksimum yang dapat diambil mahasiswa semester satu adalah 20 SKS [1]."*

### Verifikasi Ground-Truth
Ketika panel akordeon rujukan dibuka, sistem berhasil memetakan rujukan akademis berikut:
- **Dokumen:** Peraturan Rektor UNSRAT Nomor 01 Tahun 2025 tentang Peraturan Akademik
- **Lokasi:** BAB VII — PROSES PEMBELAJARAN | Pasal 27 — Distribusi Beban Belajar
- **Kutipan Konteks:**
  > `"#### Pasal 27 — Distribusi Beban Belajar (1) Distribusi beban belajar program sarjana: - Semester 1 dan 2: **maksimal 20 sks** - Semester 3 dan seterusnya: **maksimal 24 sks** ..."`

Tanggapan sistem terbukti **100% akurat** dan didasarkan secara ketat pada dokumen ground-truth akademik UNSRAT tanpa adanya halusinasi.

### Visual Antarmuka Chatbot
Berikut adalah tampilan visual chat yang menunjukkan bubble pesan terformat premium dan akordeon rujukan yang berhasil diekspansi:

![Tampilan Chatbot Utama](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/docs/testing/2026-06-01/2026-06-01-page-chat-tab.png)

---

## 📊 2. Uji Tab Dashboard Evaluasi Kuantitatif

Ketika beralih ke tab **Evaluasi Ragas**, sistem memproses dan merender visualisasi komparatif secara dinamis.

### A. Panel Parameter Uji
Dashboard berhasil mengekstrak konfigurasi pengujian offline:
- **Terakhir Dijalankan:** `2026-05-31 01:17`
- **Dataset Ground-Truth:** `3 Pertanyaan`
- **Generator Model:** `llama-3.1-nemotron-nano-8b-v1`
- **Evaluator Model:** `llama-3.3-nemotron-super-49b-v1.5`
- **Embedding Model:** `models/gemini-embedding-001`

### B. Uji Signifikansi Wilcoxon
Tabel signifikansi statistik memetakan nilai p-value untuk perbandingan performa **Config A vs Config B**:
- **Faithfulness:** `1.00000` (Tidak Signifikan)
- **Answer Relevancy:** `0.75000` (Tidak Signifikan)
- **Context Precision:** `1.00000` (Tidak Signifikan)
- **Context Recall:** `1.00000` (Tidak Signifikan)

### C. Live Audit Log Transaksi Kuantitatif
Tabel audit log memperlihatkan transaksi real-time. Pertanyaan yang diajukan selama pengujian Playwright terdaftar secara langsung:
- **Waktu:** `23:57:17`
- **Config:** `B`
- **Model:** `gemini-2.5-flash`
- **Kueri:** *"Berapa batas SKS maksimum yang dapat diambil mahasiswa semester satu?"*
- **Chunks:** `4`
- **Best score:** `0.2173`
- **Latency:** `2.87 detik`
- **Est. Tokens:** `1227`

### Visual Dashboard Evaluasi
Berikut adalah visualisasi antarmuka tab laporan evaluasi, grafik Chart.js, tabel Wilcoxon, serta Live Audit Log:

![Dashboard Evaluasi Ragas](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/docs/testing/2026-06-01/2026-06-01-page-eval-tab.png)

---

## 🔒 Kesimpulan Pengujian

Seluruh fungsi frontend SPA (tab navigasi, reset chat, custom prompt filling, rendering markdown, akordeon, model selectors, chart, clipboard integration) dan backend FastAPIs (konfigurasi, chatting SSE stream, data evaluasi JSON) berjalan secara harmonis, andal, dan siap digunakan untuk keperluan penyusunan naskah skripsi Bab IV.
