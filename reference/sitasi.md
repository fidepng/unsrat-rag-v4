
### Rangkuman & Analisis Dampak 5 Paper Chatbot Akademik (Sub-bab 2.1.1)

#### 1. Ajiz et al. (2023)

* **Sitasi Lengkap:** Ajiz et al. (2023) — *"Pengembangan Aplikasi Chatbot Informasi Akademik Berbasis Web Menggunakan Metode Artificial Intelligence Markup Language (AIML)"* (Media Jurnal Informatika / MJI, Vol. 15 No. 2, Des 2023)
* **Objek:** Chatbot layanan informasi akademik mahasiswa baru dan perkuliahan di Universitas Majalengka.


* **Metode:** *Rule-based / pattern matching* berbasis *Artificial Intelligence Markup Language* (AIML) berbasis web (PHP 8, JavaScript, MySQL, HTML 5). Alur memproses *tokenizing* dan pencocokan aturan *template*. Jika pertanyaan tidak ditemukan pada basis pengetahuan AIML, pertanyaan dialihkan ke antarmuka admin untuk ditinjau dan ditambahkan secara manual.


* **Evaluasi:** Pengujian fungsionalitas via *Black Box Testing* (10 skenario pertanyaan akademik paling sering ditanyakan hasil pendataan 100 responden) dan *White Box Testing*.


* **Hasil Kunci:** Pengujian *black box* mencatatkan hasil 100% valid untuk 10 skenario pertanyaan akademik yang telah terdefinisi di database; sistem mampu mengalirkan kueri *out-of-database* ke dashboard admin.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Menggambarkan baseline historis pendekatan konvensional berbasis aturan kaku (*rule-based AIML*) pada chatbot perguruan tinggi di Indonesia.


* **Kritik/Limitasi:** Sangat kaku bergantung pada pencocokan *pattern* eksplisit. Tidak memiliki kapabilitas *Natural Language Understanding* (NLU) maupun *semantic search*; variasi sintaksis/parafase yang tidak didaftarkan pada aturan AIML akan langsung gagal dijawab.


* **Relevansi di Bab II (2.1.1):** Berguna sebagai penanda paradigma awal chatbot akademik untuk mempertegas pergeseran metodologis menuju arsitektur RAG dan LLM yang mampu memahami kueri *unstructured natural language* tanpa perlunya *hardcoding* aturan satu per satu.





---

#### 2. Guntoro et al. (2020)

* **Sitasi Lengkap:** Guntoro et al. (2020) — *"Aplikasi Chatbot untuk Layanan Informasi dan Akademik Kampus Berbasis Artificial Intelligence Markup Language (AIML)"* (Digital Zone: Jurnal Teknologi Informasi & Komunikasi, Vol. 11 No. 2, Nov 2020)


* **Objek:** Chatbot layanan informasi pendaftaran dan akademik (AILABOT) untuk mahasiswa dan masyarakat umum di Universitas Lancang Kuning (UNILAK).


* **Metode:** *Rule-based* berbasis AIML (Library AIML 0.8.6) dengan backend Python 3.5 dan micro-framework Flask 0.12.3 di lingkungan Linux Ubuntu. Menggunakan *default response* ketika pencocokan *pattern* tidak ditemukan. Admin melakukan pembaruan pengetahuan secara manual langsung pada skrip aturan AIML.


* **Evaluasi:** *White Box* & *Black Box Testing* (8 skenario pertanyaan validasi + pengujian pengetahuan) dan *User Acceptance Testing* (UAT) kepada 10 responden.


* **Hasil Kunci:** Pengujian *Black Box* dan *White Box* mencatatkan tingkat akurasi 100% pada ruang lingkup pertanyaan tertutup, sedangkan UAT menghasilkan tingkat penerimaan pengguna sebesar 95%.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Menyediakan bukti empiris mengenai penerapan AIML berbasis web service Python/Flask di perguruan tinggi Indonesia.


* **Kritik/Limitasi:** Angka akurasi 100% bersifat semu karena hanya diuji pada *query* yang cocok secara eksak dengan *template* yang disiapkan. Pemeliharaan basis pengetahuan sangat tidak efisien karena admin harus menyunting file XML/AIML secara manual setiap ada perubahan regulasi/informasi.


* **Relevansi di Bab II (2.1.1):** Dikutip berdampingan dengan Ajiz et al. (2023) untuk membuktikan keterbatasan mendasar dari pendekatan *rule-based*, sekaligus menjadi pijakan argumentasi perlunya RAG yang mampu secara otomatis mengindeks dokumen regulasi (PDF) tanpa konversi manual ke aturan AIML.





---

#### 3. Ruindungan & Jacobus (2021)

* **Sitasi Lengkap:** Ruindungan & Jacobus (2021) — *"Chatbot Development for an Interactive Academic Information Services using the Rasa Open Source Framework"* (Jurnal Teknik Elektro dan Komputer / JTEK UNSRAT, Vol. 10 No. 1, Jan-Apr 2021)


* **Objek:** Chatbot Layanan Informasi Akademik Interaktif (LIANA) pada Program Studi Teknik Informatika Universitas Sam Ratulangi (UNSRAT).


* **Metode:** *Intent-based NLU & Intent-based Dialogue Management* berbasis Rasa Open Source (Rasa NLU untuk klasifikasi *intent* & ekstraksi entitas; Rasa Core untuk manajemen dialog/policy). Terintegrasi dengan antarmuka Rasa X pada cloud server AWS EC2 instance.


