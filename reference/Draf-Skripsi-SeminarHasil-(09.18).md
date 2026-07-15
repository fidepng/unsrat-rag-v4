Implementasi dan Evaluasi Kinerja *Chatbot* Layanan Informasi Akademik Universitas Sam Ratulangi Menggunakan Arsitektur *RETRIEVAL-AUGMENTED GENERATION* dan *Google Gemini*

PROTOTIPE

Oleh

TEOFIDE W. K. PANGEMANAN

nim: 220211060317

**![](data:image/png;base64...)**

**Universitas sam ratulangi**

**fakultas teknik**

**jurusan teknik INFORMATIKA**

**manado**

**2026**

Judul skripsi ditulis menggunakan huruf besar berukuran 14 dengan panjang tidak lebih dari 20 kata dan *kata asing* dicetak miring

[bentuk tugas akhir]

**Disusun sebagai salah satu syarat untuk memperoleh gelar Sarjana xxxxx
pada Program Studi xxxxxx di Jurusan Teknik yyyyyyyy
Fakultas Teknik Universitas Sam Ratulangi**

**Oleh**

[Nama Mahasiswa]

NIM: [NIM]

**![](data:image/png;base64...)**

**Universitas sam ratulangi**

**fakultas teknik**

**jurusan [nama jurusan]**

**manado**

**2025**

Lembar Pengesahan

|  |  |  |
| --- | --- | --- |
| Judul | : | [Judul Tugas Akhir] |
| Bentuk | : | [Bentuk Tugas Akhir] |
| Nama | : | [Nama Mahasiswa] |
| NIM | : | [NIM] |
| Program Studi | : | [Jenjang] [Nama Program Studi] |
| Jurusan | : | [Nama Jurusan] |

Menyetujui:

|  |  |
| --- | --- |
| Pembimbing I,  [Nama dan Gelar Pembimbing I]  NIP. [NIP Pembimbing I] | Pembimbing II,  [Nama dan Gelar Pembimbing II]  NIP. [NIP Pembimbing II] |

Ketua Jurusan [Nama Jurusan]

[Nama dan Gelar Ketua Jurusan]

NIP. [NIP Ketua Jurusan]

Tanggal Lulus: DD MMMM YYYY

Abstrak

Abstrak merupakan pencerminan dari isi KTIS yang mencakup, antara lain, masalah, tujuan, metode, hasil, dan kesimpulan. Isi abstrak singkat dan pada serta diketik satu spasi, maksimum satu halaman, dan diakhiri dengan minimal tigas kata kunci, diurutkan menurut abjad. Dalam *template* ini, abstrak ditulis menggunakan *style* “*Front/Backmatter*: 2. Isi,” sedangkan untuk judul bagian abstrak menggunakan *style* “*Front/Backmatter:* 1. Judul Bab Tanpa Nomor (Non-TOC).”

Kata Kunci: Abstrak, Format Penulisan, Tata Tulis Tugas Akhir

*ABSTRACT*

*Abstract in English. Use the same style, then italicize.*

# Kata Pengantar

Kata Pengantar umumnya diawali ucapan syukur, dan berisikan ucapan terima kasih kepada pihak-pihak yang berkontribusi dalam pengerjaan Tugas Akhir. Lihat contoh selengkapnya di Pedoman Penulisan KTIS. Dalam *template* ini, Kata Pengantar ditulis menggunakan *style* “*Front/Backmatter*: 2. Isi,” sedangkan untuk judul bagian Kata Pengantar menggunakan *style* “*Front/Backmatter:* 1. Judul Bab Tanpa Nomor (TOC).”

Ucapan terima kasih kepada pihak-pihak yang berkontribusi umumnya dituliskan dalam daftar berurut dengan menyebutkan peran dari yang bersangkutan. Sebagai contoh:

1. Prof. Dr. Ir. Fabian J. Manoppo, M.Agr., selaku Dekan Fakultas Teknik UNSRAT;
2. Ir. Yaulie D.Y. Rindengan, S.T., M.M., M.Sc. selaku Pembimbing I;
3. Brave A. Sugiarso, S.T., M.T., selaku Pembimbing II;
4. Ir. Alwin M. Sambul, S.T., M.Eng., Ph.D. selaku Ketua Jurusan Teknik Elektro;
5. Virginia Tulenan, S.Kom., M.TI., selaku Koordinator Program Studi S1 Teknik Informatika;
6. …dst

Penulis menyadari bahwa masih banyak terhadap kekurangan didalam penulisan ini yang disebabkan karena terbatasnya kemampuan penulis. Oleh sebab itu, segala bentuk masukan dan kritik yang membangun sangat diharapkan untuk meningkatkan kualitas tulisan ini. Semoga Tugas Akhir ini memberikan manfaat bagi banyak orang.

Manado, DD MMMM YYYY

Penulis

# Daftar Isi

