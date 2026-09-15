# Dokumentasi Lengkap & Rangkuman Detail 21 Commit: Migrasi Frontend ke Portal INSPIRE (`/`)

**Repositori:** `unsrat-rag-v4`  
**Branch:** `revisi/migrasi-ui-inspire`  
**Periode Pengerjaan:** 13 September 2026 – 15 September 2026  
**Status Akhir:** ✅ **SELESAI, TERUJI (Pytest 3 Passed), & PRODUCTION-READY**  

---

## 1. Ikhtisar Rekayasa Cabang (`revisi/migrasi-ui-inspire`)

Cabang ini didedikasikan untuk melakukan migrasi antarmuka pengguna (*frontend*) secara menyeluruh dari mockup lama yang berbasis homepage portal umum UNSRAT (`/unsratacid`) menuju **Portal INSPIRE** (`/` - `portal.unsrat.ac.id`), gerbang sistem informasi akademik terpadu Universitas Sam Ratulangi.

Sepanjang 21 commit terkelola, antarmuka berevolusi dari widget monolitik sederhana menjadi aplikasi asisten akademik modular berkelas produksi (*production-grade*) dengan paradigma **Mobile-First**, **Editorial Legal Design**, **Gestur Native Bottom Sheet**, dan **Sinkronisasi Sitasi Multi-Turn Bebas Balapan (*Race Condition*)**.

---

## 2. Rangkuman Kronologis Mendalam: 21 Commit Bersejarah

---

### Commit 1: `0237b32`
* **Pesan Commit:** `feat(demo): migrasikan mock utama ke portal INSPIRE dan preservasi mock legacy di /unsratacid`
* **Tanggal:** 13 September 2026, 20:05:40 WITA
* **Files:** `app.py`, `static/demo/index.html`, `static/demo/unsratacid.html`, `tests/integration/test_demo_serving.py`
* **Tujuan & Konteks:**
  Menginisiasi pemisahan rute pada server FastAPI agar rute utama `/` melayani mockup Portal INSPIRE yang baru, sementara mockup lama homepage UNSRAT dipindahkan ke rute `/unsratacid` tanpa memodifikasi logikanya.
* **Perubahan Teknis:**
  - `app.py`: Menambahkan endpoint FastAPI `@app.get("/unsratacid")` yang menyajikan `static/demo/unsratacid.html`. Endpoint `@app.get("/")` tetap mengarah ke `static/demo/index.html`.
  - `static/demo/unsratacid.html`: Duplikasi independen dari mockup legacy untuk dipreservasi 100%.
  - `tests/integration/test_demo_serving.py`: Menambahkan pengujian integrasi TestClient untuk memastikan kedua rute mengembalikan HTTP 200 dengan dokumen HTML yang valid.

---

### Commit 2: `dc583c3`
* **Pesan Commit:** `feat(chain): tambahkan modul pre-RAG intent router untuk sapaan murni dan pengujian 0-false-positive`
* **Tanggal:** 13 September 2026, 20:38:39 WITA
* **Files:** `src/chain.py`, `src/router.py`, `tests/integration/test_chat_greeting.py`, `tests/unit/test_router.py`
* **Tujuan & Konteks:**
  Menghemat latensi dan biaya API LLM untuk pertanyaan sapaan umum (*greeting*) seperti *"Halo"*, *"Selamat pagi"*, atau *"Hai"*, serta mencegah sapaan tersebut memicu retrieval dokumen regulasi akademik secara salah (*zero false-positive*).
* **Perubahan Teknis:**
  - `src/router.py`: Mengimplementasikan fungsi `classify_intent(query)` dengan pencocokan pola regex dan kata kunci intent deterministik.
  - `src/chain.py`: Memasang `PreRAGRouter` sebelum *retriever step*. Jika terdeteksi intent `GREETING`, sistem langsung mengalirkan respons sambutan ramah resmi tanpa melakukan vector/sparse search.
  - `tests/unit/test_router.py` & `tests/integration/test_chat_greeting.py`: 16 skenario pengujian unit & integrasi untuk memverifikasi sapaan murni ditangani $\le 5\text{ms}$ tanpa menyentuh RAG pipeline.

---

### Commit 3: `0454779`
* **Pesan Commit:** `feat(router): tambahkan penanganan intent identitas dan kapabilitas asisten akademik`
* **Tanggal:** 13 September 2026, 20:50:17 WITA
* **Files:** `src/router.py`, `tests/integration/test_chat_greeting.py`, `tests/unit/test_router.py`
* **Tujuan & Konteks:**
  Menambahkan klasifikasi intent `IDENTITY` dan `CAPABILITIES` (misal: *"Siapa kamu?"*, *"Apa yang bisa kamu lakukan?"*) agar asisten dapat memperkenalkan dirinya sebagai Asisten Akademik Resmi UNSRAT secara instan.
