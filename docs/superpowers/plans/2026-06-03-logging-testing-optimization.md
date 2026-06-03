# Logging & Testing Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mengoptimalkan sistem logging dengan rotating file log serta middleware exception di FastAPI, dan mendesain ulang serta melengkapi test suite dengan modularitas penuh menggunakan mark `offline`/`online` dan mocking ChromaDB/Gemini API.

**Architecture:** Memanfaatkan Python standard library `logging.handlers.RotatingFileHandler` untuk log rotasi, menambahkan middleware penangkap exception global di FastAPI, menstrukturkan ulang folder `tests/`, serta menggunakan `unittest.mock` untuk melakukan mocking ChromaDB dan LLM API.

**Tech Stack:** Python 3.11, Pytest, FastAPI, unittest.mock, langchain, chromadb, tiktoken.

---

### Task 1: Setup Pytest Configuration & Test Markers

**Files:**
- Create: `pytest.ini`
- Create: `tests/unit/.gitkeep`
- Create: `tests/integration/.gitkeep`
- Create: `tests/scripts/.gitkeep`

- [ ] **Step 1: Create pytest.ini**
  Buat file `pytest.ini` di root direktori proyek dengan konten berikut:
  ```ini
  [pytest]
  markers =
      offline: Pengujian yang berjalan sepenuhnya offline (unit test, mock).
      online: Pengujian konektivitas eksternal (API key real).
  testpaths = tests
  python_files = test_*.py
  ```

- [ ] **Step 2: Create directory placeholders**
  Buat file `.gitkeep` untuk direktori baru agar ter-track di Git:
  * `tests/unit/.gitkeep`
  * `tests/integration/.gitkeep`
  * `tests/scripts/.gitkeep`

- [ ] **Step 3: Commit**
  ```bash
  git add pytest.ini tests/unit/.gitkeep tests/integration/.gitkeep tests/scripts/.gitkeep
  git commit -m "test: setup pytest markers and subfolders structure"
  ```

---

### Task 2: Migrate Files & Set Up Global Mocks in conftest.py

**Files:**
- Create: `tests/conftest.py`
- Modify: Move `tests/test_citation_parser.py` -> `tests/unit/test_citation_parser.py`
- Modify: Move `tests/test_spa_serving.py` -> `tests/integration/test_spa_serving.py`
- Modify: Move scripts to `tests/scripts/` (`verify_ingestion.py`, `verify_retriever.py`, `test_nvidia_nim_api.py`)

- [ ] **Step 1: Move existing test files**
  Gunakan git command untuk memindahkan file agar riwayat git terjaga:
  ```bash
  git mv tests/test_citation_parser.py tests/unit/test_citation_parser.py
  git mv tests/test_spa_serving.py tests/integration/test_spa_serving.py
  git mv tests/verify_ingestion.py tests/scripts/verify_ingestion.py
  git mv tests/verify_retriever.py tests/scripts/verify_retriever.py
  git mv tests/test_nvidia_nim_api.py tests/scripts/test_nvidia_nim_api.py
  ```

- [ ] **Step 2: Add offline markers to migrated tests**
  Tambahkan `@pytest.mark.offline` di atas class/fungsi uji di `tests/unit/test_citation_parser.py` dan `tests/integration/test_spa_serving.py`.