* **Evaluasi:** Pengujian otomatis framework Rasa pada dataset FAQ prodi (188 sampel kalimat NLU untuk 12 *intent*, 31 sampel dialog/stories) dan pengujian percakapan *end-to-end* dengan pengguna nyata (20 model percakapan, 98 total aksi chatbot).


* **Hasil Kunci:** Evaluasi Rasa NLU memperoleh nilai *weighted average* Precision 0,995, Recall 0,995, dan F1-Score 0,995. Evaluasi model dialog (Rasa Core) memperoleh Accuracy 0,70, Precision 0,72, dan F1-Score 0,70.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** **Relevansi kelembagaan sangat tinggi** karena diteliti pada prodi yang sama (Teknik Informatika UNSRAT). Menandai transisi dari paradigma *rule-based* (AIML) ke paradigma *Machine Learning NLU*.


* **Kritik/Limitasi:** Terlihat *gap* performa yang lebar antara NLU (F1 0,995) dan manajemen dialog (F1 0,70). Hal ini terjadi karena Rasa Core bergantung pada jalur dialog kaku (*stories/rules*) yang gagal memprediksi respon tepat ketika pengguna melakukan percakapan di luar alur yang dilatihkan. Selain itu, teks respon (*utterances*) tetap harus ditulis manual secara statis.


* **Relevansi di Bab II (2.1.1) & Bab I:** Wajib menjadi *institutional baseline* utama di UNSRAT. Penelitian Anda melompati keterbatasan kaku *intent mapping* & *stories* milik Rasa ini dengan menerapkan RAG generatif yang tidak lagi memerlukan alur dialog terstruktur untuk menjawab pertanyaan akademik kompleks.





---

#### 4. Suasnawa et al. (2023)

* **Sitasi Lengkap:** Suasnawa et al. (2023) — *"Chatbot-Based Student Information Service in Indonesian Language"* (Proceedings of the 5th International Conference on Applied Science and Technology on Engineering Science / ICAST-ES 2022, SCITEPRESS 2023)


* **Objek:** Chatbot layanan informasi akademik mahasiswa berbahasa Indonesia di Politeknik Negeri Bali (PNB).


* **Metode:** *Intent-based NLU & Machine Learning Dialogue Management* berbasis Rasa Framework (Rasa NLU + Rasa Core + Rasa X). Menggunakan teknik *Interactive Learning* untuk memperluas variasi pola pertanyaan dan menekan *error* respon.


* **Evaluasi:** Evaluasi kuantitatif otomatis atas kinerja NLU dan model dialog menggunakan data percakapan aktual yang telah divalidasi.


* **Hasil Kunci:** Evaluasi NLU memperoleh Precision 0,955, Recall 0,962, dan F1-Score 0,962. Evaluasi model dialog menghasilkan Accuracy 0,82, Precision 0,85, dan F1-Score 0,85.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Mengonfirmasi bahwa penerapan *Interactive Learning* pada Rasa Framework mampu mendongkrak F1-Score model dialog (dari 0,70 pada Ruindungan & Jacobus menjadi 0,85).


* **Kritik/Limitasi:** Walaupun F1-Score dialog meningkat, sistem ini tetap tidak sanggup menyintesis jawaban yang membutuhkan penalaran lintas-dokumen regulasi. Jawaban yang diberikan terbatas pada respon tunggal yang dipetakan pada *intent* tertentu.


* **Relevansi di Bab II (2.1.1):** Menjadi representasi kuat pemanfaatan Rasa/NLU pada institusi pendidikan di Indonesia. Digunakan untuk menunjukkan batas kemampuan pendekatan NLU *intent-based*: meskipun mampu mengenali maksud kalimat dengan baik, arsitektur ini tidak memiliki komponen *retrieval* berbasis vektor/dokumen maupun generator LLM untuk merekonstruksi jawaban bernuansa hukum/regulasi.





---

#### 5. Hidayat et al. (2024)

* **Sitasi Lengkap:** Hidayat et al. (2024) — *"IMPLEMENTASI RASA FRAMEWORK PADA CHATBOT LAYANAN AKADEMIK (Studi Kasus: Fakultas Ilmu Komputer Universitas Esa Unggul)"* (KOMPUTA: Jurnal Ilmiah Komputer dan Informatika, Vol. 13 No. 2, Okt 2024)


* **Objek:** Chatbot layanan akademik Fakultas Ilmu Komputer Universitas Esa Unggul.


* **Metode:** *Intent-based NLU & Dialogue Management* berbasis RASA Framework (v3.6.15 dengan Python 3.9) yang diintegrasikan ke platform instant messaging Telegram melalui Bot Telegram API, dibangun dengan metode SDLC Waterfall.


* **Evaluasi:** *Black-box testing* melalui terminal dan pengujian fungsionalitas percakapan *end-to-end* di aplikasi Telegram untuk 24 topik pertanyaan akademik (salam, kalender akademik, jadwal UTS/UAS, pengurusan surat, syarat sidang TA, MBKM).


* **Hasil Kunci:** Chatbot terbukti akurat dalam menjawab seluruh skenario percakapan uji *black-box* (5 sampel percakapan utama) serta sukses terintegrasi penuh pada platform Telegram.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Mewakili tren studi paling mutakhir (2024) untuk pendekatan Rasa/NLU yang dikombinasikan dengan *messaging API* (Telegram).


