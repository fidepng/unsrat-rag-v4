### Bagian 1: Paper #1 – #5 (Baseline Chatbot Akademik AIML & Rasa NLU)

#### 1. Ajiz et al. (2023)

* **Sitasi Lengkap:** Ajiz et al. (2023) — *"Pengembangan Aplikasi Chatbot Informasi Akademik Berbasis Web Menggunakan Metode Artificial Intelligence Markup Language (AIML)"* (Media Jurnal Informatika / MJI, Vol. 15 No. 2, Des 2023)

* **Objek:** Chatbot layanan informasi akademik mahasiswa baru dan perkuliahan di Universitas Majalengka.

* **Metode:** *Rule-based / pattern matching* berbasis *Artificial Intelligence Markup Language* (AIML) berbasis web (PHP 8, JavaScript, MySQL, HTML 5). Alur memproses *tokenizing* dan pencocokan aturan *template*. Jika pertanyaan tidak ditemukan pada basis pengetahuan AIML, pertanyaan dialihkan ke antarmuka admin untuk ditinjau dan ditambahkan secara manual.

* **Evaluasi:** Pengujian fungsionalitas via *Black Box Testing* (10 skenario pertanyaan akademik paling sering ditanyakan hasil pendataan 100 responden) dan *White Box Testing*.

* **Hasil Kunci:** Pengujian *black box* mencatatkan hasil 100% valid untuk 10 skenario pertanyaan akademik yang telah terdefinisi di database; sistem mampu mengalirkan kueri *out-of-database* ke dashboard admin.

* **Dampak & Penilaian Kritis terhadap Penelitian:**
  * **Positif:** Menggambarkan baseline historis pendekatan konvensional berbasis aturan kaku (*rule-based AIML*) pada chatbot perguruan tinggi di Indonesia.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Sangat kaku bergantung pada pencocokan *pattern* eksplisit. Tidak memiliki kapabilitas *Natural Language Understanding* (NLU) maupun *semantic search*; variasi sintaksis/parafase yang tidak didaftarkan pada aturan AIML akan langsung gagal dijawab.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Angka akurasi 100% bersifat semu karena hanya diuji pada *query* yang cocok secara eksak dengan *template* yang disiapkan. Pemeliharaan basis pengetahuan sangat tidak efisien karena admin harus menyunting file XML/AIML secara manual setiap ada perubahan regulasi/informasi.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Terlihat *gap* performa yang lebar antara NLU (F1 0,995) dan manajemen dialog (F1 0,70). Hal ini terjadi karena Rasa Core bergantung pada jalur dialog kaku (*stories/rules*) yang gagal memprediksi respon tepat ketika pengguna melakukan percakapan di luar alur yang dilatihkan. Selain itu, teks respon (*utterances*) tetap harus ditulis manual secara statis.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Walaupun F1-Score dialog meningkat, sistem ini tetap tidak sanggup menyintesis jawaban yang membutuhkan penalaran lintas-dokumen regulasi. Jawaban yang diberikan terbatas pada respon tunggal yang dipetakan pada *intent* tertentu.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi hanya dilakukan secara kualitatif (*valid/akurat*) pada sampel percakapan terbatas tanpa melaporkan metrik statistik formal (Precision, Recall, F1-Score NLU/Dialog). Seluruh jawaban tetap diketik manual pada file `domain.yml`, sehingga pencarian informasi tidak bersifat terdistribusi ke dokumen regulasi asli.

* **Relevansi di Bab II (2.1.1):** Dikutip sebagai penutup review paradigma NLU/Rasa modern. Studi ini menegaskan bahwa meskipun Rasa v3.x telah modern dan mudah diintegrasikan ke Telegram, kelemahan utamanya tetap ada pada ketergantungan pembuatan *intent/rules/responses* manual, yang menjadi *entry point* bagi argumen RAG (LangChain + ChromaDB/BM25 + Gemini) pada skripsi Anda.

---

### Bagian 2: Paper #6 – #10 (Pengembangan NLU & Telegram API)

#### 6. Al Fajri & Hartono (2024)

* **Sitasi Lengkap:** Al Fajri & Hartono (2024) — *"Pengembangan Aplikasi Chatbot Telegram Menggunakan Framework Rasa untuk Pelayanan Administrasi di Perguruan Tinggi Universitas Stikubank"* (Jurnal JTIK: Jurnal Teknologi Informasi dan Komunikasi, Vol. 8 No. 1, Jan 2024).

* **Objek:** Layanan administrasi akademik mahasiswa dan calon mahasiswa di Biro Administrasi Akademik dan Kemahasiswaan (BAAK) Universitas Stikubank (Unisbank) Semarang.

* **Metode:** *Intent-based NLU & Dialogue Management* berbasis Rasa Open Source Framework yang dihubungkan ke platform Telegram Messenger melalui ngrok tunnel (API HTTP port 5005). Dataset pelatihan terdiri dari 213 sampel kalimat NLU dan 27 sampel dialog.

* **Evaluasi:** Black-box testing pada 4 skenario layanan (pembayaran SPP, jadwal kuliah, persyaratan penerimaan mahasiswa baru, dan unduh KHS via link Google Drive). Sistem juga dilengkapi validasi format teks dan verifikasi NIM/nama mahasiswa.

* **Hasil Kunci:** Chatbot mampu memahami pertanyaan NLU dan menjalankan perintah terstruktur dengan baik di Telegram. Namun, sistem mengalami kendala kekacauan jawaban (*random response*) ketika dimasukkan kata acak/kompleks karena penambahan *rules* pada Rasa Framework membuat locking jawaban yang sesuai menjadi sulit.

* **Dampak & Penilaian Kritis terhadap Penelitian:**
  * **Positif:** Mengonfirmasi kepraktisan integrasi Rasa Open Source dengan Telegram API untuk kebutuhan administrasi BAAK kampus di Indonesia.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Penulis mengakui adanya kendala skalabilitas pada Rasa Framework: semakin banyak kata kunci dan aturan (*rules*) yang dimasukkan, semakin sulit sistem mempertahankan konsistensi jawaban.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** **Bukan arsitektur LLM maupun RAG**, melainkan *classifier neural network* klasik. Akurasi sebesar 70% tergolong moderat dan sistem sangat terikat pada perintah (*command*) yang telah diprogramkan.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi kualitas teks generasi hanya mengandalkan BLEU Score (*n-gram overlap*) tanpa metrik evaluasi LLM/RAG modern (seperti Ragas). Tidak memiliki komponen *retriever* terpisah (bukan RAG terkontrol), melainkan mengandalkan *prompting/fine-tuning* langsung pada LLM.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Nilai Perplexity yang sangat tinggi (>900) menunjukkan model mengalami kesulitan mendasar dalam memprediksi urutan kata saat diuji pada data baru (*poor generalization*).

* **Relevansi di Bab II (2.1.2 & 2.1.5):** Menjadi pijakan *Research Gap* yang sangat penting bagi skripsi Anda: *fine-tuning* standalone LLM pada domain akademik sempit terbukti gagal/overfit (Priccilia & Girsang, 2024), sehingga pendekatan **RAG (Retrieval-Augmented Generation)** berbasis *in-context learning* menjadi solusi yang tepat tanpa perlu mengubah/mengisolasi bobot parameter model.

---

#### 10. Ji et al. (2023)

* **Sitasi Lengkap:** Ji, Z., Yu, T., Xu, Y., Lee, N., Ishii, E., & Fung, P. (2023). Towards Mitigating Hallucination in Large Language Models via Self-Reflection. *Findings of the Association for Computational Linguistics: EMNLP 2023*, 1827–1843.

* **Objek:** Mitigasi masalah halusinasi pada sistem Generative Question-Answering (GQA) domain medis/kesehatan.

* **Metode:** Kerangka kerja *interactive self-reflection* yang terdiri dari 3 *loop*:
  1. *Factual Knowledge Acquiring Loop:* Generasi pengetahuan latar belakang + evaluasi faktual via *in-context instruction scorer* ($Fs(k\vert{}D,Q)$) + refleksi/pembenahan *prompt*.
  2. *Knowledge-Consistent Answering Loop:* Generasi jawaban berbasis pengetahuan + evaluasi konsistensi via CTRLEval + refleksi/pembenahan *prompt*.
  3. *Question-Entailment Answering Loop:* Evaluasi keterlibatan (*entailment*) jawaban terhadap pertanyaan via *Sentence-BERT similarity* dan MedNLI.
  4. Diuji pada Vicuna-7B, Alpaca-LoRA-7B, ChatGPT (175B), MedAlpaca-7B, dan Robin-medical-7B pada 5 dataset medis (PubMedQA, MedQuAD, MEDIQA2019, LiveMedQA2017, MASH-QA).

* **Evaluasi:** MedNLI (tingkat sampel dan kalimat), CTRLEval, F1, ROUGE-L, serta *Human Evaluation* (klasifikasi *Fact Inconsistency*, *Query Inconsistency*, *Tangentiality*). *Uji Ablasi* mengonfirmasi bahwa pembuangan tahap *refinement* atau deskripsi aspek menurunkan faktualitas.

* **Hasil Kunci:** Metode *self-reflection loop* secara signifikan meningkatkan nilai MedNLI (Alpaca-LoRA-7B pada PubMedQA melonjak dari 0,0940 ke 0,4640) dan menekan tingkat halusinasi (faktual, kueri, maupun tangensial) pada seluruh skala model (7B hingga 175B).

* **Dampak & Penilaian Kritis terhadap Penelitian:**
  * **Positif:** Menyediakan kerangka teoretis mendalam mengenai taksonomi halusinasi LLM (*Fact Inconsistency*, *Query Inconsistency*, *Tangentiality*) serta teknik mitigasinya melalui *feedback loop* tanpa *retraining* parameter.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Membutuhkan *inference time* dan biaya token yang lebih tinggi karena proses perulangan (*generate-score-refine*).

* **Relevansi di Bab II (2.1.4, 2.1.5 & Sub-bab 2.2.8):** Dikutip pada Sub-bab Evaluasi Kinerja Sistem Berbasis LLM, Mitigasi Halusinasi, dan Sub-bab 2.2.8 (*Mekanisme Self-Reflection & Evaluasi Faktualitas LLM*). Taksonomi halusinasi Ji et al. (2023) sangat relevan mendukung analisis kualitatif pola kegagalan sistem (RQ3) pada skripsi Anda.

### Bagian 3: Paper #11 – #16 (Vector Embedding, Retrieval & Arsitektur Transformer)

#### 11. Pratami et al. (2025)

* **Sitasi Lengkap:** Pratami et al. (2025) — *"LLM-Based Chatbot for the Indonesia University IT Service Desk: Integrating DeepSeek-v3 API and a RAG Approach"* (Proceedings of the 2025 International Conference on Data Science and Its Applications / ICODSA 2025, IEEE).

* **Objek:** Chatbot *IT Service Desk* (FAQ PUTI) untuk layanan bantuan teknologi informasi bagi dosen, mahasiswa, dan staf di lingkungan Telkom University, Indonesia.

* **Metode:** Arsitektur RAG modular berbasis *web interface* Streamlit dan database Supabase (penyimpanan *vector store* + *logging interaction* sebagai JSON). Tahapan mencakup:

1. *Document Ingestion:* Ekstraksi *multi-format* (PDF, DOCX, CSV, XLSX, TXT) dengan teknik segmentasi *hybrid sentence- and token-level*.

2. *Embedding & Retrieval:* Menggunakan model `MiniLM-L6-v2` Sentence Transformer; *vector store* disimpian di Supabase untuk pencarian *cosine similarity* ($top\text{-}k$ *contextual retrieval*).

3. *Generative LLM:* Integrasi API DeepSeek-v3 untuk sintesis jawaban.

4. *Evaluasi Prompting:* Menganalisis 9 strategi *prompting* (Zero-Shot, Few-Shot, Chain-of-Thought/CoT, Meta, Self-Consistency, Generate Knowledge, Prompt Chaining, Tree of Thoughts/ToT, Automatic Prompt Engineer/APE).

* **Evaluasi:**
1. *Testing Fungsional & Hardware:* Diuji pada laptop MSI Bravo 15 (AMD Ryzen 5 5600H, GPU Radeon RX 5500M, Windows 11) menggunakan *unittest framework*.

2. *Performance Benchmarking:* Pengukuran *response time* end-to-end dan *retrieval accuracy* ($top\text{-}5$).

3. *User Experience Questionnaire (UEQ):* Diberikan kepada 26 responden (dosen, mahasiswa, dan staf kemahasiswaan/IT) menguji 6 dimensi (Attractiveness, Perspicuity, Efficiency, Dependability, Stimulation, Novelty).

4. *Pengujian Prompting:* Evaluasi akurasi ($mean \pm SD$) dari 9 strategi *prompting* terhadap acuan jawaban pakar (*expert-curated references*).

* **Hasil Kunci:**
* Sistem beroperasi stabil 24/7 dengan *retrieval accuracy* ($top\text{-}5$) melebihi **98%**.

* *Average response time* sebesar **$2,1 \pm 0,2$ detik**, mencatatkan efisiensi 35% lebih cepat dibandingkan sistem *helpdesk legacy*.

* Evaluasi UEQ meraih skor rata-rata **$4,5 \pm 0,3$** (skala 5). Pada skala skala standar UEQ benchmark (-3 hingga +3), skor tertinggi dicapai oleh *Attractiveness* ($2,09 \pm 0,15$), disusul *Perspicuity* ($2,01 \pm 0,12$), *Efficiency* ($1,95 \pm 0,18$), *Dependability* ($1,92 \pm 0,20$), *Novelty* ($1,35 \pm 0,30$), dan *Stimulation* ($1,33 \pm 0,25$).

* Hasil komparasi *prompting*: **Chain-of-Thought (CoT)** mencatatkan akurasi tertinggi sebesar **$93,1 \pm 2,1\%$** (dengan *extra latency* +0,5 detik), disusul *Tree of Thoughts* ($92,5 \pm 2,2\%$), *Automatic Prompt Engineer* ($91,0 \pm 2,0\%$), *Prompt Chaining* ($90,0 \pm 2,7\%$), *Self-Consistency* ($89,7 \pm 2,5\%$), *Meta* ($88,4 \pm 3,0\%$), *Generate Knowledge* ($87,2 \pm 3,3\%$), *Few-Shot* ($83,7 \pm 3,8\%$), dan *Zero-Shot* terendah ($78,2 \pm 4,5\%$).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan preseden empiris paling mutakhir (2025) mengenai efektivitas integrasi DeepSeek-v3 API dengan RAG berbasis Supabase dan MiniLM-L6-v2 pada *IT Service Desk* perguruan tinggi di Indonesia.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi kualitas teks generasi hanya mengandalkan akurasi pencocokan manual terhadap acuan pakar dan kuesioner persepsi pengguna (UEQ), tanpa memanfaatkan kerangka evaluasi RAG terotomatisasi (*in-context evaluation*) seperti Ragas. Komponen *retriever* hanya menguji satu model *dense* (`MiniLM-L6-v2`) tanpa adanya komparasi terhadap *sparse retrieval* (BM25) maupun *hybrid retrieval*.

* **Relevansi di Bab II (2.1.3):** Dikutip pada Sub-bab 2.1.3 (Implementasi Arsitektur RAG) untuk menggambarkan tren implementasi RAG aplikatif pada helpdesk kampus di Indonesia. Kontras dengan skripsi Anda: Pratami et al. berfokus pada variasi *prompt engineering* dan pengalaman pengguna (UEQ), sedangkan skripsi Anda membandingkan dua mekanisme *retrieval* (*Dense ChromaDB* vs *Sparse BM25*) secara terkontrol dengan evaluasi kuadran Ragas pada korpus regulasi kampus.

---

#### 12. Neumann et al. (2025)

* **Sitasi Lengkap:** Neumann et al. (2025) — *"An LLM-Driven Chatbot in Higher Education for Databases and Information Systems"* (IEEE Transactions on Education, Vol. 68, No. 1, February 2025 / Published online Oct 2024).

* **Objek:** MoodleBot, chatbot terintegrasi Learning Management System (LMS) Moodle untuk mendukung *Self-Regulated Learning* (SRL) dan *help-seeking behavior* mahasiswa pada mata kuliah "Databases and Information Systems" (700+ peserta) di RWTH Aachen University, Jerman.

* **Metode:**
1. *Architecture & Ingestion:* RAG terintegrasi antarmuka chat & forum native Moodle. Dokumen (slide kuliah, catatan kuliah, lembar latihan) diolah via LangChain text splitter, di-embed menggunakan OpenAI `text-embedding-ada-002`, dan disimpan di vector database Weaviate.

2. *Agent & LLM:* Menggunakan LangChain agent (`BaseMultiActionAgent`) berbasis OpenAI `gpt-4` (temperatur = 0). Dilengkapi *tools*: Answer Generator (`create-stuff-documents-chain` dengan batas $top\text{-}5$ dokumen konteks), Question Generator (latihan soal acak), dan Specific Question Generator.

3. *Logging & Fact-Checker:* MongoDB untuk menyimpan riwayat percakapan dan estimasi biaya token. Pengujian faktualitas otomatis menggunakan *fact-checker chain* LangChain (`LLMSummarization-CheckerChain`) berbasis `gpt-3.5-turbo`.

* **Evaluasi:**
1. *Technology Acceptance Model (TAM):* Menguji 6 konstruk (Perceived Usefulness/PU, Perceived Ease of Use/PEOU, Attitude/AT, Behavioral Intention/BI, Self-Efficacy/SE, System Accessibility/SA) pada 46 mahasiswa yang telah lulus matkul (30 mengisi kuesioner Likert 1-5, diuji via Cronbach's alpha 0,688 - 0,802, Explorative Factor Analysis/PCA, dan Multiple Linear Regression).

2. *Akurasi & Fact-Checking:* Evaluasi manual oleh Teaching Assistant (TA) pada 65 respons + masukan mahasiswa (dianalisis via matriks konfusi), serta evaluasi otomatis oleh *fact-checker chain* pada 100 respons.

3. *Cost Analysis:* Perhitungan biaya API per token (embedding database setup $0,028; *similarity search* $0,0001/query; chat $0,01–$2,33/pesan; rerata $1,65 total per mahasiswa).

* **Hasil Kunci:**
* *Hasil TAM:* Mahasiswa memberikan persepsi sangat positif terhadap PEOU ($4,6 \pm 0,54$), PU ($4,46 \pm 0,73$), AT ($4,73 \pm 0,44$), dan SA ($4,3 \pm 0,88$). Namun, minat perilaku (BI) untuk memilih MoodleBot dibandingkan tutor manusia asli tergolong rendah/moderat (**2,7 $\pm 1,14$**), menegaskan bahwa chatbot LLM berfungsi sebagai pelengkap (*complement*), bukan pengganti pengajar manusia.

* *Akurasi Manual TA:* Sebesar **88%** dari 100 respons GPT terbukti faktual dan kongruen dengan materi kuliah. Pada matriks konfusi berbasis persepsi gabungan mahasiswa & TA (65 sampel), tercatat Akurasi 69,23%, Presisi 92,31%, Sensitivitas 67,92%, dan Spesifisitas 75%.

* *Automated Fact-Checking:* Evaluasi *fact-checker chain* (`gpt-3.5-turbo`) menghasilkan Akurasi 82%, Presisi 88,04%, Sensitivitas 92,05%, namun **Spesifisitas sangat buruk (hanya 8,33%)** dan *Negative Predictive Value* 12,5%. Penulis menyimpulkan secara tegas bahwa mengandalkan LLM biasa sebagai *fact-checker* otomatis **sangat tidak direkomendasikan** (*suboptimal*) karena kecenderungan bias/kegagalan mendeteksi pernyataan salah yang dihasilkannya sendiri.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan bukti ilmiah berstandar IEEE mengenai penerimaan RAG di LMS perguruan tinggi, kerangka analisis biaya API per siswa ($1,65), serta pengujian objektif terhadap batas kemampuan *automated fact-checking* LLM.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Bergantung pada arsitektur RAG *stuff chain* berbasis API proprietary bernilai tinggi (`gpt-4` + `ada-002`). Pengujian *fact-checker* otomatis bawaan LangChain terbukti gagal mendeteksi kesalahan (spesifisitas 8,33%) karena tidak terhubung langsung dengan konteks slide dan tidak memakai metrik evaluasi RAG yang terisolasi.

* **Relevansi di Bab II (2.1.3 & 2.1.4):** Dikutip pada Sub-bab 2.1.3 (Implementasi Arsitektur RAG di LMS) dan 2.1.4 (Evaluasi Kinerja & Fact-Checking). Temuan Neumann et al. mengenai buruknya spesifisitas *fact-checker chain* internal (8,33%) menjadi landasan argumentasi kritis di skripsi Anda mengenai krusialnya mengadopsi kerangka evaluasi RAG terpisah yang multi-metrik seperti **Ragas** (*Faithfulness, Answer Relevancy, Context Precision, Context Recall*).

---

#### 13. Firdaus et al. (2024)

* **Sitasi Lengkap:** Firdaus et al. (2024) — *"Integrating Retrieval-Augmented Generation with Large Language Model Mistral 7b for Indonesian Medical Herb"* (JISKA / Jurnal Informatika Sunan Kalijaga, Vol. 9, No. 3, September 2024, pp. 230-243).

* **Objek:** Chatbot layanan informasi dan Q&A tanaman obat / herbal medis khas Indonesia berbasis korpus 9 jurnal ilmiah akademis terakreditasi.

* **Metode:**
1. *Data Processing:* Preprocessing dokumen jurnal via LangChain document loader. Ukuran *chunk* ditetapkan 500 token, *max output tokens* 512, dan *temperature* 0,5.

2. *Embedding & Vector Store:* Menggunakan `sentence-transformers` dan FAISS CPU untuk pengindeksan semantik serta pencarian kemiripan (*similarity search*).

3. *Generative LLM:* Menerapkan RAG dan membandingkan dua *open-source* LLM 7B parameter: **Mistral 7b** vs **LLaMa2 7b**.

4. *Interface:* Aplikasi berbasis web menggunakan *framework* Chainlit.

* **Evaluasi:**
1. *Human Evaluation:* Penilaian kualitatif oleh pakar etnobotani (Dr. Tri Cahyanto, M.Si. dari UIN Sunan Gunung Djati Bandung) terhadap jawaban bot pada 6 pertanyaan medis/herbal (`Q1–Q6`).

2. *Automatic NLP Metrics:* Evaluasi kuantitatif menggunakan metrik ROUGE (Precision, Recall, F-Measure) dan METEOR score.

* **Hasil Kunci:**
* Penilaian pakar etnobotani mengonfirmasi bahwa RAG Mistral 7b menghasilkan jawaban yang valid dan sesuai dengan literatur ilmiah herbal Indonesia.

* *METEOR Score:* **Mistral 7b (0,22% / 0,22)** mengungguli LLaMa2 7b (**0,14% / 0,14**) secara signifikan.

* *ROUGE Precision:* LLaMa2 7b (0,18) lebih tinggi dibandingkan Mistral 7b (0,07). Hal ini terjadi karena Mistral 7b menghasilkan jawaban yang lebih kreatif dan panjang (variasi diksi).

* *Anomali LLaMa2 7b:* Pada kueri Q4 (herbal untuk demam), model LLaMa2 7b mengalami **kegagalan RAG / repetition loop**, di mana output generasi mengulang-ulang kata secara abnormal (`Compositae/Compositing...`), sedangkan Mistral 7b menjawab dengan lancar dan tepat tanpa *repetition error*.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Mengonfirmasi keunggulan *open-source* LLM (Mistral 7b) dikombinasikan dengan FAISS CPU untuk membangun RAG pada korpus ilmiah spesifik berkonteks Indonesia.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi kuantitatif sepenuhnya bergantung pada metrik *n-gram overlap* pemrosesan bahasa alami / *machine translation* klasik (ROUGE dan METEOR) terhadap teks acuan pakar. Metrik ini tidak mampu mengukur *grounding* jawaban terhadap dokumen sumber (*Faithfulness*) maupun kualitas pencarian *retriever* (*Context Precision/Recall*). Selain itu, ukuran chunk dikuncikan secara statis pada 500 token tanpa pengujian sensitivitas chunking.

* **Relevansi di Bab II (2.1.3):** Dikutip pada Sub-bab 2.1.3 (Implementasi Arsitektur RAG) sebagai representasi studi RAG berbasis *open-source model* pada domain spesifik di Indonesia. Skripsi Anda menyempurnakan pendekatan Firdaus et al. dengan mengevaluasi dua strategi *retrieval* (*dense* vs *sparse*) serta menggantikan metrik *n-gram overlap* dengan kerangka evaluasi Ragas.

---

#### 14. Robertson & Zaragoza (2009)

* **Sitasi Lengkap:** Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*, 3(4), 333–389.

* **Objek & Scope:** Monograf komprehensif dan survei teoretis mengenai *Probabilistic Relevance Framework* (PRF), *Binary Independence Model* (BIM), model 2-Poisson, formulasi matematis algoritma penataan dokumen BM25 (*Best Matching 25*), BM25F (*Structured Fields*), serta metode optimasi parameter.

* **Metode & Formulasi Matematika Kunci:**
  1. *Probability Ranking Principle (PRP):* Mengasumsikan relevansi biner dan independen untuk menata dokumen berdasarkan penurunan probabilitas $P(rel\vert{}d,q)$.
  2. *Binary Independence Model (BIM) & RSJ Weight:* $w_i^{RSJ} = \log \frac{(r_i + 0,5)(N - R - n_i + r_i + 0,5)}{(n_i - r_i + 0,5)(R - r_i + 0,5)}$. Tanpa informasi relevansi, mereduksi menjadi varian IDF: $w_i^{IDF} = \log \frac{N - n_i + 0,5}{n_i + 0,5}$.
  3. *2-Poisson Model & Eliteness:* Memodelkan variabel tersembunyi *eliteness* ($E_i \in \{0,1\}$) untuk menjelaskan hubungan antara *term frequency* ($tf$) dan relevansi. Kontribusi istilah tunggal diposisikan tidak melebihi batas saturasi $w_i^{BIM} = \log \frac{p_1 (1-p_0)}{(1-p_1) p_0}$.
  4. *Fungsi Saturasi Non-Linear BM25:* $w_i^{BM25}(tf) = \frac{tf}{k_1 \left((1-b) + b \frac{dl}{avdl}\right) + tf} \cdot w_i^{RSJ}$, di mana $k_1$ mengontrol saturasi ($1,2 - 2,0$) dan $b$ mengontrol normalisasi panjang ($0,5 - 0,8$).
  5. *BM25F (Structured Fields):* Menggabungkan frekuensi kata dari berbagai bidang dokumen (*title, body, anchor*) sebelum fungsi saturasi non-linear: $\tilde{tf}_i = \sum_{s=1}^S v_s \frac{tf_{si}}{B_s}$.

* **Evaluasi & Metrik:** Analisis teoritis dan empiris pada korpus TREC dan *web search* menggunakan metrik *Average Precision* (MAP), *Precision at k*, dan NDCG. Optimasi parameter dievaluasi via *Greedy Robust Line Search* dan gradien.

* **Hasil Kunci:** Membuktikan secara matematis dan empiris bahwa fungsi saturasi non-linear $tf$ dan normalisasi panjang dokumen pada BM25/BM25F konsisten menjadi standar emas (*gold standard*) pencarian leksikal (*sparse retrieval*) di dunia IR. BM25F terbukti mengungguli penggabungan linier skor individual per bidang.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menjadi **rujukan kanonis dan fondasi teoretis murni** untuk seluruh arsitektur *Sparse / Lexical Retrieval* berbasis BM25.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** BM25 beroperasi murni berdasarkan pencocokan kata kunci eksak (*exact keyword match*), tanpa pemahaman semantik kontinu sehingga rentan mengalami masalah *vocabulary mismatch*. Membutuhkan optimasi grid search/gradien untuk parameter $k_1$ dan $b$ pada korpus baru.

* **Relevansi di Bab II (Sub-bab 2.2.3):** Dikutip pada **Sub-bab 2.2.3 (Sparse Retrieval & Algoritma BM25/BM25F)** sebagai acuan teoretis utama untuk menjelaskan rumus pembobotan BM25, variabel tersembunyi *eliteness*, efek saturasi $k_1$, dan normalisasi $b$. Formulasi BM25 ini digunakan sebagai arsitektur *Sparse Retriever* (Arm Config C) untuk dibandingkan terhadap *Dense Retriever* ChromaDB + `gemini-embedding-001` (Arm Config B).

#### 15. Reimers & Gurevych (2019)

* **Sitasi Lengkap:** Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP)*, hlm. 3982–3992.

