# Refactoring Academic RAG Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the academic RAG system to focus on Config B vs Config C by soft-disabling/archiving Config A and the Wilcoxon statistical test across the frontend UI, backend API, and offline pipelines, while keeping all code functional for backup purposes.

**Architecture:** Create a `backup_original` folder to store all original files. Comment out UI elements in `index.html` (Config A option, Wilcoxon card), update Chart.js logic in `app.js` to skip Config A dataset, adjust the `/api/config` endpoint in `app.py` to return `["b", "c"]`, and add interception guards to `evaluation.py` and `src/ingestion.py` to cleanly abort Config A/stats requests with a deprecation warning.

**Tech Stack:** Python, FastAPI, HTML5, Javascript, Chart.js, Tailwind CSS, Matplotlib

---

### Task 1: Create Backup Directory and Copy Original Files

**Files:**
- Create: `backup_original/`
- Copy original files to `backup_original/`

- [ ] **Step 1: Create backup folder and copy all target files**

Run the following commands in the PowerShell terminal to back up the original code:
```powershell
New-Item -ItemType Directory -Force -Path backup_original
Copy-Item app.py backup_original\app.py
Copy-Item evaluation.py backup_original\evaluation.py
Copy-Item src\config.py backup_original\config.py
Copy-Item src\ingestion.py backup_original\ingestion.py
Copy-Item static\index.html backup_original\index.html
Copy-Item static\js\app.js backup_original\app.js
```
Expected: The directory `backup_original/` is created containing exact copies of the 6 files.

- [ ] **Step 2: Commit backup files**
Run:
```bash
git add backup_original/
git commit -m "backup: archive original files containing config a and wilcoxon logic"
```
Expected: Files successfully committed to git.

---

### Task 2: Document Config A Deprecation in `src/config.py`

**Files:**
- Modify: `src/config.py`

- [ ] **Step 1: Add deprecation comments to Config A constants**
Modify the file `src/config.py` from:
```python
# ── CHROMADB COLLECTIONS ────────────────────────────────────
CHROMA_COLLECTION_A = "unsrat_rag_config_a"
CHROMA_COLLECTION_B = "unsrat_rag_config_b"
```
To:
```python
# ── CHROMADB COLLECTIONS ────────────────────────────────────
# [BACKUP/DEPRECATED - ARCHIVED]
CHROMA_COLLECTION_A = "unsrat_rag_config_a"
CHROMA_COLLECTION_B = "unsrat_rag_config_b"
```
And also modify:
```python
# ── CHUNKING — CONFIG A ──────────────────────────────────────
CHUNK_SIZE_A    = 500
CHUNK_OVERLAP_A = 100
```
To:
```python
# ── CHUNKING — CONFIG A ──────────────────────────────────────
# [BACKUP/DEPRECATED - ARCHIVED]
CHUNK_SIZE_A    = 500
CHUNK_OVERLAP_A = 100
```

- [ ] **Step 2: Commit changes**
Run:
```bash
git add src/config.py
git commit -m "refactor: add deprecation comments above Config A parameters in config.py"
```

---

### Task 3: Adjust API Configuration Endpoint in `app.py`

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Modify `/api/config` endpoint**
Modify the file `app.py` from line 49-60:
```python
@app.get("/api/config")
async def get_config():
    """
    Kembalikan daftar config dan model yang tersedia.
    (PRD Section 10.4)
    """
    return JSONResponse({
        "available_models": AVAILABLE_MODELS,
        "active_model":     LLM_MODEL_NAME,
        "configs":          ["a", "b", "c"],
    })
```
To:
```python
@app.get("/api/config")
async def get_config():
    """
    Kembalikan daftar config dan model yang tersedia.
    (PRD Section 10.4)
    """
    return JSONResponse({
        "available_models": AVAILABLE_MODELS,
        "active_model":     LLM_MODEL_NAME,
        # Config A is archived for backup. Restricting API output to B and C.
        "configs":          ["b", "c"],
    })
```

- [ ] **Step 2: Commit changes**
Run:
```bash
git add app.py
git commit -m "refactor: limit api config endpoint to configurations b and c"
```

---

### Task 4: Hide Config A and Wilcoxon UI from `static/index.html`

**Files:**
- Modify: `static/index.html`