* **Perubahan Teknis:**
  - `src/router.py`: Menambahkan pola `IDENTITY_PATTERNS` dan generator teks template resmi yang memuat profil sistem, cakupan basis data (Peraturan Rektor No. 01 Tahun 2025), dan disclaimer akademik.
  - Menambahkan penanganan fallback yang aman jika pertanyaan ambigu agar tetap diarahkan ke RAG retriever.

---

### Commit 4: `e8fccb1`
* **Pesan Commit:** `feat(ui): isolasi widget portal INSPIRE, hapus chips rekomendasi, dan buat bubble sambutan resmi`
* **Tanggal:** 13 September 2026, 21:05:23 WITA
* **Files:** `static/demo/css/inspire-chat.css`, `static/demo/index.html`, `static/demo/js/inspire-chat.js`, `tests/integration/test_demo_serving.py`
* **Tujuan & Konteks:**
  Langkah awal isolasi CSS/JS khusus untuk antarmuka demo Portal INSPIRE, membuang badge statis lama yang tidak kontekstual, dan menyusun bubble sambutan bertema portal INSPIRE.
* **Perubahan Teknis:**
  - Menciptakan `inspire-chat.css` dan `inspire-chat.js` dengan isolasi kelas `.rag-*`.
  - Mengganti latar belakang iframe menjadi `src="/inspire-unsrat-ac-id.html"`.
  - Merancang struktur awal header modal dengan logo UNSRAT dan tombol aksi dasar.

---

### Commit 5: `2f393f9`
* **Pesan Commit:** `feat(ui): checkpoint isolasi frontend portal inspire dan unsratacid`
* **Tanggal:** 14 September 2026, 20:38:20 WITA
* **Files:** `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`, `static/demo/unsratacid/css/unsratacid.css`, `static/demo/unsratacid/js/unsratacid.js`, `static/demo/index.html`, `static/demo/unsratacid.html`, `docs/superpowers/specs/2026-09-14-inspire-mobile-first-design.md`, `tests/integration/test_demo_serving.py`
* **Tujuan & Konteks:**
  Restrukturisasi direktori secara formal ke dalam folder terisolasi: `static/demo/inspire/` untuk antarmuka baru dan `static/demo/unsratacid/` untuk antarmuka legacy. Menyusun dokumen spesifikasi desain Mobile-First.
* **Perubahan Teknis:**
  - Mengorganisir aset ke folder masing-masing tanpa ada saling ketergantungan (*zero coupling*).
  - Menetapkan variabel token CSS (`--rag-primary: #7B2D2D`, `--rag-bg-canvas: #FAF9F6`, `--rag-border: #E4DFD9`).
  - Menulis spesifikasi desain `2026-09-14-inspire-mobile-first-design.md`.

---

### Commit 6: `cd99bfa`
* **Pesan Commit:** `feat(ui): implement mobile fullscreen shell and trigger button hide on open`
* **Tanggal:** 14 September 2026, 20:47:58 WITA
* **Files:** `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Mengatasi tabrakan visual tombol pemicu (*floating action button*) yang menutupi formulir input chat pada layar smartphone.
* **Perubahan Teknis:**
  - `inspire.css`: Menambahkan class `.rag-trigger.rag-trigger-hidden` dengan `opacity: 0; pointer-events: none; transform: scale(0.6);`.
  - `inspire.js`: Di dalam `toggleModal(forceState)`, saat modal terbuka (`shouldShow = true`), kelas `.rag-trigger-hidden` otomatis disematkan pada `triggerBtn`, dan dilepas kembali saat modal ditutup.

---

### Commit 7: `d415da8`
* **Pesan Commit:** `feat(ui): implement adaptive welcome state with horizontal pill scroll and uniform desktop cards`
* **Tanggal:** 14 September 2026, 21:04:51 WITA
* **Files:** `static/demo/inspire/css/inspire.css`
* **Tujuan & Konteks:**
  Mendesain ulang 5 topic chips agar adaptif: tidak memakan ruang vertikal di layar ponsel, namun tampil simetris dan elegan di layar komputer.
* **Perubahan Teknis:**
  - **Mobile (`<= 768px`):** `.rag-chips-horizontal` diubah menjadi *horizontal swipeable pill carousel* (`flex-direction: row; flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none;`). Chips berbentuk kapsul (*pill*) `rounded-full` (40px min-height).
  - **Desktop (`> 768px`):** `.rag-modal-compact .rag-chip-btn` ditata menjadi kartu $100\%$ width seragam dengan batas `max-width: 360px`, menghilangkan tepi teks yang tidak beraturan (*jagged edges*).

---

### Commit 8: `e2f4b18`
* **Pesan Commit:** `feat(ui): implement mobile native bottom sheet drawer for citations`
* **Tanggal:** 14 September 2026, 21:14:16 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Mengganti mekanisme expand split-screen desktop yang tidak cocok di mobile menjadi *Bottom Sheet Drawer* native yang meluncur dari bawah.
* **Perubahan Teknis:**
  - `index.html`: Menambahkan elemen `.rag-sheet-drag-handle` dan `#rag-sheet-backdrop`.
  - `inspire.css`: Mengatur `.rag-side-citation-panel` pada mobile sebagai fixed overlay di `bottom: 0`, tinggi `80vh`, `border-radius: 20px 20px 0 0`, dan animasi luncur `translateY(100%)` ke `translateY(0)`.
  - `inspire.js`: Memodifikasi `renderCitations` agar tidak memicu `toggleExpand(true)` jika diakses dari viewport mobile ($\le 768\text{px}$).