* **Kritik/Limitasi:** Evaluasi hanya dilakukan secara kualitatif (*valid/akurat*) pada sampel percakapan terbatas tanpa melaporkan metrik statistik formal (Precision, Recall, F1-Score NLU/Dialog). Seluruh jawaban tetap diketik manual pada file `domain.yml`, sehingga pencarian informasi tidak bersifat terdistribusi ke dokumen regulasi asli.


* **Relevansi di Bab II (2.1.1):** Dikutip sebagai penutup review paradigma NLU/Rasa modern. Studi ini menegaskan bahwa meskipun Rasa v3.x telah modern dan mudah diintegrasikan ke Telegram, kelemahan utamanya tetap ada pada ketergantungan pembuatan *intent/rules/responses* manual, yang menjadi *entry point* bagi argumen RAG (LangChain + ChromaDB/BM25 + Gemini) pada skripsi Anda.





---


Berikut adalah laporan ringkasan komprehensif dan analisis dampak dari **5 file paper tambahan** yang Anda kirimkan. Seluruh rangkuman ini disusun mengikuti struktur standar yang persis seperti sebelumnya, diselaraskan denganSub-bab pada Bab II (2.1.1 hingga 2.1.5), serta berpegang teguh pada prinsip zero-hallucination.

---

#### 6. Al Fajri & Hartono (2024)

* **Sitasi Lengkap:** Al Fajri & Hartono (2024) — *"Pengembangan Aplikasi Chatbot Telegram Menggunakan Framework Rasa untuk Pelayanan Administrasi di Perguruan Tinggi Universitas Stikubank"* (Jurnal JTIK: Jurnal Teknologi Informasi dan Komunikasi, Vol. 8 No. 1, Jan 2024).


* **Objek:** Layanan administrasi akademik mahasiswa dan calon mahasiswa di Biro Administrasi Akademik dan Kemahasiswaan (BAAK) Universitas Stikubank (Unisbank) Semarang.


* **Metode:** *Intent-based NLU & Dialogue Management* berbasis Rasa Open Source Framework yang dihubungkan ke platform Telegram Messenger melalui ngrok tunnel (API HTTP port 5005). Dataset pelatihan terdiri dari 213 sampel kalimat NLU dan 27 sampel dialog.


* **Evaluasi:** Black-box testing pada 4 skenario layanan (pembayaran SPP, jadwal kuliah, persyaratan penerimaan mahasiswa baru, dan unduh KHS via link Google Drive). Sistem juga dilengkapi validasi format teks dan verifikasi NIM/nama mahasiswa.


* **Hasil Kunci:** Chatbot mampu memahami pertanyaan NLU dan menjalankan perintah terstruktur dengan baik di Telegram. Namun, sistem mengalami kendala kekacauan jawaban (*random response*) ketika dimasukkan kata acak/kompleks karena penambahan *rules* pada Rasa Framework membuat locking jawaban yang sesuai menjadi sulit.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Mengonfirmasi kepraktisan integrasi Rasa Open Source dengan Telegram API untuk kebutuhan administrasi BAAK kampus di Indonesia.


* **Kritik/Limitasi:** Penulis mengakui adanya kendala skalabilitas pada Rasa Framework: semakin banyak kata kunci dan aturan (*rules*) yang dimasukkan, semakin sulit sistem mempertahankan konsistensi jawaban.


* **Relevansi di Bab II (2.1.1):** Dikutip bersama Ruindungan & Jacobus (2021) dan Hidayat et al. (2024) di Sub-bab 2.1.1 untuk mempertegas keterbatasan mendasar Rasa Framework dalam menangani skenario percakapan yang semakin kompleks.





---

#### 7. M Ikhsan et al. (2025)

* **Sitasi Lengkap:** M Ikhsan et al. (2025) — *"Implementasi Teknologi Chatbot sebagai Media Informasi di Universitas Negeri Medan"* (Jurnal Teknik Mesin, Industri, Elektro dan Informatika / JTMEI, Vol. 4 No. 1, Feb 2025).


* **Objek:** Layanan informasi akademik dan profil kampus untuk mahasiswa dan calon mahasiswa di Universitas Negeri Medan (UNIMED).


* **Metode:** *Artificial Neural Network* (ANN) menggunakan kelas model `Sequential` dari pustaka Keras/TensorFlow. Pengembangan menggunakan metode SDLC dan diimplementasikan pada aplikasi Telegram melalui Telegram Bot API.


* **Evaluasi:** Black-Box Testing pada 9 kategori *command/keyword* utama (`/Unimed`, `/Penerimaan`, `/Kurikulum`, `/Fasilitas`, `/Fakultas`, `/Kriteria`, `/Jurusan dan Prodi`, `/Organisasi`, `/Prosedur`) serta *command* navigasi (`/help`, `/location`, `/greetings`, `/start`).


* **Hasil Kunci:** Pengujian *Black-Box* menunjukkan seluruh fungsi *command* diterima sesuai rancangan, dengan tingkat akurasi respons sistem berada pada kisaran 70%.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Menunjukkan penerapan arsitektur *neural network* klasifikasi sederhana (Keras `Sequential`) untuk menangani perintah pesan terstruktur di Telegram.