- [ ] **Step 1: Comment out Config A option in the selector**
Modify the file `static/index.html` from lines 100-104:
```html
                          <select id="config-select" class="w-full bg-black/20 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-white/30 cursor-pointer appearance-none">
                              <option value="b" class="text-gray-800">Config B - RAG 2000 char</option>
                              <option value="a" class="text-gray-800">Config A - RAG 500 char</option>
                              <option value="c" class="text-gray-800">Config C - BM25 Baseline</option>
                          </select>
```
To:
```html
                          <select id="config-select" class="w-full bg-black/20 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-white/30 cursor-pointer appearance-none">
                              <option value="b" class="text-gray-800">Config B - RAG 2000 char</option>
                              <!-- <option value="a" class="text-gray-800">Config A - RAG 500 char [ARCHIVED]</option> -->
                              <option value="c" class="text-gray-800">Config C - BM25 Baseline</option>
                          </select>
```

- [ ] **Step 2: Hide Wilcoxon Card Container**
Modify the file `static/index.html` from line 277:
```html
                  <!-- Card Hasil Uji Statistik Wilcoxon (Dengan Clipboard Copy) -->
                  <div class="bg-white border border-[#EBE7E1] rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between">
```
To:
```html
                  <!-- Card Hasil Uji Statistik Wilcoxon (Dengan Clipboard Copy) - HIDDEN/DEPRECATED -->
                  <div class="hidden bg-white border border-[#EBE7E1] rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between">
```

- [ ] **Step 3: Commit changes**
Run:
```bash
git add static/index.html
git commit -m "ui: hide Wilcoxon card and comment out Config A from config selector"
```

---

### Task 5: Refactor Chart.js Rendering in `static/js/app.js`

**Files:**
- Modify: `static/js/app.js`

- [ ] **Step 1: Remove Config A dataset from the bar chart**
Modify the file `static/js/app.js` from line 759-789:
```javascript
        metricsChartInstance = new Chart(ctx.getContext("2d"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Config A (500 char)",
                        data: dataA,
                        backgroundColor: "rgba(123, 45, 45, 0.4)",
                        borderColor: "rgb(123, 45, 45)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Config B (2000 char)",
                        data: dataB,
                        backgroundColor: "rgba(168, 69, 69, 0.9)",
                        borderColor: "rgb(168, 69, 69)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Config C (BM25)",
                        data: dataC,
                        backgroundColor: "rgba(156, 163, 175, 0.5)",
                        borderColor: "rgb(156, 163, 175)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    }
                ]
            },
```
To:
```javascript
        metricsChartInstance = new Chart(ctx.getContext("2d"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    // Config A is archived/deprecated. Only plotting Config B and Config C.
                    {
                        label: "Config B (2000 char)",
                        data: dataB,
                        backgroundColor: "rgba(168, 69, 69, 0.9)",
                        borderColor: "rgb(168, 69, 69)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Config C (BM25)",
                        data: dataC,
                        backgroundColor: "rgba(156, 163, 175, 0.5)",
                        borderColor: "rgb(156, 163, 175)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    }
                ]
            },
```

- [ ] **Step 2: Commit changes**
Run:
```bash
git add static/js/app.js
git commit -m "ui: refactor chart rendering to display only Config B vs Config C"
```

---

### Task 6: Refactor CLI and Pipeline Executions in `evaluation.py`

**Files:**
- Modify: `evaluation.py`

- [ ] **Step 1: Add import sys**
Modify the file `evaluation.py` from line 5:
```python
import argparse
import csv
import time
from pathlib import Path
```
To:
```python
import argparse
import csv
import time
import sys
from pathlib import Path
```

- [ ] **Step 2: Intercept Config A CLI execution**
Modify `evaluation.py` from line 384-385:
```python
    if args.config:
        run_evaluation(args.config, extra_metrics=args.extra_metrics)
```
To:
```python
    if args.config:
        if args.config == "a":
            print("Config A is deprecated and archived for backup purposes.")
            sys.exit(0)
        run_evaluation(args.config, extra_metrics=args.extra_metrics)
```

