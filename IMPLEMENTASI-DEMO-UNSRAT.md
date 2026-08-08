# Rencana Implementasi: Frontend Demo Replika UNSRAT (Opsi A)

> Dokumen ini adalah spesifikasi teknis untuk implementasi fitur baru pada proyek chatbot RAG UNSRAT yang sudah berjalan. Dokumen ini ditulis untuk dua audiens: (1) pengembang/mahasiswa pemilik proyek sebagai pengingat konsep, dan (2) AI coding agent (Claude Code / Antigravity) yang akan mengeksekusi implementasi langsung di direktori proyek.
>
> **Baca dokumen ini secara utuh sebelum mulai coding.** Bagian "Batasan & Larangan Eksplisit" di akhir dokumen bersifat mengikat.

---

## 1. Konteks & Latar Belakang

Proyek ini adalah skripsi berjudul **"Implementasi dan Evaluasi Kinerja Chatbot Layanan Informasi Akademik Universitas Sam Ratulangi Menggunakan Arsitektur Retrieval-Augmented Generation dan Google Gemini"**.

Sistem saat ini terdiri dari:
- **Backend**: FastAPI (`app.py` + modul `src/`) — menangani RAG pipeline, koneksi ke Google Gemini, evaluasi RAGAS. Backend ini **API-first**, tidak bergantung pada frontend tertentu, dan **tidak boleh diubah logic-nya** dalam pekerjaan ini.
- **Frontend awal** (`static/index.html` + `static/js/app.js`): SPA sederhana (Tailwind CDN, vanilla JS, marked.js, lucide, Chart.js) yang dipakai selama pengembangan & testing. Punya dua tab: Chat dan Evaluasi (RAGAS).

**Alasan perubahan**: Dosen pembimbing meminta demo dilakukan di atas tampilan yang meniru homepage resmi unsrat.ac.id (bukan WordPress sungguhan — karena implementasi di server produksi kampus tidak memungkinkan), untuk menghindari pertanyaan penguji soal representativitas kata "Implementasi" di judul. Homepage asli di-scrape via View Page Source menjadi `unsrat-ac-id.html` dan akan dijadikan basis tampilan demo, dengan tombol pemicu modal chatbot ditambahkan di atasnya.

**Keputusan arsitektur yang sudah difinalkan** (hasil brainstorming sebelumnya, tidak perlu didiskusikan ulang):
- **Opsi A dipilih**: satu backend (`app.py`), satu port, banyak "pintu"/route untuk frontend berbeda. Tidak ada server/port kedua, tidak ada duplikasi endpoint, tidak perlu CORS (karena semua origin sama).
- Halaman **demo (replika UNSRAT) menjadi halaman utama** di `/`. Frontend awal (`index.html`) dipindah menjadi halaman sekunder di `/testing`.
- Fitur evaluasi RAGAS dipisah dari modal chatbot, menjadi halaman berdiri sendiri (tanpa sidebar/menu chat) di `/evaluation`.
- Modal chatbot di halaman demo akan **dibangun ulang UI-nya** (bukan reuse index.html mentah), dengan Tailwind CDN yang di-scope agar tidak bentrok dengan CSS bawaan tema WordPress hasil scraping.
- Field yang dipertahankan di modal: kirim-terima chat, citation, config select. Model select **tidak** wajib ditampilkan di modal demo (opsional, boleh disederhanakan — akan dirinci di bagian Fase 3).
- Tombol pemicu modal: tombol baru independen, diposisikan menumpuk di atas tombol "back-to-top" yang sudah ada di halaman asli, **tidak** menumpang di widget back-to-top maupun AddToAny (alasan: keduanya dikontrol script pihak ketiga yang bisa memanipulasi DOM-nya sendiri, dan back-to-top tersembunyi secara default sebelum scroll).

---

## 1a. Ringkasan Jawaban atas Pertanyaan Terbuka (Iterasi Kedua)

