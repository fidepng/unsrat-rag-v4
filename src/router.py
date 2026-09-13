# src/router.py — Pre-RAG Intent Router untuk Sapaan & Percakapan Ringan
# Menangani kueri sapaan umum secara deterministik tanpa memanggil retrieval atau generator LLM.
# Menghindari fallback "Maaf, tidak menemukan informasi" saat user menyapa,
# sekaligus menjaga isolasi evaluasi RAGAS (0 false positive pada kueri regulasi).

import re
import unicodedata

# Daftar kata tanya / interogatif yang menandakan kueri substantif
QUESTION_WORDS = {
    "apa", "apakah", "bagaimana", "kapan", "berapa", "kenapa", "mengapa",
    "siapa", "dimana", "mana", "tolong", "jelaskan", "sebutkan", "bisa",
    "bolehkah", "adakah", "caranya", "cara", "syarat", "langkah",
}

# Daftar entitas dan terminologi akademik domain UNSRAT
ACADEMIC_TERMS = {
    "krs", "sks", "cuti", "wisuda", "skripsi", "ukt", "bop", "ipk", "ips",
    "dosen", "dekan", "rektor", "fakultas", "jurusan", "prodi", "matakuliah",
    "matkul", "jadwal", "perkuliahan", "akademik", "registrasi", "kkt", "kkn",
    "mbkm", "magang", "sidang", "semhas", "yudisium", "ijazah", "transkrip",
    "aturan", "pedoman", "peraturan", "biaya", "pembayaran", "beasiswa",
    "kuliah", "tugas", "ujian", "uts", "uas", "semester", "unsrat",
}

# Pola regex sapaan waktu
TIME_PATTERNS = [
    (re.compile(r"^selamat\s+pagi\b", re.IGNORECASE), "Selamat pagi! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu mengenai informasi atau regulasi akademik UNSRAT?"),
    (re.compile(r"^selamat\s+siang\b", re.IGNORECASE), "Selamat siang! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu mengenai informasi atau regulasi akademik UNSRAT?"),
    (re.compile(r"^selamat\s+sore\b", re.IGNORECASE), "Selamat sore! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu mengenai informasi atau regulasi akademik UNSRAT?"),
    (re.compile(r"^selamat\s+malam\b", re.IGNORECASE), "Selamat malam! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu mengenai informasi atau regulasi akademik UNSRAT?"),
]

# Pola salam religius / kultural
RELIGIOUS_PATTERNS = [
    (re.compile(r"^(assalamu'?alaikum|assalamualaikum|assalam)\b", re.IGNORECASE), "Assalamu'alaikum! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu seputar informasi akademik atau perkuliahan di UNSRAT?"),
    (re.compile(r"^(shalom|salom|syalom)\b", re.IGNORECASE), "Shalom! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu seputar informasi akademik atau perkuliahan di UNSRAT?"),
    (re.compile(r"^salam\b", re.IGNORECASE), "Salam! Saya Asisten Akademik UNSRAT. Ada yang bisa saya bantu seputar informasi akademik atau perkuliahan di UNSRAT?"),
]

# Pola sapaan umum kasual
GENERAL_PATTERNS = [
    re.compile(r"^(halo|hai|hello|hi|hei|p|tes|test|permisi)\b", re.IGNORECASE),
]

# Pola ucapan terima kasih / penutup
CLOSING_PATTERNS = [
    re.compile(r"^(terima\s*kasih|makasih|thanks|thank\s*you|makasi)\b", re.IGNORECASE),
]

# Pola pertanyaan identitas bot (siapa anda / kamu siapa)
IDENTITY_PATTERNS = [
    re.compile(r"^(siapa\s+(anda|kamu|bot|asisten)|(anda|kamu)\s+siapa|siapakah\s+(anda|kamu))\b", re.IGNORECASE),
]

IDENTITY_REPLY = (
    "Saya adalah Asisten Akademik UNSRAT, sistem cerdas berbasis "
    "Retrieval-Augmented Generation (RAG) yang dirancang untuk membantu mahasiswa "
    "dan civitas akademika memahami peraturan akademik, kurikulum, prosedur KRS, "
    "cuti, serta layanan akademik di Universitas Sam Ratulangi."
)

