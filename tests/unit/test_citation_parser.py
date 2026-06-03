# tests/test_citation_parser.py
# Unit test untuk parse_cited_indices — fungsi kritis untuk citation system
# Jalankan: pytest tests/test_citation_parser.py -v

import pytest


# Import akan gagal sampai src/chain.py dibuat — ini intentional (TDD)
from src.chain import parse_cited_indices


@pytest.mark.offline
class TestParseCitedIndices:
    """Test suite untuk parse_cited_indices (PRD Section 6.5)."""

    def test_basic_citation(self):
        """Marker valid dalam range dikembalikan."""
        result = parse_cited_indices("Jawaban ini [1] benar.", max_source_index=3)
        assert result == [1]

    def test_multiple_citations(self):
        """Multiple marker valid dikembalikan sebagai sorted list."""
        result = parse_cited_indices("Dari [2] dan [1] serta [3].", max_source_index=3)
        assert result == [1, 2, 3]

    def test_duplicate_citations_deduplicated(self):
        """Marker yang sama tidak duplikat dalam hasil."""
        result = parse_cited_indices("[1] teks [1] teks [1]", max_source_index=2)
        assert result == [1]

    def test_out_of_range_ignored(self):
        """Marker di luar range max_source_index diabaikan tanpa crash."""
        result = parse_cited_indices("Referensi [5] tidak ada.", max_source_index=3)
        assert result == []

    def test_no_citation_returns_empty(self):
        """Teks tanpa marker mengembalikan list kosong, tidak crash."""
        result = parse_cited_indices("Jawaban tanpa referensi.", max_source_index=4)
        assert result == []

    def test_zero_max_source_index(self):
        """max_source_index=0 — semua marker di luar range."""
        result = parse_cited_indices("Teks [1].", max_source_index=0)
        assert result == []

    def test_mixed_valid_and_invalid(self):
        """Hanya marker dalam range yang dikembalikan."""
        result = parse_cited_indices("[1] valid, [10] tidak valid, [2] valid", max_source_index=3)
        assert result == [1, 2]

    def test_result_is_sorted(self):
        """Hasil selalu sorted ascending."""
        result = parse_cited_indices("[3] lalu [1] lalu [2]", max_source_index=5)
        assert result == [1, 2, 3]

    def test_empty_text_returns_empty(self):
        """String kosong mengembalikan list kosong."""
        result = parse_cited_indices("", max_source_index=4)
        assert result == []
