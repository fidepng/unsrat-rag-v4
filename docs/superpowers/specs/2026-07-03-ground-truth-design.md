# Design Spec: RAG Evaluation Ground Truth Dataset
**Tanggal:** 2026-07-03  
**Status:** Draf Awal (Untuk Test Evaluate)  
**Referensi PRD:** Section 9.1, D-B6 (Natural Language & Key Facts), FR-11 (Fallback Response)

## 1. Tujuan & Kriteria Desain
Ground truth ini dirancang untuk mengevaluasi performa sistem RAG UNSRAT secara komparatif antara **Config B (Vector RAG - 2000 char)** dan **Config C (BM25 RAG - 2000 char)**. 

### Kriteria Utama (D-B6)
*   **Natural Language & Key Facts:** Kolom `reference` berisi jawaban dalam kalimat mengalir (*natural*) yang memuat fakta kunci (angka, durasi, syarat), bukan salinan *verbatim* dari dokumen hukum.
*   **Variasi Bahasa:** Pertanyaan dibagi menjadi bahasa baku, bahasa tidak baku (informal), dan dialek Manado (contoh: *torang*, *depe*, *so*, *bole*, *jo*). Hal ini dirancang untuk menantang batas pencarian semantik (Config B) vs pencarian kata kunci literal (Config C).
*   **Out-of-Domain (OOD):** Menyertakan 3 pertanyaan di luar cakupan dokumen akademik untuk menguji keandalan similarity threshold (apakah berhasil memicu `FALLBACK_RESPONSE` tanpa berhalusinasi).

---

## 2. Struktur Dataset CSV (`eval/dataset/ground_truth.csv`)
File disimpan dalam format **CSV UTF-8 dengan BOM** (agar aman diedit kembali di Excel).

### Skema Kolom
1.  `user_input`: Pertanyaan uji.
2.  `reference`: Jawaban standar emas.
3.  `category`: Kategori (`academic`, `calendar`, `institution_profile`, `faq`, `ood`).
4.  `source_doc`: Nama file Markdown di corpus, atau `None` jika OOD.
5.  `notes`: Rujukan pasal, ayat, atau keterangan tambahan.

---

## 3. Distribusi Kategori (30 Data)

| Kategori | Jumlah Q&A | Persentase | Deskripsi Cakupan |
|---|---|---|---|
| **Academic (`academic`)** | 11 | 36,7% | Aturan SKS, KKT, Magang, Cuti, Batas Studi, Cum Laude, DO |
| **Calendar (`calendar`)** | 8 | 26,7% | Jadwal Kuliah, UAS, UTS, KRS, Wisuda, Yudisium KKT |
| **Institution Profile (`institution_profile`)** | 5 | 16,7% | Visi, Misi, Sejarah, Lambang, Bendera, Akreditasi |
| **FAQ (`faq`)** | 3 | 10,0% | Prosedur banding nilai, konversi PKM nasional, keterlambatan nilai |
| **Out-of-Domain (`ood`)** | 3 | 10,0% | Pertanyaan di luar cakupan (SIM, Piala Dunia, Tiket Pesawat) |

---

## 4. Rincian Data Ground Truth

*(Rincian lengkap 30 pertanyaan telah dituangkan ke dalam file [ground_truth.csv](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/eval/dataset/ground_truth.csv))*

---

## 5. Dokumentasi Perubahan & Panduan Revisi
Jika Anda ingin merevisi atau menambah pertanyaan di kemudian hari:
1.  Buka file `eval/dataset/ground_truth.csv` menggunakan text editor (VS Code, Notepad) or Microsoft Excel.
2.  Jika menggunakan Excel, pastikan untuk menyimpan kembali (*Save As*) dengan tipe **CSV UTF-8 (Comma delimited) (*.csv)** untuk menjaga encoding karakter khusus.
3.  Pastikan kolom `user_input` dan `reference` diapit oleh tanda kutip ganda `"` jika mengandung koma atau tanda petik di dalamnya.
