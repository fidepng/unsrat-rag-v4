# Rencana Revisi Bab 2.1 (Kajian Pustaka) — Skripsi RAG Chatbot UNSRAT

**Dokumen ini adalah brief hand-off** untuk melanjutkan revisi Sub-bab 2.1.1–2.1.5 di sesi/AI lain, tanpa perlu mengulang seluruh histori diskusi sebelumnya. Berisi konteks penelitian, seluruh temuan audit yang relevan, dan rencana kerja konkret.

---

## 1. Konteks Penelitian

- **Judul:** Implementasi dan Evaluasi Kinerja Chatbot Layanan Informasi Akademik UNSRAT Menggunakan RAG dan Google Gemini
- **Jenis:** Skripsi Prototipe (Jalur Prototipe + HAKI), Teknik Informatika UNSRAT
- **Status:** Persiapan Seminar Hasil (bukan sidang akhir)
- **Inti penelitian:** Membandingkan dua mekanisme retrieval dalam arsitektur RAG — **Config B** (dense/semantic retrieval, ChromaDB + `gemini-embedding-001`, cosine similarity) vs **Config C** (sparse/lexical retrieval, BM25) — pada korpus 9 dokumen resmi UNSRAT (188 chunk), dievaluasi dengan framework **Ragas** (Faithfulness, Answer Relevancy, Context Precision, Context Recall) atas 80 pasangan *ground truth*.
- **3 Rumusan Masalah / Tujuan (sudah selaras 3:3):**
  1. Rancang-bangun prototipe chatbot RAG (LangChain + ChromaDB + Gemini)
  2. Komparasi kinerja dense vs sparse retrieval via Ragas
  3. Karakterisasi pola kegagalan tiap mekanisme retrieval + implikasi mitigasi
- **Gaya penulisan:** Wajib mengikuti skill `stop-slop-id-akademik-v2` (hindari "selain itu", "dengan demikian", em dash, pola "X dan Y" repetitif, monotoni "menunjukkan/mengindikasikan").
- **Prinsip kerja:** Zero-hallucination, tidak boleh mengarang data/klaim, semua sitasi harus bisa dipertanggungjawabkan penulis saat sidang.

---

## 2. Struktur Bab 2.1 Saat Ini (sebelum revisi)

| Sub-bab | Judul saat ini                                     | Isi                                                                                                    |
| ---------| ----------------------------------------------------| --------------------------------------------------------------------------------------------------------|
| 2.1.1   | Pendekatan pada Chatbot Akademik Perguruan Tinggi  | AIML (Ajiz 2023, Guntoro 2020), Rasa/NLU (Ruindungan 2021, Suasnawa 2022, Al Fajri 2024, Hidayat 2024) |
| 2.1.2   | Adopsi Large Language Models pada Layanan Akademik | M Ikhsan et al. (2025), Priccilia & Girsang (2024), Muna et al. (2025)                                 |
| 2.1.3   | Implementasi Arsitektur RAG                        | Pratami (2025), Neumann (2025), Firdaus (2024), + argumen chunking trade-off (Bhat 2025)               |
| 2.1.4   | Evaluasi Kinerja Sistem Berbasis LLM dan RAG       | Lakatos (2025), Khasanova Zafar kizi & Suh (2025), Koay (2026)                                         |
| 2.1.5   | Research Gap                                       | Sintesis penutup + Tabel 2.1 Penelitian Terkait                                                        |

---

## 3. Temuan Audit yang Sudah Dilakukan (WAJIB ditindaklanjuti)

### 3.1 Masalah kategorisasi sitasi — M Ikhsan et al. (2025)
- Dikutip di 2.1.2 sebagai contoh "adopsi LLM", tapi paper aslinya (sudah dikonfirmasi dari teks draf sendiri) memakai **model Sequential dari Keras** — arsitektur *neural network* klasik, **bukan LLM**.
- **Keputusan:** direkomendasikan **DIHAPUS** dari 2.1.2 dan dari Tabel 2.1 (opsi paling aman, tidak melemahkan paragraf karena Priccilia&Girsang + Muna et al. sudah cukup).
- Alternatif jika ingin dipertahankan: pindah ke 2.1.1 dengan framing "kategori ketiga: neural network klasifikasi" — tapi menambah kompleksitas untuk nilai tambah kecil.

### 3.2 Duplikasi argumen — Bhat et al. (2025)
- Argumen *trade-off* presisi ekstraksi vs keutuhan konteks (tergantung ukuran chunk) dikutip **dua kali** dengan kalimat nyaris identik: di 2.1.3 dan di 2.2.8.
- **Keputusan:** ramping di 2.1.3 jadi hanya kalimat transisi singkat ("dibahas lebih lanjut di 2.2.8"), detail lengkap cukup satu tempat di 2.2.8.

