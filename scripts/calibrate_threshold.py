# scripts/calibrate_threshold.py
# Kalibrasi empiris SIMILARITY_THRESHOLD (D-B7)
# Jalankan: python scripts/calibrate_threshold.py
# Hasil digunakan untuk memvalidasi atau menyesuaikan nilai threshold di config.py

import sys
from pathlib import Path
# Bypass ModuleNotFoundError ketika dijalankan langsung sebagai script mandiri
sys.path.append(str(Path(__file__).parent.parent))

import traceback
import chromadb
from chromadb.config import Settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import (
    CHROMA_DIR_B, CHROMA_COLLECTION_B,
    EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, RETRIEVAL_K, SIMILARITY_THRESHOLD,
    GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID
)
from src.logger_manager import get_logger

# Inisialisasi logger terpusat untuk audit trail skripsi
logger = get_logger("calibrate_threshold")

print(f"\n{'='*70}")
print(f"       AUTOMATED SIMILARITY THRESHOLD CALIBRATOR — CONFIG B")
print(f"       Threshold Aktif Saat Ini di config.py: {SIMILARITY_THRESHOLD}")
print(f"{'='*70}")

logger.info("Memulai proses kalibrasi empiris SIMILARITY_THRESHOLD (D-B7)")

# 1. Validasi Keberadaan Database & Koneksi (Tangguh/Anti-Crash)
try:
    if not CHROMA_DIR_B.exists():
        raise FileNotFoundError(f"Direktori database '{CHROMA_DIR_B}' tidak ditemukan.")
    
    # Menonaktifkan telemetri anonymized ChromaDB untuk melenyapkan log telemetry error (D-B7 Best Practice)
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR_B),
        settings=Settings(anonymized_telemetry=False)
    )
    
    collection = client.get_collection(CHROMA_COLLECTION_B)
    
    # Cek apakah koleksi kosong
    if collection.count() == 0:
        raise ValueError(f"Koleksi '{CHROMA_COLLECTION_B}' terdeteksi kosong (0 chunks).")
        
    logger.info(f"Koneksi ChromaDB berhasil. Jumlah chunk terdaftar: {collection.count()}")

except Exception as e:
    err_msg = (
        f"\n[FATAL ERROR] Gagal menghubungkan ke ChromaDB!\n"
        f"Detail Error: {str(e)}\n\n"
        f"👉 SOLUSI: Harap pastikan Anda telah menjalankan pipeline ingestion terlebih dahulu\n"
        f"           untuk memasukkan dokumen akademik ke database dengan perintah:\n"
        f"           python src/ingestion.py\n"
    )
    print(err_msg)
    logger.error(f"Koneksi ChromaDB Gagal: {str(e)}", exc_info=True)
    sys.exit(1)

# Inisialisasi model embedding Google GenAI
try:
    gemini_emb_kwargs = {
        "model": EMBEDDING_MODEL_NAME,
        "task_type": "retrieval_query",
    }
    
    if GOOGLE_APPLICATION_CREDENTIALS:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        gemini_emb_kwargs["credentials"] = creds
        gemini_emb_kwargs["project"] = GCP_PROJECT_ID
    else:
        gemini_emb_kwargs["google_api_key"] = GOOGLE_API_KEY

    embedding_fn = GoogleGenerativeAIEmbeddings(**gemini_emb_kwargs)
except Exception as e:
    err_msg = (
        f"\n[FATAL ERROR] Gagal menginisialisasi Google GenAI Embeddings!\n"
        f"Detail Error: {str(e)}\n\n"
        f"👉 SOLUSI: Periksa koneksi internet Anda dan pastikan nilai GOOGLE_API_KEY di berkas .env\n"
        f"           sudah terkonfigurasi dengan benar.\n"
    )
    print(err_msg)
    logger.error(f"Inisialisasi Embeddings Gagal: {str(e)}", exc_info=True)
    sys.exit(1)

import pandas as pd
CALIBRATION_TESTSET_PATH = Path("eval/dataset/calibration_testset.csv")

relevant_queries = []
if CALIBRATION_TESTSET_PATH.exists():
    try:
        df_cal = pd.read_csv(CALIBRATION_TESTSET_PATH)
        if "user_input" in df_cal.columns:
            relevant_queries = df_cal["user_input"].dropna().astype(str).tolist()
            logger.info(f"Berhasil memuat {len(relevant_queries)} kueri relevan dari {CALIBRATION_TESTSET_PATH}")
    except Exception as e:
        logger.error(f"Gagal memuat calibration set: {e}")

