# Laporan Audit Kualitas Dataset RAG - ground_truth.csv

*Dihasilkan secara otomatis pada: 2026-08-06 19:49:07 WITA*


## 1. Statistik Volume & Cakupan Dokumen

Total Baris Kueri Terdaftar: **80**


#### Distribusi Berkas Regulasi Sumber (Source Doc):

| Dokumen Regulasi | Jumlah Kueri |
| --- | --- |
| Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md | 32 |
| Kalender_Akademik_UNSRAT_Genap_2025-2026.md | 11 |
| 01_sejarah.md | 6 |
| nan | 5 |
| 07_akreditasi.md | 4 |
| 02_visi_misi.md | 4 |
| 04_lambang.md | 4 |
| 05_bendera.md | 4 |
| 06_mars_hymne.md | 4 |
| 03_tujuan_sasaran_strategi.md | 4 |
| 03_tujuan_sasaran_strategi.md, Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md | 1 |
| Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md, 01_sejarah.md | 1 |


#### Distribusi Tipologi Kueri (Category):

| Kategori / Tipe Kueri | Jumlah Kueri |
| --- | --- |
| semantic | 34 |
| lexical | 16 |
| multi-hop | 15 |
| abstract | 15 |


## 2. Distribusi Bias Leksikal vs Semantik

- **Rata-rata Tumpang Tindih Kata (Lexical Overlap)**: 51.28%
- **Kueri Tipe Pencocokan Kata Kunci (Lexical Bias >50% overlap)**: 34 (42.50%)
- **Kueri Tipe Makna/Parafrase (Semantic Bias <=20% overlap)**: 13 (16.25%)


## 3. Validitas & Kualitas Data

- **Kueri Kosong (Empty User Input)**: 0
- **Jawaban Referensi Kosong (Empty Reference)**: 0
- **Rata-rata Panjang Kueri**: 14.2 kata
- **Rata-rata Panjang Jawaban Referensi**: 73.7 kata


## 4. Sampel Kasus Klasifikasi Kueri

#### Sampel Kueri Potensi Lexical Bias (>50% Overlap)

- **Q**: berapa sks untuk magang
- **R**: *Beban SKS untuk kegiatan magang di Universitas Sam Ratulangi (UNSRAT) dibedakan berdasarkan status mahasiswa sebagai berikut:
1. Bagi Mahasiswa UNSRAT (Program MBKM / Pembelajaran di Luar Program Studi)
Kegiatan magang merupakan salah satu bentuk pemenuhan beban belajar resmi. Jumlah SKS yang dapat diakui dan dikonversikan adalah:
Setara 20 SKS untuk pemenuhan sebagian beban belajar selama 1 (satu) semester di program studi yang berbeda di UNSRAT atau luar UNSRAT.
Maksimal 40 SKS untuk pemenuhan beban belajar paling lama 2 (dua) semester di luar UNSRAT.

Bagi Mahasiswa Asing (Magang di UNSRAT)
Mahasiswa asing dari perguruan tinggi luar negeri yang diakui dapat diterima untuk melakukan magang atau kuliah paruh waktu di UNSRAT dengan beban:
Minimal 14 SKS.*
- *Overlap Score*: 75.00%


- **Q**: Berapa ukuran bendera universitas UNSRAT dan apa warna dasarnya?
- **R**: *Ukuran bendera Universitas Sam Ratulangi (UNSRAT) adalah lebar 160 cm x panjang 185 cm dengan warna dasar kuning.*
- *Overlap Score*: 55.56%


#### Sampel Kueri Potensi Semantic Bias (<=20% Overlap - Natural Language)

- **Q**: What activities are included in the research process standards under Pasal 81, and how must non-confidential research results be disseminated?
- **R**: *Kegiatan dalam Standar Proses Penelitian (Pasal 81)
Proses dan pengelolaan penelitian meliputi kegiatan:
 Perencanaan
 Pelaksanaan
 Penilaian
 Pengawasan
 Pengendalian penelitian

Penyebarluasan Hasil Penelitian yang Tidak Bersifat Rahasia
Hasil penelitian yang tidak bersifat rahasia, tidak mengganggu, dan/atau tidak membahayakan kepentingan umum atau nasional wajib disebarluaskan dengan cara:
 Diseminarkan
 Dipublikasikan
 Dipatenkan
 Dan/atau cara lain yang dapat digunakan untuk menyampaikan hasil penelitian kepada masyarakat*
- *Overlap Score*: 10.53%


- **Q**: klo sy nnti blajar trkait riset yg wajib ngacu k standar penelitian, mtd pembelajran apa aja yg bsa sy plih?
- **R**: *Metode pembelajaran yang dapat dipilih untuk pelaksanaan pembelajaran mata kuliah (termasuk proses pembelajaran yang terkait dengan penelitian mahasiswa yang wajib mengacu pada Standar Penelitian) meliputi:
1. Diskusi kelompok
2. Simulasi
3. Studi kasus
4. Pembelajaran kolaboratif
5. Pembelajaran kooperatif
6. Pembelajaran berbasis proyek
7. Pembelajaran berbasis masalah
8. Pembelajaran daring, atau
9. Metode pembelajaran lain yang dapat secara efektif memfasilitasi pemenuhan capaian pembelajaran lulusan.

Setiap mata kuliah dapat menggunakan satu atau gabungan dari beberapa metode pembelajaran tersebut.*
- *Overlap Score*: 16.67%



## 5. Metodologi & Rumus Perhitungan Overlap Leksikal

Untuk memvalidasi bias linguistik pada dataset evaluasi RAG, skrip ini menghitung persentase tumpang tindih leksikal murni antara kueri pengguna ($Q$) dan teks jawaban referensi ($R$).

**Formula Perhitungan Overlap:**
Teks kueri dan jawaban dibersihkan dari tanda baca, diturunkan case-nya menjadi lowercase, dan dipecah menjadi kumpulan kata (*set of words*). Overlap dihitung menggunakan rasio kueri terwakili:
$$\text{Lexical Overlap}(Q, R) = \frac{|Q_{\text{words}} \cap R_{\text{words}}|}{|Q_{\text{words}}|}$$

**Interpretasi Bias:**
- **Lexical Bias (> 50%)**: Pertanyaan cenderung menggunakan kata kunci yang sama persis dengan dokumen regulasi (memudahkan pencarian kata kunci/BM25).
- **Semantic Bias (<= 20%)**: Pertanyaan berupa parafrase atau kalimat tanya alami yang maknanya sama tetapi menggunakan kosa kata yang berbeda (menguji kekuatan pencarian vektor semantik).