- **Desain UI modal (tahap awal)**: mengikuti gaya visual `tab-chat` di `index.html` (palet warna maroon `#7B2D2D`, bubble chat, animasi slide-up, welcome message dengan quick-question buttons) — **tanpa sidebar**. Karena `config-select`/`model-select` di `index.html` berada di dalam sidebar (bukan di `tab-chat`), keduanya dipindah ke **header modal** (baris kecil di atas area pesan). Ini didetailkan di Fase 2/3. Anda boleh mengubah styling ini kapan saja setelah kode berjalan — tidak ada bagian dari fase awal yang mengunci desain final.
- **Alpine.js: tidak diperlukan.** Vanilla JS (hasil ekstraksi `app.js`, sudah teruji) cukup untuk toggle modal, streaming state, dan render pesan. Menambah Alpine.js berarti dependency baru yang tidak perlu dan tidak konsisten dengan kode existing.
- **Modularitas & debug**: ditegaskan lewat penamaan ID yang di-prefix (lihat Bagian 3a) dan pemisahan tanggung jawab antar file JS (lihat Bagian 5a).
- **Tidak merusak kondisi existing**: ditegaskan lewat mekanisme Preflight Tailwind (lihat Bagian 5, poin risiko baru) dan checklist regresi di Fase 6 yang sudah ada sebelumnya, kini diperluas.
- **Environment**: proyek berjalan di conda env `unsrat-rag` — semua instruksi command di dokumen ini mengasumsikan env tersebut sudah aktif (`conda activate unsrat-rag`).
- **Tools tambahan (context7, playwright, dsb.)**: dijelaskan di Bagian 9 (baru) — bukan tools yang saya panggil saat menulis dokumen ini, melainkan instruksi untuk AI coding agent memakainya di lingkungan eksekusinya sendiri, jika tersedia.
- **Deviasi dari AI coding agent**: diperbolehkan untuk hal non-arsitektural, dengan syarat didokumentasikan — mekanismenya dijelaskan di Bagian 7a (baru).

---

## 2. Tech Stack

| Layer | Teknologi | Catatan |
|---|---|---|
| Backend | FastAPI (existing, tidak berubah) | `app.py` + `src/` |
| Frontend demo baru | HTML statis + Tailwind CSS via **CDN** (bukan build process) | Konsisten dengan pendekatan `index.html` yang sudah ada — tidak perlu `package.json`/npm untuk CSS |
| JS demo | Vanilla JS, hasil ekstraksi & refactor dari `app.js` | File baru: `chat-widget.js`, `eval-standalone.js` |
| Markdown rendering | marked.js (CDN, sama seperti sekarang) | |
| Icon | lucide (CDN, sama seperti sekarang) | |
| Chart (halaman evaluasi) | Chart.js (CDN, sama seperti sekarang) | |
| Static file serving | `StaticFiles` FastAPI (existing) + route tambahan | |
| Version control | Git, branch `main` sudah berjalan | Branch kerja baru akan dibuat, lihat Bagian 6 |

**Tidak ada dependency Python baru.** Tidak ada dependency Node/npm baru. Ini murni penambahan file statis + sedikit route baru di `app.py`.

---

## 3. Struktur Direktori (Target Akhir)

Struktur `static/` saat ini:
```
static/
├── assets/
│   └── logo-unsrat.png
├── js/
│   ├── app.js
│   └── dev.js
├── dev.html
└── index.html
```

Struktur `static/` setelah implementasi:
```
static/
├── assets/
│   └── logo-unsrat.png
├── js/
│   ├── app.js              # TIDAK DIUBAH — tetap melayani /testing
│   └── dev.js               # TIDAK DIUBAH
├── demo/                     # BARU
│   ├── index.html            # Replika homepage UNSRAT + tombol trigger + modal (markup)
│   ├── evaluation.html       # Halaman evaluasi RAGAS standalone (tanpa sidebar/menu chat)
│   ├── css/
│   │   └── demo-modal.css    # (opsional) CSS scoped khusus modal, jika Tailwind CDN saja tidak cukup
│   ├── js/
│   │   ├── chat-widget.js    # Hasil ekstraksi logic chat dari app.js (defensif, self-contained)
│   │   └── eval-standalone.js # Hasil ekstraksi logic tab-eval dari app.js
│   └── assets/                # Aset lokal tambahan jika diperlukan (mis. ikon custom tombol trigger)
├── dev.html
└── index.html                 # TIDAK DIUBAH — kini disajikan di /testing, bukan /
```

