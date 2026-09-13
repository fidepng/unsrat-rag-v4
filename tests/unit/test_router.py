# tests/unit/test_router.py
import pytest
from src.router import check_greeting_intent

@pytest.mark.offline
def test_pure_greetings_detected():
    """Verifikasi sapaan umum murni menghasilkan jawaban ramah."""
    greetings = [
        "halo", "Halo!", "HALO", "hai", "Hai!", "hello", "hi", "hei",
        "p", "P", "tes", "test", "permisi", "halooo", "haiiii"
    ]
    for g in greetings:
        res = check_greeting_intent(g)
        assert res is not None, f"Gagal mengenali sapaan murni: {g}"
        assert "Asisten Akademik UNSRAT" in res

@pytest.mark.offline
def test_time_based_greetings_detected():
    """Verifikasi salam waktu (pagi, siang, sore, malam) dikenali dan dijawab spesifik."""
    time_greetings = [
        ("selamat pagi", "Selamat pagi"),
        ("Selamat Siang!", "Selamat siang"),
        ("selamat sore", "Selamat sore"),
        ("Selamat Malam", "Selamat malam"),
    ]
    for phrase, expected_phrase in time_greetings:
        res = check_greeting_intent(phrase)
        assert res is not None, f"Gagal mengenali salam waktu: {phrase}"
        assert expected_phrase.lower() in res.lower()

@pytest.mark.offline
def test_religious_and_closing_greetings_detected():
    """Verifikasi salam religius/kultural dan ucapan terima kasih."""
    salam_list = ["assalamu'alaikum", "assalamualaikum", "shalom", "salam", "Salam!"]
    for s in salam_list:
        res = check_greeting_intent(s)
        assert res is not None, f"Gagal mengenali salam: {s}"
        assert "Salam" in res or "Asisten Akademik" in res

    closing_list = ["terima kasih", "makasih", "Terima kasih banyak!", "thanks", "thank you"]
    for c in closing_list:
        res = check_greeting_intent(c)
        assert res is not None, f"Gagal mengenali ucapan terima kasih: {c}"
        assert "Sama-sama" in res

@pytest.mark.offline
def test_compound_queries_pass_to_rag():
    """Verifikasi pertanyaan majemuk (sapaan + pertanyaan akademik) TIDAK dicegat (return None)."""
    compound_queries = [
        "Halo, berapa sks semester 1?",
        "Selamat pagi, apa syarat cuti akademik?",
        "Hai, tolong jelaskan prosedur pengisian KRS",
        "Halo apa itu MBKM?",
        "Permisi, jadwal wisuda tahun ini kapan?",
        "Halo admin, berapa biaya UKT?",
        "Selamat siang, bagaimana cara menghubungi dosen PA?",
    ]
    for cq in compound_queries:
        res = check_greeting_intent(cq)
        assert res is None, f"Pertanyaan majemuk keliru dicegat router: {cq}"

@pytest.mark.offline
def test_pure_academic_queries_pass_to_rag():
    """Verifikasi kueri akademik reguler murni lolos langsung ke RAG (return None)."""
    academic_queries = [
        "Syarat cuti akademik?",
        "Visi dan Misi UNSRAT?",
        "Beban SKS semester 1?",
        "Jadwal Wisuda tahun ini?",
        "Prosedur pengisian KRS?",
        "Berapa batas masa studi program sarjana?",
        "Bagaimana sanksi jika terlambat membayar UKT?",
    ]
    for aq in academic_queries:
        res = check_greeting_intent(aq)
        assert res is None, f"Kueri akademik keliru dicegat router: {aq}"

@pytest.mark.offline
def test_empty_or_invalid_inputs():
    """Verifikasi input kosong atau hanya tanda baca tidak memicu router."""
    invalids = ["", "   ", "...", "???", "!!!", "---"]
    for inv in invalids:
        assert check_greeting_intent(inv) is None

@pytest.mark.offline
def test_identity_queries_detected():
    """Verifikasi kueri menanyakan identitas bot dijawab dengan perkenalan Asisten Akademik."""
    identity_queries = [
        "siapa anda", "siapa anda?", "kamu siapa", "siapa kamu",
        "siapakah anda", "anda siapa", "siapakah kamu?"
    ]
    for q in identity_queries:
        res = check_greeting_intent(q)
        assert res is not None, f"Gagal mengenali kueri identitas: {q}"
        assert "Asisten Akademik UNSRAT" in res

@pytest.mark.offline
def test_capability_queries_detected():
    """Verifikasi kueri menanyakan fungsi/kapabilitas bot dijawab dengan panduan fitur."""
    capability_queries = [
        "apa bisa anda lakukan", "apa yang bisa anda lakukan",
        "apa yang bisa kamu lakukan?", "kamu bisa apa", "anda bisa apa",
        "apa fungsi anda", "bisa bantu apa", "apa kegunaan anda"
    ]
    for q in capability_queries:
        res = check_greeting_intent(q)
        assert res is not None, f"Gagal mengenali kueri kapabilitas: {q}"
        assert "membantu" in res or "akademik UNSRAT" in res

@pytest.mark.offline
def test_academic_who_and_what_queries_pass_to_rag():
    """Verifikasi kueri siapa/apa yang menyangkut pejabat/kebijakan akademik kampus tetap lolos ke RAG."""
    queries = [
        "Siapa rektor UNSRAT?",
        "Siapa dekan fakultas teknik?",
        "Apa yang harus dilakukan jika terlambat bayar UKT?",
        "Apa sanksi jika melanggar aturan akademik?",
        "Siapa yang menandatangani KRS?",
    ]
    for q in queries:
        res = check_greeting_intent(q)
        assert res is None, f"Kueri akademik siapa/apa keliru dicegat router: {q}"

@pytest.mark.offline
def test_ground_truth_never_intercepted():
    """Verifikasi seluruh 361 pertanyaan evaluasi di ground_truth.csv 100% lolos ke RAG."""
    import pandas as pd
    from pathlib import Path
    gt_path = Path("eval/dataset/ground_truth.csv")
    if not gt_path.exists():
        pytest.skip("ground_truth.csv tidak ditemukan")
    df = pd.read_csv(gt_path)
    for idx, row in df.iterrows():
        q = str(row["user_input"])
        res = check_greeting_intent(q)
        assert res is None, f"Pertanyaan evaluasi baris {idx} terintercept oleh router: '{q}'"