* **Kritik/Limitasi:** **Bukan arsitektur LLM maupun RAG**, melainkan *classifier neural network* klasik. Akurasi sebesar 70% tergolong moderat dan sistem sangat terikat pada perintah (*command*) yang telah diprogramkan.


* **Relevansi di Bab II (2.1.1 / 2.1.2):** Sebagaimana hasil audit pada Rencana Revisi, paper ini **bukan contoh LLM**. Jika dipertahankan di Sub-bab 2.1.1, harus diframing sebagai pendekatan *Neural Network* Klasik untuk memperlihatkan tahapan evolusi teknologi: *Rule-Based AIML* → *Neural Network Klasik* → *Machine Learning NLU* → *Generative LLM & RAG*.





---

#### 8. Muna et al. (2025)

* **Sitasi Lengkap:** Muna et al. (2025) — *"SIAKIF-BOTS: GEMINI AI FOR ACADEMIC SERVICE CHATBOTS"* (Journal of Applied Engineering and Technological Science / JAETS, Vol. 6 No. 2, Apr 2025).


* **Objek:** Chatbot layanan akademik "SiAkif" di Telkom University Purwokerto (mencakup KRS, MBKM, Tugas Akhir, dan informasi fasilitas).


* **Metode:** Generative Large Language Model (LLM) berbasis Google Gemini API (dianalisis perbandingan antara Gemini 1.0 Pro, Gemini 1.5 Flash, Gemini 1.5 Pro, dan BERT). Diintegrasikan ke Telegram Bot menggunakan Google AI Studio API. Konfigurasi generasi: `temperature=0.7`, `top_p=0.75`, `top_k=64`, dan `max_output_tokens=8192`.


* **Evaluasi:** Pengujian pada 15 kueri uji yang terbagi ke 3 kategori (5 *in-dataset*, 5 *out-of-dataset/relevant*, 5 *out-of-context/irrelevant*). Metrik evaluasi mencakup BLEU Score (otomatis dan manual) serta *Response Time* (detik).


* **Hasil Kunci:** Model **Gemini 1.5 Flash** meraih kinerja terbaik dengan akurasi BLEU Score 88% dan waktu respon rata-rata 7,2 detik. Pengujian kueri *in-dataset* mencatatkan rata-rata BLEU Score 0,88 (otomatis) dan 0,86 (manual). Kueri di luar konteks berhasil ditolak secara konsisten dengan pesan *"Maaf, Saya Tidak Dilatih Untuk Itu"*. BERT mendapatkan kinerja terendah (akurasi 27%, respon 12,3 detik).


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Menjadi preseden kuat adopsi LLM generatif terkini (Gemini 1.5 Flash) pada platform Telegram untuk layanan akademik perguruan tinggi di Indonesia.


* **Kritik/Limitasi:** Evaluasi kualitas teks generasi hanya mengandalkan BLEU Score (*n-gram overlap*) tanpa metrik evaluasi LLM/RAG modern (seperti Ragas). Tidak memiliki komponen *retriever* terpisah (bukan RAG terkontrol), melainkan mengandalkan *prompting/fine-tuning* langsung pada LLM.


* **Relevansi di Bab II (2.1.2):** Rujukan utama untuk adopsi Google Gemini pada layanan akademik. Skripsi Anda menyempurnakan pendekatan Muna et al. dengan menambahkan arsitektur RAG terkontrol (ChromaDB/BM25) dan kerangka evaluasi 4-metrik Ragas.





---

#### 9. Priccilia & Girsang (2024)

* **Sitasi Lengkap:** Priccilia & Girsang (2024) — *"Indonesian generative chatbot model for student services using GPT"* (International Journal of Informatics and Communication Technology / IJ-ICT, Vol. 13 No. 1, Apr 2024).


* **Objek:** Chatbot layanan mahasiswa terkait praktikum (prosedur operasional laboratorium, protes kelompok, protes nilai) pada perguruan tinggi swasta di Indonesia.


* **Metode:** *Fine-tuning* arsitektur Generative Pre-trained Transformer 2 (GPT-2) Bahasa Indonesia dalam 3 varian ukuran (Small 12 layer, Medium 24 layer, Large 28 layer). Menggunakan teknik augmentasi data *Easy Data Augmentation* (EDA) dan *BERT fill-mask pipeline* (memperluas dataset dari 644 pasangan QA menjadi 1.288 pasangan QA).


* **Evaluasi:** BLEU Score, Perplexity (PPL), serta Training/Validation Loss pada *private dataset* (1030 train, 129 val, 129 test) dan MultiWOZ terjemahan.


* **Hasil Kunci:** **GPT-2 Small** memberikan kinerja tertinggi dengan BLEU Score 0,753 (Loss 1,720; PPL 974,13). Varian GPT-2 Medium (BLEU 0,565) dan Large (BLEU 0,570) mengalami *overfitting* berat. Penulis secara tegas menyimpulkan bahwa *generative chatbot* berbasis *fine-tuning* standalone **sangat tidak direkomendasikan** untuk domain layanan mahasiswa yang sempit dengan dataset terbatas.


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Menyediakan bukti empiris krusial mengenai bahaya *overfitting* dan kegagalan *fine-tuning* LLM standalone pada korpus akademik yang terbatas.


* **Kritik/Limitasi:** Nilai Perplexity yang sangat tinggi (>900) menunjukkan model mengalami kesulitan mendasar dalam memprediksi urutan kata saat diuji pada data baru (*poor generalization*).


