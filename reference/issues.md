# 2.2.1 Chatbot dan Conversational AI

#### **[Sitasi #2: Dam et al., 2024]**

* **Teks/Klaim dalam Laporan:** "Pendekatan pra-LLM memisahkan Natural Language Understanding (NLU), Dialogue Management (DM), dan Natural Language Generation (NLG) ke dalam tiga modul independen yang bekerja berurutan. Arsitektur Transformer generatif meleburkan ketiga fungsi tersebut ke dalam satu jaringan tunggal berbasis self-attention, di mana representasi sintaksis dan semantik saling memengaruhi pada lapisan komputasinya (Dam et al., 2024)."
* **Status Validasi:** ❌ MISQUOTED / TIDAK SESUAI
* **Kutipan Asli dari Paper (PDF):**
> *"The vanilla transformer model, proposed by Vaswani et al. [74] ... is built on the encoder-decoder architecture... The GPT-series models use an autoregressive or causal decoder architecture with a one-way attention mask... Self-Attention Mechanism: $Attention(Q,K,V) = softmax(\frac{QK^T}{\sqrt{d_k}})V$"*
> 


* **Lokasi di Paper:** File 1 (Dam et al., 2024) — Halaman 6–7, Section II.B (*Large Language Models (LLMs)*).


* **Evaluasi & Analisis:** **TIDAK SESUAI (Over-attribution / Extrapolation)**. Meskipun Dam et al. membahas arsitektur Transformer dan mekanisme *self-attention* pada Section II.B, paper tersebut **TIDAK PERNAH** menguraikan pemisahan pipa kerja pra-LLM menjadi "tiga modul independen (NLU, DM, NLG) yang bekerja berurutan" maupun frasa bahwa Transformer "meleburkan ketiga modul tersebut". Konsep arsitektur modular NLU-DM-NLG merupakan teori umum *Conversational AI* (misal: McTear, 2002; Jurafsky & Martin), bukan poin/klaim asli dari paper Dam et al. (2024).


* **Rekomendasi Perbaikan:**
* Hapus rujukan `(Dam et al., 2024)` untuk klaim pemisahan 3 modul NLU-DM-NLG tersebut, lalu ganti dengan rujukan literatur klasik *dialogue systems* yang relevan.
* Jika ingin tetap merujuk ke Dam et al. (2024), sesuaikan kalimatnya agar berfokus pada apa yang benar-benar dibahas di PDF, yaitu pergeseran dari pencocokan pola (*pattern matching*) ke *autoregressive/causal decoder transformer*.

---

# 2.2.3	Information Retrieval dan Sistem Question-Answering

#### **[Sitasi #5: Robertson & Zaragoza, 2009]**

* **Teks/Klaim dalam Laporan:** "Kelemahan mendasarnya tetap pada sifat pencocokan leksikal. BM25 hanya mengenali kecocokan kata kunci secara eksak. Sinonim atau parafrase yang tidak muncul literal pada dokumen tidak akan tertangkap sebagai relevan (Robertson & Zaragoza, 2009). Fenomena vocabulary mismatch inilah yang menjadi argumen utama pembandingan terhadap pencarian semantik pada penelitian ini."
* **Status Validasi:** ❌ MISQUOTED / TIDAK SESUAI DALAM PDF
* **Kutipan Asli dari Paper (PDF):** *Istilah "vocabulary mismatch" maupun pembahasan komparatif spesifik mengenai kelemahan leksikal BM25 versus pencarian semantik (dense retrieval/semantic search) TIDAK DITEMUKAN di dalam monograf ini.*

* **Lokasi di Paper:** Tidak Ada / Tidak Ditemukan.
* **Evaluasi & Analisis:**
* Meskipun secara teori umum *Information Retrieval* (IR) pernyataan ini benar (bahwa BM25 adalah model leksikal *bag-of-words* yang tidak menangani sinonim secara langsung), **mencantumkan sitasi (Robertson & Zaragoza, 2009) pada kalimat ini adalah bentuk *misattribution* (salah atribusi sumber)**.


* Monograf Robertson & Zaragoza (2009) fokus pada landasan matematis internal PRF, BM25, dan BM25F. Penulis hanya menyebut istilah sinonim secara singkat dalam konteks *Query Expansion* (Section 3.2, hal. 351), bukan dalam kerangka kritik *"vocabulary mismatch"* terhadap pemodelan semantik modern.