---

### Commit 9: `993e022`
* **Pesan Commit:** `docs(superpowers): commit mobile-first implementation plan`
* **Tanggal:** 14 September 2026, 21:22:55 WITA
* **Files:** `docs/superpowers/plans/2026-09-14-inspire-mobile-first-plan.md`
* **Tujuan & Konteks:**
  Mendokumentasikan rencana implementasi SDD (Subagent-Driven Development) 4 tugas untuk rekayasa mobile-first.

---

### Commit 10: `b25118d`
* **Pesan Commit:** `feat(ui): implement mobile peek-through sheet and orchestrated motion choreography`
* **Tanggal:** 14 September 2026, 21:49:59 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Mengubah modal mobile dari fullscreen 100% kaku menjadi *Peek-Through Sheet* (`top: 54px`), menyisakan header Portal INSPIRE di bagian atas tetap terlihat saat presentasi atau ujian skripsi, memberikan kepastian visual bahwa chatbot tertanam di dalam portal INSPIRE.
* **Perubahan Teknis:**
  - `inspire.css`: Menetapkan `top: calc(env(safe-area-inset-top, 0px) + 54px)`, `height: calc(100dvh - 54px)`, `border-radius: 22px 22px 0 0`.
  - Mengimplementasikan kurva transisi geometris `cubic-bezier(0.16, 1, 0.3, 1)` untuk morphing pembukaan modal yang halus tanpa loncatan visual.

---

### Commit 11: `d5cddb0`
* **Pesan Commit:** `style(ui): polish UI/UX micro-details, standardize Lucide icons, and add interactive inline citations`
* **Tanggal:** 15 September 2026, 14:30:08 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Pembersihan total estetika visual: mengganti semua emoji dengan ikon SVG Lucide profesional, menyempurnakan layout header, dan menghadirkan sitasi inline interaktif `[1]`, `[2]` di dalam teks markdown jawaban bot.
* **Perubahan Teknis:**
  - Mengganti seluruh ikon dengan Lucide SVG (`book-open`, `settings`, `refresh-cw`, `x`, `sparkles`, `external-link`).
  - Menambahkan regex parser pada `inspire.js` untuk mendeteksi `[1]`, `[2]` dalam jawaban streaming dan mengubahnya menjadi tombol `<button class="rag-inline-citation">`.

---

### Commit 12: `f401e5a`
* **Pesan Commit:** `feat(ui): polish expand icon axis, reset popover, settings dropdown, and card citations`
* **Tanggal:** 15 September 2026, 15:00:05 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Penyempurnaan detail UI berdasarkan umpan balik pengguna: arah panah ikon expand disesuaikan secara horizontal, pembuatan popover konfirmasi reset chat, dan pembersihan whitespace berlebih pada dropdown pengaturan model.
* **Perubahan Teknis:**
  - `index.html` & `inspire.css`: Merancang `.rag-reset-popover` dengan konfirmasi aksi dua tombol (Batal / Mulai Ulang) dan panah segitiga indikator.
  - Merapikan padding dan grid pada `.rag-settings-dropdown`.
  - Menyesuaikan placeholder textarea menjadi ringkas: *"Ketik pertanyaan disini..."*.

---

