import pytest
from unittest.mock import MagicMock, patch
import src.retriever
from src.retriever import retrieve_chunks

@pytest.mark.offline
class TestRetriever:
    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        src.retriever._chroma_collections.clear()
        src.retriever._chroma_clients.clear()
        with patch("src.retriever._get_embedding_fn") as mock_get_fn:
            mock_emb = MagicMock()
            mock_emb.embed_query.return_value = [0.1, 0.2, 0.3]
            mock_get_fn.return_value = mock_emb
            yield

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