**Prinsip penting**: `static/index.html`, `static/js/app.js`, `static/js/dev.js`, `static/dev.html` **tidak disentuh sama sekali**. Semua pekerjaan baru terisolasi di `static/demo/`.

### 3a. Konvensi Penamaan ID/Class (Wajib — Mitigasi Risiko Bentrok)

`unsrat-ac-id.html` adalah halaman WordPress kompleks dengan ratusan class/ID bawaan tema dan plugin (RevSlider, AddToAny, smooth-back-to-top-button, dll). Untuk mencegah collision ID (dua elemen ID sama dalam satu dokumen adalah HTML tidak valid dan bisa membuat `getElementById` mengambil elemen yang salah) dan memudahkan debug (mudah dikenali mana elemen buatan sendiri vs bawaan tema saat inspect element), **semua elemen baru yang ditambahkan ke `static/demo/index.html` wajib diberi prefix `rag-`**, misalnya:
- `id="rag-chatbot-widget"` (container pembungkus seluruh fitur: tombol trigger + modal)
- `id="rag-trigger-btn"`
- `id="rag-modal"`, `id="rag-modal-overlay"`, `id="rag-modal-close"`
- `id="rag-chat-form"`, `id="rag-user-input"`, `id="rag-send-btn"`, `id="rag-chat-messages"`
- `id="rag-config-select"`, `id="rag-model-select"` (catatan: sengaja beda dari `config-select`/`model-select` di `index.html` lama — dua dokumen berbeda tidak masalah kalau ID sama, tapi prefix tetap dipakai konsisten untuk kejelasan saat membaca kode `chat-widget.js`)

`chat-widget.js` dan `eval-standalone.js` HARUS mereferensikan ID dengan prefix ini, bukan meng-copy nama ID persis dari `app.js` lama (`chat-form`, `user-input`, dst — nama-nama generik ini yang berisiko collision dengan tema WordPress).

---

## 4. Perubahan pada `app.py`

Hanya bagian routing di akhir file (`# ── Static Files & Root ──`) yang berubah. Tidak ada perubahan pada endpoint `/api/*` manapun (chat, evaluation, dev, dsb — semuanya tetap seperti sekarang).

**Route target:**

| Path | Isi yang disajikan | Keterangan |
|---|---|---|
| `/` | `static/demo/index.html` | Halaman utama baru (demo replika UNSRAT) |
| `/evaluation` | `static/demo/evaluation.html` | Halaman evaluasi RAGAS standalone |
| `/testing` | `static/index.html` | Frontend awal (SPA lengkap: chat + eval + model select), dipertahankan untuk keperluan testing/debug |
| `/dev` | `static/dev.html` | **Tidak berubah** — tetap seperti sekarang |
| `/static/*` | Static file mount | **Tidak berubah** — tetap melayani semua asset lama maupun baru (termasuk `static/demo/js/*`, `static/demo/assets/*`, karena berada di bawah folder `static/`) |
| `/api/*` | Semua endpoint API | **Tidak berubah sama sekali** |

**Logika fungsi `root()` yang sekarang** (baris ~601-607) akan diarahkan ulang untuk membaca `static/demo/index.html`, dan sebuah fungsi baru ditambahkan untuk `/testing` yang membaca `static/index.html` (logic-nya identik dengan `root()` yang lama, hanya path file dan nama fungsi yang berbeda). Fungsi baru ketiga untuk `/evaluation` mengikuti pola yang sama, membaca `static/demo/evaluation.html`.

Pola pembacaan file tetap konsisten dengan yang sudah ada: baca sebagai `HTMLResponse`, dengan fallback pesan "belum tersedia" jika file belum dibuat — pola defensif yang sama seperti fungsi `root()` original.

---

## 5. Alur Kerja / Fase Implementasi