### Commit 13: `171a0bc`
* **Pesan Commit:** `feat(ui): implement Option B borderless editorial citations, fix minimize icon, and refine mobile dismissal`
* **Tanggal:** 15 September 2026, 17:34:08 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Merombak total panel sumber rujukan yang sebelumnya dinilai terlalu padat (*overcrowded*). Menghapus tag dan badge teknis retrieval, beralih ke desain **Option B: Borderless Editorial Legal Flow**.
* **Perubahan Teknis:**
  - Menghapus tag *"Regulasi Resmi"*, badge *"Vektor"*, *"BM25"*, dan animasi border glow tebal.
  - Menyusun item rujukan dengan tipografi editorial bersih, pemisah garis 1px `#E4DFD9`, dan nomor sitasi badge `[1]`.
  - Menambahkan efek aktif *Tactile Micro-Nudge Animation* (gesekan lembut 7px ke kanan dan kembali dalam 0.42 detik) yang elegan dan tidak merusak keterbacaan teks.

---

### Commit 14: `ae68c87`
* **Pesan Commit:** `fix(ui): scope inline citations to containing message and preserve per-message sources`
* **Tanggal:** 15 September 2026, 18:33:59 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Menyelesaikan bug di mana menekan sitasi `[1]` pada pesan chat lama malah membuka data sitasi dari pesan chat terbaru.
* **Perubahan Teknis:**
  - `inspire.js`: Menambahkan `this.state.messageSourcesMap = new Map()` di state management.
  - Setiap pesan bot diberi atribut unik `data-msg-id="rag-msg-${Date.now()}"`.
  - Tombol sitasi inline `[1]` disematkan atribut `data-msg-id`. Saat diklik, script mengambil array rujukan spesifik milik pesan tersebut dari `messageSourcesMap`, bukan dari variabel global.

---

### Commit 15: `caa4562`
* **Pesan Commit:** `fix(ui): choreograph scroll-then-nudge animation and implement fluid inline metadata breadcrumbs`
* **Tanggal:** 15 September 2026, 19:05:34 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Menata metadata hierarki hukum (BAB, Bagian, Pasal) agar tidak kaku di sisi kiri, serta memperbaiki urutan animasi agar efek micro-nudge tidak terlewat saat viewport panel sedang melakukan scrolling ke item target.
* **Perubahan Teknis:**
  - **Fluid Inline Breadcrumb:** Metadata dipecah menjadi path horizontal yang mengalir: `<div class="rag-editorial-path"><span class="rag-path-bab">BAB XII</span> / <span class="rag-path-bagian">Bagian 12</span> / <span class="rag-path-pasal-pill">Pasal 55</span></div>`.
  - **Koreografi Scroll-Then-Nudge:** Script memeriksa apakah item sudah terlihat di viewport. Jika belum, script melakukan `scrollTo({ top, behavior: 'smooth' })`, memasang listener event `scrollend` (dengan timer fallback dinamis), dan baru memicu class `.rag-citation-highlighted` tepat setelah scroll berhenti.

---

### Commit 16: `3f9ebb5`
* **Pesan Commit:** `fix(ui): eliminate cross-chat citation desync race condition and fix top scroll alignment`
* **Tanggal:** 15 September 2026, 19:24:20 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Menghilangkan kondisi balapan (*race condition*) sinkronisasi state sitasi multi-turn dan memastikan klik sitasi `[1]` selalu mengalirkan viewport ke puncak container (`scrollTop = 0`) tanpa tersangkut di tengah.
* **Perubahan Teknis:**
  - Menambahkan tracking `this.state.displayedMsgId` pada elemen `#rag-side-citation-panel`.
  - Pengecekan `isAlreadyDisplayingSameSources` kini memvalidasi kesamaan `displayedMsgId`. Jika berpindah antar chat, panel dirender ulang secara sinkron sebelum scrolling dilakukan.
  - Perhitungan `targetScrollTop` untuk indeks pertama dikunci pasti di `0px`.

---

### Commit 17: `324afb2`
* **Pesan Commit:** `feat(ui): implement mobile swipe-down gesture to dismiss bottom sheet drawer`
* **Tanggal:** 15 September 2026, 20:48:38 WITA
* **Files:** `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Mengimplementasikan gestur sentuh swipe-down pada drag handle mobile bottom sheet untuk menutup panel secara natural.
* **Perubahan Teknis:**
  - `inspire.js`: Menggunakan Pointer Events (`pointerdown`, `pointermove`, `pointerup`) dengan `setPointerCapture(e.pointerId)`.
  - Tracking delta gerakan jari secara linier dan menerapkan pemudaran opasitas backdrop proporsional.
  - Threshold 80px: geser $> 80\text{px}$ menutup panel; $< 80\text{px}$ memantulkan kembali (*snap-back*).

---

### Commit 18: `64797ae`
* **Pesan Commit:** `fix(ui): resolve mobile bottom sheet backdrop stacking context and finalize swipe-down gesture`
* **Tanggal:** 15 September 2026, 21:30:59 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`
* **Tujuan & Konteks:**
  Menyelesaikan bug kritis di mana saat sumber rujukan dibuka di mobile, layar menjadi gelap total dan setiap tap langsung menutup drawer.
