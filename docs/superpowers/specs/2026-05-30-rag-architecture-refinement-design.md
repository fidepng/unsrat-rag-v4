# Design Spec: RAG Architecture Refinement
**Tanggal:** 2026-05-30
**Sesi:** Socratic Design Refinement — Pra-Konstruksi
**Status:** ✅ Disetujui — Siap ke writing-plans

---

## Konteks

Dokumen ini merangkum keputusan arsitektur hasil sesi brainstorming (Socratic design
refinement) terhadap `prd_srs-v4.md` sebelum fase konstruksi dimulai. Semua perubahan
di bawah ini telah diaplikasikan langsung ke `prd_srs-v4.md` sebagai Single Source of
Truth.

---

## Keputusan yang Diambil

### D-B1 — Hapus Summary Chunk dari Pipeline Ingestion
**Masalah:** `retrieval_summary` di YAML frontmatter dibuat oleh AI tanpa review manusia.
Field ini digunakan untuk membuat "summary chunk" tambahan di ChromaDB dengan asumsi
meningkatkan recall — asumsi yang belum divalidasi secara empiris.

**Keputusan:** Hapus mekanisme summary chunk dari `ingestion.py`. Field `retrieval_summary`
diturunkan dari WAJIB ke opsional (catatan dokumentasi manusia saja).

**Justifikasi:** Corpus < 100 halaman dengan two-stage chunking yang sudah terstruktur
per-Pasal. Summary chunk yang tidak di-review manusia berisiko menurunkan kualitas
retrieval, bukan meningkatkannya. YAGNI: tidak ada bukti empiris manfaatnya.

**Dampak:** FR-04 dihapus. D-08 dicabut.

---

### D-B2 — Slim REQUIRED_YAML_FIELDS ke 3 Field
**Masalah:** `REQUIRED_YAML_FIELDS` memvalidasi 9 field, sebagian besar tidak dikonsumsi
oleh kode apapun saat runtime.

**Audit field:**
| Field | Dikonsumsi Kode | Keputusan |
|-------|----------------|-----------|
| `doc_id` | ✅ Chunk ID, citation panel | Tetap WAJIB |
| `title` | ✅ Citation panel | Tetap WAJIB |
| `category` | ✅ Error analysis | Tetap WAJIB |
| `content_type` | ❌ Disimpan tapi tidak dipakai | Turun ke opsional |
| `valid_from` | ❌ Tidak disimpan di ChromaDB | Turun ke opsional |
| `status` | ❌ Nilai tidak pernah dicek kode | Turun ke opsional |
| `retrieval_summary` | ❌ Dihapus (D-B1) | Turun ke opsional |
| `chunk_strategy` | ❌ Tidak dibaca runtime (D-A1) | Turun ke opsional |
| `last_updated` | ❌ Tidak disimpan di ChromaDB | Turun ke opsional |

**Keputusan:**
```python
REQUIRED_YAML_FIELDS = ["doc_id", "title", "category"]
```

**Justifikasi status:** File yang tidak aktif cukup dihapus dari `data/corpus/`. Semua
file yang ada di direktori tersebut dianggap aktif by convention. Tidak perlu enforcement
kode untuk corpus statis 10 file. (Complexity reduction.)

---

### D-B3 — Hapus `priority` dan `chunk_type` dari ChromaDB Metadata
**Masalah:** Kedua field ini disimpan ke ChromaDB tetapi tidak pernah dibaca oleh kode
retrieval, citation, atau evaluasi manapun.

- `priority`: tidak ada reranking, tidak ada pre-filter berdasarkan priority
- `chunk_type`: hanya relevan untuk summary chunk, yang sudah dihapus (D-B1)

**Keputusan:** Hapus keduanya dari schema metadata ChromaDB.

**ChromaDB metadata schema baru:**
```python
{
    "doc_id":       str,
    "title":        str,
    "category":     str,
    "content_type": str,
    "bab":          str,
    "bagian":       str,
    "pasal":        str,
    "chunk_id":     str,
    "status":       str,
}
```

---

### D-B4 — Hapus `/api/log_transaction` Endpoint
**Masalah:** Endpoint ini redundan. `chain.py` sudah memiliki akses ke semua data yang
dibutuhkan untuk logging (query, retrieved chunks, response, timing) dan `logger_manager`
sudah menangani ini. Endpoint terpisah berarti extra HTTP call dari frontend, dengan data
yang backend sudah miliki.

**Keputusan:** Hapus `POST /api/log_transaction`. Semua logging ke `transaksi_chat.csv`
dilakukan sepenuhnya di dalam `chain.py` via `logger_manager` setelah streaming selesai.

---