[Kata Pengantar v](#_Toc233978993)

[Daftar Isi vi](#_Toc233978994)

[Daftar Tabel ix](#_Toc233978995)

[Daftar Gambar x](#_Toc233978996)

[Daftar Potongan Kode Program xi](#_Toc233978997)

[1 Bab I Pendahuluan 1](#_Toc233978998)

[1.1 Latar Belakang 1](#_Toc233978999)

[1.2 Rumusan Masalah 3](#_Toc233979000)

[1.3 Batasan Masalah 3](#_Toc233979001)

[1.4 Tujuan 5](#_Toc233979002)

[1.5 Manfaat 5](#_Toc233979003)

[1.5.1 Manfaat Teoritis 5](#_Toc233979004)

[1.5.2 Manfaat Praktis 5](#_Toc233979005)

[2 Bab II Landasan Teori 7](#_Toc233979006)

[2.1 Kajian Pustaka 7](#_Toc233979007)

[2.1.1 Pendekatan pada Chatbot Akademik Perguruan Tinggi 7](#_Toc233979008)

[2.1.2 Adopsi Large Language Models pada Layanan Informasi Berbasis Regulasi 8](#_Toc233979009)

[2.1.3 Implementasi Arsitektur Retrieval-Augmented Generation (RAG) 9](#_Toc233979010)

[2.1.4 Evaluasi Kinerja Sistem Berbasis LLM dan RAG 10](#_Toc233979011)

[2.1.5 *Research Gap* 10](#_Toc233979012)

[2.2 Dasar Teori 12](#_Toc233979013)

[2.2.1 Chatbot dan Conversational AI 12](#_Toc233979014)

[2.2.2 Information Retrieval dan Sistem Question-Answering 13](#_Toc233979015)

[2.2.3 Pencarian Leksikal BM25 13](#_Toc233979016)

[2.2.4 Vector Database dan Embedding 14](#_Toc233979017)

[2.2.5 Large Language Models (LLM) 14](#_Toc233979018)

[2.2.6 Google Gemini 15](#_Toc233979019)

[2.2.7 Retrieval-Augmented Generation (RAG) 16](#_Toc233979020)

[2.2.8 Strategi Segmentasi Dokumen (*Chunking*) 17](#_Toc233979021)

[2.2.9 Framework LangChain 17](#_Toc233979022)

[2.2.10 Framework Evaluasi Ragas 18](#_Toc233979023)

[3 Bab III Metodologi 19](#_Toc233979024)

[3.1 Jenis dan Alur Penelitian 19](#_Toc233979025)

[3.1.1 Pendekatan Design Science Research (DSR) 19](#_Toc233979026)

[3.1.2 Kerangka Kerja Penelitian 19](#_Toc233979027)

[3.2 Alat dan Bahan 21](#_Toc233979028)

[3.2.1 Spesifikasi Perangkat 21](#_Toc233979029)

[3.2.2 Korpus Data Penelitian 22](#_Toc233979030)

[3.3 Perancangan Sistem RAG 22](#_Toc233979031)

[3.3.1 Arsitektur Umum Sistem 22](#_Toc233979032)

[3.3.2 Pemrosesan Data dan *Chunking* 24](#_Toc233979033)

[3.3.3 Mekanisme *Retrieval* 26](#_Toc233979034)

[3.3.4 *Prompt Engineering* dan Generasi Respons 28](#_Toc233979035)

[3.4 Skenario Eksperimen dan Evaluasi 29](#_Toc233979036)

[3.4.1 Skenario Pengujian (Config B vs Config C) 29](#_Toc233979037)

[3.4.2 Penyusunan *Dataset Ground Truth* 30](#_Toc233979038)

[3.4.3 Metrik Evaluasi dan Operasionalisasi Ragas 30](#_Toc233979039)

[4 BAB IV Hasil dan Pembahasan 33](#_Toc233979040)

[4.1 Hasil Implementasi Sistem 33](#_Toc233979041)

[4.1.1 Statistik *Corpus* dan *Ingestion* 33](#_Toc233979042)

[4.1.2 Validasi Empiris Ukuran *Chunk* 35](#_Toc233979043)

[4.1.3 Demonstrasi Antarmuka *Prototype* 36](#_Toc233979044)

[4.2 Hasil Evaluasi Kuantitatif (jelaskan Aktivitas DSR: Evaluation) 40](#_Toc233979045)

[4.2.1 Perbandingan Metrik Ragas: Config B vs Config C 40](#_Toc233979046)

[4.2.2 Analisis Distribusi Per-*Query* 40](#_Toc233979047)

[4.2.3 Perbandingan Latensi Respons (Deskriptif) 40](#_Toc233979048)

[4.3 Analisis Kegagalan Kualitatif 40](#_Toc233979049)

[4.3.1 Pola Kegagalan Config B (RAG Semantik) 40](#_Toc233979050)

[4.3.2 Pola Kegagalan Config C (BM25 Leksikal) 40](#_Toc233979051)

[4.3.3 Komparasi Pola Kegagalan Antar Konfigurasi 40](#_Toc233979052)

[4.4 Pembahasan 40](#_Toc233979053)

[4.4.1 Interpretasi Komparatif Config B vs Config C 40](#_Toc233979054)

[4.4.2 *Trade-off* Konsumsi Token dan Latensi 40](#_Toc233979055)

[4.4.3 Implikasi Temuan untuk Sistem RAG Domain Regulasi 40](#_Toc233979056)

[5 Penutup 41](#_Toc233979057)

[5.1 Kesimpulan 41](#_Toc233979058)

[5.2 Saran 41](#_Toc233979059)

[Daftar Pustaka 42](#_Toc233979060)

[Lampiran I Judul Lampiran I 49](#_Toc233979061)

# Daftar Tabel

[Tabel 2.1 Penelitian Terkait 11](#_Toc233978986)

[Tabel 3.1 Pemetaan Aktivitas DSR Peffers et al. (2007) pada Penelitian 19](#_Toc233978987)

[Tabel 3.2 Rincian Spesifikasi Lingkungan Pengembangan 21](#_Toc233978988)

[Tabel 3.3 Parameter Variabel Kontrol Eksperimen 29](#_Toc233978989)

[Tabel 4.1 Komposisi Dokumen Korpus Penelitian 33](#_Toc233978990)

[Tabel 4.2 Ringkasan Pipeline Ingestion Config B 34](#_Toc233978991)

[Tabel 4.3 Statistik Deskriptif Panjang Section Dokumen Korpus 35](#_Toc233978992)

# Daftar Gambar

[Gambar 3.1 Bagan Alur Kerja Penelitian 20](#_Toc233978979)

[Gambar 3.2 Arsitektur Sistem 23](#_Toc233978980)

[Gambar 3.3 Diagram Alir Pipeline Ingestion 25](#_Toc233978981)

[Gambar 3.4 Diagram Alir Pipeline RAG per Request 27](#_Toc233978982)

[Gambar 3.5. Contoh bagan yang menjabarkan mengenai langkah-langkah dalam penelitian/pengerjaan tugas akhir. 32](#_Toc233978983)

[Gambar 4.1 Antarmuka Halaman Chat 38](#_Toc233978984)

[Gambar 4.2 Antarmuka Halaman Evaluasi 39](#_Toc233978985)

# Daftar Potongan Kode Program

[Potongan Kode Program 4.1 Contoh Metadata Chunk 35](#_Toc233978977)

# Bab I Pendahuluan

## Latar Belakang

Digitalisasi layanan di institusi pendidikan tinggi telah menghasilkan peningkatan volume dokumen, regulasi, dan prosedur akademik yang dapat diakses secara digital. Meskipun memberikan kemudahan distribusi, kompleksitas arsitektur teknologi informasi di perguruan tinggi yang menggunakan berbagai sistem yang tidak saling terintegrasi memicu timbulnya hambatan berupa fragmentasi data (Gkrimpizi et al., 2023). Fragmentasi terjadi ketika data tersebar di berbagai platform dan dokumen yang tidak terintegrasi, sehingga menghalangi pandangan yang komprehensif untuk penerapan solusi digital serta memicu permasalahan konsistensi dan kualitas data (Gkrimpizi et al., 2023). Akibatnya, mahasiswa harus menavigasi keseluruhan situs web atau platform secara manual untuk menemukan satu informasi spesifik, sebuah proses yang tidak efisien dan melelahkan serta sering berujung pada diskrepansi informasi yang memengaruhi pengambilan keputusan mereka (Attigeri et al., 2024; Khasanova Zafar kizi & Suh, 2025).

Tantangan aksesibilitas dan fragmentasi informasi ini turut terjadi di Universitas Sam Ratulangi (UNSRAT). Regulasi dan prosedur akademik di UNSRAT tersebar pada berbagai platform, mulai dari dokumen resmi seperti Peraturan Rektor UNSRAT Nomor 01 Tahun 2025 dan Kalender Akademik Semester Genap 2025/2026, portal INSPIRE, hingga kanal komunikasi tidak resmi antarmahasiswa. Untuk memverifikasi indikasi ini secara empiris, penulis melakukan studi pendahuluan berupa kuesioner terhadap mahasiswa aktif UNSRAT. Berdasarkan 20 responden yang terkumpul, tidak satu pun responden menyatakan tidak pernah mengalami kesulitan menelusuri aturan atau prosedur kampus, dan 70% di antaranya (14 dari 20 responden) mengaku pernah mengalami miskomunikasi, memperoleh informasi keliru, atau terlewat tenggat waktu akibat informasi yang simpang siur. Pola ini konsisten dengan kanal yang digunakan responden: meski 85% responden turut mengandalkan situs web resmi kampus sebagai salah satu sumber, lebih dari separuh (60%) tetap menempuh jalur informal seperti bertanya kepada teman, kakak tingkat, atau grup percakapan angkatan untuk memastikan kebenaran informasi, padahal tingkat kepercayaan responden terhadap kanal informal tersebut secara konsisten lebih rendah dibanding dokumen atau web resmi kampus. Temuan ini mengindikasikan kesenjangan antara kanal resmi yang tersedia dan kebutuhan mahasiswa akan kepastian informasi, sehingga mereka tetap mencari validasi dari sumber yang justru kurang mereka percaya.

Hambatan aksesibilitas informasi ini dapat diatasi melalui penerapan teknologi *Natural Language Processing* (NLP), khususnya *Large Language Models* (LLM) berbasis arsitektur Transformer oleh Vaswani et al. (2017) menawarkan jalan keluar dari hambatan aksesibilitas ini. Google Gemini (Gemini Team et al., 2025), sebagai salah satu model mutakhir yang memiliki kapabilitas penalaran logis, pemrosesan dialog kontekstual, terbukti efektif dalam memproses kueri layanan akademik berbahasa Indonesia (Muna et al., 2025). Implementasi model ini sebagai sistem informasi berbasis percakapan (*conversational information system*) membuka peluang untuk menyediakan jawaban langsung yang tervalidasi dari dokumen resmi institusi, sehingga menggeser paradigma pencarian informasi manual menjadi akses satu pintu (*single point of access*) bagi pengguna.

Meskipun memiliki kapabilitas generasi teks tingkat lanjut, LLM memiliki kerentanan struktural terhadap fenomena halusinasi (*hallucination*). (Ji, Lee, et al., 2023) mendefinisikan halusinasi sebagai kondisi di mana model menghasilkan informasi yang terdengar meyakinkan secara linguistik, namun secara substansi menyimpang dari fakta. Dalam konteks informasi akademik, halusinasi berisiko memberikan panduan yang menyesatkan terkait syarat kelulusan, tenggat waktu, atau prosedur administratif yang bersifat mengikat. Untuk mengatasi keterbatasan ini, arsitektur *Retrieval-Augmented Generation* (RAG) yang diperkenalkan oleh (Lewis et al., 2021) diimplementasikan dengan memaksa LLM untuk mengambil (*retrieve*) teks relevan dari korpus dokumen eksternal sebelum menyintesis jawaban. Mekanisme ini dirancang untuk meningkatkan keterlacakan (*groundedness*) respons terhadap sumber dokumen resmi yang diakses. Penelitian ini berfokus pada pengujian performa sistem RAG tersebut, secara khusus mengukur kinerja pendekatan pencarian semantik (*semantic search*) berbasis representasi vektor (*vector embedding*) dibandingkan dengan *baseline* pencarian leksikal (*lexical search*) konvensional berbasis algoritma BM25 pada domain dokumen berbahasa Indonesia.

Sejumlah penelitian sebelumnya telah mengembangkan *chatbot* layanan informasi akademik di Indonesia, umumnya dengan mengandalkan pendekatan berbasis aturan (*rule-based*) seperti AIML atau *framework* *Natural Language Understanding* (NLU) seperti RASA (Ajiz et al., 2023; Guntoro et al., 2020; Ruindungan & Jacobus, 2021). Perkembangan terkini menunjukkan transisi menuju adopsi LLM; sebagai contoh, integrasi model Mistral 7B dan RAG untuk domain tanaman herbal obat berbahasa Indonesia (Firdaus et al., 2024), serta penerapan *neural network* pada layanan akademik di institusi lain (M Ikhsan et al., 2025). Akan tetapi, terdapat *research gap* yang signifikan pada literatur saat ini: belum ada studi yang secara komprehensif mengevaluasi dan membandingkan kinerja sistem RAG berbasis *semantic search* dengan *baseline* leksikal pada spesifik dokumen peraturan akademik perguruan tinggi di Indonesia. Penelitian ini bertujuan untuk mengisi celah tersebut dengan mengevaluasi kedua metode pencarian menggunakan *framework* evaluasi otomatis Ragas (Es et al., 2024), sehingga menghasilkan perbandingan metrik kuantitatif yang terstandarisasi dan dapat direproduksi.

## Rumusan Masalah

Berdasarkan latar belakang yang telah dijelaskan, penelitian ini merumuskan dua pertanyaan penelitian sebagai berikut:

1. Bagaimana merancang dan mengimplementasikan *prototype chatbot* layanan informasi akademik Universitas Sam Ratulangi menggunakan arsitektur *Retrieval-Augmented Generation* (RAG) dengan *framework* LangChain dan *Large Language Model* (LLM) Google Gemini?
2. Bagaimana perbandingan kinerja antara pendekatan *vector semantic search* dibandingkan *baseline* eksperimen kontrol berbasis algoritma *lexical search* BM25 pada arsitektur RAG tersebut, diukur menggunakan *framework* evaluasi otomatis Ragas?

## Batasan Masalah

Agar penelitian lebih terarah dan dapat diukur hasilnya secara objektif, penelitian ini dibatasi oleh hal-hal berikut:

1. Sistem dibangun sebatas purwarupa penelitian (*research prototype*) yang beroperasi di lingkungan *localhost*, tanpa mencakup tahap *deployment* ke *server* publik untuk penggunaan berskala luas dan tidak diintegrasikan dengan sistem informasi akademik universitas yang telah berjalan
2. Korpus pengetahuan terbatas pada dokumen resmi tingkat universitas, yang mencakup: (a) Peraturan Rektor UNSRAT Nomor 01 Tahun 2025, (b) Kalender Akademik Semester Genap 2025/2026, dan (c) tujuh dokumen profil institusi. Sistem tidak memuat regulasi tingkat fakultas maupun data dinamis seperti jadwal perkuliahan atau pengumuman.
3. Pengujian komparatif dibatasi pada evaluasi dua metode pencarian informasi (*retrieval*), yaitu *vector semantic search* menggunakan ChromaDB dan *lexical search* menggunakan algoritma BM25 sebagai *baseline* eksperimen kontrol yang diperlukan untuk mengukur nilai tambah pendekatan RAG secara kuantitatif, dengan parameter ukuran *chunk* dokumen yang dikunci identik untuk kedua metode.
4. Evaluasi kinerja dibatasi pada empat metrik pengujian otomatis dari *framework* Ragas (*faithfulness, answer\_relevancy, context\_precision,* dan *context\_recall*) serta pengukuran latensi respons secara deskriptif. Penelitian ini tidak mencakup evaluasi *usability* antarmuka (seperti *System Usability Scale*) maupun pengujian kepuasan pengguna akhir.
5. Pengukuran latensi respons dieksekusi pada lingkungan *single-user* tanpa simulasi beban *concurrent*, sehingga data latensi yang dihasilkan ditujukan untuk perbandingan komparatif antarmetode dan tidak merepresentasikan performa sistem pada kondisi beban *multi-user*.

## Tujuan

Tujuan dari penelitian ini adalah:

1. Merancang dan mengimplementasikan *prototype chatbot* layanan informasi akademik Universitas Sam Ratulangi berbasis arsitektur *Retrieval-Augmented Generation* (RAG) menggunakan *framework* LangChain, *vector database* ChromaDB, dan *Large Language Model* (LLM) Google Gemini.
2. Mengevaluasi dan membandingkan kinerja pendekatan *vector semantic search* dengan algoritma *lexical search* BM25 menggunakan *framework* Ragas terhadap dataset *ground truth* dokumen resmi institusi.
3. Menganalisis pola kegagalan sistem (*failure analysis*) secara kualitatif beserta distribusi kinerja per kueri untuk mengidentifikasi karakteristik dari masing-masing metode *retrieval*.

## Manfaat

### Manfaat Teoritis

1. Memberikan kontribusi empiris terhadap literatur penerapan arsitektur RAG pada domain peraturan akademik berbahasa Indonesia melalui komparasi terukur antara *semantic search* dan *lexical search* menggunakan *framework* Ragas.
2. Menyediakan kerangka metodologi evaluasi sistem RAG yang mencakup klasifikasi pola kegagalan (*failure analysis*) dan analisis sebagai instrumen interpretasi bagi penelitian *prototype* *conversational* AI sejenis.
3. Memperkaya literatur penerapan kerangka kerja *Design Science Research* (DSR) dalam perancangan dan evaluasi *chatbot* institusional pada konteks pendidikan tinggi di Indonesia.

### Manfaat Praktis

1. Menghasilkan *prototype* fungsional *chatbot* sebagai *proof-of-concept* yang dapat dijadikan fondasi pengembangan sistem informasi akademik terintegrasi AI di Universitas Sam Ratulangi maupun perguruan tinggi lainnya.
2. Memberikan rekomendasi teknis berbasis data mengenai metode *retrieval* untuk pemrosesan dokumen peraturan perguruan tinggi berbahasa Indonesia, guna mendukung pengambilan keputusan bagi pengembang sistem serupa.

# Bab II Landasan Teori

## Kajian Pustaka

### Pendekatan pada Chatbot Akademik Perguruan Tinggi

Pengembangan chatbot layanan informasi akademik di perguruan tinggi Indonesia banyak menerapkan pendekatan Artificial Intelligence Markup Language (AIML) berbasis pattern matching (Ajiz et al., 2023; Guntoro et al., 2020). Pendekatan ini terbukti efisien untuk pertanyaan repetitif dan terstruktur. Penelitian di Universitas Lancang Kuning dengan basis pengetahuan akademik (seperti alamat kampus, syarat pendaftaran, langkah pendaftaran, program studi, jalur kuliah, biaya kuliah, dan cara daftar) mencapai keberhasilan fungsional 100% pada pengujian black-box dan white-box, serta kepuasan UAT 95% dari 10 responden (Guntoro et al., 2020). Studi serupa di Universitas Majalengka, yang menghimpun 10 FAQ dari hasil survei terhadap 100 responden, juga menunjukkan AIML mampu memberi jawaban akurat melalui proses tokenisasi dan pencocokan pola kata dengan aturan dalam *database* (Ajiz et al., 2023). Kelemahan mendasarnya muncul ketika masukan pengguna tidak memiliki kecocokan leksikal persis dengan *template* basis data, sistem gagal memproses dan hanya mengembalikan jawaban default atau mengarahkan pertanyaan ke administrator (Ajiz et al., 2023; Guntoro et al., 2020).

Pergeseran ke kerangka *Natural Language Understanding* (NLU) khususnya Rasa Framework meningkatkan kemampuan sistem mengenali maksud pengguna dari variasi kalimat. Pada implementasinya, *chatbot* LIANA yang dilatih dengan 188 sampel kalimat dan 12 jenis *intent* mencatatkan performa NLU rata-rata tertimbang (*precision, recall, F1-Score*) sebesar 0,995 (Ruindungan & Jacobus, 2021). Hasil serupa dicapai *chatbot* mahasiswa di Politeknik Negeri Bali dengan *precision* 0,955, *recall* 0,962, *F1-Score* 0,962 pada evaluasi NLU, serta akurasi model dialog sebesar 0,82 (Suasnawa et al., 2022). Kerangka kerja ini juga terintegrasi dengan API *platform* *chatting*, studi di Universitas Esa Unggul mencatat *chatbot* Telegram berbasis RASA berhasil diintegrasikan dan mampu merespons 24 topik pertanyaan akademik guna menyediakan layanan informasi akademik 24 jam penuh (Hidayat et al., 2024).

Meski performa NLU tinggi, subsistem manajemen dialog (seperti pada Rasa Core) memiliki karakteristik pemodelan karena basis pengetahuannya terstruktur: pengembang harus memetakan dialog dan respons secara manual ke berkas konfigurasi seperti *rules.yml* dan *stories.yml* (Hidayat et al., 2024; Suasnawa et al., 2022). Studi yang melatih 31 sampel dialog mencatat akurasi prediksi respons model dialog sebesar 0,70, *recall* 0,72, dan F1-Score 0,70 (Ruindungan & Jacobus, 2021), sementara penelitian di Politeknik Negeri Bali mencatat akurasi model dialog sebesar 0,82 dengan nilai presisi 0,85 dan F1-Score 0,85 (Suasnawa et al., 2022). Ketergantungan pada pemetaan skenario tersebut menuntut pendefinisian aturan yang komprehensif agar sistem tidak rentan menghasilkan respons yang kurang sesuai. Al Fajri & Hartono (2024) mendokumentasikan bahwa *chatbot* Telegram di Universitas Stikubank mampu menyajikan jawaban dengan baik, namun rentan menampilkan jawaban acak ketika menerima masukan kata kunci acak yang berada di luar skenario *rules* yang telah didefinisikan.

### Adopsi Large Language Models pada Layanan Informasi Berbasis Regulasi

Pengembangan agen percakapan pada pendidikan tinggi di Indonesia mulai bergeser dari pendekatan berbasis aturan ke penggunaan model pembelajaran mesin yang lebih adaptif. M Ikhsan et al. (2025) merancang layanan chatbot akademik di Universitas Negeri Medan menggunakan model Sequential dari Keras melalui pendekatan SDLC dengan akurasi sekitar 70% berdasarkan pengujian *Black-Box*, sementara Priccilia & Girsang (2024) mengadaptasi GPT-2 versi Small ke bahasa Indonesia untuk tanya-jawab praktikum mahasiswa menggunakan 1.288 pasang data latih yang diaugmentasi dan mencapai skor BLEU 0,753. Transisi ini berlanjut ke pemanfaatan LLM mutakhir: Muna et al. (2025) mengembangkan chatbot layanan akademik bertenaga Google Gemini 1.5 Flash di Telkom University Purwokerto dan mengonfirmasi kapabilitas model tersebut memproses kueri administratif berbahasa Indonesia secara kontekstual dengan raihan rata-rata skor BLEU mencapai 0,88.

Ketiga studi ini memperlihatkan pola yang sama: makin canggih model generatif yang dipakai, makin baik pula kealamian responsnya tetapi persoalan keandalan faktual tidak otomatis ikut membaik. Priccilia & Girsang (2024) sendiri mencatat nilai perplexity yang tinggi pada pengujian GPT-2, yang menunjukkan kesulitan model dalam memprediksi urutan kata saat menemui data baru akibat keterbatasan ukuran dataset. Pada sistem layanan akademik yang berpijak pada regulasi tertulis dan mengikat, kelemahan semacam ini berisiko langsung pada validitas informasi yang disampaikan ke mahasiswa dan bukan sekadar isu kualitas bahasa (Ji, Yu, et al., 2023).

### Implementasi Arsitektur Retrieval-Augmented Generation (RAG)

Arsitektur RAG telah diuji pada berbagai skala infrastruktur dan varian LLM. Pratami et al. (2025) mengintegrasikan API DeepSeek-v3 dengan basis data vektor Supabase untuk mengotomatisasi IT Service Desk universitas, dengan pendekatan Chain-of-Thought prompting mencapai akurasi tertinggi 93,1% meski menambah sedikit latensi komputasi. Sistem modular ini juga mencatatkan stabilitas operasional 24/7 dengan akurasi pencarian di atas 98% serta skor *User Experience Questionnaire* (UEQ) yang memuaskan sebesar 4,5 ± 0,3. Neumann et al. (2025) menyematkan chatbot berbasis GPT-4 ke LMS Moodle untuk memandu Self-Regulated Learning dan *help-seeking behavior*, mencapai akurasi 88% dalam merespons bantuan akademik mahasiswa yang mencakup kueri administratif, diskusi konsep kuliah, hingga pembuatan soal latihan. Untuk domain berbahasa Indonesia, Firdaus et al. (2024) menerapkan RAG pada Mistral 7B untuk literatur tanaman herbal obat dan mengungguli model LLaMa2 7B pada metrik METEOR.

Ketiga studi ini menegaskan bahwa efektivitas RAG bergantung pada dua faktor teknis: keandalan mesin pencari (retriever) dan strategi pemotongan teks (chunking). Pencarian leksikal probabilistik seperti BM25 lazim dipakai sebagai baseline pembanding karena kesederhanaannya dalam mencocokkan kata (Robertson & Zaragoza, 2009), tetapi rentan gagal ketika pengguna memakai sinonim yang berbeda dari teks sumber. Kelemahan yang dapat diatasi melalui pencarian semantik berbasis representasi vektor (Reimers & Gurevych, 2019). Pada sisi chunking, Bhat et al. (2025) mengonfirmasi adanya trade-off antara presisi ekstraksi dan keutuhan konteks yang bergantung pada karakteristik dokumen, argumen inilah yang mendasari pemilihan strategi chunking pada penelitian ini.

### Evaluasi Kinerja Sistem Berbasis LLM dan RAG

Evaluasi sistem RAG generasi awal umumnya bergantung pada metrik berbasis kecocokan kata (lexical overlap) seperti Exact Match, ROUGE, dan BLEU (Lewis et al., 2021). Pendekatan ini juga dipakai Lakatos et al. (2025) saat membandingkan RAG dengan Domain-Specific Fine-Tuning, dan hasilnya konsisten menunjukkan keunggulan RAG dalam menyerap pengetahuan domain spesifik tanpa perlu pelatihan ulang model.

Meski demikian, metrik n-gram memiliki kelemahan mendasar: metrik ini rentan memberikan penalti keliru pada jawaban yang secara makna sudah benar namun berbeda susunan kata dari teks referensi (Khasanova Zafar kizi & Suh, 2025). Pergeseran menuju pendekatan LLM-as-a-Judge yang reference-free salah satunya diwakili oleh framework Ragas menjadi respons atas keterbatasan ini. Khasanova Zafar kizi & Suh (2025) memanfaatkan Ragas untuk mengevaluasi kinerja keseluruhan RAG *pipeline* pada sistem informasi penerimaan mahasiswa internasional, Sedangkan Koay et al. (2026) memakainya sebagai metrik validasi utama saat menguji metode pemotongan teks berbasis struktur (*structure-aware chunking*) yang kompleks. Kedua studi ini menjadi preseden metodologis langsung bagi pemilihan Ragas sebagai instrumen evaluasi pada penelitian ini.

### *Research Gap*

Chatbot akademik di Indonesia bergeser dari sistem berbasis *intent* seperti yang dikembangkan oleh Suasnawa et al. (2022) menuju ke arsitektur RAG berbasis LLM (Dzaki Salman & Nasution, 2026; Husain et al., 2025). Meskipun implementasi RAG berbahasa Indonesia telah mulai diterapkan, literatur menunjukkan bahwa fokus eksplorasinya mayoritas masih terbatas pada domain non-regulasi dan non-administratif, seperti tanaman herbal (Firdaus et al., 2024), dan diagnosis medis dasar (Muhammad Adrinta Abdurrazzaq et al., 2025).

Pada dokumen hukum dan regulasi, BM25 terbukti tetap kompetitif dan mampu mengimbangi *dense retrieval* yang belum di-*fine-tuning* untuk domain tersebut (Mori et al., 2025). Ragas pun sudah dipakai pada chatbot akademik Indonesia, tetapi sebatas mengaudit satu system RAG tunggal, bukan membandingkan dua metode *retrieval* secara terkontrol (Artayasa et al., 2025). Korpus peraturan akademik perguruan tinggi berbahasa Indonesia sendiri nyaris belum dijadikan objek eksperimen komparatif yang terkontrol antara metode penelusuran semantik dan leksikal.

Berdasarkan dari kekosongan itu, tugas akhir ini disusun sebagai prototipe chatbot akademik yang sekaligus melakukan uji komparatif: apakah *semantic search* berbasis ChromaDB benar-benar mengungguli *baseline* BM25 pada dokumen akademik perguruan tinggi menggunakan *framework* Ragas (Es et al., 2024). Penelitian ini disusun untuk mengisi celah tersebut pada konteks Universitas Sam Ratulangi Manado.

Tabel 2.1 Penelitian Terkait

|  |  |  |  |
| --- | --- | --- | --- |
| Referensi | Metode/Pendekatan | Domain | Hasil Utama |
| Guntoro et al. (2020); Ajiz et al. (2023) | *Rule-based*, *Artificial Intelligence Markup Language* (AIML) | Layanan informasi akademik perguruan tinggi | Keberhasilan fungsional 100%, *User Acceptance Test* 95% |
| Ruindungan & Jacobus (2021); Suasnawa et al. (2022); Al Fajri & Hartono (2024); Hidayat et al. (2024) | *Natural Language Understanding* (NLU), Rasa Framework, integrasi API Telegram | Administrasi dan FAQ mahasiswa | F1-Score hingga 0,995; akurasi prediksi respons 0,70–0,82 |
| M Ikhsan et al. (2025) | *Neural network* (*Sequential model*, Keras) | Chatbot akademik universitas | Akurasi ±70% |
| Priccilia & Girsang (2024) | GPT-2 Small (adaptasi Bahasa Indonesia) | Tanya-jawab praktikum mahasiswa | BLEU 0,753; *perplexity* tinggi |
| Muna et al. (2025) | *Generative LLM*, Google Gemini (API), Telegram Bot | Chatbot layanan akademik | BLEU 0,88 |
| Ji et al. (2023) | Tinjauan teoretis dan klasifikasi | Halusinasi pada LLM | Klasifikasi 3–8 tipe halusinasi; metode *self-reflection* |
| Robertson & Zaragoza (2009) | Algoritma probabilistik BM25 (*lexical search*) | *Information retrieval* | — |
| Reimers & Gurevych (2019) | *Sentence-BERT* (SBERT), *semantic search* | *Vector embedding* | Reduksi waktu komputasi dari 65 jam ke 5 detik |
| Lewis et al. (2021) | *Retrieval-Augmented Generation* (RAG) | Tugas NLP berbasis pengetahuan | Exact Match, BLEU, ROUGE |
| Neumann et al. (2025); Firdaus et al. (2024) | RAG (GPT-4; Mistral 7B) | LMS kampus; chatbot tanaman medis | Akurasi faktual 88%; METEOR 0,22 |
| Pratami et al. (2025) | RAG, API DeepSeek-v3, Supabase, *Chain-of-Thought* | *IT Service Desk* universitas | Akurasi *retrieval* >98%; akurasi CoT 93,1%; latensi 2,1 detik |
| Lakatos et al. (2025) | Komparasi RAG vs *Domain-Specific Fine-Tuning* | Sistem berbasis pengetahuan | ROUGE, BLEU, *Coverage Score* |
| Khasanova Zafar kizi & Suh (2025) | Ragas Framework, *semantic chunking* | Chatbot penerimaan mahasiswa internasional | Answer Relevancy 0,80; Faithfulness 0,86 |
| Bhat et al. (2025) | Analisis komparatif *chunk size* (64–1024 token) | *Long-document retrieval* | Trade-off presisi ekstraksi vs. keutuhan konteks |
| Koay et al. (2026) | Ragas Framework, *structure-aware chunking* | Ekstraksi tabel dokumen akademik | Content Precision 0,92; Content Relevance 0,93 |

## Dasar Teori

### *Chatbot* dan *Conversational* AI

Secara konseptual, *chatbot* merujuk pada perangkat lunak yang menyimulasikan interaksi manusia melalui antarmuka digital dengan menggunakan bahasa alami (Abu Shawar & Atwell, 2007). Dalam perkembangannya, teknologi ini mengalami transisi dari era pra-LLM (yang mencakup *chatbot* berbasis aturan pencocokan pola sederhana dan asisten suara pintar) menuju era *Conversational* AI berbasis LLM yang mampu memahami konteks dialog secara mendalam (Dam et al., 2024).

Perbedaan mendasar antargenerasi ini terletak pada arsitektur pemrosesannya. Pendekatan konvensional memisahkan tugas ke dalam modul-modul *independent*, mulai dari *Natural Language Understanding* (NLU), Dialog Management (DM), dan Natural Language Generation (NLG) yang bekerja secara berurutan (Kulkarni et al., 2019). Era Generative AI meleburkan seluruh fungsi ini ke dalam satu arsitektur jaringan saraf terpadu, di mana elemen struktural sintaksis dan semantik saling memengaruhi secara erat melalui mekanisme *self-attention* (Orrù et al., 2025). Peleburan fungsional ini memungkinkan penciptaan *chatbot* yang sangat sensitif terhadap konteks percakapan guna menghasilkan interaksi yang lebih natural (Vadlamani & Borada, 2025). Meskipun demikian, pemanfaatan model bahasa generatif berskala besar pada domain spesifik yang menuntut akurasi informasi tinggi tetap menghadapi tantangan berupa kerentanan struktural terhadap halusinasi faktual, yang menghasilkan jawaban salah namun meyakinkan (Dam et al., 2024).

### Information Retrieval dan Sistem Question-Answering

Pencarian data tidak terstruktur dari koleksi dokumen berskala besar untuk memenuhi kebutuhan informasi spesifik adalah domain kajian Information Retrieval (IR) (Manning et al., 2008). Perkembangannya mengarah pada sistem Question-Answering (QA) modern, yang tidak lagi sekadar mengembalikan daftar dokumen relevan melainkan menyintesis jawaban langsung dalam bahasa alami. Arsitektur seperti DrQA (Chen et al., 2017) menandai transisi ini dengan menggabungkan penelusuran dokumen klasikal (berbasis TF-IDF dan pencocokan n-gram) dengan pemahaman teks (*machine comprehension*) berbasis jaringan saraf tiruan (*recurrent neural network*) (Jurafsky & Martin, 2026).

Sistem QA berbasis dokumen konvensional ini bekerja secara ekstraktif dengan mendeteksi potongan teks jawaban langsung dari dokumen rujukan (Chen et al., 2017). Dalam perkembangannya, pendekatan ekstraktif tersebut kini bertransisi menjadi sistem QA berbasis dokumen modern yang direpresentasikan oleh arsitektur *Retrieval-Augmented Generation* (RAG) (Jurafsky & Martin, 2026). Pada arsitektur RAG, proses ekstraksi teks telah digantikan oleh kemampuan generatif LLM untuk menyintesis jawaban.

### Pencarian Leksikal BM25

BM25 (*Best Match* 25) merupakan formulasi praktis dari *Probabilistic Relevance Framework* (PRF) yang didasarkan pada prinsip pemeringkatan probabilitas (*Probability Ranking Principle*) (Robertson & Zaragoza, 2009). Algoritma ini menjadi algoritma pemeringkatan probabilistik yang lazim dipakai sebagai *baseline* kontrol dalam penelitian IR karena konsistensi kinerjanya untuk pencarian berbasis kata kunci (Al-Joofi et al., 2026; Robertson & Zaragoza, 2009). Fungsi pemeringkatan BM25 terhadap sebuah dokumen untuk kueri yang terdiri dari *term* dirumuskan sebagai berikut (Kang et al., 2023):

Di mana menyatakan frekuensi kemunculan term di dalam dokumen, adalah panjang dokumen, dan merupakan rata-rata panjang dokumen dalam seluruh koleksi (Kang et al., 2023). Formula ini dikontrol oleh dua parameter penting: parameter yang meregulasi skala saturasi frekuensi kata pada dokumen, serta parameter (berkisar antara 0 hingga 1) yang mengontrol derajat normalisasi panjang dokumen (Robertson & Zaragoza, 2009). Keterbatasan utama *lexical search* seperti BM25 adalah ketergantungannya pada pencocokan kata kunci secara eksak (*exact matching*). Hal ini mengakibatkan algoritma rentan terhadap *lexical mismatch* atau *term mismatch*, yaitu kegagalan sistem dalam mengenali dokumen relevan jika pengguna menggunakan sinonim atau diksi yang berbeda dari teks sumber sehingga melewatkan informasi yang berhubungan secara konseptual (Kang et al., 2023; Lee et al., 2024).

### *Vector Database* dan *Embedding*

*Vector database* adalah sistem penyimpanan yang dirancang secara khusus untuk mengelola representasi teks dalam bentuk vektor numerik berdimensi tinggi (*dense embeddings*). Tingkat kemiripan arah makna antar-vektor diukur melalui *cosine similarity*, yaitu nilai kosinus dari sudut antara dua vektor yang menentukan derajat kemiripannya (Manning et al., 2008). Meskipun pada model ruang vektor klasik formula ini diterapkan pada representasi leksikal jarang (sparse vectors) seperti tf-idf, prinsip geometris tersebut tetap diadopsi pada representasi padat modern. Pendekatan ini memungkinkan pencarian dokumen berdasarkan pemahaman konteks, bukan sekadar pencocokan karakter, dan berfungsi sebagai penyimpanan persisten yang memfasilitasi *similarity search* vektor secara efisien dalam arsitektur RAG, sebagaimana diimplementasikan lewat integrasi basis data vektor Supabase dan model embedding MiniLM-L6-v2 (Pratami et al., 2025).

### Large Language Models (LLM)

*Large Language Models* (LLM) adalah model *neural network* berparameter masif. Kemampuan LLM menyintesis bahasa manusia secara kontekstual bersumber dari proses pre-training pada tugas seperti masked language modeling dan prediksi kata secara autoregresif atas korpus teks berskala masif (Y. Yao et al., 2024). Fondasi arsitekturalnya adalah Transformer (Vaswani et al., 2017), yang menggantikan pemrosesan sekuensial pada RNN dan LSTM dengan mekanisme self-attention yang memungkinkan seluruh token dalam satu sekuens diproses paralel sekaligus menangkap dependensi makna jarak jauh secara lebih efisien.

Kapabilitas ini datang dengan dua keterbatasan. Pertama, pengetahuan model terkunci pada data hingga waktu pelatihan (*parametric memory*) dan tidak otomatis mengikuti perubahan informasi terkini. Kedua, model rentan terhadap halusinasi (*hallucination*) yaitu kondisi ketika *output* terdengar meyakinkan secara linguistik namun menyimpang dari fakta (Ji, Yu, et al., 2023). Zhang et al. (2025) mengklasifikasikan halusinasi ke dalam tiga kategori: *input-conflicting* (bertentangan dengan masukan pengguna), *context-conflicting* (bertentangan dengan informasi yang dihasilkan oleh model itu sendiri sebelumnya), dan *fact-conflicting hallucination* (bertentangan dengan fakta dunia nyata). Pada sistem yang berpijak pada kepatuhan regulasi seperti layanan akademik, kecenderungan model merekayasa jawaban faktual bukan sekadar cacat kualitas, melainkan risiko yang mengikat secara administratif. Karena menghilangkan halusinasi sepenuhnya sulit dicapai tanpa mengorbankan performa generatif model (Sun et al., 2024), upaya mitigasi yang berkembang saat ini berfokus pada menekan dampaknya, salah satunya melalui arsitektur RAG (C. Yao & Fujita, 2024; Zhang et al., 2025).

### Google Gemini

Google Gemini merupakan keluarga model AI multimodal berbasis Transformer yang mampu memproses dan menyintesis teks, gambar, audio, dan video sekaligus (Gemini Team et al., 2025). Di antara variannya, Flash banyak diterapkan dalam sistem percakapan *real-time* karena kemampuan generatifnya yang tinggi serta efisiensi waktu responsnya (Muna et al., 2025), pertimbangan yang relevan untuk sistem percakapan real-time seperti pada penelitian ini.

Dalam arsitektur RAG, efektivitas Gemini sebagai generator jawaban akhir sangat dipengaruhi oleh strategi segmentasi dokumen (*chunking*) yang digunakan; batas segmentasi yang adaptif terbukti krusial dalam menyajikan informasi prosedural yang utuh dan akurat (Gomez-Cabello et al., 2025). Muna et al. (2025) membuktikan model ini mampu memproses interaksi administratif mahasiswa berbahasa Indonesia secara konsisten, sebuah preseden empiris yang mendasari pemilihannya pada penelitian ini.

### *Retrieval-Augmented Generation* (RAG)

*Retrieval-Augmented Generation* (RAG) adalah arsitektur yang mengintegrasikan kemampuan generasi teks model bahasa dengan mekanisme pencarian informasi dari basis data eksternal. Lewis et al. (2021) memperkenalkan RAG sebagai jawaban atas ketergantungan LLM pada memori parametrik yaitu pengetahuan yang terkunci pada bobot model sejak masa pelatihan. Dengan menyambungkan model bahasa ke basis data eksternal (non-parametric memory) yang bersifat *human-readable* dan *human-writable*, RAG memungkinkan sistem mengambil informasi yang dinamis dan dapat diverifikasi. Keunggulan utama ini membuatnya lebih sesuai dibanding fine-tuning untuk domain dengan kebutuhan pembaruan data konstan dan akurasi faktual presisi, mengingat LLM terbukti kesulitan mempelajari fakta baru melalui *unsupervised fine-tuning* (Ovadia et al., 2024), dan integrasi *fine-tuning* dengan RAG justru berisiko menurunkan kemampuan atensi model dalam memahami konteks (Lakatos et al., 2025)**.**

Secara operasional, pada paradigma *Naive* RAG, sistem berjalan melalui tiga tahap sekuensial (Gao et al., 2024). Pada indexing, korpus dokumen dipotong menjadi chunk, diubah menjadi representasi vektor (embedding), lalu disimpan ke basis data. Pada retrieval, kueri pengguna diubah menjadi vektor untuk memindai dan menarik chunk dengan kedekatan semantik tertinggi. Pada generation, chunk yang berhasil ditarik digabungkan dengan kueri asli sebagai landasan faktual yang membatasi ruang sintesis model. Meskipun terdapat temuan paradoks bahwa keberadaan *noise* atau dokumen tidak relevan pada posisi tertentu kadang kala dapat meningkatkan kemampuan penalaran LLM (Sharma, 2025), eliminasi *noise* yang tidak terkendali tetap menjadi tantangan utama. Oleh karena itu kontrol pada tahap pencarian, seperti penerapan ambang batas kemiripan (similarity threshold), menjadi instrumen krusial untuk memastikan LLM hanya memproses konteks yang relevan (Gao et al., 2024; Lakatos et al., 2025).

### Strategi Segmentasi Dokumen (*Chunking*)

Chunking menentukan langsung kualitas dan relevansi konteks yang ditarik oleh sistem pencari dalam arsitektur RAG. Ukuran potongan teks membawa trade-off yang inheren: potongan kecil memberi presisi ekstraksi fakta tinggi karena meminimalkan noise, sementara potongan besar lebih unggul mempertahankan pemahaman konteks yang komprehensif (Bhat et al., 2025). Efektivitas ukuran chunk ini juga sangat sensitif terhadap arsitektur model *embedding* yang digunakan (Bhat et al., 2025). Keseimbangan ini berdampak langsung pada akurasi jawaban akhir serta efisiensi performa keseluruhan *pipeline* RAG (Gomez-Cabello et al., 2025; Sharma, 2025).

Dua kategori segmentasi lazim digunakan. Pertama, pemotongan ukuran tetap (fixed-size chunking) membagi teks secara mekanis berdasarkan kuota karakter atau token (Koay et al., 2026); pendekatannya efisien secara komputasi tetapi sering memotong kalimat tepat di tengah gagasan pokok. Kedua, pemotongan struktural (structural chunking) mengandalkan batas logis bawaan dokumen seperti tipe elemen dokumen (Yepes et al., 2024) atau struktur tabel kompleks (Koay et al., 2026). Pendekatan ini terbukti secara konsisten meningkatkan akurasi *retrieval* serta koherensi semantik dibanding pemotongan kaku (Koay et al., 2026; Yepes et al., 2024).

Pada dokumen legal atau regulasi, di mana ikatan logis antar-ayat dan pasal tidak dapat dipisahkan, pemotongan ukuran tetap terbukti memutus koneksi hierarkis sehingga menghilangkan makna kontekstualnya(Reuter et al., 2025). Batas pemotongan karenanya perlu dipertahankan pada unit struktural yang utuh agar satu klausul atau pasal tidak kehilangan maknanya (Beauchemin et al., 2024).

### *Framework* LangChain

LangChain adalah open-source framework untuk pengembangan aplikasi berbasis LLM yang memfasilitasi alur kerja model bahasa agar modular, *composable*, dan *extensible* (Bang et al., 2026). Desain ini menyederhanakan siklus pengembangan pipeline yang kompleks serta memungkinkan penggabungan atau substitusi komponen pencarian (*retrieval*) dan pengurutan ulang (*re-ranking*) secara fleksibel (Bhat et al., 2025). Dalam penelitian sebelumnya, pustaka LangChain terbukti andal digunakan untuk mendukung proses *preprocessing* dokumen data secara terstruktur (Firdaus et al., 2024). Sifat modularnya memungkinkan penggantian retriever pada tahap evaluasi tanpa mengubah keseluruhan struktur kode.

### *Framework* Evaluasi Ragas

Ragas adalah *automated evaluation framework* yang dirancang untuk mengukur kinerja sistem RAG melalui pendekatan LLM-as-a-Judge: sebuah model bahasa ditugaskan sebagai asesor objektif untuk menilai berbagai dimensi kualitas tanpa bergantung pada ketersediaan anotasi rujukan manusia (ground truth) (Es et al., 2024; Sharma, 2025). Pendekatan evaluasi *reference-free* ini sangat krusial karena dalam skenario dunia nyata, *dataset* berlabel sering kali sulit diakses (Es et al., 2024). Pendekatan ini menggantikan atau melengkapi metrik tradisional berbasis n-gram (BLEU, Exact Match) yang rentan memberi penalti keliru pada variasi kalimat yang maknanya sudah tepat, sebagaimana dibuktikan secara empiris di mana skor RAGAS yang tinggi sering kali berlawanan dengan rendahnya skor BLEU/ROUGE akibat perbedaan parafrase semata (Khasanova Zafar kizi & Suh, 2025).

*Framework* Ragas awalnya memperkenalkan tiga metrik utama untuk mengevaluasi kualitas RAG (Es et al., 2024), yang kemudian dalam perkembangannya di berbagai riset optimasi diperluas menjadi beberapa metrik tambahan (Koay et al., 2026). Metrik-metrik tersebut meliputi:

1. *Faithfulness*: Mengukur tingkat konsistensi faktual (bebas halusinasi) antara jawaban LLM dengan dokumen konteks yang ditarik.
2. *Answer Relevancy*: Mengevaluasi sejauh mana jawaban yang dihasilkan relevan dan menjawab esensi kueri pengguna.
3. *Context Precision*: Mengukur akurasi pemeringkatan *retriever* dalam menempatkan potongan dokumen yang paling relevan pada urutan teratas.
4. *Context Recall*: Menilai tingkat kelengkapan informasi pencarian dengan memastikan seluruh fakta *ground truth* berhasil ditarik sistem.

# Bab III Metodologi

## Jenis dan Alur Penelitian

### Pendekatan Design Science Research (DSR)

Penelitian ini menggunakan kerangka *Design Science Research* (DSR) sebagai pendekatan metodologi utama. DSR dipilih karena berfokus pada perancangan dan evaluasi artefak teknologi informasi untuk menyelesaikan permasalahan operasional yang praktis (Hevner & Chatterjee, 2010). Dalam penelitian ini, artefak yang dikembangkan berupa *prototype* *chatbot* layanan informasi akademik menggunakan arsitektur *Retrieval-Augmented Generation* (RAG).

Tahapan penelitian mengadopsi enam aktivitas DSR yang diusulkan oleh Peffers et al. (2007). Pemetaan aktivitas tersebut terhadap alur penyelesaian masalah pada penelitian ini diuraikan pada Tabel 3.1.

Tabel 3.1 Pemetaan Aktivitas DSR Peffers et al. (2007) pada Penelitian

|  |  |  |
| --- | --- | --- |
| AKTIVITAS DSR | DESKRIPSI UMUM | MANIFESTASI DALAM PENELITIAN INI |
| *Problem Identification & Motivation* | Mendefinisikan masalah yang akan diselesaikan. | Identifikasi masalah fragmentasi informasi akademik UNSRAT dan keterbatasan halusinasi pada model LLM murni. |
| *Definition of Objectives of a Solution* | Menetapkan tujuan solusi secara spesifik dan terukur. | Penetapan tiga tujuan penelitian teknis terkait performa *retrieval* dan akurasi jawaban sistem. |
| *Design & Development* | Merancang dan membangun artefak pendukung. | Perancangan arsitektur RAG, *pipeline ingestion*, dan mekanisme *retrieval* pada dua konfigurasi sistem (vektor vs BM25). |
| *Demonstration* | Mendemonstrasikan artefak dalam menyelesaikan masalah. | Uji coba sistem berjalan, pengujian fungsionalitas antarmuka, dan validasi *chunking* dokumen. |
| *Evaluation* | Mengukur kinerja artefak terhadap tujuan penelitian. | Evaluasi performa menggunakan metrik *Ragas* dan perbandingan latensi respons. |
| *Communication* | Menyebarluaskan temuan penelitian. | Penyusunan laporan akhir dan dokumentasi. |

### Kerangka Kerja Penelitian

Alur kerja penelitian digambarkan melalui kerangka pikir yang menghubungkan tahap identifikasi akar masalah, perancangan solusi teknis, hingga tahap evaluasi akhir. Gambar 3.1 menyajikan bagan alir yang menjadi pedoman pelaksanaan penelitian ini.

![](data:image/png;base64...)

Gambar 3.1 Bagan Alur Kerja Penelitian

Secara umum, setelah tahap identifikasi masalah, alur penelitian ini terbagi melalui dua jalur utama:

1. Jalur Rekayasa: Rangkaian tahap teknis yang berfokus pada pengumpulan dan pra-pemrosesan korpus dokumen akademik UNSRAT, dilanjutkan dengan pembangunan artefak sistem. Pada tahap ini, dikembangkan dua konfigurasi sistem: Config B (Sistem Utama) yang menggunakan pendekatan pencarian semantik (*vector search*), dan Config C (*Baseline*) yang menggunakan pencarian leksikal (BM25).
2. Jalur Evaluasi: Rangkaian tahap pengujian untuk membandingkan kinerja kedua konfigurasi (Config B dan Config C). Jalur ini mencakup pelaksanaan eksperimen komparatif yang terkontrol, pengukuran metrik evaluasi menggunakan *framework* Ragas, serta analisis pola kegagalan untuk menarik simpulan akhir dan menghasilkan *prototype* yang fungsional.

## Alat dan Bahan

### Spesifikasi Perangkat

Implementasi dan pengujian *prototype* pada penelitian ini dilakukan pada satu lingkungan komputasi tunggal. Proses komputasi berat seperti inferensi LLM dan model *embedding* dieksekusi menggunakan *Application Programming Interface* (API) berbasis *cloud.* Rincian spesifikasi lingkungan pengembangan ditunjukkan pada Tabel 3.2.

Tabel 3.2 Rincian Spesifikasi Lingkungan Pengembangan

|  |  |  |
| --- | --- | --- |
| KATEGORI | ITEM | KONFIGURASI / DESKRIPSI |
| *Hardware* | CPU | AMD Ryzen 5 5600H @ 3.30 GHz |
|  | GPU | NVIDIA RTX 3050 Laptop (Catatan: Inferensi dilakukan melalui API cloud, tidak menggunakan GPU lokal) |
|  | RAM | 16 GB |
|  | OS | Windows 11 Home 64-bit |
| Lingkungan Pemrograman | Python | Python 3.11  (Conda environment: unsrat-rag) |
|  | *Package Manager* | Conda (Miniconda) |
|  | *Libraries* | LangChain (langchain-google-genai, langchain-chroma), ChromaDB, FastAPI, Uvicorn, Ragas, rank-bm25, pandas, PyYAML. UI: Chart.js, Tailwind CSS. |
|  | *Frontend* | HTML/CSS/JavaScript vanilla, Chart.js 4.x, Tailwind CSS 3.x, Marked.js, Lucide Icons |
|  | IDE & VCS | Visual Studio Code, Git |
| Model | Model *Generator* | gemini-3.5-flash (Google AI Studio API) |
|  | Model *Evaluator* | gemini-2.5-flash (Google AI Studio API) |
|  | Model *Embedding* | gemini-embedding-001 (Google AI Studio API) |
| Infrastruktur Data | *Vector DB* | ChromaDB 0.5.0 (*Config B*) |
|  | Indeks Leksikal | BM25Okapi / rank-bm25 (*Config C*) |
| *Retriever* | top-*k* | 4 |
|  | *Similarity Threshold* | 0.3 (Khusus untuk *Config B*) |

### Korpus Data Penelitian

Korpus penelitian ini dibatasi pada tiga jenis dokumen resmi tingkat universitas: (a) Peraturan Rektor UNSRAT Nomor 01 Tahun 2025, (b) Kalender Akademik Semester Genap 2025/2026, dan (c) tujuh dokumen profil institusi. Seluruh dokumen diperoleh dari situs resmi institusi (unsrat.ac.id) pada periode Mei-Juni 2026. Keputusan untuk membatasi korpus pada dokumen tingkat universitas, bukan per-fakultas bukan semata-mata keterbatasan teknis, melainkan pilihan metodologis yang disengaja. Cakupan yang lebih luas tanpa batas yang jelas akan mempersulit verifikasi kebenaran jawaban sistem selama evaluasi.

## Perancangan Sistem RAG

### Arsitektur Umum Sistem

Sistem *chatbot* informasi akademik dirancang ke dalam lima lapisan fungsional yang saling terintegrasi: lapisan korpus, *pipeline ingestion*, *pipeline retrieval* dan *chain*, *backend*, serta *frontend*. Arsitektur sistem secara keseluruhan ditunjukkan pada Gambar 3.2.

![](data:image/png;base64...)

Gambar 3.2 Arsitektur Sistem

Dua pipeline terpisah menjadi inti sistem ini. *Pipeline ingestion* berjalan satu kali untuk memproses dokumen mentah menjadi indeks basis data, sedangkan *pipeline retrieval* dan *chain* berjalan pada setiap permintaan pengguna. Pemisahan ini menempatkan proses yang berat secara komputasi (*embedding* seluruh korpus) di luar jalur respons *real-time*, sehingga waktu tanggap sistem terhadap pertanyaan pengguna tidak terbebani oleh proses *indexing*.

Pada sisi *backend*, sistem menggunakan *framework* FastAPI untuk melayani dua *endpoint* utama: /api/chat untuk layanan percakapan dan /api/evaluation untuk evaluasi. Respons dari LLM dikirimkan ke *frontend* secara bertahap (token per token) menggunakan mekanisme *Server-Sent Events* (SSE) dengan empat tipe status: *thinking*, *token*, *citations*, dan *done*. Mekanisme streaming ini dipilih agar pengguna melihat jawaban mulai muncul tanpa menunggu seluruh respons selesai dihasilkan.

### Pemrosesan Data dan *Chunking*

Langkah pertama dalam perancangan *pipeline ingestion* adalah mengonversi dokumen PDF menjadi format Markdown (.md) secara manual. Pendekatan konversi manual ini dipilih untuk meminimalisasi artefak teks yang sering muncul pada alat konversi otomatis (seperti spasi ganda atau pemenggalan kata yang salah) serta memastikan hierarki teks seperti Bab, Bagian, dan Pasal tertandai dengan benar menggunakan format *heading* Markdown (#, ##, ###, ####). Setiap dokumen juga dilengkapi dengan metadata YAML *frontmatter* yang memuat identitas dokumen (doc\_id), judul (title), dan kategori (category).

Pemecahan dokumen menjadi potongan teks (*chunk*) diimplementasikan menggunakan strategi pemisahan hibrida dua tahap (*two-stage hybrid chunking*). Diagram alir proses ini dapat dilihat pada Gambar 3.3.

![](data:image/png;base64...)

Gambar 3.3 Diagram Alir Pipeline Ingestion

1. Tahap 1 (*Structural Split*): Dokumen dipotong berdasarkan batas logis *heading* *Markdown* menggunakan MarkdownHeaderTextSplitter. Tujuannya adalah agar satu unit informasi utuh (misalnya satu pasal peraturan) tidak terpotong di tengah kalimat dan tersebar ke dua *chunk* berbeda.
2. Tahap 2 (*Size Normalization*): Potongan dari Tahap 1 yang ukurannya melebihi batas akan dinormalisasi menggunakan RecursiveCharacterTextSplitter.

Parameter yang digunakan adalah chunk\_size=2000 karakter dengan chunk\_overlap=200 karakter, merujuk pada dukungan literatur bahwa pemotongan berbasis elemen dokumen hingga sekitar 2.000 karakter secara konsisten meningkatkan akurasi *retrieval* dan tanya-jawab (Yepes et al., 2024), sekaligus mempertahankan integritas hierarki dokumen regulasi sebagaimana dibahas pada Sub-sub-bab 2.2.8. Kombinasi strategi pemisahan dua tahap ini memastikan struktur logis tetap terjaga, sementara batas 2000 karakter memberi ruang cukup agar kalimat dalam satu unit informasi yang saling bergantung tidak terpotong saat diindeks.

### Mekanisme *Retrieval*

Sistem dirancang untuk menguji dua mekanisme *retrieval* (pencarian) yang berbeda. Kedua konfigurasi ini menggunakan ukuran *chunk* yang identik sehingga variabel yang dibandingkan murni pada teknik pencariannya saja. Diagram alir proses pencarian *per-request* diilustrasikan pada Gambar 3.4.

![](data:image/png;base64...)

Gambar 3.4 Diagram Alir Pipeline RAG per Request

* **Config B (*Semantic Search*):** Menggunakan basis data ChromaDB dan model gemini-embedding-001 dengan parameter task\_type="retrieval\_query". Pencarian dilakukan berdasarkan perhitungan jarak kosinus (*cosine distance*).
* **Config C (*Lexical Search*):** Berfungsi sebagai *baseline* kontrol, menggunakan algoritma pencocokan kata kunci BM25Okapi melalui pustaka rank-bm25.

Kedua mekanisme diatur untuk mengembalikan 4 *chunk* teratas (top-. Khusus pada Config B, sistem menerapkan filter ambang batas kemiripan (*similarity threshold*). Berdasarkan proses kalibrasi empiris menggunakan metrik jarak kosinus (rentang 0 hingga 2), nilai ambang batas ditetapkan sebesar 0,3. Jika tidak ada *chunk* yang memiliki jarak di bawah 0,3, sistem akan memicu mekanisme *fallback* dan mengembalikan respons bawaan tanpa memanggil LLM guna mencegah halusinasi jawaban saat menjawab kueri yang berada di luar domain korpus. Config C tidak memiliki mekanisme ini karena BM25 selalu mengembalikan empat hasil teratas terlepas dari seberapa rendah skor leksikalnya.

Sistem evaluasi ini secara spesifik memisahkan antara *retrieved contexts* (seluruh *chunk* yang ditarik oleh sistem pencari) dan *citation sources* (*chunk* yang diekstraksi dan disitasi oleh LLM pada respons akhir).

### *Prompt Engineering* dan Generasi Respons

Integrasi konteks dengan LLM Google Gemini diatur melalui *prompt engineering* agar jawaban yang dihasilkan bersumber secara ketat dari dokumen yang ditemukan. Seluruh *chunk* dari tahap *retrieval* digabungkan ke dalam satu blok teks terstruktur dengan menyertakan prefiks identifikasi format [Sumber N: judul - bab]. *System prompt* mendikte model untuk membaca sumber tersebut dan secara wajib menyisipkan penanda sitasi *inline* [N] pada akhir pernyataan yang diambil dari dokumen. Instruksi pada *system prompt* dikunci dan tidak diubah di antara konfigurasi pengujian untuk mempertahankan variabel kontrol.

Respons mentah dari LLM dipindai menggunakan *Regular Expression* (Regex) untuk mengekstrak angka di dalam kurung siku (\[(\d+)\]) yang mengekstrak daftar rujukan. Proses ini memetakan klaim jawaban LLM ke dokumen sumber aslinya (*citation sources*). *Parser* ini dirancang memiliki toleransi kesalahan; marker sitasi yang merujuk pada indeks di luar rentang valid akan diabaikan tanpa menghentikan eksekusi program.

Untuk mendukung interaksi dialog, sistem mengimplementasikan manajemen memori percakapan berkapasitas 5 giliran terakhir (MEMORY\_K=5). Memori ini dikelola pada sesi memori lokal dan dikirim ulang pada setiap kueri baru untuk mempertahankan konteks riwayat percakapan.

## Skenario Eksperimen dan Evaluasi

### Skenario Pengujian (Config B vs Config C)

Penelitian ini dirancang dengan pendekatan eksperimen komparatif terkontrol (*controlled comparative experiment*). Pengujian membandingkan dua konfigurasi sistem dengan memanipulasi satu variabel independen secara spesifik, sementara seluruh variabel lainnya dikunci untuk memastikan validitas perbandingan.

Variabel independen pada penelitian ini adalah mekanisme *retrieval*. Sistem utama (Config B) menggunakan pencarian semantik berbasis vektor (*cosine similarity*) melalui ChromaDB, sedangkan sistem *baseline* (Config C) menggunakan pencarian leksikal berbasis algoritma BM25.

Variabel dependen adalah nilai empat metrik Ragas (*faithfulness*, *answer\_relevancy*, *context\_precision*, dan *context\_recall*) masing-masing dalam rentang [0, 1] serta *response\_time\_seconds* sebagai metrik deskriptif sekunder.

Variabel kontrol dikunci identik antara Config B dan Config C agar perbedaan hasil hanya mencerminkan perbedaan mekanisme retrieval, sebagaimana dirangkum pada Tabel 3.3 berikut.

Tabel 3.3 Parameter Variabel Kontrol Eksperimen

|  |  |
| --- | --- |
| VARIABEL KONTROL | NILAI YANG DIKUNCI |
| Dataset Ground Truth | Identik |
| Model Generator | gemini-3.5-flash |
| Model Embedding | gemini-embedding-001 |
| System Prompt | Dikunci, tidak diubah antar konfigurasi. |
| Nilai retrieval (top-*k*) | 4 chunk teratas (top- |
| Model Evaluator Ragas | gemini-2.5-flash |
| Ukuran Chunk | 2000 karakter, overlap 200 karakter |

Penguncian parameter ukuran *chunk* memastikan bahwa Config C tidak melakukan pencarian pada dokumen utuh, melainkan pada irisan *chunk* yang sama persis dengan yang diindeks oleh Config B.

Eksperimen dieksekusi secara *sequential*, di mana evaluasi Config B diselesaikan terlebih dahulu sebelum Config C dalam satu sesi yang sama. Protokol pengujian mewajibkan reset memori riwayat percakapan (chat\_history = []) sebelum setiap kueri dieksekusi. Hal ini dilakukan untuk mencegah kebocoran konteks (*context leak*) di mana jawaban LLM berpotensi terpengaruh oleh interaksi pada pertanyaan sebelumnya.

### Penyusunan *Dataset Ground Truth*

Instrumen evaluasi utama dalam penelitian ini adalah *dataset ground truth* yang disusun secara manual dan disimpan dalam format CSV. Dataset ini memuat lima atribut utama: kueri pengguna (user\_input), jawaban ideal (reference), kategori dokumen (category), doc\_id dokumen sumber (source\_doc), dan catatan tambahan (notes).

Pertanyaan disusun menggunakan prinsip *natural language* untuk mensimulasikan cara mahasiswa nyata berinteraksi dengan *chatbot*, alih-alih menggunakan *query* teknis atau legalistik.

Keterbatasan yang perlu diakui adalah penyusunan *ground truth* hanya dilakukan peneliti tunggal sehingga memiliki risiko bias konfirmasi. Mitigasi yang dilakukan adalah mendokumentasikan proses penyusunan secara transparan dan mendistribusikan pertanyaan secara merata ke seluruh dokumen corpus, termasuk pertanyaan tentang informasi yang secara eksplisit tidak tersedia dalam corpus (*out-of-domain questions*), untuk menguji mekanisme *fallback* sistem.

### Metrik Evaluasi dan Operasionalisasi Ragas

Evaluasi kualitas jawaban dan *retrieval* dilakukan secara terotomatisasi menggunakan pendekatan *LLM-as-a-Judge* melalui empat metrik Ragas yang secara konseptual telah dijabarkan pada Bab II. Pada implementasi fungsionalnya, parameter yang diteruskan ke fungsi evaluasi Ragas adalah seluruh *chunk* yang berhasil ditarik oleh sistem pencari (*retrieved contexts*), bukan sebatas *chunk* yang akhirnya disitasi oleh LLM (*citation sources*). Keputusan ini diambil untuk menghindari bias pengukuran: jika hanya chunk yang dikutip yang diteruskan, nilai *context\_recall* akan cenderung terlihat tinggi karena jumlah konteks yang dievaluasi menjadi lebih sedikit dan lebih mudah dianggap 'tercakup' oleh jawaban referensi. Menggunakan seluruh *retrieved\_contexts* memastikan metrik mencerminkan kualitas *retrieval* yang sesungguhnya, bukan seberapa selektif LLM dalam mengutip.

Konfigurasi *runtime* Ragas menggunakan max\_workers=1 yaitu evaluasi dieksekusi secara sekuensial, timeout=300 detik, dan max\_retries=10. Pilihan max\_workers=1 memperlambat proses evaluasi, tetapi memberikan stabilitas yang jauh lebih baik terhadap *rate limit* API; evaluasi paralel pada skala dataset penelitian ini secara konsisten memicu penolakan API pada uji coba awal, sehingga kecepatan dikorbankan demi keandalan hasil.

![](data:image/x-emf;base64...)

Gambar 3.5. Contoh bagan yang menjabarkan mengenai langkah-langkah dalam penelitian/pengerjaan tugas akhir.

# Bab IV Hasil dan Pembahasan

## Hasil Implementasi Sistem

### Statistik *Corpus* dan *Ingestion*

Proses prapemrosesan data dilakukan dengan mengonversi dokumen regulasi dan profil akademik Universitas Sam Ratulangi (UNSRAT) ke dalam format Markdown (.md) secara terstruktur. Struktur ini ditandai menggunakan hierarki *heading* (# hingga ####) untuk memisahkan setiap unit informasi secara logis.

#### Karakteristik Struktural Korpus Akademik

Korpus data penelitian mencakup sembilan dokumen referensi utama yang merepresentasikan aturan akademik, agenda kegiatan, serta profil institusional universitas. Rincian metrik ukuran berkas dalam satuan *bytes* dan jumlah *section* terstruktur yang berhasil diekstrak berdasarkan penanda *header* dapat dilihat pada Tabel 4.1.

Tabel 4.1 Komposisi Dokumen Korpus Penelitian

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| NO | NAMA DOKUMEN | KATEGORI | UKURAN (*BYTES*) | JUMLAH *HEADER* |
| 1 | 01\_sejarah.md | *institution\_profile* | 8.364 | 11 |
| 2 | 02\_visi\_misi.md | *institution\_profile* | 2.252 | 5 |
| 3 | 03\_tujuan\_sasaran\_strategi.md | *institution\_profile* | 8.882 | 5 |
| 4 | 04\_lambang.md | *institution\_profile* | 9.056 | 7 |
| 5 | 05\_bendera.md | *institution\_profile* | 4.165 | 4 |
| 6 | 06\_mars\_hymne.md | *institution\_profile* | 2.978 | 5 |
| 7 | 07\_akreditasi.md | *institution\_profile* | 2.746 | 3 |
| 8 | Kalender\_Akademik\_UNSRAT\_Genap\_2025-2026.md | *academic* | 14.067 | 24 |
| 9 | Peraturan\_Akademik\_UNSRAT\_2025\_RAG\_REVISED.md | *calendar* | 121.184 | 133 |
| - | Total Korpus |  | 173.690 | 197 |

Data pada Tabel 4.1 menunjukkan bahwa Dokumen Peraturan Akademik merupakan komponen terbesar dalam korpus, merepresentasikan 69,77% dari total ukuran teks dan memuat 133 *section*.

#### Log Proses Ingestion Sistem

Eksekusi *pipeline ingestion* diuji melalui dua skenario operasi pada lingkungan lokal guna memvalidasi aspek penanganan redundansi (*idempotency*) dan stabilitas waktu pemrosesan. Ringkasan statistik dari log historis mesin pembangun indeks vector database ChromaDB (Config B) dirangkum pada Tabel 4.2.

Tabel 4.2 Ringkasan Pipeline Ingestion Config B

|  |  |  |
| --- | --- | --- |
| Parameter | Run 1 - Inkremental | Run 2 - Clean Build |
| *Files Processed* | 9 | 9 |
| *Chunks Generated* | 312 | 179 |
| *Chunks Inserted* | 295 | 179 |
| *Chunks Duplicate Skipped* | 14 | 0 |
| *Chunks Too Short Skipped* | 3 | 0 |
| *Execution Time* (detik) | 187,40 | 149,25 |

Proses *ingestion* dieksekusi dalam dua skenario (inkremental dan *clean build*) untuk memvalidasi penanganan redundansi (*idempotency*) sistem. Mengacu pada mekanisme deduplikasi dan filter batas minimum karakter yang telah dirancang pada Bab III, sistem secara otomatis mengabaikan 14 *chunk* duplikat (via *hash* MD5) dan 3 *chunk* residu sintaksis (< 50 karakter) pada Run 1. Setelah penyesuaian, eksekusi *clean build* (Run 2) menghasilkan 179 *chunk* yang siap diindeks ke dalam ChromaDB maupun indeks BM25.

#### Representasi Struktur Metadata *Chunks*

Setiap unit teks yang berhasil diindeks ke dalam database dilengkapi skema metadata terstruktur guna mendukung mekanisme penyaringan konteks (*metadata filtering*) dan visualisasi rujukan balik pada antarmuka pengguna. Contoh representasi metadata untuk *chunk* dari dokumen regulasi akademik disajikan pada Potongan Kode Program 4.1.

Potongan Kode Program 4.1 Contoh Metadata Chunk

1. {
2. "chunk\_id": "2a8d3a5e4fe50670c74eb1b43bd75f78",
3. "metadata": {
4. "doc\_id": "UNSRAT-REG-2025-001",
5. "title": "Peraturan Rektor UNSRAT Nomor 01 Tahun 2025 tentang Peraturan Academic",
6. "category": "academic",
7. "content\_type": "regulation",
8. "bab": "BAB VI — KURIKULUM",
9. "bagian": "Bagian Pertama — Jenis Kurikulum dan Capaian Pembelajaran",
10. "pasal": "Pasal 17 — Definisi Kurikulum",
11. "status": "active"
12. },
13. "content": "## BAB VI — KURIKULUM \n### Bagian Pertama — Jenis Kurikulum dan Capaian Pembelajaran \n#### Pasal 17 — Definisi Kurikulum \nKurikulum merupakan seperangkat rencana dan pengaturan mengenai tujuan, isi, dan bahan pembelajaran, serta cara yang digunakan sebagai pedoman penyelenggaraan pembelajaran di UNSRAT untuk mencapai tujuan program studi."
14. }

Potongan Kode Program 4.1 menunjukkan bahwa MarkdownHeaderTextSplitter berhasil menyisipkan metadata hierarkis dokumen (BAB, Bagian, dan Pasal) ke dalam setiap *chunk*.

### Validasi Empiris Ukuran *Chunk*

#### Analisis Distribusi Panjang *Section* Dokumen

Pengukuran panjang karakter terhadap 197 *section* teks di dalam korpus menghasilkan sebaran statistik sebagai berikut:

Tabel 4.3 Statistik Deskriptif Panjang Section Dokumen Korpus

|  |  |
| --- | --- |
| METRIK | NILAI |
| Panjang Minimum | 13 karakter (berupa sub-header pendek) |
| Rata-rata (*Mean*) | 783,3 karakter |
| Median (Persentil ke-50) | 465,0 karakter |
| Persentil ke-75 | 817,0 karakter |
| Persentil ke-90 | 1.352,8 karakter |
| Persentil ke-95 | 1.788,6 karakter |
| Persentil ke-99 | 4.682,4 karakter |
| Panjang Maksimum | 31.293 karakter |

Dokumen regulasi memiliki sebaran *positively skewed*, di mana mayoritas pasal memiliki ukuran ringkas namun terdapat *outlier* bernilai sangat besar. Sebagai contoh, nilai maksimum sebesar 31.293 karakter ditemukan pada Pasal 1 Peraturan Rektor yang memuat format tabel kompleks berisi 77 entri definisi istilah akademik. Jika Pasal 1 tersebut dieksklusi dari perhitungan, nilai rata-rata panjang pasal beserta uraian sub-ayatnya berada pada angka 848 karakter.

#### Justifikasi Pemilihan Parameter Batas Karakter

Distribusi persentil pada Tabel IV.3 mengonfirmasi bahwa penetapan batas maksimal 2.000 karakter merupakan keputusan desain yang optimal untuk menjaga integritas semantik regulasi akademik. Mengingat nilai persentil ke-95 berada pada angka 1.788,6 karakter, batas 2.000 karakter ini secara matematis mengamankan 96,45% *section* dalam korpus (sejumlah 197 - 7 = 190 *section*) untuk dipertahankan secara utuh tanpa terpotong di tengah kalimat.

Langkah mempertahankan keutuhan *section* ini krusial pada dokumen hukum demi menjaga ikatan konteks antar-ayat. Untuk menangani sisa 3,55% *section* yang berukuran lebih besar (seperti Pasal 1 yang memuat 77 definisi istilah dengan total 31.293 karakter), sistem mengandalkan mekanisme pemisahan Tahap 2 menggunakan *RecursiveCharacterTextSplitter*. Pendekatan ini memastikan pemotongan teks panjang tetap jatuh pada batas tanda baca terdekat, sehingga meminimalkan hilangnya konteks akibat pemotongan karakter secara naif.

### Demonstrasi Antarmuka *Prototype*

Antarmuka *prototype* dibangun sebagai Single Page Application (SPA) dengan dua tab utama: **Tab Chat** untuk interaksi kueri dan **Tab Evaluasi** untuk pemantauan kinerja sistem. Pemisahan fungsional ini mengikuti prinsip separation of concerns yaitu jalur percakapan pengguna tidak berbagi beban dengan proses evaluasi yang dieksekusi secara terpisah melalui endpoint /api/evaluation.

Antarmuka dibangun menggunakan HTML5, JavaScript vanilla, dan Tailwind CSS, dengan visualisasi metrik menggunakan Chart.js dan *parsing* Markdown melalui Marked.js. Seluruh komponen frontend ini dilayani oleh FastAPI melalui endpoint /static/.

#### Tab Chat

Antarmuka Tab Chat difungsikan sebagai media interaksi utama untuk menguji fungsionalitas sistem. Panel ini memuat kontrol untuk pengalihan *query* antara Config B dan Config C, serta area percakapan utama. Pengiriman token teks dari LLM ke sisi *client* diimplementasikan menggunakan protokol *Server-Sent Events* (SSE).

*Output* LLM yang berhasil dieksekusi melalui *retrieval* akan dilengkapi dengan sitasi *inline* berformat [N]. Sebagai wujud antarmuka dari mekanisme *Citation Parser*, pengguna dapat mengklik penanda tersebut untuk memicu sebuah *tooltip*. Komponen *tooltip* ini merender metadata dari *chunk* referensi terkait, mencakup hierarki dokumen asli (BAB, Bagian, Pasal) beserta nilai metrik relevansinya (*cosine distance)* untuk Config B atau skor pemeringkatan BM25 untuk Config C.

Pada skenario di mana kueri terindikasi berada di luar korpus atau terblokir oleh *similarity threshold* (merujuk pada logika filter di Sub-bab 3.3.3), antarmuka akan merender *fallback response*. Secara visual, kondisi ini ditandai dengan tidak munculnya elemen penanda sitasi dan panel sumber rujukan pada jendela percakapan.

![](data:image/png;base64...)

Gambar 4.1 Antarmuka Halaman Chat

#### Tab Evaluasi

Tab Evaluasi mengambil data dari endpoint /api/evaluation yang membaca hasil komputasi Ragas dan log transaksi dari transaksi\_chat.csv. Tab ini menampilkan tiga panel:

* **Panel Metadata Pengujian** merangkum konteks eksperimen: nama model generator, model evaluator, model embedding, jumlah pasangan ground truth yang dievaluasi, dan tanggal eksekusi.
* **Panel Grafik Kinerja Komparatif** menampilkan grouped bar chart (Chart.js) untuk keempat metrik Ragas dengan sumbu Y dikunci pada rentang 0-1,0. Config B dan Config C ditampilkan berdampingan per metrik. Gambar 4.2 menunjukkan tangkapan layar panel ini.
* **Panel Audit Log Transaksi** menampilkan lima transaksi percakapan terakhir yang berhasil dicatat, kueri pengguna, konfigurasi yang digunakan, waktu respons dalam detik, jumlah chunk yang berhasil di-retrieve, dan chunk ID masing-masingnya.

![](data:image/png;base64...)

Gambar 4.2 Antarmuka Halaman Evaluasi

## Hasil Evaluasi Kuantitatif (jelaskan Aktivitas DSR: Evaluation)

### Perbandingan Metrik Ragas: Config B vs Config C

### Analisis Distribusi Per-*Query*

### Perbandingan Latensi Respons (Deskriptif)

## Analisis Kegagalan Kualitatif

### Pola Kegagalan Config B (RAG Semantik)

### Pola Kegagalan Config C (BM25 Leksikal)

### Komparasi Pola Kegagalan Antar Konfigurasi

## Pembahasan

### Interpretasi Komparatif Config B vs Config C

### *Trade-off* Konsumsi Token dan Latensi

### Implikasi Temuan untuk Sistem RAG Domain Regulasi

# Penutup

## Kesimpulan

## Saran

Daftar Pustaka

Abu Shawar, B., & Atwell, E. (2007). Chatbots: Are they Really Useful? *Journal for Language Technology and Computational Linguistics*, *22*(1), 29–49. https://doi.org/10.21248/jlcl.22.2007.88

Ajiz, M. F., Ramadan, M. F. S., Mutia, H. D., & Yanuari, P. D. (2023). Pengembangan Aplikasi Chatbot Informasi Akademik Berbasis Web Menggunakan Metode Artificial Intelligence Markup Language (AIML). *Media Jurnal Informatika*, *15*(2), 143. https://doi.org/10.35194/mji.v15i2.3316

Al Fajri, M. R., & Hartono, B. (2024). Pengembangan Aplikasi Chatbot Telegram Menggunakan Framework Rasa untuk Pelayanan Administrasi di Perguruan Tinggi Universitas Stikubank. *Jurnal JTIK (Jurnal Teknologi Informasi Dan Komunikasi)*, *8*(1), 133–136. https://doi.org/10.35870/jtik.v8i1.1370

Al-Joofi, W., Sagheer, A., & Hamdoun, H. (2026). A Multi-Stage Hybrid Retrieval Framework for the Scientific Literature with Cross-Encoder Re-Ranking. *Applied Sciences*, *16*(10), 4813. https://doi.org/10.3390/app16104813

Artayasa, P. A. S., Kusuma, A. S., & Sugiartawan, P. (2025). *Enhancing Academic Chatbot Accuracy With Retrieval-Augmented Generation in Higher Education*. 427–432. https://doi.org/10.1109/isct66099.2025.11297210

Attigeri, G., Agrawal, A., & Kolekar, S. V. (2024). Advanced NLP Models for Technical University Information Chatbots: Development and Comparative Analysis. *IEEE Access*, *12*, 29633–29647. https://doi.org/10.1109/ACCESS.2024.3368382

Bang, B., Yoon, J., Chang, D.-J., Park, S., & Lee, Y. O. (2026). Retrieval augmented large language model system for comprehensive drug contraindications. *Health Information Science and Systems*, *14*(1), 26. https://doi.org/10.1007/s13755-025-00420-z

Beauchemin, D., Khoury, R., & Gagnon, Z. (2024). Quebec Automobile Insurance Question-Answering With Retrieval-Augmented Generation. *Proceedings of the Natural Legal Language Processing Workshop 2024*, 48–60. https://doi.org/10.18653/v1/2024.nllp-1.5

Bhat, S. R., Rudat, M., Spiekermann, J., & Flores-Herr, N. (2025). *Rethinking Chunk Size For Long-Document Retrieval: A Multi-Dataset Analysis*. http://arxiv.org/abs/2505.21700

Chen, D., Fisch, A., Weston, J., & Bordes, A. (2017). Reading Wikipedia to Answer Open-Domain Questions. *Proceedings of the 55th Annual Meeting of the Association for          Computational Linguistics (Volume 1: Long Papers)*, *1*, 1870–1879. https://doi.org/10.18653/v1/P17-1171

Dam, S. K., Hong, C. S., Qiao, Y., & Zhang, C. (2024). *A Complete Survey on LLM-based AI Chatbots*. http://arxiv.org/abs/2406.16937

Dzaki Salman, M., & Nasution, T. (2026). Implementation of Retrieval-Augmented Generation Method on Large Language Model for Development of Campus Service and Information Chatbot. *INOVTEK Polbeng-Seri Informatika*, *11*(1), 298–309.

Es, S., James, J., Espinosa Anke, L., & Schockaert, S. (2024). RAGAs: Automated Evaluation of Retrieval Augmented Generation. *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations*, 150–158. https://doi.org/10.18653/v1/2024.eacl-demo.16

Firdaus, D., Sumardi, I., & Kulsum, Y. (2024). Integrating Retrieval-Augmented Generation with Large Language Model Mistral 7b for Indonesian Medical Herb. *JISKA (Jurnal Informatika Sunan Kalijaga)*, *9*(3), 230–243. https://doi.org/10.14421/jiska.2024.9.3.230-243

Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H. (2024). *Retrieval-Augmented Generation for Large Language Models: A Survey*. http://arxiv.org/abs/2312.10997

Gemini Team, Anil, R., Borgeaud, S., Alayrac, J.-B., Yu, J., Soricut, R., Schalkwyk, J., Dai, A. M., Hauth, A., Millican, K., Silver, D., Johnson, M., Antonoglou, I., Schrittwieser, J., Glaese, A., Chen, J., Pitler, E., Lillicrap, T., Lazaridou, A., … Vinyals, O. (2025). *Gemini: A Family of Highly Capable Multimodal Models*. http://arxiv.org/abs/2312.11805

Gkrimpizi, T., Peristeras, V., & Magnisalis, I. (2023). Classification of Barriers to Digital Transformation in Higher Education Institutions: Systematic Literature Review. *Education Sciences*, *13*(7), 746. https://doi.org/10.3390/educsci13070746

Gomez-Cabello, C. A., Prabha, S., Haider, S. A., Genovese, A., Collaco, B. G., Wood, N. G., Bagaria, S., & Forte, A. J. (2025). Comparative Evaluation of Advanced Chunking for Retrieval-Augmented Generation in Large Language Models for Clinical Decision Support. *Bioengineering*, *12*(11), 1194. https://doi.org/10.3390/bioengineering12111194

Guntoro, G., Loneli Costaner, & Lisnawita, L. (2020). Aplikasi Chatbot untuk Layanan Informasi dan Akademik Kampus Berbasis Artificial Intelligence Markup Language (AIML). *Digital Zone: Jurnal Teknologi Informasi Dan Komunikasi*, *11*(2), 291–300. https://doi.org/10.31849/digitalzone.v11i2.5049

Hevner, A., & Chatterjee, S. (2010). *Design Science Research in Information Systems* (pp. 9–22). https://doi.org/10.1007/978-1-4419-5653-8\_2

Hidayat, I. N., Christanto, D., Rifai, A. N., & Bahrul Ulum, M. (2024). IMPLEMENTASI RASA FRAMEWORK PADA CHATBOT LAYANAN AKADEMIK (Studi Kasus: Fakultas Ilmu Komputer Universitas Esa Unggul). *Komputa?: Jurnal Ilmiah Komputer Dan Informatika*, *13*(2), 79–90. https://doi.org/10.34010/komputa.v13i2.12178

Husain, M. L., Wibisono, Y., & Anisyah, A. (2025). Development of an Academic Services Chatbot Based on Retrieval-Augmented Generation (RAG). *Brilliance: Research of Artificial Intelligence*, *5*(2), 727–735. https://doi.org/10.47709/brilliance.v5i2.6719

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of Hallucination in Natural Language Generation. *ACM Computing Surveys*, *55*(12), 1–38. https://doi.org/10.1145/3571730

Ji, Z., Yu, T., Xu, Y., Lee, N., Ishii, E., & Fung, P. (2023). Towards Mitigating LLM Hallucination via Self Reflection. *Findings of the Association for Computational Linguistics: EMNLP 2023*, 1827–1843. https://doi.org/10.18653/v1/2023.findings-emnlp.123

Jurafsky, D., & Martin, J. H. (2026). *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition with Language Models* (3rd ed.). https://web.stanford.edu/~jurafsky/slp3/

Kang, B., Kim, Y., & Shin, Y. (2023). An Efficient Document Retrieval for Korean Open-Domain Question Answering Based on ColBERT. *Applied Sciences*, *13*(24), 13177. https://doi.org/10.3390/app132413177

Khasanova Zafar kizi, M., & Suh, Y. (2025). Design and Performance Evaluation of LLM-Based RAG Pipelines for Chatbot Services in International Student Admissions. *Electronics*, *14*(15), 3095. https://doi.org/10.3390/electronics14153095

Koay, X.-K., Ong, L.-Y., & Goh, P.-Y. (2026). Structure-Aware Chunking for Complex Tables in Retrieval-Augmented Generation Systems. *Emerging Science Journal*, *10*(1), 184–205. https://doi.org/10.28991/ESJ-2026-010-01-09

Kulkarni, P., Mahabaleshwarkar, A., Kulkarni, M., Sirsikar, N., & Gadgil, K. (2019). Conversational AI: An Overview of Methodologies, Applications &amp; Future Scope. *2019 5th International Conference On Computing, Communication, Control And Automation (ICCUBEA)*, 1–7. https://doi.org/10.1109/ICCUBEA47591.2019.9129347

Lakatos, R., Pollner, P., Hajdu, A., & Joó, T. (2025). Investigating the Performance of Retrieval-Augmented Generation and Domain-Specific Fine-Tuning for the Development of AI-Driven Knowledge-Based Systems. *Machine Learning and Knowledge Extraction*, *7*(1), 15. https://doi.org/10.3390/make7010015

Lee, J., Cha, H., Hwangbo, Y., & Cheon, W. (2024). Enhancing Large Language Model Reliability: Minimizing Hallucinations with Dual Retrieval-Augmented Generation Based on the Latest Diabetes Guidelines. *Journal of Personalized Medicine*, *14*(12), 1131. https://doi.org/10.3390/jpm14121131

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2021). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. http://arxiv.org/abs/2005.11401

M Ikhsan, Dila Marta Putri, Siti Nurjanah, Asde Rahmawati, Fahrizal Fahrizal, & Bastul Wajhi Akramunnas. (2025). Implementasi Teknologi Chatbot sebagai Media Informasi di Universitas Negeri Medan. *Jurnal Teknik Mesin, Industri, Elektro Dan Informatika*, *4*(1), 265–277. https://doi.org/10.55606/jtmei.v4i1.4820

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. https://doi.org/10.1017/CBO9780511809071

Mori, L., Sousa De Oliveira, C., Yih, Y., & Ventresca, M. (2025). *Assessing the Performance Gap Between Lexical and Semantic Models for Information Retrieval With Formulaic Legal Language* (Vol. 25). https://github.com/larimo/lexsem-legal-ir.

Muhammad Adrinta Abdurrazzaq, Edwin Lesmana Tjiong, Aulia Fasya, Michelle Hiu, & Joses Tanuwidjaya. (2025). An Indonesian Chatbot for Disease Diagnosis Using Retrieval-Augmented Generation. *INOVTEK Polbeng - Seri Informatika*, *10*(3), 1877–1887. https://doi.org/10.35314/9nnkn955

Muna, B. L., Sudianto, S., & Usman, M. L. L. (2025). SiAkif-Bots: Gemini AI for Academic Service Chatbots. *Journal of Applied Engineering and Technological Science (JAETS)*, *6*(2), 1237–1253. https://doi.org/10.37385/jaets.v6i2.6728

Neumann, A. T., Yin, Y., Sowe, S., Decker, S., & Jarke, M. (2025). An LLM-Driven Chatbot in Higher Education for Databases and Information Systems. *IEEE Transactions on Education*, *68*(1), 103–116. https://doi.org/10.1109/TE.2024.3467912

Orrù, G., Melis, G., & Sartori, G. (2025). Large language models and psychiatry. *International Journal of Law and Psychiatry*, *101*, 102086. https://doi.org/10.1016/j.ijlp.2025.102086

Ovadia, O., Brief, M., Mishaeli, M., & Elisha, O. (2024). Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs. *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, 237–250. https://doi.org/10.18653/v1/2024.emnlp-main.15

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A Design Science Research Methodology for Information Systems Research. *Journal of Management Information Systems*, *24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Pratami, R., Ruhallah, M. L., & Gozali, A. A. (2025). LLM-Based Chatbot for the Indonesia University IT Service Desk: Integrating DeepSeek-v3 API and a RAG Approach. *2025 International Conference on Data Science and Its Applications (ICoDSA)*, 979–984. https://doi.org/10.1109/ICoDSA67155.2025.11157184

Priccilia, S., & Girsang, A. S. (2024). Indonesian generative chatbot model for student services using GPT. *International Journal of Informatics and Communication Technology (IJ-ICT)*, *13*(1), 50. https://doi.org/10.11591/ijict.v13i1.pp50-56

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, 3980–3990. https://doi.org/10.18653/v1/D19-1410

Reuter, M., Lingenberg, T., Liepina, R., Lagioia, F., Lippi, M., Sartor, G., Passerini, A., & Sayin, B. (2025). Towards Reliable Retrieval in RAG Systems for Large Legal Datasets. *Proceedings of the Natural Legal Language Processing Workshop 2025*, 17–30. https://doi.org/10.18653/v1/2025.nllp-1.3

Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends® in Information Retrieval*, *4*(1–2), 1–174. https://doi.org/10.1561/1500000019

Ruindungan, D. G. S., & Jacobus, A. (2021). Chatbot Development for an Interactive Academic Information Services using the Rasa Open Source Framework. *Jurnal Teknik Elektro Dan Komputer*, *10 (1)*, 61–68. https://doi.org/https://doi.org/10.35793/jtek.v10i1.31150

Sharma, C. (2025). *Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers*. http://arxiv.org/abs/2506.00054

Suasnawa, I., Wiratama, I., Sudiartha, I., Caturbawa, I., Sapteka, A., & Indrayana, I. (2022). Chatbot-Based Student Information Service in Indonesian Language. *Proceedings of the 5th International Conference on Applied Science and Technology on Engineering Science*, 223–227. https://doi.org/10.5220/0011753800003575

Sun, Y., Sheng, D., Zhou, Z., & Wu, Y. (2024). AI hallucination: towards a comprehensive classification of distorted information in artificial intelligence-generated content. *Humanities and Social Sciences Communications*, *11*(1), 1278. https://doi.org/10.1057/s41599-024-03811-x

Vadlamani, S., & Borada, D. (2025). The Role of LLM Agent Apps in Conversational AI. *International Journal of Research in Modern Engineering & Emerging Technology*, *13*(4), 205–223. https://doi.org/10.63345/ijrmeet.org.v13.i4.12

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). *Attention Is All You Need*. http://arxiv.org/abs/1706.03762

Yao, C., & Fujita, S. (2024). Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags. *Electronics (Switzerland)*, *13*(23). https://doi.org/10.3390/electronics13234643

Yao, Y., Duan, J., Xu, K., Cai, Y., Sun, Z., & Zhang, Y. (2024). A survey on large language model (LLM) security and privacy: The Good, The Bad, and The Ugly. *High-Confidence Computing*, *4*(2), 100211. https://doi.org/10.1016/j.hcc.2024.100211

Yepes, A. J., You, Y., Milczek, J., Laverde, S., & Li, R. (2024). *Financial Report Chunking for Effective Retrieval Augmented Generation*. http://arxiv.org/abs/2402.05131

Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., Huang, X., Zhao, E., Zhang, Y., Xu, C., Chen, Y., Wang, L., Luu, A. T., Bi, W., Shi, F., & Shi, S. (2025). Siren’s Song in the AI Ocean: A Survey on Hallucination in Large Language Models. *Computational Linguistics*, *51*(4), 1373–1418. http://arxiv.org/abs/2309.01219

Lampiran I
Judul Lampiran I