### Fase 0 — Persiapan
1. Aktifkan environment: `conda activate unsrat-rag`. Semua command Python/uvicorn di fase-fase berikutnya mengasumsikan env ini aktif.
2. Pastikan branch `main` dalam kondisi bersih (`git status`), commit atau stash perubahan pending.
3. Buat branch baru: `feature/unsrat-demo-frontend` (detail di Bagian 6).
4. Buat struktur folder `static/demo/`, `static/demo/js/`, `static/demo/css/`, `static/demo/assets/` (folder kosong dulu).
5. Baseline check sebelum ada perubahan apa pun: jalankan server (`python app.py`), buka `/`, `/testing` (belum ada, akan 404/pakai fallback lama — wajar), `/dev`, dan uji satu request chat penuh di frontend lama untuk mencatat baseline perilaku "normal" saat ini. Ini jadi acuan pembanding di Fase 6.

### Fase 1 — Routing Backend
1. Tambahkan 2 fungsi route baru di `app.py` (`/testing`, `/evaluation`) mengikuti pola `root()` yang sudah ada.
2. Ubah fungsi `root()` (`/`) agar membaca `static/demo/index.html` alih-alih `static/index.html`.
3. Test manual: jalankan server, akses ketiga path dengan file placeholder kosong dulu (boleh HTML kosong `<h1>placeholder</h1>`) untuk pastikan routing bekerja sebelum lanjut ke isi asli.

### Fase 2 — Halaman Demo (Homepage Replika)
1. Salin `unsrat-ac-id.html` ke `static/demo/index.html`.
2. **Jangan ubah struktur/markup asli WordPress-nya** kecuali untuk menyisipkan, tepat sebelum `</body>`: (a) satu `<div id="rag-chatbot-widget">` pembungkus berisi tombol trigger + kerangka modal, (b) tag `<script>`/`<link>` tambahan untuk Tailwind CDN + `chat-widget.js`, diletakkan sesudah semua script bawaan tema (agar tidak mengganggu urutan load script WordPress yang sudah ada).
3. Sisipkan tombol trigger baru (`#rag-trigger-btn`): posisi `fixed`, `bottom-right`, ditumpuk di atas elemen `.smooth-back-to-top-button` yang sudah ada (beri jarak/margin agar tidak tumpang tindih — cek posisi persis elemen back-to-top itu di CSS asli sebelum menentukan offset), dengan ikon berbeda (misal ikon `message-square` dari lucide) agar semantiknya jelas berbeda dari back-to-top maupun AddToAny.
4. Bangun markup modal (`#rag-modal`) mengikuti **gaya visual `tab-chat` di `index.html`** (palet maroon `#7B2D2D`/`#963E3E`, bubble style, welcome message dengan quick-question buttons, custom scrollbar) — **tanpa sidebar**. Karena tidak ada sidebar, `config-select`/`model-select` dipindah menjadi baris kecil di **header modal** (di atas area pesan, di bawah judul modal + tombol close). Referensi elemen persis yang perlu direplikasi gayanya: baris 148–203 `index.html` (area `tab-chat`) untuk body modal, dan baris 93–125 `index.html` (bagian config/model dropdown di sidebar) untuk dipindah ke header modal.
5. Modal default `hidden` (via Tailwind `class="hidden"` atau setara), baru tampil saat tombol trigger diklik (toggle class, bukan reload halaman, bukan iframe).
6. Ini adalah **desain tahap awal** — struktur/style boleh diiterasi lebih lanjut setelah semua fungsi terbukti bekerja. Prioritas Fase 2 adalah kelengkapan fungsi, bukan kesempurnaan visual.

