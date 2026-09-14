# Spesifikasi Desain: Migrasi Mobile-First & Adaptive Hybrid Chatbot Widget UNSRAT (Portal INSPIRE)

**Tanggal:** 2026-09-14  
**Status:** Draf Tervalidasi (Ready for Review)  
**Target:** Endpoint `/` (Portal INSPIRE)  
**File Terdampak:**  
- `static/demo/index.html`  
- `static/demo/inspire/css/inspire.css`  
- `static/demo/inspire/js/inspire.js`  

---

## 1. Latar Belakang & Masalah (Problem Statement)

Portal INSPIRE (`/`) saat ini mengimplementasikan widget chatbot akademik dengan pendekatan **Desktop-First**. Ketika diakses melalui perangkat smartphone (viewport mobile, misalnya `375 × 667 px`), ditemukan 4 masalah UI/UX kritis berdasarkan audit Playwright dan Impeccable Design Review:

1. **Ukuran Window Tidak Pas di Layar Ponsel:**  
   Widget berstatus `.rag-modal-compact` dengan margin tetap (`bottom: 96px; right: 36px; max-width: calc(100vw - 48px)`), sehingga melayang canggung seperti kartu desktop mini dengan latar belakang portal mengintip di tepian. Tombol resize/expand (`#rag-expand-btn`) masih muncul padahal di mobile mode expand tidak relevan.
2. **Tabrakan Hitbox Kritis (Trigger vs Send Button):**  
   Tombol pemicu mengambang `#rag-trigger-btn` (`z-index: 1000000`, posisi `bottom: 28px; right: 36px`) tidak pernah disembunyikan saat modal terbuka. Di mobile, posisinya menempati area koordinat yang sama persis dengan tombol kirim (`#rag-send-btn`), memicu salah sentuh (accidental tap).
3. **Kerusakan Layout Saat Membuka "Sumber Rujukan":**  
   Menekan tombol `[N] Sumber Rujukan` memicu `toggleExpand(true)` yang memaksa widget desktop ke ukuran `92vw` di tengah layar (`transform: translate(-50%, -50%)`). Panel rujukan lalu menimpa chat secara kaku (`position: absolute; inset: 0`), membuat pengguna kehilangan konteks percakapan dan terperangkap di mode expanded.
4. **Welcome State Kaku & Bergerigi di Mobile:**  
   5 tombol chip topik menggunakan `width: fit-content` yang dipusatkan di tengah (`align-items: center`), menghasilkan tumpukan tombol dengan lebar yang tidak seragam (bergerigi/jagged). Spasi vertikal memakan terlalu banyak tempat sehingga input box tertekan ke bawah.

---

## 2. Batasan & Ruang Lingkup (Scope & Boundaries)

- **Fokus Utama:** 100% pada widget chatbot di portal INSPIRE (`/`).
- **Strictly Untouched:**
  - Portal legacy `/unsratacid` (file `static/demo/unsratacid.html` dan direktori `static/demo/unsratacid/`) **100% tidak boleh disentuh**.
  - Background portal mock (`/inspire-unsrat-ac-id.html`) tetap apa adanya.
  - Backend API (`/api/chat`, `app.py`), retrieval pipeline, konfigurasi RAG, dan evaluasi RAGAS tidak diubah.

---

## 3. Keputusan Arsitektur Desain (Design Decisions)

Berdasarkan brainstorming dan persetujuan pengguna:
1. **Mekanisme Rujukan di Mobile:** **Opsi A (Native Mobile Bottom Sheet Drawer)**.
2. **Topik Welcome State di Mobile:** **Horizontal Scrollable Pill Chips**.
3. **Pendekatan Desktop Compact:** **Opsi 2 (Adaptive Hybrid)** — Desktop compact tetap mempertahankan kenyamanan desktop (kartu topik berlebar seragam, logo 72px, split side-by-side citations, dan trigger button disembunyikan saat modal terbuka).

---

## 4. Rincian Spesifikasi Teknis

### A. Mobile-First Shell (`@media (max-width: 768px)`)
- **Container Window (`#rag-modal`):**
  - Menggunakan layout **Fullscreen App Shell**:
    ```css
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100% !important;
    height: 100% !important;
    height: 100dvh !important;
    max-width: 100vw !important;
    max-height: 100dvh !important;
    border-radius: 0 !important;
    border: none !important;
    box-shadow: none !important;
    transform: none !important;
    ```
  - Input form docked di bagian bawah dengan menghormati safe-area ponsel:
    `padding-bottom: max(12px, env(safe-area-inset-bottom));`
- **Header Actions di Mobile:**
  - Tombol expand `#rag-expand-btn` disembunyikan secara permanen (`display: none !important;`).
  - Sisa elemen header: Judul "Asisten Akademik UNSRAT", tombol panduan `(?)`, gear `settings`, tombol `reset`, dan tombol close `(✕)`.
- **Siklus Hidup Trigger Button (`#rag-trigger-btn`):**
  - Pada `toggleModal()` di `inspire.js`:
    - Saat modal terbuka: Tambahkan class `.rag-trigger-hidden` pada `#rag-trigger-btn` (`opacity: 0; pointer-events: none; transform: scale(0.6);`).
    - Saat modal ditutup: Hapus class `.rag-trigger-hidden`.
  - Aturan ini berlaku baik di mobile maupun desktop untuk menghilangkan visual clutter.

