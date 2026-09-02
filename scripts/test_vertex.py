import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Paksa load .env dari root folder proyek
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

print("=== 1. CHECK ENVIRONMENT VARIABLES ===")
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0535443522")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
api_key = os.getenv("GOOGLE_API_KEY")

print(f"GOOGLE_APPLICATION_CREDENTIALS : {cred_path}")
print(f"File Exists                    : {os.path.exists(cred_path) if cred_path else False}")
print(f"Project ID                     : {project_id}")
print(f"Location                       : {location}")
print(f"GOOGLE_API_KEY Set             : {bool(api_key)}\n")

success_count = 0

# ── TEST 1: GOOGLE AI STUDIO (GEMINI DEVELOPER API) ─────────
if api_key:
    print("=== 2. TESTING GOOGLE AI STUDIO (GEMINI DEVELOPER API) ===")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Balas kata: 'KONEKSI_AI_STUDIO_BERHASIL'"
        )
        print("[SUCCESS] Response dari Gemini AI Studio:")
        print(response.text.strip())
        success_count += 1
    except Exception as e:
        print(f"[FAILED] Error calling Gemini AI Studio API:\n{e}\n")
else:
    print("=== 2. SKIPPING GOOGLE AI STUDIO TEST (GOOGLE_API_KEY belum di-set di .env) ===\n")

# ── TEST 2: GOOGLE CLOUD VERTEX AI ───────────────────────────
print("=== 3. TESTING VERTEX AI (GOOGLE-GENAI UNIFIED SDK) ===")
try:
    from google import genai
    vertex_loc = "us-central1" if location == "asia-southeast1" else location

    if cred_path and os.path.exists(cred_path):
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=vertex_loc,
        )
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Balas kata: 'KONEKSI_VERTEX_BERHASIL'"
        )
        print("[SUCCESS] Response dari Vertex AI:")
        print(res.text.strip())
        success_count += 1
    else:
        print("[WARN] GOOGLE_APPLICATION_CREDENTIALS file tidak ditemukan.")
except Exception as e:
    print(f"[FAILED] Error calling Vertex AI API:\n{e}\n")

if success_count > 0:
    print("\n==========================================")
    print(" [SUMMARY] DI SINI: TEST BERHASIL!")
    print("==========================================")
else:
    print("\n==========================================")
    print(" [SUMMARY] SEMUA METODE PENGETESAN GAGAL.")
    print(" Silakan tinjau petunjuk perbaikan di bawah.")
    print("==========================================")