# Pola pertanyaan kapabilitas bot (apa yang bisa anda lakukan / bisa apa saja)
CAPABILITY_PATTERNS = [
    re.compile(r"^(apa\s+(saja\s+)?(yang\s+)?bisa\s+(anda|kamu)\s+(lakukan|bantu)|(anda|kamu)\s+bisa\s+apa|apa\s+(fungsi|kegunaan|peran)\s+(anda|kamu)|bisa\s+(bantu|tolong)\s+apa(\s+saja)?)\b", re.IGNORECASE),
]

CAPABILITY_REPLY = (
    "Saya dapat membantu Anda menemukan dan memahami informasi resmi akademik UNSRAT, seperti:\n"
    "1. Prosedur pengisian, persetujuan, dan perubahan KRS\n"
    "2. Ketentuan cuti akademik dan batas masa studi\n"
    "3. Beban SKS per semester dan syarat kelulusan\n"
    "4. Informasi pelaksanaan KKT/KKN dan wisuda\n"
    "5. Hak, kewajiban, dan sanksi akademik mahasiswa\n\n"
    "Silakan ketik pertanyaan spesifik yang ingin Anda ketahui!"
)


def _normalize_text(text: str) -> str:
    """Normalisasi teks: bersihkan aksen, tanda baca, dan lipat huruf berulang (haloooo -> halo)."""
    # Hapus aksen/diakritik
    nfkd = unicodedata.normalize("NFKD", text)
    clean = "".join(c for c in nfkd if not unicodedata.combining(c))
    
    # Lowercase & ganti tanda baca dengan spasi (kecuali apostrof untuk assalamu'alaikum)
    clean = clean.lower()
    clean = re.sub(r"[^\w\s']", " ", clean)
    
    # Reduksi huruf berulang lebih dari 2 kali (contoh: halooo -> halo, haiiii -> hai)
    clean = re.sub(r"(.)\1{2,}", r"\1", clean)
    
    return re.sub(r"\s+", " ", clean).strip()


def check_greeting_intent(query: str) -> str | None:
    """
    Evaluasi apakah query merupakan sapaan murni, pertanyaan identitas, atau kapabilitas.
    
    Returns:
        str: Pesan jawaban ramah/deskripsi jika terdeteksi.
        None: Jika kueri adalah pertanyaan akademik atau mengandung substansi (wajib diteruskan ke RAG).
    """
    if not query or not query.strip():
        return None

    normalized = _normalize_text(query)
    if not normalized:
        return None

    words = normalized.split()
    word_count = len(words)

    # ── GUARD 1: Panjang kata maksimum untuk intent percakapan ringan ───────────
    if word_count > 8:
        return None

    # ── GUARD 2: Jangan cegat jika mengandung istilah regulasi akademik ────────
    words_set = set(words)
    if words_set.intersection(ACADEMIC_TERMS):
        return None

    # ── IDENTITAS & KAPABILITAS ASISTEN ────────────────────────────────────────
    for pattern in IDENTITY_PATTERNS:
        if pattern.search(normalized):
            return IDENTITY_REPLY

    for pattern in CAPABILITY_PATTERNS:
        if pattern.search(normalized):
            return CAPABILITY_REPLY

    # ── GUARD 3: Untuk sapaan standar, abaikan jika mengandung kata tanya ───────
    if words_set.intersection(QUESTION_WORDS):
        return None

    # ── EVALUASI POLA SAPAAN STANDAR ───────────────────────────────────────────

    # 1. Salam Waktu
    for pattern, reply in TIME_PATTERNS:
        if pattern.search(normalized):
            return reply

    # 2. Salam Religius / Kultural
    for pattern, reply in RELIGIOUS_PATTERNS:
        if pattern.search(normalized):
            return reply

    # 3. Ucapan Terima Kasih / Penutup
    for pattern in CLOSING_PATTERNS:
        if pattern.search(normalized):
            return (
                "Sama-sama! Senang bisa membantu. Jika masih ada hal lain yang "
                "ingin ditanyakan seputar akademik UNSRAT, silakan tanyakan kembali."
            )

    # 4. Sapaan Umum
    for pattern in GENERAL_PATTERNS:
        if pattern.search(normalized):
            return (
                "Halo! Saya Asisten Akademik UNSRAT. Silakan tanyakan informasi "
                "seputar perkuliahan, regulasi, KRS, cuti, atau hal akademik lainnya di UNSRAT."
            )

    return None
