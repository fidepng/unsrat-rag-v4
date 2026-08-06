# Laporan Analisis Mendalam Evaluasi RAGAS (n=80)

*Dihasilkan secara otomatis pada: 2026-08-06 19:49:40 WITA*


## 1. Statistik Volume Dataset

Analisis dilakukan secara komparatif antara dua konfigurasi RAG:
- **Config B (Dense Retrieval - Vector Search)**: 80 kueri teruji.
- **Config C (Sparse Retrieval - BM25)**: 80 kueri teruji.


## 2. Perbandingan Rata-Rata Metrik (Global Mean)

| Metrik | Config B (Dense) | Config C (Sparse) | Selisih (B - C) |
| --- | --- | --- | --- |
| Faithfulness | 0.8044 | 0.8108 | -0.0064 |
| Answer Relevancy | 0.7553 | 0.6772 | +0.0782 |
| Context Precision | 0.8323 | 0.6562 | +0.1760 |
| Context Recall | 0.7931 | 0.6294 | +0.1636 |


## 3. Distribusi Sebaran Statistik Skor Individual

| Config | Metrik | Mean | Median | Min | Max | % Sempurna (1.0) | % Gagal (0.0) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Config B (Dense) | Faithfulness | 0.804 | 1.0 | 0.0 | 1.0 | 62.5% | 12.5% |
| Config B (Dense) | Answer Relevancy | 0.755 | 0.797 | 0.0 | 0.931 | 0.0% | 6.2% |
| Config B (Dense) | Context Precision | 0.832 | 1.0 | 0.0 | 1.0 | 0.0% | 7.5% |
| Config B (Dense) | Context Recall | 0.793 | 1.0 | 0.0 | 1.0 | 62.5% | 10.0% |
| Config C (Sparse) | Faithfulness | 0.811 | 1.0 | 0.0 | 1.0 | 50.6% | 2.5% |
| Config C (Sparse) | Answer Relevancy | 0.677 | 0.793 | 0.0 | 0.933 | 0.0% | 16.5% |
| Config C (Sparse) | Context Precision | 0.656 | 0.819 | 0.0 | 1.0 | 0.0% | 18.8% |
| Config C (Sparse) | Context Recall | 0.629 | 0.775 | 0.0 | 1.0 | 47.5% | 21.2% |


## 4. Audit Kegagalan Retrieval (Konteks Kosong)

- **Config B (Dense)**: 2 kueri gagal melakukan retrieval (Konteks Kosong / Terfilter Threshold).
- **Config C (Sparse)**: 0 kueri gagal melakukan retrieval (Konteks Kosong).


## 5. Analisis Kasus Kegagalan Spesifik (Config B)

#### Top 5 Kelemahan Context Precision (Mengambil Informasi Tidak Relevan):

| Kueri / Pertanyaan | Context Precision | Context Recall | Answer Relevancy |
| --- | --- | --- | --- |
| Kalau dulu pernah di-DO dari S1, masih ada kesempatan daftar ulang nggak di kampus yang sama? | 0.0 | 0.0 | 0.0 |
| Wisuda tahun ini ada berapa kali dan sekitar bulan apa saja? | 0.0 | 0.75 | 0.7385874291057407 |
| Me looking at old UNSRAT archive record for leadership. What exactly is Dekan do, and how many maximum semester for student in Program Sarjana to finish their study? | 0.0 | 0.2222222222222222 | 0.8692288208106608 |
| Helo, my name is Andi Pratama and I am a prospektiv undergraduat student who wants to join a top reserch university to develop my akademik and entreprenurial skils. I am trying to figur out how the campus is organized to suport students. Can you tel me what exactly is the role of a Dekan, and what is the duty of a Dosen who helps with final asigments? And also, looking at the list of past Rectors, who was the Rektor in charge from 2008 to 2014 that woud normaly isue the decree to apoint a Dekan? | 0.0 | 0.0 | 0.0 |
| klo sy nnti blajar trkait riset yg wajib ngacu k standar penelitian, mtd pembelajran apa aja yg bsa sy plih? | 0.0 | 0.0 | 0.0 |


#### Top 5 Kelemahan Context Recall (Informasi Relevan Terlewat / Tidak Terambil):