* **Relevansi di Bab II (2.1.2 & 2.1.5):** Menjadi pijakan *Research Gap* yang sangat penting bagi skripsi Anda: *fine-tuning* standalone LLM pada domain akademik sempit terbukti gagal/overfit (Priccilia & Girsang, 2024), sehingga pendekatan **RAG (Retrieval-Augmented Generation)** berbasis *in-context learning* menjadi solusi yang tepat tanpa perlu mengubah/mengisolasi bobot parameter model.





---

#### 10. Ji et al. (2023)

* **Sitasi Lengkap:** Ji et al. (2023) — *"Towards Mitigating Hallucination in Large Language Models via Self-Reflection"* (Findings of the Association for Computational Linguistics: EMNLP 2023, Des 2023).


* **Objek:** Mitigasi masalah halusinasi pada sistem Generative Question-Answering (GQA) domain medis/kesehatan.


* **Metode:** Kerangka kerja *interactive self-reflection* yang terdiri dari 3 *loop*: (1) *Factual Knowledge Acquiring Loop* (generasi pengetahuan latar belakang + evaluasi faktualitas via *in-context instruction scorer* + *refinement*); (2) *Knowledge-Consistent Answering Loop* (generasi jawaban berbasis pengetahuan + evaluasi konsistensi via CTRLEval + *refinement*); (3) *Question-Entailment Answering Loop* (evaluasi *entailment* via *Sentence-BERT similarity*). Diuji pada Vicuna-7B, Alpaca-LoRA-7B, ChatGPT (175B), MedAlpaca-7B, dan Robin-medical-7B pada 5 dataset medis (PubMedQA, MedQuAD, MEDIQA2019, LiveMedQA2017, MASH-QA).


* **Evaluasi:** MedNLI (tingkat sampel dan kalimat), CTRLEval, F1, ROUGE-L, serta *Human Evaluation* via Mechanical Turk (klasifikasi *Fact Inconsistency*, *Query Inconsistency*, *Tangentiality*).


* **Hasil Kunci:** Metode *self-reflection loop* secara signifikan meningkatkan nilai MedNLI (contoh: Alpaca-LoRA-7B pada PubMedQA melonjak dari 0,0940 menjadi 0,4640) dan menekan tingkat halusinasi (faktual, kueri, maupun tangensial) pada seluruh skala model (7B hingga 175B).


* **Dampak & Penilaian Kritis terhadap Penelitian:**
* **Positif:** Menyediakan kerangka teoretis yang sangat matang mengenai taksonomi halusinasi LLM (*Fact Inconsistency*, *Query Inconsistency*, *Tangentiality*) serta teknik mitigasinya melalui *feedback loop*.


* **Kritik/Limitasi:** Membutuhkan *inference time* dan biaya token yang lebih tinggi karena proses perulangan (*generate-score-refine*).


* **Relevansi di Bab II (2.1.4 / 2.1.5):** Dikutip pada Sub-bab Evaluasi Kinerja Sistem Berbasis LLM & Mitigasi Halusinasi. Taksonomi halusinasi dari Ji et al. (2023) sangat relevan dipakai untuk mendukung analisis kualitatif pola kegagalan sistem (RQ3) pada skripsi Anda.





---

### Pemetaan Ringkas Penempatan 10 Paper di Bab II (2.1.1 – 2.1.5)

Dengan masuknya 5 paper tambahan ini, berikut adalah peta distribusi seluruh 10 paper yang telah dirangkum:

| Sub-bab | Fokus Pembahasan | Paper yang Dikutip |
| --- | --- | --- |
| **2.1.1** | Pendekatan Chatbot Akademik Tradisional & NLU | Ajiz et al. (2023), Guntoro et al. (2020), M Ikhsan et al. (2025) *(Neural Network Klasik)*, Ruindungan & Jacobus (2021), Suasnawa et al. (2023), Hidayat et al. (2024), Al Fajri & Hartono (2024).

 |
| **2.1.2** | Adopsi Large Language Models (LLM) pada Layanan Akademik | Priccilia & Girsang (2024) *(Kegagalan Fine-tuning Standalone)*, Muna et al. (2025) *(Adopsi Generative Gemini)*.

 |
| **2.1.4** | Evaluasi Kinerja & Mitigasi Halusinasi LLM | Ji et al. (2023) *(Taksonomi Halusinasi & Self-Reflection)*.

 |
| **2.1.5** | Research Gap & Sintesis Penutup | Mengontraskan kegagalan *Fine-tuning* (Priccilia & Girsang) dan keterbatasan *Prompting* tanpa Retriever (Muna et al.) dengan keunggulan RAG terkontrol (ChromaDB/BM25 + Gemini) yang diuji kuadran Ragas.

 |

---
#### 32. Vadlamani & Borada (2025)

* **Sitasi Lengkap:** Vadlamani, S., & Borada, D. (2025) — *"The Role of LLM Agent Apps in Conversational AI"* (International Journal of Research in Modern Engineering and Emerging Technology / IJRMEET, Vol. 13, Issue 04, April 2025, hlm. 205–223).


* **Objek:** Peran fungsional *LLM Agent Applications* dalam evolusi Conversational AI, komparasi terhadap chatbot tradisional, serta evaluasi eksperimental kinerja agen pada skenario multi-domain (*customer service, healthcare support, educational guidance*).


