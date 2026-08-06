import sys
import argparse
import string
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
REPORT_MD_PATH = ROOT_DIR / "docs" / "reports" / "laporan_audit_dataset.md"

class MarkdownReport:
    def __init__(self):
        self.content = []
        
    def add_title(self, title):
        self.content.append(f"# {title}\n")
        self.content.append(f"*Dihasilkan secara otomatis pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WITA*\n")
        
    def add_section(self, section):
        self.content.append(f"\n## {section}\n")
        
    def add_paragraph(self, text):
        self.content.append(f"{text}\n")
        
    def add_code_block(self, text):
        self.content.append(f"```text\n{text}\n```\n")
        
    def add_table(self, df):
        headers = list(df.columns)
        table_lines = []
        table_lines.append("| " + " | ".join(headers) + " |")
        table_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for _, row in df.iterrows():
            row_str = "| " + " | ".join(str(val).replace("\n", " ") for val in row) + " |"
            table_lines.append(row_str)
        self.content.append("\n".join(table_lines) + "\n")
        
    def save(self, filepath):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(self.content))
        print(f"\n[+] Laporan Audit Dataset berhasil diekspor ke: {filepath}")

def compute_lexical_overlap(row):
    q_words = set(str(row['user_input']).lower().translate(str.maketrans('', '', string.punctuation)).split())
    r_words = set(str(row['reference']).lower().translate(str.maketrans('', '', string.punctuation)).split())
    if not q_words:
        return 0.0
    overlap = len(q_words.intersection(r_words)) / len(q_words)
    return overlap

