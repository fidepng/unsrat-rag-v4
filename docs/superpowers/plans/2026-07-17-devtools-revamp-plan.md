# Implementation Plan: Dev Tools Revamp (v4.0)

## Overview
This document outlines the step-by-step implementation plan for revamping the Dev Tools page (`/dev`). The new UI will adopt a modern, bright "Light Theme" (ui-ux-pro-max aesthetic) and introduce 4 main modules:
1. Model Tester & Switcher (replacing Pre-flight)
2. Raw Chunk Viewer
3. Retrieval Search Playground
4. Collapsible Eval Runs Manager & Real-time Log Terminal

**Constraint:** All changes must be strictly isolated to the `/api/dev/` namespace and `/dev` frontend, without affecting the main RAG pipeline.

## Task 1: Backend Setup for Model Tester & Switcher
- **Goal:** Allow users to test and temporarily switch the active generator LLM model in the development environment.
- **File:** `app.py`
- **Actions:**
  1. Add a `POST /api/dev/test_model` endpoint that accepts a model name, tests it using `src.chain.get_response` with a simple "Hello" prompt, and returns the response and latency.
  2. Add a `POST /api/dev/set_model` endpoint that updates the active model state in-memory (or overrides it).

## Task 2: Backend Setup for Raw Chunk Viewer
- **Goal:** Enable viewing original, unformatted markdown chunks one by one by index (1-179).
- **File:** `app.py`
- **Actions:**
  1. Add a `GET /api/dev/chunks?index={n}&config={b|c}` endpoint.
  2. For config `b`, fetch the chunk from ChromaDB using `collection.get(limit=1, offset=n-1)`.
  3. For config `c`, fetch the chunk from `bm25_index.pkl`.
  4. Ensure the endpoint returns the exact raw text (including markdown syntax like `**`, `__`, `|`).

## Task 3: Backend Setup for Retrieval Search Playground
- **Goal:** Allow debugging of sparse vs dense retrieval by simulating a query and showing retrieved chunks and scores.
- **File:** `app.py`
- **Actions:**
  1. Add a `GET /api/dev/retrieval_test?query={q}&config={b|c}` endpoint.
  2. Import `retrieve_chunks` from `src.retriever`.
  3. Call `retrieve_chunks` with the query and config, and return the chunks with their distance/scores.

## Task 4: Frontend UI Revamp (Light Theme)
- **Goal:** Redesign `static/dev.html` to a modern light theme (ui-ux-pro-max standard).
- **File:** `static/dev.html`
- **Actions:**
  1. Change Tailwind classes from `bg-slate-950` to a clean light UI (e.g., `bg-slate-50`, `text-slate-900`, `bg-white` cards with subtle shadows).
  2. Update typography to look impeccable (using Inter, proper whitespace).
  3. Prepare structural layout for the 4 new modules.

## Task 5: Frontend Logic for Model Tester & Switcher
- **Goal:** Implement the logic in JS to test and switch models.
- **File:** `static/js/dev.js`
- **Actions:**
  1. Replace the "Pre-flight Check" section with a dropdown/list of available models (Gemini, NIM, etc.).
  2. Add "Test Model" button to call `/api/dev/test_model` and display result & latency.
  3. Add "Set Active" button to call `/api/dev/set_model`.

## Task 6: Frontend Logic for Raw Chunk Viewer
- **Goal:** Implement the Chunk Viewer UI with pagination.
- **File:** `static/js/dev.js`
- **Actions:**
  1. Add a module for Chunk Viewer.
  2. Add Next/Prev buttons and a specific index input.
  3. Fetch from `/api/dev/chunks` and display the raw markdown inside a `<pre><code>` block to preserve original formatting.

## Task 7: Frontend Logic for Retrieval Search Playground
- **Goal:** Implement the Retrieval search bar and results display.
- **File:** `static/js/dev.js`
- **Actions:**
  1. Add a search input and config toggle (Dense vs Sparse).
  2. Fetch from `/api/dev/retrieval_test` on submit.
  3. Render the retrieved chunks elegantly, showing chunk metadata and similarity scores.

## Task 8: Eval Runs Manager & Log Terminal Integration
- **Goal:** Update the existing tables and logs to match the light theme and use accordions.
- **File:** `static/dev.html` & `static/js/dev.js`
- **Actions:**
  1. Make the Eval Runs Manager table collapsible (accordion) so it doesn't clutter the page.
  2. Convert the terminal to a light theme variant (e.g., white background with dark monospace text, or keep a dark terminal box inside the light page for contrast).
  3. Ensure the modularity of the JS code.