- [ ] **Step 3: Create tests/conftest.py with mocks**
  Tulis file `tests/conftest.py` yang berisi global mock fixtures:
  ```python
  import pytest
  from unittest.mock import MagicMock, patch

  @pytest.fixture(autouse=True)
  def mock_chroma():
      with patch("chromadb.PersistentClient") as mock_client:
          mock_instance = MagicMock()
          mock_client.return_value = mock_instance
          
          mock_collection = MagicMock()
          mock_instance.get_collection.return_value = mock_collection
          mock_instance.get_or_create_collection.return_value = mock_collection
          
          mock_collection.query.return_value = {
              "ids": [["chunk_1"]],
              "documents": [["Syarat SKS maksimal per semester adalah 24 SKS."]],
              "metadatas": [[{"doc_id": "pedoman_1", "title": "Pedoman Akademik", "category": "peraturan", "status": "active"}]],
              "distances": [[0.15]]
          }
          mock_collection.get.return_value = {
              "ids": ["chunk_1"],
              "documents": ["Syarat SKS maksimal per semester adalah 24 SKS."],
              "metadatas": [{"doc_id": "pedoman_1", "title": "Pedoman Akademik", "category": "peraturan", "status": "active"}]
          }
          mock_collection.count.return_value = 1
          yield mock_instance

  @pytest.fixture(autouse=True)
  def mock_embeddings():
      with patch("langchain_google_genai.GoogleGenerativeAIEmbeddings") as mock_embed_class:
          mock_instance = MagicMock()
          mock_embed_class.return_value = mock_instance
          mock_instance.embed_query.return_value = [0.1] * 768
          mock_instance.embed_documents.return_value = [[0.1] * 768]
          yield mock_instance

  @pytest.fixture(autouse=True)
  def mock_google_llm():
      with patch("langchain_google_genai.ChatGoogleGenerativeAI") as mock_llm_class:
          mock_instance = MagicMock()
          mock_llm_class.return_value = mock_instance
          
          mock_response = MagicMock()
          mock_response.content = "Berdasarkan pedoman akademik [1], mahasiswa dapat mengambil maksimal 24 SKS."
          mock_instance.invoke.return_value = mock_response
          yield mock_instance

  @pytest.fixture(autouse=True)
  def mock_nim_llm():
      with patch("langchain_openai.ChatOpenAI") as mock_openai_class:
          mock_instance = MagicMock()
          mock_openai_class.return_value = mock_instance
          
          mock_response = MagicMock()
          mock_response.content = "UNSRAT"
          mock_instance.invoke.return_value = mock_response
          yield mock_instance
  ```

- [ ] **Step 4: Run tests to verify migration**
  Jalankan: `pytest -m offline`
  Pastikan 11 tes asli berhasil dijalankan tanpa error.

- [ ] **Step 5: Commit**
  ```bash
  git add tests/conftest.py tests/unit/test_citation_parser.py tests/integration/test_spa_serving.py
  git commit -m "test: migrate files and configure global mock fixtures in conftest.py"
  ```

---

### Task 3: Implement Logging Optimization (RotatingFileHandler)

**Files:**
- Modify: `src/logger_manager.py`
- Create: `tests/unit/test_logger_manager.py`

- [ ] **Step 1: Write test_logger_manager.py first (TDD)**
  Tulis test di `tests/unit/test_logger_manager.py`:
  ```python
  import pytest
  import csv
  from src.logger_manager import get_logger, log_ingestion_report, log_chat_transaction

  @pytest.mark.offline
  class TestLoggerManager:
      def test_logger_creation(self):
          logger = get_logger("test_logger_unit")
          assert logger.name == "test_logger_unit"
          assert len(logger.handlers) >= 2

      def test_log_ingestion_report(self, tmp_path):
          test_csv = tmp_path / "ingestion_test.csv"
          with pytest.MonkeyPatch().context() as mp:
              mp.setattr("src.logger_manager.INGESTION_LOG_PATH", test_csv)
              log_ingestion_report(
                  config="a",
                  files_processed=5,
                  chunks_generated=20,
                  chunks_inserted=18,
                  chunks_duplicate_skipped=2,
                  chunks_too_short_skipped=0,
                  execution_time_seconds=12.34
              )
              assert test_csv.exists()
              with open(test_csv, "r", encoding="utf-8") as f:
                  reader = list(csv.DictReader(f))
                  assert len(reader) == 1
                  assert reader[0]["config"] == "a"
                  assert reader[0]["files_processed"] == "5"

      def test_log_chat_transaction(self, tmp_path):
          test_csv = tmp_path / "chat_test.csv"
          with pytest.MonkeyPatch().context() as mp:
              mp.setattr("src.logger_manager.CHAT_LOG_PATH", test_csv)
              log_chat_transaction(
                  config="b",
                  model_llm="gemini-3.5-flash",
                  user_query="Halo",
                  chunks_retrieved_count=2,
                  retrieved_chunk_ids=["id1", "id2"],
                  best_similarity_score=0.123,
                  average_similarity_score=0.456,
                  response_time_seconds=1.5,
                  estimated_prompt_tokens=100,
                  estimated_completion_tokens=50,
                  estimated_total_tokens=150,
                  found_state=True,
                  answer_preview="Preview"
              )
              assert test_csv.exists()
              with open(test_csv, "r", encoding="utf-8") as f:
                  reader = list(csv.DictReader(f))
                  assert len(reader) == 1
                  assert reader[0]["config"] == "b"
                  assert reader[0]["user_query"] == "Halo"
                  assert reader[0]["estimated_total_tokens"] == "150"
  ```

