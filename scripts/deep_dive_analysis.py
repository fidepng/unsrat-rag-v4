import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def deep_dive():
    print("="*80)
    print("DEEP DIVE ANALYSIS: RAG PIPELINE (n=80)")
    print("="*80)
    
    df_b = pd.read_csv("eval/results/hasil_config_b.csv")
    df_c = pd.read_csv("eval/results/hasil_config_c.csv")
    
    metrics = ['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']
    
    print("\n[DISTRIBUSI SKOR METRIK - CONFIG B (ChromaDB)]")
    for m in metrics:
        if m in df_b.columns:
            data = df_b[m].dropna()
            print(f"{m:<18}: Mean={data.mean():.3f}, Median={data.median():.3f}, Min={data.min():.3f}, Max={data.max():.3f}, % Sempurna(1.0)={(data==1.0).mean():.1%}, % Gagal(0.0)={(data==0.0).mean():.1%}")

    print("\n[DISTRIBUSI SKOR METRIK - CONFIG C (BM25)]")
    for m in metrics:
        if m in df_c.columns:
            data = df_c[m].dropna()
            print(f"{m:<18}: Mean={data.mean():.3f}, Median={data.median():.3f}, Min={data.min():.3f}, Max={data.max():.3f}, % Sempurna(1.0)={(data==1.0).mean():.1%}, % Gagal(0.0)={(data==0.0).mean():.1%}")

    print("\n[ANALISA ERROR & KEGAGALAN SPESIFIK]")
    err_b = pd.read_csv("eval/results/error_analysis_config_b.csv")
    
    # Analyze by failure type (context_precision vs context_recall vs faithfulness)
    # Ragas low precision means retrieved contexts had irrelevant info.
    # Ragas low recall means retrieved contexts missed the ground truth answer.
    
    print("\nTop 5 Kelemahan Context Precision (Irrelevant Chunks Retrieved) - Config B:")
    bad_prec = err_b.sort_values('context_precision').head(5)
    for _, r in bad_prec.iterrows():
        print(f"Q: {r['user_input']}")
        print(f"  Precision: {r['context_precision']:.2f} | Recall: {r['context_recall']:.2f} | Relevancy: {r['answer_relevancy']:.2f}")

    print("\nTop 5 Kelemahan Context Recall (Missing Info) - Config B:")
    bad_rec = err_b.sort_values('context_recall').head(5)
    for _, r in bad_rec.iterrows():
        print(f"Q: {r['user_input']}")
        print(f"  Recall: {r['context_recall']:.2f} | Precision: {r['context_precision']:.2f} | Relevancy: {r['answer_relevancy']:.2f}")

if __name__ == "__main__":
    deep_dive()