* **Metode:**
1. *Pergeseran Paradigma Arsitektur:* Menguraikan evolusi dari *Rule-based Chatbots* $\rightarrow$ *Standalone LLM Chatbots* $\rightarrow$ *LLM Agent Applications* (agen otonom berbasis LLM yang dilengkapi mekanisme memori, *real-time feedback loops*, *domain customization*, dan *multimodal integration*).


2. *Simulasi Eksperimental Multi-Domain:* Pengujian agen LLM pada 3 skenario (*Customer Service, Healthcare Assistance, Educational Support*) menggunakan metrik multidimensi:
* *Contextual Retention* (persentase retensi konteks pada percakapan *multi-turn*: diukur pada *Turn 1* dan *Turn 2+*).


* *Response Accuracy* (% Jawaban Benar, Salah, Ambigu).


* *User Engagement* (durasi interaksi rata-rata, *response rate*, % *follow-up queries*).


* *Emotional Intelligence & User Satisfaction* (% Keterlibatan Emosional dan skor Kepuasan Pengguna skala 1–10).


* *Task Completion Rate & Adaptability* (% Penyesuaian *real-time* & % Penyelesaian Tugas).






* **Hasil Kunci:**
* *Retensi Konteks Multi-Turn:* Skenario *Customer Service* mencatatkan retensi konteks tertinggi (**90%**), disusul *Educational Support* (**85%**), sedangkan *Healthcare Assistance* mengalami penurunan retensi paling drastis (**70%** retensi; 15% hilang di turn 1, 15% hilang di turn 2+) akibat tingginya kompleksitas dan variabilitas kueri.


* *Akurasi Respons:* *Customer Service* (**85% benar**), *Educational Support* (**80% benar**), dan *Healthcare Assistance* (**75% benar**, 15% salah, 10% ambigu).


* *Keterlibatan Emosional & Kepuasan Pengguna:* Skenario *Healthcare Assistance* mencatatkan skor kepuasan tertinggi (**9,2/10**) karena tingkat *High Emotional Engagement* yang dominan (**80%**), disusul *Customer Service* (8,5/10) dan *Educational Support* (8,0/10).


* *Tingkat Penyelesaian Tugas (Task Completion Rate):* *Customer Service* (**90%**), *Educational Support* (**85%**), dan *Healthcare Assistance* (**80%**).


* Penulis menyimpulkan bahwa mekanisme retensi memori (*memory retention*) dan penyesuaian *real-time* berbasis umpan balik adalah kunci utama untuk mempertahankan koherensi percakapan *multi-turn*.




* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* **Positif:** Menyediakan bukti empiris mutakhir (2025) mengenai dinamika penurunan retensi konteks (*context loss*) pada percakapan *multi-turn* yang kompleks.


* **Kritik/Limitasi:** Pengujian menggunakan profil partisipan sintetis (*fabricated user profiles*) dalam lingkungan simulasi terkontrol.




* **Relevansi di Sub-bab 2.2 (Dasar Teori Arsitektur LLM Agent & Retensi Konteks):** Dikutip pada **Sub-bab 2.2 (Dasar Teori Arsitektur Agentic LLM & Pengelolaan Konteks Multi-Turn)**. Temuan Vadlamani & Borada (2025) melegitimasi krusialnya mengintegrasikan mekanisme *Vector Store / Retriever* (seperti ChromaDB/BM25 pada RAG) untuk menjaga retensi fakta agar tidak terjadi *context loss* saat percakapan akademik berlangsung secara *multi-turn*.

---

Berikut adalah hasil analisis dan ekstraksi terstruktur dari **3 file paper/buku asli** yang Anda kirimkan (`241ab197...pdf`, `1930f0d0...pdf`, dan `0fc0488e...pdf`).

Rangkuman ini disusun sesuai dengan standar format `sitasi-bab2.md` yang telah kita tetapkan, dengan penekanan khusus pada penyediaan fondasi teoretis untuk **Sub-bab 2.2 (Dasar Teori)** skripsi Anda.

---

### Rangkuman & Analisis 3 Sumber Fondasi Teoretis (Sub-bab 2.2 Dasar Teori)

---

#### 33. Manning, Raghavan, & Schütze (2009)

* **Sitasi Lengkap:** Manning, C. D., Raghavan, P., & Schütze, H. (2009). *An Introduction to Information Retrieval*. Cambridge University Press.
* **Objek / Cakupan:** Buku teks standar Information Retrieval (IR) modern yang mencakup teori, arsitektur, dan algoritma sistem pencarian informasi berbasis teks tak terstruktur hingga semi-terstruktur.
* **Metode / Materi Kunci:**
* Membahas struktur data **Inverted Index** (Dictionary & Postings List) sebagai fondasi utama efisiensi pencarian teks.
* *Linguistic Preprocessing & Tokenization*: pemrosesan karakter, *case folding*, penanganan *stop words*, serta *stemming/lemmatization*.
* **Model Retrieval Leksikal / Sparse:** Pembobotan *tf-idf*, *Vector Space Model* berbasis *cosine similarity*, serta model probabilistik **Okapi BM25** (yang memperhitungkan frekuensi term *tf*, *inverse document frequency/idf*, dan normalisasi panjang dokumen $L_d / L_{ave}$).
* *Index Construction & Compression*: algoritma *Blocked Sort-Based Indexing* (BSBI), *Single-Pass In-Memory Indexing* (SPIMI), *distributed indexing* (MapReduce), serta teknik kompresi *Variable Byte* (VB) dan $\gamma$-encoding.


