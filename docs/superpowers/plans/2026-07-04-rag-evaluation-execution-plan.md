# RAG Evaluation Execution and Verification Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute RAG evaluation for Config B and Config C, generate comparative visualizations, and verify results with the new formalized ground truth dataset.

**Architecture:** Sequentially run the Ragas evaluation pipeline on the updated in-domain ground truth, output results to CSV, and generate comparative PNG charts.

**Tech Stack:** Python 3.11, Ragas, pandas, scipy, matplotlib, conda

---

### Task 1: Execute Config B Evaluation

**Files:**
- Test: `evaluation.py`
- Output: `eval/results/hasil_config_b.csv`

- [ ] **Step 1: Execute Config B evaluation script**

Run:
```bash
conda run -n unsrat-rag python evaluation.py --config b
```
Expected: The script loads 30 ground truth rows, calls `llama-3.1-8b-instruct` to get RAG answers, runs Ragas evaluation using `qwen/qwen3-next-80b-a3b-instruct` as LLM-as-a-Judge, and outputs results.

- [ ] **Step 2: Verify Config B output file exists and has 30 evaluated rows**

Run:
```bash
python -c "import pandas as pd; df = pd.read_csv('eval/results/hasil_config_b.csv'); print('Rows:', len(df)); print('Metrics calculated:', 'faithfulness' in df.columns)"
```
Expected:
```
Rows: 30
Metrics calculated: True
```

- [ ] **Step 3: Commit Config B evaluation results**

Run:
```bash
git add eval/results/hasil_config_b.csv eval/results/error_analysis_config_b.csv
git commit -m "eval: update config b evaluation results and error analysis"
```

---

### Task 2: Execute Config C Evaluation

**Files:**
- Test: `evaluation.py`
- Output: `eval/results/hasil_config_c.csv`

- [ ] **Step 1: Execute Config C evaluation script**

Run:
```bash
conda run -n unsrat-rag python evaluation.py --config c
```
Expected: The script runs BM25 retrieval, generates answers, executes Ragas evaluations, and saves output.

- [ ] **Step 2: Verify Config C output file exists and has 30 evaluated rows**

Run:
```bash
python -c "import pandas as pd; df = pd.read_csv('eval/results/hasil_config_c.csv'); print('Rows:', len(df)); print('Metrics calculated:', 'faithfulness' in df.columns)"
```
Expected:
```
Rows: 30
Metrics calculated: True
```

- [ ] **Step 3: Commit Config C evaluation results**

Run:
```bash
git add eval/results/hasil_config_c.csv eval/results/error_analysis_config_c.csv
git commit -m "eval: update config c evaluation results and error analysis"
```

---

### Task 3: Generate Comparative Visualization

**Files:**
- Test: `evaluation.py`
- Output: `eval/results/perbandingan_visual.png`

- [ ] **Step 1: Run visualization generator**

Run:
```bash
conda run -n unsrat-rag python evaluation.py --visualize
```
Expected: Matplotlib generates the comparison bar chart and saves it.

- [ ] **Step 2: Verify visualization chart exists**

Run:
```bash
python -c "import os; print('Chart exists:', os.path.exists('eval/results/perbandingan_visual.png'))"
```
Expected:
```
Chart exists: True
```

- [ ] **Step 3: Commit visualization image**

Run:
```bash
git add eval/results/perbandingan_visual.png
git commit -m "eval: update comparative visualization chart"
```
