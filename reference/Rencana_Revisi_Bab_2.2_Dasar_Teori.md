# Rencana Revisi Bab 2.2 (Dasar Teori) — Skripsi RAG Chatbot UNSRAT

**Dokumen hand-off** untuk melanjutkan revisi Sub-bab 2.2.1–2.2.10 di sesi/AI lain. Revisi 2.1 (Kajian Pustaka) **sudah selesai** di sesi sebelumnya — dokumen ini murni untuk 2.2 (Dasar Teori).

---

## 1. Konteks Penelitian (ringkas — detail penuh ada di file revisi 2.1)

- **Judul:** Implementasi dan Evaluasi Kinerja Chatbot Layanan Informasi Akademik UNSRAT Menggunakan RAG dan Google Gemini
- **Inti:** Config B (dense, ChromaDB + `gemini-embedding-001`) vs Config C (sparse, BM25) pada korpus 9 dokumen UNSRAT (188 chunk), dievaluasi via Ragas (Faithfulness, Answer Relevancy, Context Precision, Context Recall), 80 pasang ground truth.
- **Generator:** `gemini-3.5-flash` (perlu verifikasi manual — lihat Bagian 6 poin 3).
- **Gaya penulisan:** wajib `stop-slop-id-akademik-v2`.
- **Prinsip kerja:** zero-hallucination — semua sitasi dan klaim numerik harus bisa dipertanggungjawabkan penulis saat sidang.

---

## 2. Aturan Sitasi Tambahan (khusus revisi 2.2)

> "Prioritaskan 5 tahun terakhir dan jurnal internasional bereputasi atau jurnal nasional Sinta 1–2. Artikel di atas 5 tahun boleh dipakai jika sangat sering disitasi dan menjadi landasan riset terkini di jurnal internasional."

**Paper yang lolos klausul pengecualian ("exempt foundational")** — boleh dipakai meski >5 tahun karena merupakan sumber primer metode yang dipakai langsung di skripsi, bukan sekadar tinjauan pendukung:

| Paper | Usia (per 2026) | Alasan exempt |
|---|---|---|
| Vaswani et al. (2017) | 9 th | Sumber formula self-attention, dasar Transformer di semua LLM modern |
| Lewis et al. (2020) | 6 th | Paper asli/seminal RAG |
| Robertson & Zaragoza (2009) | 17 th | Monograf kanonis formula BM25 — dipakai langsung sebagai Config C |
| Reimers & Gurevych (2019) | 7 th | Paper asli SBERT, dasar bi-encoder dense retrieval |
| Mikolov et al. (2013) | 13 th | Paper asli Word2Vec, dasar historis word embedding |
| Manning, Raghavan & Schütze (2009) | 17 th | Textbook kanonis IR (inverted index, TF-IDF, metrik evaluasi baku) |
| Karpukhin et al. (2020) | 6 th | Paper asli DPR, masih jadi rujukan utama riset dense retrieval terkini |

**Paper >5 tahun yang TIDAK direkomendasikan (gagal klausul pengecualian):**
- Abu Shawar & Atwell (2007) — 19 tahun, sudah terwakili empirisnya oleh Ajiz/Guntoro (2023) di 2.1.1, tidak menambah nilai landasan teori baru.
- Robertson et al. (1994) / Robertson & Walker (1994) — kandungan matematisnya sudah tercakup penuh di Robertson & Zaragoza (2009), redundan jika dipakai bertiga.

---

## 3. Peta 60 Paper → Kategori Pemakaian

### 3.1 Sudah dipakai di Bab 2.1 (jangan diulang detail, cross-reference saja bila perlu)
Ajiz (2023), Ruindungan & Jacobus (2021), Suasnawa (2023), Al Fajri & Hartono (2024), Muna (2025), Priccilia & Girsang (2024), Pratami (2025), Neumann (2025), Firdaus (2024), Bhat (2025), Lakatos (2025), Khasanova & Suh (2025), Salman (2026), Husain (2025), Pusparini (2025), Artayasa (2025), Abdurrazzaq (2025). *(Guntoro, Hidayat, M Ikhsan, Koay, Mori — sudah dihapus/diganti di 2.1, tetap tidak dipakai di 2.2.)*

