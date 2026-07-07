# Ragas v0.4 Evaluation Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the evaluation pipeline to support Ragas v0.4 `EvaluationDataset`, create a synthetic testset generator using Gemini 2.5 Flash, and expand the curated ground truth dataset.

**Architecture:** 
1. `generate_testset.py` will read markdown files using `frontmatter`, create Langchain `Document` objects, and use Ragas' `TestsetGenerator` to create synthetic evaluation questions.
2. `evaluation.py` will be modified to drop Hugging Face `Dataset` and instead construct a list of `SingleTurnSample` objects to feed into `EvaluationDataset` as required by Ragas v0.4.
3. The `ground_truth.csv` file will be expanded manually by appending 15 high-quality QA pairs to better cover academic and FAQ categories.

**Tech Stack:** Python, Ragas v0.4, Langchain, Google Generative AI (Gemini 2.5 Flash).

---

### Task 1: Create Synthetic Test Generator

**Files:**
- Create: `scripts/generate_testset.py`

- [ ] **Step 1: Write the generation script**

Create `scripts/generate_testset.py` with the following implementation:

```python
import os
from pathlib import Path
from dotenv import load_dotenv
import frontmatter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from ragas.testset.generator import TestsetGenerator

# Ensure API key is loaded explicitly
env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def generate_synthetic_data():
    print("Initializing LLMs...")
    generator_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    critic_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    print("Initializing TestsetGenerator...")
    generator = TestsetGenerator.from_langchain(
        generator_llm=generator_llm,
        critic_llm=critic_llm,
        embeddings=embeddings
    )
    
    # Read corpus
    corpus_dir = Path("data/corpus")
    docs = []
    
    if not corpus_dir.exists():
        print(f"Error: {corpus_dir} does not exist. Please run from project root.")
        return

    for md_file in corpus_dir.glob("*.md"):
        post = frontmatter.load(md_file)
        docs.append(Document(page_content=post.content, metadata=post.metadata))
        
    print(f"Loaded {len(docs)} documents from corpus.")
    
    # Generate testset (test_size can be adjusted)
    print("Generating synthetic testset. This may take a while...")
    testset = generator.generate_with_langchain_docs(docs, test_size=10)
    
    # Save output
    output_path = Path("eval/dataset/synthetic_testset.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = testset.to_pandas()
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic testset saved to {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
```

- [ ] **Step 2: Commit**

```bash
git add scripts/generate_testset.py
git commit -m "feat: add synthetic testset generator using Ragas v0.4"
```

---

### Task 2: Expand Curated Ground Truth Dataset

**Files:**
- Modify: `eval/dataset/ground_truth.csv`

- [ ] **Step 1: Append 15 new questions to ground truth**

Append the following 15 lines to the end of `eval/dataset/ground_truth.csv`:

