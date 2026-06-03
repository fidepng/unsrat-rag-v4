# tests/verify_retriever.py
# Verification script for src/retriever.py (Task 6)

import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.retriever import retrieve_chunks

def clean_preview(text: str) -> str:
    return text[:100].replace('\n', ' ')

def main():
    print("==================================================")
    print("VERIFIKASI RETRIEVER - CONFIG B (VECTOR SEARCH)")
    print("==================================================")
    
    query_b = "syarat yudisium sarjana"
    print(f"Query: '{query_b}'")
    chunks_b = retrieve_chunks(query_b, "b")
    print(f"[+] Retrieved {len(chunks_b)} chunks (Threshold <= 0.65)")
    for idx, c in enumerate(chunks_b):
        preview = clean_preview(c['content'])
        print(f"  #{idx+1} [dist={c['distance']:.4f}] | {c['doc_id']} | {preview}...")
        
    print("\n==================================================")
    print("VERIFIKASI RETRIEVER - CONFIG C (BM25 KEYWORD SEARCH)")
    print("==================================================")
    
    query_c = "SKS maksimal per semester"
    print(f"Query: '{query_c}'")
    chunks_c = retrieve_chunks(query_c, "c")
    print(f"[+] Retrieved {len(chunks_c)} chunks")
    for idx, c in enumerate(chunks_c):
        preview = clean_preview(c['content'])
        print(f"  #{idx+1} [score={c['score']:.4f}] | {c['doc_id']} | {preview}...")

    # Let's perform a basic check that we got results
    if len(chunks_b) > 0 and len(chunks_c) > 0:
        print("\n[+] SUCCESS: Unified Retriever works beautifully!")
        sys.exit(0)
    else:
        print("\n[-] FAILURE: One of the retrievers returned 0 results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