* **Objek:** Sentence-BERT (SBERT), modifikasi arsitektur pretrained BERT/RoBERTa menggunakan jaringan siam (*siamese*) dan triplet untuk menghasilkan *dense sentence embeddings* berdimensi tetap yang dapat dibandingkan secara efisien menggunakan *cosine similarity*.

* **Metode & Arsitektur:**
  1. *Masalah Cross-Encoder BERT:* Pencarian pasangan paling mirip pada 10.000 kalimat membutuhkan $\approx 50$ juta komputasi inferensi ($\approx 65$ jam pada GPU V100).
  2. *Siamese Architecture:* Mengumpankan kalimat A dan B secara terpisah ke jaringan BERT dengan bobot terikat (*shared/tied weights*).
  3. *Pooling Strategy:* Menguji `MEAN` (rerata seluruh token output), `MAX` (nilai maksimum), dan `CLS` (output token [CLS]). Strategi `MEAN` ditetapkan sebagai default.
  4. *Objective Functions:* *Classification Objective* ($o = \text{softmax}(W_t(u, v, \vert{}u-v\vert{}))$ pada SNLI 570k dan MultiNLI 430k pasang), *Regression Objective* (MSE pada *cosine similarity*), dan *Triplet Objective*.

* **Evaluasi & Metrik:** Evaluasi *Semantic Textual Similarity* (STS 2012–2016, STSb, SICK-R) mengukur Spearman's rank correlation $\rho$. Evaluasi transfer learning SentEval (7 tugas: MR, CR, SUBJ, MPQA, SST, TREC, MRPC), Argument Facet Similarity (AFS), dan Wikipedia Sections Distinction.

* **Hasil Kunci:**
  * *Efisiensi Komputasi:* Memangkas waktu pencarian pasangan kalimat dari **65 jam menjadi $\approx 5$ detik** (generasi 10.000 embedding SBERT) + **0,01 detik** (komputasi *cosine similarity*). GPU Throughput mencapai **2.042 kalimat/detik** dengan *smart batching*.
  * *Unsupervised STS Benchmark:* SBERT-NLI-large meraih korelasi Spearman **79,23** (vs `Avg. BERT embeddings` 46,35, `BERT CLS` 29,19, `GloVe` 58,02, `InferSent` 68,03, `USE` 74,92).
  * *Supervised STSb & SentEval:* SBERT-NLI-STSb-large meraih korelasi Spearman **86,10** pada STSb (on-par dengan cross-encoder BERT 88,77) dan rerata **87,69%** pada 7 tugas transfer learning SentEval.
  * *Ablation Study:* Membuktikan bahwa komponen selisih absolut elemen **$\vert{}u-v\vert{}$** adalah fitur paling vital dalam pelatihan klasifikasi siam.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menjawab masalah krusial efisiensi komputasi pencarian semantik dengan menjadi **rujukan kanonis dan fondasi teoretis murni** untuk seluruh arsitektur *Dense Retrieval / Bi-Encoder Vector Embeddings*.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Kompresi seluruh isi teks ke dalam satu vektor berdimensi tetap (*fixed-size vector*) dapat menyebabkan hilangnya informasi kata kunci terisolasi (seperti nomor pasal atau istilah entitas spesifik). Untuk tugas inferensi kompleks yang membutuhkan perbandingan kata-demi-kata mendalam, akurasi *bi-encoder* sedikit di bawah *cross-encoder* BERT murni.

* **Relevansi di Bab II (Sub-bab 2.2.4):** Dikutip pada **Sub-bab 2.2.4 (Bi-Encoder, Sentence Embeddings, dan Dense Retrieval)**. Prinsip Bi-Encoder SBERT ini melandasi fungsi *Dense Retriever* ChromaDB + `gemini-embedding-001` (Arm Config B) pada skripsi Anda.

#### 16. Bhat et al. (2025)

* **Sitasi Lengkap:** Bhat et al. (2025) — *"Rethinking Chunk Size for Long-Document Retrieval: A Multi-Dataset Analysis"* (arXiv preprint arXiv:2505.21700v2 [cs.IR], Published May 2025 / June 10, 2025, Fraunhofer IAIS, Germany).

* **Objek:** Analisis empiris sistematis mengenai dampak ukuran *chunk* (*fixed-size token chunking*) dan interaksinya terhadap kinerja *retrieval* (Recall@k) lintas 6 dataset Question Answering (QA) dokumen panjang dan berbagai arsitektur model *embedding*.

* **Metode:**
1. *Fixed-Size Token Chunking:* Diuji tanpa overlap pada variasi ukuran: **64, 128, 256, 512, dan 1024 token** menggunakan LlamaIndex `TokenTextSplitter`.

2. *Dataset Dokumen Panjang:* NarrativeQA (~51,8k token/doc), Natural Questions / NQ (~6,9k token/doc), NewsQA* (~8,4k token/doc), COVID-QA* (~10k token/doc), TechQA* (~7,5k token/doc), SQuAD* (~8k token/doc). (Dataset bertanda * disintesis/dijahit (*stitched*) hingga mencapai panjang minimum 50.000 karakter).

3. *Embedding Models:* Komparasi dua model embedding dengan karakteristik berbeda: `stella_en_1.5B_v5` (Decoder-based, context window >130k token) vs `snowflake-arctic-embed-l-v2.0` (Encoder-based, context window 8192 token).

4. *Retrieval Metric:* Kalkulasi cosine similarity, diukur berdasarkan metrik Recall@1 hingga Recall@5.

* **Hasil Kunci:**
* *Trade-off Ukuran Chunk:*
* **Small Chunks (64–128 token):** Sangat optimal untuk dataset dengan jawaban ringkas dan terisolasi (SQuAD: Recall@1 tertinggi 64,1% pada 64 token; ukuran 512 token justru menurunkan recall sebesar 10–15% akibat *noise* konteks).

* **Large Chunks (512–1024 token):** Mutlak diperlukan untuk dokumen dengan jawaban berkonteks luas atau tersebar (*long & dispersed context*). Contoh: TechQA (Recall@1 melonjak dari 16,5% pada 128 token menjadi 61,3% pada 512 token); NarrativeQA (Recall@1 naik dari 4,2% pada 64 token ke 10,7% pada 1024 token); NQ (puncak Recall@1 pada 512 dan 1024 token).

* *Interaksi Sensitivitas Model Embedding:*
* Model *decoder-based* (`Stella`) menunjukkan kinerja lebih kuat pada ukuran chunk besar (512–1024 token) karena mampu memanfaatkan *global chunk context* dari arsitektur decoder-nya.

* Model *encoder-based* (`Snowflake`) lebih unggul pada chunk kecil (64–128 token) dalam menangkap hubungan entitas *fine-grained*, namun kinerjanya merosot pada chunk besar karena *objective pre-training*-nya memfavoritkan interaksi lokal token.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti empiris mutakhir (2025) mengenai dinamika *trade-off* ukuran chunking, membuktikan bahwa tidak ada satu ukuran chunk tunggal yang optimal untuk semua jenis dokumen.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi *ground truth retrieval* hanya mengandalkan pencocokan string eksplisit (*string match*) antara jawaban acuan dan dokumen, tanpa evaluasi relevansi semantik/Ragas. Pengujian terbatas pada pencarian *dense retrieval* tanpa membandingkannya dengan *sparse retrieval* (BM25).

* **Relevansi di Bab II (2.1.3 & 2.2.8):** Dikutip pada Sub-bab 2.1.3 (Implementasi RAG & Trade-off Chunking) dan dielaborasi secara mendalam pada Sub-bab **2.2.8 (Chunking & Segmentasi Teks)**. Temuan Bhat et al. (2025) melegitimasi penetapan ukuran chunk yang dikunci identik (misalnya 188 chunk pada korpus 9 dokumen regulasi UNSRAT) sebagai variabel kontrol ketat (*controlled variable*) saat membandingkan arm *Dense ChromaDB* vs arm *Sparse BM25*.

---

### Bagian 4: Paper #17 – #20 (Framework RAG, Generation & Advanced RAG)

#### 17. Lewis et al. (2020)

* **Sitasi Lengkap:** Lewis et al. (2020) — *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"* (Advances in Neural Information Processing Systems 33 / NeurIPS 2020, pp. 9459-9474).

* **Objek:** Tugas-tugas Pemrosesan Bahasa Alami padat pengetahuan (*knowledge-intensive NLP tasks*), mencakup *Open-Domain Question Answering* (Natural Questions / NQ, TriviaQA / TQA, WebQuestions / WQ, CuratedTrec / CT), *Abstractive QA* (MS-MARCO NLG), *Jeopardy Question Generation*, serta *Fact Verification* (FEVER).

* **Metode:** Memperkenalkan arsitektur umum *Retrieval-Augmented Generation* (RAG) yang menggabungkan memori parametrik (*parametric memory* berbasis pre-trained seq2seq BART-large 400M parameters) dan memori non-parametrik (*non-parametric memory* berupa *dense vector index* Wikipedia 21 juta *chunks* @100 kata). Indeks diakses menggunakan *neural retriever* pre-trained Bi-Encoder *Dense Passage Retriever* (DPR) berbasis Maximum Inner Product Search (MIPS) via FAISS. Mengusulkan dua varian arsitektur:

1. **RAG-Sequence Model:** Menggunakan dokumen laten $z$ yang sama untuk menggenerasi seluruh sekuens token target $y$:

$$p_{\text{RAG-Sequence}}(y\vert{}x) \approx \sum_{z \in \text{top-}k(p(\cdot\vert{}x))} p_\eta(z\vert{}x) \prod_{i}^N p_\theta(y_i\vert{}x, z, y_{1:i-1})$$

2. **RAG-Token Model:** Mengambil dokumen laten yang berbeda untuk setiap token target $y_i$ yang digenerasi:

$$p_{\text{RAG-Token}}(y\vert{}x) \approx \prod_{i}^N \sum_{z \in \text{top-}k(p(\cdot\vert{}x))} p_\eta(z\vert{}x) p_\theta(y_i\vert{}x, z, y_{1:i-1})$$

Pelatihan dilakukan secara *joint end-to-end fine-tuning* pada *query encoder* $BERT_q$ dan generator BART, sementara *document encoder* $BERT_d$ dan indeks dokumen dikunci (*fixed*).

* **Evaluasi:** Metrik Exact Match (EM) pada Open QA; BLEU-1 dan ROUGE-L pada MS-MARCO; Q-BLEU-1 serta *Human Evaluation* (dimensi *Factuality* dan *Specificity*) pada Jeopardy QGen; dan *Label Accuracy* pada FEVER (3-way & 2-way).

* **Hasil Kunci:**
* *Open-Domain QA:* RAG mencatatkan *state-of-the-art* pada NQ (EM 44,5% RAG-Seq / 44,1% RAG-Tok), TQA Wiki (68,0% RAG-Seq), WQ (45,5% RAG-Tok), dan CT (52,2% RAG-Seq), mengungguli model *closed-book* parametrik murni (T5-11B) maupun pendekatan *open-book* ekstraktif (REALM, DPR). RAG mampu menjawab kueri dengan benar sebesar 11,8% pada NQ meskipun jawaban tidak ada pada dokumen terambil.

* *Abstractive QA (MS-MARCO):* RAG-Seq meraih ROUGE-L 40,8 dan BLEU-1 44,2, mengungguli baseline BART murni (ROUGE-L 38,2 / BLEU-1 41,6).

* *Jeopardy QGen:* RAG-Tok meraih Q-BLEU-1 22,2 (vs BART 19,7). Evaluasi manusia membuktikan RAG jauh lebih faktual (42,7% RAG unggul vs 7,1% BART unggul) dan lebih spesifik (37,4% RAG unggul vs 16,8% BART unggul).