```csv
Apa tujuan utama pelaksanaan KKT di Unsrat?,"Kuliah Kerja Terpadu (KKT) bertujuan memberikan pengalaman pengabdian kepada masyarakat, melatih mahasiswa memecahkan masalah di lapangan secara lintas sektoral, dan membangun empati terhadap masyarakat.",academic,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Pasal 55 (1)
Siapa yang bertugas sebagai pembimbing KKT?,"Dosen Pembimbing Lapangan (DPL) yang ditunjuk oleh Rektor bertugas membimbing, memantau, dan mengevaluasi pelaksanaan KKT mahasiswa.",academic,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Pasal 55 (3)
Bagaimana prosedur pendaftaran wisuda bagi mahasiswa yang telah lulus ujian skripsi?,"Mahasiswa yang telah dinyatakan lulus ujian akhir program studi dan yudisium harus mendaftar wisuda melalui portal INSPIRE paling lambat dua minggu sebelum pelaksanaan wisuda.",academic,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Pasal 69 (2)
Berapa nilai minimal kelulusan untuk mata kuliah skripsi/tugas akhir?,"Nilai kelulusan minimum untuk ujian tugas akhir/skripsi pada program sarjana adalah C.",academic,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Pasal 67 (3)
Apakah mahasiswa pindahan dari universitas lain bisa diakui masa studinya?,"Ya, masa studi yang telah ditempuh di perguruan tinggi asal akan diperhitungkan dalam batas maksimal masa studi di UNSRAT berdasarkan hasil konversi SKS.",academic,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Pasal 19 (4)
Apakah diperbolehkan mengganti dosen pembimbing skripsi di tengah proses bimbingan?,"Penggantian dosen pembimbing dapat dilakukan dengan alasan yang dapat dipertanggungjawabkan melalui usulan Koordinator Program Studi dan persetujuan Dekan/Direktur.",academic,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Pasal 65 (5)
Kapan perkuliahan semester ganjil tahun akademik 2026/2027 dimulai?,Perkuliahan semester ganjil 2026/2027 direncanakan akan dimulai pada awal bulan Agustus 2026 berdasarkan kalender akademik tahunan.,calendar,Kalender_Akademik_UNSRAT_Genap_2025-2026.md,Proyeksi Ganjil
Kapan batas akhir pembayaran UKT untuk mahasiswa lama pada semester genap?,Batas akhir pembayaran UKT untuk semester genap tahun 2025/2026 adalah tanggal 31 Januari 2026.,calendar,Kalender_Akademik_UNSRAT_Genap_2025-2026.md,Jadwal UKT
Siapa rektor Universitas Sam Ratulangi saat ini?,Prof. Dr. Ir. Oktovian Berty Alexander Sompie M.Eng. IPU. ASEAN Eng. adalah Rektor Universitas Sam Ratulangi untuk periode berjalan.,institution_profile,01_sejarah.md,Rektor Saat Ini
Berapa jumlah fakultas yang ada di Universitas Sam Ratulangi?,"Universitas Sam Ratulangi saat ini memiliki 11 Fakultas, antara lain Kedokteran, Teknik, Pertanian, Peternakan, Perikanan dan Ilmu Kelautan, Ekonomi dan Bisnis, Hukum, Ilmu Sosial dan Ilmu Politik, Ilmu Budaya, MIPA, serta Kesehatan Masyarakat.",institution_profile,03_fakultas.md,Daftar Fakultas
Apa tugas pokok unit LPPM di UNSRAT?,"Lembaga Penelitian dan Pengabdian kepada Masyarakat (LPPM) bertugas mengoordinasikan, memantau, dan menilai pelaksanaan kegiatan penelitian dan pengabdian kepada masyarakat oleh civitas akademika.",institution_profile,05_lembaga.md,Tugas LPPM
Dimana alamat kampus utama Universitas Sam Ratulangi?,"Kampus utama Universitas Sam Ratulangi berlokasi di Jl. Kampus Unsrat Bahu, Kota Manado, Sulawesi Utara.",institution_profile,01_sejarah.md,Lokasi Kampus
Apakah mahasiswa bisa mencicil pembayaran UKT jika mengalami kesulitan keuangan?,"Pembayaran UKT pada dasarnya dibayarkan lunas, namun dalam kondisi khusus mahasiswa dapat mengajukan permohonan keringanan atau penundaan melalui prosedur resmi yang disetujui pimpinan fakultas/universitas.",faq,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Kebijakan UKT
Bagaimana cara mendapatkan transkrip nilai resmi dari fakultas?,"Mahasiswa dapat mengunduh transkrip sementara melalui INSPIRE, namun untuk transkrip resmi bertanda tangan harus diajukan permohonannya melalui bagian akademik fakultas.",faq,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Layanan Akademik
Apa sanksi jika terbukti melakukan plagiarisme pada skripsi?,"Mahasiswa yang terbukti melakukan plagiarisme akan dikenakan sanksi akademik berat, yang dapat berupa pembatalan kelulusan, pencabutan ijazah, hingga pemberhentian tidak hormat (drop out).",faq,Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md,Sanksi Plagiarisme
```

- [ ] **Step 2: Commit**

```bash
git add eval/dataset/ground_truth.csv
git commit -m "feat: add 15 new manually curated questions to ground truth"
```

---

### Task 3: Refactor Evaluation Script for Ragas v0.4

**Files:**
- Modify: `evaluation.py`

- [ ] **Step 1: Replace dataset building logic in evaluation.py**

In `evaluation.py`, replace the `try/except` block and preceding variable declaration that converts `results` into the HF dataset (around line 364 to 445):

```python
<<<<
        # Bangun dataset untuk Ragas
        eval_data = {
            "question":           [r["user_input"]           for r in results],
            "answer":             [r["response"]             for r in results],
            "contexts":           [r["retrieved_contexts"]   for r in results],
            "ground_truth":       [r["reference"]            for r in results],
        }

        # Konfigurasi sequential untuk stabilitas (Section 12.2)
        run_config = RunConfig(max_workers=1, timeout=300, max_retries=10)

        # Metrik yang dijalankan
====
        # Konfigurasi sequential untuk stabilitas (Section 12.2)
        run_config = RunConfig(max_workers=1, timeout=300, max_retries=10)

        # Metrik yang dijalankan
>>>>
```
and then replace the specific execution logic in `evaluation.py` at line 431:

```python
<<<<
        try:
            from datasets import Dataset
            ragas_dataset = Dataset.from_dict(eval_data)

            ragas_result = evaluate(
                dataset=ragas_dataset,
                metrics=base_metrics,
                run_config=run_config,
            )
            ragas_df = ragas_result.to_pandas()
        except Exception as e:
            logger.error(f"Ragas evaluate() gagal: {e}")
            logger.error("Jalankan `use context7` untuk verifikasi API Ragas yang terinstall.")
            raise
====
        try:
            from ragas import EvaluationDataset, SingleTurnSample
            
            samples = []
            for r in results:
                sample = SingleTurnSample(
                    user_input=r["user_input"],
                    response=r["response"],
                    retrieved_contexts=r["retrieved_contexts"],
                    reference=r["reference"]
                )
                samples.append(sample)
                
            ragas_dataset = EvaluationDataset(samples=samples)

            ragas_result = evaluate(
                dataset=ragas_dataset,
                metrics=base_metrics,
                run_config=run_config,
            )
            ragas_df = ragas_result.to_pandas()
        except Exception as e:
            logger.error(f"Ragas evaluate() gagal: {e}")
            logger.error("Pastikan Ragas v0.4 terpasang. Error detail di atas.")
            raise
>>>>
```

- [ ] **Step 2: Commit**

```bash
git add evaluation.py
git commit -m "refactor: update evaluate() to use Ragas v0.4 EvaluationDataset"
```