* **Evaluasi:** Menguraikan metodologi evaluasi sistem IR menggunakan koleksi uji standar (seperti TREC dan INEX) serta metrik *unranked* dan *ranked retrieval* (Precision, Recall, *Interpolated Average Precision*, MAP, NDCG, dan statistik Kappa untuk *assessing relevance*).
* **Hasil Kunci:** Menyediakan landasan matematis dan algoritmik fundamental untuk *sparse/lexical retrieval* (BM25), kalkulasi skor keterhubungan dokumen, serta metode kompresi dan pengindeksan data berksala besar.
* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* **Positif:** Merupakan rujukan teoretis utama (*gold standard*) untuk menjelaskan mekanisme **BM25 / Sparse Retrieval** yang Anda gunakan pada **Config C**, serta struktur *inverted index* pada Bab 2.2.
* **Kritik / Limitasi:** Diterbitkan pada 2009 sehingga fokus utamanya terbatas pada IR klasik dan belum mencakup pendekatan *dense retrieval* berbasis *deep neural embeddings* modern maupun arsitektur RAG generatif.
* **Relevansi & Penempatan di Bab II (2.2):** Wajib dikutip di **Sub-bab 2.2.1 (*Inverted Index & Tokenization*)** dan **Sub-bab 2.2.2 (*Model Lexical/Sparse Retrieval: BM25*)**. Sebagaimana temuan audit (Poin 3.3), buku teoretis murni ini **dikeluarkan dari Tabel 2.1** (Penelitian Terkait Aplikatif) dan dialokasikan khusus mendasari Dasar Teori di Sub-bab 2.2.



---

#### 34. Chen, Fisch, Weston, & Bordes (2017) — DrQA

* **Sitasi Lengkap:** Chen, D., Fisch, A., Weston, J., & Bordes, A. (2017). Reading Wikipedia to Answer Open-Domain Questions. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 1870–1879.
* **Objek:** *Open-Domain Question Answering* (ODQA) berbasis dokumen teks penuh Wikipedia (~5,07 juta artikel) tanpa bergantung pada *Knowledge Base* terstruktur (*Machine Reading at Scale* / MRS).
* **Metode:** Mengembangkan kerangka kerja **DrQA** yang terdiri dari dua modul terpisah:
1. **Document Retriever:** Memakai *unigram/bigram hashing* (menggunakan *murmur3 hash* hingga $2^{24}$ bin) yang dikombinasikan dengan pencocokan bobot TF-IDF untuk mengambil 5 artikel Wikipedia paling relevan secara cepat.
2. **Document Reader:** Model *machine comprehension* berbasis *Multi-layer Bidirectional Long Short-Term Memory* (BiLSTM) yang menerima representasi *feature vector* paragraf (*GloVe word embeddings*, *exact match features* [original, lowercase, lemma], *POS/NER/TF tags*, dan *aligned question embedding* via *attention*) untuk memprediksi *span* posisi jawaban (*start* dan *end*).


* Dilatih menggunakan kombinasi *Multitask Learning* dan *Distant Supervision* (DS) untuk mengasosiasikan pasangan pertanyaan-jawaban tanpa dokumen referensi eksplisit.


* **Evaluasi:** Diuji pada SQuAD (*standard machine comprehension* & *full Wikipedia setting*), serta 3 dataset ODQA lainnya: CuratedTREC, WebQuestions, dan WikiMovies. Metrik yang digunakan adalah *Exact Match* (EM) dan *F1-Score*.
* **Hasil Kunci:**
* Pada task SQuAD *single-paragraph reading*, Document Reader mencapai EM 70,0% dan F1 79,0% pada *test set*.
* Pada evaluasi *Full Wikipedia* (menjawab langsung dari seluruh Wikipedia), DrQA (Multitask DS) meraih akurasi EM 29,8% (SQuAD), 25,4% (CuratedTREC), 20,7% (WebQuestions), dan 36,5% (WikiMovies) — mengungguli sistem *pipeline* klasik YodaQA pada TREC dan WebQuestions.
* Pemanfaatan *distant supervision* dan *multitask learning* terbukti secara signifikan mendongkrak performa generalisasi model pada domain yang bervariasi.


* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* **Positif:** Menjadi *milestone* dan preseden historis penting yang meletakkan paradigma arsitektur **Retriever-Reader** (cikal bakal RAG) untuk menjawab pertanyaan dari korpus dokumen tak terstruktur skala besar.
* **Kritik / Limitasi:** Komponen *retrieval*-nya masih mengandalkan *sparse matching* klasik (TF-IDF bigram), dan *reader*-nya menggunakan BiLSTM ekstraktif (*span prediction*), bukan LLM generatif. Akibatnya, DrQA tidak mampu menyintesis jawaban baru yang bersifat generatif/parafase dan rentan mengalami penurunan akurasi (*drop* dari 69,5% ke 27,1% pada SQuAD) saat diuji pada skala dokumen penuh akibat *false positives* kalimat bertopik serupa.
* **Relevansi & Penempatan di Bab II (2.2 & 2.1):** Dikutip pada **Sub-bab 2.2.7 (Arsitektur Retrieval-Augmented / Pipeline Retriever-Reader)** untuk menunjukkan titik awal evolusi Retriever-Reader (DrQA: TF-IDF + BiLSTM) menuju RAG generatif modern (LangChain + ChromaDB/BM25 + Gemini). Juga dapat diletakkan di 2.1.3/2.1.4 sebagai pembanding evolusi arsitektur.



