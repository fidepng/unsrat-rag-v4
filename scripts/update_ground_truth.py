import os
import time
import math
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from tqdm import tqdm

def load_entire_corpus(corpus_dir: Path) -> str:
    """Menggabungkan seluruh file markdown menjadi satu string raksasa."""
    all_text = []
    for md_file in sorted(corpus_dir.glob("*.md")):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            all_text.append(f"==================================================\n"
                            f"NAMA FILE: {md_file.name}\n"
                            f"==================================================\n"
                            f"{content}\n")
    return "\n".join(all_text)

# Definisi skema Pydantic untuk output
class GroundTruthOutput(BaseModel):
    reference: str = Field(description="Jawaban yang SANGAT DETAIL, komprehensif, dan mendalam berdasarkan korpus. Untuk pertanyaan multihop, jelaskan alur logikanya secara lengkap. Isi 'TIDAK DITEMUKAN' jika tidak ada di korpus.")
    source_doc: str = Field(description="Nama file tempat jawaban ditemukan, misal: '01_sejarah.md'. Kosongkan jika tidak ditemukan.")
    notes: str = Field(description="Pasal, Bab, atau bagian spesifik. Kosongkan jika tidak ditemukan.")

def main():
    # Load environment variables (API Key)
    load_dotenv()
    
    # Setup paths
    ROOT_DIR = Path(__file__).parent.parent
    DATASET_PATH = ROOT_DIR / "eval" / "dataset" / "ground_truth.csv"
    OUTPUT_PATH = ROOT_DIR / "eval" / "dataset" / "ground_truth_updated.csv"
    CORPUS_DIR = ROOT_DIR / "data" / "corpus"
    
    if not DATASET_PATH.exists():
        print(f"Error: {DATASET_PATH} tidak ditemukan.")
        return

    # Load dataset asli
    df = pd.read_csv(DATASET_PATH)
    print(f"Memuat {len(df)} baris dari ground_truth.csv")

    # Injeksi Full Corpus
    print("Membaca seluruh corpus menjadi satu teks raksasa...")
    full_corpus_text = load_entire_corpus(CORPUS_DIR)
    print(f"Ukuran total corpus: {len(full_corpus_text)} karakter.")

    import sys
    sys.path.append(str(ROOT_DIR))
    from src.config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GOOGLE_API_KEY

    # Inisialisasi LLM Gemini Pro dengan Timeout Super Longgar
    print("Inisialisasi LLM gemini-3.1-pro-preview...")
    kwargs_llm = {
        "model": "gemini-3.1-pro-preview",
        "temperature": 0.0,
        "max_retries": 5,
        "timeout": 300  
    }

    if GOOGLE_APPLICATION_CREDENTIALS:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        kwargs_llm["credentials"] = creds
        kwargs_llm["project"] = GCP_PROJECT_ID
        kwargs_llm["vertexai"] = True  
    elif GOOGLE_API_KEY:
        kwargs_llm["api_key"] = GOOGLE_API_KEY

    llm = ChatGoogleGenerativeAI(**kwargs_llm)
    
    # Menggunakan with_structured_output ke Skema Tunggal
    structured_llm = llm.with_structured_output(GroundTruthOutput)

    # Prompt Engineering Single Question (Fokus 100%)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Anda adalah Evaluator Ahli Kualitas Data untuk sistem RAG. Anda diberikan SELURUH dokumen korpus akademik universitas sekaligus.
Tugas Anda:
1. Baca pertanyaan pengguna.
2. Cari dan temukan jawabannya di dalam korpus. Jika pertanyaannya kompleks (multihop), gabungkan informasi dari berbagai bagian dokumen dengan teliti.
3. Berikan jawaban yang SANGAT DETAIL, KOMPREHENSIF, dan PANJANG. Jangan menyingkat informasi penting. Gunakan gaya bahasa formal.
4. Identifikasi NAMA FILE (contoh: 01_sejarah.md) dan BAGIAN/PASAL untuk jawaban tersebut.

PENTING:
- Kerahkan 100% kemampuan penalaran Anda hanya untuk satu pertanyaan ini.
- Jika jawaban BENAR-BENAR TIDAK ADA di korpus, isi reference dengan "TIDAK DITEMUKAN". Jangan berhalusinasi.
"""),
        ("human", "KORPUS UNIVERSITAS:\n{full_corpus_text}\n\nPertanyaan Pengguna: {user_input}\n\nBerikan output JSON Anda:")
    ])
    
    chain = prompt | structured_llm

    print(f"\nMemulai generasi jawaban (MODE 1-by-1 FOKUS TINGGI). Ini memakan waktu lebih lama demi kualitas maksimal...")
    
    for index, row in tqdm(df.iterrows(), total=len(df)):
        user_input = row['user_input']
            
        # Hard Retry Loop (Ketahanan Jaringan Ekstra)
        MAX_RETRIES = 10
        for attempt in range(MAX_RETRIES):
            try:
                # Panggil API 1-by-1
                response = chain.invoke({
                    "full_corpus_text": full_corpus_text,
                    "user_input": user_input
                })
                
                # Update DataFrame
                df.at[index, 'reference'] = response.reference
                df.at[index, 'source_doc'] = response.source_doc
                df.at[index, 'notes'] = response.notes
                        
                break # Sukses! Keluar dari loop retry
                
            except Exception as e:
                print(f"\n[Error] Attempt {attempt+1}/{MAX_RETRIES} Gagal memproses Baris {index}: '{user_input[:30]}...' -> Error: {e}")
                
                if attempt == MAX_RETRIES - 1:
                    print(f"[Fatal] Menyerah pada Baris {index}. Melewati pertanyaan ini.")
                    break 
                
                print("[Warning] Jaringan bermasalah atau Limit Vertex. Menunggu 15 detik sebelum re-upload...")
                time.sleep(15)
            
        # Incremental Backup per Pertanyaan
        df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
            
        # Jeda antar pertanyaan untuk mendinginkan kuota Vertex
        time.sleep(5)

    print(f"\nLuar biasa! File ground truth baru berhasil diselesaikan (Kualitas Fokus Tinggi) dan disimpan ke:\n{OUTPUT_PATH}")

if __name__ == "__main__":
    main()
