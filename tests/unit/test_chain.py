import pytest
from unittest.mock import MagicMock, patch
from src.chain import run_rag_chain

@pytest.mark.offline
class TestChain:
    @patch("src.chain.retrieve_chunks")
    @patch("src.chain.log_chat_transaction")
    def test_run_rag_chain_config_b(self, mock_log_chat, mock_retrieve):
        # Mock retrieval returning a single valid chunk
        mock_retrieve.return_value = [
            {
                "content": "SKS maksimal adalah 24 SKS per semester.",
                "doc_id": "pedoman_1",
                "title": "Pedoman Akademik",
                "category": "peraturan",
                "distance": 0.1
            }
        ]
        
        # Call run_rag_chain
        res = run_rag_chain(
            query="Berapa SKS maksimal?",
            config_choice="b",
            model_name="nvidia/llama-3.1-nemotron-nano-8b-v1"
        )
        
        assert res["found_state"] is True
        assert "SKS" in res["answer"]
        assert len(res["sources"]) == 1
        assert res["sources"][0]["doc_id"] == "pedoman_1"
        mock_log_chat.assert_called_once()