### D-B5 — Hapus `reinitialize_llm()`, Gunakan Stateless `_get_llm()`
**Masalah:** `reinitialize_llm(model_name)` memodifikasi objek LLM global di `chain.py`,
melanggar prinsip stateless backend yang sudah dideklarasikan di Section 6.7. Berpotensi
race condition meski sistem single-user lokal (relevan saat development/testing multi-tab).

**Keputusan:** Hapus `reinitialize_llm()`. Gunakan pattern stateless:

```python
_llm_cache: dict[str, Any] = {}

def _get_llm(model_name: str):
    """Kembalikan LLM instance untuk model tertentu. Cache per model name."""
    if model_name not in _llm_cache:
        _llm_cache[model_name] = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=LLM_TEMPERATURE,
            max_output_tokens=LLM_MAX_OUTPUT_TOKENS,
            top_p=LLM_TOP_P,
        )
    return _llm_cache[model_name]

def get_response(query, config, chat_history, model_name, streaming=False):
    llm = _get_llm(model_name)   # ← stateless, per-request
    ...
```

**Justifikasi:** Ini lebih *sederhana* dari desain sebelumnya (menghapus satu fungsi),
bukan lebih kompleks. Konsisten penuh dengan filosofi stateless backend.

---

### D-B6 — Ground Truth `reference`: Natural Language, Bukan Verbatim
**Masalah:** Format penulisan `reference` di `ground_truth.csv` tidak dispesifikasikan,
berpotensi bias pada metrik `context_recall`.

**Keputusan:** `reference` ditulis sebagai natural language answer dengan key facts
(angka, tanggal, kondisi edge case) — bukan copy-paste verbatim teks hukum dari dokumen.

**Contoh:**
```
# ❌ VERBATIM (terlalu mudah untuk context_recall)
"Beban studi mahasiswa per semester paling banyak 24 (dua puluh empat) SKS
sebagaimana diatur dalam Pasal 14 ayat (2)..."

# ✅ NATURAL LANGUAGE (mengukur semantic recall dengan benar)
"Mahasiswa dapat mengambil maksimum 24 SKS per semester. Namun jika IPS
semester sebelumnya di bawah 2.00, batas maksimalnya turun menjadi 18 SKS."
```

**Justifikasi:** Ragas `context_recall` mendekomposisi `reference` menjadi atomic claims
dan mengecek apakah retrieved contexts mengandungnya secara semantik. Reference yang
terlalu verbatim membuat metrik trivial; reference yang mengandung kondisi edge case
mengukur kemampuan retrieval yang sesungguhnya.

---

### D-B7 — Kalibrasi Empiris `SIMILARITY_THRESHOLD` Sebelum Evaluasi Resmi
**Masalah:** Nilai `SIMILARITY_THRESHOLD = 0.65` dipilih berdasarkan rekomendasi AI
tanpa validasi empiris. Parameter ini menentukan apakah sistem menjawab atau diam
(fallback) — tidak ada justifikasi metodologis.

**Keputusan:** Tambahkan step kalibrasi empiris sebagai bagian dari metodologi
(Bab III), bukan sebagai sensitivity analysis tersendiri.

**Prosedur (±30 menit, sekali sebelum evaluasi resmi):**
1. Jalankan 10 query sampel: 5 yang jelas relevan, 5 yang jelas tidak relevan
2. Catat cosine distance yang dikembalikan ChromaDB untuk setiap query
3. Verifikasi bahwa ada gap yang jelas antara dua kelompok distance
4. Sesuaikan nilai threshold jika gap tidak terlihat; catat hasilnya
5. Dokumentasikan di Bab III dengan kalimat: *"Parameter similarity threshold
   dikalibrasi secara empiris menggunakan 10 query sampel sebelum evaluasi utama..."*

**Bukan:** Sensitivity analysis (uji 6+ nilai threshold) — ini di luar scope penelitian.

---

## Yang TIDAK Diubah (Keputusan Dipertahankan)

| Keputusan | Alasan Dipertahankan |
|-----------|---------------------|
| k=4, cosine distance | Reasonable default; akan divalidasi via kalibrasi threshold |
| Two-stage chunking | Best practice untuk corpus Markdown terstruktur |
| Wilcoxon hanya A vs B | Config C adalah baseline deskriptif, bukan hipotesis inferensial |
| BM25 chunk_size = Config B | Fair comparison metodologi (D-A3) |
| Stateless frontend history | Sudah benar (D-A12) |
| Tiktoken cl100k_base | Estimasi yang cukup akurat untuk Gemini; overhead 0ms |
| max_workers=1 di Ragas | Trade-off stabilitas vs kecepatan yang disengaja |

---

## Dampak pada Dokumen

Semua perubahan code-critical (D-B1 s/d D-B5) telah diaplikasikan ke `prd_srs-v4.md`.
D-B6 dan D-B7 didokumentasikan di Section 9.1 dan Section 12.2b PRD.
