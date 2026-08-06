# Laporan Hasil Analisis Validasi Empiris Ukuran Chunk
**Tujuan Pembentukan:** Bukti perhitungan objektif (berdasarkan data historis/korpus aktual) untuk merevisi **Bab 4.1.2 Validasi Empiris Ukuran Chunk** dalam penulisan laporan Skripsi.

---

## 1. Metodologi Perhitungan

Penghitungan statistik panjang *chunk* ini dilakukan pada **Tahap 1 Pemisahan (Struktural)**. Hal ini dilakukan untuk mengukur panjang natural dari masing-masing ayat/pasal sebelum mekanisme pemotongan paksa berdasarkan karakter (Tahap 2) diterapkan.

### 1.1 Komponen yang Digunakan
1. **Target Data**: Seluruh file Markdown dokumen regulasi yang berada di direktori `data/corpus/`.
2. **Library**: 
   - `langchain_text_splitters.MarkdownHeaderTextSplitter` (Untuk memecah teks mengikuti hierarki heading Markdown secara akurat).
   - `numpy` (Untuk ekstraksi matriks statistik seperti rata-rata, persentil, min, dan max).
   - `frontmatter` (Untuk mengurai metadata YAML dan mengambil isi/body murni dokumen).
3. **Filter**: *Section* dengan panjang kurang dari 50 karakter (sebagaimana didefinisikan oleh `MIN_CHUNK_LENGTH` di `src/config.py`) dieksklusi untuk menghindari noise berupa header kosong.

### 1.2 Skrip Eksekusi (Source of Truth)
Skrip perhitungan dapat ditemukan di `scripts/analyze_chunks.py`. Skrip ini mereplikasi secara parsial alur pemisahan di dalam file `src/ingestion.py` (`_parse_and_chunk`) untuk menjamin konsistensi logika pembagian teks, lalu menerapkan perhitungan *array numpy* terhadap jumlah karakter tiap *section*.

Skrip akan mengekspor luaran akhirnya secara otomatis ke file `docs/statistik_chunk_analisis.json`.

---

## 2. Hasil Eksekusi dan Data Statistik

Berikut adalah hasil eksekusi perhitungan terbaru setelah korpus mengalami pembersihan:

**Tabel 4.3. Statistik Deskriptif Panjang Section Dokumen Korpus**

| METRIK                       | NILAI TERUKUR    |
| :-----------------------------| :-----------------|
| Total *Section*              | 161 *section*    |
| Panjang Minimum              | 60 karakter      |
| Rata-rata (Mean)             | 1.162,3 karakter |
| Median (Persentil ke-50)     | 830,0 karakter   |
| Persentil ke-75              | 1.348,0 karakter |
| Persentil ke-90              | 1.900,0 karakter |
| Persentil ke-95              | 2.617,0 karakter |
| Persentil ke-99              | 7.414,0 karakter |
| Panjang Maksimum (*Outlier*) | 15.599 karakter  |

### 2.1 Analisis Outlier (Nilai Maksimum)
*Outlier* dengan panjang ekstrem 15.599 karakter adalah **Pasal 1** dari file `Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md`. Pasal ini berisi format daftar/tabel kompleks yang mendefinisikan 77 istilah akademik berbeda dalam satu blok *section* tunggal.

Jika nilai outlier ekstrem tersebut dikecualikan dari array perhitungan (karena merusak visualisasi distribusi), **rata-rata (*mean*) sesungguhnya akan turun dari 1.162,3 menjadi 1.072,0 karakter.** Hal ini mengonfirmasi sifat data regulasi yang sangat *positively skewed* (condong ke kanan).

---

## 3. Justifikasi Ilmiah untuk Laporan (Draft Narasi)

Berdasarkan data di atas, berikut adalah draf narasi yang dapat digunakan dalam laporan Anda untuk menjustifikasi pemilihan angka **2.000 karakter** (sebagai `CHUNK_SIZE` Tahap 2):

> "Distribusi persentil dari 161 *section* korpus mengonfirmasi bahwa penetapan batas maksimal **2.000 karakter** merupakan keputusan desain sistem yang sangat optimal. Data menunjukkan nilai persentil ke-90 berada pada rentang angka **1.900,0 karakter**. Artinya, batas maksimal 2.000 karakter secara matematis mengamankan **91,93%** *section* struktural (148 dari 161 *section*) untuk dipertahankan secara utuh tanpa terpotong di tengah kalimat atau penjelasan."

> "Langkah mempertahankan keutuhan hierarki *section* ini krusial pada domain dokumen hukum demi menjaga ikatan konteks dan rujukan silang (cross-reference) antar-ayat tetap berada di dalam satu *chunk* *embedding* yang sama. Untuk menangani sisa **8,07%** *section* berukuran *outlier* (seperti Pasal 1 yang memuat 77 definisi istilah dengan total 15.599 karakter), sistem mengandalkan mekanisme pemisahan Tahap 2 yang menggunakan `RecursiveCharacterTextSplitter`. Pendekatan lapis kedua ini memastikan pemotongan teks panjang berukuran tidak wajar tetap jatuh pada batas blok (paragraf/tanda baca) terdekat, yang meminimalkan kerugian semantik akibat *chunking*."

---

## 4. Cara Mereproduksi (Reproducibility)
Gunakan perintah ini di root direktori proyek jika ada perubahan data di masa depan dan angka perlu dihitung ulang:
```bash
python scripts/analyze_chunks.py --source-only
```
Output dapat dilihat langsung pada konsol terminal dan akan disimpan secara rapi di dalam file JSON `docs/statistik_chunk_analisis.json`.
