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
