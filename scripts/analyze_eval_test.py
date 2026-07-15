import pandas as pd

def analyze_results():
    try:
        df_b = pd.read_csv("eval/results/hasil_config_b.csv")
        df_c = pd.read_csv("eval/results/hasil_config_c.csv")
    except Exception as e:
        print(f"Error loading CSVs: {e}")
        return

    print("="*50)
    print("ANALISA HASIL TESTING (n=5/10)")
    print("="*50)
    
    print(f"\nJumlah Data Dievaluasi - Config B: {len(df_b)}")
    print(f"Jumlah Data Dievaluasi - Config C: {len(df_c)}")

    metrics = ['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']
    
    print("\n--- Rata-Rata Skor Metrik ---")
    print(f"{'Metrik':<20} | {'Config B (Dense)':<18} | {'Config C (Sparse)':<18}")
    print("-" * 60)
    
    for m in metrics:
        if m in df_b.columns and m in df_c.columns:
            mean_b = df_b[m].mean()
            mean_c = df_c[m].mean()
            
            # Check for NaN
            nan_b = df_b[m].isna().sum()
            nan_c = df_c[m].isna().sum()
            
            nan_b_str = f"({nan_b} NaN)" if nan_b > 0 else ""
            nan_c_str = f"({nan_c} NaN)" if nan_c > 0 else ""
            
            print(f"{m:<20} | {mean_b:.4f} {nan_b_str:<8} | {mean_c:.4f} {nan_c_str:<8}")
        else:
            print(f"{m:<20} | Tidak ditemukan     | Tidak ditemukan")

    print("\n--- Validasi Eksekusi ---")
    # Check if retrieved_contexts are not empty
    if 'retrieved_contexts' in df_b.columns:
        empty_retrieval_b = (df_b['retrieved_contexts'] == '[]').sum() + df_b['retrieved_contexts'].isna().sum()
        print(f"Config B: {empty_retrieval_b} pertanyaan gagal melakukan retrieval (list kosong).")
    
    if 'retrieved_contexts' in df_c.columns:
        empty_retrieval_c = (df_c['retrieved_contexts'] == '[]').sum() + df_c['retrieved_contexts'].isna().sum()
        print(f"Config C: {empty_retrieval_c} pertanyaan gagal melakukan retrieval (list kosong).")

if __name__ == "__main__":
    analyze_results()
