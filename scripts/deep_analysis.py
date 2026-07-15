import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def analyze():
    print("="*60)
    print("DEEP ANALYSIS: RAGAS EVALUATION (n=80)")
    print("="*60)
    
    # Load data
    df_b = pd.read_csv("eval/results/hasil_config_b.csv")
    df_c = pd.read_csv("eval/results/hasil_config_c.csv")
    
    print(f"\n1. JUMLAH DATA: Config B ({len(df_b)}), Config C ({len(df_c)})")
    
    # Metrics
    metrics = ['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']
    print("\n2. PERBANDINGAN RATA-RATA METRIK:")
    print(f"{'Metrik':<20} | {'Config B (Dense)':<18} | {'Config C (Sparse)':<18}")
    print("-" * 60)
    
    for m in metrics:
        if m in df_b.columns and m in df_c.columns:
            mean_b = df_b[m].mean()
            mean_c = df_c[m].mean()
            diff = mean_b - mean_c
            diff_str = f"(+{diff:.4f})" if diff > 0 else f"({diff:.4f})"
            print(f"{m:<20} | {mean_b:.4f} {diff_str:>9} | {mean_c:.4f}")
            
    # Retrieval Fails
    print("\n3. ANALISIS RETRIEVAL:")
    def count_empty_retrieval(df):
        if 'retrieved_contexts' not in df.columns: return 0
        return (df['retrieved_contexts'].astype(str) == '[]').sum() + df['retrieved_contexts'].isna().sum()
        
    empty_b = count_empty_retrieval(df_b)
    empty_c = count_empty_retrieval(df_c)
    
    print(f"Config B: {empty_b} pertanyaan gagal melakukan retrieval (Threshold 0.3 terlalu ketat?)")
    print(f"Config C: {empty_c} pertanyaan gagal melakukan retrieval (Threshold len token?)")

    # Error Analysis
    print("\n4. WORST QUERIES (DARI ERROR ANALYSIS):")
    try:
        err_b = pd.read_csv("eval/results/error_analysis_config_b.csv")
        err_c = pd.read_csv("eval/results/error_analysis_config_c.csv")
        
        print("\n[CONFIG B - Top 3 Kegagalan Utama]")
        for i, r in err_b.head(3).iterrows():
            print(f"- Q: {r['user_input']}")
            print(f"  Score: {r['avg_metric_score']:.3f} | Note: {str(r.get('failure_notes', ''))[:100]}...")
            
        print("\n[CONFIG C - Top 3 Kegagalan Utama]")
        for i, r in err_c.head(3).iterrows():
            print(f"- Q: {r['user_input']}")
            print(f"  Score: {r['avg_metric_score']:.3f} | Note: {str(r.get('failure_notes', ''))[:100]}...")
    except Exception as e:
        print(f"Error loading error analysis: {e}")

if __name__ == "__main__":
    analyze()
