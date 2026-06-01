# UNSRAT RAG Chatbot — Project Progress Tracker (TODO)

This file tracks the status of all implementation tasks for the Sistem Chatbot Informasi Akademik UNSRAT Berbasis RAG. 

*   **Current Research Stage:** 🧪 Calibration & Evaluation Prep (Post-Task 10)
*   **Active Testing Models (NVIDIA NIM):** 
    *   Generator (`LLM_MODEL_NAME`): `llama-3.1-nemotron-nano-8b-v1`
    *   Evaluator (`EVALUATOR_MODEL_NAME`): `llama-3.3-nemotron-super-49b-v1.5` *(Complies with D-16 bias mitigation)*
    *   Embedding (`EMBEDDING_MODEL_NAME`): `models/gemini-embedding-001`

---

## 📋 Task List & Completion Status

### ✅ Phase 1: Core System Implementation (Tasks 1 - 10)
All files and functional specifications for the RAG architecture have been fully implemented and verified. Unit tests are completely passing!

*   [x] **Task 1: Project Foundation & Environment**
    *   Conda environment, dependencies (`environment.yml`), and environment variables (`.env`) established.
*   [x] **Task 2: src/config.py — Pusat Konfigurasi**
    *   Created `src/config.py` as the single source of truth for all parameters.
*   [x] **Task 3: src/logger_manager.py — Logging Terpusat**
    *   Structured system logging, ingestion reporting, and chat history CSV logging.
*   [x] **Task 4: src/ingestion.py — Pipeline Data Ingestion**
    *   Completed parsing markdown files, two-stage chunking (Config A/B), and MD5 hash idempotency.
*   [x] **Task 5: src/bm25_retriever.py — BM25 Index (Config C)**
    *   Built BM25 retrieval directly using `rank-bm25` (satisfying D-A6).
*   [x] **Task 6: src/retriever.py — Unified Retrieval Interface**
    *   Created unified retriever class for globally retrieving chunks from Config A, B, and C.
*   [x] **Task 7: src/chain.py — RAG Chain + Citation + SSE**
    *   Implemented inline citation extraction, stateless LLM wrapper, and SSE streaming with four events.
*   [x] **Task 8: app.py — FastAPI Backend**
    *   Created endpoints for chat, configuration, and evaluation statistics.
*   [x] **Task 9: static/ — SPA Frontend**
    *   Built beautiful Vanilla HTML/CSS/JS frontend with dual-tabs, thinking indicators, and comparison charts.
*   [x] **Task 10: evaluation.py — Pipeline Evaluasi Ragas**
    *   Implemented Ragas metrics evaluation, Wilcoxon signed-rank test calculation, and Matplotlib chart generation.

---

### ⏳ Phase 2: Calibration, Data Expansion & Validation (Tasks 11 - 13)
We are currently entering this stage to finalize the research data for the skripsi thesis.

#### [ ] Task 11: Kalibrasi SIMILARITY_THRESHOLD (D-B7)
*   [ ] **Step 11.1:** Write empirical calibration script (`tests/calibrate_threshold.py`) to evaluate retrieval accuracy across multiple thresholds (e.g., 0.55, 0.60, 0.65, 0.70).
*   [ ] **Step 11.2:** Run calibration using the current ground truth.
*   [ ] **Step 11.3:** Analyze recall/precision and adjust `SIMILARITY_THRESHOLD` in `src/config.py` if needed.
*   [ ] **Step 11.4:** Commit configuration updates.

#### [ ] Task 12: Persiapan Ground Truth (D-B6)
*   [ ] **Step 12.1:** Expand `eval/dataset/ground_truth.csv` from the minimal 3 test questions to 30–50 natural language question-answer pairs covering academic regulations, vision-misi, and calendar.
*   [ ] **Step 12.2:** Verify that references represent key facts (not verbatim copy-paste) as required by D-B6.
*   [ ] **Step 12.3:** Commit the expanded ground truth dataset.

#### [ ] Task 13: Evaluasi Resmi & Validasi Akhir
*   [ ] **Step 13.1:** Clear out old test evaluation outputs (`ctx purge` / delete old result CSVs).
*   [ ] **Step 13.2:** Execute official evaluation for Config A: `python evaluation.py --config a`
*   [ ] **Step 13.3:** Execute official evaluation for Config B: `python evaluation.py --config b`
*   [ ] **Step 13.4:** Execute official evaluation for Config C: `python evaluation.py --config c`
*   [ ] **Step 13.5:** Compute final Wilcoxon signed-rank statistics: `python evaluation.py --stats`
*   [ ] **Step 13.6:** Generate comparativegrouped bar charts: `python evaluation.py --plot`
*   [ ] **Step 13.7:** Perform error analysis on the top-10 failing queries per config.
*   [ ] **Step 13.8:** Compile the final skripsi appendix materials.