### B. Mobile Bottom Sheet Drawer untuk "Sumber Rujukan"
- **Komponen & Markup:**
  - Menambahkan struktur drawer sheet di dalam `#rag-chatbot-widget` atau memanfaatkan `#rag-side-citation-panel` dengan adaptive CSS.
  - Elemen visual:
    - **Backdrop Sheet:** `.rag-sheet-backdrop` (latar gelap transparan `rgba(0, 0, 0, 0.4)` dengan efek fade-in).
    - **Drag Handle Bar:** Pill abu-abu lembut (`width: 38px; height: 4.5px; border-radius: 3px; background: #D6D0C7; margin: 8px auto 6px auto;`).
    - **Header Sheet:** Judul "Sumber Rujukan (N)" + tombol close `(✕)`.
    - **Body Sheet:** Daftar kartu rujukan akademis (`overflow-y: auto`).
- **CSS di Mobile (`<= 768px`):**
  - `position: fixed; left: 0; right: 0; bottom: 0; height: 80dvh; max-height: 85dvh; border-radius: 20px 20px 0 0; background: #FAF9F6; box-shadow: 0 -12px 36px rgba(0, 0, 0, 0.2); z-index: 100000; transform: translateY(100%); transition: transform 0.28s cubic-bezier(0.32, 0.72, 0, 1);`
  - Class `.rag-sheet-open`: `transform: translateY(0);`.
- **Logika JS (`inspire.js`):**
  - Di mobile (`window.innerWidth <= 768`):
    - Klik `.rag-citation-header` **TIDAK** memanggil `toggleExpand(true)`.
    - Mengaktifkan bottom sheet drawer dan backdrop. Percakapan chat tetap berada di posisi scroll terakhir di latar belakang.
    - Menutup drawer dapat dilakukan via tombol close `(✕)` di sheet, tap pada backdrop, atau tombol Escape.
  - Di desktop (`window.innerWidth > 768`):
    - Tetap memanggil alur split mode (side-by-side) seperti sedia kala.

### C. Welcome State Topik (Adaptive Hybrid)
- **Di Mobile (`<= 768px`):**
  - **Logo UNSRAT:** Diskalakan ke `52px` (hemat vertikal).
  - **Spasi Top:** Margin dan padding dirampingkan dengan irama 8dp.
  - **5 Topik Pertanyaan (Horizontal Scrollable Pill Chips):**
    - Container:
      ```css
      display: flex;
      flex-direction: row;
      flex-wrap: nowrap;
      overflow-x: auto;
      gap: 8px;
      width: 100%;
      padding: 4px 16px 8px 16px;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
      ```
    - Pill button:
      `border-radius: 9999px; white-space: nowrap; padding: 8px 14px; font-size: 12px; min-height: 42px; display: inline-flex; align-items: center; gap: 8px;`
    - Sentuhan pada pill mengisi template ke textarea dan mengaktifkan tombol kirim secara mulus.
- **Di Desktop Compact (`> 768px`):**
  - **Logo UNSRAT:** Tetap `72px` proporsional.
  - **5 Topik Pertanyaan (Uniform Full-Width Cards):**
    - Container: `width: 100%; max-width: 360px; display: flex; flex-direction: column; gap: 8px; align-items: stretch;`
    - Card button: Lebar seragam 100% (`width: 100%; box-sizing: border-box;`), sudut membulat `border-radius: 12px`, teks rata kiri, icon di kiri dan panah chevron kanan rata kanan.
    - Hover state: Halus dengan aksen Maroon UNSRAT (`#7B2D2D`).

---

## 5. Rencana Verifikasi (Verification Plan)

1. **Uji Playwright Viewport Mobile (375 × 667 px & 390 × 844 px):**
   - Verifikasi widget fullscreen tanpa border-radius dan tanpa celah tepi.
   - Verifikasi tombol `#rag-expand-btn` tidak tampak di mobile.
   - Verifikasi `#rag-trigger-btn` tersembunyi saat widget terbuka (bebas tabrakan koordinat dengan tombol send).
   - Verifikasi welcome state: logo 52px, pill chips dapat di-scroll horizontal tanpa memakan ruang vertikal berlebih.
   - Verifikasi Sumber Rujukan: klik rujukan memunculkan Bottom Sheet Drawer 80dvh tanpa mengubah ukuran jendela utama, chat tetap utuh di latar.
2. **Uji Playwright Viewport Desktop (1280 × 800 px):**
   - Verifikasi mode compact tetap floating (`420px × 600px`).
   - Verifikasi kartu topik welcome state rapi dan seragam lebarnya (100% width, tidak bergerigi).
   - Verifikasi klik Sumber Rujukan tetap membuka mode split side-by-side.
   - Verifikasi tombol expand berfungsi normal di desktop.
3. **Uji Non-Regresi `/unsratacid`:**
   - Navigasi ke `/unsratacid` memastikan 100% tampilan dan fungsi legacy tidak mengalami perubahan.
