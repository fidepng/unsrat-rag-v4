import os
import time
from pathlib import Path
from dotenv import load_dotenv
import frontmatter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- BEGIN RAGAS COMPATIBILITY HACK ---
# Ragas (even in 0.4.3) mistakenly tries to import ChatVertexAI and VertexAI from langchain_community
# which were removed in LangChain 1.x. We mock them here to prevent ModuleNotFoundError.
import sys, types
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

# Ensure API key is loaded explicitly
env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def generate_synthetic_data():
    print("Initializing LLMs...")
    # Best practice: max_retries=10 untuk meredam 429 API Limit
    kwargs_llm = {"model": "gemini-3.1-pro-preview", "max_retries": 10}
    kwargs_emb = {"model": "models/gemini-embedding-001"}
    
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from src.config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GOOGLE_API_KEY
    
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
    
    # Read corpus
    corpus_dir = Path("data/corpus")
    raw_docs = []
    
    if not corpus_dir.exists():
        print(f"Error: {corpus_dir} does not exist. Please run from project root.")
        return

    for md_file in corpus_dir.glob("*.md"):
        post = frontmatter.load(md_file)
        raw_docs.append(Document(page_content=post.content, metadata=post.metadata))
        
    print(f"Loaded {len(raw_docs)} documents from corpus.")
    
    # --- BEST PRACTICE: Pre-splitting ---
    # Memotong dokumen agar berukuran kecil (kurang dari 500 token).
    # Ini membuat Ragas v0.4 secara otomatis melewati fitur HeadlineSplitter (yang sering error)
    # dan menggunakan rute transformasi ringkasan (SummaryExtractor) yang jauh lebih stabil.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, # Sekitar 300-400 token
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(raw_docs)
    print(f"Split into {len(docs)} chunks for stable Ragas processing.")
    
    # Konfigurasi Anti-Limit (Sudah Dioptimalkan untuk Paid Tier):
    # Menggunakan 16 workers paralel untuk mempercepat proses generasi hingga 10x-16x lipat.
    run_config = RunConfig(max_workers=16, timeout=300, max_retries=10)
    
    # Generate testset
    print("Generating synthetic testset. This may take a while...")
    testset = generator.generate_with_langchain_docs(
        docs, 
        testset_size=20,
        run_config=run_config
    )
    
    # Save output
    output_path = Path("eval/dataset/synthetic_testset.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = testset.to_pandas()
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic testset saved to {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()