### 3.2 Kandidat utama untuk 2.2 (assign satu lokasi primer per paper — lihat Bagian 4)
Ji et al. (2023)*, Robertson & Zaragoza (2009), Reimers & Gurevych (2019), Lewis et al. (2020), Es et al. (2024), Manning Raghavan & Schütze (2009), Karpukhin et al. (2020), Jurafsky & Martin (2026), Mikolov et al. (2013), Vaswani et al. (2017), Zhang et al. (2025), Hoffmann et al. (2022), Gemini Team (2025), Gemini Team (2024), Dam et al. (2024), Gao et al. (2024), Ovadia et al. (2024), Jimeno Yepes et al. (2024), Gomez-Cabello et al. (2025), Beauchemin et al. (2024).

*(\*Ji et al. sudah dipakai di 2.1.4/2.1.5 — di 2.2 hanya cross-reference singkat kalau perlu, JANGAN dijadikan sumber taksonomi 3-arah karena taksonomi itu milik Zhang et al.)*

### 3.3 Direkomendasikan TIDAK dipakai di Bab II (exclude — alasan di kolom)

| Paper | Alasan exclude |
|---|---|
| Orrù et al. (2025) — psikiatri | Terlalu jauh dari lingkup teknis RAG/IR; jurnal psikiatri, berisiko dibaca sebagai citation padding oleh penguji |
| Kulkarni et al. (2019) | Redundan dengan Dam et al. (2024) yang lebih baru & lebih relevan (pipeline NLU-DM-NLG sudah tercakup) |
| Abu Shawar & Atwell (2007) | >5 tahun, gagal klausul pengecualian (lihat Bagian 2) |
| Robertson et al. (1994); Robertson & Walker (1994) | Redundan — isinya sudah dirangkum penuh di Robertson & Zaragoza (2009) |
| Kang et al. (2023); Lee et al. (2024); Al-Joofi et al. (2026) | Fokus *hybrid/late-interaction retrieval* — skripsi Anda **tidak menguji hybrid**, hanya dense vs sparse murni. Berisiko scope-creep. Boleh disebut 1 kalimat di Bab V (Saran) sebagai *future work*, bukan di 2.2 |
| Yao et al. (2024) — security survey | Di luar lingkup RQ, kecuali Bab I/Batasan Masalah Anda eksplisit menyinggung keamanan/guardrail |
| Sun et al. (2024) — taksonomi 8-tipe | Lebih cocok mendukung analisis kualitatif RQ3 di Bab IV/2.1.5, bukan landasan teori 2.2 |
| Yao & Fujita (2024) — Adaptive RAG | Arsitektur agentic RAG tidak diimplementasikan di skripsi ini; opsional 1 kalimat "arah pengembangan lanjutan" saja |
| Google (2023) — PaLM 2 | Opsional/boleh dipotong untuk efisiensi sitasi — nilai tambahnya kecil dibanding Gemini Team (2024/2025) yang sudah mencakup evolusi arsitektur |
| Koay et al. (2026) | Sudah diputuskan exclude sejak revisi 2.1 (korpus UNSRAT tidak bertabel kompleks) |
| Bang et al. (2025) — kontraindikasi obat | Domain medis, kurang relevan dibanding Reuter (2025)/Beauchemin (2024) yang sudah mewakili argumen *chunking* dokumen legal/regulasi secara lebih pas |

---

## 4. Rekomendasi Penempatan per Sub-bab (2.2.1–2.2.10)

