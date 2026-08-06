import pandas as pd
import numpy as np
import warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).parent.parent
REPORT_MD_PATH = ROOT_DIR / "docs" / "reports" / "laporan_analisis_evaluasi.md"

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
        print(f"\n[+] Laporan Analisis Evaluasi berhasil diekspor ke: {filepath}")

def analyze():
    # Load data
    try:
        df_b = pd.read_csv("eval/results/hasil_config_b.csv")
        df_c = pd.read_csv("eval/results/hasil_config_c.csv")
    except Exception as e:
        print(f"[!] Gagal memuat CSV hasil evaluasi: {e}")
        return

    report = MarkdownReport()
    report.add_title("Laporan Analisis Mendalam Evaluasi RAGAS (n=80)")
    
    # 1. Jumlah Data
    report.add_section("1. Statistik Volume Dataset")
    summary_text = (
        f"Analisis dilakukan secara komparatif antara dua konfigurasi RAG:\n"
        f"- **Config B (Dense Retrieval - Vector Search)**: {len(df_b)} kueri teruji.\n"
        f"- **Config C (Sparse Retrieval - BM25)**: {len(df_c)} kueri teruji."
    )
    report.add_paragraph(summary_text)
    print("="*60)
    print("ANALISIS EVALUASI RAGAS")
    print("="*60)
    print(summary_text)

    # 2. Perbandingan Rata-rata Global
    report.add_section("2. Perbandingan Rata-Rata Metrik (Global Mean)")
    metrics = ['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']
    
    global_compare = []
    for m in metrics:
        if m in df_b.columns and m in df_c.columns:
            mean_b = df_b[m].mean()
            mean_c = df_c[m].mean()
            diff = mean_b - mean_c
            diff_str = f"+{diff:.4f}" if diff > 0 else f"{diff:.4f}"
            global_compare.append({
                "Metrik": m.replace("_", " ").title(),
                "Config B (Dense)": round(mean_b, 4),
                "Config C (Sparse)": round(mean_c, 4),
                "Selisih (B - C)": diff_str
            })
            
    df_global = pd.DataFrame(global_compare)
    report.add_table(df_global)
    
    print("\n--- Perbandingan Rata-rata Global ---")
    print(df_global.to_string(index=False))

    # 3. Distribusi Sebaran Statistik Skor
    report.add_section("3. Distribusi Sebaran Statistik Skor Individual")
    
    dist_rows = []
    for cfg_code, cfg_label, df in [("B", "Config B (Dense)", df_b), ("C", "Config C (Sparse)", df_c)]:
        for m in metrics:
            if m in df.columns:
                data = df[m].dropna()
                dist_rows.append({
                    "Config": cfg_label,
                    "Metrik": m.replace("_", " ").title(),
                    "Mean": round(data.mean(), 3),
                    "Median": round(data.median(), 3),
                    "Min": round(data.min(), 3),
                    "Max": round(data.max(), 3),
                    "% Sempurna (1.0)": f"{(data == 1.0).mean() * 100:.1f}%",
                    "% Gagal (0.0)": f"{(data == 0.0).mean() * 100:.1f}%"
                })
                
    df_dist = pd.DataFrame(dist_rows)
    report.add_table(df_dist)
    
    print("\n--- Sebaran Statistik Skor ---")
    print(df_dist.to_string(index=False))

    # 4. Analisis Kegagalan Retrieval (Empty Retrieval)
    report.add_section("4. Audit Kegagalan Retrieval (Konteks Kosong)")
    def count_empty_retrieval(df):
        if 'retrieved_contexts' not in df.columns: return 0
        return (df['retrieved_contexts'].astype(str) == '[]').sum() + df['retrieved_contexts'].isna().sum()
    empty_b = count_empty_retrieval(df_b)
    empty_c = count_empty_retrieval(df_c)
    
    retrieval_text = (
        f"- **Config B (Dense)**: {empty_b} kueri gagal melakukan retrieval (Konteks Kosong / Terfilter Threshold).\n"
        f"- **Config C (Sparse)**: {empty_c} kueri gagal melakukan retrieval (Konteks Kosong)."
    )
    report.add_paragraph(retrieval_text)
    print("\n--- Audit Kegagalan Retrieval ---")
    print(retrieval_text)

    # 5. Top 5 Worst Performers in Context Precision & Recall (Config B - Dari Hasil Mentah)
    report.add_section("5. Analisis Kasus Kegagalan Spesifik (Config B)")
    
    report.add_paragraph("#### Top 5 Kelemahan Context Precision (Mengambil Informasi Tidak Relevan):")
    # Urutkan data mentah hasil_config_b untuk mendapat kueri bermasalah
    bad_prec = df_b.sort_values('context_precision').head(5)[['user_input', 'context_precision', 'context_recall', 'answer_relevancy']]
    bad_prec.columns = ['Kueri / Pertanyaan', 'Context Precision', 'Context Recall', 'Answer Relevancy']
    report.add_table(bad_prec)

    report.add_paragraph("\n#### Top 5 Kelemahan Context Recall (Informasi Relevan Terlewat / Tidak Terambil):")
    bad_rec = df_b.sort_values('context_recall').head(5)[['user_input', 'context_precision', 'context_recall', 'answer_relevancy']]
    bad_rec.columns = ['Kueri / Pertanyaan', 'Context Precision', 'Context Recall', 'Answer Relevancy']
    report.add_table(bad_rec)

    # 6. Top 3 worst queries per config
    report.add_section("6. Sampel Kasus Kegagalan Terburuk (Audit Manual)")
    for label, err_path in [("Config B (Dense)", "eval/results/error_analysis_config_b.csv"), 
                            ("Config C (Sparse)", "eval/results/error_analysis_config_c.csv")]:
        try:
            err_df = pd.read_csv(err_path)
            report.add_paragraph(f"#### Worst Queries - {label}")
            for i, r in err_df.head(3).iterrows():
                report.add_paragraph(
                    f"1. **Q**: {r['user_input']}\n"
                    f"   - *Rata-rata Skor*: {r['avg_metric_score']:.3f}\n"
                    f"   - *Catatan Analisis*: {str(r.get('failure_notes', 'N/A'))}\n"
                )
        except Exception as e:
            report.add_paragraph(f"*Gagal memuat kueri terburuk {label}: {e}*")

    # 7. Metodologi RAGAS & Referensi Akademis
    report.add_section("7. Metodologi Evaluasi & Referensi Ilmiah")
    methodology_text = (
        "Evaluasi dilakukan menggunakan metrik dari framework **RAGAS (Retrieval Augmented Generation Assessment)** "
        "yang berbasis *LLM-as-a-Judge* (dalam hal ini menggunakan model evaluator `gemini-3.1-pro-preview`). "
        "Berikut adalah definisi matematis dan konseptual dari metrik yang diukur:\n\n"
        "1. **Faithfulness (Keshahihan)**: Mengukur kebenaran faktual jawaban terhadap konteks yang diambil.\n"
        "   $$\\text{Faithfulness} = \\frac{\\text{Jumlah statement yang didukung konteks}}{\\text{Total statement dalam jawaban}}$$\n"
        "2. **Answer Relevancy (Kerelevanan Jawaban)**: Mengukur seberapa tepat jawaban menjawab inti pertanyaan.\n"
        "3. **Context Precision (Ketepatan Konteks)**: Mengukur apakah potongan teks (chunk) yang relevan ditempatkan "
        "pada peringkat atas hasil pencarian.\n"
        "4. **Context Recall (Kecakupan Konteks)**: Mengukur sejauh mana semua informasi yang dibutuhkan untuk "
        "menjawab pertanyaan (berdasarkan referensi ground truth) berhasil diambil oleh retriever.\n\n"
        "**Referensi Ilmiah Utama:**\n"
        "- Es, S., Jha, A., Espinosa, A. P., Anshu, A., & & others. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation*. arXiv preprint arXiv:2309.15217."
    )
    report.add_paragraph(methodology_text)

    # Save to Markdown file
    report.save(REPORT_MD_PATH)

if __name__ == "__main__":
    analyze()
