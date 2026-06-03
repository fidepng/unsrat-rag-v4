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
        mock_response.content = "Berdasarkan pedoman akademik [1], mahasiswa dapat mengambil maksimal 24 SKS."
        mock_instance.invoke.return_value = mock_response
        yield mock_instance