* **Diagnosa & Solusi (*The Stacking Context Trap*):**
  - `#rag-modal` memiliki `isolation: isolate` dengan `z-index: 999999`.
  - `#rag-sheet-backdrop` sebelumnya berada di luar `#rag-modal` dengan `z-index: 1000001`, sehingga browser merender backdrop hitam di depan seluruh isi modal termasuk di depan drawer.
  - **Solusi:** Memindahkan `#rag-sheet-backdrop` ke dalam `#rag-modal` sebagai saudara kandung drawer, dengan `z-index: 100` untuk backdrop dan `z-index: 200` untuk drawer.

---

### Commit 19: `effbad4`
* **Pesan Commit:** `fix(ui): unify mobile backdrop dimming and add solid bottom bleed with elastic stretch to citation bottom sheet`
* **Tanggal:** 15 September 2026, 23:38:06 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Menyatukan efek redup pada seluruh layar mobile (Portal INSPIRE di atas 54px + chatbox di belakang) agar tidak tampak terpecah dan terputus.
* **Perubahan Teknis:**
  - Menambahkan kelas koordinasi `.rag-citations-active` pada overlay layar penuh (`#rag-modal-overlay`).
  - Menetapkan nilai warna gelap yang identik (`rgba(15, 12, 10, 0.64)`) pada overlay portal dan backdrop chat.
  - Sinkronisasi realtime pemudaran opasitas kedua backdrop saat panel ditarik ke bawah.

---

### Commit 20: `48b42dd`
* **Pesan Commit:** `fix(ui): implement dynamic height expansion and snap points for mobile bottom sheet drawer`
* **Tanggal:** 15 September 2026, 23:46:55 WITA
* **Files:** `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, `static/demo/inspire/js/inspire.js`
* **Tujuan & Konteks:**
  Menyelesaikan masalah saat drawer ditarik ke atas: bagian bawah menjadi ruang kosong dan header keluar menabrak batas atas.
* **Diagnosa & Solusi (*Dynamic Height Expansion & Dual-Snap Points*):**
  - Mengubah logika tarik atas: bukan lagi menggeser posisi koordinat elemen (`translateY`), melainkan **menambah tinggi fisik aktual (`height`)** drawer dari dasar layar (`bottom: 0`).
  - Kontainer konten `.rag-side-citation-body` (dengan `flex: 1; overflow-y: auto;`) secara otomatis memanjang dan langsung menampilkan isi teks rujukan (`editorial-passage`) lebih banyak tanpa celah kosong.
  - Header dikunci secara presisi di puncak drawer dan dibatasi maksimum pada `calc(100dvh - 54px)`, sehingga tidak pernah keluar dari area pandang.
  - Menghadirkan **Dual-Snap Points** ($75\text{vh} \leftrightarrow \text{Full Height}$).

---

### Commit 21: `b5dea38`
* **Pesan Commit:** `docs: add comprehensive frontend migration and design evolution report`
* **Tanggal:** 15 September 2026, 23:53:05 WITA
* **Files:** `docs/laporan-migrasi-frontend-inspire.md`
* **Tujuan & Konteks:**
  Mendokumentasikan seluruh laporan arsitektur, evolusi desain, dan hasil pengujian branch `revisi/migrasi-ui-inspire` ke dalam file dokumentasi resmi repositori.

---

## 3. Rangkuman Metrik & Verifikasi Kualitas Akhir

* **Total Commit:** 21 commits
* **Pengujian Integrasi Server:** `pytest tests/integration/test_demo_serving.py` $\to$ **3 PASSED (100%)**
* **Pengujian Unit & Sapaan Router:** `pytest tests/unit/test_router.py tests/integration/test_chat_greeting.py` $\to$ **100% PASSED**
* **Preservasi Mockup Legacy `/unsratacid`:** **100% UNTOUCHED (0 byte delta)**
* **Validasi Sintaksis JS:** `node -c static/demo/inspire/js/inspire.js` $\to$ **Syntax OK (0 error)**
* **Knowledge Graph Codebase:** `graphify update .` $\to$ **2074 nodes, 2337 edges, 293 communities synchronized**
