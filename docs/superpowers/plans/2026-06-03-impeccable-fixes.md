# Impeccable UI/UX Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean up the double-header layouts by removing the top header entirely, adjust sidebar brand text, enhance contrast on footnote disclaimer, and integrate `response_time_seconds` into the Wilcoxon statistical test and RAGAS dashboard.

**Architecture:** We will modify `static/index.html` to eliminate the header tag and its variant layout container. We will adjust the sidebar branding details and update the disclaimer text style. Finally, we will modify `evaluation.py` to run Wilcoxon signed-rank tests for latency (`response_time_seconds`), which dynamically registers it on the FastAPI `/api/evaluation` endpoint and renders it automatically in the frontend Wilcoxon table.

**Tech Stack:** HTML5, CSS (Tailwind CDN), JavaScript (SPA client app), Python (FastAPI, pandas, scipy, pytest)

---

### Task 1: Clean Up Header Layouts in static/index.html
**Files:**
- Modify: `static/index.html:143-198`
- Test: `tests/test_spa_serving.py`

- [ ] **Step 1: Write/inspect current header tests**
  Run: `conda run -n unsrat-rag pytest tests/test_spa_serving.py -v`
  Expected: PASS

- [ ] **Step 2: Modify static/index.html to remove the top headers entirely**
  Remove lines 143 to 198 (which contain the header tag and the `data-impeccable-variants` block).
  
  Target content in `static/index.html` around line 143:
  ```html
          <!-- Area Konten Utama -->
          <main class="flex-1 flex flex-col h-full overflow-hidden relative">
              <!-- Header melintang atas -->
              <!-- impeccable-variants-start 2bb724a7 -->
              <div data-impeccable-variants="2bb724a7" ...>
              ...
              </div>
              <!-- impeccable-variants-end 2bb724a7 -->
  ```
  Replacement content:
  ```html
          <!-- Area Konten Utama -->
          <main class="flex-1 flex flex-col h-full overflow-hidden relative">
  ```

- [ ] **Step 3: Run pytest to verify the page still serves correctly**
  Run: `conda run -n unsrat-rag pytest tests/test_spa_serving.py -v`
  Expected: PASS

- [ ] **Step 4: Commit changes**
  ```bash
  git add static/index.html
  git commit -m "style: remove top header layouts entirely"
  ```

---

### Task 2: Adjust Sidebar Brand Text and Footnote Color Contrast
**Files:**
- Modify: `static/index.html:68-69`, `static/index.html:252-255`

- [ ] **Step 1: Modify sidebar brand text in static/index.html**
  Change the description under the logo from "Sistem RAG Penelitian" to "Asisten Akademik".
  
  Target content:
  ```html
                      <h2 class="font-bold text-base leading-tight uppercase tracking-wider">UNSRAT</h2>
                      <p class="text-white/60 text-[10px] uppercase font-bold tracking-widest">Sistem RAG Penelitian</p>
  ```
  Replacement content:
  ```html
                      <h2 class="font-bold text-base leading-tight uppercase tracking-wider">UNSRAT</h2>
                      <p class="text-white/60 text-[10px] uppercase font-bold tracking-widest">Asisten Akademik</p>
  ```

- [ ] **Step 2: Modify footnote color class for WCAG contrast compliance**
  Change the disclaimer text color from `text-gray-400` to `text-[#6B6661]` (achieves a contrast ratio of >4.5:1 on `#FAF9F6`).
  
  Target content:
  ```html
                    <!-- Catatan Kaki Disclaimer Formal (Section 6) -->
                    <div class="flex items-center space-x-1.5 text-[10px] text-gray-400 mt-5 text-center">
                        <i data-lucide="shield-alert" class="w-3.5 h-3.5 flex-shrink-0 text-gray-400"></i>
                        <span>Sistem ini adalah prototipe penelitian berbasis LLM. Tanggapan didasarkan pada dokumen ground-truth peraturan resmi Universitas Sam Ratulangi. Harap verifikasi informasi penting ke sub-bagian akademik fakultas Anda.</span>
                    </div>
  ```
  Replacement content:
  ```html
                    <!-- Catatan Kaki Disclaimer Formal (Section 6) -->
                    <div class="flex items-center space-x-1.5 text-[10px] text-[#6B6661] mt-5 text-center">
                        <i data-lucide="shield-alert" class="w-3.5 h-3.5 flex-shrink-0 text-[#6B6661]"></i>
                        <span>Sistem ini adalah prototipe penelitian berbasis LLM. Tanggapan didasarkan pada dokumen ground-truth peraturan resmi Universitas Sam Ratulangi. Harap verifikasi informasi penting ke sub-bagian akademik fakultas Anda.</span>
                    </div>
  ```

- [ ] **Step 3: Commit changes**
  ```bash
  git add static/index.html
  git commit -m "style: adjust sidebar text and compliance contrast"
  ```

---

### Task 3: Add response_time_seconds to Wilcoxon test in evaluation.py
**Files:**
- Modify: `evaluation.py:291`
- Test: `conda run -n unsrat-rag python evaluation.py --stats`

- [ ] **Step 1: Modify evaluation.py to include latency in Wilcoxon tests**
  Add `"response_time_seconds"` to the metric iteration loop.
  
  Target content around line 291:
  ```python
      results = []
      for metric in METRICS_COLS:
          if metric not in df_a.columns or metric not in df_b.columns:
  ```
  Replacement content:
  ```python
      results = []
      for metric in METRICS_COLS + ["response_time_seconds"]:
          if metric not in df_a.columns or metric not in df_b.columns:
  ```

- [ ] **Step 2: Run statistical test script to regenerate results**
  Run: `conda run -n unsrat-rag python evaluation.py --stats`
  Expected: Success, statistical_test.csv gets updated with `response_time_seconds` row.

- [ ] **Step 3: Commit changes**
  ```bash
  git add evaluation.py
  git commit -m "feat: run Wilcoxon statistical test on response_time_seconds"
  ```

---

### Task 4: Verify UI Changes in Web Browser
**Files:**
- Verify: `http://localhost:8501/`

- [ ] **Step 1: Check page reload**
  Reload the browser page and confirm that:
  1. The overlapping top headers are gone.
  2. The sidebar brand subtitle reads "ASISTEN AKADEMIK".
  3. The disclaimer text is darker and easier to read.
  4. Under the "Evaluasi RAGAS" tab, the Wilcoxon table contains a row for "Response Time Seconds" with statistic, p-value, significance, and winner.

- [ ] **Step 2: Take a final verification screenshot**
