import pytest
from src.bm25_retriever import _tokenize

@pytest.mark.offline
class TestBM25Retriever:
    def test_tokenize(self):
        tokens = _tokenize("Halo! Ini adalah kueri BM25.")
        assert "halo" in tokens
        assert "ini" in tokens
        assert "adalah" in tokens
        assert "kueri" in tokens
        assert "bm25" in tokens
        assert "halo!" not in tokens

    def test_tokenize_short_tokens_filtered(self):
        tokens = _tokenize("a b c de fg")
        assert "a" not in tokens
        assert "b" not in tokens
        assert "c" not in tokens
        assert "de" in tokens
        assert "fg" in tokens
