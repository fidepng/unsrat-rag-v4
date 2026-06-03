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
        assert chunks[0]["metadata"]["doc_id"] == "pedoman_1"
        assert chunks[0]["metadata"]["title"] == "Judul"

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