### 3.3 Tabel 2.1 (Penelitian Terkait) mencampur dua jenis sumber
- Berisi studi aplikatif (Guntoro, Muna, Pratami, dst) **dicampur** dengan paper fondasi teoretis murni (Robertson & Zaragoza 2009/BM25, Reimers & Gurevych 2019/SBERT, Lewis et al. 2021/RAG) yang kolom "Hasil Utama"-nya kosong ("—").
- **Keputusan:** keluarkan 3 baris fondasi teoretis itu dari Tabel 2.1 — mereka harus dikutip di 2.2 (Dasar Teori) saja, bukan di tabel perbandingan penelitian terdahulu.

### 3.4 Sitasi "nama-drop" tanpa elaborasi di 2.1.5
- **Dzaki Salman & Nasution (2026)** dan **Husain et al. (2025)** disebut sekali tanpa penjelasan temuan spesifik: *"...menuju ke arsitektur RAG berbasis LLM (Dzaki Salman & Nasution, 2026; Husain et al., 2025)."*
- **UPDATE PENTING:** kedua paper ini **sudah dibaca penuh** (lihat Bagian 4 di bawah) — jadi sitasi ini sekarang **wajib dielaborasi**, bukan dihapus. Lihat rencana penempatan di Bagian 5.

### 3.5 Kesalahan format sitasi APA — Salman et al. (2026)
- Paper "Implementation of Retrieval-Augmented Generation Method..." ditulis oleh 4 penulis: **Muhammad Dzaki Salman** (penulis pertama), Rahmaddeni, Torkis Nasution, Susanti.
- Draf saat ini menulis sitasi sebagai **"Dzaki Salman & Nasution, 2026"** — ini **salah kaidah APA** (menggabungkan penulis pertama dan ketiga seolah hanya berdua).
- **Perbaikan wajib:** ganti ke **"Salman et al. (2026)"** di semua kemunculan (badan teks + Daftar Pustaka), dan cek urutan alfabetis Daftar Pustaka (harus di bawah "Salman", bukan "Dzaki Salman").

### 3.6 Judul 2.1.2 tidak akurat terhadap isi
- Judul "...Layanan Informasi **Berbasis Regulasi**" tapi isi ketiga studi (M Ikhsan, Priccilia&Girsang, Muna) sebenarnya membahas layanan akademik/praktikum **umum**, bukan spesifik dokumen regulasi formal.
- **Keputusan:** ganti judul jadi **"Adopsi Large Language Models pada Layanan Informasi Akademik"** (hapus kata "Berbasis Regulasi").

### 3.7 Sub-bab 2.2.9 (LangChain) terlalu tipis
- Di luar cakupan 2.1, tapi dicatat: pertimbangkan dilebur ke penutup 2.2.7 (RAG) karena isinya hanya ~1 paragraf pendek. *(Bukan prioritas untuk sesi revisi 2.1 ini, hanya catatan.)*

---

## 4. Laporan lengkap Paper di Drf awal (Sebelum reivisi)

Bisa dilihat di file: **sitasi-bab2.md** (terlampir)

---

## 5. Draf Paragraf Revisi Research Gap (2.1.5) — Sudah Disiapkan

Draf berikut sudah dibuat di sesi sebelumnya dan siap dipakai/disempurnakan:

> Pada dokumen hukum dan regulasi, pencarian leksikal (sparse retrieval) terbukti tetap kompetitif dibandingkan teknik pencarian semantik yang belum memakai representasi embedding neural modern. Pusparini et al. (2025) mengonfirmasi hal ini secara empiris pada korpus regulasi pemerintah Indonesia (BRIN): BM25 dan TF-IDF menghasilkan presisi yang hampir identik (0,435) dan jauh mengungguli Latent Semantic Indexing (0,112), meski penelitian tersebut tidak melibatkan arsitektur RAG maupun proses generasi jawaban oleh LLM sama sekali. Ragas pun sudah mulai dipakai pada chatbot akademik Indonesia berbasis RAG, baik untuk mengaudit satu sistem tunggal (Artayasa et al., 2025; Husain et al., 2025) maupun, yang paling relevan, untuk membandingkan mekanisme dense dan sparse retrieval secara langsung pada chatbot layanan kampus (Salman et al., 2026). Namun studi terakhir ini mengevaluasi retrieval menggunakan metrik IR klasik (precision, recall, NDCG) ditambah satu metrik Faithfulness tunggal, tanpa kerangka empat-metrik Ragas yang menilai kualitas retrieval dan generasi secara terpisah (context precision dan context recall), dan tanpa analisis kegagalan kualitatif per mekanisme retrieval. Korpus peraturan akademik perguruan tinggi berbahasa Indonesia sendiri, dengan kontrol variabel ukuran chunk yang dikunci identik antarkonfigurasi serta analisis pola kegagalan sistematis, nyaris belum dijadikan objek eksperimen komparatif seperti ini.