### Fase 3 — Ekstraksi & Pembuatan `chat-widget.js`
Ekstraksi dilakukan **dari logic yang sudah ada di `static/js/app.js`**, bukan ditulis dari nol, untuk menjaga konsistensi perilaku yang sudah teruji. Bagian yang diekstraksi:
- State management: `chatHistory`, `isStreaming`, `isUserAborted`, `abortController`.
- Fungsi utilitas: `safeCreateIcons()`, `scrollToBottom()`, `getTimestamp()`, `escapeHtml()`, `setStreamingState()`, `handleAbort()`, `handleError()`, `renderCitations()`.
- Event handler form submit (`chatForm` submit listener) — termasuk logic bikin bubble user & bot, animasi, thinking-phase interval, pemanggilan `fetch("/api/chat", ...)` dengan streaming response, parsing markdown via `marked`, render citation.
- Config select & model select: elemen `configSelect`/`modelSelect`/`badgeConfig` dan logic `updateConfigBadge()`, `loadSystemConfig()` (fetch ke `/api/config` untuk populate pilihan model) — dipertahankan, dipindah ke header modal sesuai Fase 2.
- **Tidak diekstraksi** (karena terkait tab evaluasi, tidak relevan untuk modal): `tabChatBtn`, `tabEvalBtn`, `refreshEvalBtn`, `loadEvaluationData()`, dan seluruh elemen `btn-copy-*`/`meta-*`/`dot-run-*`.
- Semua ID yang direferensikan harus versi ber-prefix `rag-` (lihat Bagian 3a), **bukan** ID asli dari `app.js` (`chat-form`, `user-input`, dst).

**Struktur modular file** (untuk memudahkan debug — poin 2 permintaan Anda): `chat-widget.js` disusun sebagai satu objek/namespace (bukan variabel global bertebaran), contoh pola:
```
const RagChatWidget = {
  state: { chatHistory: [], isStreaming: false, ... },
  init() { /* pasang semua event listener, dipanggil sekali saat modal pertama dibuka atau saat DOMContentLoaded */ },
  openModal() { ... },
  closeModal() { ... },
  sendMessage(query) { ... },
  renderUserBubble(...) { ... },
  renderBotBubble(...) { ... },
  renderCitations(...) { ... },
  // dst — satu fungsi bernama jelas per tanggung jawab, bukan satu blok besar tak terstruktur
};
```
Pola ini memudahkan debug (nama fungsi muncul jelas di stack trace error) dan mencegah polusi variabel global yang bisa bentrok dengan script tema WordPress (banyak tema lama pakai variabel global longgar).

**Prinsip wajib**: setiap `document.getElementById(...)` di `chat-widget.js` harus diikuti null-check sebelum `addEventListener` dipasang (`if (el) { el.addEventListener(...) }` atau pola setara), karena markup modal baru kemungkinan tidak punya semua ID yang sama persis seperti `app.js` lama. Ini mencegah satu elemen hilang menghentikan seluruh script (root cause yang sudah diidentifikasi sebelumnya).

### Fase 4 — Halaman Evaluasi Standalone
1. Buat `static/demo/evaluation.html`: markup diambil dari bagian `<div id="tab-eval">` di `static/index.html` (baris ~205 dst di file asli), **tanpa** sidebar navigasi dan tanpa elemen tab-chat.
2. Buat `static/demo/js/eval-standalone.js`: ekstraksi `loadEvaluationData()` dan seluruh handler terkait (`refreshEvalBtn`, `btnCopyWilcoxon`, `btnCopyAudit`, `btnDownloadAudit`, elemen `meta-*`, `dot-run-*`, chart instance) dari `app.js`, dengan null-check defensif yang sama.
3. Halaman ini memanggil endpoint `/api/evaluation` yang sudah ada — **tidak ada perubahan backend** untuk fitur ini.

### Fase 5 — Styling & Integrasi Visual

**⚠️ RISIKO TEKNIS YANG SUDAH TERKONFIRMASI (bukan spekulasi) — wajib ditangani di fase ini:**

`index.html` yang sudah berjalan memuat Tailwind CDN **tanpa menonaktifkan Preflight** (`tailwind.config` di baris 20–30 `index.html` hanya berisi `theme.extend`, tidak ada `corePlugins: { preflight: false }`). Ini aman di `index.html` karena itu halaman kosong yang sepenuhnya dikontrol Tailwind. **Ini TIDAK aman kalau ditempelkan apa adanya ke `unsrat-ac-id.html`**, karena Tailwind Preflight adalah reset CSS global (mirip `normalize.css` yang diperkuat) yang berlaku ke **seluruh dokumen**, bukan hanya ke elemen di dalam container tertentu. Kalau dibiarkan default, Preflight akan me-reset margin/padding/list-style/border pada seluruh elemen tema WordPress (heading, button, list, form, dst) begitu Tailwind CDN dimuat — nyaris pasti merusak tampilan asli homepage, bukan cuma "berpotensi".