| Kueri / Pertanyaan | Context Precision | Context Recall | Answer Relevancy |
| --- | --- | --- | --- |
| Kalau dulu pernah di-DO dari S1, masih ada kesempatan daftar ulang nggak di kampus yang sama? | 0.0 | 0.0 | 0.0 |
| kapan mulai UAS untuk semester genap ini? | 0.9999999999 | 0.0 | 0.8419880112498633 |
| Sejak kapan sih kampus ini resmi jadi PTN (universitas negeri)? | 0.9999999999 | 0.0 | 0.7210332896031626 |
| In my capacity as a university archivist dedicated to preserving institutional history and maintaining accurate records, I am compiling a comprehensive overview of the operational and strategic frameworks of UNSRAT. Could you please elucidate how UNSRAT structures its vision, mission, and strategies to achieve its long-term objectives, while also detailing the specific administrative protocols students must navigate, such as the system used for student identification coding and the procedures for registering their academic courses on Portal INSPIRE? | 0.3333333333 | 0.0 | 0.7552460185709906 |
| Bagaimana cara agar bisa lulus dalam 3,5 tahun? | 0.0 | 0.0 | 0.0 |


## 6. Sampel Kasus Kegagalan Terburuk (Audit Manual)

#### Worst Queries - Config B (Dense)

1. **Q**: Kalau dulu pernah di-DO dari S1, masih ada kesempatan daftar ulang nggak di kampus yang sama?
   - *Rata-rata Skor*: 0.000
   - *Catatan Analisis*: nan


1. **Q**: Helo, my name is Andi Pratama and I am a prospektiv undergraduat student who wants to join a top reserch university to develop my akademik and entreprenurial skils. I am trying to figur out how the campus is organized to suport students. Can you tel me what exactly is the role of a Dekan, and what is the duty of a Dosen who helps with final asigments? And also, looking at the list of past Rectors, who was the Rektor in charge from 2008 to 2014 that woud normaly isue the decree to apoint a Dekan?
   - *Rata-rata Skor*: 0.000
   - *Catatan Analisis*: nan


1. **Q**: klo sy nnti blajar trkait riset yg wajib ngacu k standar penelitian, mtd pembelajran apa aja yg bsa sy plih?
   - *Rata-rata Skor*: 0.000
   - *Catatan Analisis*: nan


#### Worst Queries - Config C (Sparse)

1. **Q**: In my capacity as a university archivist dedicated to preserving institutional history and maintaining accurate records, I am compiling a comprehensive overview of the operational and strategic frameworks of UNSRAT. Could you please elucidate how UNSRAT structures its vision, mission, and strategies to achieve its long-term objectives, while also detailing the specific administrative protocols students must navigate, such as the system used for student identification coding and the procedures for registering their academic courses on Portal INSPIRE?
   - *Rata-rata Skor*: 0.050
   - *Catatan Analisis*: nan


1. **Q**: Kalau nggak puas sama nilai yang keluar, ada tenggat waktu buat komplain nggak?
   - *Rata-rata Skor*: 0.083
   - *Catatan Analisis*: nan


1. **Q**: Kalau dulu pernah di-DO dari S1, masih ada kesempatan daftar ulang nggak di kampus yang sama?
   - *Rata-rata Skor*: 0.125
   - *Catatan Analisis*: nan



## 7. Metodologi Evaluasi & Referensi Ilmiah

Evaluasi dilakukan menggunakan metrik dari framework **RAGAS (Retrieval Augmented Generation Assessment)** yang berbasis *LLM-as-a-Judge* (dalam hal ini menggunakan model evaluator `gemini-3.1-pro-preview`). Berikut adalah definisi matematis dan konseptual dari metrik yang diukur:

1. **Faithfulness (Keshahihan)**: Mengukur kebenaran faktual jawaban terhadap konteks yang diambil.
   $$\text{Faithfulness} = \frac{\text{Jumlah statement yang didukung konteks}}{\text{Total statement dalam jawaban}}$$
2. **Answer Relevancy (Kerelevanan Jawaban)**: Mengukur seberapa tepat jawaban menjawab inti pertanyaan.
3. **Context Precision (Ketepatan Konteks)**: Mengukur apakah potongan teks (chunk) yang relevan ditempatkan pada peringkat atas hasil pencarian.
4. **Context Recall (Kecakupan Konteks)**: Mengukur sejauh mana semua informasi yang dibutuhkan untuk menjawab pertanyaan (berdasarkan referensi ground truth) berhasil diambil oleh retriever.

**Referensi Ilmiah Utama:**
- Es, S., Jha, A., Espinosa, A. P., Anshu, A., & & others. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation*. arXiv preprint arXiv:2309.15217.
