# Design Specification: Dev Tools Page Revamp

## 1. Overview
Revamp the developer tools page (`/dev`) to provide a robust, modern, and modular debugging environment for the UNSRAT RAG system. The new design shifts from a stiff "dark hacker" theme to a modern, bright UI aligned with the main page. The additions focus exclusively on enhancing debugging and research capabilities without impacting the core RAG pipelines.

## 2. Core Principles
- **Working Minimum & Focused:** Avoid over-engineering. Every component must directly serve debugging or research efficiency.
- **Isolated & Modular:** All Dev Tools frontend code (HTML/JS/CSS) and backend endpoints must be entirely isolated from the main RAG application. Future additions should be plug-and-play.
- **Raw Truth:** Visualizations of text chunks must represent the raw data exactly as seen by the LLM (preserving markdown formatting).

## 3. Architecture & Modular Breakdown

### 3.1. Frontend (`static/dev.html` & `static/js/dev.js`)
The UI will use a Light Modern Theme (bright, ample whitespace, rounded corners, subtle shadows) adopting `ui-ux-pro-max` aesthetic standards. The page is broken down into distinct modules:

*   **Module A: Model Tester & Switcher**
    *   **Purpose:** Replaces the rigid Pre-flight check.
    *   **UI:** A dropdown listing available models from `.env`. A "Test Connection" button measures latency. A "Set Active" button dynamically updates the active model state.
*   **Module B: Raw Chunk Viewer**
    *   **Purpose:** View corpus chunks exactly as stored.
    *   **UI:** 1-by-1 navigation (Prev, Next, Go To).
    *   **Data rendering:** Text is placed in a `<pre>` monospace block to preserve exact markdown (`**bold**`, `###`, tables, etc.).
*   **Module C: Retrieval Search Playground**
    *   **Purpose:** Test retrieval accuracy without running full LLM generation.
    *   **UI:** Search input box and a selector (ChromaDB vs BM25). Shows Top-K retrieved chunks and their similarity scores.
*   **Module D: Collapsible Eval Runs Manager**
    *   **Purpose:** Manage past evaluation results without cluttering the screen.
    *   **UI:** Accordion/collapsible list. Default view only shows the currently active evaluation config.
*   **Module E: Real-time Log Terminal**
    *   **Purpose:** Tail the system log. Placed cleanly at the bottom.

### 3.2. Backend (FastAPI in `app.py`)
All new endpoints must be namespaced under `/api/dev/` to prevent interference with public routes.
New/Refactored endpoints:
- `POST /api/dev/test_model`: Takes a model provider name, performs a lightweight ping, returns status and latency.
- `POST /api/dev/set_model`: Updates the active model state.
- `GET /api/dev/chunks?index={n}`: Retrieves a single chunk directly from ChromaDB (Config B) along with its metadata.
- `GET /api/dev/retrieval_test?query={q}&method={chroma|bm25}`: Runs a vector or sparse search and returns the top chunks with scores.
- Existing runs, logs, and status endpoints remain but might be refactored for clarity.

## 4. Isolation & Safety
- **No Impact on Core Pipelines:** The RAG retrieval pipeline and evaluation scripts remain untouched. Dev tools endpoints will simply invoke existing retriever functions or query the DBs directly.
- **Extensibility:** The frontend JS will be structured modularly (e.g., separate functions for initializing each module) so adding a new tool later doesn't require rewriting the whole script.

## 5. Ambiguity Check & Resolutions
- *Which index does the Chunk Viewer read?* It reads directly from ChromaDB via `collection.get()` to perfectly reflect the Dense RAG vectors, not `bm25_index.pkl`.
- *Does "Set Active" modify `.env`?* Modifying `.env` programmatically in Python can be tricky and prone to race conditions if the app relies on `os.environ`. The implementation will focus on dynamically overriding the active instance in memory/state, or safely updating the config file if supported by the current architecture.

## 6. Success Criteria
- The Dev Tools UI is visually consistent with the bright, modern main page.
- Developers can quickly test a model, read raw chunks, test retrievals, and view logs from a single dashboard.
- No disruptions or side-effects to the main RAG application or evaluation workflows.