**Mitigasi wajib**: saat menyisipkan `<script>` config Tailwind di `static/demo/index.html`, WAJIB menonaktifkan Preflight:
```html
<script>
  tailwind.config = {
    corePlugins: { preflight: false },
    theme: { extend: { /* boleh isi warna/font custom di sini jika perlu */ } }
  }
</script>
<script src="https://cdn.tailwindcss.com"></script>
```
Dengan Preflight nonaktif, utility class Tailwind (`flex`, `p-4`, `rounded-xl`, dst) tetap berfungsi normal untuk styling elemen baru (`#rag-chatbot-widget`), tapi Tailwind tidak lagi menimpa reset CSS bawaan tema WordPress di elemen-elemen lain.

**Langkah Fase 5:**
1. Tambahkan Tailwind CDN dengan konfigurasi Preflight nonaktif seperti di atas.
2. Bungkus semua elemen buatan sendiri (tombol trigger, modal, isi modal) di dalam `#rag-chatbot-widget` (lihat Bagian 3a) — ini juga memudahkan verifikasi visual: apa pun style yang tampak salah di luar container ini artinya ada kebocoran/bentrok yang harus diinvestigasi.
3. Uji visual bertahap: (a) buka halaman **sebelum** menyisipkan Tailwind sama sekali — screenshot sebagai baseline; (b) sisipkan Tailwind dengan Preflight nonaktif — bandingkan screenshot, harus identik dengan baseline di luar area modal; (c) baru lanjut styling modal.
4. Jika ada tools screenshot/browser automation tersedia di lingkungan eksekusi (lihat Bagian 9), gunakan untuk membandingkan screenshot before/after secara otomatis alih-alih hanya visual manual.

### Fase 6 — Testing Menyeluruh (Checklist)
- [ ] `/` menampilkan homepage replika UNSRAT utuh (hover, animasi, link — sesuai klaim awal bahwa file scraping ini berjalan mandiri)
- [ ] Tombol trigger muncul sejak halaman dimuat (tanpa perlu scroll)
- [ ] Modal terbuka/tertutup dengan benar, tidak mengganggu scroll halaman di belakangnya
- [ ] Chat: kirim pertanyaan → streaming jawaban tampil → citation muncul jika ada
- [ ] Config select di modal berfungsi, mengubah `config` yang dikirim ke `/api/chat`
- [ ] `/evaluation` menampilkan data evaluasi RAGAS dengan benar (chart, tabel, tombol copy/download)
- [ ] `/testing` menampilkan `index.html` versi awal, **berperilaku identik seperti sebelum perubahan ini** (regresi check — chat, eval, model select semua masih berfungsi seperti semula)
- [ ] `/dev` tidak terpengaruh sama sekali
- [ ] Tidak ada error di browser console pada ketiga halaman (`/`, `/testing`, `/evaluation`)
- [ ] Endpoint `/api/*` tidak ada yang berubah perilakunya (uji manual salah satu, misal `/api/config`, dari kedua frontend)
- [ ] Tampilan `unsrat-ac-id.html` di luar area `#rag-chatbot-widget` **identik secara visual** dengan sebelum penyisipan Tailwind (bandingkan dengan baseline Fase 5 poin 3)
- [ ] Tidak ada ID duplikat dalam satu dokumen (cek manual via `document.querySelectorAll('[id]')` di console lalu cari duplikat, atau validator HTML)
- [ ] Perbandingan hasil jawaban chatbot untuk pertanyaan yang sama antara `/` (modal baru) dan `/testing` (frontend lama) — harus menghasilkan jawaban yang konsisten (membuktikan backend benar-benar tidak berubah, memperkuat argumen portabilitas di Bagian 8)
- [ ] `git diff main` dicek: pastikan tidak ada baris berubah di `static/index.html`, `static/js/app.js`, `static/js/dev.js`, `static/dev.html`, atau seluruh isi `src/`

