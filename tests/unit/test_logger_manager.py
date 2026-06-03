import pytest
import csv
import os
from src.logger_manager import get_logger, log_ingestion_report, log_chat_transaction, _reset_logger_manager

@pytest.fixture(autouse=True)
def clean_logger_state(tmp_path, monkeypatch):
    # Reset state logger_manager before test
    _reset_logger_manager()
    
    # Patch directory & file paths to fully isolate the tests
    test_logs_dir = tmp_path / "logs"
    monkeypatch.setattr("src.logger_manager.LOGS_DIR", test_logs_dir)
    monkeypatch.setattr("src.logger_manager.SYSTEM_LOG_PATH", test_logs_dir / "unsrat_rag.log")
    monkeypatch.setattr("src.logger_manager.INGESTION_LOG_PATH", test_logs_dir / "ingestion_report.csv")
    monkeypatch.setattr("src.logger_manager.CHAT_LOG_PATH", test_logs_dir / "transaksi_chat.csv")
    
    yield
    
    # Reset state logger_manager after test
    _reset_logger_manager()

@pytest.mark.offline
class TestLoggerManager:
    def test_logger_creation(self):
        logger = get_logger("test_logger_unit")
        assert logger.name == "test_logger_unit"
        assert len(logger.handlers) >= 2
        
        # Verify both loggers write through the same shared handlers
        logger2 = get_logger("test_logger_unit_2")
        assert logger2.handlers == logger.handlers

    def test_log_ingestion_report(self):
        from src.logger_manager import INGESTION_LOG_PATH
        
        log_ingestion_report(
            config="a",
            files_processed=5,
            chunks_generated=20,
            chunks_inserted=18,
            chunks_duplicate_skipped=2,
            chunks_too_short_skipped=0,
            execution_time_seconds=12.34
        )
        assert INGESTION_LOG_PATH.exists()
        with open(INGESTION_LOG_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) == 1
            row = reader[0]
            
            # Verify complete CSV schema fields and contents
            assert "timestamp" in row
            assert row["config"] == "a"
            assert row["files_processed"] == "5"
            assert row["chunks_generated"] == "20"
            assert row["chunks_inserted"] == "18"
            assert row["chunks_duplicate_skipped"] == "2"
            assert row["chunks_too_short_skipped"] == "0"
            assert row["execution_time_seconds"] == "12.34"

    def test_log_chat_transaction(self):
        from src.logger_manager import CHAT_LOG_PATH
        
        long_query = "Halo " * 100 # >200 characters to check truncation
        log_chat_transaction(
            config="b",
            model_llm="gemini-3.5-flash",
            user_query=long_query,
            chunks_retrieved_count=2,
            retrieved_chunk_ids=["id1", "id2"],
            best_similarity_score=0.123456,
            average_similarity_score=0.456789,
            response_time_seconds=1.5678,
            estimated_prompt_tokens=100,
            estimated_completion_tokens=50,
            estimated_total_tokens=150,
            found_state=True,
            answer_preview="Preview " * 100
        )
        assert CHAT_LOG_PATH.exists()
        with open(CHAT_LOG_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) == 1
            row = reader[0]
            
            # Verify complete CSV schema fields and contents
            assert "timestamp" in row
            assert row["config"] == "b"
            assert row["model_llm"] == "gemini-3.5-flash"
            # Verify truncation to 200 chars
            assert len(row["user_query"]) == 200
            assert row["user_query"] == long_query[:200]
            assert row["chunks_retrieved_count"] == "2"
            # Verify list format
            assert row["retrieved_chunk_ids"] == "id1|id2"
            # Verify rounding to 4 decimals
            assert row["best_similarity_score"] == "0.1235"
            assert row["average_similarity_score"] == "0.4568"
            assert row["response_time_seconds"] == "1.5678"
            assert row["estimated_prompt_tokens"] == "100"
            assert row["estimated_completion_tokens"] == "50"
            assert row["estimated_total_tokens"] == "150"
            # Verify boolean serialization
            assert row["found_state"] == "True"
            assert len(row["answer_preview"]) == 200