- [ ] **Step 2: Run test to make sure it fails**
  Run: `pytest tests/unit/test_logger_manager.py -v` (Fails if log directory/paths are not matching or RotatingFileHandler is not imported)

- [ ] **Step 3: Update src/logger_manager.py with RotatingFileHandler**
  Ubah bagian handler di `src/logger_manager.py` (Baris 33-44) untuk menggunakan `RotatingFileHandler` dengan max 5MB dan backupCount 3:
  ```python
  from logging.handlers import RotatingFileHandler

  # ... di dalam get_logger(name) ...
      # File handler — semua level dengan rotasi file (max 5MB, keep 3 backups)
      fh = RotatingFileHandler(
          SYSTEM_LOG_PATH,
          maxBytes=5 * 1024 * 1024,
          backupCount=3,
          encoding="utf-8"
      )
      fh.setLevel(logging.DEBUG)
      fh.setFormatter(formatter)
  ```

- [ ] **Step 4: Run tests to verify it passes**
  Run: `pytest tests/unit/test_logger_manager.py -v` -> Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add src/logger_manager.py tests/unit/test_logger_manager.py
  git commit -m "feat: implement RotatingFileHandler logging and corresponding unit tests"
  ```

---

### Task 4: Implement Ingestion Unit Tests

**Files:**
- Create: `tests/unit/test_ingestion.py`

- [ ] **Step 1: Write test_ingestion.py**
  Tulis unit test untuk fungsi internal `src/ingestion.py`:
  ```python
  import pytest
  from unittest.mock import MagicMock
  from src.ingestion import _make_chunk_id, _parse_and_chunk, _embed_with_retry

  @pytest.mark.offline
  class TestIngestion:
      def test_make_chunk_id(self):
          h1 = _make_chunk_id("doc_1", "konten")
          h2 = _make_chunk_id("doc_1", "konten")
          h3 = _make_chunk_id("doc_1", "konten2")
          assert h1 == h2
          assert h1 != h3
          assert len(h1) == 32

      def test_parse_and_chunk_missing_yaml(self, tmp_path):
          file_path = tmp_path / "test_missing.md"
          file_path.write_text("---\ntitle: Judul\ncategory: Peraturan\n---\nKonten", encoding="utf-8")
          chunks = _parse_and_chunk(file_path, chunk_size=500, chunk_overlap=50)
          assert chunks == []

      def test_parse_and_chunk_valid(self, tmp_path):
          file_path = tmp_path / "test_valid.md"
          file_path.write_text("---\ndoc_id: pedoman_1\ntitle: Judul\ncategory: Peraturan\n---\n# Judul Pertama\n## Bab I\nIni konten peraturan akademik.", encoding="utf-8")
          chunks = _parse_and_chunk(file_path, chunk_size=500, chunk_overlap=50)
          assert len(chunks) > 0
          assert chunks[0]["doc_id"] == "pedoman_1"
          assert chunks[0]["title"] == "Judul"

      def test_embed_with_retry_success(self):
          mock_embedding_fn = MagicMock()
          mock_embedding_fn.embed_documents.return_value = [[0.1, 0.2]]
          res = _embed_with_retry(mock_embedding_fn, ["teks"])
          assert res == [[0.1, 0.2]]

      def test_embed_with_retry_failure(self):
          mock_embedding_fn = MagicMock()
          mock_embedding_fn.embed_documents.side_effect = Exception("API error")
          with pytest.raises(RuntimeError) as exc_info:
              _embed_with_retry(mock_embedding_fn, ["teks"], max_retries=2)
          assert "Embedding gagal setelah 2 attempt" in str(exc_info.value)
  ```

- [ ] **Step 2: Run test to make sure it passes**
  Run: `pytest tests/unit/test_ingestion.py -v` -> Expected: PASS

- [ ] **Step 3: Commit**
  ```bash
  git add tests/unit/test_ingestion.py
  git commit -m "test: add unit tests for ingestion parsing, hashing, and retry embedding logic"
  ```

---

### Task 5: Implement BM25 Retriever Unit Tests

**Files:**
- Create: `tests/unit/test_bm25_retriever.py`

- [ ] **Step 1: Write test_bm25_retriever.py**
  Tulis unit test untuk parser tokenisasi BM25 di `tests/unit/test_bm25_retriever.py`:
  ```python
  import pytest
  from src.bm25_retriever import _tokenize

  @pytest.mark.offline
  class TestBM25Retriever:
      def test_tokenize(self):
          tokens = _tokenize("Halo! Ini adalah kueri BM25.")
          assert "halo" in tokens
          assert "ini" in tokens
          assert "kueri" in tokens
          assert "bm25" in tokens
          assert "halo!" not in tokens

      def test_tokenize_short_tokens_filtered(self):
          tokens = _tokenize("a b c de fg")
          assert "a" not in tokens
          assert "de" in tokens
          assert "fg" in tokens
  ```

- [ ] **Step 2: Run test to make sure it passes**
  Run: `pytest tests/unit/test_bm25_retriever.py -v` -> Expected: PASS

- [ ] **Step 3: Commit**
  ```bash
  git add tests/unit/test_bm25_retriever.py
  git commit -m "test: add unit tests for BM25 tokenizer"
  ```

---

### Task 6: Implement Retriever Unit Tests

**Files:**
- Create: `tests/unit/test_retriever.py`

- [ ] **Step 1: Write test_retriever.py**
  Tulis unit test untuk `src/retriever.py` yang memvalidasi routing ke BM25 atau ChromaDB dan validasi filtering distance:
  ```python
  import pytest
  from unittest.mock import MagicMock, patch
  from src.retriever import retrieve_chunks

  @pytest.mark.offline
  class TestRetriever:
      @patch("src.retriever.CHROMA_DIR_B")
      @patch("src.retriever.chromadb.PersistentClient")
      def test_retrieve_chunks_config_b_empty(self, mock_client_class, mock_chroma_dir):
          mock_client = MagicMock()
          mock_client_class.return_value = mock_client
          mock_collection = MagicMock()
          mock_client.get_collection.return_value = mock_collection
          
          mock_collection.query.return_value = {
              "ids": [[]],
              "documents": [[]],
              "metadatas": [[]],
              "distances": [[]]
          }
          
          res = retrieve_chunks("syarat yudisium", "b")
          assert res == []

      @patch("src.retriever.CHROMA_DIR_B")
      @patch("src.retriever.chromadb.PersistentClient")
      def test_retrieve_chunks_config_b_filtered_by_threshold(self, mock_client_class, mock_chroma_dir):
          mock_client = MagicMock()
          mock_client_class.return_value = mock_client
          mock_collection = MagicMock()
          mock_client.get_collection.return_value = mock_collection
          
          mock_collection.query.return_value = {
              "ids": [["c1", "c2"]],
              "documents": [["Dokumen lolos", "Dokumen tidak lolos"]],
              "metadatas": [[{"doc_id": "d1"}, {"doc_id": "d2"}]],
              "distances": [[0.3, 0.8]]
          }
          
          res = retrieve_chunks("test query", "b")
          assert len(res) == 1
          assert res[0]["content"] == "Dokumen lolos"
  ```

- [ ] **Step 2: Run test to verify it passes**
  Run: `pytest tests/unit/test_retriever.py -v` -> Expected: PASS

- [ ] **Step 3: Commit**
  ```bash
  git add tests/unit/test_retriever.py
  git commit -m "test: add unit tests for retrieval selection and threshold filter"
  ```

---

### Task 7: Implement RAG Chain Unit Tests

**Files:**
- Create: `tests/unit/test_chain.py`

- [ ] **Step 1: Write test_chain.py**
  Tulis unit test untuk `src/chain.py` yang memvalidasi output token, latensi, logging, dan formatting sitasi:
  ```python
  import pytest
  from unittest.mock import MagicMock, patch
  from src.chain import run_rag_chain

  @pytest.mark.offline
  class TestChain:
      @patch("src.chain.retrieve_chunks")
      @patch("src.chain.log_chat_transaction")
      def test_run_rag_chain_config_b(self, mock_log_chat, mock_retrieve):
          mock_retrieve.return_value = [
              {
                  "content": "SKS maksimal adalah 24 SKS per semester.",
                  "doc_id": "pedoman_1",
                  "title": "Pedoman Akademik",
                  "category": "peraturan",
                  "distance": 0.1
              }
          ]
          
          res = run_rag_chain(
              query="Berapa SKS maksimal?",
              config_choice="b",
              model_name="gemini-3.5-flash"
          )
          
          assert res["found_state"] is True
          assert "SKS" in res["answer"]
          assert len(res["sources"]) == 1
          assert res["sources"][0]["doc_id"] == "pedoman_1"
          mock_log_chat.assert_called_once()
  ```

- [ ] **Step 2: Run test to verify it passes**
  Run: `pytest tests/unit/test_chain.py -v` -> Expected: PASS

- [ ] **Step 3: Commit**
  ```bash
  git add tests/unit/test_chain.py
  git commit -m "test: add unit tests for RAG chain orchestration and logger tracking"
  ```

---

### Task 8: Implement FastAPI Exception Logging Middleware & Integration Tests

**Files:**
- Modify: `app.py`
- Create: `tests/integration/test_chat_api.py`

- [ ] **Step 1: Write test_chat_api.py first (TDD)**
  Tulis test di `tests/integration/test_chat_api.py` untuk menguji endpoint chat sukses dan menangkap exception lewat middleware:
  ```python
  import pytest
  from fastapi.testclient import TestClient
  from unittest.mock import patch
  from app import app

  client = TestClient(app)

  @pytest.mark.offline
  class TestChatAPI:
      @patch("app.run_rag_chain")
      def test_chat_endpoint_success(self, mock_run_chain):
          mock_run_chain.return_value = {
              "answer": "SKS maksimal adalah 24 SKS [1].",
              "sources": [{"doc_id": "pedoman_1", "title": "Pedoman", "category": "peraturan"}],
              "found_state": True,
              "response_time": 1.23,
              "tokens": {"prompt": 10, "completion": 5, "total": 15}
          }
          
          payload = {
              "query": "Berapa SKS?",
              "config": "b",
              "model": "gemini-1.5-flash"
          }
          response = client.post("/api/chat", json=payload)
          assert response.status_code == 200
          json_data = response.json()
          assert "answer" in json_data
          assert json_data["answer"] == "SKS maksimal adalah 24 SKS [1]."

      @patch("app.run_rag_chain")
      def test_chat_endpoint_internal_error_middleware(self, mock_run_chain):
          mock_run_chain.side_effect = ValueError("Koneksi gagal tak terduga")
          
          payload = {
              "query": "Berapa SKS?",
              "config": "b",
              "model": "gemini-1.5-flash"
          }
          response = client.post("/api/chat", json=payload)
          assert response.status_code == 500
          json_data = response.json()
          assert "detail" in json_data
          assert "Terjadi kesalahan internal pada server" in json_data["detail"]
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/integration/test_chat_api.py -v` (Fails on unhandled exception crash, returns HTML/traceback error page instead of a nice JSONResponse 500)

- [ ] **Step 3: Implement global exception handler middleware in app.py**
  Tambahkan middleware exception handler di `app.py`:
  ```python
  from fastapi.responses import JSONResponse
  from src.logger_manager import get_logger

  # Import get_logger jika belum
  logger = get_logger("app")

  @app.exception_handler(Exception)
  async def global_exception_handler(request, exc):
      logger.exception(f"Unhandled exception occurred during request: {request.url.path}")
      return JSONResponse(
          status_code=500,
          content={"detail": "Terjadi kesalahan internal pada server. Silakan hubungi administrator."}
      )
  ```

- [ ] **Step 4: Run all tests to verify they all pass**
  Run: `pytest -m offline`
  Pastikan seluruh test (unit & integration) berhasil dijalankan secara offline dan 100% PASS.

- [ ] **Step 5: Commit**
  ```bash
  git add app.py tests/integration/test_chat_api.py
  git commit -m "feat: implement global exception logging middleware and integration test for chat API"
  ```