### Fase 7 — Dokumentasi & Commit
1. Update README proyek (jika ada) dengan peta URL baru (`/`, `/testing`, `/evaluation`, `/dev`).
2. Commit bertahap sesuai fase (lihat Bagian 6), bukan satu commit besar di akhir.

---

## 6. Git Workflow

**Kondisi saat ini**: repo sudah berjalan, branch `main` aktif menyimpan versi stabil (frontend awal + backend yang sudah teruji).

**Strategi:**
1. Branch baru dari `main`: `feature/unsrat-demo-frontend`.
2. Commit granular per fase (memudahkan rollback per bagian jika ada yang perlu direvisi):
   - `chore: setup folder structure static/demo`
   - `feat(routing): tambah route /testing dan /evaluation, alihkan / ke demo`
   - `feat(demo): tambah homepage replika unsrat dengan tombol trigger dan kerangka modal`
   - `feat(demo): ekstraksi chat-widget.js dari app.js`
   - `feat(demo): implementasi halaman evaluasi standalone`
   - `style(demo): styling modal dan scoping tailwind`
   - `test: verifikasi manual seluruh route dan fitur` (commit dokumentasi hasil testing, bukan kode)
   - `docs: update README dengan peta URL baru`
3. **Tidak ada commit yang menyentuh** `static/index.html`, `static/js/app.js`, `static/js/dev.js`, `static/dev.html`, atau logic apa pun di dalam `src/`. Kalau diff pada file-file ini muncul di commit manapun, itu tanda ada yang keluar dari scope — harus direview ulang.
4. Setelah semua fase lulus checklist Fase 6, merge ke `main` via pull request (meski solo project, PR description berguna sebagai dokumentasi keputusan untuk lampiran skripsi).
5. Tag opsional setelah merge: `v1.1-demo-frontend` — memudahkan Anda kembali ke titik ini kalau perlu referensi versi persis yang dipakai saat sidang.

---

## 7. Batasan & Larangan Eksplisit (WAJIB DIPATUHI AI CODING AGENT)

1. **JANGAN** mengubah logic apa pun di dalam `src/` (RAG chain, config, logger, preflight). Pekerjaan ini murni penambahan frontend + routing.
2. **JANGAN** mengubah endpoint `/api/*` yang sudah ada — tidak menambah field baru ke `ChatRequest`/model lain, tidak mengubah response shape, tidak mengubah `/api/evaluation`.
3. **JANGAN** mengubah isi `static/index.html`, `static/js/app.js`, `static/js/dev.js`, `static/dev.html`. Ini adalah baseline yang harus tetap berperilaku identik di `/testing`.
4. **JANGAN** menambahkan dependency Python baru ke `requirements.txt` (tidak diperlukan untuk pekerjaan ini — murni frontend statis + routing).
5. **JANGAN** menambahkan build process (npm/webpack/PostCSS) untuk Tailwind — gunakan CDN, sesuai keputusan yang sudah difinalkan.
5a. **JANGAN** menambahkan Alpine.js atau state-management library lain — vanilla JS (pola namespace di Fase 3) sudah cukup dan sudah diputuskan.
6. **JANGAN** mengaktifkan `CORSMiddleware` atau middleware baru apa pun — tidak diperlukan karena semua frontend disajikan dari origin yang sama (satu app, satu port).
7. **JANGAN** menyisipkan trigger button chatbot ke dalam markup widget AddToAny (`.a2a_kit`) atau menggantikan tombol `.smooth-back-to-top-button` — harus jadi elemen baru yang independen.
8. Kalau ada ambiguitas yang muncul saat implementasi (misal ID elemen di `unsrat-ac-id.html` yang bentrok tak terduga dengan Tailwind, atau struktur `app.js` yang lebih kompleks dari yang terdokumentasi di sini), **STOP dan tanyakan ke user**, jangan mengambil keputusan desain baru secara sepihak.
9. **Jangan mengklaim atau mengasumsikan** perilaku API/library yang tidak terverifikasi dari kode yang ada di repo ini atau dari dokumentasi resmi yang benar-benar dibaca (lihat Bagian 9). Kalau tidak yakin tentang suatu detail (misal versi API Tailwind CDN terbaru, perilaku `StreamingResponse` FastAPI di edge-case tertentu), verifikasi dulu (baca kode/dokumentasi), jangan menebak.