# Fallback ke hardcoded jika gagal atau kosong
if not relevant_queries:
    logger.warning("Menggunakan kueri relevan hardcoded sebagai fallback.")
    relevant_queries = [
        "berapa SKS maksimal per semester", # Baku
        "syarat yudisium sarjana", # Baku
        "kalo mau cuti kuliah tuh gimana ya bang caranya?", # Slang / Gaul
        "Who be the rector in records from Juli 2014?", # Bahasa inggris terjemahan
        "kalo ketauan skripsinya nyontek/plagiat konsekuensinya apa", # Slang / Parafrase
    ]

# 5 kueri TIDAK RELEVAN umum
irrelevant_queries = [
        "harga makan siang di kantin", # Out of domain mutlak
        "resep masak ayam goreng", # Out of domain mutlak
        "bagaimana cara daftar CPNS dosen kementerian pendidikan?", # Hard Negative (Akademik tapi bukan Unsrat)
        "syarat lulus LPDP luar negeri", # Hard Negative (Akademik tapi bukan Unsrat)
        "siapa rektor universitas indonesia tahun ini", # Hard Negative (Tebakan menjebak)
    ]

# Penampung data statistik
relevant_top1 = []
relevant_all = []
irrelevant_top1 = []
irrelevant_all = []

# --- PROSES KUERI RELEVAN ---
print("\n>>> [1/2] Memproses Query RELEVAN (Harapan: Kosinus Kecil < Threshold)...")
logger.info("Memproses 5 kueri akademik relevan...")
for q in relevant_queries:
    try:
        emb = embedding_fn.embed_query(q)
        res = collection.query(query_embeddings=[emb], n_results=RETRIEVAL_K, include=["distances"])
        dists = res["distances"][0]
        
        # Validasi jika hasil query kosong
        if not dists:
            raise ValueError(f"Query '{q}' tidak mengembalikan chunk apapun.")
            
        relevant_top1.append(dists[0])
        relevant_all.extend(dists)
        
        log_line = f"  * '{q[:40]}...' -> Cosine Distances: {[f'{d:.3f}' for d in dists]}"
        print(log_line)
        logger.debug(f"Relevant query: '{q}' -> dists: {dists}")
        
    except Exception as e:
        print(f"  [ERROR] Gagal memproses query '{q}': {str(e)}")
        logger.error(f"Gagal memproses query relevan '{q}': {str(e)}")

# --- PROSES KUERI TIDAK RELEVAN ---
print("\n>>> [2/2] Memproses Query TIDAK RELEVAN (Harapan: Kosinus Besar > Threshold)...")
logger.info("Memproses 5 kueri luar domain tidak relevan...")
for q in irrelevant_queries:
    try:
        emb = embedding_fn.embed_query(q)
        res = collection.query(query_embeddings=[emb], n_results=RETRIEVAL_K, include=["distances"])
        dists = res["distances"][0]
        
        # Validasi jika hasil query kosong
        if not dists:
            raise ValueError(f"Query '{q}' tidak mengembalikan chunk apapun.")
            
        irrelevant_top1.append(dists[0])
        irrelevant_all.extend(dists)
        
        log_line = f"  * '{q[:40]}...' -> Cosine Distances: {[f'{d:.3f}' for d in dists]}"
        print(log_line)
        logger.debug(f"Irrelevant query: '{q}' -> dists: {dists}")
        
    except Exception as e:
        print(f"  [ERROR] Gagal memproses query '{q}': {str(e)}")
        logger.error(f"Gagal memproses query tidak relevan '{q}': {str(e)}")

# --- ANALISIS STATISTIK OTOMATIS (BEST PRACTICE) ---
if not relevant_top1 or not irrelevant_top1:
    print("\n[FATAL ERROR] Gagal mengumpulkan data kalibrasi yang cukup. Proses dihentikan.")
    logger.error("Kumpulan data kalibrasi kosong. Menghentikan kalkulasi.")
    sys.exit(1)

max_rev_top1 = max(relevant_top1)
avg_rev_top1 = sum(relevant_top1) / len(relevant_top1)
min_irr_top1 = min(irrelevant_top1)
avg_irr_top1 = sum(irrelevant_top1) / len(irrelevant_top1)

# Log data statistik awal ke file
logger.info(f"Statistik Relevan Top-1: max={max_rev_top1:.4f}, avg={avg_rev_top1:.4f}")
logger.info(f"Statistik Tidak Relevan Top-1: min={min_irr_top1:.4f}, avg={avg_irr_top1:.4f}")