* **Rekomendasi Perbaikan:**
Hapus sitasi *(Robertson & Zaragoza, 2009)* dari kalimat tersebut, dan gantikan dengan rujukan literatur klasik IR yang memang memformulasikan masalah *vocabulary mismatch* secara spesifik (misalnya: **Furnas et al., 1987** atau **Manning et al., 2008**).
*Contoh Revisi Kalimat:*
> "Kelemahan mendasar BM25 terletak pada sifat pencocokan leksikalnya yang hanya mengenali kata kunci secara eksak. Hal ini menyebabkan dokumen yang menggunakan sinonim atau parafrase dari kueri tidak tertangkap sebagai dokumen relevan, suatu fenomena yang dikenal sebagai *vocabulary mismatch* (Furnas et al., 1987; Manning et al., 2008). Permasalahan inilah yang menjadi argumen utama digunakannya pencarian semantik pada penelitian ini."



---

# 2.2.4	Pencarian Semantik (Dense Retrieval): Embedding dan Cosine Similarity

#### **[Sitasi #2: Mikolov et al., 2013]**

* **Teks/Klaim dalam Laporan:** "Akar historis representasi ini bermula dari model word embedding seperti Word2Vec, yang membuktikan bahwa aljabar vektor sederhana mampu menangkap hubungan analogi antar-kata secara linier pada ruang kontinu berdimensi tetap (Mikolov et al., 2013)."
* **Status Validasi:** ⚠️ CITE-IN-CITE / SECONDARY SOURCE
* **Kutipan Asli dari Paper (PDF):** *"Using a word offset technique where simple algebraic operations are performed on the word vectors, it was shown for example that vector("King") - vector("Man") + vector("Woman") results in a vector that is closest to the vector representation of the word Queen [20]."*

* **Lokasi di Paper:** Halaman 2, Bagian 1.1 (*Goals of the Paper*) & Bagian 4 (*Results*)


* **Evaluasi & Analisis:** Paper Mikolov et al. (2013) yang dilampirkan (*Efficient Estimation of Word Representations in Vector Space*) memang menguji hubungan aljabar linier secara komprehensif. Namun, untuk klaim penemuan awal hubungan analogi kata (*King - Man + Woman = Queen*), paper ini sebenarnya mengutip publikasi mereka sebelumnya (`[20]`: Mikolov, Yih, & Zweig, 2013, *NAACL*). Format penulisan APA 7th `(Mikolov et al., 2013)` untuk penulis berjumlah lebih dari dua sudah benar secara kaidah format.
* **Rekomendasi Perbaikan:** Jika Anda merujuk pada pengenalan arsitektur CBOW/Skip-gram dan pembuktian analoginya, sitasi ini valid. Namun jika merujuk spesifik pada penemuan fenomena analogi linier pertama kali, disarankan merujuk ke rujukan primernya: `(Mikolov, Yih, & Zweig, 2013)`.

---

#### **[Sitasi #3: Mikolov et al., 2013]**

* **Teks/Klaim dalam Laporan:** "Word2Vec menghasilkan satu vektor statis per kata dan tidak membedakan makna berdasarkan konteks kalimat. Keterbatasan itulah yang kemudian diatasi oleh representasi kontekstual berbasis arsitektur Transformer (Mikolov et al., 2013)."
* **Status Validasi:** ❌ MISQUOTED / TIDAK SESUAI (Anakronisme Faktual)
* **Kutipan Asli dari Paper (PDF):** *Tidak ditemukan dalam PDF.* Paper Mikolov et al. (2013) dipublikasikan pada tahun 2013 dan fokus pada arsitektur Word2Vec.


* **Lokasi di Paper:** N/A
* **Evaluasi & Analisis:** Terjadi **kesalahan fatal/anakronisme ilmiah**. Arsitektur Transformer baru ditemukan dan diperkenalkan oleh Vaswani et al. pada tahun 2017 (*Attention Is All You Need*), sedangkan representasi kontekstual berbasis Transformer baru dipopulerkan oleh BERT (Devlin et al., 2018). Mikolov et al. (2013) sama sekali tidak membahas Transformer maupun pemecahan masalah *static word embedding* menggunakan Transformer.


* **Rekomendasi Perbaikan:** Hapus sitasi `(Mikolov et al., 2013)` dari kalimat tersebut dan ubah rujukannya.
* *Saran Revisi Kalimat:* `"Word2Vec menghasilkan satu vektor statis per kata dan tidak membedakan makna berdasarkan konteks kalimat. Keterbatasan itulah yang kemudian diatasi oleh representasi kontekstual berbasis arsitektur Transformer (Devlin et al., 2018; Vaswani et al., 2017)."`



---