**Prinsip kerja utama:** setiap paper punya **satu lokasi primer**. Jangan ulangi elaborasi penuh paper yang sama di banyak sub-bab (pelajaran dari revisi 2.1 — lihat kasus Husain/Salman yang sempat direncanakan dobel). Target: **maksimal 3–4 sitasi baru per sub-bab**.

### 2.2.1 — Chatbot dan Conversational AI
- **Primer:** Dam et al. (2024) — survei transisi rule-based → generative, taksonomi Encoder-Decoder/Causal Decoder/Prefix Decoder, formula self-attention.
- **Sekunder (opsional, 1 kalimat penutup saja):** Vadlamani & Borada (2025) — evolusi Rule-based → Standalone LLM → LLM Agent, untuk menutup paragraf transisi menuju sub-bab berikutnya.
- **Exclude:** Abu Shawar & Atwell, Kulkarni (lihat 3.3).

### 2.2.2 — Information Retrieval dan Sistem Question-Answering
- **Primer:** Manning, Raghavan & Schütze (2009) — definisi IR klasik, inverted index, TF-IDF (exempt).
- **Sekunder:** Jurafsky & Martin (2026) — transisi ekstraktif → RAG modern, definisi Perplexity/Cross-Entropy yang dipakai konsisten di seluruh Bab II.
- **⚠️ Perlu tindakan:** par. 149 (contoh arsitektur DrQA) **tidak punya sumber terverifikasi** di 59 paper Anda. Tambahkan paper DrQA asli (Chen et al., 2017) ke `sitasi-bab2Full.md`, atau ganti contoh dengan Karpukhin et al. (2020) yang sudah terverifikasi (geser detail DPR-nya cukup disinggung sekilas di sini, detail penuh tetap di 2.2.4). **UPDATE: PAPER Chen 2017 SDH DITAMBAHKAN**

### 2.2.3 — Pencarian Leksikal (Sparse Retrieval): Algoritma BM25
- **Primer tunggal:** Robertson & Zaragoza (2009) — cukup satu sumber untuk seluruh formula ($k_1$, $b$, saturasi, RSJ weight), karena monograf ini sudah mencakup isi Robertson et al. (1994) dan Robertson & Walker (1994).
- **Drop:** Robertson et al. (1994), Robertson & Walker (1994) — redundan (lihat 3.3).

### 2.2.4 — Pencarian Semantik (Dense Retrieval): Embedding dan Cosine Similarity
- **Primer:** Reimers & Gurevych (2019) — SBERT, dasar bi-encoder.
- **Sekunder:** Mikolov et al. (2013) — transisi historis word embedding → sentence embedding (1 paragraf pembuka saja).
- **Sekunder:** Karpukhin et al. (2020) — bukti empiris dense > sparse pada kueri umum, DENGAN catatan kelemahannya pada kueri berbasis frasa langka (nuansa penting untuk argumen RQ2 Anda: kenapa sparse tetap kompetitif pada dokumen regulasi berkosakata formal).
- **Jangan tambahkan** Al-Joofi/Kang/Lee di sini (hybrid, di luar lingkup — lihat 3.3). Kalau ingin menyinggung *hybrid* sama sekali, cukup 1 kalimat penutup "beberapa penelitian mulai mengeksplorasi kombinasi dense-sparse (Al-Joofi et al., 2026), namun berada di luar cakupan penelitian ini yang membandingkan dense dan sparse secara terisolasi."

### 2.2.5 — Large Language Models (LLM)
- **Primer:** Vaswani et al. (2017) — self-attention, fondasi Transformer (exempt).
- **Primer:** Zhang et al. (2025) — **ganti sumber taksonomi 3-arah halusinasi di par. 168 dari [kosong] menjadi Zhang et al., BUKAN Ji et al.** (lihat temuan Bagian 6 poin 1).
- **Opsional:** Hoffmann et al. (2022) — scaling laws, mendukung argumen kenapa model kecil (Flash) + data banyak > model besar boros komputasi; bisa juga digeser ke 2.2.6 jika ingin dikaitkan langsung ke Gemini.
- **Cross-ref singkat saja:** Ji et al. (2023) — sudah dipakai penuh di 2.1.4/2.1.5, di sini cukup "sebagaimana dibahas pada Sub-bab 2.1.4" tanpa elaborasi ulang.
- **Exclude:** Orrù et al. (2025), Yao et al. (2024) — lihat 3.3.