* *Index Hot-Swapping:* Mengganti indeks memori non-parametrik (Wikipedia dump Dec 2016 ke Dec 2018) terbukti langsung memperbarui pengetahuan dunia model tanpa memerlukan pelatihan ulang (*retraining*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Paper pionir (*seminal paper*) yang mendefinisikan paradigma RAG secara formal. Membuktikan bahwa sintesis *dense retriever* (DPR) dan *generative LLM* (BART) efektif menekan halusinasi serta meningkatkan faktualitas jawaban.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Proses inferensi membutuhkan komputasi indeks vektor yang besar. *Document index* dibekukan selama pelatihan sehingga pembaharuan vektor dokumen tidak terjadi secara *real-time* saat *backpropagation*.

* **Relevansi di Bab II & Sub-bab 2.2 (Dasar Teori):** Berfungsi sebagai **fondasi teoretis utama arsitektur RAG**. Harus dikutip di **Sub-bab 2.2 (Dasar Teori RAG)** dan **Sub-bab 2.1.3**.

---

#### 18. Lakatos et al. (2025)

* **Sitasi Lengkap:** Lakatos et al. (2025) — *"Investigating the Performance of Retrieval-Augmented Generation and Domain-Specific Fine-Tuning for the Development of AI-Driven Knowledge-Based Systems"* (Machine Learning and Knowledge Extraction / MDPI, Vol. 7, No. 1, 15, Feb 2025).

* **Objek:** Komparasi empiris sistematis antara *Retrieval-Augmented Generation* (RAG) versus *Domain-Specific Fine-Tuning* (DFT) pada pengembangan sistem berbasis pengetahuan teradaptasi domain (korpus spesifik: budidaya jagung/CORN, monitoring perkotaan/UB, CORD-19, dan MedQuAD).

* **Metode:**
1. *Model LLM yang Diuji:* GPT-J-6B, OPT-6.7B, LLaMA-7B, dan LLaMA-2-7B.

2. *Domain-Specific Fine-Tuning (DFT):* Fine-tuning instruksi Q&A (dibatasi $\le 256$ token) menggunakan *categorical cross-entropy loss*, *batch size* 4, *learning rate* $2 \times 10^{-4}$, selama 5 epoch.

3. *Retrieval-Augmented Generation (RAG):* LLaMA-2-7B base model + pengindeksan *cosine similarity threshold* berbasis Sentence Transformer `MiniLM-L6-v2`. Menguji dua tipe indeks: $ID_q$ (vektor berbasis paragraf/pertanyaan) dan $ID_s$ (vektor berbasis kalimat/sentences).

4. *Coverage Score (CS):* Mengusulkan formula metrik baru berbasis *cosine similarity* rerata tingkat kalimat:

$$\text{CS} = \sum_{i=1}^M \frac{\max_k (\text{Cosine}(rs_{i,j}, gs_{i,k}))}{M}$$

* **Evaluasi:** Evaluasi kuantitatif menggunakan ROUGE, BLEU, METEOR, dan Coverage Score (CS) pada dataset uji terisolasi yang dibentuk via reduksi dimensi UMAP dan pemutusterusan klaster HDBSCAN.

* **Hasil Kunci:**
* Sistem RAG secara konsisten mengungguli DFT pada hampir seluruh metrik utama:

* **ROUGE:** RAG mencatatkan rerata **0,2896** vs DFT **0,2473** (+17%).

* **BLEU:** RAG mencatatkan rerata **0,0680** vs DFT **0,0600** (+13%).

* **Coverage Score (CS):** RAG mencatatkan rerata **0,5516** vs DFT **0,4046** (+36%).
*(Baseline LLaMA-2-7B murni tanpa RAG/DFT: ROUGE 0,1351; BLEU 0,0029; CS 0,3622)*.

* DFT hanya unggul tipis pada METEOR (0,2606 vs RAG 0,2456), menunjukkan variasi kata/kreativitas yang sedikit lebih tinggi.

* **Anomali / Temuan Kritis:** Menggabungkan RAG pada model yang sudah di-fine-tune (**RAG with DFT**) justru mengalami **penurunan kinerja yang tajam** (ROUGE 0,2299; BLEU 0,0436; CS 0,3667). Threshold RAG optimal pada model base adalah 0,5, sedangkan pada model DFT bernilai 1,0 (rejection rate 100%). Penulis menyimpulkan bahwa fine-tuning domain merusak/mereduksi kemampuan alami LLM dalam menginterpretasikan konteks RAG.

* Konfigurasi terbaik: LLaMA-2-7B base + RAG indeks tingkat kalimat ($ID_s$) menghasilkan ROUGE 0,30; METEOR 0,25; BLEU 0,07; dan CS 0,55.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti empiris yang sangat kuat bahwa RAG berbasis *in-context learning* jauh lebih superior dalam menekan halusinasi dan menjaga cakupan semantik dibandingkan *fine-tuning* standalone (DFT), serta memberikan peringatan bahaya mengombinasikan RAG dengan model yang di-fine-tune.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Pengujian dibatasi pada teks pendek (256 token limit per jawaban) dan evaluasi RAG tidak menggunakan kerangka evaluasi RAG modern yang terisolasi seperti Ragas.

* **Relevansi di Bab II (2.1.2 & 2.1.5):** Dikutip pada Sub-bab 2.1.2 dan Sub-bab 2.1.5 (Research Gap). Berpasangan dengan Priccilia & Girsang (2024) untuk mempertegas argumentasi bahwa *fine-tuning* standalone terbukti gagal/overfit pada domain akademik/spesifik sempit, sehingga arsitektur RAG terkontrol menjadi pilihan terbaik.

---

#### 19. Khasanova Zafar kizi & Suh (2025)

* **Sitasi Lengkap:** Khasanova Zafar kizi & Suh (2025) — *"Design and Performance Evaluation of LLM-Based RAG Pipelines for Chatbot Services in International Student Admissions"* (Electronics / MDPI, Vol. 14, No. 15, 3095, August 2025).

* **Objek:** Chatbot RAG layanan informasi pendaftaran mahasiswa internasional di Kongju National University (KNU), Korea Selatan.

* **Metode:**
1. *Korpus & Dual Reference Dataset:* PDF panduan admisi (29 hal) + 38 FAQ web (FAQ1) + 11 FAQ kantor Urusan Internasional (FAQ2). Dievaluasi menggunakan **dua dataset acuan**: *LLM-generated QA* (72 pasang) dan *Human-tagged QA* (62 pasang buatan mahasiswa nyata/penerima beasiswa GKS).

2. *Chunking & Embedding:* Recursive Character Text Splitter vs Semantic Chunker. Embedded via `all-MiniLM-L6-v2` (384-dim) disimpan pada FAISS vector store ($top\text{-}k=5$).

3. *Retriever:* MMR, Dense Retriever, Hybrid (BM25 + Dense), MultiQuery Retriever (Dense / Hybrid), dan MultiVector Retriever.

4. *LLM Generator:* Commercial Cloud (OpenAI GPT-4o) vs Local Open-Source via Ollama (LLaMA3 8B, OpenChat-7B v3.5, Zephyr-7B, Neural-Chat-7B).

* **Evaluasi:**
1. Kerangka evaluasi **RAGAS** (*Answer Relevancy, Faithfulness, Context Recall, Context Precision*) + Metrik NLP Heuristik (ROUGE, BLEU, METEOR, SemScore/BERTScore).

2. Analisis latensi *end-to-end* ($detik$) per tahapan (*embedding, retrieval, generation*).

* **Hasil Kunci:**
* *Hasil Pipeline Baseline (Algo 1–12):* GPT-4o + Semantic Chunking + Dense Retriever (Algo-5) meraih skor RAGAS tertinggi pada LLM-generated QA (rerata RAGAS 0,7351; Answer Relevancy 0,8013, Faithfulness 0,8646, Context Recall 0,7153, Context Precision 0,5593) dan Human-tagged QA (rerata RAGAS 0,7249; Answer Relevancy 0,7606, Faithfulness 0,8538, Context Recall 0,6306, Context Precision 0,6549).

* *Optimalisasi Open-Source Model (Algo 13–23):* Penggabungan model *open-source* lokal `OpenChat-7b-v3.5-0106-fp16` + Recursive Chunking + **MultiQuery Hybrid Retriever (Dense + BM25)** (Algo-23) sukses **mengungguli GPT-4o** dengan rerata RAGAS **0,7377** pada Human-tagged QA dan **0,7408** pada LLM-generated QA.

* *Trade-off Latensi Mendasar:* Konfigurasi OpenChat teroptimasi (14GB fp16 + MultiQuery Hybrid) mengalami lonjakan latensi yang sangat drastis (**17,39 detik total**: retrieval 6,13s, generation 11,25s pada Human-tagged QA) dibanding LLaMA3 baseline (1,26s–1,76s total) atau GPT-4o API (2,37s–2,70s total).

* *Analisis Dual Dataset:* Dataset LLM-generated QA mencatatkan skor kuantitatif lebih tinggi karena struktur pertanyaan selaras dengan dokumen, sementara Human-tagged QA mencerminkan variasi bahasa alami nyata yang membutuhkan penalaran lebih luas.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan bukti empiris bahwa RAG pipeline berbasis *open-source model* lokal (OpenChat) dengan MultiQuery Hybrid Retrieval sanggup menyamai/mengungguli commercial LLM (GPT-4o) pada layanan pendaftaran perguruan tinggi. Memberikan wawasan komprehensif mengenai *trade-off* akurasi vs latensi serta perbedaan evaluasi *LLM-generated vs Human-tagged QA*.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Latensi OpenChat teroptimasi sangat lambat (>17 detik), kurang ideal untuk percakapan *real-time* tanpa teknik akuantisasi. Ukuran dataset manusia tergolong terbatas (62 QA pairs).

* **Relevansi di Bab II (2.1.2, 2.1.4, & 2.1.5):** Dikutip di Sub-bab 2.1.2 (Adopsi RAG Layanan Akademik Kampus), Sub-bab 2.1.4 (Evaluasi Ragas & Latensi), dan Sub-bab 2.1.5 (Research Gap).

---

#### 20. Koay et al. (2026)

* **Sitasi Lengkap:** Koay et al. (2026) — *"Structure-Aware Chunking for Complex Tables in Retrieval-Augmented Generation Systems"* (Emerging Science Journal, Vol. 10, No. 1, February 2026, pp. 184-205).

* **Objek:** Kerangka kerja *Structure-Aware Chunking* kustom untuk menangani dokumen struktur kurikulum/matakuliah perguruan tinggi yang kaya akan tabel kompleks (multi-kolom, multi-baris, *merged cells*, dan *nested headers*) dalam sistem RAG.

* **Metode:**
1. *Parsing:* Menggunakan **Camelot** (Lattice Mode) dengan opsi `copy_text=True` untuk mengekstraksi grid tabel secara presisi dan meneruskan teks header tergabung (*merged headers*) secara otomatis.

2. *Customized Structure-Aware Chunking Workflow:* (1) *Term Identification & Extraction* (ekstraksi header semester/term); (2) *Subject-to-Term Mapping* (pemetaan matakuliah ke term); (3) *Category Carry-Forward Logic & Credit Hour Validation* (penelusuran kategori berjenjang & validasi SKS/credit hour); (4) *Structured Triple Construction* (pembentukan unit triple terstruktur: `(Subject, Credit Hour, Category)` yang dikelompokkan per term akademik).

3. *Embedding & RAG Pipeline:* Embedding `BAAI/bge-m3` (generation) & `text-embedding-3-small` (evaluation), ChromaDB vector store, generator LLaMA-3 70B (Meta AI), evaluator GPT-3.5 Turbo.

4. *Baseline Komparasi:* Baseline 1 (PyPDFLoader + Recursive Chunking), Baseline 2 (LlamaParse markdown mode + Recursive Chunking), Baseline 3 (Camelot + Recursive Chunking), dan Proposed Method (Camelot + Structure-Aware Chunking).

* **Evaluasi:** Menggunakan kerangka kerja RAGAS pada 50 kueri akademis buatan pakar + *ground truth*: Faithfulness, Answer Relevancy, Content Precision, Content Recall, Content Relevance, dan Answer Accuracy (dinilai oleh 2 hakim LLM).

* **Hasil Kunci:**
* Metode *Structure-Aware Chunking* yang diusulkan mengungguli seluruh baseline pada hampir semua metrik:

* **Answer Accuracy:** **0,73** (vs Baseline 1: 0,32, Baseline 2: 0,43, Baseline 3: 0,39).

* **Content Precision:** **0,92** (vs Baseline 1: 0,57, Baseline 2: 0,62, Baseline 3: 0,29).

* **Content Relevance:** **0,93** (vs Baseline 1: 0,77, Baseline 2: 0,83, Baseline 3: 0,65).

* **Answer Relevancy:** **0,81** (vs Baseline 1: 0,72, Baseline 2: 0,77, Baseline 3: 0,65).

* **Content Recall:** **0,82** (sama dengan Baseline 1: 0,82).

* Faithfulness diusulkan meraih 0,78 (sedikit di bawah Baseline 2 LlamaParse: 0,81), namun LlamaParse terbukti mengalami kegagalan struktural fatal (gagal menjawab kueri seperti matakuliah di Term D karena meratakan/flattening header tabel).

* Menunjukkan bahwa perbaikan pada parser saja (Baseline 3 Camelot + Recursive) tanpa strategi chunking terstruktur menghasilkan performa paling buruk (Answer Accuracy 0,39; Content Precision 0,29) karena pemotongan token kaku merusak asosiasi antar-baris/kolom.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Membuktikan secara empiris bahwa parsing berkualitas tinggi harus dipadukan dengan strategi *chunking* berbasis struktur (*structure-aware chunking*) untuk mempertahankan asosiasi entitas pada tabel kompleks dokumen akademik kampus.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Logika chunking sangat disesuaikan (*customized*) dengan format tabel kurikulum spesifik, sehingga membutuhkan rekonfigurasi aturan jika diterapkan pada tata letak tabel yang sangat berbeda atau teks naratif tidak terstruktur.

* **Relevansi di Bab II (2.1.3 & 2.1.4):** Dikutip di Sub-bab 2.1.3 (Implementasi Arsitektur RAG & Chunking pada Tabel/Dokumen Kompleks) dan Sub-bab 2.1.4 (Evaluasi Ragas).

---

### Bagian 5: Paper #21 – #26 (Studi Kasus RAG & Metric Evaluasi RAGAS)

#### 21. Salman et al. (2026)

* **Sitasi Lengkap:** Salman et al. (2026) — *"Implementation of Retrieval-Augmented Generation Method on Large Language Model for Development of Campus Service and Information Chatbot"* (INOVTEK Polbeng - Seri Informatika, Vol. 11, Issue 1, February 2026, pp. 298-309).

* **Objek:** Chatbot layanan dan informasi kampus di Universitas Sains dan Teknologi Indonesia (USTI), Pekanbaru.

* **Metode:**
1. *Knowledge Base & Indexing:* Pengolahan 29 dokumen publik resmi USTI (profil, akademis, fasilitas) yang dipotong menggunakan teknik *adaptive chunking*.

2. *Hybrid Retrieval:* Menggabungkan *dense retrieval* berbasis embedding `intfloat/multilingual-e5-base` (vektor FAISS) dan *sparse retrieval* berbasis `BM25` (pencarian leksikal JSONL). Hasil kedua metode digabungkan menggunakan *Reciprocal Rank Fusion* (RRF dengan konstanta $k=15$).

3. *Cross-Encoder Reranking:* 10 kandidat teratas dari RRF diacak ulang urutannya (*reranked*) menggunakan model `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` untuk memilih 3 *chunk* terbaik sebagai konteks.

4. *Generative LLM:* Menggunakan model LLaMA 3.1 8B Instant yang diakses via API inferensi Groq dengan antarmuka Streamlit UI.

* **Evaluasi:** Evaluasi dilakukan menggunakan 13 kueri uji. Metrik retrieval mencakup Precision@3, Recall@3, F1-Score@3, dan NDCG@3. Metrik generasi mencakup BERTScore (Precision, Recall, F1) dan *Faithfulness* (menggunakan framework RAGAS).

* **Hasil Kunci:**
* *Hasil Retrieval:* Konfigurasi *Hybrid + RRF + Rerank* menghasilkan kinerja pencarian terbaik dibanding metode tunggal, dengan Precision@3 sebesar **71,7%**, Recall@3 sebesar **87,5%**, F1-Score@3 sebesar **78,8%**, dan NDCG@3 sebesar **96,3%**. (Sebagai pembanding: FAISS murni meraih Precision@3 64,1% & NDCG 88,2%; BM25 murni meraih Precision@3 69,2% & NDCG 94,5%).

* *Hasil Generasi:* Integrasi RAG terbukti meningkatkan kualitas respons dibanding LLM tanpa retrieval (*LLM-only*), di mana BERTScore-F1 naik dari 84,8% menjadi **89,4%** dan nilai *Faithfulness* mencapai **88,8%**.

* *Temuan Anomali:* Pada pengujian *Faithfulness*, FAISS murni justru mencatatkan skor lebih tinggi (**93,6%**) dibanding Hybrid RAG (**88,8%**), sebuah temuan yang menunjukkan adanya *trade-off* antara kelengkapan pencarian leksikal dan konsistensi faktual generasi.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menjadi preseden penelitian RAG kampus berbasis *hybrid retrieval* (e5-base + BM25 + Cross-Encoder) yang paling dekat lokasinya di Indonesia.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi komponen *retriever* hanya mengandalkan metrik IR klasik (Precision, Recall, NDCG) tanpa mengukur *Context Precision* dan *Context Recall* dari Ragas secara terpisah. Skala pengujian sangat terbatas (13 kueri uji) dan penetapan *ground truth* hanya dilakukan oleh *single annotator* (penulis sendiri).

* **Relevansi di Bab II (2.1.2 & 2.1.5):** Dikutip di Sub-bab 2.1.2 dan dielaborasi pada Sub-bab **2.1.5 (Research Gap)**. Skripsi Anda menyempurnakan Salman et al. dengan mengevaluasi komparasi *dense vs sparse* terkontrol menggunakan kerangka 4-metrik Ragas penuh serta analisis pola kegagalan kualitatif.

---

#### 22. Husain et al. (2025)

* **Sitasi Lengkap:** Husain et al. (2025) — *"Development of an Academic Services Chatbot Based on Retrieval-Augmented Generation (RAG)"* (Brilliance: Research of Artificial Intelligence, Vol. 5, No. 2, November 2025, pp. 727-735).

* **Objek:** Chatbot layanan administrasi akademik Fakultas Pendidikan Matematika dan Ilmu Pengetahuan Alam (FPMIPA) Universitas Pendidikan Indonesia (UPI).

* **Metode:**
1. *Knowledge Base:* Dokumen resmi FPMIPA UPI diproses menggunakan pustaka `docling` (*HybridChunker*) dengan enkapsulasi metadata hierarkis (*parent_id*, *child_ids*, *next_id*) dan di-embed menggunakan `gemini-embedding-001` ke dalam *vector store* Qdrant.

2. *Multi-Stage RAG Pipeline:* (a) *Query Contextualization* (mengubah kueri ambigu menjadi pertanyaan *standalone*); (b) *Query Decomposition* (memecah kueri menjadi sub-pertanyaan via LLM); (c) *Dense Retrieval* (mengambil top-15 *chunks* dari Qdrant); (d) *Context Expansion* (menarik *parent/adjacent nodes* dan dokumen sejudul); (e) *Reranking* via `FlashrankRerank` (`ms-marco-MiniLM-L-12-v2`) untuk mengambil top-5 *chunks*; (f) Generasi jawaban menggunakan **Gemini 2.5 Pro** via LangChain dan Streamlit UI.

* **Evaluasi:** Menggunakan 100 kueri uji yang dibagi menjadi 3 kategori (60 *factual*, 20 *reasoning*, dan 20 *out-of-context*) yang dievaluasi menggunakan framework RAGAS (Faithfulness, Answer Relevancy, Context Recall, Semantic Similarity, Factual Correctness).

* **Hasil Kunci:**
* *Pertanyaan Faktual (60 kueri):* Meraih kinerja sangat tinggi dengan *Faithfulness* **0,9100**, *Context Recall* **0,8519**, *Semantic Similarity* **0,7682**, dan *Answer Relevancy* **0,6862**.

* *Pertanyaan Penalaran / Reasoning (20 kueri):* Kinerja *retrieval* merosot tajam di mana *Context Recall* turun menjadi **0,5926** dan *Answer Relevancy* turun menjadi **0,4182**, meskipun nilai *Faithfulness* tetap tinggi (**0,9048**).

* *Pertanyaan Luar Konteks / Out-of-Context (20 kueri):* Sistem sukses menolak menjawab (*graceful refusal*) pada **81,25%** kasus (*Factual Correctness Precision* 0,8125; F1-Score 0,6875), yang secara efektif mencegah terjadinya halusinasi.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan preseden metodologis RAG multi-tahap yang sangat matang di Indonesia, lengkap dengan pengujian kueri penalaran (*reasoning*) dan mekanisme penolakan halusinasi (*out-of-context refusal*).

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Pipeline hanya berjalan pada satu jalur pencarian (*dense-only retrieval* + reranker) tanpa menyediakan lengan pembanding leksikal (*sparse BM25*).

* **Relevansi di Bab II (2.1.2, 2.1.4, & 2.1.5):** Dikutip pada Sub-bab 2.1.2, 2.1.4, dan 2.1.5. Angka *Faithfulness* dan *refusal rate* Husain et al. menjadi pembanding presisi untuk analisis evaluasi Ragas pada skripsi Anda.

---

#### 23. Mori et al. (2025)

* **Sitasi Lengkap:** Mori et al. (2025) — *"Assessing the Performance Gap Between Lexical and Semantic Models for Information Retrieval With Formulaic Legal Language"* (Proceedings of the International Conference on Artificial Intelligence and Law / ICAIL '25, ACM, pp. 1-16).

* **Objek:** *Legal passage/paragraph retrieval* pada dokumen putusan Court of Justice of the European Union (CJEU) yang memiliki bahasa hukum sangat terstruktur, formulaik, dan berulang.

* **Metode:** Membandingkan *lexical models* (BM25, TF-IDF 1-gram & 2-gram) melawan *zero-shot dense models* (SBERT, SimCSE, Nomic, OpenAI Ada-v2, Emb-3-large) dan *fine-tuned dense models* (SBERT-ft, LegalSBERT-ft) pada korpus 83.503 paragraf dan 102.507 sitasi.

* **Evaluasi:** Evaluasi kuantitatif menggunakan Recall@K ($k=1,5,10,20$), nDCG@10, MAP, dan MRR. Dilengkapi analisis statistik korelasi kesamaan kueri-dokumen menggunakan *word-level mean edit distance*, *N-grams overlap*, dan *Longest Common Subsequence* (LCS).

* **Hasil Kunci:**
* **BM25 sebagai Baseline Sangat Kuat:** BM25 mengungguli seluruh model *zero-shot dense* (SBERT, SimCSE, Nomic, Emb-3-large) pada Recall@5,10,20 dan nDCG@10. BM25 hanya dilampaui oleh model *proprietary* Ada-v2 pada R@1, MAP, dan MRR.

* *Keunggulan Fine-Tuning:* Model *fine-tuned dense* (LegalSBERT-ft 110M) meraih kinerja terbaik secara keseluruhan (R@1 0,4202; R@5 0,6859; MAP 0,5814; MRR 0,6486).

* *Analisis Karakteristik Dokumen:* BM25 terbukti mengungguli model *dense* secara signifikan pada kueri yang lebih panjang ($>102$ kata) serta pada skenario di mana pengulangan kata kunci eksplisit (*verbatim quotes*) kurang dominan atau berupa parafase halus. Sebaliknya, model *dense zero-shot* sering mengalami distraksi (*noise*) dari konteks tambahan di luar kalimat kutipan.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti teoretis dan empiris yang sangat kuat bahwa BM25 (*sparse retrieval*) sangat kompetitif dan bahkan melampaui *dense embedding* pada korpus dokumen hukum/regulasi yang formulaik.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Penelitian ini murni merupakan studi *Information Retrieval* (IR) paragraf tanpa melibatkan komponen generator LLM maupun arsitektur RAG.

* **Relevansi di Bab II (2.1.5 & Sub-bab 2.2):** Dikutip pada Sub-bab 2.1.5 (Research Gap) dan menjadi rujukan pendukung di Sub-bab **2.2 (Dasar Teori Sparse Retrieval / BM25)**. Berpasangan dengan Pusparini et al. (2025) untuk melegitimasi Hipotesis RQ2 skripsi Anda mengenai daya saing BM25 pada dokumen regulasi kampus.

---

#### 24. Artayasa et al. (2025)

* **Sitasi Lengkap:** Artayasa et al. (2025) — *"Enhancing Academic Chatbot Accuracy With Retrieval-Augmented Generation in Higher Education"* (2025 IEEE International Symposium on Consumer Technology / ISCT 2025, IEEE, pp. 427-432).

* **Objek:** Chatbot layanan informasi akademik mahasiswa (jadwal kuliah, biaya, kriteria, visi-misi) di Institut Bisnis dan Teknologi Indonesia (INSTIKI), Bali.

* **Metode:** Pipeline RAG berbasis LangChain, OpenAIEmbeddings (`text-embedding-ada-002`), *vector store* FAISS, dan generator OpenAI GPT-4. Preprocessing menggunakan `RecursiveCharacterTextSplitter` (chunk size 1000 token, overlap 200 token) pada korpus 180 entri teks akademis.

* **Evaluasi:** Evaluasi otomatis pada 50 kueri uji (45 *in-context*, 5 *out-of-context*) menggunakan dua kerangka metrik: (1) **RAGAS** (Faithfulness, Answer Relevancy, Context Precision, Context Recall); dan (2) **Evaluasi Berbasis MRR** (MRR, Semantic Similarity, Answer Relevancy, Faithfulness).

* **Hasil Kunci:**
* *Hasil RAGAS:* Meraih rerata skor RAGAS sebesar **84,21%** ( Faithfulness 0,7293; Answer Relevancy 0,8869; Context Precision 0,8444; Context Recall 0,9078).

* *Hasil Evaluasi MRR:* Meraih rerata skor sebesar **82,19%** (MRR 0,9000; Semantic Similarity 0,8928; Answer Relevancy 0,8167; Faithfulness 0,6783).

* Sistem terbukti konsisten menghasilkan jawaban dan perhitungan biaya kuliah yang akurat meskipun kalimat pertanyaan divariasikan secara anonim.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti kepraktisan penerapan RAGAS dan MRR untuk mengaudit kinerja chatbot RAG kampus di Indonesia.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Evaluasi hanya menguji satu konfigurasi *dense-only* (FAISS + OpenAI) tanpa membandingkannya dengan *sparse retrieval* (BM25) atau model *open-source*, serta bergantung penuh pada API *proprietary*.

* **Relevansi di Bab II (2.1.2 & 2.1.4):** Dikutip pada Sub-bab 2.1.2 dan Sub-bab 2.1.4 (Evaluasi Kinerja Chatbot Akademik).

---

#### 25. Es et al. (2024)

* **Sitasi Lengkap:** Es et al. (2024) — *"RAGAS: Automated Evaluation of Retrieval Augmented Generation"* (Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations / EACL 2024, pp. 150-158).

* **Objek:** Kerangka kerja *reference-free automated evaluation* (RAGAS) untuk mengevaluasi pipeline RAG tanpa bergantung pada *ground truth human annotations*.

* **Metode:** Memformulasi 3 metrik evaluasi utama berbasis LLM (`gpt-3.5-turbo-16k`):
1. **Faithfulness:** Memecah jawaban $a_s(q)$ menjadi klaim-klaim atomik $S(a_s(q))$, lalu memverifikasi proporsi klaim yang dapat diinferensikan dari konteks $c(q)$:

$$F = \frac{\vert{}V\vert{}}{\vert{}S\vert{}}$$

2. **Answer Relevance:** Menggenerasi $n$ pertanyaan buatan dari jawaban $a_s(q)$, lalu mengukur rerata *cosine similarity* embedding-nya (`text-embedding-ada-002`) terhadap kueri asli $q$:

$$AR = \frac{1}{n} \sum_{i=1}^n \cos(E_{gi}, E_o)$$

3. **Context Relevance:** Mengukur proporsi kalimat krusial yang diekstrak dari $c(q)$ dibanding total kalimat konteks.
Sistem mewajibkan output LLM berformat JSON terstruktur untuk menjamin reproduksibilitas.

* **Evaluasi:** Membangun dataset **WikiEval** (50 halaman Wikipedia peristiwa terkini >2022) untuk mengukur tingkat keselarasan (*accuracy agreement*) prediksi RAGAS terhadap penilaian juri manusia (*human annotators*) dibanding dua baseline: *GPT Score* dan *GPT Ranking*.

* **Hasil Kunci:** Metrik RAGAS mencapai tingkat keselarasan (*accuracy agreement*) tertinggi terhadap juri manusia: *Faithfulness* **0,95** (vs GPT Score 0,72 / Ranking 0,54); *Answer Relevance* **0,78** (vs 0,52 / 0,40); dan *Context Relevance* **0,70** (vs 0,63 / 0,52). Penggunaan format output JSON terbukti secara signifikan meningkatkan stabilitas skor antar-run.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Paper pionir (*seminal paper*) yang menjadi **fondasi teoretis dan metodologis utama** untuk kerangka evaluasi RAGAS yang Anda gunakan dalam skripsi.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Sangat bergantung pada kapabilitas model evaluator (seperti GPT-3.5/GPT-4), sehingga perubahan pada API penyedia model dapat mempengaruhi konsistensi skor.

* **Relevansi di Bab II & Sub-bab 2.2 (Dasar Teori):** Dikutip di Sub-bab **2.2 (Dasar Teori Framework RAGAS)** dan Sub-bab 2.1.4.

---

#### 26. Abdurrazzaq et al. (2025)

* **Sitasi Lengkap:** Abdurrazzaq et al. (2025) — *"An Indonesian Chatbot for Disease Diagnosis Using Retrieval-Augmented Generation"* (Jurnal INOVTEK Polbeng - Seri Informatika, Vol. 10, No. 3, November 2025, pp. 1877-1887).

* **Objek:** Chatbot medis Bahasa Indonesia untuk penelusuran diagnosis penyakit berbasis model *open-source* GPT-OSS-20B dan RAG.

* **Metode:**
1. *Domain Filter:* Filter awal berbasis Logistic Regression (TF-IDF 1-2 gram) untuk menyaring kueri non-medis sebelum diproses LLM.

2. *Retrieval & Reranking:* Pemetaan semantik `jina-embeddings-v3` (1024-dim) + FAISS L2 distance untuk mengambil 100 kandidat awal, diacak ulang (*reranked*) menggunakan gabungan *Hybrid* (FAISS L2 + BM25).

3. *Generative LLM:* Model *open-source* GPT-OSS-20B dengan instruksi sistem terstruktur via *function calling* `medical_assistant`. Data: 1.366 artikel medis (scraping) + 135.276 percakapan dokter-pasien.

* **Evaluasi:** Evaluasi *Domain Filter* (Precision, Recall, F1, Accuracy); Evaluasi *Retrieval* (Top-K Accuracy $K=1,5,10,20,30$); dan pengujian alur antarmuka via *Black-box testing*.

* **Hasil Kunci:**
* *Domain Filter:* Meraih skor 1,0 pada data sintetis, namun mengalami misklasifikasi pada kueri bahasa alami (gagal menyaring kalimat sosial seperti *"Halo, apa kabar?"*).

* *Retrieval:* Reranker *Hybrid* (FAISS L2 + BM25) memberikan kinerja paling stabil pada Top-30 Accuracy sebesar **0,699** (vs FAISS L2 0,695 dan BM25 murni 0,596). Namun, akurasi Top-1 masih rendah (L2 0,246 vs Hybrid 0,239) akibat kueri pasien yang ambigu.

* *Black-box Testing:* Seluruh skenario fungsionalitas sistem terbukti "Berhasil" secara teknis, namun respons belum divalidasi oleh pakar klinis.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan preseden aplikasi RAG *open-source* Bahasa Indonesia yang mengombinasikan *domain filter* dan *hybrid reranking*.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Ketahanan *domain filter* terbukti lemah pada kueri alami dan tidak ada evaluasi terstandardisasi menggunakan Ragas maupun validasi klinis.

* **Relevansi di Bab II (2.1.2 & 2.1.3):** Dikutip pada Sub-bab 2.1.2 dan Sub-bab 2.1.3.

---

### Bagian 6: Paper #27 – #32 (Analisis Domain Akademik & Agentic Conversational AI)

#### 27. Pusparini et al. (2025)

* **Sitasi Lengkap:** Pusparini et al. (2025) — *"Evaluating Information Retrieval Models for Indonesia's Government Legal Documents"* (Proceedings of the 2025 5th International Conference of Science and Information Technology in Smart Administration / ICSINTESA 2025, IEEE, pp. 246-251).

* **Objek:** Dokumen peraturan dan regulasi internal Badan Riset dan Inovasi Nasional (BRIN), Indonesia (terdiri dari 75 dokumen PDF dengan ketebalan 3 hingga 172 halaman).

* **Metode:**
1. *Text Preprocessing:* Pembersihan teks Bahasa Indonesia mencakup tokenisasi, normalisasi (*lowercasing* & pembuangan tanda baca), serta pembuangan kata henti (*stopword removal*) menggunakan corpus Bahasa Indonesia pada pustaka NLTK.

2. *Komparasi 3 Metode Information Retrieval (IR) Klasik:*
* **Best Match 25 (BM25):** Algoritma probabilistik berbasis *term frequency* (TF) sub-linear dan normalisasi panjang dokumen (menggunakan kelas `BM25Okapi` dengan parameter standar $k_1 = 1,2$ dan $b = 0,75$).

* **Term Frequency-Inverse Document Frequency (TF-IDF):** Model pembobotan statistik gabungan frekuensi kata dalam dokumen dan kebalikan frekuensi dokumen dalam korpus.

* **Latent Semantic Indexing (LSI):** Teknik pemetaan semantik laten berbasis reduksi dimensi *Singular Value Decomposition* (SVD) pada matriks istilah-dokumen ($A \approx T \cdot S \cdot D^T$) dan pengukuran jarak *cosine similarity*.

3. *Ground Truth:* Pengujian menggunakan 50 kueri kata kunci *ground truth* yang terdiri dari 1 hingga 3 kata Bahasa Indonesia.

* **Evaluasi:** Mengukur kinerja sistem pencarian dokumen menggunakan metrik kuantitatif berbasis *confusion matrix*: **Average Precision**, **Average Recall**, **Average F1-Score**, dan **Mean Average Precision (MAP)**.

* **Hasil Kunci:**
* *Average Precision:* BM25 (**0,435**) dan TF-IDF (**0,435**) jauh mengungguli LSI (**0,112**).

* *Average Recall:* LSI mencatatkan *recall* tertinggi (**0,921**), namun dengan presisi yang sangat buruk (0,112) karena LSI mengambil terlalu banyak dokumen yang hanya berkaitan secara longgar. BM25 dan TF-IDF mencatatkan *recall* **0,898**.

* *Average F1-Score:* BM25 (**0,456**) dan TF-IDF (**0,456**) jauh lebih seimbang dan unggul dibanding LSI (**0,167**).

* *Mean Average Precision (MAP):* **BM25 meraih MAP tertinggi sebesar 0,449**, sedikit mengungguli TF-IDF (**0,448**) dan jauh melampaui LSI (**0,152**).

* Penulis menyimpulkan secara tegas bahwa teknik pencocokan istilah eksak (*exact term-matching*) seperti BM25 adalah metode terbaik dan paling konsisten untuk pencarian dokumen regulasi pemerintah Indonesia.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti empiris langsung pada korpus regulasi pemerintah Indonesia (BRIN) bahwa metode pencarian leksikal persis (*BM25 & TF-IDF*) sangat dominan dibandingkan metode semantik laten klasik (LSI).

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Ukuran dataset dan kueri sangat terbatas (hanya 75 dokumen dan 50 kueri pendek 1–3 kata). Murni merupakan studi *Information Retrieval* (IR) dokumen tanpa komponen generator LLM, arsitektur RAG, maupun pengujian terhadap model *dense neural embedding* modern (seperti SBERT, `gemini-embedding-001`, dll.).

* **Relevansi di Bab II (2.1.5 & Sub-bab 2.2):** Dikutip pada **Sub-bab 2.1.5 (Research Gap)** untuk melegitimasi argumen bahwa *sparse retrieval* (BM25) terbukti sangat kompetitif pada dokumen hukum/regulasi Indonesia. Berpasangan dengan Mori et al. (2025) di **Sub-bab 2.2 (Dasar Teori Sparse Retrieval / BM25)** sebagai landasan rujukan empiris spesifik konteks Indonesia.

---
Berikut adalah analisis dan ringkasan terstruktur dari 5 file paper asli yang Anda kirimkan. Analisis ini disusun secara presisi dengan orientasi utama untuk melengkapi **Sub-bab 2.2 (*Dasar Teori*)** pada Bab II skripsi Anda, melengkapi repositori file `sitasi-bab2.md`.

---

#### 28. Abu Shawar & Atwell (2007)

* **Sitasi Lengkap:** Abu Shawar, B., & Atwell, E. (2007) — *"Chatbots: Are they Really Useful?"* (LDV-Forum / Forum für Sprachtechnologie und Computerlinguistik, Vol. 22 No. 1, hlm. 29–49).

* **Objek:** Evaluasi manfaat praktis chatbot pada berbagai domain (pendidikan, *information retrieval*, e-commerce, hiburan) serta pengembangan teknik pelatihan ulang (*retraining*) otomatis berbasis korpus dialog (*dialogue corpora*).

* **Metode:**
1. *Arsitektur AIML (Artificial Intelligence Mark-up Language):* Membedah struktur markup berbasis XML yang terdiri dari elemen *topic* dan *category* (aturan pencocokan pasangan `<pattern>` dan `<template>`).

2. *Tipe Kategori AIML:* (a) *Atomic categories* (pencocokan string eksak tanpa wildcard); (b) *Default categories* (menggunakan wildcard `_` dan `*`); (c) *Recursive categories* (menggunakan tag `<srai>` dan `<sr>` untuk reduksi simbolik, pemecahan kalimat *divide-and-conquer*, dan penanganan sinonim).

3. *Algoritma Pencocokan Pola ALICE:* Berbasis pencocokan kata-demi-kata (*word-by-word*) untuk menemukan *longest pattern match* menggunakan struktur pohon *Graphmaster* (*nodemappers*) dengan teknik pencarian *Depth-First Search* (DFS).

4. *Otomatisasi Pelatihan AIML dari Korpus:* Pengusulan program Java 4-fase (Ekstraksi teks $\rightarrow$ Preprocessing/filtering filler $\rightarrow$ Konversi Turn-1=pattern & Turn-2=template $\rightarrow$ Generasi berkas AIML). Menggunakan strategi *First Word* dan *Most Significant Word* (berdasarkan frekuensi term terendah / *highest information content*).

5. *Aplikasi FAQchat:* Implementasi ALICE yang dilatih ulang dengan korpus FAQ *School of Computing* University of Leeds sebagai alternatif mesin pencari (Google) dalam tugas Information Retrieval (IR).

* **Evaluasi:** Pengujian tugas pencarian informasi (*information-seeking tasks*) pada 15 topik FAQ oleh 21 responden (staf dan mahasiswa) membandingkan luaran FAQchat melawan Google.

* **Hasil Kunci:**
* Sekitar dua pertiga pengguna (66%) berhasil menemukan jawaban yang dicari menggunakan FAQchat, dan mayoritas pengguna lebih memilih FAQchat dibandingkan Google.

* Keunggulan FAQchat terletak pada kemampuannya menyajikan jawaban langsung (*direct answers*) daripada sekadar daftar tautan web, serta menekan jumlah tautan yang harus dibaca pengguna.

* *Keterbatasan Utama AIML/ALICE:* Sistem tidak menyimpan riwayat percakapan (*stateless/lack of conversation history*), tidak memiliki pemahaman semantik (*pure keyword/pattern matching*), serta menghasilkan respon melingkar (*circular/nonsense*) saat kueri berada di luar aturan terdaftar.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan landasan teoretis historis yang sangat kuat mengenai mekanisme *Pattern Matching* dan arsitektur AIML pada generasi awal chatbot.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Pengondisian aturan manual (*hand-coded*) sangat tidak efisien dan tidak memiliki fleksibilitas semantik untuk memahami variasi sintaksis kueri alami.

* **Relevansi di Sub-bab 2.2 (Dasar Teori Evolusi Chatbots):** Dikutip pada **Sub-bab 2.2 (Dasar Teori Evolusi Chatbot & Rule-Based Systems)**. Berfungsi sebagai titik tolak teoretis untuk menjelaskan keterbatasan paradigma pencocokan kata kunci (*lexical pattern matching*) kaku tanpa memori konteks, sebelum terjadinya pergeseran menuju arsitektur *Vector Embedding* dan *Generative LLM*.

---

#### 29. Kulkarni et al. (2019)

* **Sitasi Lengkap:** Kulkarni, P., Sirsikar, N., Mahabaleshwarkar, A., Gadgil, K., & Kulkarni, M. (2019) — *"Conversational AI: An Overview of Methodologies, Applications & Future Scope"* (Proceedings of the 2019 5th International Conference on Computing Communication Control and Automation / ICCUBEA 2019, IEEE, hlm. 1–6).

* **Objek:** Tinjauan sistematis atas metrik, metodologi, dan arsitektur komponen utama *Conversational AI* tradisional hingga berbasis *Deep Learning* sebelum era Large Language Models.

* **Metode:**
1. *Natural Language Understanding (NLU):* Menguraikan dua tugas inti:

* **Named Entity Recognition (NER):** Evolusi dari RegEx $\rightarrow$ *Conditional Random Fields* (CRF) $\rightarrow$ CNN $\rightarrow$ BiLSTM-CNN-CRF dan *BiLSTM + Sigmoid Classifier* untuk ekstraksi entitas.

* **Intent Classification (IC):** Evolusi dari HMM/Decision Trees/SVM $\rightarrow$ *Hierarchical LSTM* (H-LSTM + Memory) $\rightarrow$ *Bidirectional LSTM* (BiLSTM).

2. *Dialogue Management (DM):* Mengatur aksi agen dan pelacakan status (*state tracking*: *Grounded, Slot Filling, Initiative, Context Switch*). Komparasi metode: *Switch Statements*, *Finite State Machines* (FSM), *Supervised ML*, *Deep Reinforcement Learning* (DRL dengan *reward/penalty*), dan POMDP (*Partially Observable Markov Decision Process*) / *Belief-based DM*.

3. *Natural Language Generation (NLG):* Mengonversi data terstruktur menjadi teks alami. Komparasi metode: *Template/Rule-based*, *N-Gram Generator*, SC-LSTM (*Semantically Conditioned LSTM*), *Seq2Seq*, dan *Seq2Seq + Reinforcement Learning* (Actor-Critic / Q-Learning).

* **Evaluasi:** Evaluasi performa komponen berbasis metrik F1-score (NER), Akurasi Klasifikasi (IC), *Conversation Success Rate* (DM), serta Skor BLEU dan ROUGE (NLG).

* **Hasil Kunci:**
* Model BiLSTM NLU mencapai F1-score 0,632 pada ekstraksi entitas-relasi ekosistem terbuka. Model BiLSTM Intent Classification meraih akurasi hingga **94,16%** dalam memetakan maksud pengguna.

* Agensi DM berbasis *Deep Reinforcement Learning* (DRL) berhasil melampaui pendekatan berbasis aturan heuristik dengan peningkatan *conversation success rate* **$>50\%$** dan melampaui *supervised agents* sebesar **$>30\%$**.

* Penggabungan *Seq2Seq + RL* (Actor-Critic) pada NLG menghasilkan skor ROUGE-1 (40,88), ROUGE-2 (17,80), dan ROUGE-L (38,54) yang secara signifikan lebih tinggi dibanding rerata metode konvensional.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan pemetaan arsitektur komprehensif mengenai pipeline *Conversational AI* klasik yang terbagi kaku menjadi tiga blok terpisah (NLU $\rightarrow$ DM $\rightarrow$ NLG).

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Pendekatan pipelining ini memiliki kelemahan *error propagation* (kesalahan pada blok NLU akan merusak keputusan DM dan output NLG).

* **Relevansi di Sub-bab 2.2 (Dasar Teori Arsitektur Conversational AI):** Dikutip pada **Sub-bab 2.2 (Dasar Teori Arsitektur Modular Conversational AI)**. Digunakan sebagai pembanding teoretis untuk mengontraskan arsitektur *pipeline modular* kaku (NLU-DM-NLG) dengan arsitektur **RAG (Retrieval-Augmented Generation)** modern yang menyatukan komponen *retrieval* dan *generation* secara lebih fleksibel.

---

#### 30. Dam et al. (2024)

* **Sitasi Lengkap:** Dam, S. K., Hong, C. S., Qiao, Y., & Zhang, C. (2024) — *"A Complete Survey on LLM-based AI Chatbots"* (arXiv preprint arXiv:2406.16937v1 [cs.CL], hlm. 1–23).

* **Objek:** Survei komprehensif mengenai fondasi teoretis, evolusi arsitektur Transformer, mekanisme *In-Context Learning*, *Chain-of-Thought*, taksonomi aplikasi multi-sistem (ChatGPT, BARD/Gemini, Bing Chat, Claude, Ernie Bot), serta analisis tantangan terbuka berbasis sudut pandang Data dan Pengetahuan.

* **Metode & Formulasi Matematika Kunci:**
1. *Taksonomi Arsitektur Transformer LLM:*
* **Encoder-Decoder (Vanilla Transformer):** Encoder memetakan sekuens input menjadi representasi abstrak via *multi-head self-attention*, sedangkan Decoder menggenerasi sekuens target secara autoregresif via *cross-attention*.

* **Causal Decoder (Autoregressive):** Menggunakan *one-way attention mask* yang membatasi setiap token hanya dapat memperhatikan token-token sebelumnya dan dirinya sendiri (diadopsi oleh seri GPT).

* **Prefix Decoder:** Mengaplikasikan perhatian dua arah (*bidirectional attention*) pada token awalan (*prefix*) dan perhatian searah (*unidirectional attention*) saat memprediksi token luaran.

2. *Formulasi Matematika Self-Attention Mechanism:*

$$Attention(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

di mana matriks $Q$ (Query), $K$ (Key), dan $V$ (Value) merepresentasikan proyeksi linear dari token input, dan skalar $\frac{1}{\sqrt{d_k}}$ berfungsi membedakan skala (*scaling factor*) untuk mencegah *vanishing gradient* pada fungsi Softmax.

3. *Kapabilitas Emergen LLM:*
* **In-Context Learning (ICL):** Kemampuan memahami dan mengeksekusi tugas berdasarkan instruksi/contoh pada draf input tanpa melakukan pembaruan bobot (*weight updates*).

* **Chain-of-Thought (CoT) Prompting:** Teknik pengarahan yang memprovokasi LLM untuk menguraikan tahapan penalaran intermediet (*intermediate reasoning steps*) secara sekuensial sebelum memproduksi jawaban final.

* **Evaluasi:** Evaluasi lintasan historis LLM (dari GPT-1, BERT, GPT-2, GPT-3, PaLM, LLaMA, GPT-4, PaLM 2, LLaMA 2) berdasarkan ukuran parameter, korpus pelatihan, dan panjang *context window*.

* **Hasil Kunci:**
* Membuktikan korelasi positif antara skala parameter (3B pada Flan-T5 hingga ~1760B pada Gemini Ultra) terhadap lonjakan skor penalaran murni (MMLU benchmark pada CoT prompting).

* Menyusun taksonomi tantangan terbuka LLM ke dalam 3 kategori utama:

1. *Tantangan Teknis:* **Knowledge Recency** (keterbatasan batas waktu data pelatihan), **Logical Reasoning** (penurunan kinerja tajam pada pertanyaan penalaran multi-tahap dibanding tunggal), dan **Hallucination** (halusinasi intrinsik & ekstrinsik).

2. *Tantangan Etika:* **Transparency** (*black-box models*), **Data Bias**, **Privacy Risks**, dan **Unfairness** (ketimpangan linguistik non-Inggris dan ekonomi).

3. *Tantangan Penyalahgunaan:* **Academic Misuse**, **Over-reliance**, dan **Distribution of Misinformation**.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan landasan teoretis dan formulasi matematis yang sangat mutakhir mengenai arsitektur Transformer, mekanisme *Self-Attention*, serta taksonomi limitasi LLM.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Berbentuk survei literatur tingkat tinggi tanpa pengujian eksperimental mandiri pada korpus dokumen spesifik.

* **Relevansi di Sub-bab 2.2 (Dasar Teori Large Language Models & Self-Attention):** Berfungsi sebagai **rujukan teoretis utama pada Sub-bab 2.2 (Dasar Teori Large Language Models, Arsitektur Transformer & Self-Attention)**. Formulasi matematis $Attention(Q,K,V)$ dan penjelasan arsitektur *Causal Decoder* dari paper ini menjadi landasan saat menjelaskan fungsi Google Gemini pada arsitektur skripsi Anda.

---

#### 31. Orrù et al. (2025)

* **Sitasi Lengkap:** Orrù, G., Melis, G., & Sartori, G. (2025) — *"Large language models and psychiatry"* (International Journal of Law and Psychiatry, Vol. 101, 102086, hlm. 1–8).

* **Objek:** Pemodelan komputasional pikiran (*computational modeling of the mind*), kapabilitas kognitif LLM (GPT-3.5, GPT-4, Chinchilla, Med-PaLM 2) dibandingkan pemrosesan kognitif manusia, fenomena *emergence*, serta kebangkitan kembali teori *Associationism*.

* **Metode:**
1. *Evaluasi Kognitif Metodologi Psikologi:* Memperlakukan LLM sebagai partisipan aktif dalam eksperimen psikologi kognitif untuk menguji *Theory of Mind*, penalaran analogi, pemahaman metafora/idiom, *common sense Q&A*, *Raven's Progressive Matrices* (kecerdasan cair / *fluid intelligence*), dan *Wason Selection Task*.

2. *Analisis Pola Kesalahan (Error Patterns):* Membandingkan *intuitive errors*, *availability/representativeness heuristics*, *framing effects*, dan *believability bias* pada manusia versus *hallucinations* pada LLM.

3. *Strategi Optimasi Kognitif:* Membandingkan **Fine-tuning** (penyesuaian bobot jaringan permanen melalui dataset domain spesifik) versus **Prompting / In-Context Learning** (pengarahan pemrosesan sementara tanpa pembaruan bobot) dan dampaknya terhadap fenomena skala (*scaling*).

* **Hasil Kunci:**
* **Pencapaian Kognitif LLM:** GPT-4 mencatatkan kinerja setara manusia pada tes *Raven's Progressive Matrices* dan *Theory of Mind* (Kosinski 2023; Gandhi et al. 2024), membuktikan kemampuan konstruksi model mental internal.

* **Batas Keterbatasan Kognitif:** LLM masih merosot signifikan pada *causal reasoning* murni (gagal membedakan kondisi *common cause* vs *causal chain*) dan *complex autonomous planning* (misalnya kegagalan pada tes leksikal *Tower of Hanoi*).

* **Pola Kesalahan Paralel:** Pada tes penalaran silogistik (*Wason Selection Task*), LLM (seperti Chinchilla) menunjukkan bias yang identik dengan manusia: lebih sensitif terhadap validitas logis ketika memuat kesimpulan konkrit/terverifikasi dibanding bentuk abstrak.

* **Implikasi Teoretis Asosiasionisme:** LLM membuktikan bahwa arsitektur asosiatif murni (*connectionist/associative networks*) berskala besar yang dilengkapi mekanisme perhatian (*attention*) sanggup menyatukan struktur sintaksis dan semantik secara simultan (mementahkan klaim pemisahan kaku sintaks-semantik Noam Chomsky). Penulis menyimpulkan bahwa LLM berhasil **membangkitkan kembali teori Asosiasionisme (*Associationism*)** sebagai model komputasional kognisi manusia yang valid.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan perspektif teoretis yang sangat mendalam mengenai hakikat LLM sebagai sistem asosiatif statistik berskala besar.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Berfokus pada analisis kognitif kualitatif dan eksperimen psikologi tanpa membahas arsitektur teknik *retrieval* dokumen (*Information Retrieval*).

* **Relevansi di Sub-bab 2.2 (Dasar Teori Kognisi LLM & Asosiasionisme):** Dikutip pada **Sub-bab 2.2 (Dasar Teori Kognisi LLM & Pemrosesan In-Context)**. Digunakan untuk melegitimasi mengapa LLM dasar mengalami *causal reasoning gap* dan halusinasi jika berdiri sendiri (*standalone*), sehingga memerlukan arsitektur terkontrol seperti **RAG (Retrieval-Augmented Generation)** yang menyuplai fakta eksternal tepercaya ke dalam *context window*.

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

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Pengujian menggunakan profil partisipan sintetis (*fabricated user profiles*) dalam lingkungan simulasi terkontrol.

* **Relevansi di Sub-bab 2.2 (Dasar Teori Arsitektur LLM Agent & Retensi Konteks):** Dikutip pada **Sub-bab 2.2 (Dasar Teori Arsitektur Agentic LLM & Pengelolaan Konteks Multi-Turn)**. Temuan Vadlamani & Borada (2025) melegitimasi krusialnya mengintegrasikan mekanisme *Vector Store / Retriever* (seperti ChromaDB/BM25 pada RAG) untuk menjaga retensi fakta agar tidak terjadi *context loss* saat percakapan akademik berlangsung secara *multi-turn*.

---

### Bagian 7: Paper #33 – #42 (Fondasi Teoretis Information Retrieval & Arsitektur LLM)

#### 33. Robertson et al. (1994) — Okapi at TREC-3

* **Sitasi Lengkap:** Robertson, S. E., Walker, S., Jones, S., Hancock-Beaulieu, M. M., & Gatford, M. (1994). Okapi at TREC-3. *NIST Special Publication 500-225: Proceedings of the Third Text Retrieval Conference (TREC-3)*, 109–126.

* **Objek & Scope:** Evaluasi eksperimental sistem Okapi pada *benchmark* TREC-3 (Disk 1, 2, dan 3) yang memperkenalkan formulasi awal BM25, pencarian berbasis *passage*, serta ekspansi kueri otomatis.

* **Metode / Arsitektur Teoretis:**
1. *Formulasi gabungan BM25:* Penggabungan model BM11 (hipotesis *verbosity*) dan BM15 (tanpa normalisasi panjang) menjadi $BM25(k_1, k_2, k_3, b)$ dengan komponen istilah $\frac{tf^c}{K^c + tf^c}$ di mana $K = k_1 ((1-b) + b \frac{dl}{avdl})$.

2. *Passage Searching:* Penentuan *passage* pada saat *runtime* berdasarkan unit paragraf konsekutif untuk mencegah penalti terhadap dokumen panjang.

3. *Query Expansion tanpa Relevansi (Blind Feedback):* Ekstraksi istilah terbaik dari dokumen peringkat teratas pada pencarian awal menggunakan *Robertson Selection Value* (RSV).

* **Evaluasi & Metrik:** Evaluasi ad-hoc dan *routing* pada Topik 101–150 dan 151–200 menggunakan metrik *Average Precision* (AveP), Precision at 5/30/100 (P5, P30, P100), R-Precision (R-Prec), dan *Relevant Retrieved* (Rel).

* **Hasil Kunci:**
* Penggunaan BM25 bersama ekspansi kueri dan *passage retrieval* menghasilkan peningkatan signifikan (AveP mencapai $0,389$ pada kueri ekspansi + *passage* dibanding $0,337$ pada baseline).

* Nilai $b \approx 0,75$ memberikan kompromi optimal antara BM11 dan BM15.

* *Passage searching* terbukti meningkatkan presisi dan efektivitas ekspansi kueri.

* **Dampak & Penilaian Kritis:**
  * **Positif:** Menjadi bukti empiris pertama di dunia yang memvalidasi keunggulan fungsi BM25 dan pentingnya segmentasi teks (*passage*) dalam skala korpus besar.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Penentuan *passage* pada saat *runtime* berbasis kombinasi paragraf membutuhkan beban komputasi kuadratik $\mathcal{O}(\mathcal{A}^2)$ terhadap jumlah atom teks.

* **Relevansi & Penempatan Spesifik di Sub-bab 2.2:** Dikutip pada **Sub-bab 2.2.3 (Algoritma BM25)** dan **Sub-bab 2.2.8 (Mekanisme Chunking & Passage Retrieval)**. Studi ini melegitimasi mengapa dokumen regulasi akademik UNSRAT perlu dipecah menjadi *chunk/passage* agar skor *retrieval* tidak terdistorsi oleh panjang dokumen.

---

#### 34. Robertson & Walker (1994) — Approximations to 2-Poisson

* **Sitasi Lengkap:** Robertson, S. E., & Walker, S. (1994). Some Simple Effective Approximations to the 2-Poisson Model for Probabilistic Weighted Retrieval. *Proceedings of the 17th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '94)*, 232–241.

* **Objek & Scope:** Penurunan matematis dari fungsi penyederhanaan yang praktis (BM11 dan BM15) untuk mendekati model teoretis 2-Poisson yang sangat kompleks.

* **Metode / Arsitektur Teoretis:**
1. Penurunan matematis kurva saturasi non-linear $w = \frac{tf}{k_1 + tf} w^{(1)}$ dari persamaan log-odds 2-Poisson.

2. Formulasi hipotesis *Verbosity* (dokumen panjang memakai lebih banyak kata untuk menyampaikan hal yang sama) versus hipotesis *Scope* (dokumen panjang menggabungkan banyak topik).

3. Pemodelan frekuensi istilah kueri ($qtf$) melalui pengali $\frac{qtf}{k_3 + qtf}$.

* **Evaluasi & Metrik:** Pengujian pada korpus TREC Disks 1 & 2 (743.000 dokumen, Topik 101–150). Metrik: AveP, P5, P30, P100, RP, dan Recall.

* **Hasil Kunci:**
* BM11 (dengan normalisasi panjang) meningkatkan *Average Precision* hingga 50% dibanding bobot *inverse collection frequency* (BM1) pada kueri pendek ($0,199 \rightarrow 0,300$) dan melonjak drastis pada kueri panjang ($0,085 \rightarrow 0,485$).

* Membuktikan bahwa nilai $k_1$ bernilai kecil ($1,0 - 2,0$) sudah memberikan dampak peningkatan performa yang sangat tajam.

* **Dampak & Penilaian Kritis:**
  * **Positif:** Memberikan landasan filosofis dan konseptual mendasar mengenai alasan di balik bentuk kurva cembung penyeimbang $tf$.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Kombinasi pengali $qtf$ dengan $tf$ dokumen diakui penulis belum memiliki landasan integrasi teoretis yang tunggal, melainkan gabungan heuristik dua model.

* **Relevansi & Penempatan Spesifik di Sub-bab 2.2:** Dikutip pada **Sub-bab 2.2.3 (Dasar Teori Probabilistic Relevance Framework & Penyeimbangan Frekuensi Istilah BM25)**. Dipakai untuk mendukung penjelasan matematis mengapa RAG berbasis BM25 membutuhkan kontrol parameter $k_1$ dan $b$.

---

#### 35. Al-Joofi et al. (2026)

* **Sitasi Lengkap:** Al-Joofi, W., Sagheer, A., & Hamdoun, H. (2026). A Multi-Stage Hybrid Retrieval Framework for the Scientific Literature with Cross-Encoder Re-Ranking. *Applied Sciences*, 16(10), 4813.

* **Objek & Scope:** Kerangka kerja *multi-stage retrieval* untuk literatur ilmiah berbasis klaim, menggabungkan pencarian leksikal (BM25), *dense retrieval* (SciBERT, SPECTER, SciNCL), peleburan hibrida (RRF), serta *re-ranking Cross-Encoder* (MS MARCO MiniLM) pada SciFact, PubMedQA, dan SciDocs.

* **Metode / Arsitektur Teoretis:**
1. *Candidate Retrieval:* Pencarian bi-encoder dense berbasis FAISS (SciBERT, SPECTER, SciNCL) berpasangan dengan leksikal BM25.

2. *Hybrid Fusion:* *Reciprocal Rank Fusion* (RRF, $k=60$) untuk menggabungkan hasil peringkat dari sistem heterogen tanpa kalibrasi skor.

3. *Cross-Encoder Re-ranking:* Pengodean bersama (*joint encoding*) kueri-dokumen menggunakan MS MARCO MiniLM pada 100 kandidat teratas.

4. *Ablasi:* Evaluasi ekspansi kueri leksikal (RM3) vs ekspansi semantik (SPECTER), serta perbandingan enkripsi level-dokumen vs *Passage-level Max Pooling* (MaxP).

* **Evaluasi & Metrik:** NDCG@10, MAP@10, Recall@10, MRR@10, uji signifikansi statistik (paired t-test, Shapiro-Wilk, Wilcoxon signed-rank, Cohen's d), efisiensi komputasi, serta analisis LIME dan *attention heatmap*.

* **Hasil Kunci:**
* Model *dense* berdiri sendiri SciNCL meraih NDCG@10 sebesar $0,503$ (mengungguli BM25 sebesar $0,348$).

* Peleburan RRF murni (SciNCL + BM25) mengalami penurunan performa menjadi $0,475$ akibat efek dilusi (*RRF dilution effect*) di mana kandidat BM25 yang tidak relevan merusak peringkat SciNCL.

* Tahap *Cross-Encoder Re-ranking* menjadi pendorong utama performa puncak ($NDCG@10 = 0,523$; $MAP@10 = 0,479$; $Recall@10 = 0,642$; $MRR@10 = 0,497$).

* Ekspansi RM3 memicu *query drift* ($NDCG@10$ turun ke $0,327$), dan *Passage MaxP pooling* merusak konteks dokumen ilmiah ($NDCG@10$ SPECTER anjlok dari $0,432$ ke $0,251$).

* **Dampak & Penilaian Kritis:**
  * **Positif:** Sangat relevan karena membedah secara mendalam bahaya dilusi RRF dan kegagalan *max pooling* pada dokumen ilmiah.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Penggunaan *Cross-Encoder* meningkatkan *latency* komputasi hingga $\approx 50\text{ ms/query}$ dan pemanfaatan GPU hingga 17,6%.

* **Relevansi & Penempatan Spesifik di Sub-bab 2.2:** Dikutip pada **Sub-bab 2.2.4 (Dense Retrieval)**, **Sub-bab 2.2.6 (Hybrid Retrieval & Rank Fusion RRF)**, dan **Sub-bab 2.2.7 (Arsitektur Multi-Stage & Cross-Encoder Re-ranking)**. Menjadi acuan pembanding langsung untuk menganalisis mengapa *dense* dan *sparse* berinteraksi secara tertentu dalam RAG.

---

#### 36. Kang et al. (2023)

* **Sitasi Lengkap:** Kang, B., Kim, Y., & Shin, Y. (2023). An Efficient Document Retrieval for Korean Open-Domain Question Answering Based on ColBERT. *Applied Sciences*, 13(24), 13177.

* **Objek & Scope:** Penerapan paradigma *late interaction* ColBERT pada sistem *Open-Domain Question Answering* (ODQA) Bahasa Korea menggunakan korpus AI-Hub skala besar.

* **Metode / Arsitektur Teoretis:**
1. *Late Interaction Architecture:* Pengodean independen untuk kueri dan dokumen berbasis enkoder Bahasa Korea (KoBERT, KLUE-RoBERTa, KoBigBird, KLUE-BERT, KoSBERT), diikuti oleh interaksi ringan berbasis *MaxSim* ($\sum \max \text{cosine similarity}$).

2. *Top-k Re-ranking:* Re-ranking pada 1.000 kandidat teratas hasil ekstraksi BM25.

3. *Morpheme-based Tokenization:* Analisis morfem menggunakan Mecab untuk menangani sifat aglutinatif Bahasa Korea.

* **Evaluasi & Metrik:** MRR@10, MRR@100, Recall@50, Recall@200, dan *Latency* (ms/query).

* **Hasil Kunci:**
* ColBERT berbasis KoSBERT meraih kinerja terbaik ($MRR@10 = 68,15$, *Latency* $= 873\text{ ms}$), mengungguli BM25 ($MRR@10 = 55,25$) dan 23 kali lebih cepat dibanding *dense retrieval* KoSBERT penuh ($20.411\text{ ms}$).

* Tokenisasi morfemik via Mecab meningkatkan MRR@10 lebih lanjut menjadi $69,19$.

* **Dampak & Penilaian Kritis:**
  * **Positif:** Mengonfirmasi bahwa paradigma *late interaction* memberikan kompromi paling ideal antara kecepatan inferensi *bi-encoder* dan akurasi interaksi token ala *cross-encoder*.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Membutuhkan ruang penyimpanan indeks vektor yang lebih besar karena harus menyimpan representasi vektor di tingkat token, bukan hanya satu vektor tunggal per dokumen.

* **Relevansi & Penempatan Spesifik di Sub-bab 2.2:** Dikutip pada **Sub-bab 2.2.4 (Dense Semantic Search)** dan **Sub-bab 2.2.7 (Arsitektur Late Interaction & Kompromi Efisiensi-Akurasi)**. Menjadi referensi teoretis untuk arsitektur pencarian vektor yang efisien.

---

#### 37. Lee et al. (2024)

* **Sitasi Lengkap:** Lee, J., Cha, H., Hwangbo, Y., & Cheon, W. (2024). Enhancing Large Language Model Reliability: Minimizing Hallucinations with Dual Retrieval-Augmented Generation Based on the Latest Diabetes Guidelines. *Journal of Personalized Medicine*, 14(12), 1131.

* **Objek & Scope:** Pengembangan sistem *Dual Retrieval-Augmented Generation* (Dual RAG) berbasis panduan medis diabetes (KDA 2023 dan ADA 2023) untuk meminimalkan halusinasi LLM pada domain kesehatan.

* **Metode / Arsitektur Teoretis:**
1. *Dual RAG Framework:* Penggabungan pencarian semantik *dense* (menguji 11 model enkoder seperti Solar Embedding-1-large Upstage, OpenAI text-embedding-3-large/small, gte-multilingual) dengan pencarian kata kunci *sparse* BM25.

2. *Tokenisasi Spesifik Bahasa:* Penggunaan *tokenizer* analisis morfemik `ko_kiwi` untuk teks Bahasa Korea dan `porter_stemmer` untuk Bahasa Inggris.

3. *Chunking Strategy:* Ukuran *chunk* 1.000 karakter dengan *overlap* 200 karakter.

* **Evaluasi & Metrik:** F1-Score, Recall, Precision, MAP, MRR, dan NDCG pada berbagai nilai $k$ (1, 3, 5, 10, 50).

* **Hasil Kunci:**
* Model *dense* Upstage Solar Embedding-1-large memberikan akurasi terbaik untuk panduan Bahasa Korea (f1 = $0,258$, recall = $0,788$), sedangkan OpenAI text-embedding-3-large memimpin pada panduan Bahasa Inggris.

* *Tokenizer* morfemik `ko_kiwi` mengungguli `porter_stemmer` secara signifikan pada teks Bahasa Korea ($NDCG = 0,542$ vs $0,497$ pada $k=50$).

* Pendekatan *Ensemble Retriever* berhasil menggabungkan presisi tinggi dari *dense search* dengan cakupan luas dari *sparse search*.

* **Dampak & Penilaian Kritis:**
  * **Positif:** Mengonfirmasi secara empiris pentingnya pemrosesan morfologi spesifik bahasa pada pencarian dokumen regulasi bertata bahasa kompleks.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:** Limitasi:** Penggunaan *tokenizer* morfemik (`ko_kiwi`) menambah *processing time* ($\approx 1,0 - 1,1\text{ detik}$) dibanding *stemmer* biasa.

* **Relevansi & Penempatan Spesifik di Sub-bab 2.2:** Dikutip pada **Sub-bab 2.2.2 (Arsitektur RAG & Mitigasi Halusinasi)**, **Sub-bab 2.2.3 (Sparse Retrieval & Tokenisasi Morphological)**, dan **Sub-bab 2.2.6 (Ensemble/Hybrid Retrieval)**. Mendukung argumen skripsi Anda mengenai perlunya menggabungkan *dense* dan *sparse* retrieval untuk menangani dokumen regulasi/hukum.

---

#### 38. Karpukhin et al. (2020) — Dense Passage Retrieval (DPR)

* **Sitasi Lengkap:** Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W. (2020). Dense Passage Retrieval for Open-Domain Question Answering. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, hlm. 6769–6781.
* **Objek:** Pencarian pasase (*passage retrieval*) skala besar pada sistem *open-domain question answering* (QA) menggunakan korpus Wikipedia bahasa Inggris (21.015.324 pasase 100-kata).
* **Metode / Arsitektur:**
1. Arsitektur *dual-encoder* berbasis dua jaringan BERT-base (*uncased*) independen: $E_Q(\cdot)$ untuk pemetaan kueri/pertanyaan dan $E_P(\cdot)$ untuk pemetaan pasase teks ke dalam ruang vektor kontinu $d$-dimensi ($d=768$).
2. Skor similaritas dihitung menggunakan fungsi *inner product* (dot product): $\text{sim}(q,p) = E_Q(q)^T E_P(p)$.
3. Pengindeksan pasase dilakukan secara *offline* menggunakan pustaka FAISS (pencarian MIPS / HNSW).
4. Skema pelatihan menggunakan *in-batch negatives* (ukuran batch 128) yang dikombinasikan dengan 1 pasase *hard negative* dari BM25 per pertanyaan, tanpa membutuhkan *pretraining* tugas tambahan seperti *Inverse Cloze Task* (ICT).
5. *Reader Model:* Model cross-attention berbasis BERT-base yang menghitung *passage selection score* dan *answer span score*.

* **Evaluasi & Metrik:** Evaluasi komponen *retriever* menggunakan metrik *Top-$k$ retrieval accuracy* ($k \in \{20, 100\}$) pada 5 dataset QA open-domain: Natural Questions (NQ), TriviaQA, WebQuestions (WQ), CuratedTREC (TREC), dan SQuAD v1.1. Evaluasi *end-to-end* QA menggunakan metrik *Exact Match* (EM).
* **Hasil Kunci:**
* *Akurasi Top-20 Retrieval (NQ):* DPR mencapai **78,4%** (single dataset) dan **79,4%** (multi-dataset), mengungguli BM25 (59,1%) secara signifikan.
* *Akurasi Top-20 Dataset Lain:* TriviaQA 79,4% (vs BM25 66,9%); WQ 75,0% (vs BM25 55,0%); TREC 89,1% (vs BM25 70,9%).
* *Akurasi End-to-End QA (Exact Match):* NQ mencapai **41,5% EM** (mengungguli ORQA 33,3% dan REALM 40,4%); TriviaQA 56,8%; WQ 42,4%; TREC 49,4%.
* *Kecepatan Inferensi:* FAISS CPU index mampu memproses **995,0 pertanyaan per detik**, jauh lebih cepat dibanding Lucene BM25 (23,7 pertanyaan per detik per CPU thread).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* *Positif:* Membuktikan secara empiris bahwa pencarian berbasis *dense representation* murni mampu melampaui kerangka *sparse representation* (BM25) dalam keterhitungan *top-k accuracy* maupun *end-to-end QA accuracy*.
* *Kritik/Limitasi:* DPR dapat mengalami penurunan performa pada kueri yang sangat bergantung pada frasa langka atau kata kunci spesifik (misalnya kata kunci nama tokoh "Thoros of Myr"), di mana BM25 terkadang tetap lebih unggul karena mekanisme *exact term matching*.
* *Relevansi di Sub-bab 2.2 (Dasar Teori Dense Retrieval vs Sparse Retrieval):* Pustaka rujukan teoretis utama untuk menjelaskan mekanisme *Dense Retrieval* (Config B pada skripsi Anda yang menggunakan `gemini-embedding-001` + ChromaDB) serta memberikan pembandingan konseptual dan empiris terhadap *Sparse Retrieval* BM25 (Config C).

---

#### 39. Chen, Fisch, Weston, & Bordes (2017) — DrQA

* **Sitasi Lengkap:** Chen, D., Fisch, A., Weston, J., & Bordes, A. (2017). Reading Wikipedia to Answer Open-Domain Questions. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 1870–1879.

* **Objek / Cakupan:** *Open-Domain Question Answering* (ODQA) dan pencapaian paradigma *Machine Reading at Scale* (MRS) dengan menggunakan seluruh teks tak terstruktur Wikipedia ($\approx 5,07$ juta artikel, 9,0 juta token unik) sebagai satu-satunya sumber pengetahuan tanpa bergantung pada *Knowledge Base* terstruktur.

* **Metode / Materi Kunci:**
* Mengembangkan kerangka kerja dua tahap **DrQA** (*Retriever-Reader Pipeline*), yang menjadi cikal bakal arsitektur RAG modern:

1. **Document Retriever:** Sistem pencarian *sparse* non-ML yang efisien menggunakan *unigram/bigram hashing* (pemetaan *murmur3 hash* hingga $2^{24}$ bin) yang dikombinasikan dengan pembobotan vektor *TF-IDF bag-of-words* untuk mengambil 5 artikel Wikipedia paling relevan secara cepat.

2. **Document Reader:** Model *machine comprehension* berbasis 3-layer *Bidirectional Long Short-Term Memory* (BiLSTM, $h=128$). Vektor fitur paragraf mencakup 300D *GloVe word embeddings* (dengan *fine-tuning* pada 1.000 kata pertanyaan paling sering), fitur biner *exact match* (bentuk asli, huruf kecil, dan lemma), fitur token (POS tag, NER tag, dan *term frequency*), serta *aligned question embedding* menggunakan mekanisme *soft attention*. Model memprediksi *span* posisi awal dan akhir dari teks jawaban.

* **Distant Supervision (DS) & Multitask Learning:** Skema pelatihan otomatis untuk mengasosiasikan pasangan pertanyaan-jawaban tanpa dokumen referensi eksplisit dengan mengambil paragraf yang mengandung pencocokan jawaban dan tumpang-tindih *n-gram* tertinggi, dilanjutkan dengan pelatihan bersama (*multitask*) lintas dataset.

* **Evaluasi & Hasil Kunci:**
* *SQuAD Single-Paragraph Comprehension:* Pada pengujian baca paragraf tunggal SQuAD, *Document Reader* meraih akurasi *Exact Match* (EM) **70,0%** dan *F1-Score* **79,0%** pada *test set*.

* *Full Wikipedia ODQA Setting:* Ketika dievaluasi secara langsung untuk menjawab pertanyaan dari seluruh korpus Wikipedia (tanpa diberi tahu lokasi paragrafnya) menggunakan *Multitask DS*, DrQA mencatatkan akurasi EM sebesar **29,8%** (SQuAD), **25,4%** (CuratedTREC), **20,7%** (WebQuestions), dan **36,5%** (WikiMovies).

* Hasil DrQA pada CuratedTREC mengungguli sistem *pipeline* terintegrasi klasik YodaQA.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Merupakan *milestone* historis utama yang meletakkan dasar arsitektur dua tahap **Retriever-Reader** (yang kemudian berkembang menjadi *Retrieval-Augmented Generation* / RAG) untuk menjawab pertanyaan faktual dari skala dokumen besar tak terstruktur.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Komponen *retriever*-nya masih mengandalkan pencocokan leksikal *sparse* (TF-IDF bigram) tanpa representasi semantik *dense*; komponen *reader*-nya bersifat ekstraktif (*span prediction* BiLSTM) sehingga tidak mampu menyintesis atau memparafrasekan jawaban baru; serta terjadi penurunan akurasi yang tajam (dari 69,5% ke 27,1% pada SQuAD) saat diperluas ke seluruh Wikipedia akibat tingginya *false positives* dari kalimat bertopik serupa.

* **Relevansi & Penempatan di Bab II:** Dikutip pada **Sub-bab 2.1.3 (Evolusi Arsitektur RAG & Retriever-Reader Pipeline)**, **Sub-bab 2.2.6 (Arsitektur Retrieval-Augmented Generation / RAG)**, dan **Sub-bab 2.2.8 (Evaluasi Retrieval & Extractive Span Matching)**.

#### 40. Jurafsky & Martin (2026) — Speech and Language Processing (3rd ed. Draft)

* **Sitasi Lengkap:** Jurafsky, D., & Martin, J. H. (2026). *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition with Language Models* (3rd ed. draft, Jan 6, 2026). Stanford University & University of Colorado at Boulder.
* **Objek:** Buku teks acuan utama yang menyajikan kerangka teoretis dan matematis komprehensif pemrosesan bahasa alami (NLP), *language modeling*, *logistic regression*, *vector semantics*, *Transformers*, *Large Language Models* (LLM), serta *Retrieval-based Models* (IR & RAG).
* **Metode / Arsitektur yang Diuraikan:**
1. *N-gram Language Models (Bab 3):* Estimasi Maximum Likelihood (MLE), asumsi Markov, pengukuran Perplexity ($PP(W) = P(w_1 \dots w_N)^{-1/N}$), serta teknik *smoothing* (Laplace/Add-1, Add-$k$, Linear Interpolation, Stupid Backoff).
2. *Logistic Regression & Klasifikasi (Bab 4):* Pemetaan Sigmoid ($\sigma(z) = \frac{1}{1+e^{-z}}$), fungsi Softmax untuk klasifikasi multi-kelas, *Cross-Entropy Loss* ($L_{CE}$), *Stochastic Gradient Descent* (SGD), serta metrik Precision, Recall, $F_1$-score, Macro/Micro-averaging.
3. *Embeddings & Vector Semantics (Bab 5):* *Distributional hypothesis* (Firth & Harris), *co-occurrence matrix*, Cosine Similarity ($\frac{\vec{v} \cdot \vec{w}}{\vert{}\vec{v}\vert{}\vert{}\vec{w}\vert{}}$), arsitektur Word2Vec (Skip-gram & CBOW), GloVe, dan FastText.
4. *Retrieval-based Models & RAG (Bab 11):* Kerangka arsitektur *Retrieval-Augmented Generation* (RAG) yang menggabungkan modul *retriever* (dense/sparse) dengan *Generative LLM* untuk menghasilkan jawaban berdasar konteks dokumen rujukan.

* **Evaluasi & Metrik:** Menyajikan formulasi matematis baku untuk evaluasi model bahasa alami (Perplexity, Precision, Recall, $F_1$-score, Exact Match, BLEU) serta landasan pengujian signifikansi statistik (*bootstrap test*).
* **Hasil Kunci:** Menyediakan dasar matematis formal untuk seluruh komponen pemrosesan bahasa alami modern, memformulasikan hubungan antara *cross-entropy* dan *perplexity*, serta memberikan landasan teoretis untuk integrasi komponen *retriever* dan *generator* pada RAG.
* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* *Positif:* Menyediakan rujukan teoretis kanonis yang mutakhir untuk mendefinisikan seluruh konsep dasar NLP, RAG, Cosine Similarity, Cross-Entropy Loss, $F_1$-score, dan *language modeling*.
* *Kritik/Limitasi:* Berbentuk pustaka acuan umum (buku teks), sehingga menyintesis konsep-konsep teoretis secara luas tanpa menyajikan satu eksperimen empiris spesifik pada dataset tunggal.
* *Relevansi di Sub-bab 2.2 (Dasar Teori RAG, Vector Semantics, dan Metrik Evaluasi):* Sumber acuan teoretis utama untuk mendefinisikan persamaan matematika baku pada Sub-bab 2.2.

---

#### 41. Mikolov et al. (2013) — Word2Vec (CBOW & Skip-gram)

* **Sitasi Lengkap:** Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient Estimation of Word Representations in Vector Space. *arXiv preprint arXiv:1301.3781*. (Dipresentasikan pada ICLR 2013).
* **Objek:** Pembentukan representasi vektor kontinu (*dense word embeddings*) dari korpus teks berskala besar (Google News 6 miliar kata dan data hingga 1,6 miliar kata).
* **Metode / Arsitektur:**
1. *Continuous Bag-of-Words (CBOW):* Memprediksi kata target berdasarkan kata-kata konteks sekitarnya ($N$ kata sebelum dan sesudah), di mana vektor konteks dirata-ratakan tanpa memperhitungkan urutan kata. Kompleksitas komputasi pelatihan: $Q = N \times D + D \times \log_2(V)$.
2. *Continuous Skip-gram:* Memprediksi kata-kata konteks dalam jangkauan $C$ berdasarkan kata target tunggal. Kompleksitas komputasi pelatihan: $Q = C \times (D + D \times \log_2(V))$.
3. Menggunakan *Hierarchical Softmax* berbasis *Huffman binary tree* untuk mengurangi kompleksitas output dari $O(V)$ menjadi $O(\log_2 V)$. Pelatihan dikembangkan secara paralel menggunakan framework terdistribusi DistBelief.

* **Evaluasi & Metrik:** Dataset "Semantic-Syntactic Word Relationship" yang terdiri dari 8.869 pertanyaan semantik dan 10.675 pertanyaan sintaktik (total 19.544 pertanyaan analogi $\vec{x} = \vec{v}_b - \vec{v}_a + \vec{v}_c$). Evaluasi juga dilakukan pada Microsoft Research Sentence Completion Challenge.
* **Hasil Kunci:**
* Model Skip-gram (300 dimensi, 783M kata) mencapai akurasi keseluruhan **53,3%** (Semantik 50,0%, Sintaktik 55,9%).
* Pada framework DistBelief (1000 dimensi, 6B kata), Skip-gram mencapai akurasi **65,6%** (Semantik 66,1%, Sintaktik 65,1%), sementara CBOW mencapai **63,7%**.
* Membuktikan bahwa aljabar vektor sederhana mampu menangkap hubungan analogi kata secara linier ($\text{Vector("King")} - \text{Vector("Man")} + \text{Vector("Woman")} \approx \text{Vector("Queen")}$).
* Kombinasi Skip-gram dengan RNNLM mencapai rekor *state-of-the-art* **58,9% akurasi** pada Microsoft Sentence Completion Challenge.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* *Positif:* Menandai pergeseran historis dari *sparse representation* (one-hot/count-based) ke *dense continuous embeddings* yang efisien dan mampu menyimpan hubungan semantik linier.
* *Kritik/Limitasi:* Menghasilkan *static embeddings* (satu kata hanya memiliki satu vektor tunggal), sehingga tidak sanggup membedakan makna kata polisemi yang bervariasi tergantung konteks kalimat.
* *Relevansi di Sub-bab 2.2 (Dasar Teori Word Embeddings dan Vector Space Model):* Pijakan teoretis mendasar untuk menjelaskan evolusi *Word Embeddings* menuju *Sentence/Passage Embeddings* dan *Vector Database* (ChromaDB) pada arsitektur RAG.

---

#### 42. Vaswani et al. (2017) — Transformer Architecture

* **Sitasi Lengkap:** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems (NIPS 2017)*, Vol. 30, hlm. 5998–6008.
* **Objek:** Arsitektur pemrosesan urutan (*sequence transduction / machine translation*) yang menghilangkan lapisan rekurensi (RNN/LSTM) dan konvolusi (CNN) sepenuhnya.
* **Metode / Arsitektur:**
1. Arsitektur **Transformer** berbasis *Encoder-Decoder* yang sepenuhnya mengandalkan **Self-Attention**.
2. **Scaled Dot-Product Attention:** $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$, di mana faktor skalasi $\frac{1}{\sqrt{d_k}}$ mencegah *vanishing gradient* pada nilai $d_k$ besar.
3. **Multi-Head Attention:** Memproyeksikan Query, Key, dan Value sebanyak $h$ kali secara paralel ($h=8$, $d_k = d_v = 64$ untuk $d_{\text{model}}=512$) guna menangkap informasi dari berbagai ruang subspace representasi.
4. **Position-wise Feed-Forward Networks (FFN):** Dua transformasi linear dengan aktivasi ReLU di antaranya.
5. **Positional Encoding:** Fungsi sinusoidal ($\sin$ dan $\cos$) dengan frekuensi berbeda untuk menyuntikkan informasi urutan/posisi token secara deterministik.
6. Encoder terdiri dari $N=6$ layer identik (tiap layer memiliki 2 sub-layer: Multi-Head Self-Attention dan FFN dengan *residual connection* dan *Layer Normalization*). Decoder terdiri dari $N=6$ layer identik (dengan tambahan sub-layer *Masked Multi-Head Attention*).

* **Evaluasi & Metrik:** Dataset penerjemahan WMT 2014 English-to-German (EN-DE, 4,5 juta pasang kalimat) dan English-to-French (EN-FR, 36 juta pasang kalimat). Metrik: BLEU score dan biaya komputasi (FLOPs).
* **Hasil Kunci:**
* Model *Transformer (big)* mencapai skor **28,4 BLEU** pada WMT 2014 English-to-German (meningkat >2,0 BLEU melampaui seluruh model SOTA dan *ensemble* sebelumnya) dengan waktu latih 3,5 hari pada 8 GPU NVIDIA P100.
* Pada WMT 2014 English-to-French, *Transformer (big)* mencatatkan skor **41,0 BLEU**.
* Kompleksitas sekuensial per layer berkurang dari $O(n)$ pada RNN menjadi $O(1)$ pada *Self-Attention*, memungkinkan paralelisasi komputasi secara masif selama pelatihan.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* *Positif:* Menjadi pondasi arsitektur paling fundamental bagi Large Language Models (LLM) modern (seperti Google Gemini, BERT, dan RoBERTa) yang digunakan dalam penelitian RAG Anda.
* *Kritik/Limitasi:* Kompleksitas memori dan komputasi *Self-Attention* bersifat kuadratis $O(n^2)$ terhadap panjang urutan ($n$), sehingga memerlukan strategi *chunking* atau *restricted attention* ketika memproses dokumen berukuran panjang.
* *Relevansi di Sub-bab 2.2 (Dasar Teori Arsitektur Transformer dan Self-Attention):* Landasan teoretis utama untuk menjelaskan mekanisme kerja generator LLM (Google Gemini) dan *encoder* embedding dalam sistem RAG.

---

### Bagian 8: Paper #43 – #52 (Knowledge Injection, Scaling Laws & Model Generatif LLM)

#### 43. Manning, Raghavan, & Schütze (2009) — An Introduction to Information Retrieval

* **Sitasi Lengkap:** Manning, C. D., Raghavan, P., & Schütze, H. (2009). *An Introduction to Information Retrieval*. Cambridge University Press.
* **Objek:** Buku teks acuan utama bidang *Information Retrieval* (IR), mencakup pemrosesan teks, *Inverted Index*, *Boolean Retrieval*, *Tolerant Retrieval*, *Index Construction & Compression*, *Term Weighting*, *Vector Space Model*, *Probabilistic IR*, *Okapi BM25*, dan *Language Models for IR*.
* **Metode & Konsep Kunci yang Dibahas:**
1. *Boolean Retrieval & Inverted Index (Bab 1 & 2):* Struktur *Inverted Index* (Dictionary + Postings Lists), pemrosesan kueri Boolean, *postings merge algorithm* dengan kompleksitas waktu $O(x+y)$, *skip pointers*, *biword index*, *positional index*.
2. *Vector Space Model & Pembobotan TF-IDF (Bab 6):* Skalasi Term Frequency ($tf_{t,d}$), Inverse Document Frequency ($idf_t = \log(N / df_t)$), bobot $tf\text{-}idf_{t,d} = tf_{t,d} \times idf_t$, dan Cosine Similarity pada ruang vektor.
3. *Probabilistic IR & Okapi BM25 (Bab 11):* Probability Ranking Principle (PRP), Binary Independence Model (BIM), dan fungsi pemeringkatan non-biner **Okapi BM25** yang memperhitungkan *saturating term frequency* ($k_1$) dan *document length normalization* ($b$).
4. *Language Models for IR (Bab 12):* Query likelihood model.

* **Evaluasi & Metrik:** Formulasi baku metrik evaluasi IR: Precision, Recall, $F_1$-score, Mean Average Precision (MAP), Mean Reciprocal Rank (MRR), dan Normalized Discounted Cumulative Gain (NDCG).
* **Hasil Kunci:** Menyajikan landasan sistematis seluruh algoritma IR klasik, membuktikan secara matematis efisiensi *inverted index* dan keunggulan pemeringkatan BM25 serta *vector space model* atas pencarian Boolean mentah.
* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
* *Positif:* Menyediakan rujukan teoretis paling sah dan standar untuk algoritma *Sparse Retrieval* **BM25** (Config C pada skripsi Anda), *Inverted Index*, serta fungsi pembobotan *tf-idf*.
* *Kritik/Limitasi:* Berfokus pada pencocokan leksikal (*lexical matching / sparse space*), sehingga tidak mencakup representasi semantik *dense vector* berbasis *deep neural networks* yang berkembang pada era setelahnya.
* *Relevansi di Sub-bab 2.2 (Dasar Teori Information Retrieval, Inverted Index, dan BM25):* Pustaka rujukan teoretis utama untuk menjelaskan mekanisme kerja *Sparse Retrieval* BM25 dan metrik evaluasi IR klasik.

---

#### 44. Yao, Duan, Xu, Cai, Sun, & Zhang (2024)

* **Sitasi Lengkap:** Yao, Y., Duan, J., Xu, K., Cai, Y., Sun, Z., & Zhang, Y. (2024). A survey on large language model (LLM) security and privacy: The Good, The Bad, and The Ugly. *High-Confidence Computing*, 4(1), 100211. (Elsevier).
* **Objek / Cakupan:** Survei komprehensif mengenai taksonomi keamanan dan privasi *Large Language Models* (LLM) yang mencakup 281 paper, dikategorikan ke dalam tiga ranah utama: *"The Good"* (aplikasi keamanan yang menguntungkan), *"The Bad"* (penggunaan ofensif/serangan siber), dan *"The Ugly"* (kerentanan inheren LLM beserta strategi mitigasinya).
* **Metode / Materi Kunci:**
1. *The Good (83 Paper):* Kontribusi LLM untuk keamanan kode sepanjang *software lifecycle* (*secure coding, test case generation/fuzzing, vulnerable code detection, malware detection, program repair*) dan keamanan data (*data integrity, data confidentiality, data reliability, data traceability/watermarking*).
2. *The Bad (54 Paper):* Serangan siber yang memanfaatkan kapabilitas penalaran LLM, terbagi atas *Hardware-level* (side-channel), *OS-level* (privilege escalation), *Software-level* (malware generation), *Network-level* (phishing, CAPTCHA breaking), dan *User-level* (misinformation, social engineering, FraudGPT, WormGPT).
3. *The Ugly (143 Paper):* Kerentanan internal AI (*data poisoning, backdoor attacks, attribute/membership inference, training data extraction, prompt injection, jailbreaking, DoS*) dan kerentanan non-AI (*RCE pada aplikasi terintegrasi LLM, side-channel, supply chain plugin*).
4. *Strategi Pertahanan (Defenses):* Pertahanan pada arsitektur model, pembersihan korpus pra-pelatihan (*corpora cleaning: detoxification, debiasing, de-identification*), *optimization methods* (*adversarial training, safe instruction tuning*), serta pertahanan inferensi (*instruction pre-processing, in-process malicious detection, post-processing self-critique*).

* **Evaluasi & Hasil Kunci:**
* Komunitas peneliti lebih dominan memanfaatkan LLM untuk memperkuat keamanan dibanding menggunakannya sebagai alat serangan (83 vs 54 paper).
* Mayoritas studi (17 dari 25 paper) mengonfirmasi bahwa metode analisis keamanan berbasis LLM mengungguli pendekatan konvensional (*Higher code coverage, higher accuracy, lower cost*).
* Serangan tingkat pengguna (*User-level attacks*) merupakan bentuk penyalahgunaan paling dominan (33 paper) karena memanfaatkan kemampuan penalaran bahasa yang menyerupai manusia.
* *Safe instruction tuning* dan evaluasi pengaruh arsitektur model terhadap keamanan LLM diidentifikasi sebagai area yang masih minim diteliti.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan kerangka teoretis yang sangat luas mengenai spektrum risiko keamanan LLM, khususnya ancaman *prompt injection* dan *data leakage*.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Sebagai paper survei, studi ini tidak melakukan pengujian eksperimental mandiri pada korpus regulasi akademik.

* **Relevansi & Penempatan Spesifik di Bab II:** Dikutip pada **Sub-bab 2.2.5 (*Large Language Models, Keamanan, & Guardrails*)** dan **Sub-bab 2.1.4 (*Evaluasi Kinerja & Keamanan Sistem Berbasis LLM*)**. Sangat penting untuk mendasari perlunya mekanisme *guardrails*, pembersihan *prompt*, dan pembatasan hak akses saat mengintegrasikan LLM Gemini dalam arsitektur RAG skripsi Anda.

---

#### 45. Zhang et al. (2025) — MIT Press

* **Sitasi Lengkap:** Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., Huang, X., Zhao, E., Zhang, Y., Chen, Y., Wang, L., Luu, A. T., Bi, W., Shi, F., & Shi, S. (2025). Siren’s Song in the AI Ocean: A Survey on Hallucination in Large Language Models. *Computational Linguistics*, 51(1), 1–45. (MIT Press).
* **Objek / Cakupan:** Survei definitif mengenai taksonomi, akar penyebab (*sources*), tolok ukur evaluasi (*benchmarks*), serta strategi mitigasi halusinasi pada *Large Language Models* (LLM).
* **Metode / Materi Kunci:**
1. *Taksonomi 3-Arah Halusinasi LLM:*
* **Input-conflicting hallucination:** Generasi teks menyimpang dari dokumen/instruksi sumber yang dimasukkan pengguna.
* **Context-conflicting hallucination:** Teks yang dihasilkan bertentangan dengan konteks/pernyataan yang dibuat oleh LLM itu sendiri sebelumnya dalam percakapan *multi-turn*.
* **Fact-conflicting hallucination:** Teks yang dihasilkan bertentangan dengan fakta dunia nyata atau tidak dapat diverifikasi oleh basis pengetahuan tepercaya.

2. *Empat Sumber Utama Halusinasi:* (a) Memorisasi pengetahuan parametrik yang salah/berderau dari korpus *pre-training*; (b) *Overinflated self-confidence* (kepercayaan diri berlebihan pada batas pengetahuan yang tidak jelas); (c) Proses *alignment* yang bermasalah (*sycophancy* dan SFT yang memaksa model menjawab kueri di luar kapasitasnya); (d) Risiko strategi generasi (*decoding randomness* & *hallucination snowballing*).
3. *Taksonomi Mitigasi Terstruktur Masa Inferensi:* Menguraikan *Context-Aware Decoding* (CAD), *Inference-Time Intervention* (ITI), *Chain-of-Verification* (CoVe), *Uncertainty Exploitation* (SelfCheckGPT), *Multi-agent debate*, serta **Resorting to External Knowledge / RAG**.

* **Evaluasi & Hasil Kunci:**
* Menegaskan bahwa pendekatan *Resorting to External Knowledge* (RAG) merupakan salah satu strategi mitigasi halusinasi masa inferensi yang paling efektif karena bersifat *plug-and-play*, mampu menyuntikkan *up-to-date knowledge* tanpa mengubah parameter model, serta meningkatkan *interpretability* (dapat ditelusuri kembali ke dokumen referensi).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Merupakan **rujukan teoretis paling authoritative (Computational Linguistics 2025)** untuk merumuskan definisi dan taksonomi halusinasi LLM pada Bab II skripsi Anda.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Menunjukkan bahwa metrik evaluasi otomatis berbasis overlap klasik (BLEU/ROUGE) tidak lagi memadai untuk mengukur halusinasi LLM *free-form*, melegitimasi penggunaan kerangka kerja modern seperti Ragas.

* **Relevansi & Penempatan Spesifik di Bab II:** Rujukan utama untuk **Sub-bab 2.2.8 (*Teori Halusinasi LLM & Taksonomi 3-Arah*)**, **Sub-bab 2.2.7 (*Retrieval-Augmented Generation*)**, dan **Sub-bab 2.1.4 (*Evaluasi Kinerja Sistem Berbasis LLM & Mitigasi Halusinasi*)**.

---

#### 46. Sun, Sheng, Zhou, & Wu (2024) — Nature Portfolio

* **Sitasi Lengkap:** Sun, Y., Sheng, D., Zhou, Z., & Wu, Y. (2024). AI hallucination: towards a comprehensive classification of distorted information in artificial intelligence-generated content. *Humanities and Social Sciences Communications*, 11(1), 1278. (Nature Portfolio / Springer Nature).
* **Objek / Cakupan:** Klasifikasi komprehensif informasi terdistorsi (*distorted information*) pada *Artificial Intelligence-Generated Content* (AIGC) berbasis analisis konten empiris terhadap 243 sampel kegagalan ChatGPT (284 unit analisis/titik kesalahan).
* **Metode / Materi Kunci:**
* Mengombinasikan 75 kategori terdistorsi dari literatur media sosial dan AIGC menjadi skema pengodean 2 tingkat.
* Menggunakan analisis konten kuantitatif dan kualitatif dengan uji reliabilitas antar-koder metode Holsti (mencapai konsistensi 89%).
* Menghasilkan taksonomi hierarkis berisi **8 Tipe Kesalahan Tingkat Pertama** dan **31 Tipe Kesalahan Tingkat Kedua**:
1. *Overfitting* (Illusions of confidence, Falling into traps, Flattery) — 25 unit.
2. *Logic errors* (Causal uncorrelation, Contradictions) — 25 unit.
3. *Reasoning errors* (Spatial, Temporal, Physical, Psychological, Interpersonal, Hypothetical) — 116 unit (*paling dominan*).
4. *Mathematical errors* (Satire, Metaphorical, Conceptual, Measurement units, Calculation) — 58 unit.
5. *Unfounded fabrication* (False health info, False proof, Pseudoscience, False academic info) — 10 unit.
6. *Factual errors* (Common sense mistakes, Objective fact errors, Author's work errors) — 36 unit.
7. *Text output errors* (Repetition, Programming code, Translation, Grammar, Spelling) — 20 unit.
8. *Other errors* (Discrimination, Restrictive filtering, Harmful info) — 11 unit.

* **Evaluasi & Hasil Kunci:**
* *Reasoning errors* (116 unit) dan *Mathematical/Measurement errors* (58 unit) terbukti menjadi jenis kesalahan yang paling sering dihasilkan oleh LLM generatif.
* Menunjukkan secara empiris bahwa kecenderungan model untuk bersikap *flattery* (menyenangkan pengguna) dan *falling into traps* (terjebak pertanyaan pancingan) merupakan bentuk *overfitting* yang sering memicu informasi palsu.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti taksonomi kesalahan empiris berbasis sampel dunia nyata yang sangat berguna untuk mengategorikan pola kegagalan sistem pada analisis kualitatif (Rumusan Masalah 3 / RQ3) skripsi Anda.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Sampel terbatas pada ChatGPT standalone (GPT-3.5/GPT-4) tanpa komponen *retriever* terpisah (bukan arsitektur RAG terkontrol).

* **Relevansi & Penempatan Spesifik di Bab II:** Dikutip pada **Sub-bab 2.2.8 (*Taksonomi Empiris Kesalahan Teks AIGC*)** serta **Sub-bab 2.1.4 / 2.1.5 (*Karakterisasi Pola Kegagalan Sistem & Research Gap*)**.

---

#### 47. Yao & Fujita (2024)

* **Sitasi Lengkap:** Yao, C., & Fujita, S. (2024). Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags. *Electronics*, 13(23), 4643. (MDPI).
* **Objek / Cakupan:** Pengembangan kerangka kerja *Adaptive Retrieval-Augmented Generation* (RAG) yang mengendalikan proses *retrieval* dan evaluasi dokumen eksternal menggunakan *reflective tags* serta teknik *Chain-of-Thought* (CoT).
* **Metode / Materi Kunci:**
1. *Adaptive Retrieval Tag (`RTV`):* LLM secara mandiri mengevaluasi apakah kueri dapat dijawab menggunakan pengetahuan internal. Jika tidak mampu, LLM memicu pencarian dokumen eksternal via tag `RTV`.
2. *Reflective Document Evaluation Tags:* Dokumen hasil pencarian diproses secara paralel dan dievaluasi langkah demi langkah menggunakan 3 tag reflektif:
* `RLV` (*Relevance*): Menilai relevansi dokumen terhadap kueri berbasis *cosine similarity* embedding Sentence-BERT (*"Relevant"* / *"Irrelevant"*).
* `SPT` (*Support*): Menilai tingkat dukungan fakta terhadap pertanyaan (*"Fully Supported"*, *"Partially Supported"*, *"Not Supported"*).
* `PIT` (*Point Score*): Memberikan skor kelayakan dokumen dari skala 1 sampai 5.

3. *Generasi Paralel & CoT:* Teks dengan skor tertinggi dari dokumen terpillih digunakan untuk menyintesis jawaban akhir secara bertahap (*step-by-step reasoning*).

* **Evaluasi & Hasil Kunci:**
* Diuji pada 4 dataset (*ARC-Challenge, PubHealth, PopQA-Long-Tail, TriviaQA*) menggunakan baseline Qwen dan GPT-3.5.
* Integrasi RAG reflektif secara konsisten mendongkrak akurasi di seluruh dataset. Peningkatan paling signifikan terjadi pada dataset *fact-checking* **PubHealth** (Qwen + RAG melonjak **+7,09%** dari 58,42% ke 65,51%; GPT-3.5 + RAG melonjak **+3,56%** dari 68,70% ke 72,26%).
* *Uji Ablasi:* Menghapus tag `RTV` atau tag evaluasi reflektif (`RLV`, `SPT`, `PIT`) secara signifikan menurunkan akurasi sistem, membuktikan bahwa pemfilteran konteks berderau via tag reflektif sangat vital untuk menekan halusinasi.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan arsitektur *Agentic / Adaptive RAG* yang sangat relevan untuk mengatasi masalah *noisy/irrelevant context* yang sering merusak presisi pencarian dokumen regulasi.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Evaluasi hanya mengukur metrik akurasi akhir (*Accuracy*), belum mengadopsi metrik kualitas RAG spesifik seperti *Context Precision* atau *Faithfulness* milik Ragas.

* **Relevansi & Penempatan Spesifik di Bab II:** Dikutip pada **Sub-bab 2.2.6 (*Arsitektur Agentic & Adaptive RAG*)** dan **Sub-bab 2.1.3 (*Implementasi Arsitektur RAG*)** untuk menunjukkan tren pergeseran dari RAG pasif menuju RAG reflektif adaptif.

---

#### 48. Hoffmann et al. (2022) — Chinchilla Scaling Laws

* **Sitasi Lengkap:** Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., de Las Casas, D., Hendricks, L. A., Welbl, J., Clark, A., Hennigan, T., Noland, E., Millican, K., van den Driessche, G., Damoc, B., Guy, A., Osindero, S., Simonyan, K., Elsen, E., Rae, J. W., Vinyals, O., & Sifre, L. (2022). *Training Compute-Optimal Large Language Models*. arXiv preprint arXiv:2203.15556.
* **Objek / Cakupan:** Formulasi hukum skala (*scaling laws*) efisiensi komputasi optimal untuk *Large Language Models* (LLM) autoregresif berbasis arsitektur Transformer.
* **Metode / Materi Kunci:**
* Meneliti proporsi optimal antara ukuran model ($N$, jumlah parameter) dan jumlah data pelatihan ($D$, jumlah token) berdasarkan batas komputasi FLOP ($C$).
* Melatih lebih dari 400 model bahasa dengan rentang 70 juta hingga lebih dari 16 miliar parameter pada 5 miliar hingga 500 miliar token menggunakan 3 pendekatan empiris:
1. *Fix model size & vary training tokens:* Memvariasikan jumlah langkah pelatihan dengan *cosine learning rate decay* yang disesuaikan dengan total langkah.
2. *IsoFLOP profiles:* Memvariasikan ukuran model pada 9 tingkat anggaran FLOP konstan ($6\times10^{18}$ hingga $3\times10^{21}$ FLOPs) untuk menemukan titik minimum *loss*.
3. *Parametric loss modeling:* Memodelkan *loss* akhir sebagai fungsi parametrik $\hat{L}(N,D) = E + \frac{A}{N^\alpha} + \frac{B}{D^\beta}$ menggunakan *Huber loss optimization*.

* **Hasil Kunci / Temuan Utama:**
* Membantah kesimpulan *scaling law* terdahulu (Kaplan et al., 2020) yang menyatakan parameter harus diskalakan lebih cepat daripada token ($N \propto C^{0.73}, D \propto C^{0.27}$).
* Hoffmann et al. membuktikan bahwa untuk komputasi optimal, **ukuran model dan jumlah token pelatihan harus diskalakan secara seimbang/sama besar** ($N_{opt} \propto C^{0.50}$ dan $D_{opt} \propto C^{0.50}$). Setiap penggandaan ukuran model wajib diimbangi dengan penggandaan jumlah token data pelatihan.
* Mengonfirmasi hipotesis ini dengan melatih model **Chinchilla** (70 miliar parameter, 1.4 triliun token) pada anggaran FLOP yang identik dengan Gopher (280 miliar parameter, 300 miliar token). Chinchilla secara konsisten mengungguli Gopher (280B), GPT-3 (175B), Jurassic-1 (178B), dan Megatron-Turing NLG (530B) pada berbagai pengujian (*MMLU*: 67,5% vs Gopher 60,0%), dengan biaya inferensi yang jauh lebih murah.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Memberikan landasan teoretis mendasar mengapa model yang lebih kecil namun dilatih dengan token yang lebih banyak (seperti keluarga Gemini Flash/Pro modern) jauh lebih efisien dan unggul secara performa serta latensi.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Fokus utama paper adalah pada tahap *pre-training* autoregresif tak terstruktur, belum mengevaluasi secara langsung dampak *retrieval-augmented generation* (RAG) atau pengindeksan vektor eksternal.

* **Relevansi & Penempatan di Bab II (2.2):** Wajib dikutip pada **Sub-bab 2.2.5 (*Large Language Models, Scaling Laws, & Efisiensi Komputasi*)** untuk menjelaskan dasar matematika efisiensi model generatif yang digunakan sebagai *generator* dalam arsitektur RAG skripsi Anda.

---

#### 49. Gemini Team (2025) — Gemini 2.5 Technical Report

* **Sitasi Lengkap:** Gemini Team, Google. (2025). *Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities*. arXiv preprint arXiv:2507.06261.
* **Objek / Cakupan:** Arsitektur, kapabilitas penalaran dinamis (*thinking*), pemrosesan multimodal native, jendela konteks panjang, dan kapabilitas agen dari keluarga model Gemini 2.5 (Gemini 2.5 Pro, Gemini 2.5 Flash, serta Gemini 2.0 Flash/Flash-Lite).
* **Metode / Materi Kunci:**
* *Arsitektur:* Sparse Mixture-of-Experts (MoE) Transformer yang dioptimalkan untuk stabilitas pelatihan skala besar pada infrastruktur TPUv5p.
* *Native Multimodality & Long Context:* Mendukung input teks, gambar, audio, dan video hingga konteks 1 juta+ token secara native.
* *Inference-Time Thinking (Penalaran Dinamis):* Model dilatih menggunakan *Reinforcement Learning* (RL) untuk memanfaatkan alokasi komputasi tambahan saat inferensi (*thinking budget*). Model merekonstruksi langkah penalaran internal sebelum menghasilkan jawaban akhir.
* *Post-Training & Mitigasi Keamanan:* Peningkatan *Reinforcement Learning from Human and Critic Feedback* (RL*F*), *verifiable rewards*, serta pelatihan adversarial untuk menahan serangan *indirect prompt injection*.

* **Hasil Kunci / Temuan Utama:**
* Gemini 2.5 Pro meraih performa SOTA pada benchmark koding dan penalaran (AIME 2025: 88,0%, GPQA Diamond: 86,4%, LiveCodeBench: 74,2%, Humanity's Last Exam: 21,6%).
* *Skalabilitas Thinking Budget:* Meningkatkan jumlah token *thinking* internal berbanding lurus dengan kenaikan akurasi pada masalah kompleks (AIME 2025 melonjak dari ~67% pada 1.024 token menjadi >87% pada 32.768 token).
* Gemini 2.5 Flash bertindak sebagai model hibrida penalaran dengan latensi dan biaya inferensi yang jauh lebih rendah, bahkan melampaui performa Gemini 1.5 Pro generasi sebelumnya.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan rujukan teoretis paling mutakhir mengenai arsitektur LLM *generator* (Google Gemini) yang Anda gunakan pada skripsi, khususnya bagaimana kapabilitas penalaran dinamis dan *long-context* dikelola oleh model.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Sebagai laporan teknis industri, detail jumlah parameter spesifik dan konfigurasi internal MoE tidak dipublikasikan secara eksplisit karena alasan komersial.

* **Relevansi & Penempatan di Bab II (2.2):** Wajib dikutip pada **Sub-bab 2.2.5 (*Large Language Models & Arsitektur Google Gemini*)** untuk menjelaskan spesifikasi, mekanisme penalaran, dan evolusi generator LLM yang Anda integrasikan via API LangChain.

---

#### 50. Gemini Team (2024) — Gemini 1.5 Technical Report

* **Sitasi Lengkap:** Gemini Team, Google. (2024). *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context*. arXiv preprint arXiv:2403.05530.
* **Objek / Cakupan:** Arsitektur, efisiensi komputasi, dan evaluasi kapabilitas pemrosesan konteks panjang (*long-context retrieval & reasoning*) hingga 10 juta token pada Gemini 1.5 Pro dan Gemini 1.5 Flash.
* **Metode / Materi Kunci:**
* *Arsitektur:* Gemini 1.5 Pro berbasis Sparse Mixture-of-Experts (MoE) Transformer; Gemini 1.5 Flash berbasis Transformer decoder terdistilasi secara *online* dari 1.5 Pro untuk pencapaian latensi rendah.
* *Metodologi Evaluasi Long-Context:*
1. *Diagnostic Probing:* Pengujian *perplexity* (Negative Log-Likelihood / NLL) pada dokumen panjang, eksperimen *Needle-in-a-Haystack* (teks, video, audio), *Multiple Needles*, dan *Multi-round Co-reference Resolution* (MRCR).
2. *Realistic Long-Context Tasks:* *In-context language learning* (MTOB: penerjemahan bahasa Kalamang dari 1 buku grammar ~250k token), *Long-document QA* (buku *Les Misérables* ~710k token), *Long-context Audio ASR*, dan *Long-video QA*.

* **Hasil Kunci / Temuan Utama:**
* *Needle-in-a-Haystack:* Gemini 1.5 Pro mencatatkan tingkat *recall* nyaris sempurna (>99,7%) pada konteks hingga 1 juta token di seluruh modalitas (teks, audio 107 jam, video 10,5 jam), dan mempertahankan *recall* >99,2% hingga 10 juta token teks.
* *Long-document QA vs RAG:* Pada tugas tanya-jawab dokumen penuh (*Les Misérables* ~710k token), memasukkan seluruh dokumen ke dalam jendela konteks Gemini 1.5 Pro menghasilkan jawaban yang lebih unggul (78% *win-rate*) dibandingkan pendekatan RAG eksternal berbasis *chunking* 4k token (TF-IDF/Vector Search) yang digabungkan dengan Gemini 1.5 Pro atau GPT-4 Turbo.
* *In-context Learning:* Mampu mempelajari tata bahasa Kalamang (bahasa langka dengan <200 penutur) secara *in-context* dari dokumentasi linguistic tanpa *fine-tuning* bobot model.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan argumen teoretis dan komparasi empiris yang sangat krusial antara pendekatan RAG (*retriever* eksternal + *chunking*) dengan *In-Context Long-Context Reasoning*.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Meskipun konteks panjang 1M+ token menunjukkan *recall* tinggi pada pencarian fakta (*needle*), biaya token dan latensi inferensi untuk konteks raksasa tetap menjadi *trade-off* utama jika dibandingkan dengan RAG berbasis *chunking* hemat token (seperti ChromaDB/BM25 pada eksperimen skripsi Anda).

* **Relevansi & Penempatan di Bab II (2.2):** Wajib dikutip pada **Sub-bab 2.2.6 (*Arsitektur Retrieval-Augmented Generation vs. Long-Context Prompting*)** dan **Sub-bab 2.2.7 (*Metrik Evaluasi Sistem IR & Ragas*)**.

---

#### 51. Google (2023) — PaLM 2 Technical Report

* **Sitasi Lengkap:** Google. (2023). *PaLM 2 Technical Report*. arXiv preprint arXiv:2305.10403.
* **Objek / Cakupan:** Arsitektur, pemodelan komputasi optimal, kemampuan multibahasa, penalaran matematika, koding, dan evaluasi keamanan pada keluarga model PaLM 2 (ukuran S, M, L, dan varian koding PaLM 2-S*).
* **Metode / Materi Kunci:**
* *Arsitektur & Pre-training Objective:* Berbasis Transformer decoder yang dilatih menggunakan kombinasi obyektif *denoising* yang diselaraskan dengan penelitian UL2 (*Unifying Language Learning Paradigms*).
* *Validation of Scaling Laws:* Menguji secara independen *scaling laws* Hoffmann et al. (2022) pada skala komputasi besar ($1\times10^{19}$ hingga $1\times10^{22}$ FLOPs), mengonfirmasi bahwa parameter $N$ dan token $D$ harus diskalakan secara seimbang ($N \propto C^{0.49}, D \propto C^{0.51}$).
* *Multilingual Mixture:* Dataset mencakup dokumen multibahasa tak terstruktur dari ratusan bahasa, dokumen paralel, kode pemrograman, dan data matematika.
* *Control Tokens:* Penggunaan token kontrol pada tahap *pre-training* untuk mengendalikan tingkat toksisitas respons saat inferensi.

* **Hasil Kunci / Temuan Utama:**
* Model PaLM 2-L (dengan ukuran parameter yang jauh lebih kecil daripada PaLM 540B) berhasil melampaui performa PaLM 540B secara konsisten pada penalaran bahasa, koding (HumanEval pass@1: 37,6%), matematika (GSM8K: 92,2%), translasi (WMT21 MQM), dan lulus uji kompetensi bahasa profesional (HSK 7-9, PLIDA C2, DELE C2).
* Menegaskan bahwa optimasi campuran data pre-training dan obyektif pelatihan (UL2) memberikan peningkatan kualitas yang lebih signifikan dibandingkan sekadar memperbesar jumlah parameter model secara masif.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan fondasi evolusi sejarah arsitektur LLM Google sebelum era Gemini, mendasari pemahaman tentang bagaimana obyektif *denoising* (UL2) dan dataset multibahasa dibentuk.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** PaLM 2 masih berarsitektur *dense Transformer* generasi sebelum Mixture-of-Experts (MoE) dan belum mendukung konteks panjang hingga jutaan token sebagaimana Gemini 1.5/2.5.

* **Relevansi & Penempatan di Bab II (2.2):** Dikutip pada **Sub-bab 2.2.5 (*Large Language Models, Arsitektur Transformer, & Obyektif Pelatihan UL2*)** untuk menjelaskan evolusi fondasi LLM generatif.

---

#### 52. DeepMind (2026) — Gemini 3.5 Flash Model Evaluation Methodology & Results

* **Sitasi Lengkap:** DeepMind / Google. (2026). *Model Evaluation - Approach, Methodology & Results: Gemini 3.5 Flash*. Laporan Evaluasi Resmi Google DeepMind (Mei 2026).
* **Objek / Cakupan:** Laporan metodologi dan hasil evaluasi kuantitatif model **Gemini 3.5 Flash** di berbagai domain kemampuan (koding agen, UI control, tugas pakar, multimodal, konteks panjang, dan penalaran akademik) per Mei 2026.
* **Metode / Materi Kunci:**
* *Metodologi Evaluasi:* Pengujian *single-attempt* (pass@1) tanpa *majority voting* atau *parallel test-time compute* via Gemini API (`gemini-3.5-flash`) dengan konfigurasi *sampling default*.
* *Benchmark Agen & Koding:* Terminal-Bench 2.1 (harness Terminus-2), SWE-Bench Pro (harness Antigravity), MCP Atlas (Model Context Protocol), Toolathlon.
* *Benchmark UI Control & Expert Tasks:* OSWorld-Verified (agen eksekusi komputer 1080p via `pyautogui`), Finance Agent v2, GDPval-AA.
* *Multimodal & Long Context:* CharXiv Reasoning, MMMU-Pro, Blueprint-Bench 2, MRCR v2 (8-needle, batas 128k dan 1M token).
* *Reasoning & Academic:* Humanity's Last Exam (HLE), ARC-AGI-2 (puzel penalaran abstrak semi-private).
* *Pembanding:* Gemini 3 Flash, Gemini 3.1 Pro, Claude Sonnet 4.6, Claude Opus 4.7, dan GPT-5.5.

* **Hasil Kunci / Temuan Utama:**
* Gemini 3.5 Flash mencatatkan skor koding agen terminal tertinggi pada Terminal-bench 2.1 (**76,2%** vs Gemini 3 Flash 58,0%), MCP Atlas (**83,6%**), OSWorld-Verified UI control (**78,4%**), dan GDPval-AA (**1656 Elo**).
* Pada benchmark konteks panjang MRCR v2 (8-needle), Gemini 3.5 Flash mencapai skor **77,3%** pada 128k token dan **26,6%** pada 1M token.
* Menunjukkan tren evolusi di mana model kelas *Flash* (ringan/latensi rendah) berhasil menyamai atau melampaui performa model kelas *Pro/Opus* generasi sebelumnya pada tugas-tugas berbasis agen (*agentic workflows*) dan penggunaan alat (*tool use*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan data acuan empiris paling mutakhir (2026) mengenai batas kemampuan model generatif efisien kelas *Flash* dalam mengeksekusi *tool use*, *long context retrieval*, dan alur kerja agen.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Berupa dokumen ringkasan hasil evaluasi (*evaluation sheet*), bukan makalah arsitektur penuh, sehingga fokus utamanya adalah perbandingan skor benchmark.

* **Relevansi & Penempatan di Bab II (2.2):** Dikutip pada **Sub-bab 2.2.5 (*Perkembangan LLM Lightweight/Flash*)** dan **Sub-bab 2.2.7 (*Metrik Evaluasi Sistem IR & Benchmark Agen*)**.

---

### Bagian 9: Paper #53 – #60 (Evaluasi RAG, Hallucination Benchmarks & Domain-Specific QA)

#### 53. Gao et al. (2024)

* **Sitasi Lengkap:** Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H. (2024). Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv preprint arXiv:2312.10997v5*.
* **Objek / Cakupan:** *Comprehensive survey paper* mengenai perkembangan, taksonomi, dan arsitektur *Retrieval-Augmented Generation* (RAG) pada era Large Language Models (LLM).
* **Metode / Materi Kunci:**
1. **Evolusi Paradigma RAG:** Mengategorikan RAG ke dalam 3 tahap evolusi:
* *Naive RAG:* Alur sekuensial klasik *Retrieve-Read* (Indexing $\rightarrow$ Retrieval $\rightarrow$ Generation).
* *Advanced RAG:* Menambahkan optimasi *Pre-Retrieval* (query rewriting, query expansion, indexing granularity, metadata) dan *Post-Retrieval* (reranking, context compression/filtering).
* *Modular RAG:* Arsitektur terintegrasi yang fleksibel, mendukung penggantian/penambahan modul fungsional (*Search, Memory, Routing, Predict, Task Adapter*) serta pola interaksi dinamis (*Rewrite-Retrieve-Read, Generate-Read, DSP, ITER-RETGEN, Self-RAG, FLARE*).

2. **Tiga Komponen Utama:**
* *Retrieval:* Sumber data (unstructured, semi-structured PDF, structured KG, LLM-generated), granularitas (*token, phrase, sentence, proposition, chunk, document*), pengindeksan (*chunking, metadata, structural index/KG*), optimasi kueri, serta *hybrid retrieval* (sparse BM25 + dense neural).
* *Generation:* *Context curation* (reranking, ekstraksi/kompresi konteks seperti LLMLingua dan RECOMP) serta *LLM fine-tuning* (RA-DIT).
* *Augmentation Process:* *Iterative retrieval*, *Recursive retrieval*, dan *Adaptive retrieval* (retrieval berbasis ambang batas konfidensi/token refleksi).

* **Evaluasi:** Merangkum *RAG Triad Quality Scores* (*Context Relevance, Answer Faithfulness, Answer Relevance*) dan 4 kemampuan kunci (*Noise Robustness, Negative Rejection, Information Integration, Counterfactual Robustness*), serta alat/benchmark evaluasi (*RAGAS, ARES, TruLens, RGB, RECALL, CRUD-RAG*).
* **Hasil Kunci:** Menyajikan pemetaan menyeluruh mengenai keunggulan RAG dibandingkan *Fine-Tuning* murni (RAG unggul dalam dinamika data *real-time*, interpretabilitas, dan pencegahan halusinasi) serta menegaskan bahwa kapasitas LLM *Long-Context* tidak menggantikan RAG karena pertimbangan kecepatan inferensi, keterlihatan proses penalaran (*observability*), dan efisiensi biaya.
* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Merupakan **rujukan taksonomi RAG paling berwibawa** yang menjelaskan perbedaan antara Naive, Advanced, dan Modular RAG. Menjadi landasan teoritis yang sangat kuat untuk menjelaskan alur RAG pada metode skripsi Anda.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Sebagai paper *survey*, artikel ini memberikan gambaran luas mengenai puluhan teknik, namun tidak menyajikan eksperimen empiris sendiri pada korpus spesifik perguruan tinggi Indonesia.

* **Relevansi & Penempatan di Bab II (2.2 & 2.1):** Wajib dikutip di **Sub-bab 2.2.7 (Arsitektur RAG & Taksonomi Paradigma)**, **Sub-bab 2.2.8 (Teknik Optimasi Retrieval & Chunking Strategy)**, serta **Sub-bab 2.2.10 (Framework Evaluasi Ragas)**. Juga memperkuat argumen di **2.1.3** dan **2.1.5 (Research Gap)** mengenai pentingnya memilih arsitektur retrieval yang tepat.

---

#### 54. Ovadia et al. (2024) — EMNLP 2024

* **Sitasi Lengkap:** Ovadia, O., Brief, M., Mishaeli, M., & Elisha, O. (2024). Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024)* (pp. 237–250).
* **Objek:** Studi komparatif empiris antara *Unsupervised Fine-Tuning* (*continual pre-training*) dan *Retrieval-Augmented Generation* (RAG) untuk injeksi pengetahuan fakta (*knowledge injection*) pada LLM (Llama2-7B, Mistral-7B, Orca2-7B).
* **Metode / Materi Kunci:**
1. Menguji efektivitas injeksi pengetahuan pada dua kategori data:
* *MMLU Benchmark:* 5 domain pengetahuan terstruktur (Anatomy, Astronomy, College Biology, College Chemistry, Prehistory) untuk menguji pengetahuan yang pernah dilihat (*previously seen knowledge*).
* *Current Events Task:* Dataset baru berbasis 910 soal pilihan ganda dari Wikipedia AS periode Agustus–November 2023 untuk menguji fakta yang benar-benar baru (*unseen knowledge* pasca-cutoff LLM).

2. Menganalisis 4 konfigurasi: *Base Model*, *Base Model + RAG* (menggunakan embedding `bge-large-en` dan FAISS, $K \in \{0..5\}$), *Fine-Tuned (FT)*, dan *FT + RAG*.
3. Menerapkan augmentasi data berbasis parafrasa (*GPT-4 paraphrasing* hingga 10 variasi per *chunk*) untuk mengevaluasi dampak repetisi terhadap *fine-tuning*.

* **Evaluasi:** Metrik akurasi jawaban pilihan ganda berdasarkan skor *log-likelihood* opsi jawaban menggunakan kerangka *LM-Evaluation-Harness*.
* **Hasil Kunci:**
* **RAG secara konsisten mengungguli Unsupervised Fine-Tuning** di seluruh eksperimen, baik untuk pengetahuan yang sudah ada di pre-training maupun pengetahuan faktual yang benar-benar baru.
* LLM **sangat kesulitan mempelajari fakta faktual baru hanya melalui unsupervised fine-tuning biasa** (bahkan FT standar pada Llama2 untuk data *current events* mengalami degradasi performa/lupa akibat *catastrophic forgetting* atau *immemorization*).
* Pengajaran fakta baru via Fine-Tuning hanya dapat sedikit meningkat jika fakta tersebut diulang dalam **banyak variasi parafrasa yang beragam** (*repetitive data augmentation*).
* Penggabungan FT + RAG tidak memberikan dorongan performa yang konsisten dan cenderung tidak stabil dibandingkan RAG murni.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan **bukti empiris tingkat tinggi (EMNLP 2024)** yang memvalidasi keputusan metodologis skripsi Anda untuk **menggunakan RAG daripada me-fine-tune LLM** dalam menginjeksikan dokumen regulasi akademik UNSRAT.
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Fokus evaluasi pada *unsupervised fine-tuning* (continual pre-training), belum mencakup teknik *instruction-tuning* atau RLHF yang dikombinasikan dengan QA berpasangan.

* **Relevansi & Penempatan di Bab II (2.1 & 2.2):** Sangat krusial diletakkan di **Sub-bab 2.1.2 (Adopsi LLM pada Layanan Akademik)** dan **Sub-bab 2.1.5 (Research Gap & Justifikasi Metodologis RAG vs Fine-Tuning)** untuk membuktikan secara ilmiah mengapa RAG berbasis *in-context learning* adalah pilihan terbaik untuk dokumen regulasi. Juga diletakkan di **Sub-bab 2.2.7 (Dasar Teori RAG)**.

---

#### 55. Sharma (2025)

* **Sitasi Lengkap:** Sharma, C. (2025). Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers. *arXiv preprint arXiv:2506.00054v1*. (Under review at ACM TOIS).
* **Objek / Cakupan:** Tinjauan sistematis mutakhir (2025) mengenai arsitektur RAG, teknik optimasi *end-to-end* (retrieval, filtering, efficiency, robustness, reranking), evaluasi empiris komparatif pada *Short-form* dan *Multi-hop QA*, serta batas ketahanan (*robustness frontiers*) terhadap noise, halusinasi, dan serangan adversaris.
* **Metode / Materi Kunci:**
1. **Taksonomi Arsitektural 4 Pilar:**
* *Retriever-based:* Query-centric (RQ-RAG, RAG-Fusion, KRAGEN), Retriever-centric adaptation (Re2G, SimRAG, RankRAG), Granularity-aware (LongRAG, FILCO).
* *Generator-based:* Faithfulness-aware decoding (SELF-RAG, SelfMem), Context compression & utility filtering (FiD-Light, xRAG, GenRT), Retrieval-guided generation.
* *Hybrid:* Multi-round retrieval (IM-RAG, GenGround), Dynamic retrieval triggering (DRAGIN, FLARE, CRAG), Utility-driven joint optimization (Stochastic RAG).
* *Robustness & Security-oriented:* Noise-adaptive training (RAAT), Hallucination-aware decoding (RAGTruth), Adversarial robustness & security (BadRAG, TrojanRAG).

2. **Analisis Teknik Optimasi:** Membedah *context filtering* (FILCO, IB Filtering, SEER, RAG-Ex), *efficiency/latency acceleration* (Sparse RAG, Speculative Pipelining, RAGCache), dan *reranking* (RLT, ToolRerank, RankRAG, RAG-Fusion).

* **Evaluasi:** Melakukan analisis komparatif atas puluhan *framework* RAG pada dataset *Short-form QA* (PopQA, TriviaQA, ARC, NQ) dan *Multi-hop QA* (HotpotQA, 2Wiki, MuSiQue), serta merangkum *framework* evaluasi mutakhir (*ARES, RAGAS, RGB, RAGTruth, MIRAGE, FeB4RAG, BERGEN*).
* **Hasil Kunci:**
* Optimasi komponen *retrieval* (terutama *query decomposition* dan *reranking*) merupakan pendorong peningkatan performa terbesar pada *multi-hop reasoning*.
* Kerangka *hybrid* berbasis umpan balik dinamis (seperti Self-CRAG dan Self-RAG) memberikan lonjakan skor keandalan faktual (*FactScore*) tertinggi (hingga +0,456).
* *Retrieval* murni tanpa mekanisme penyaringan/verifikasi konteks pasca-pencarian rentan terhadap *retrieval noise*, halusinasi, dan kerentanan keamanan (*backdoor/poisoning attacks*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan taksonomi dan komparasi empiris terbaru (2025) untuk memperjelas posisi arsitektur RAG, serta memberikan argumen kuat mengenai perlunya evaluasi *Context Precision/Recall* dan *Faithfulness* (seperti pada kerangka Ragas skripsi Anda).
  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Mengulas banyak *framework* kompleks (seperti *graph-based* dan *agentic RAG*) yang memerlukan *resource* komputasi besar, yang melebihi skala prototipe skripsi pada umumnya.

* **Relevansi & Penempatan di Bab II (2.2 & 2.1):** Dikutip di **Sub-bab 2.2.7 (Arsitektur & Taksonomi RAG Modern)**, **Sub-bab 2.2.8 (Teknik Filtering & Reranking)**, dan **Sub-bab 2.2.10 (Metrik & Benchmarking Evaluasi Ragas)**. Juga memperkuat uraian di **2.1.4 (Evaluasi Kinerja Sistem Berbasis RAG)**.

---

#### 56. Gomez-Cabello et al. (2025)

* **Sitasi Lengkap:** Gomez-Cabello, C. A., Prabha, S., Haider, S. A., Genovese, A., Collaco, B. G., Wood, N. G., Bagaria, S., & Forte, A. J. (2025). Comparative Evaluation of Advanced Chunking for Retrieval-Augmented Generation in Large Language Models for Clinical Decision Support. *Bioengineering*, 12(11), 1194.

* **Objek / Cakupan:** Evaluasi komparatif strategi pemotongan dokumen (*chunking*) pada arsitektur Retrieval-Augmented Generation (RAG) berbasis LLM (Google Gemini 1.0 Pro) untuk sistem pendukung keputusan klinis (perawatan pasca-operasi rhinoplasty pada 30 kueri klinis).

* **Metode / Materi Kunci:**
* Mengunci seluruh tumpukan arsitektur RAG agar identik (backbone LLM: **Gemini 1.0 Pro**, *embedding model*: Vertex AI `text-embedding-004` 768-D, *vector store*: Chroma DB, top-$k = 5$), dengan variabel bebas tunggal berupa strategi *chunking* dokumen:

1. *Fixed-size Baseline (Recursive Character):* Pemotongan berbasis karakter $\approx 1000$ karakter dengan *overlap* $\approx 100$ karakter.

2. *Semantic Cluster Chunking:* Kalimat dipisah via spaCy, diwakili vektor TF-IDF, lalu dikelompokkan dengan K-means ($k=6$ kluster) berdasarkan kemiripan isi.

3. *Proposition-Based Chunking:* Menggunakan LLM (Vertex AI `text-bison@002`, `temperature=0.2`, `max_tokens=256`) untuk mengekstrak pernyataan fakta atomik dari setiap kalimat, lalu digabungkan hingga kapasitas $\approx 500$ kata.

4. *Adaptive Chunking (Pendekatan Baru):* Penentuan batas *chunk* secara dinamis menggunakan *Sentence Transformer* (`all-MiniLM-L6-v2`) dengan ambang batas *cosine similarity* $\ge 0,8$ dan batasan $\approx 500$ kata. Setiap *chunk* yang selesai diberi penambahan judul deskriptif singkat (*micro-header* 5–15 kata) secara otomatis menggunakan model inferensi BART (`facebook/bart-large-cnn`).

* **Evaluasi & Hasil Kunci:**
* *Medical Accuracy* (Skala Likert 1–3 oleh pakar medis): *Adaptive chunking* meraih skor rerata tertinggi ($2,37 \pm 0,72$; 87% respons minimal agak akurat, 50% sepenuhnya akurat), signifikan secara statistik melampaui *Fixed Baseline* ($1,63 \pm 0,72$; 50% agak akurat, 13% sepenuhnya akurat; $p = 0,001$, *Cohen's d* = 1,03). Strategi *Proposition* ($2,07 \pm 0,78$) dan *Semantic* ($2,03 \pm 0,76$) berada di tingkat menengah.

* *Clinical Relevance:* *Adaptive* mencatatkan rerata $2,90 \pm 0,40$ (93% sepenuhnya relevan) dengan deviasi standar paling sempit, menunjukkan stabilitas jawaban yang lebih tinggi dibandingkan *Baseline* ($2,60 \pm 0,81$; 80% sepenuhnya relevan).

* *Information Retrieval (IR) Metrics:* *Adaptive chunking* mengungguli seluruh metode pada *Precision* (0,50 vs 0,17 *Baseline*), *Recall* (0,875 vs 0,40 *Baseline*), dan *F1-score* (0,643 vs 0,235 *Baseline*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti eksperimental kuat yang mengisolasi *chunking policy* sebagai penentu utama kualitas *retrieval* dan akurasi jawaban, serta membuktikan bahwa penyesuaian batas semantik + injeksi *micro-header* meningkatkan kinerja RAG secara signifikan tanpa perlu *fine-tuning* bobot LLM.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Parameter ambang batas kemiripan (0,8) dan batas kata (500 kata) dituning secara lokal pada korpus tunggal spesifik, serta belum melaporkan uji reliabilitas antar-penilai (*inter-rater reliability*).

* **Relevansi & Penempatan di Bab II:** Dikutip pada **Sub-bab 2.1.3 (Implementasi Arsitektur RAG & Trade-off Chunking)** dan **Sub-bab 2.2.8 (Evaluasi Kinerja Systems & Strategi Chunking)**. Studi ini menjadi rujukan empiris langsung penggunaan **Gemini LLM** dalam pengujian strategi *chunking* dinamis.

---

#### 57. Jimeno Yepes et al. (2024)

* **Sitasi Lengkap:** Jimeno Yepes, A., You, Y., Milczek, J., Laverde, S., & Li, L. (2024). Financial Report Chunking for Effective Retrieval Augmented Generation. *arXiv preprint arXiv:2402.05131v3*.

* **Objek / Cakupan:** Strategi pemotongan dokumen berbasis elemen struktur visual/layout dokumen (*Element-Type Based Chunking*) dibandingkan dengan *chunking* berbasis ukuran token tetap (128, 256, 512 token) pada laporan keuangan SEC (dataset FinanceBench: 141 pertanyaan dari 80 dokumen laporan 10-K, 10-Q, 8-K).

* **Metode / Materi Kunci:**
* Menggunakan model *vision encoder-decoder* (Chipper / Unstructured) berbasis arsitektur Donut untuk mengidentifikasi elemen dokumen per halaman (*Narrative Text, Title, Table, Header, Footer*).

* *Structural Chunking Algorithm:* Penggabungan elemen dilakukan secara berurutan hingga batas 2.048 karakter. Jika menemukan elemen *Title* atau *Table*, *chunk* baru langsung dimulai. Tabel dipertahankan utuh dalam satu *chunk* tanpa dipotong di tengah baris/kolom.

* Penambahan Metadata: Setiap *chunk* diperkaya dengan metadata berupa *Keywords* (GPT-4), *Summary paragraph*, atau *Prefix & Table Description* (dua kalimat pertama + deskripsi kapasi tabel).

* *RAG Stack:* Weaviate Vector DB, *sentence-transformer* `multi-qa-mpnet-base-dot-v1`, generator GPT-4 (top-10 retrieval).

* **Evaluasi & Hasil Kunci:**
* *Q&A Accuracy* (Evaluasi Manual vs Gold Standard): *Element-based chunking* (Chipper Keywords / Prefix) mencatatkan akurasi jawaban tertinggi sebesar **53,19%**, mengungguli strategi token kaku Base 128 (35,46%), Base 256 (36,88%), dan Base 512 (48,23%).

* *Retrieval Accuracy:* Penggabungan hasil *Chipper Aggregation* meraih *Page Accuracy* 84,40%, ROUGE 0,568, dan BLEU 0,452.

* *Efisiensi Komputasi & Indeksasi:* *Element-based chunking* hanya menghasilkan 62.529 total *chunk* (rerata 260,57 *chunk*/dokumen), memangkas jumlah *chunk* hingga separuh dibandingkan metode agregasi token kaku (112.155 *chunk*), yang secara langsung menghemat biaya indeksasi basis data vektor dan menekan latensi *query*.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Membuktikan bahwa *chunking* berbasis tipe elemen struktur dokumen (*heading*, paragraf, tabel) menghilangkan kebutuhan pencarian hiperparameter ukuran token secara manual (*no tuning required*) dan menghasilkan representasi semantik yang lebih utuh.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Membutuhkan tahap ekstraksi layout berdaya komputasi tinggi (*vision encoder-decoder*) pada fase pra-pemrosesan awal.

* **Relevansi & Penempatan di Bab II:** Dikutip pada **Sub-bab 2.1.3 (Implementasi Arsitektur RAG)**, **Sub-bab 2.2.1 (Pra-pemrosesan Teks & Pemisahan Elemen Dokumen)**, dan **Sub-bab 2.2.8 (Efisiensi Indeksasi Vektor & Evaluasi Retrieval)**.

---

#### 58. Reuter et al. (2025)

* **Sitasi Lengkap:** Reuter, M., Lingenberg, T., Liepiņa, R., Lagioia, F., Lippi, M., Sartor, G., Passerini, A., & Sayin, B. (2025). Towards Reliable Retrieval in RAG Systems for Large Legal Datasets. *Proceedings of the Natural Legal Language Processing Workshop 2025*, 17–30.

* **Objek / Cakupan:** Penanganan masalah *Document-Level Retrieval Mismatch* (DRM) pada arsitektur RAG yang beroperasi di atas korpus dokumen hukum terstruktur berskala besar (LegalBench-RAG: CUAD, MAUD, ContractNLI, PrivacyQA).

* **Metode / Materi Kunci:**
* Formulasi Kegagalan **Document-Level Retrieval Mismatch (DRM):** Mengidentifikasi dan mengukur persentase *chunk* terambil ($top-k$) yang berasal dari dokumen sumber yang **salah** akibat tingginya tingkat redudansi leksikal dan klausul *boilerplate* antar-dokumen hukum (pada baseline ContractNLI, DRM mencapai $> 95\%$).

* **Summary-Augmented Chunking (SAC):** Teknik pengayaan konteks pra-pencarian (*pre-retrieval context enrichment*) dengan menghasilkan ringkasan sintetis singkat tingkat dokumen ($\approx 150$ karakter via `gpt-4o-mini`) sebagai "sidik jari dokumen", lalu menempelkannya (*prepend*) pada setiap *chunk* teks rekursif (500 karakter) sebelum di-embedding (`gte-large`) dan diindeks ke FAISS.

* Komparasi Strategi Summarization: Membandingkan *Generic Summarization Prompt* dengan *Expert-Guided Summarization Prompt* (meta-prompt khusus yang dirancang bersama pakar hukum untuk mengekstrak variabel pembeda spesifik seperti nama pihak, batasan kerahasiaan, dan pengecualian).

* **Evaluasi & Hasil Kunci:**
* Penerapan SAC menekan DRM secara drastis di seluruh dataset (memotong tingkat kesalahan hingga separuhnya; rerata DRM keseluruhan turun dari $\approx 46\%$ menjadi $\approx 22\%$ pada top-1, dan dari $\approx 78\%$ menjadi $\approx 38\%$ pada top-64).

* Penurunan DRM secara langsung mendongkrak metrik *Text-Level Precision* dan *Text-Level Recall*.

* *Temuan Kontra-Intuitif:* Ringkasan Generik (*Generic SAC*) secara konsisten **mengungguli** Ringkasan Berbasis Pakar (*Expert-Guided SAC*) pada *text-level precision/recall*. Analisis kualitatif menunjukkan bahwa ringkasan pakar yang terlalu padat dan spesifik menyebabkan *overfitting* fitur hukum, sehingga mengganggu keselarasan semantik (*query alignment*) saat vektor ringkasan + *chunk* dikompresi ke dalam ruang embedding.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyajikan taksonomi kegagalan retrieval baru (DRM) yang sangat relevan untuk korpus regulasi kampus UNSRAT yang memiliki kemiripan struktur format, serta menawarkan solusi *pre-retrieval* yang ringan (hanya 1 panggil LLM per dokumen) tanpa mengubah arsitektur RAG.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Pengujian terbatas pada pencarian satu tahap (*single-stage dense retrieval*) dan belum mengukur dampak akhir generasi teks secara *end-to-end*.

* **Relevansi & Penempatan di Bab II:** Dikutip pada **Sub-bab 2.1.3 (Arsitektur RAG)**, **Sub-bab 2.1.4 (Karakterisasi Pola Kegagalan Retrieval / Failure Modes)**, dan **Sub-bab 2.2.7 (Pengelolaan Konteks Multi-Turn & Pre-Retrieval Enrichment)**.

---

#### 59. Beauchemin, Gagnon, & Khoury (2024)

* **Sitasi Lengkap:** Beauchemin, D., Gagnon, Z., & Khoury, R. (2024). Quebec Automobile Insurance Question-Answering With Retrieval-Augmented Generation. *Proceedings of the Natural Legal Language Processing Workshop 2024*, 48–60.

* **Objek / Cakupan:** Evaluasi arsitektur Advanced RAG berbasis GPT-4o untuk layanan *Question-Answering* (QA) domain hukum/regulasi asuransi mobil di Quebec pada dataset 82 pasang pertanyaan awam dan jawaban pakar.

* **Metode / Materi Kunci:**
* *Parent-Child Chunking:* Dokumen dipotong menjadi *chunk* anak sebesar 500 karakter untuk pengindeksan kemiripan vektor (`text-embedding-ada-002`), namun ketika *chunk* anak cocok, konteks *parent* (seluruh pasal/artikel utama) yang dikembalikan ke LLM.

* *Context Compression:* Hasil pencarian diintegrasikan dan dikompresi menggunakan LLM pemroses sebelum disuntikkan ke *prompt* generasi GPT-4o untuk menghindari efek *lost-in-the-middle*.

* Eksperimen 6 Konfigurasi Refrensi: *Zero-shot* (tanpa RAG), *No references* (hanya prompt engineering), *Laws*, *+F.P.Q. 1*, *+AMF*, dan *All references* (seluruh korpus regulasi).

* Evaluasi Komprehensif: Metrik n-gram (BLEU, ROUGE, METEOR), kemiripan pemaknaan embedding (BERTScore, MeaningBERT), serta *Manual Exam Score* oleh pakar (-1 point untuk pernyataan salah/menyesatkan, 0–2 point per kriteria jawaban).

* **Evaluasi & Hasil Kunci:**
* Konfigurasi *All references* meraih skor tertinggi baik pada metrik otomatis (BLEU-1 33,77%; ROUGE-L 33,61%; BERTScore 78,87%) maupun *Manual Exam Score* (51,74% vs *Zero-shot* 24,23%).

* *Temuan Krusial Mitigasi Risiko:* Evaluasi manual mengungkap bahwa **5% hingga 13% jawaban yang dihasilkan sistem RAG lengkap masih mengandung setidaknya satu pernyataan salah/halusinasi (*false statement*)** yang berpotensi menyesatkan pengguna.

* Injeksi acuan parsial (*incomplete references*) justru menurunkan kualitas jawaban dibandingkan tanpa acuan (*No references*), karena memaksa LLM mengabaikan pengetahuan bawaan yang benar dan menggantikannya dengan konteks terpotong (*context leakage/disruption*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Memberikan bukti empiris lapangan mengenai pentingnya penyediaan korpus regulasi yang utuh dan teknik *parent-child chunking*.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Menggunakan LLM tertutup (GPT-4o) yang rentan terhadap risiko kebocoran data pelatihan (*data leakage*) dari dokumen regulasi publik.

* **Relevansi & Penempatan di Bab II:** Dikutip pada **Sub-bab 2.1.2 (Adopsi LLM pada Layanan Terstruktur)**, **Sub-bab 2.1.4 (Evaluasi Kinerja Sistem & Risiko Halusinasi)**, serta **Sub-bab 2.2.6 (Arsitektur RAG & Parent-Child Chunking)**.

---

#### 60. Bang et al. (2025/2026)

* **Sitasi Lengkap:** Bang, B., Yoon, J., Chang, D.-J., Park, S., & Lee, Y. O. (2025). Retrieval Augmented Large Language Model System for Comprehensive Drug Contraindications. *Preprint / Hongik University & HD Junction*.

* **Objek / Cakupan:** Pengembangan dan evaluasi sistem *Question-Answering* (QA) RAG terintegrasi untuk mendeteksi kontraindikasi obat medis pada populasi rentan (anak-anak/pediatrik, wanita hamil, dan interaksi kombinasi obat) berbasis data resmi *Drug Utilization Review* (DUR).

* **Metode / Materi Kunci:**
* **Hybrid Retrieval System with Re-ranking:** Mengombinasikan pencocokan semantik *dense vector* (`text-embedding-3-small` diindeks pada Milvus Vector DB berbasis *cosine similarity*) dan pencocokan leksikal *sparse* (algoritma BM25 berbasis TF-IDF) via kerangka kerja LangChain, dilanjutkan dengan komponen *Reranker* untuk mengurutkan ulang hasil gabungan sebelum dikirim ke LLM generator.

* **Concept-Level Chunking Strategy:** Setiap entri aturan kontraindikasi dari basis data DUR dipotong menjadi unit semantik tunggal yang mandiri (*discrete clinical concept/restriction*, e.g., batas usia spesifik atau tingkat kontraindikasi kehamilan) dengan batasan maksimum 1.000 token dan **tanpa overlap** untuk menjaga keutuhan dokumen regulasi.

* **Generative LLM:** Menggunakan **GPT-4o-mini** sebagai model dasar.

* **Evaluasi & Hasil Kunci:**
* *Performa Model Standalone (Tanpa RAG):* LLM komersial tanpa RAG (GPT-4o-mini, Claude 3.5 Haiku, LLaMA 3.1 8B Instruct) menunjukkan kinerja buruk dengan akurasi klasifikasi kontraindikasi hanya berkisar antara 0,49 hingga 0,52 (GPT-4o-mini) dan F1-score $< 0,66$.

* *Performa Sistem RAG (Ours):* Integrasi RAG meningkatkan akurasi dan F1-score secara signifikan:
* **Kontraindikasi Kehamilan:** Akurasi **0,94** (F1 0,94).

* **Kontraindikasi Pediatrik / Usia:** Akurasi **0,92** (F1 0,92).

* **Interaksi Antar-Obat (DDI):** Akurasi **0,79** (F1 0,73).

* *Taksonomi Evaluasi Grounding & Reason:* Mengklasifikasikan respons ke dalam 4 kategori penalaran: (1) *Explicit contraindication supported by context*, (2) *Explicit non-contraindication with false evidence*, (3) *Inferred contraindication without evidence (hallucination)*, dan (4) *Explicit non-contraindication supported by context*. Validasi rasional medis menggunakan ontologi kata kunci (*keyword ontology*) mencatatkan Precision/Recall sangat tinggi pada kategori klinis kritis.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti empiris kuat bahwa penggabungan pencarian hibrida (*Hybrid Dense + Sparse Search*) yang dilengkapi dengan tahap *Re-ranking* serta pemotongan dokumen berbasis konsep tunggal (*discrete concept chunking*) secara efektif menekan halusinasi faktual dan meningkatkan presisi pada domain bernuansa regulasi/hukum ketat.

  * **Kritik/Limitasi:** Limitasi:** Limitasi:**  Limitasi:** Kinerja pencarian mengalami penurunan pada kueri kompleks berbasis multi-entitas (seperti interaksi kombinasi obat / DDI dengan F1 0,73), serta evaluasi rasional medis masih sangat bergantung pada pencocokan kata kunci (*keyword matching*).

* **Relevansi & Penempatan di Bab II:** Dikutip pada **Sub-bab 2.1.2 (Adopsi LLM pada Layanan Terstruktur/Regulasi)**, **Sub-bab 2.1.3 (Implementasi Arsitektur RAG & Hybrid Retrieval)**, **Sub-bab 2.2.2 (Sparse Search / BM25 & Reranking)**, dan **Sub-bab 2.2.8 (Evaluasi Kinerja RAG & Granularitas Chunking)**.

---

Seluruh rangkuman ini disusun mengikuti standar format terstruktur `sitasi-full.md`, berpegang teguh pada prinsip *zero-hallucination*, serta dilengkapi pemetaan penempatan spesifik di Bab II (Sub-bab 2.1 Studi Aplikatif vs Sub-bab 2.2 Dasar Teori).

---

### Bagian 10: Paper #61 – #68 (Continual Learning, Catastrophic Forgetting & Fondasi NLP/Dialogue)

#### 61. Luo et al. (2025)

* **Sitasi Lengkap:** Luo, Y., Yang, Z., Meng, F., Li, Y., Zhou, J., & Zhang, Y. (2025). *An Empirical Study of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning*. arXiv preprint arXiv:2308.08747v5 [cs.CL].

* **Objek:** Evaluasi empiris fenomena *Catastrophic Forgetting* (CF) pada *Large Language Models* (LLM) generatif selama proses *continual instruction tuning*.

* **Metode:**
* Pengujian dilatih secara sekuensial pada 5 tugas instruksi: *Text Simplification* (Simp) $\rightarrow$ *Empathetic Dialogue* (Emdg) $\rightarrow$ *Inquisitive Question Generation* (InqQG) $\rightarrow$ *Explanation Generation* (Exp) $\rightarrow$ *Headline Generation* (HGen).

* Arsitektur model yang diuji: BLOOMZ (1.1B, 1.7B, 3B, 7.1B; *decoder-only*), mT0 (1.2B, 3.7B; *encoder-decoder*), serta LLAMA-7B dan ALPACA-7B.

* **Evaluasi:**
* Menggunakan benchmark MMLU (*Domain Knowledge*: STEM, Social, Human, Other), *Reasoning* (BoolQ, PIQA, Winogrande, Hellaswag, MathQA, Mutual), *Reading Comprehension* (RACE-high, RACE-middle), serta *Bias* (CrowS-Pairs).

* Metrik utama: *Forgetting metric* ($FG_i$), yaitu rata-rata persentase penurunan performa evaluasi dibandingkan model awal ($R_0$).

* **Hasil Kunci:**
* Fenomena *catastrophic forgetting* secara umum terjadi pada seluruh skala LLM (1B hingga 7B). Kemampuan *Reading Comprehension* mengalami *forgetting* paling parah, disusul *Domain Knowledge*.

* **Efek Skala Model:** Semakin besar skala model (misal BLOOMZ 7.1B vs 1.1B), persentase penurunan performa ($FG$) justru semakin tajam. Hal ini terjadi karena model besar memiliki *initial performance* yang jauh lebih tinggi, sehingga saat dipaksa *fitting* ke tugas instruksi baru, penurunannya menjadi sangat signifikan.

* **Efek Arsitektur:** Arsitektur *decoder-only* (BLOOMZ) menunjukkan ketahanan retensi pengetahuan yang lebih baik (nilai $FG$ lebih rendah) dibandingkan *encoder-decoder* (mT0) pada skala parameter sebanding.

* **Mitigasi:** *General instruction tuning* (seperti penggabungan data ALPACA) terbukti dapat memitigasi tingkat *forgetting* pada *fine-tuning* lanjutan.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti empiris krusial bahwa melakukan *continual fine-tuning* parametrik pada LLM dapat merusak pengetahuan umum dan kemampuan penalaran model.

  * **Kritik/Limitasi:**  Limitasi:** Eksperimen dibatasi hingga skala 7B parameter karena keterbatasan komputasi.

* **Relevansi & Penempatan di Skripsi:** Dikutip pada **Sub-bab 2.1.2** dan **Sub-bab 2.1.5 (Research Gap)**. Temuan Luo et al. (2025) melegitimasi mengapa skripsi Anda memilih pendekatan **RAG (Retrieval-Augmented Generation)** berbasis *in-context learning* daripada melakukan *continual fine-tuning* pada LLM Gemini: RAG menjaga bobot parametrik LLM tetap utuh sehingga terhindar dari *catastrophic forgetting*.

---

#### 62. Chen et al. (2020) — RecAdam

* **Sitasi Lengkap:** Chen, S., Hou, Y., Cui, Y., Che, W., Liu, T., & Yu, X. (2020). Recall and Learn: Fine-tuning Deep Pretrained Language Models with Less Forgetting. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 7870–7881.

* **Objek:** Mitigasi *catastrophic forgetting* saat mengadaptasi *Deep Pretrained Language Models* (PLM) ke tugas *downstream*.

* **Metode:** Mengembangkan mekanisme *Recall and Learn* yang diintegrasikan ke dalam optimizer Adam, dinamakan **RecAdam**. Terdiri dari 2 komponen utama:

1. *Pretraining Simulation:* Mengestimasi objektif pre-training sebagai penalti kuadratik berbasis jarak parameter tanpa membutuhkan akses ke data pre-training asli.

2. *Objective Shifting:* Menggunakan fungsi *sigmoid annealing* $\lambda(t)$ untuk menggeser fokus optimasi secara bertahap dari *recalling* pengetahuan pre-training ke pembelajaran tugas *target downstream*.

* **Evaluasi:** Diuji menggunakan BERT-base (108M) dan ALBERT-xxlarge (235M) pada 8 tugas benchmark GLUE (MNLI, QQP, QNLI, SST-2, CoLA, STS-B, MRPC, RTE).

* **Hasil Kunci:**
* RecAdam mengungguli *vanilla fine-tuning* pada 7 dari 8 tugas GLUE menggunakan BERT-base (+1.0% peningkatan rerata skor median).

* Pada tugas dengan data kecil (<10k sampel), RecAdam memberikan peningkatan signifikan (+1.7% rerata).

* BERT-base yang dilatih dengan RecAdam mampu melampaui performa rerata *vanilla fine-tuning* BERT-large.

* Model dapat diinisialisasi secara acak (*random initialization*) dan tetap mencapai performa lebih tinggi karena ruang pencarian parameter yang lebih luas.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan teknik tingkat *optimizer* yang sangat efisien untuk memitigasi *forgetting* saat fine-tuning PLM.

  * **Kritik/Limitasi:**  Limitasi:** Membutuhkan *tuning hyperparameter* ($k$ dan $t_0$) yang sensitif untuk tiap tugas *downstream*.

* **Relevansi & Penempatan di Skripsi:** Dikutip pada **Sub-bab 2.2 (Dasar Teori Fine-Tuning PLM & Mitigasi Catastrophic Forgetting)** sebagai pembanding teknis optimasi pemodelan bahasa.

---

#### 63. Goodfellow et al. (2015)

* **Sitasi Lengkap:** Goodfellow, I. J., Mirza, M., Xiao, D., Courville, A., & Bengio, Y. (2015). An Empirical Investigation of Catastrophic Forgetting in Gradient-Based Neural Networks. arXiv preprint arXiv:1312.6211v3 [stat.ML].

* **Objek:** Investigasi empiris mengenai tingkat keparahan *catastrophic forgetting* pada jaringan saraf tiruan modern menggunakan berbagai algoritma pelatihan dan fungsi aktivasi.

* **Metode:**
* Membandingkan *Stochastic Gradient Descent* (SGD) standar vs **Dropout**.

* Membandingkan 4 fungsi aktivasi: Logistic Sigmoid, Rectified Linear (ReLU), Hard Local Winner Take All (LWTA), dan Maxout.

* Diuji pada 3 tipe hubungan antar tugas: *Input reformatting* (MNIST permuted), *Similar tasks* (Amazon reviews), dan *Dissimilar tasks* (MNIST vs Amazon).

* **Evaluasi:** Menggunakan kurva *possibilities frontier* yang memplot *trade-off* antara error tugas baru vs error tugas lama.

* **Hasil Kunci:**
* Pelatihan dengan **Dropout** secara konsisten menjadi algoritma terbaik dalam memitigasi *catastrophic forgetting* pada seluruh jenis pasangan tugas.

* Kombinasi aktivasi **Maxout + Dropout** menjadi satu-satunya metode yang selalu berada pada batas performa terbaik (*possibilities frontier*) di semua pengujian.

* Peringkat fungsi aktivasi sangat bergantung pada tipe tugas (LWTA unggul di tugas *dissimilar*, tetapi terburuk di tugas *similar*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Merupakan studi fondasi klasik yang membuktikan secara empiris bahwa regularisasi struktur (*Dropout*) membantu mempertahankan kapasitas representasi jaringan saraf.

  * **Kritik/Limitasi:**  Limitasi:** Pengujian dilakukan pada *feedforward neural network* klasik 2-hidden layer dan belum mencakup arsitektur Transformer.

* **Relevansi & Penempatan di Skripsi:** Merupakan **sumber fondasi teoretis murni**. Dikutip pada **Sub-bab 2.2 (Dasar Teori Regularisasi & Catastrophic Forgetting)** dan **dikeluarkan dari Tabel 2.1** (Penelitian Terkait Aplikatif).

---

#### 64. Kirkpatrick et al. (2017) — EWC

* **Sitasi Lengkap:** Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A. A., ... & Hadsell, R. (2017). Overcoming catastrophic forgetting in neural networks. *Proceedings of the National Academy of Sciences (PNAS)*, 114(13), 3521–3526.

* **Objek:** Mengatasi *catastrophic forgetting* pada jaringan saraf tiruan sekuensial menggunakan pendekatan yang terinspirasi dari konsolidasi sinaptik otak.

* **Metode:** Mengembangkan algoritma **Elastic Weight Consolidation (EWC)**. EWC memperlambat tingkat pembaharuan (*learning rate*) pada parameter-parameter yang dianggap penting untuk tugas-tugas sebelumnya.

* Menggunakan formulasi Bayes dan *Laplace approximation*, di mana matriks Informasi Fisher (Fisher Information Matrix / $F$) digunakan untuk mengukur tingkat kepentingan tiap bobot $\theta_i$ bagi tugas sebelumnya.

* Menerapkan penalti kuadratik: $\mathcal{L}(\theta) = \mathcal{L}_B(\theta) + \sum_i \frac{\lambda}{2} F_i (\theta_i - \theta_{A,i}^*)^2$.

* **Evaluasi:** Diuji pada *Permuted MNIST* (supervised learning) dan pembelajaran sekuensial 10 game Atari 2600 menggunakan *Deep Q-Networks* (DQN; reinforcement learning).

* **Hasil Kunci:**
* EWC berhasil mempertahankan kinerja pada tugas-tugas lama tanpa mengorbankan kemampuan mempelajari tugas baru.

* Pada domain RL, EWC memungkinkan satu agen DQN tunggal dengan kapasitas parameter tetap untuk memainkan multiple game Atari secara sekuensial.

* Analisis matriks Fisher menunjukkan bahwa EWC mendorong pembagian representasi (*shared representations*) pada lapisan-lapisan akhir jaringan.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Paper *milestone* yang meletakkan dasar metodologis *prior-focused regularization* untuk *continual learning*.

  * **Kritik/Limitasi:**  Limitasi:** Menggunakan asumsi *diagonal Fisher* yang cenderung meremehkan ketidakpastian parameter (*underestimates parameter uncertainty*).

* **Relevansi & Penempatan di Skripsi:** Merupakan **sumber fondasi teoretis murni**. Dikutip pada **Sub-bab 2.2 (Dasar Teori Continual Learning & Regularisasi Bobot)** dan **dikeluarkan dari Tabel 2.1**.

---

#### 65. Mikolov, Yih, & Zweig (2013)

* **Sitasi Lengkap:** Mikolov, T., Yih, W. T., & Zweig, G. (2013). Linguistic Regularities in Continuous Space Word Representations. *Proceedings of NAACL-HLT 2013*, 746–751.

* **Objek:** Identifikasi keteraturan sintaktis dan semantik dalam ruang vektor kontinu dari representasi kata yang dipelajari oleh *Recurrent Neural Network Language Model* (RNNLM).

* **Metode:** **Vector Offset Method** berbasis *cosine similarity*. Mengasumsikan bahwa hubungan antar kata diwakili oleh vektor offset yang konstan.

* Untuk menjawab analogi $a:b :: c:d$ (di mana $d$ tidak diketahui), dihitung vektor $y = x_b - x_a + x_c$, kemudian dicari kata $w$ dengan *cosine similarity* tertinggi: $w = \arg\max_w \frac{x_w y^T}{\Vert{}x_w\Vert{} \Vert{}y\Vert{}}$.

* Contoh ikonik: $x_{King} - x_{Man} + x_{Woman} \approx x_{Queen}$.

* **Evaluasi:**
* Dataset Analogi Sintaktis baru (8.000 pertanyaan: kata sifat, kata benda, kata kerja).

* SemEval-2012 Task 2 (*Measuring Relation Similarity*, 69 relasi semantik).

* **Hasil Kunci:**
* Vektor RNNLM (dimensi 1600) berhasil menjawab hampir 40% pertanyaan analogi sintaktis secara tepat (jauh mengungguli LSA yang hanya 11.3%).

* Pada SemEval-2012, RNNLM mengungguli sistem *state-of-the-art* terbaik sebelumnya (UTD-NB) dengan Spearman's $\rho = 0.275$ dan MaxDiff Accuracy $0.418$.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Paper pionir yang membuktikan bahwa *distributed word representations* menangkap hubungan semantik/sintaktis secara aljabar vektor.

  * **Kritik/Limitasi:**  Limitasi:** Representasi kata masih bersifat statis (satu kata satu vektor), belum terkontekstualisasi seperti Transformer modern.

* **Relevansi & Penempatan di Skripsi:** Merupakan **sumber fondasi teoretis murni**. Dikutip pada **Sub-bab 2.2.3 (Vector Semantics, Dense Embeddings, & Cosine Similarity)** dan **dikeluarkan dari Tabel 2.1**.

---

#### 66. Devlin et al. (2019) — BERT

* **Sitasi Lengkap:** Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, 4171–4186.

* **Objek:** Pemodelan representasi bahasa terkontekstualisasi secara dwiarah mendalam (*deep bidirectional*) menggunakan Transformer Encoder.

* **Metode:**
* Pre-training dua tugas tanpa pengawasan:
1. **Masked Language Model (MLM):** Mengacak 15% token masukan dan memprediksi kata asli berdasarkan konteks kiri dan kanan sekaligus.

2. **Next Sentence Prediction (NSP):** Memprediksi apakah kalimat B merupakan kelanjutan dari kalimat A.

* Arsitektur: $BERT_{BASE}$ ($L=12, H=768, A=12$, 110M param) dan $BERT_{LARGE}$ ($L=24, H=1024, A=16$, 340M param).

* **Evaluasi:** Diuji pada 11 tugas NLP utama: GLUE Benchmark, SQuAD v1.1, SQuAD v2.0, SWAG, dan CoNLL-2003 NER.

* **Hasil Kunci:**
* Mencapai *state-of-the-art* baru pada 11 tugas NLP. Menolak keterbatasan model searah (*unidirectional*) seperti OpenAI GPT.

* Meningkatkan skor GLUE menjadi 80.5% (+7.7% di atas SOTA sebelumnya), MultiNLI menjadi 86.7%, SQuAD v1.1 F1 menjadi 93.2, dan SQuAD v2.0 F1 menjadi 83.1.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Paper paling revolusioner yang menandai era *Pre-trained Language Models* (PLM) berbasis Transformer Encoder.

  * **Kritik/Limitasi:**  Limitasi:** Proses pre-training membutuhkan sumber daya komputasi yang sangat besar (16 TPU selama 4 hari).

* **Relevansi & Penempatan di Skripsi:** Merupakan **sumber fondasi teoretis murni**. Dikutip pada **Sub-bab 2.2.5 (Large Language Models & Arsitektur Transformer)** dan **Sub-bab 2.2.6 (Dense Embeddings/Dense Retrieval)**. **Dikeluarkan dari Tabel 2.1**.

---

#### 67. Furnas et al. (1987) — The Vocabulary Problem

* **Sitasi Lengkap:** Furnas, G. W., Landauer, T. K., Gomez, L. M., & Dumais, S. T. (1987). The Vocabulary Problem in Human-System Communication. *Communications of the ACM*, 30(11), 964–971.

* **Objek:** Variabilitas spontan dalam pemilihan kata (*spontaneous word choice*) oleh manusia saat merujuk pada objek/perintah dalam sistem komputer (*The Vocabulary Problem*).

* **Metode:** Studi empiris terhadap pilihan kata spontan pada 5 domain aplikasi: *Text editing*, *Message decoder*, *Common objects*, *Classified ads*, dan *Recipe keywords*. Simulasi statistik dikembangkan untuk menguji performa berbagai strategi pencarian (*Armchair naming*, *Best single name*, *Aliases*, *Unlimited aliasing*).

* **Hasil Kunci:**
* **Variabilitas Luar Biasa:** Dua orang secara spontan memilih kata yang sama untuk merujuk pada objek yang sama memiliki probabilitas **kurang dari 0.20** (hanya 7% - 18% kesepakatan).

* **Kegagalan Armchair Naming:** Metode konvensional di mana desainer menentukan 1 nama tunggal (*Armchair method*) menghasilkan tingkat kegagalan **80% hingga 90%** pada pencarian pertama pengguna.

* **Mitos "Nama Alami":** Tidak ada satu pun kata terbaik yang "jelas" atau "alami" untuk suatu objek. Pilihan nama paling populer pun hanya mencakup <30% percobaan pengguna.

* **Solusi Unlimited Aliasing:** Penyediaan indeks alias yang sangat banyak (*unlimited aliases*) dan mekanisme *interactive disambiguation* terbukti meningkatkan angka keberhasilan hingga 3-5 kali lipat.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Legitimasi historis paling mendasar mengapa sistem *lexical matching* kaku (*keyword-based*) sering gagal dan mengapa pencarian semantik (*dense retrieval*) atau augmentasi kueri RAG sangat dibutuhkan.

* **Relevansi & Penempatan di Skripsi:** Dikutip pada **Sub-bab 1.1 (Latar Belakang)** dan **Sub-bab 2.2.2 (Model Lexical/Sparse Retrieval & Keterbatasannya)** untuk mendasari argumentasi mengapa pencarian leksikal persis murni tidak cukup bagi interaksi percakapan akademik.

---

#### 68. McTear (2002) — Spoken Dialogue Technology

* **Sitasi Lengkap:** McTear, M. F. (2002). Spoken Dialogue Technology: Enabling the Conversational User Interface. *ACM Computing Surveys (CSUR)*, 34(1), 90–169.

* **Objek:** Survei komprehensif mengenai teknologi, komponen, dan arsitektur *Spoken Dialogue Systems* (SDS) / *Conversational User Interface*.

* **Metode:**
* Mengklasifikasikan sistem dialog ke dalam 3 jenis strategi pengontrolan (*dialogue control strategies*):
1. *Finite State-based:* Dialog kaku berbasis alur grafik terstruktur.

2. *Frame-based:* Dialog berbasis pengisian slot (*form-filling*) yang lebih fleksibel.

3. *Agent-based:* Dialog kompleks ber-agen (BDI, *rational agency*, *theorem proving*).

* Menguraikan *pipeline* komponen SDS: ASR (*Speech Recognition*), NLU (*Language Understanding*), *Dialogue Manager*, *External Communication* (DB/KB), *Response Generation*, dan TTS (*Speech Synthesis*).

* **Hasil Kunci:**
* Sistem *Finite State* sangat mudah dibuat tetapi sangat kaku dan rentan gagal jika pengguna menyimpang dari alur.

* Sistem *Frame-based* (seperti Philips Train System) berhasil mendukung *multiple slot filling* dan verifikasi implisit.

* Sistem *Agent-based* (seperti TRAINS dan Circuit-Fix-It Shop) mampu menangani *mixed-initiative dialogue* dan *collaborative problem solving*.

* Menekankan pentingnya strategi verifikasi (*explicit* vs *implicit confirmation*) dan pengawasan kesalahan (*error recovery*).

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Rujukan survei *landmark* paling otoritatif untuk taksonomi arsitektur *Conversational AI* dan *Dialogue Management* tradisional sebelum era LLM.

* **Relevansi & Penempatan di Skripsi:** Dikutip pada **Sub-bab 2.1.1 (Pendekatan pada Chatbot Akademik Perguruan Tinggi)** untuk mempertegas evolusi arsitektur *Dialogue Management*: *Finite-State* $\rightarrow$ *Frame-based/Intent NLU* $\rightarrow$ *Agent-based* $\rightarrow$ *Generative LLM & RAG*.

---

### Bagian 11: Paper #69 – #72 (Metodologi DSRM & Framework Evaluasi Chatbot)

#### 69. Peffers, Tuunanen, Rothenberger, & Chatterjee (2007)

* **Sitasi Lengkap:** Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A Design Science Research Methodology for Information Systems Research. *Journal of Management Information Systems*, 24(3), 45–77.

* **Objek / Fokus:** Pengusulan kerangka kerja metodologi *Design Science Research Methodology* (DSRM) yang rinci, konsisten, dan terstruktur untuk memandu serta mengevaluasi penelitian berbasis perancangan artefak di disiplin Sistem Informasi (SI).

* **Metode / Kerangka Kerja Kunci:**
* **Kerangka Kerja 6 Tahap DSRM (Nominal Process Model):**
1. **Problem Identification and Motivation:** Mendefinisikan masalah spesifik dan membenarkan pentingnya nilai solusi.

2. **Define Objectives for a Solution:** Menurunkan tujuan kuantitatif/kualitatif solusi dari spesifikasi masalah dan batas kelayakan.

3. **Design and Development:** Menciptakan artefak (dapat berupa *constructs, models, methods, instantiations*, atau properti baru dari sumber daya teknis/sosial).

4. **Demonstration:** Menunjukkan kemampuan artefak dalam menyelesaikan masalah melalui eksperimen, simulasi, *case study*, atau *proof of concept*.

5. **Evaluation:** Mengukur dan mengobservasi sejauh mana artefak mendukung penyelesaian masalah dibandingkan tujuan di Tahap 2, menggunakan metrik empiris/logis yang relevan.

6. **Communication:** Mengkomunikasikan masalah, artefak, kebaruan (*novelty*), serta efektivitasnya kepada komunitas ilmiah maupun praktisi.

* **4 Titik Masuk Penelitian (*Research Entry Points*):**
* *Problem-Centered Initiation* (berawal dari observasi masalah riil/praktis).

* *Objective-Centered Solution* (berawal dari kebutuhan industri/studi yang dapat diselesaikan dengan artefak baru).

* *Design & Development-Centered Initiation* (berawal dari artefak eksisting yang ingin diterapkan pada domain baru).

* *Client/Context Initiated* (berawal dari solusi praktis di lapangan yang kemudian diberi rigor akademis).

* **Evaluasi & Demonstrasi:** DSRM dievaluasi secara retrospektif menggunakan 4 studi kasus nyata berbasis perancangan artefak SI (*CATCH Data Warehouse*, *Software Reuse Metric*, *CGUsipClient SIP-based video*, dan *Digia CSC Method*) untuk membuktikan keselarasan dan fleksibilitas model.

* **Hasil Kunci:** Menyediakan model proses nominal dan model mental standar bagi peneliti, *reviewer*, dan pembaca untuk memahami, menjalankan, dan menilai legitimasi karya ilmiah berbasis *Design Science*.

* **Relevansi & Penempatan di Skripsi Anda:**
* **Bab 3 (Metodologi Penelitian - Utama):** Menjadi **fondasi utama alur metodologi skripsi Anda**. Penelitian Anda menggunakan pendekatan ***Problem-Centered Initiation***: diawali dari masalah rendahnya akurasi/fleksibilitas chatbot akademik konvensional, diikuti perancangan prototipe RAG (LangChain + ChromaDB/BM25 + Gemini), eksperimen komparatif (Config B vs C), hingga evaluasi terukur via kerangka Ragas.

* **Bab 1 (Latar Belakang):** Dikutip untuk melegitimasi pendekatan perancangan artefak (*prototype skripsi*) sebagai metode riset ilmiah yang valid dalam Sistem Informasi/Teknik Informatika.

---

#### 70. Hevner & Chatterjee (2015)

* **Sitasi Lengkap:** Hevner, A. R., & Chatterjee, S. (2015). *Design Science Research in Information Systems*. AIS Reference Syllabi, Association for Information Systems (AIS).

* **Objek / Fokus:** Silabus referensi dan penyusunan paradigma *Design Science Research* (DSR) sebagai pendekatan pemecahan masalah (*problem-solving paradigm*) yang menciptakan artefak sosio-teknis inovatif dalam bidang Sistem Informasi.

* **Metode / Materi Kunci:**
* **Prinsip Utama DSR:** DSR berfokus pada penciptaan artefak (*constructs, models, methods, instantiations*) untuk memecahkan masalah praktis dunia nyata sekaligus memberikan kontribusi terhadap basis pengetahuan (*knowledge base*).

* **Dinamika Pengetahuan (*Knowledge Consumption & Production*):** Peneliti menyerap pengetahuan dari *knowledge base* (teori, metode eksisting) dan lingkungan aplikasi (*environment*), lalu menghasilkan pengetahuan baru melalui proses *building* dan *evaluation*.

* **Dualitas Design dalam SI:** *Design* dipandang sebagai proses iteratif (*set of activities* / kata kerja) dan sekaligus produk akhir (*artifact* / kata benda).

* **Kriteria Evaluasi Artefak:** Evaluasi harus menguji fungsionalitas, kelengkapan, konsistensi, akurasi, performa, keandalan (*reliability*), hingga utilitas (*utility*) artefak dalam lingkungan aplikasinya.

* **Hasil Kunci:** Menyajikan sintesis komprehensif mengenai bagaimana DSR menghubungkan kebutuhan lingkungan (*relevance*) dengan rigor akademis (*rigor*), serta memetakan matriks kontribusi pengetahuan (*Knowledge Contribution Matrix*).

* **Relevansi & Penempatan di Skripsi Anda:**
* **Bab 1 (Latar Belakang):** Dikutip untuk mempertegas bahwa pembuatan prototipe Chatbot RAG akademik di UNSRAT bukan sekadar pekerjaan teknis/pemrograman, melainkan sebuah riset DSR yang bertujuan memecahkan masalah layanan informasi akademik (*relevance*) sekaligus menguji hipotesis kinerja retrieval (*rigor*).

* **Bab 3 (Metodologi Penelitian) & Bab 2.2:** Mendasari klasifikasi artefak skripsi Anda sebagai sebuah ***Instantiation*** (prototipe sistem RAG jalan) serta melegitimasi perlunya pengujian kualitatif dan kuantitatif (Ragas) untuk mengukur *utility* dan *efficacy* artefak tersebut.

---

Kedua file paper yang Anda kirimkan (**Gkrimpizi et al., 2023** dan **Attigeri et al., 2024**) **berhasil dibaca dan dianalisis secara penuh**.

Berikut adalah ekstraksi terstruktur dan analisis mendalam dari kedua paper tersebut untuk melengkapi basis pengetahuan pada file `sitasi-bab2.md` serta pemetaannya pada skripsi Anda.

---

#### 71. Gkrimpizi, Peristeras, & Magnisalis (2023)

* **Sitasi Lengkap:** Gkrimpizi, T., Peristeras, V., & Magnisalis, I. (2023). Classification of Barriers to Digital Transformation in Higher Education Institutions: Systematic Literature Review. *Education Sciences*, 13(7), 746.

* **Objek / Cakupan:** Identifikasi dan klasifikasi hambatan/tantangan (*barriers*) dalam implementasi inisiatif Transformasi Digital pada Perguruan Tinggi (*Higher Education Institutions* / HEIs).

* **Metode:** *Systematic Literature Review* (SLR) mengikuti protokol PRISMA pada basis data Web of Science dan Scopus, yang menganalisis 44 studi primer (23 dari SLR + 21 dari *citation tracking* & *grey literature*).

* **Hasil Kunci:**
* Mengidentifikasi **20 hambatan spesifik** dalam transformasi digital perguruan tinggi.

* Mengelompokkan 20 hambatan tersebut ke dalam **6 kategori utama**:

1. ***Environmental***: Keterbatasan anggaran/dana (*budgetary constraints*) dan kerangka regulasi/hukum (*regulatory framework & legal issues*).

2. ***Strategic***: Kurangnya perencanaan strategis holistik, ketiadaan visi bersama, serta tidak adanya rencana aksi dan kebijakan institusional.

3. ***Organisational***: Kurangnya kelincahan (*agility*), pandangan ROI yang sempit, dan lemahnya koordinasi antar-departemen.

4. ***Technological***: Infrastruktur IT yang tidak memadai, tantangan integrasi teknologi dalam sistem pendidikan, risiko keamanan & privasi, fragmentasi data, serta kendala *legacy systems* & sistem pihak ketiga.

5. ***People (Skills & HR)***: Rendahnya literasi digital staff/mahasiswa, kurangnya kepemimpinan perubahan (*leadership for change*), keterbatasan waktu akibat beban kerja akademisi, dan layanan dukungan IT yang tidak memadai.

6. ***Cultural***: Resistensi terhadap perubahan (*resistance to change*), sikap/kepercayaan (*attitudes & beliefs*), dan budaya birokratis/konservatif.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan taksonomi hambatan transformasi digital perguruan tinggi yang sangat komprehensif (20 hambatan dalam 6 kategori).

  * **Kritik/Limitasi:**  Limitasi:** Kajian ini bersifat makro/sistemik pada tingkat institusi dan tidak mengevaluasi solusi teknis spesifik (seperti arsitektur AI/RAG) untuk mengatasi hambatan tersebut secara langsung.

* **Relevansi & Penempatan di Skripsi Anda:**
* **Bab 1 (Latar Belakang):** Sangat kuat untuk mendasari argumen latar belakang mengenai pentingnya otomatisasi layanan informasi akademik. Hambatan seperti *Data Fragmentation*, *Inadequate IT Support Service*, *Workload of Academic Staff*, dan *Lack of Agility* di perguruan tinggi melegitimasi perlunya menghadirkan chatbot berbasis RAG yang dapat beroperasi 24/7 tanpa menambah beban administratif dosen/staf.

* **Bab 2.1 / Bab 2.2:** Dikutip pada Sub-bab Konteks Adopsi TI Kampus untuk memperlihatkan dinamika lingkungan sosio-teknis tempat prototipe RAG Anda diterapkan.

---

#### 72. Attigeri, Agrawal, & Kolekar (2024)

* **Sitasi Lengkap:** Attigeri, G., Agrawal, A., & Kolekar, S. V. (2024). Advanced NLP Models for Technical University Information Chatbots: Development and Comparative Analysis. *IEEE Access*, 12, 29633–29647.

* **Objek / Cakupan:** Pengembanan dan komparasi kinerja 5 model NLP/Chatbot untuk layanan informasi dan konseling pendaftaran/akademik pada universitas teknik (memproses kueri sederhana, kompleks, hingga majemuk).

* **Metode:**
* Mengumpulkan dataset 250 pertanyaan akademik/konseling (program studi, syarat masuk, akreditasi, prospek kerja, perbedaan kurikulum).

* Mengimplementasikan dan membandingkan **5 arsitektur chatbot**:

1. ***Smart Bot***: Neural Network berbasis TensorFlow/TFLearn (*Lancaster Stemmer*, *Softmax output*, 2 *hidden layers*).

2. ***Sam***: Feed-Forward Neural Network berbasis PyTorch (*Porter Stemmer*, activation *ReLU*).

3. ***Big Mouth***: *TF-IDF Vectorization* + *Cosine Similarity*.

4. ***Hercules***: *Sequential Neural Network* (Keras/TensorFlow) dengan teknik *Dropout* (50% & 30%) dan optimizer *Adam* untuk mencegah *overfitting*.

5. ***ALICE***: *Pattern matching* berbasis *Artificial Intelligence Markup Language* (AIML).

* Diuji menggunakan *Confusion Matrix*, akurasi berbasis dataset sampel (144 kueri), serta pengujian 150 kueri percakapan langsung (*simple, complex, compound queries*, dan kueri dengan *spelling errors*).

* **Hasil Kunci:**
* **Model *Hercules* (Sequential NN + Dropout + Adam) meraih kinerja terbaik** dengan akurasi 89% pada pengujian kueri dan klasifikasi paling stabil karena berhasil mencegah *overfitting*.

* Model berbasis *Neural Network* (*Hercules*, *Smart Bot*, *Sam*) secara signifikan mengungguli model non-neural (*Big Mouth* / TF-IDF dan *ALICE* / AIML).

* Model pencocokan aturan (AIML) gagal total saat dihadapkan pada kueri yang memiliki kesalahan ejaan (*spelling mistakes*), kueri majemuk (*compound queries*), maupun kueri dengan variasi sintaksis baru.

* **Dampak & Penilaian Kritis terhadap Penelitian Anda:**
  * **Positif:** Menyediakan bukti eksperimental mutakhir (2024) mengenai perbandingan performa berbagai arsitektur NLP klasik dan Neural Network pada korpus pertanyaan akademik universitas.

  * **Kritik/Limitasi:**  Limitasi:** Meskipun *Hercules* berhasil pada intent classification, sistem ini masih terikat pada *predefined responses* (jawaban statis yang dipetakan per *intent*). Sistem ini **belum menggunakan arsitektur RAG maupun LLM Generatif**, sehingga tidak sanggup melakukan ekstraksi/sintesis jawaban bernuansa dari dokumen hukum/regulasi akademik yang panjang.

* **Relevansi & Penempatan di Skripsi Anda:**
* **Bab 2.1 (Kajian Pustaka - Sub-bab 2.1.1 & 2.1.2):** Sangat krusial sebagai *baseline* komparatif terkini (2024). Paper ini menjadi jembatan transisi metodologis yang sempurna: memperlihatkan bahwa meskipun *Sequential Neural Network* unggul dibanding AIML/TF-IDF, batas kemampuannya tetap ada pada ketergantungan *predefined responses*. Hal ini secara eksplisit menjadi **Research Gap** utama skripsi Anda untuk melompat ke arsitektur **RAG (LangChain + ChromaDB/BM25 + Gemini)**.
