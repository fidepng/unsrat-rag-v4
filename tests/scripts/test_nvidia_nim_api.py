# tests/test_nvidia_nim_api.py
import os
import time
import sys
# Inject parent directory to sys.path to allow running as standalone script (best practice)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Import centralized logging manager (FR-28, NFR-08)
from src.logger_manager import get_logger

# Initialize centralized logger for the NIM test runner
logger = get_logger("test_nvidia_nim")

def verify_model(model_id, api_name):
    logger.info(f"Memulai testing NVIDIA NIM model: {model_id} (Endpoint: {api_name})")
    print(f"\n--- Testing Model: {model_id} (API Name: {api_name}) ---")
    
    api_key = os.getenv("NVIDIA_NIM_API_KEY")
    if not api_key:
        logger.error("NVIDIA_NIM_API_KEY tidak ditemukan di environment (.env)!")
        print("[ERROR] Error: NVIDIA_NIM_API_KEY not found in environment!")
        return False
    
    try:
        logger.debug(f"Menginisialisasi ChatOpenAI untuk model NIM: {api_name}")
        llm = ChatOpenAI(
            model=api_name,
            api_key=api_key,
            openai_api_base="https://integrate.api.nvidia.com/v1",
            temperature=0.1,
            max_tokens=64,
            timeout=15, # 15s timeout
        )
        
        start_time = time.time()
        messages = [HumanMessage(content="Say the word 'UNSRAT' and nothing else.")]
        
        logger.debug(f"Mengirim request ke NVIDIA NIM untuk model: {model_id}...")
        response = llm.invoke(messages)
        latency = time.time() - start_time
        
        logger.info(f"Sukses memanggil model {model_id} | Latensi: {latency:.4f}s | Response: {repr(response.content.strip())}")
        print(f"[SUCCESS] Success!")
        print(f"   Response: {repr(response.content.strip())}")
        print(f"   Latency:  {latency:.2f}s")
        return True
    except Exception as e:
        logger.error(f"Gagal memanggil model {model_id} via NIM | Error: {e}")
        print(f"[FAIL] Failed to invoke {model_id} via NIM!")
        print(f"   Error detail: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    
    # ⚠️ KEPATUHAN RATE LIMIT NVIDIA NIM (40 RPM):
    # Kami mendokumentasikan batas 40 Requests Per Minute (RPM) dari NVIDIA NIM.
    # Setiap request dijeda untuk menghindari burst limit error.
    logger.warning("NVIDIA NIM API limit dideteksi: Up to 40 RPM. Menjalankan pengujian dengan jeda aman.")
    
    models_to_test = [
        ("llama-3.1-nemotron-nano-8b-v1", "nvidia/llama-3.1-nemotron-nano-8b-v1"),
        ("llama-3.3-nemotron-super-49b-v1.5", "nvidia/llama-3.3-nemotron-super-49b-v1.5"),
        ("gemma-4-31b-it", "google/gemma-4-31b-it"),
        ("llama-3.1-8b-instruct", "meta/llama-3.1-8b-instruct")
    ]
    
    print("==================================================")
    print("       NVIDIA NIM API CONNECTIVITY TEST           ")
    print("==================================================")
    print(" [WARNING] NIM Rate Limit: Up to 40 RPM (Jeda 1.5s)")
    print("==================================================")
    
    results = {}
    for m_id, api_name in models_to_test:
        results[m_id] = verify_model(m_id, api_name)
        # Jeda 1.5 detik untuk mematuhi rate limit 40 RPM (60s / 40 = 1.5s per request)
        time.sleep(1.5)
        
    print("\n==================================================")
    print("                 TEST RESULTS                     ")
    print("==================================================")
    logger.info("--- RINGKASAN HASIL PENGUJIAN KONEKTIVITAS NIM ---")
    for m_id, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f" {m_id:<36} : {status}")
        logger.info(f"Model {m_id:<36} : {status}")
    print("==================================================")
