---
doc_id: "UNSRAT-PROFILE-2020-005"
title: "Bendera Universitas Sam Ratulangi"
version: "1.2"
language_primary: "id"
language_secondary: null
institution: "Universitas Sam Ratulangi"
unit_penerbit: "Humas UNSRAT"

content_type: "narrative"
category: "institution_profile"
subcategory:
  - "bendera"
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
source_url: "https://www.unsrat.ac.id/profil-unversitas/"
supersedes: null
superseded_by: null

valid_from: null
valid_until: null
status: "active"
last_updated: "2026-07-22"
last_verified: "2026-07-22"

retrieval_summary: "Dokumen narasi profil institusi ini mendeskripsikan spesifikasi resmi bendera Universitas Sam Ratulangi (UNSRAT) di tingkat universitas maupun fakultas. Bendera universitas berukuran 160x185 cm berwarna dasar kuning, sementara bendera fakultas berukuran 90x130 cm dengan warna khas masing-masing. Dokumen memuat tabel lengkap 11 warna bendera spesifik untuk setiap fakultas dan Program Pascasarjana di lingkungan UNSRAT, mulai dari Hijau Tua (Kedokteran) hingga Coklat Muda (Pascasarjana)."

chunk_strategy: "by_section"
chunk_notes: "Potong per heading ## (Bendera Universitas, Bendera Fakultas dan Program Pascasarjana). Tabel 'Warna Bendera Per Fakultas' berukuran kecil (~500+ karakter dengan catatan disclosure, 11 baris) sehingga aman berada dalam satu chunk utuh tanpa risiko terpotong RecursiveCharacterTextSplitter (chunk_size=2000); dipertahankan sebagai tabel (bukan list) karena data bersifat tabular murni (1 fakultas -> 1 warna). PERBAIKAN v1.2 (re-verification 22 Juli 2026): ditambahkan catatan disclosure eksplisit bahwa baris ke-8 tabel ('Ilmu Pendidikan') tidak konsisten dengan nama fakultas di UNSRAT-PROFILE-2026-001 ('Ilmu Politik') — keduanya dipertahankan verbatim sesuai bagian sumber masing-masing, inkonsistensi didisclose bukan disilent-fix."
embedding_model: "text-embedding-001"
priority: 4

related_docs:
  - "UNSRAT-PROFILE-2020-004"

tags:
  - bendera
  - atribut_kampus
  - warna_fakultas
  - identitas_visual
  - profil_institusi

keywords:
  - "Bendera UNSRAT"
  - "Warna Bendera Fakultas"
  - "Ukuran Bendera UNSRAT"
  - "bendera kuning"
  - "Fakultas Kedokteran"
  - "Fakultas Teknik"
  - "Fakultas Pertanian"
  - "Fakultas Peternakan"
  - "Fakultas Perikanan"
  - "Fakultas Ekonomi"
  - "Fakultas Hukum"
  - "Fakultas Sastra"
  - "FMIPA"
  - "Program Pascasarjana"

entities:
  - "Universitas Sam Ratulangi"
  - "UNSRAT"
  - "Fakultas Kedokteran"
  - "Fakultas Teknik"
  - "Fakultas Pertanian"
  - "Fakultas Peternakan"
  - "Fakultas Perikanan dan Ilmu Kelautan"
  - "Fakultas Ekonomi"
  - "Fakultas Hukum"
  - "Fakultas Ilmu Sosial dan Ilmu Pendidikan"
  - "Fakultas Sastra"
  - "Fakultas Matematika dan Ilmu Pengetahuan Alam"
  - "Program Pascasarjana"
---

# Bendera Universitas Sam Ratulangi

> Referensi gambar bendera: https://www.unsrat.ac.id/wp-content/uploads/2020/11/bendera_UNSRAT.jpg

---

## Bendera Universitas

Bendera UNSRAT berbentuk **empat persegi** dengan spesifikasi berikut:

- **Ukuran:** Lebar 160 cm x Panjang 185 cm
- **Warna dasar:** Kuning
- **Tengah:** Terdapat lambang universitas

---

## Bendera Fakultas dan Program Pascasarjana

Bendera fakultas dan program pascasarjana berbentuk **empat persegi** dengan spesifikasi:

- **Ukuran:** Lebar 90 cm x Panjang 130 cm
- **Tengah:** Terdapat lambang fakultas atau program pascasarjana yang bersangkutan

### Warna Bendera Per Fakultas

| No  | Fakultas                                      | Warna Bendera |
| -----| -----------------------------------------------| ---------------|
| 1   | Fakultas Kedokteran                           | Hijau Tua     |
| 2   | Fakultas Teknik                               | Biru Tua      |
| 3   | Fakultas Pertanian                            | Hijau Muda    |
| 4   | Fakultas Peternakan                           | Coklat        |
| 5   | Fakultas Perikanan dan Ilmu Kelautan          | Biru Muda     |
| 6   | Fakultas Ekonomi                              | Kelabu        |
| 7   | Fakultas Hukum                                | Merah         |
| 8   | Fakultas Ilmu Sosial dan Ilmu Pendidikan      | Jingga        |
| 9   | Fakultas Sastra                               | Ungu          |
| 10  | Fakultas Matematika dan Ilmu Pengetahuan Alam | Putih         |
| 11  | Program Pascasarjana                          | Coklat Muda   |

> **Catatan disclosure — inkonsistensi penamaan pada sumber resmi:** baris ke-8 di atas ditulis persis sesuai sumber sebagai **"Fakultas Ilmu Sosial dan Ilmu Pendidikan"**. Namun pada dokumen Sejarah (`UNSRAT-PROFILE-2026-001`), fakultas yang sama disebut **"Fakultas Ilmu Sosial dan Ilmu Politik"** (FISIP) — sesuai nama resmi fakultas yang berlaku saat ini. Inkonsistensi ini ADA PADA SUMBER RESMI ITU SENDIRI (dua bagian berbeda dari halaman yang sama, kemungkinan typo lama yang tak pernah diperbaiki), bukan kesalahan transkripsi dokumen ini. Baris tabel di atas dipertahankan verbatim demi kesetiaan sumber; untuk pertanyaan RAG mengenai nama resmi fakultas, rujuk ke `UNSRAT-PROFILE-2026-001` (Ilmu Politik) sebagai yang lebih konsisten dengan penamaan fakultas resmi saat ini.