**Catatan:** paragraf ini masih perlu di-cross-check dengan gaya `stop-slop-id-akademik-v2` (cek pola kalimat, variasi panjang, dsb) saat revisi final berlangsung.

---

## 6. Rencana Kerja Revisi 2.1.1–2.1.5 (Checklist Tindakan)

Urutan disarankan untuk sesi revisi selanjutnya:

- [ ] **2.1.1** — audit ulang apakah semua sitasi (Ajiz, Guntoro, Ruindungan, Suasnawa, Al Fajri, Hidayat) masih perlu dipertahankan semua atau ada yang redundan (**belum diaudit detail di sesi sebelumnya** — cek satu per satu overlap argumen sebelum revisi besar)
- [ ] **2.1.2** — (a) hapus M Ikhsan et al. (2025) dari teks + Tabel 2.1; (b) ganti judul jadi "...Layanan Informasi Akademik"; (c) tambahkan Husain et al. (2025) sebagai pembanding metodologis kuat, evaluasi apakah Muna et al. (2025) masih perlu dipertahankan berdampingan atau cukup digantikan sebagian bobotnya
- [ ] **2.1.3** — ramping argumen Bhat et al. (2025) jadi kalimat transisi singkat saja (detail lengkap tetap di 2.2.8)
- [ ] **2.1.4** — belum diaudit detail di sesi sebelumnya, perlu cek relevansi Lakatos/Khasanova/Koay terhadap paragraf masing-masing sebelum revisi besar
- [ ] **2.1.5** — (a) revisi paragraf Research Gap dengan draf di Bagian 5; (b) perbaiki format sitasi "Dzaki Salman & Nasution" → "Salman et al. (2026)"; (c) elaborasi sitasi Husain et al. dan Salman et al. yang sebelumnya nama-drop; (d) verifikasi ulang apakah Mori et al. (2025) masih dipertahankan atau digantikan Pusparini et al. (2025)
- [ ] **Tabel 2.1** — keluarkan 3 baris fondasi teoretis (Robertson & Zaragoza/BM25, Reimers & Gurevych/SBERT, Lewis et al./RAG), sisakan hanya studi aplikatif chatbot/RAG yang sebanding metodologinya; pertimbangkan tambah baris untuk Salman et al. (2026), Husain et al. (2025), Pusparini et al. (2025)
- [ ] **Seluruh Daftar Pustaka** — cek ulang entri "Dzaki Salman & Nasution" jadi entri alfabetis "Salman", tambahkan entri Husain et al. (2025) dan Pusparini et al. (2025) jika belum ada
- [ ] **Cek gaya bahasa** — jalankan hasil revisi 2.1.1–2.1.5 melalui prinsip skill `stop-slop-id-akademik-v2` untuk memastikan tidak ada pola AI-sounding yang baru muncul dari proses editing

---

## 7. Prinsip yang Harus Dipegang Selama Revisi (agar sesuai tujuan awal Anda)

1. **Sitasi minimum tapi maksimal dipertanggungjawabkan** — tujuan Anda eksplisit: kurangi jumlah sitasi redundan, pertahankan hanya yang benar-benar Anda pahami isinya dan siap ditanya detail saat sidang.
2. **Jangan overclaim novelty** — dengan adanya Salman et al. (2026), klaim "belum ada penelitian yang membandingkan..." harus dipersempit presisinya (lihat Bagian 5), tidak dihapus sepenuhnya karena gap Anda tetap valid secara spesifik.
3. **Setiap studi yang disebut di 2.1 harus dijelaskan temuan konkretnya** — tidak boleh ada lagi pola "nama-drop" (sebut nama tanpa elaborasi), seperti kasus 3.4 di atas.
4. **Verifikasi silang seperti kasus M Ikhsan** — sebelum revisi final, cek ulang apakah semua sitasi lain di 2.1 (terutama yang levelnya "second-hand" dan belum pernah dibaca full paper-nya oleh penulis) benar-benar akurat terhadap metode/hasil yang diklaim.

---

*File ini dibuat sebagai ringkasan hand-off dari sesi diskusi sebelumnya (audit struktural Bab II, verifikasi sitasi M Ikhsan, dan analisis 3 paper baru: Salman et al. 2026, Husain et al. 2025, Pusparini et al. 2025). Silakan lanjutkan revisi 2.1.1–2.1.5 berdasarkan checklist di Bagian 6.*
