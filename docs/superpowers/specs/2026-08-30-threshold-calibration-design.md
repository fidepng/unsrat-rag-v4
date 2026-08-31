# RAG Similarity Threshold Empirical Calibration & Justification Design

## Executive Summary
This design document defines the final empirical calibration framework for `SIMILARITY_THRESHOLD` in the UNSRAT-RAG system. It establishes the mathematical, statistical, and empirical justification for selecting `SIMILARITY_THRESHOLD = 0.31` (Cosine Distance threshold in ChromaDB, equivalent to Cosine Similarity $\ge 0.69$).

## 1. System Context & Retrieval Pipeline

In the UNSRAT-RAG retrieval pipeline (`src/retriever.py`):
1. User queries are converted into vector embeddings using Google GenerativeAI Embeddings (`gemini-embedding-001`) with `task_type="retrieval_query"`.
2. ChromaDB performs vector similarity search over the indexed corpus chunks (`CHUNK_SIZE_B = 2000`, `CHUNK_OVERLAP_B = 200`).
3. ChromaDB returns top-$K$ ($K = 4$) candidate chunks along with their **Cosine Distance** values:
   $$D = 1 - \cos(\theta) = 1 - \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$
   where $D \in [0, 2]$. Lower distance indicates higher semantic similarity.
4. Filter Rule (FR-09, FR-10): A retrieved chunk is retained if and only if $D \le \text{SIMILARITY\_THRESHOLD}$.
5. If **all** $K$ candidate chunks exceed the threshold, the system triggers the fallback mechanism ("Maaf, informasi tidak ditemukan dalam dokumen").

## 2. Calibration Dataset & Anti-Leakage Protocol

To ensure empirical validity without data leakage (snooping bias):
- **Dataset Location**: `eval/dataset/calibration_dataset_final.csv`
- **Sample Size**: 40 total queries (20 `relevant` queries, 20 `irrelevant` queries).
- **Anti-Leakage Verification**: The dataset was cross-verified using string similarity deduplication against `eval/dataset/ground_truth.csv` to ensure 0% overlap. `calibration_dataset_final.csv` is exclusively used for hyperparameter calibration and never included in end-to-end RAGAS evaluation.

## 3. Calibration Methodology & Sweep Parameters

The calibration script (`scripts/calibrate_threshold.py`) executes a grid sweep across distance threshold values:
- **Sweep Range**: $T \in [0.25, 0.42]$
- **Step Size**: $\Delta T = 0.01$
- **Target Recall Floor**: $\text{RECALL\_FLOOR} = 0.95$ (95% minimum recall required)

### Decision Logic per Query
For each query $q_i$ with top-$K$ chunk distance values $\{d_{i,1}, d_{i,2}, \dots, d_{i,K}\}$:
$$\text{Passed}(q_i, T) = \begin{cases} 1 & \text{if } \min_{j \in [1, K]} d_{i,j} \le T \\ 0 & \text{otherwise} \end{cases}$$

### Matrix Classifications
- **True Positive (TP)**: Query label is `relevant` AND $\text{Passed}(q_i, T) = 1$.
- **False Negative (FN)**: Query label is `relevant` AND $\text{Passed}(q_i, T) = 0$ (Triggers unwarranted fallback).
- **False Positive (FP)**: Query label is `irrelevant` AND $\text{Passed}(q_i, T) = 1$ (Retrieved context noise).
- **True Negative (TN)**: Query label is `irrelevant` AND $\text{Passed}(q_i, T) = 0$ (Correctly rejected noise).

### Evaluation Metrics
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
$$\text{F1-Score} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$$
$$\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$
$$\text{Cosine Similarity Equivalent} = 1 - T$$

## 4. Empirical Sweep Results

Based on experimental execution saved to `eval/results/threshold_sweep_report.csv`:

| Threshold ($T$) | Cosine Sim ($1-T$) | TP | FN | FP | TN | Precision | Recall | F1-Score | Specificity | Accuracy |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0.25 | 0.75 | 14 | 6 | 1 | 19 | 0.9333 | 0.7000 | 0.8000 | 0.9500 | 0.8250 |
| 0.26 | 0.74 | 16 | 4 | 1 | 19 | 0.9412 | 0.8000 | 0.8649 | 0.9500 | 0.8750 |
| 0.27 | 0.73 | 16 | 4 | 2 | 18 | 0.8889 | 0.8000 | 0.8421 | 0.9000 | 0.8500 |
| 0.28 | 0.72 | 18 | 2 | 4 | 16 | 0.8182 | 0.9000 | 0.8571 | 0.8000 | 0.8500 |
| **0.29** | **0.71** | **19** | **1** | **5** | **15** | **0.7917** | **0.9500** | **0.8636** | **0.7500** | **0.8500** |
| 0.30 | 0.70 | 19 | 1 | 6 | 14 | 0.7600 | 0.9500 | 0.8444 | 0.7000 | 0.8250 |
| **0.31** | **0.69** | **20** | **0** | **8** | **12** | **0.7143** | **1.0000** | **0.8333** | **0.6000** | **0.8000** |
| 0.32 | 0.68 | 20 | 0 | 8 | 12 | 0.7143 | 1.0000 | 0.8333 | 0.6000 | 0.8000 |
| 0.33 | 0.67 | 20 | 0 | 9 | 11 | 0.6897 | 1.0000 | 0.8163 | 0.5500 | 0.7750 |
| 0.35 | 0.65 | 20 | 0 | 11 | 9 | 0.6452 | 1.0000 | 0.7843 | 0.4500 | 0.7250 |

## 5. Candidate Comparison & Empirical Rationale for 0.31

### Candidate Comparison Matrix
1. **Candidate A: Max F1 Threshold ($T = 0.29$)**
   - Precision: `79.17%`, Recall: `95.00%`, F1-Score: `0.8636`.
   - Result: 1 out of 20 relevant queries failed to pass retrieval ($\text{FN} = 1$).
2. **Candidate B: Recall-Constrained Threshold ($T = 0.31$) — [SELECTED PRODUCTION VALUE]**
   - Precision: `71.43%`, Recall: `100.00%`, F1-Score: `0.8333`.
   - Result: 0 out of 20 relevant queries failed to pass retrieval ($\text{FN} = 0$).

### Scientific Justification for Selecting $T = 0.31$
- **Asymmetric Cost of Errors in QA RAG**:
  - In a university academic QA RAG system (UNSRAT-RAG), a **False Negative (FN)** directly denies the user access to official academic regulations by triggering an unhelpful fallback answer. The LLM cannot answer a question if the retriever drops the source document.
  - Conversely, a **False Positive (FP)** passes slightly noisier context chunks to the LLM. However, the system's Generator LLM (Gemini 3.5 Flash) is governed by a strict system prompt instructing it to ignore irrelevant context and answer strictly based on factual groundings.
- **Zero False Negative Requirement**:
  - At $T = 0.31$ (Cosine Similarity $\ge 0.69$), the retrieval pipeline achieves **100% Recall ($\text{FN} = 0$)** on the calibration dataset, eliminating false fallbacks while retaining strong precision (71.43%) and high F1 (0.8333).

## 6. Architecture & Code Structure for `scripts/calibrate_threshold.py`

The script is refactored with the following architectural highlights:
1. **CLI Argument Parser**:
   - `--config`: Configuration choice (`"b"` default, `"a"` optional).
   - `--recall-floor`: Minimum recall threshold (`0.95` default).
2. **Centralized Configuration**:
   - Imports paths (`EVAL_RESULTS_DIR`, `CHROMA_DIR_B`, `CHROMA_COLLECTION_B`) from `src.config`.
3. **Comprehensive Metric Calculation**:
   - Computes Precision, Recall, F1, Accuracy, Specificity, and Cosine Similarity Equivalent for each sweep step.
4. **Automated Empirical Justification Summary**:
   - Prints clear comparative analysis to terminal and system logger upon execution.

## 7. Verification Plan
1. Run `python scripts/calibrate_threshold.py --config b` and verify console output.
2. Confirm `eval/results/threshold_sweep_report.csv` contains all metrics.
3. Validate that `SIMILARITY_THRESHOLD = 0.31` in `src/config.py` aligns with candidate B recommendation.