print(f"\n{'='*70}")
print("[STATS] LAPORAN ANALISIS STATISTIK OTOMATIS")
print(f"{'='*70}")
print(f"  1. Kueri Relevan (Top-1 Match):")
print(f"     - Jarak Kosinus Terjauh (Max): {max_rev_top1:.3f}")
print(f"     - Rata-rata Jarak Kosinus (Avg): {avg_rev_top1:.3f}")
print(f"  2. Kueri Tidak Relevan (Top-1 Match):")
print(f"     - Jarak Kosinus Terdekat (Min): {min_irr_top1:.3f}")
print(f"     - Rata-rata Jarak Kosinus (Avg): {avg_irr_top1:.3f}")

print(f"\n[ANALISIS] Analisis Pemisahan Zona Semantik:")
if max_rev_top1 < min_irr_top1:
    gap = min_irr_top1 - max_rev_top1
    rec_threshold = (max_rev_top1 + min_irr_top1) / 2
    analysis_log = f"[OK] SUKSES: Ditemukan celah pemisahan sempurna sebesar {gap:.3f}! Batas keputusan tengah: {rec_threshold:.3f}"
    print(f"  [OK] SUKSES: Ditemukan celah pemisahan sempurna sebesar {gap:.3f}!")
    print(f"  [!] Batas Keputusan (Decision Boundary) Tengah: {rec_threshold:.3f}")
    logger.info(analysis_log)
else:
    # Terjadi overlap (jarak kueri relevan terjauh > kueri tidak relevan terdekat)
    overlap = max_rev_top1 - min_irr_top1
    # Pendekatan Berbasis Recall untuk RAG:
    # Threshold harus lebih besar dari jarak relevan terjauh (max_rev_top1) agar kueri relevan tidak terbuang (False Negatives).
    rec_threshold = max_rev_top1 + 0.01 
    
    analysis_log = f"[WARN] Terjadi tumpang tindih sebesar {overlap:.3f}. Menggunakan pendekatan Recall-Optimized. Rekomendasi: {rec_threshold:.3f}"
    print(f"  [WARN] PERINGATAN: Terjadi tumpang tindih (overlap) ruang vektor sebesar {overlap:.3f}.")
    print(f"  -> Jarak Relevan Terjauh (Max): {max_rev_top1:.3f}")
    print(f"  -> Jarak Irrelevan Terdekat (Min): {min_irr_top1:.3f}")
    print(f"  [INFO] Analisis: Secara empiris, jika menggunakan nilai rata-rata, kueri relevan terjauh ({max_rev_top1:.3f}) akan tertolak.")
    print(f"  [INFO] Memutuskan penggunaan metode 'Recall-Optimized Threshold' (Max Relevan + Margin 0.01).")
    print(f"  [!] Batas Keputusan Rekomendasi: {rec_threshold:.3f}")
    logger.warning(analysis_log)

# Berikan rekomendasi aksi konkret
print(f"\n[RECOMMENDATION] REKOMENDASI FORMAL UNTUK METODOLOGI SKRIPSI:")
print(f"  -> Nilai Threshold Optimal Berdasarkan Data Riil: {rec_threshold:.3f}")
logger.info(f"Rekomendasi threshold optimal hasil kalibrasi: {rec_threshold:.4f}")

# Hitung selisih dengan threshold saat ini
diff = abs(SIMILARITY_THRESHOLD - rec_threshold)
if SIMILARITY_THRESHOLD < max_rev_top1:
    print(f"  [CRITICAL] Nilai saat ini ({SIMILARITY_THRESHOLD}) LEBIH KECIL dari kueri relevan terjauh ({max_rev_top1:.3f}).")
    print(f"             Secara matematis, ini akan menolak pertanyaan valid dan menyebabkan skor Context Recall turun!")
    print(f"  [ACTION] Harap edit manual berkas 'src/config.py' baris 80, ubah menjadi:")
    print(f"           SIMILARITY_THRESHOLD = {rec_threshold:.3f}")
elif diff <= 0.02:
    print(f"  [OK] Nilai saat ini ({SIMILARITY_THRESHOLD}) sudah sangat dekat dengan nilai optimal. Tidak perlu diubah.")
    logger.info(f"Threshold saat ini ({SIMILARITY_THRESHOLD}) dinyatakan valid dan optimal.")
else:
    print(f"  [WARN] Nilai saat ini ({SIMILARITY_THRESHOLD}) kurang optimal (selisih {diff:.3f}).")
    print(f"  [ACTION] Harap edit manual berkas 'src/config.py' baris 80, ubah menjadi:")
    print(f"           SIMILARITY_THRESHOLD = {rec_threshold:.3f}")

print(f"{'='*70}\n")
logger.info("Kalibrasi SIMILARITY_THRESHOLD selesai dikerjakan.")