def audit_dataset(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"[!] Error: File dataset {filepath} tidak ditemukan.")
        return

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"[!] Gagal membaca file dataset: {e}")
        return

    report = MarkdownReport()
    report.add_title(f"Laporan Audit Kualitas Dataset RAG - {path.name}")
    
    total_rows = len(df)
    
    print("="*60)
    print(f"DATASET AUDIT: {path.name} (n={total_rows})")
    print("="*60)

    # 1. Volume & Coverage
    report.add_section("1. Statistik Volume & Cakupan Dokumen")
    volume_summary = f"Total Baris Kueri Terdaftar: **{total_rows}**"
    report.add_paragraph(volume_summary)
    print(volume_summary)
    
    if 'source_doc' in df.columns:
        report.add_paragraph("\n#### Distribusi Berkas Regulasi Sumber (Source Doc):")
        dist_src = df['source_doc'].value_counts(dropna=False).reset_index()
        dist_src.columns = ['Dokumen Regulasi', 'Jumlah Kueri']
        report.add_table(dist_src)
        print("\nDistribusi Source Doc:")
        print(dist_src.to_string(index=False))
    
    if 'category' in df.columns:
        report.add_paragraph("\n#### Distribusi Tipologi Kueri (Category):")
        dist_cat = df['category'].value_counts(dropna=False).reset_index()
        dist_cat.columns = ['Kategori / Tipe Kueri', 'Jumlah Kueri']
        report.add_table(dist_cat)
        print("\nDistribusi Kategori:")
        print(dist_cat.to_string(index=False))
        
    # 2. Distribution & Bias (Lexical Overlap)
    report.add_section("2. Distribusi Bias Leksikal vs Semantik")
    df['lexical_overlap'] = df.apply(compute_lexical_overlap, axis=1)
    avg_overlap = df['lexical_overlap'].mean()
    
    high_overlap = len(df[df['lexical_overlap'] > 0.5])
    low_overlap = len(df[df['lexical_overlap'] <= 0.2])
    
    bias_text = (
        f"- **Rata-rata Tumpang Tindih Kata (Lexical Overlap)**: {avg_overlap:.2%}\n"
        f"- **Kueri Tipe Pencocokan Kata Kunci (Lexical Bias >50% overlap)**: {high_overlap} ({high_overlap/total_rows:.2%})\n"
        f"- **Kueri Tipe Makna/Parafrase (Semantic Bias <=20% overlap)**: {low_overlap} ({low_overlap/total_rows:.2%})"
    )
    report.add_paragraph(bias_text)
    print("\nBias Analysis:")
    print(bias_text)
    
    # 3. Quality & Validity
    report.add_section("3. Validitas & Kualitas Data")
    empty_q = int(df['user_input'].isna().sum())
    empty_r = int(df['reference'].isna().sum())
    q_len = df['user_input'].apply(lambda x: len(str(x).split())).mean()
    r_len = df['reference'].apply(lambda x: len(str(x).split())).mean()
    
    quality_text = (
        f"- **Kueri Kosong (Empty User Input)**: {empty_q}\n"
        f"- **Jawaban Referensi Kosong (Empty Reference)**: {empty_r}\n"
        f"- **Rata-rata Panjang Kueri**: {q_len:.1f} kata\n"
        f"- **Rata-rata Panjang Jawaban Referensi**: {r_len:.1f} kata"
    )
    report.add_paragraph(quality_text)
    print("\nQuality & Length Stats:")
    print(quality_text)
    
    # 4. Samples of High and Low overlap
    report.add_section("4. Sampel Kasus Klasifikasi Kueri")
    
    if high_overlap > 0:
        report.add_paragraph("#### Sampel Kueri Potensi Lexical Bias (>50% Overlap)")
        sample_high = df[df['lexical_overlap'] > 0.5].sample(min(2, high_overlap), random_state=42)
        for _, r in sample_high.iterrows():
            report.add_paragraph(
                f"- **Q**: {r['user_input']}\n"
                f"- **R**: *{r['reference']}*\n"
                f"- *Overlap Score*: {r['lexical_overlap']:.2%}\n"
            )
            
    if low_overlap > 0:
        report.add_paragraph("#### Sampel Kueri Potensi Semantic Bias (<=20% Overlap - Natural Language)")
        sample_low = df[df['lexical_overlap'] <= 0.2].sample(min(2, low_overlap), random_state=42)
        for _, r in sample_low.iterrows():
            report.add_paragraph(
                f"- **Q**: {r['user_input']}\n"
                f"- **R**: *{r['reference']}*\n"
                f"- *Overlap Score*: {r['lexical_overlap']:.2%}\n"
            )

    # 5. Metodologi Audit Bias Leksikal
    report.add_section("5. Metodologi & Rumus Perhitungan Overlap Leksikal")
    methodology_text = (
        "Untuk memvalidasi bias linguistik pada dataset evaluasi RAG, "
        "skrip ini menghitung persentase tumpang tindih leksikal murni antara kueri pengguna "
        "($Q$) dan teks jawaban referensi ($R$).\n\n"
        "**Formula Perhitungan Overlap:**\n"
        "Teks kueri dan jawaban dibersihkan dari tanda baca, diturunkan case-nya menjadi lowercase, "
        "dan dipecah menjadi kumpulan kata (*set of words*). Overlap dihitung menggunakan rasio kueri terwakili:\n"
        "$$\\text{Lexical Overlap}(Q, R) = \\frac{|Q_{\\text{words}} \\cap R_{\\text{words}}|}{|Q_{\\text{words}}|}$$\n\n"
        "**Interpretasi Bias:**\n"
        "- **Lexical Bias (> 50%)**: Pertanyaan cenderung menggunakan kata kunci yang sama persis "
        "dengan dokumen regulasi (memudahkan pencarian kata kunci/BM25).\n"
        "- **Semantic Bias (<= 20%)**: Pertanyaan berupa parafrase atau kalimat tanya alami "
        "yang maknanya sama tetapi menggunakan kosa kata yang berbeda (menguji kekuatan pencarian vektor semantik)."
    )
    report.add_paragraph(methodology_text)

    # Save to Markdown
    report.save(REPORT_MD_PATH)

def main():
    parser = argparse.ArgumentParser(description="Tool Audit Kualitas Leksikal & Semantik Dataset RAG")
    parser.add_argument("dataset_path", nargs="?", default="eval/dataset/ground_truth.csv", 
                        help="Path ke berkas CSV dataset ground truth (default: eval/dataset/ground_truth.csv)")
    args = parser.parse_args()
    
    audit_dataset(args.dataset_path)

if __name__ == "__main__":
    main()
