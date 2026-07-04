# Design Specification: Redesign of RAG Chatbot Evaluation (Config B vs Config C)

**Date:** 2026-07-04  
**Topic:** Redesign of RAG Evaluation Methodology and Ground Truth dataset for UNSRAT RAG.  
**Context:** Thesis/Skripsi on RAG Chatbot Implementation and Evaluation at Sam Ratulangi University.

---

## 1. Background and Identified Flaws

During the initial evaluation of the UNSRAT RAG system, the evaluation scores of **Config B (Vector Search)** and **Config C (BM25 Search)** were found to be very close, with BM25 paradoxically showing higher *Faithfulness* (0.6615 vs 0.6197). An in-depth error analysis revealed two structural flaws in the evaluation setup:

1. **Ragas Evaluation Bias on Empty Contexts (Fallback Bias):**
   * Config B employs a `SIMILARITY_THRESHOLD = 0.3`. When queries are Out-of-Domain (OOD), no chunks pass this threshold, returning an empty context list (`[]`).
   * For empty contexts, the RAG chain directly outputs the hardcoded `FALLBACK_RESPONSE`, which contained positive claims (links to Portal INSPIRE, contact info for Academic Dept and Rektorat).
   * Ragas Faithfulness calculates the proportion of claims in the response supported by the retrieved contexts. Since the context is empty, the fallback links are flagged as unsupported ("hallucinated"), penalizing Config B with a faithfulness score of `0.20 - 0.25`.
   * Config C (BM25) has no threshold, always retrieving some chunks. The LLM is called, realizes the context is irrelevant, and generates a custom "not found" response. Because it contains no positive claims, Ragas rates it as `1.00` in faithfulness, artificially boosting BM25's score.
   
2. **Colloquial Gap (Dialect Mismatch):**
   * The ground truth dataset contained queries in local Manado dialect (slang), whereas the corpus is written in formal, legalistic Bahasa Indonesia.
   * Standard embedding models and BM25 leksikal searches failed to match dialectal terms (e.g. `"so DO"`, `"boleh mo maso"`) with the formal text (`"putus studi"`, `"tidak dapat kembali"`), causing both search engines to perform poorly and yield similar low scores.

---

## 2. Redesign Architecture and Scope

The redesigned methodology resolves these issues by applying three minimalist changes that ensure a scientifically fair comparison without expanding the scope of the thesis:

1. **Purge and Formalize Ground Truth (`eval/dataset/ground_truth.csv`):**
   * Remove the 3 Out-of-Domain queries from the quantitative Ragas evaluation.
   * Translate all 27 colloquial/dialectal queries into formal Bahasa Indonesia. This isolates the retrieval performance variable (dense semantic search vs sparse keyword matching) from the translation handling variable.
   * Add 3 new relevant, in-domain queries based on the student survey answers (such as Cum Laude criteria and PKKMB scheduling) to keep the total evaluation size at exactly **30 queries** (a robust, standard benchmark size).
   * Distribute the categories according to the PRD:
     * 12 queries (40%) $\rightarrow$ `academic`
     * 9 queries (30%) $\rightarrow$ `calendar`
     * 6 queries (20%) $\rightarrow$ `institution_profile`
     * 3 queries (10%) $\rightarrow$ `faq`

2. **Neutralize Fallback Response (`src/config.py`):**
   * Redefine `FALLBACK_RESPONSE` to be a neutral, claim-free message. If any query fails retrieval and triggers a fallback, it will not carry links that trigger Ragas faithfulness penalties:
     ```python
     FALLBACK_RESPONSE = (
         "Maaf, saya tidak menemukan informasi yang relevan mengenai "
         "pertanyaan Anda dalam dokumen regulasi yang tersedia."
     )
     ```
   * Move specific contact details (e.g. Rektorat, INSPIRE link) to the UI layer, keeping the LLM generation payload clean.

3. **Isolate OOD Handling as a System Feature:**
   * Treat Out-of-Domain detection (similarity thresholding) as a **chatbot feature** rather than an Ragas evaluation task. Quantitative Ragas evaluation is restricted to the 30 in-domain, formal Indonesian queries.

---

## 3. Ground Truth Specifications

The ground truth dataset is finalized at exactly 30 entries. The fields are: `user_input`, `reference`, `category`, `source_doc`, and `notes`.

### Distribution Table

| Category | Count | Percentage | Target Document |
| --- | :---: | :---: | --- |
| `academic` | 12 | 40% | `Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md` |
| `calendar` | 9 | 30% | `Kalender_Akademik_UNSRAT_Genap_2025-2026.md` |
| `institution_profile` | 6 | 20% | `01_sejarah.md`, `02_visi_misi.md`, `04_lambang.md`, etc. |
| `faq` | 3 | 10% | `Peraturan_Akademik_UNSRAT_2025_RAG_REVISED.md` |
| **Total** | **30** | **100%** | |

---

## 4. Verification and Implementation Plan

1. **Verify Ingestion:** Run ingestion to ensure the Chroma DB collections are clean.
2. **Execute Evaluation:** 
   * Run `conda run -n unsrat-rag python evaluation.py --config b`
   * Run `conda run -n unsrat-rag python evaluation.py --config c`
3. **Compare and Visualize:**
   * Run `conda run -n unsrat-rag python evaluation.py --visualize`
   * Inspect the resulting `perbandingan_visual.png` and update the thesis Bab IV charts.
4. **Error Analysis:** Verify the 10 lowest-scoring queries for both configurations in `error_analysis_config_b.csv` and `error_analysis_config_c.csv`.
