---
doc_id: "UNSRAT-PROFILE-2020-004"
title: "Lambang Universitas Sam Ratulangi"
version: "1.2"
language_primary: "id"
language_secondary: null
institution: "Universitas Sam Ratulangi"
unit_penerbit: "Humas UNSRAT"

content_type: "narrative"
category: "institution_profile"
subcategory:
  - "lambang"
  - "identitas_visual"
audience:
  - "publik"
  - "mahasiswa_s1"
  - "mahasiswa_s2"
  - "mahasiswa_s3"
  - "mahasiswa_profesi"
  - "dosen"
  - "tendik"
  - "pimpinan"
access_level: "public"

nomor_sk: null
tanggal_penetapan: null
pejabat_penandatangan: null
source_document: null
source_url: "https://www.unsrat.ac.id/profil-unversitas/#1605173171703-2c418561-d17d"
supersedes: null
superseded_by: null

valid_from: null
valid_until: null
status: "active"
last_updated: "2026-07-22"
last_verified: "2026-07-22"

retrieval_summary: "Dokumen narasi profil institusi ini menguraikan arti, makna filosofis, dan tata cara penggunaan lambang resmi Universitas Sam Ratulangi (UNSRAT). Elemen visual lambang terdiri dari bidang dasar segi lima yang melambangkan Pancasila, serta bulatan tengah berisi lukisan pohon kelapa dengan 12 elemen bermakna yang merepresentasikan Tridharma Perguruan Tinggi, semangat Proklamasi Kemerdekaan 17 Agustus 1945, dan identitas daerah Sulawesi Utara. Dokumen juga mengatur ketentuan penempatan lambang pada atribut dan ruang resmi universitas."

chunk_strategy: "by_section"
chunk_notes: "Potong per heading ## / ### (Arti Lambang, Makna Lambang > Bidang Dasar, Makna Lambang > Bulatan Tengah, Makna Keseluruhan, Penggunaan Lambang). PERUBAHAN v1.1: 12 elemen 'Bulatan Tengah (Lambang Kelapa)' diubah dari tabel 2 kolom (No/Elemen/Makna) menjadi list bernomor '**Elemen N** — deskripsi elemen. Makna: penjelasan.' Alasan: versi tabel v1.0 berukuran ~3600 karakter untuk satu section — jauh melebihi chunk_size=2000, sehingga RecursiveCharacterTextSplitter memotongnya menjadi 2 chunk dan baris ke-4 s.d. ke-12 kehilangan header kolom 'No | Elemen | Makna' (chunk yatim, konteks tak terbaca LLM). Format list baru membuat setiap elemen sepenuhnya self-contained (elemen + makna dalam satu blok teks), sehingga aman dipotong di titik manapun oleh splitter tanpa kehilangan konteks. PERBAIKAN v1.2 (re-verification 22 Juli 2026 terhadap HTML sumber resmi): ditemukan 3 silent-edit pada v1.1 yang mengubah ejaan asli tanpa disclosure ('distilir' vs sumber 'distylir'; 'l'esprit des corps' vs sumber 'l'espirit des corps'; 'instituendum et scolarium' vs sumber 'menginstorum et scolarium') — SEMUA dikembalikan verbatim ke ejaan sumber dan didisclose via footnote [^ejaan-asli] di akhir dokumen, sesuai kebijakan anti-silent-edit di RAG_VALIDATION_CONTEXT.md. Satu koreksi ejaan yang memang disengaja ('tjujuan'->'tujuan', 'pengadan'->'pengadaan') tetap dipertahankan tapi kini didisclose eksplisit via footnote [^koreksi-tujuan]."
embedding_model: "text-embedding-001"
priority: 4

related_docs:
  - "UNSRAT-PROFILE-2026-001"
  - "UNSRAT-PROFILE-2020-005"
  - "UNSRAT-PROFILE-2020-006"

tags:
  - lambang
  - logo
  - identitas_visual
  - profil_institusi
  - pancasila
  - tridharma_pt
  - filosofi

keywords:
  - "Lambang UNSRAT"
  - "Logo UNSRAT"
  - "Makna Lambang"
  - "Arti Lambang UNSRAT"
  - "Pohon Kelapa"
  - "Warna Lila"
  - "Atribut UNSRAT"
  - "Proklamasi 1945"
  - "Dies Natalis"
  - "segi lima"

entities:
  - "Universitas Sam Ratulangi"
  - "UNSRAT"
  - "Pancasila"
  - "UUD 1945"
---

# Lambang Universitas Sam Ratulangi

> Referensi gambar lambang: https://www.unsrat.ac.id/wp-content/uploads/2020/11/logo_unsrat_large.jpg

---

## Arti Lambang

Lambang UNSRAT memiliki tiga elemen visual utama:

1. **Bentuk dan wajah bilangannya berwarna kelabu** — menjadi dasar bagi lukisan ciri khas serta nama lambang yang tertera di atasnya.
2. **Nama yang melingkari lukisan (sebagai fokus)** — berwarna biru dan berada di antara dua lembaga berwarna lila. Keseluruhannya mempunyai hubungan timbal balik dengan dasar dan isi lukisan, serta menggambarkan struktur yang hidup, dinamis, utuh, bulat, dan lengkap.
3. **Lukisan di tengah** — berupa kelapa berwarna lila dan merah, tersusun dalam satu bulatan yang utuh merupakan satu ciri khas, yang bermakna proses pertumbuhan dan perkembangan.

---

## Makna Lambang

### Bidang Dasar

- **Bidang dasar segi lima** merupakan lambang Pancasila.
- **Warna kelabu** melambangkan nilai-nilai luhur Pancasila yang menjadi tugas UNSRAT sebagai:
  1. Penggali dan pencari kebenaran,
  2. Pengenal dan penerus kebenaran untuk dunia sekitarnya, dan
  3. Pembela dan pelindung kebenaran.