### 7a. Protokol Deviasi dari Dokumen Ini (Untuk AI Coding Agent)

AI coding agent **diperbolehkan** menyimpang dari detail non-arsitektural di dokumen ini (misal nama variabel internal, urutan langkah kecil, detail styling) **jika**:
1. Deviasi tidak melanggar satu pun larangan di Bagian 7 (batasan keras).
2. Deviasi tetap konsisten dengan keputusan arsitektur yang sudah difinalkan (Opsi A, satu backend, Tailwind CDN tanpa build process, tanpa Alpine.js, dsb).
3. Deviasi **didokumentasikan eksplisit** di salah satu dari: (a) commit message yang menjelaskan apa & kenapa, atau (b) file `static/demo/CHANGES.md` yang mencatat setiap penyimpangan dari dokumen ini beserta alasannya.

Untuk deviasi yang **menyentuh keputusan arsitektural** (struktur folder, mekanisme routing, apakah butuh dependency baru, dsb) — **tidak boleh diputuskan sepihak oleh agent**, harus dikonfirmasi ke user dulu (sesuai Bagian 7 poin 8).

---

## 9. Tools Pendukung untuk AI Coding Agent (Gunakan Jika Tersedia di Lingkungan Eksekusi)

Dokumen ini ditulis tanpa memverifikasi tools MCP/skill apa yang aktif di lingkungan eksekusi Anda (Claude Code / Antigravity) — cek ketersediaan sebelum memakainya, jangan asumsikan semuanya aktif. Jika tersedia, gunakan sesuai konteks berikut:
- **context7** (atau tool dokumentasi resmi sejenis): gunakan untuk verifikasi API/opsi konfigurasi terbaru dari Tailwind CDN, FastAPI (`StreamingResponse`, `StaticFiles`), lucide, dan marked.js sebelum menulis kode yang bergantung padanya — terutama karena pengetahuan bawaan model bisa saja sudah usang dibanding versi CDN terkini yang di-load `@latest`/`lib/marked.umd.js` tanpa pin versi.
- **playwright** (atau browser automation sejenis): gunakan untuk Fase 5 poin 3–4 (screenshot before/after Preflight) dan Fase 6 (checklist otomatis: cek elemen ada, tidak ada console error, request `/api/chat` sukses) — mengurangi ketergantungan pada verifikasi visual manual yang rawan lolos dari mata.
- **Tools lain yang disebutkan user** (gstack, superpowers, ui-ux-pro-max, impeccable, context-mode): gunakan sesuai fungsinya masing-masing jika relevan dan tersedia — dokumen ini tidak mengetahui kapabilitas pasti masing-masing tool tersebut, jadi agent perlu menilai sendiri relevansinya per fase, dan tidak memaksakan penggunaan tool yang tidak jelas manfaatnya untuk suatu langkah.

---

## 10. Konteks Tambahan untuk Laporan Skripsi (Non-Teknis, untuk Diingat)

Argumen yang sudah disiapkan untuk sidang terkait keputusan arsitektur ini:
- Backend RAG bersifat API-first dan tidak berubah sama sekali baik untuk frontend awal maupun frontend replika WordPress — ini adalah bukti langsung portabilitas arsitektur sistem, bisa didemokan eksplisit ("perhatikan, backend yang sama persis melayani kedua frontend ini").
- Keterbatasan yang harus diakui secara jujur jika ditanya penguji: (1) belum ada bukti integrasi nyata ke WordPress produksi, (2) CORS/autentikasi produksi belum diimplementasikan (di luar scope karena semuanya lokal), (3) server dev (`uvicorn` biasa) belum production-grade. Ketiganya cocok dimasukkan sebagai bagian "Keterbatasan Penelitian" di skripsi.