### 2.2.6 — Google Gemini
- **Primer:** Gemini Team (2024) — Gemini 1.5 Technical Report (long-context, MoE, distillation Flash).
- **Primer:** Gemini Team (2025) — Gemini 2.5 Technical Report (thinking budget, reasoning benchmark).
- **⚠️ WAJIB DIVERIFIKASI MANUAL sebelum dipakai:** DeepMind (2026) — Gemini 3.5 Flash evaluation report. Saya tidak bisa mengonfirmasi keberadaan/akurasi dokumen ini (di luar jangkauan verifikasi saya). Jika model generator Anda benar `gemini-3.5-flash`, pastikan laporan ini benar-benar ada dan diakses langsung dari domain resmi Google DeepMind sebelum dikutip, karena ini menyangkut akurasi teknis inti metodologi skripsi Anda. **UPDATE: YA TERVERIFIKASI**
- **Opsional (boleh dipotong untuk efisiensi):** Google (2023) — PaLM 2, hanya jika ingin menjaga narasi evolusi historis lengkap sebelum era Gemini.

### 2.2.7 — Retrieval-Augmented Generation (RAG)
- **Primer:** Lewis et al. (2020) — definisi formal RAG-Sequence/RAG-Token (exempt, seminal).
- **Primer:** Gao et al. (2024) — taksonomi Naive/Advanced/Modular RAG, cocok persis untuk menjelaskan par. 176 (3 tahap indexing-retrieval-generation).
- **Primer:** Ovadia et al. (2024) — bukti empiris EMNLP RAG > fine-tuning, memperkuat argumen par. 175 dengan sumber internasional bereputasi tinggi (melengkapi Priccilia & Girsang yang sudah dipakai di 2.1.2).
- **Catatan integrasi 2.2.9 (LangChain):** sesuai catatan audit 2.1 (temuan 3.7), pertimbangkan lebur 2.2.9 ke penutup 2.2.7 di sini, karena LangChain adalah *framework* implementasi (bukan konsep teoretis independen) — cukup 1 paragraf penutup yang mencatat penggunaannya pada penelitian yang sudah dikutip (Neumann 2025, Artayasa 2025, Firdaus 2024, Pratami 2025 semuanya sudah memakai LangChain dalam metodologinya).
- **Jangan pakai** Sharma (2025) di sini — sudah dialokasikan ke 2.2.10 agar tidak redundan dengan Gao et al. (lihat di bawah).
- **Opsional/Bab V saja:** Yao & Fujita (2024) — Adaptive RAG, di luar cakupan implementasi.

### 2.2.8 — Strategi Segmentasi Dokumen (Chunking)
- **Primer:** Bhat et al. (2025) — sudah diramping di 2.1.3, di sini baru dielaborasi penuh (trade-off ukuran chunk, sensitivitas model embedding).
- **Primer:** Jimeno Yepes et al. (2024) — structural/element-type chunking, sumber langsung untuk klaim par. 179 soal *structural chunking mengungguli fixed-size*.
- **Primer:** Gomez-Cabello et al. (2025) — bukti empiris sensitivitas chunk terhadap model embedding dan LLM Gemini, mendukung par. 178.
- **Primer:** Beauchemin et al. (2024) — *parent-child chunking* pada dokumen hukum/regulasi, sumber langsung paling pas untuk klaim par. 180 soal pasal/klausul tidak boleh terputus. **Catat juga temuan pentingnya:** meski chunking sudah optimal, 5–13% jawaban RAG tetap mengandung halusinasi — nuansa jujur yang perlu masuk sebagai keterbatasan di Bab IV.
- **Opsional (pilih salah satu, jangan dua-duanya untuk efisiensi):** Reuter et al. (2025) — *Document-Level Retrieval Mismatch* pada dokumen legal, relevan tapi lebih maju (multi-dokumen retrieval) daripada fokus chunking-tunggal skripsi Anda. Sertakan hanya jika ingin memperkaya diskusi keterbatasan.
- **Exclude:** Koay et al. (2026), Bang et al. (2025) — lihat 3.3.