- [ ] **Step 3: Bypass and archive Wilcoxon test**
Modify `evaluation.py` from line 386-387:
```python
    elif args.stats:
        run_statistical_test()
```
To:
```python
    elif args.stats:
        # --- ARCHIVED WILCOXON TEST ---
        print("Wilcoxon statistical test is deprecated and archived for backup purposes.")
        # run_statistical_test()
```

- [ ] **Step 4: Update plot configuration to exclude Config A**
Modify `evaluation.py` from line 331-332:
```python
    configs = {"a": "Config A (500)", "b": "Config B (2000)", "c": "Config C (BM25)"}
    metrics = METRICS_COLS
```
To:
```python
    # Config A is archived. Exclusively plotting Config B vs C.
    configs = {"b": "Config B (2000)", "c": "Config C (BM25)"}
    metrics = METRICS_COLS
```
And modify lines 346-347:
```python
    width  = 0.25
    colors = ["#800000", "#c9a227", "#4a4a4a"]
```
To:
```python
    width  = 0.35
    colors = ["#c9a227", "#4a4a4a"]
```
And modify line 359:
```python
    ax.set_title("Perbandingan Kinerja Config A vs B vs C — UNSRAT RAG")
```
To:
```python
    ax.set_title("Perbandingan Kinerja Config B vs C — UNSRAT RAG")
```

- [ ] **Step 5: Commit changes**
Run:
```bash
git add evaluation.py
git commit -m "refactor: soft-disable Config A and Wilcoxon CLI execution, update matplotlib visualize plot"
```

---

### Task 7: Refactor Ingestion Pipeline in `src/ingestion.py`

**Files:**
- Modify: `src/ingestion.py`

- [ ] **Step 1: Make --config optional defaulting to "b", and import sys**
Modify `src/ingestion.py` from lines 5-8:
```python
import argparse
import hashlib
import time
from pathlib import Path
```
To:
```python
import argparse
import hashlib
import time
import sys
from pathlib import Path
```
Modify lines 273-277:
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingestion pipeline UNSRAT RAG")
    parser.add_argument("--config", choices=["a", "b"], required=True, help="Config A atau B")
    parser.add_argument("--rebuild", action="store_true", help="Hapus collection dan rebuild dari nol")
```
To:
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingestion pipeline UNSRAT RAG")
    parser.add_argument("--config", choices=["a", "b"], default="b", help="Config A atau B (default: b)")
    parser.add_argument("--rebuild", action="store_true", help="Hapus collection dan rebuild dari nol")
```

- [ ] **Step 2: Intercept Config A ingestion**
Modify `src/ingestion.py` from lines 277-279:
```python
    args = parser.parse_args()
    run_ingestion(args.config, args.rebuild)
```
To:
```python
    args = parser.parse_args()
    if args.config == "a":
        print("Config A is deprecated and archived for backup purposes.")
        sys.exit(0)
    run_ingestion(args.config, args.rebuild)
```

- [ ] **Step 3: Commit changes**
Run:
```bash
git add src/ingestion.py
git commit -m "refactor: default ingestion pipeline to Config B and deprecate Config A run"
```

---

### Task 8: Verification

- [ ] **Step 1: Test Ingestion CLI defaults and deprecation**
Run: `python src/ingestion.py`
Expected: Processes Config B ingestion (running files, print out info).
Run: `python src/ingestion.py --config a`
Expected: Prints `"Config A is deprecated and archived for backup purposes."` and exits without executing.

- [ ] **Step 2: Test Evaluation CLI deprecation**
Run: `python evaluation.py --config a`
Expected: Prints `"Config A is deprecated and archived for backup purposes."` and exits.
Run: `python evaluation.py --stats`
Expected: Prints `"Wilcoxon statistical test is deprecated and archived for backup purposes."` and exits.

- [ ] **Step 3: Test Matplotlib visualization**
Run: `python evaluation.py --visualize`
Expected: Saves `eval/results/perbandingan_visual.png`. Check the file to verify it only has two bars (Config B and Config C) per metric.

- [ ] **Step 4: Run server and check UI selector and Wilcoxon card**
Run: `python app.py`
Expected: Starts the FastAPI server successfully.
Open: `http://localhost:8501/` (or whatever the port is)
Expected: 
1. The sidebar dropdown for Config only shows Config B and Config C.
2. In the Evaluation tab, the Wilcoxon card is hidden.
3. The Ragas chart displays only Config B and Config C.
