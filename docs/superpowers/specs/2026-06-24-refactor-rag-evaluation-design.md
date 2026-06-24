# Design Specification: Refactoring Academic RAG Evaluation
**Topic:** Soft-Disabling Config A and Wilcoxon Test (B vs C Focus)  
**Date:** 2026-06-24  
**Author:** Antigravity  

---

## 1. Overview
The goal of this refactoring is to adapt the academic RAG chatbot system to focus exclusively on comparing **Config B** (RAG, 2000-character chunk) vs **Config C** (BM25 baseline, 2000-character chunk). 

To preserve the historical capability of the code, **Config A** (RAG, 500-character chunk) and the **Wilcoxon Signed-Rank Test** (comparing A vs B) will be soft-disabled, commented out, or bypassed rather than permanently deleted.

---

## 2. Backup Plan
Before making any modifications, a complete snapshot of all files to be edited will be copied into a dedicated backup folder:
*   **Backup Folder:** `backup_original/` at the workspace root.
*   **Files to Backup:**
    1.  `app.py` $\rightarrow$ `backup_original/app.py`
    2.  `evaluation.py` $\rightarrow$ `backup_original/evaluation.py`
    3.  `src/config.py` $\rightarrow$ `backup_original/config.py`
    4.  `src/ingestion.py` $\rightarrow$ `backup_original/ingestion.py`
    5.  `static/index.html` $\rightarrow$ `backup_original/index.html`
    6.  `static/js/app.js` $\rightarrow$ `backup_original/app.js`

---

## 3. Detailed Specifications

### A. Frontend Changes (`static/index.html` & `static/js/app.js`)
*   **Config Selector Dropdown (`#config-select`):** 
    *   Comment out the Config A `<option>` tag in `static/index.html`.
    ```html
    <select id="config-select" ...>
        <option value="b" ...>Config B - RAG 2000 char</option>
        <!-- <option value="a" ...>Config A - RAG 500 char [ARCHIVED]</option> -->
        <option value="c" ...>Config C - BM25 Baseline</option>
    </select>
    ```
*   **Wilcoxon Table Container:**
    *   Add the CSS class `hidden` to the Wilcoxon card container div in `static/index.html` to hide it from the UI.
    ```html
    <div class="hidden bg-white border border-[#EBE7E1] rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between">
        <!-- Wilcoxon contents -->
    </div>
    ```
    *   *Safety:* The elements remain in the DOM so that query selectors in `app.js` (e.g., `document.getElementById("wilcoxon-table-body")`) do not return `null` and crash execution.
*   **Chart.js Rendering:**
    *   In `static/js/app.js`, keep the local variable `dataA` initialized to prevent reference errors, but remove the Config A dataset object from the datasets array passed to `new Chart(...)`.
    *   The bar chart will render only two bars side-by-side: Config B and Config C.

### B. Backend API Changes (`app.py` & `src/config.py`)
*   **Config Endpoint (`/api/config`):**
    *   Change the `"configs"` array in the JSON response of `GET /api/config` from `["a", "b", "c"]` to `["b", "c"]`.
*   **Evaluation Endpoint (`/api/evaluation`):**
    *   Leave the loop parsing `hasil_config_a.csv` intact to allow rendering if historical files exist on disk, but UI charting and UI selection will ignore it.
*   **Config constants (`src/config.py`):**
    *   Add `# [BACKUP/DEPRECATED - ARCHIVED]` comment headers above all Config A properties (`CHUNK_SIZE_A`, `CHUNK_OVERLAP_A`, `CHROMA_DIR_A`, `CHROMA_COLLECTION_A`). Do not delete them to prevent import failure in other files.

### C. Pipeline CLI changes (`evaluation.py` & `src/ingestion.py`)
*   **CLI Config A Run (`evaluation.py`):**
    *   If `--config a` is passed, print `"Config A is deprecated and archived for backup purposes."` and exit cleanly.
*   **CLI Stats Run (`evaluation.py`):**
    *   Bypass the `run_statistical_test()` execution when `--stats` is called. Wrap the call in `# --- ARCHIVED WILCOXON TEST ---` comments and print an archive notification message.
*   **Visualization Matplotlib (`evaluation.py`):**
    *   In `run_visualization()`, update `configs` to only include `{"b": "Config B (2000)", "c": "Config C (BM25)"}`.
    *   Adjust bar `width` from `0.25` to `0.35` and update titles/labels accordingly.
*   **Ingestion Pipeline (`src/ingestion.py`):**
    *   Make `--config` default to `"b"` in `argparse`.
    *   If `--config a` is passed, abort with a deprecation print statement.

---

## 4. Verification Plan

### Manual Verification Steps
1.  **Check Ingestion Defaults:**
    *   Run `python src/ingestion.py` (without arguments) $\rightarrow$ verify it defaults to config B.
    *   Run `python src/ingestion.py --config a` $\rightarrow$ verify it prints the deprecation message and exits.
2.  **Check Evaluation CLI:**
    *   Run `python evaluation.py --config a` $\rightarrow$ verify it prints the deprecation message and exits.
    *   Run `python evaluation.py --stats` $\rightarrow$ verify it prints the deprecation message and exits.
    *   Run `python evaluation.py --visualize` $\rightarrow$ verify the generated image `eval/results/perbandingan_visual.png` contains only B and C bars.
3.  **Check Server & Web UI:**
    *   Start server: `python app.py`
    *   Open UI $\rightarrow$ check config dropdown (only B and C visible).
    *   Go to Evaluation tab $\rightarrow$ check Ragas chart (only Config B and C bars visible), check Wilcoxon card (hidden from display).

---

## 5. Reactivation Guide
To restore the deprecated features in the future:
1.  **Re-enable CLI:** Remove the `if config == "a"` guard blocks in `evaluation.py` and `src/ingestion.py`, and uncomment the `run_statistical_test()` call in `evaluation.py`.
2.  **Re-enable UI Selector:** Uncomment the `<option>` tag for Config A in `static/index.html`.
3.  **Re-enable Wilcoxon Table:** Remove the `hidden` class from the Wilcoxon card div in `static/index.html`.
4.  **Re-enable Charting:** Restore the dataset object for Config A in the `datasets` list of `static/js/app.js`.
5.  **Re-enable API:** Re-add `"a"` to the `"configs"` array in `app.py`.