### 2.2.9 — Framework LangChain
- **Rekomendasi struktural:** lebur ke penutup 2.2.7 (lihat catatan di atas). Jika tetap dipertahankan sebagai sub-bab terpisah, catat: **tidak ada paper akademik murni tentang LangChain di 59 paper Anda** (karena LangChain adalah dokumentasi software, bukan makalah ilmiah) — sitasi yang tepat adalah merujuk ke penelitian yang memakainya sebagai bukti penerapan (Neumann 2025, Artayasa 2025, Firdaus 2024, Pratami 2025), bukan mengarang sitasi akademik untuk framework itu sendiri.

### 2.2.10 — Framework Evaluasi Ragas
- **Primer:** Es et al. (2024) — paper asli RAGAS (exempt/seminal, EACL 2024).
- **Sekunder:** Sharma (2025) — survei RAG 2025 dengan sudut pandang evaluasi/robustness (ARES, RAGTruth, dsb.), melengkapi Gao et al. (2024) yang sudah dipakai di 2.2.7 dengan sudut pandang berbeda (arsitektur vs evaluasi) sehingga tidak redundan.
- **Cross-ref singkat:** Khasanova & Suh (2025), Artayasa (2025) — sudah dipakai penuh di 2.1.4, cukup disebut sekilas di sini sebagai "penerapan langsung di konteks kampus Indonesia (lihat Sub-bab 2.1.4)".

---

## 5. Checklist Tindakan (urutan disarankan)

- [ ] **2.2.1** — ganti sumber jadi Dam et al. (2024) sebagai primer; hapus rencana pakai Abu Shawar & Atwell/Kulkarni.
- [ ] **2.2.2** — isi Manning et al. (2009) & Jurafsky & Martin (2026); **selesaikan dulu isu DrQA** (tambah paper aslinya ke `sitasi-bab2Full.md` atau ganti contoh).
- [ ] **2.2.3** — sederhanakan jadi 1 sumber (Robertson & Zaragoza 2009) untuk seluruh formula BM25.
- [ ] **2.2.4** — isi Reimers & Gurevych, Mikolov, Karpukhin; tambahkan nuansa kelemahan DPR pada kueri frasa langka (penting untuk argumen RQ2).
- [ ] **2.2.5** — **PENTING:** perbaiki atribusi taksonomi halusinasi par. 168 dari Ji et al. → Zhang et al. (2025); isi Vaswani et al.; opsional Hoffmann et al.
- [ ] **2.2.6** — isi Gemini Team (2024) & (2025); **jangan submit sitasi paper #51 (Gemini 3.5 Flash) sebelum diverifikasi manual**; putuskan apakah PaLM 2 tetap dipakai atau dipotong.
- [ ] **2.2.7** — isi Lewis et al., Gao et al., Ovadia et al.; putuskan apakah 2.2.9 dilebur ke sini.
- [ ] **2.2.8** — isi Bhat (elaborasi penuh), Jimeno Yepes, Gomez-Cabello, Beauchemin; putuskan apakah Reuter et al. ditambahkan.
- [ ] **2.2.9** — putuskan lebur ke 2.2.7 atau tetap berdiri sendiri dengan sitasi tidak langsung (lihat catatan di atas).
- [ ] **2.2.10** — isi Es et al. sebagai primer; Sharma sebagai sekunder (sudut evaluasi, bukan arsitektur, agar tidak tumpang tindih dengan Gao et al. di 2.2.7).
- [ ] **Cek ulang seluruh Bab II** — pastikan tidak ada paper yang dielaborasi penuh di lebih dari satu sub-bab (pola yang sama dengan revisi 2.1: satu lokasi primer per paper, cross-reference singkat di lokasi lain jika perlu).
- [ ] **Daftar Pustaka** — tambahkan seluruh entri baru dari Bagian 4 di atas (~20 paper), pastikan format APA dan urutan alfabetis konsisten.
- [ ] **Cek gaya bahasa** — jalankan hasil revisi melalui skill `stop-slop-id-akademik-v2`.