---

#### 35. Jurafsky & Martin (2026 Draft)

* **Sitasi Lengkap:** Jurafsky, D., & Martin, J. H. (2026). *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition with Language Models* (3rd ed. draft). Stanford University & University of Colorado at Boulder.
* **Objek / Cakupan:** Buku teks komprehensif acuan utama *Natural Language Processing* (NLP) dan *Large Language Models* (LLM) terkini (draf publik Januari 2026).
* **Metode / Materi Kunci (Fokus pada Bab 11 & Materi Terkait RAG/LLM):**
* **Subword Tokenization (Bab 2):** Menjelaskan algoritma *Byte-Pair Encoding* (BPE) sebagai standar pra-pemrosesan teks pada LLM modern untuk mengatasi masalah *unknown words* ($OOV$) dan efisiensi kosakata.
* **Embeddings & Vector Semantics (Bab 5):** Dasar matematika representasi *dense vector* (Word2vec, GloVe) dan pengukuran kemiripan semantik via *cosine similarity*.
* **Transformers & LLM Architecture (Bab 7, 8, 9, 10):** Mekanisme *Self-Attention*, *Transformer Blocks*, *Masked Language Models*, hingga tahap *Post-training* (*Instruction Tuning* dan *Preference Alignment/RLHF/DPO*).
* **Retrieval-based Models & RAG (Bab 11):** Secara spesifik mengulas pencarian berbasis vektor (*Information Retrieval with Dense Vectors*), evaluasi sistem IR, serta arsitektur **Retrieval-Augmented Generation (RAG)** yang mengombinasikan komponen *retriever* dengan generator LLM untuk menginjeksikan pengetahuan eksternal secara dinamis ke dalam *prompt*.


* **Evaluasi:** Menjelaskan kerangka evaluasi IR (Precision, Recall, F1, MAP) serta evaluasi Question Answering / RAG (*Exact Match*, *F1-Score*, *Perplexity*, ROUGE, BLEU, serta metrik kualitas RAG).
* **Hasil Kunci:** Menyajikan formulasi teoretis dan arsitektural paling mutakhir mengenai bagaimana arsitektur RAG bekerja: mengintegrasikan pencarian konteks terrelevant (*sparse/dense*) dengan augmentasi *prompt* pada LLM untuk menekan risiko halusinasi faktual dan mengatasi keterbatasan memori parametrik LLM.
* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* **Positif:** Merupakan **rujukan teoretis paling authoritative dan mutakhir (2026)** untuk mendasari seluruh konsep utama pada Sub-bab 2.2 skripsi Anda (Tokenization BPE, Dense Embeddings, Transformer, LLM Gemini, dan Arsitektur RAG).
* **Kritik / Limitasi:** Sebagai buku teks umum, Jurafsky & Martin menyajikan arsitektur dan landasan teoretis secara umum, namun tidak menyediakan angka performa empiris spesifik pada korpus peraturan akademik perguruan tinggi Indonesia (yang menjadi eksperimen spesifik skripsi Anda).
* **Relevansi & Penempatan di Bab II (2.2):** Rujukan fondasi utama untuk **Sub-bab 2.2.4 (*Subword Tokenization & BPE*)**, **Sub-bab 2.2.5 (*Large Language Models & Gemini*)**, **Sub-bab 2.2.6 (*Dense Retrieval & Vector Embeddings*)**, dan **Sub-bab 2.2.7 (*Retrieval-Augmented Generation / RAG*)**.



---

### Pemetaan Penempatan 3 Paper/Buku Baru pada Sub-bab 2.2 (Dasar Teori)

Dengan dibedahnya 3 sumber teoretis ini, berikut adalah pemetaan penempatannya di **Sub-bab 2.2 (Dasar Teori)** Bab II Skripsi Anda:

| Sub-bab 2.2 | Judul Topik Teori | Rujukan Utama yang Digunakan |
| --- | --- | --- |
| **2.2.1** | *Inverted Index* & Pra-pemrosesan Teks | Manning et al. (2009), Jurafsky & Martin (2026) |
| **2.2.2** | *Sparse/Lexical Retrieval* & Algoritma Okapi BM25 | Manning et al. (2009) |
| **2.2.3** | *Vector Semantics*, *Dense Embeddings*, & Cosine Similarity | Jurafsky & Martin (2026), Manning et al. (2009) |
| **2.2.4** | *Subword Tokenization* (Byte-Pair Encoding / BPE) | Jurafsky & Martin (2026) |
| **2.2.5** | *Large Language Models* (LLM) & Arsitektur Gemini | Jurafsky & Martin (2026) |
| **2.2.6** | Arsitektur *Retrieval-Augmented Generation* (RAG) & Pipeline *Retriever-Reader* | Jurafsky & Martin (2026), Chen et al. (2017) *(DrQA)* |
| **2.2.7** | Metrik Evaluasi Sistem IR & Ragas | Manning et al. (2009), Jurafsky & Martin (2026) |

---