### Bulatan Tengah (Lambang Kelapa)

Bulatan berisi lukisan di tengah berasal dari ciri khas yang terdapat di daerah Sulawesi Utara, dengan makna sebagai berikut:

- **Elemen 1 — Satu biji kelapa dengan tiga matanya menghadap ke bawah** (tempat keluarnya akar lembaga), melambangkan UNSRAT sebagai suatu lembaga pendidikan tinggi yang melaksanakan Tridharma Perguruan Tinggi berdasarkan Pancasila di bumi Indonesia.
- **Elemen 2 — Warna lila pada bagian-bagian kelapa yang distylir**[^ejaan-asli] melambangkan warna kebudayaan yang hidup, bertumbuh, dan berkembang.
- **Elemen 3 — Warna merah pada bakal-bakal buah yang sedang tumbuh serta buah yang telah matang dan dapat dipetik,** melambangkan hasil proses pertumbuhan yang sedang disiapkan dan siap untuk digunakan dalam fungsi sosial.
- **Elemen 4 — Bagian-bagian kelapa yang mencuat berbentuk tangkai halus berwarna lila, saling berhubungan satu sama lain,** melambangkan semangat kekeluargaan (_l'espirit des corps_)[^ejaan-asli] dalam sivitas akademika.
- **Elemen 5 — Sepasang seludang berwarna lila yang melindungi bakal-bakal buah,** melambangkan dalam rangka melaksanakan Tridharma Perguruan Tinggi, UNSRAT memiliki tugas: _menginstorum et scolarium_ dan _scientiarum_.[^ejaan-asli]
- **Elemen 6 — 17 bakal buah berwarna merah, 8 ruas pada batang kelapa berwarna lila, 9 pelepah berwarna ungu (masing-masing memiliki 5 helai daun),** melambangkan dalam menjalankan tugasnya Unsrat dijiwai dan diisi oleh semangat Proklamasi Kemerdekaan Indonesia 17 Agustus 1945.
- **Elemen 7 — Tiga pelepah kelapa berwarna lila,** melambangkan tugas dan falsafah perguruan tinggi dalam bentuk Tridharma Perguruan Tinggi.
- **Elemen 8 — Dua pasang seludang berwarna lila di kiri-kanan ketiga pelepah,** melambangkan proses _"patah tumbuh hilang berganti"_.
- **Elemen 9 — Sembilan bagian lukisan berwarna lila di sekitar pohon kelapa,** melambangkan bulan September sebagai Dies Natalis UNSRAT.
- **Elemen 10 — Satu pelepah kelapa menghadap ke atas yang sedang terbuka (mekar) kelima helai daunnya,** melambangkan UNSRAT dijiwai semangat Proklamasi Kemerdekaan Indonesia 17 Agustus 1945 untuk terus berupaya mencapai tujuan dan cita-cita bangsa Indonesia merdeka.
- **Elemen 11 — Nama dan tempat universitas berwarna biru,** melambangkan fakta hidup, landasan teguh, pasti, dan dinamis.
- **Elemen 12 — Lembaga-lembaga kelapa berwarna lila di antara nama dan tempat universitas,** melambangkan bahwa UNSRAT yang memulai kegiatannya di Manado, terus akan hidup sebagai universitas yang menjadi milik dan dapat dimanfaatkan oleh seluruh rakyat dan bangsa Indonesia.

> Catatan: Istilah **"distylir"**, **"l'espirit des corps"**, dan **"menginstorum et scolarium"** DIPERTAHANKAN PERSIS sesuai ejaan pada sumber resmi (www.unsrat.ac.id/profil-unversitas/), meskipun tampak seperti ejaan tidak baku (kemungkinan "distilir", "l'esprit de corps", dan istilah Latin heraldik yang sudah usang). Karena tidak ada dokumen otoritatif lain (mis. SK penetapan lambang tahun 1965) yang bisa dijadikan rujukan koreksi, istilah ini TIDAK dikoreksi dan dipertahankan verbatim untuk menghindari asumsi/halusinasi makna.

### Makna Keseluruhan

Makna lambang secara keseluruhan menggambarkan **kepribadian, cita-cita, tugas, dan kewajiban UNSRAT** sebagai alat dan abdi yang berusaha mencapai tujuan sesuai cita-cita perjuangan nasional bangsa Indonesia sebagaimana tercantum dalam Pembukaan UUD 1945, termasuk:

- Usaha mencerdaskan kehidupan bangsa,
- Memajukan pengembangan ilmu pengetahuan dan teknologi,
- Pengembangan kebudayaan, serta
- Pengolahan sumberdaya alam,

...dalam rangka kemakmuran dan kesejahteraan bangsa Indonesia pada umumnya serta rakyat dan daerah Sulawesi Utara pada khususnya.

---

## Penggunaan Lambang

Penggunaan dan tatacara lambang UNSRAT diatur menurut ketentuan tersendiri melalui peraturan khusus universitas. Dengan memperhatikan lambang tersebut, maka pembuatan / pengadan dan penempatannya disesuaikan dengan jenis dan tingkat kebutuhan penggunaan tersebut. Beberapa hal dikemukakan disini sebagai contoh, ukuran kecil besar dengan dasar perbandingan yang sama dalam hal pembuatannya, menetap tidaknya dalam hal penempatan misalnya di ruang Rektor, Kantor Pusat, Auditorium, ruang Dekan, Stempel / Cap, Kalung Jabatan, Tropi, Gordon, dokumen-dokumen tertulis, cetakan, ijasah, sertifikat, piagam, dan lain sebagainya, sepanjang yang menyangkut jenis atribut dengan menggunakan lambang Universitas Sam Ratulangi.