---

## 6. Hal yang Wajib Diverifikasi Penulis Sebelum Finalisasi (bukan hasil karangan AI — murni temuan audit)

1. **Kesalahan atribusi taksonomi halusinasi** di par. 168 draf .docx: teks tiga-kategori (input-conflicting/context-conflicting/fact-conflicting) adalah milik **Zhang et al. (2025)**, bukan Ji et al. (2023). Wajib diperbaiki — ini technically salah kutip, bukan sekadar isu gaya.
2. **Sitasi DrQA (par. 149) tidak punya sumber di korpus 59 paper.** Perlu ditambahkan atau diganti — jangan biarkan slot kosong terisi dengan sitasi yang tidak diverifikasi.
3. **Paper #48, #49, #50, #51 (technical report Gemini/PaLM)** — terutama #51 (Gemini 3.5 Flash, Mei 2026) berada di luar jangkauan verifikasi saya. Karena ini menyangkut akurasi teknis model generator yang benar-benar dipakai di skripsi Anda, **verifikasi langsung ke sumber resmi wajib dilakukan** sebelum sidang — bukan sekadar isu sitasi, tapi isu keakuratan metodologi.
4. **Nama model "gemini-3.5-flash" dan "gemini-3.1-pro"** yang disebut di par. 172 draf — pastikan ini nama resmi yang benar-benar dipakai di implementasi Anda (bukan salah ketik dari versi lain), karena akan ditanyakan langsung oleh penguji sidang.

---

## 7. Prinsip Kerja (diwariskan dari revisi 2.1, berlaku juga di 2.2)

1. **Satu lokasi primer per paper** — hindari pola "sebar sitasi ke banyak sub-bab" yang sempat direncanakan untuk Husain/Salman di revisi 2.1.
2. **Sitasi minimum tapi maksimal dipertanggungjawabkan** — target 3–4 sitasi baru per sub-bab, bukan menumpuk semua 59 paper ke dalam 10 sub-bab.
3. **Tidak overclaim, tidak mengarang** —slot sitasi kosong di draf tidak boleh diisi sembarang paper hanya karena topiknya mirip; harus benar-benar merepresentasikan klaim kalimat tersebut (lihat kasus Ji vs Zhang di atas sebagai contoh kesalahan yang harus dihindari terulang).
4. **Exempt foundational papers boleh dipakai meski >5 tahun**, tapi HANYA jika memang sumber primer metode yang dipakai langsung (BM25, Transformer, SBERT, RAG, dsb.) — bukan sekadar "paper lama yang terkenal".
5. **Verifikasi manual wajib untuk sitasi berisiko tinggi** (technical report model AI yang sangat baru) — AI (saya) tidak bisa menjadi validator tunggal untuk klaim yang berada di luar cutoff pengetahuan atau tanpa akses pencarian langsung.

---

*File ini dibuat berdasarkan pembacaan penuh atas 60 entri di `sitasi-bab2Full.md` (Bagian 1–9) serta teks lengkap Sub-bab 2.2.1–2.2.10 dari draf `.docx` (par. 144–190). Silakan lanjutkan revisi berdasarkan checklist di Bagian 5.*
