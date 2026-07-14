import os
import sys
import time
import difflib
from pathlib import Path
from dotenv import load_dotenv
import frontmatter
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- BEGIN RAGAS COMPATIBILITY HACK (dari script asli, dipertahankan) ---
import types
if 'langchain_community.chat_models' not in sys.modules:
    sys.modules['langchain_community.chat_models'] = types.ModuleType('langchain_community.chat_models')
if 'langchain_community.chat_models.vertexai' not in sys.modules:
    dummy_cv = types.ModuleType('langchain_community.chat_models.vertexai')
    dummy_cv.ChatVertexAI = None
    sys.modules['langchain_community.chat_models.vertexai'] = dummy_cv
if 'langchain_community.llms' not in sys.modules:
    dummy_llms = types.ModuleType('langchain_community.llms')
    dummy_llms.VertexAI = None
    sys.modules['langchain_community.llms'] = dummy_llms
# --- END RAGAS COMPATIBILITY HACK ---

from ragas.testset import TestsetGenerator
from ragas import RunConfig

env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# ── KONFIGURASI ANTI-LEAKAGE ──────────────────────────────────────────
# Testset ini KHUSUS untuk kalibrasi SIMILARITY_THRESHOLD.
# TIDAK BOLEH digabung/dipakai sebagai bagian dari eval/dataset/ground_truth.csv.
GROUND_TRUTH_PATH   = Path("eval/dataset/ground_truth.csv")
CALIBRATION_OUTPUT  = Path("eval/dataset/calibration_testset.csv")
SIMILARITY_DEDUP_CUTOFF = 0.55  # difflib ratio; lebih rendah = lebih ketat membuang kandidat mirip


def generate_calibration_testset():
    print("Initializing LLMs...")
    kwargs_llm = {"model": "gemini-3.1-pro-preview", "max_retries": 2, "timeout": 120}
    kwargs_emb = {"model": "models/gemini-embedding-001", "max_retries": 2, "timeout": 30}

    sys.path.append(str(Path(__file__).parent.parent))
    from src.config import (
        GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GOOGLE_API_KEY,
        CHUNK_SIZE_B, CHUNK_OVERLAP_B,
    )

    if GOOGLE_APPLICATION_CREDENTIALS:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        kwargs_llm["credentials"] = creds
        kwargs_llm["project"] = GCP_PROJECT_ID
        kwargs_emb["credentials"] = creds
        kwargs_emb["project"] = GCP_PROJECT_ID
    else:
        kwargs_llm["google_api_key"] = GOOGLE_API_KEY
        kwargs_emb["google_api_key"] = GOOGLE_API_KEY

    generator_llm = ChatGoogleGenerativeAI(**kwargs_llm)
    embeddings = GoogleGenerativeAIEmbeddings(**kwargs_emb)

    print("Initializing TestsetGenerator...")
    generator = TestsetGenerator.from_langchain(
        llm=generator_llm,
        embedding_model=embeddings
    )

    corpus_dir = Path("data/corpus")
    raw_docs = []

    if not corpus_dir.exists():
        print(f"Error: {corpus_dir} does not exist. Please run from project root.")
        return

    for md_file in corpus_dir.glob("*.md"):
        post = frontmatter.load(md_file)
        raw_docs.append(Document(page_content=post.content, metadata=post.metadata))

    print(f"Loaded {len(raw_docs)} documents from corpus.")

    # NOTE (perbaikan dari versi asli): pakai chunk_size/overlap yang SAMA dengan
    # konfigurasi produksi (CHUNK_SIZE_B/CHUNK_OVERLAP_B di src/config.py), bukan
    # angka hardcoded terpisah (1500/200), supaya pertanyaan yang digenerate
    # mencerminkan granularitas context yang sama dengan yang dipakai retriever asli.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE_B,
        chunk_overlap=CHUNK_OVERLAP_B,
    )
    docs = text_splitter.split_documents(raw_docs)
    print(f"Split into {len(docs)} chunks for stable Ragas processing.")

    run_config = RunConfig(max_workers=16, timeout=300, max_retries=10)

    # testset_size dinaikkan ke 25: cukup untuk calibration set yang lebih robust
    # (n=25 relevan) dibanding 5 query manual sebelumnya, tapi tetap murah/cepat
    # karena akan disaring lagi (dedup) setelah ini.
    print("Generating synthetic calibration testset. This may take a while...")
    testset = generator.generate_with_chunks(
        chunks=docs,
        testset_size=25,
        run_config=run_config
    )

    df = testset.to_pandas()
    print(f"Generated {len(df)} raw synthetic questions.")

    # ── DEDUP / ANTI-LEAKAGE CHECK ──────────────────────────────────────
    # Buang kandidat yang mirip (paraphrase-level) dengan ground_truth.csv,
    # supaya calibration set benar-benar independen dari eval set final.
    if GROUND_TRUTH_PATH.exists():
        gt = pd.read_csv(GROUND_TRUTH_PATH)
        gt_questions = gt["user_input"].astype(str).tolist()

        keep_mask = []
        dropped = []
        for q in df["user_input"].astype(str):
            close = difflib.get_close_matches(q, gt_questions, n=1, cutoff=SIMILARITY_DEDUP_CUTOFF)
            if close:
                keep_mask.append(False)
                dropped.append((q, close[0]))
            else:
                keep_mask.append(True)

        if dropped:
            print(f"\n[ANTI-LEAKAGE] {len(dropped)} pertanyaan dibuang karena mirip ground_truth.csv:")
            for q, match in dropped:
                print(f"  - '{q[:60]}...' ~ '{match[:60]}...'")

        df = df[keep_mask].reset_index(drop=True)
        print(f"\n[ANTI-LEAKAGE] Tersisa {len(df)} pertanyaan bersih untuk calibration set.")
    else:
        print(f"[WARNING] {GROUND_TRUTH_PATH} tidak ditemukan — dedup leakage check DILEWATI. "
              f"Cek manual sebelum dipakai kalibrasi!")

    CALIBRATION_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CALIBRATION_OUTPUT, index=False)
    print(f"\nCalibration testset saved to {CALIBRATION_OUTPUT}")
    print("INGAT: file ini HANYA untuk kalibrasi threshold, JANGAN digabung ke ground_truth.csv.")


if __name__ == "__main__":
    generate_calibration_testset()