import pandas as pd
import ast

def merge_synthetic_to_ground_truth(synthetic_path, ground_truth_path):
    print("Membaca datasets...")
    df_synthetic = pd.read_csv(synthetic_path)
    df_gt = pd.read_csv(ground_truth_path)

    # Siapkan list untuk menyimpan row baru
    new_rows = []
    
    for _, row in df_synthetic.iterrows():
        # Kolom wajib
        user_input = row['user_input']
        reference = row['reference']
        
        # Kolom opsional, kita petakan dari metadata synthetic
        category = "synthetic_" + str(row.get('synthesizer_name', 'unknown')).replace('_synthesizer', '')
        source_doc = "synthetic_generation"
        notes = f"Persona: {row.get('persona_name')}, Style: {row.get('query_style')}, Length: {row.get('query_length')}"
        
        new_rows.append({
            'user_input': user_input,
            'reference': reference,
            'category': category,
            'source_doc': source_doc,
            'notes': notes
        })
        
    df_new = pd.DataFrame(new_rows)
    
    # Menggabungkan data
    df_merged = pd.concat([df_gt, df_new], ignore_index=True)
    
    # Menghapus duplikat berdasarkan user_input jika ada
    df_merged.drop_duplicates(subset=['user_input'], keep='last', inplace=True)
    
    print(f"Total data ground truth sebelumnya: {len(df_gt)}")
    print(f"Total data sintetis yang ditambahkan: {len(df_new)}")
    print(f"Total data setelah merge (tanpa duplikat): {len(df_merged)}")
    
    # Menyimpan kembali ke ground truth
    df_merged.to_csv(ground_truth_path, index=False, encoding='utf-8-sig')
    print(f"Berhasil menyimpan {len(df_merged)} baris ke {ground_truth_path}")

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    base_dir = Path("eval/dataset")
    synthetic = base_dir / "synthetic_testset.csv"
    gt = base_dir / "ground_truth.csv"
    
    if synthetic.exists() and gt.exists():
        merge_synthetic_to_ground_truth(synthetic, gt)
    else:
        print("File synthetic_testset.csv atau ground_truth.csv tidak ditemukan di eval/dataset/")
