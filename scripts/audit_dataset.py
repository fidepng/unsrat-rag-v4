import pandas as pd
import numpy as np
import string

def compute_lexical_overlap(row):
    q_words = set(str(row['user_input']).lower().translate(str.maketrans('', '', string.punctuation)).split())
    r_words = set(str(row['reference']).lower().translate(str.maketrans('', '', string.punctuation)).split())
    if not q_words:
        return 0.0
    overlap = len(q_words.intersection(r_words)) / len(q_words)
    return overlap

def audit_dataset(filepath):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return

    print("="*50)
    print("DATASET AUDIT REPORT")
    print("="*50)
    
    # 1. Volume & Coverage
    print("\n1. Volume & Coverage:")
    total_rows = len(df)
    print(f"Total Baris: {total_rows}")
    
    if 'source_doc' in df.columns:
        print("\nDistribusi Source Doc:")
        print(df['source_doc'].value_counts(dropna=False))
    
    if 'category' in df.columns:
        print("\nDistribusi Category (Tipologi Query):")
        print(df['category'].value_counts(dropna=False))
        
    # 2. Distribution & Bias
    print("\n2. Lexical vs Semantic Bias:")
    df['lexical_overlap'] = df.apply(compute_lexical_overlap, axis=1)
    avg_overlap = df['lexical_overlap'].mean()
    print(f"Rata-rata Lexical Overlap (Kata kunci sama antara Q dan A): {avg_overlap:.2%}")
    
    high_overlap = len(df[df['lexical_overlap'] > 0.5])
    low_overlap = len(df[df['lexical_overlap'] <= 0.2])
    print(f"Pertanyaan Exact Match / Lexical Bias (>50% overlap): {high_overlap} ({high_overlap/total_rows:.2%})")
    print(f"Pertanyaan Paraphrased / Semantic Bias (<=20% overlap): {low_overlap} ({low_overlap/total_rows:.2%})")
    
    # 3. Quality & Validity
    print("\n3. Quality & Validity:")
    empty_q = df['user_input'].isna().sum()
    empty_r = df['reference'].isna().sum()
    print(f"Empty user_input: {empty_q}")
    print(f"Empty reference: {empty_r}")
    
    # Average lengths
    q_len = df['user_input'].apply(lambda x: len(str(x).split())).mean()
    r_len = df['reference'].apply(lambda x: len(str(x).split())).mean()
    print(f"Rata-rata panjang user_input: {q_len:.1f} kata")
    print(f"Rata-rata panjang reference: {r_len:.1f} kata")
    
    print("\n--- SAMPLE HIGH OVERLAP (Potensi Lexical Bias) ---")
    if high_overlap > 0:
        sample_high = df[df['lexical_overlap'] > 0.5].sample(min(2, high_overlap))
        for _, r in sample_high.iterrows():
            print(f"Q: {r['user_input']}\nA: {r['reference']}\n")
            
    print("--- SAMPLE LOW OVERLAP (Potensi Semantic Bias) ---")
    if low_overlap > 0:
        sample_low = df[df['lexical_overlap'] <= 0.2].sample(min(2, low_overlap))
        for _, r in sample_low.iterrows():
            print(f"Q: {r['user_input']}\nA: {r['reference']}\n")

if __name__ == "__main__":
    audit_dataset("eval/dataset/ground_truth.csv")
