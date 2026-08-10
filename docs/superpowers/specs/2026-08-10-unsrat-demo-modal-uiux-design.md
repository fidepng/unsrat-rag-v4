# Design Spec: Refinsi UI/UX Modal Chatbot UNSRAT

> **Status**: APPROVED BY USER  
> **Tanggal**: 10 Agustus 2026  
> **Target Berkas**: `static/demo/index.html`, `static/demo/css/demo-modal.css`, `static/demo/js/chat-widget.js`  
> **Tujuan Utama**: Meningkatkan estetika visual & ergonomi interaksi modal chatbot UNSRAT secara modular, bebas kedipan (*no blinking*), presisi layout 1:1, dan teruji zero-regression.

---

## 1. Arsitektur Komponen & State Engine Terisolasi

Widget chatbot dikembangkan menggunakan skema modular terenkapsulasi dalam namespace `RagChatWidget` di `chat-widget.js`:

```
RagChatWidget
├── State Engine (status, mode, currentConfig, currentModel, chatHistory, citations)
├── View Renderer (Header, WelcomeBody, MessagesList, CitationPanel, TextareaForm)
└── Event Controller (FormSubmit, AbortStream, ToggleExpand, ToggleSettings, ClearChat)
```

### 1.1 Token Warna (100% Konsisten dengan SPA `/testing`)
* **Primary Maroon**: `#7B2D2D` (Header modal, bubble user, tombol utama, ikon aktif)
* **Primary Hover**: `#963E3E`
* **Primary Active/Pressed**: `#5C1F1F`
* **Netral Hangat Terang**: `#FAF9F6` (Background header rujukan & area sekunder)
* **Netral Hangat Border**: `#E4DFD9` (Border pemisah section)
* **Status Amber**: `amber-700` / `amber-50` (Badge pembatalan stream pengguna)
* **Status Merah**: `red-600` / `red-100` (Badge error)
* **Status Hijau**: `emerald-500` / `emerald-100` (Indikator status online)

---

## 2. Mode Ukuran Modal: Compact ↔ Expanded

| Mode | Dimensi & Posisi | Trigger Aktif |
| :--- | :--- | :--- |
| **Compact** *(default)* | Lebar `420px`, tinggi `580px`, melayang kanan-bawah (`bottom: 90px; right: 24px`) | Modal dibuka pertama kali |
| **Expanded** | Lebar `85vw`, tinggi `85vh`, posisi tengah (`top: 50%; left: 50%; transform: translate(-50%, -50%)`) | Klik tombol Expand ATAU klik tombol *Rujukan Dokumen* saat Compact |

### 2.1 Aturan Transisi Asimetris
* **Compact → Expanded**: Terjadi otomatis saat tombol Expand (`maximize-2`) atau tombol *Rujukan Dokumen* diklik.
* **Expanded → Compact**: **Hanya** terjadi lewat klik manual tombol Collapse (`minimize-2`). Sistem tidak pernah mengecilkan modal sendiri.
* **Animasi CSS**: Menggunakan `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)` untuk gerakan membesar/mengecil tanpa *diagonal jump*.
* **Backdrop Overlay**: `background: rgba(0, 0, 0, 0.45)` tanpa heavy `backdrop-filter: blur()` untuk menjamin kinerja 60 FPS bebas lag pada slider/video background UNSRAT.

---

## 3. Header Modal, Window Controls, & Feature Flag

### 3.1 Ikon & Branding
* **100% Lucide Icons (`data-lucide="..."`)**: Dilarang menggunakan emoji Unicode.
* **Logo UNSRAT**: Menggunakan logo resmi `/static/assets/logo-unsrat.png` di dalam *Welcome Body Card*.

### 3.2 Tata Letak Header Modal
* **Top-Left (Kiri)**: Tombol **Maximize / Minimize (`maximize-2` / `minimize-2`)**.
* **Tengah**: Judul *"Asisten Akademik UNSRAT"*.
* **Top-Right (Kanan, Kiri ke Kanan)**:
  1. **Settings (`settings`)**: Toggle collapsible panel parameter.
  2. **Reset Percakapan (`rotate-ccw`)**: Mengosongkan UI & riwayat percakapan.
  3. **Close (`x`)**: Menutup modal.

### 3.3 Feature Flag Parameter System
```javascript
const FEATURE_FLAGS = {
  showConfigModelSelect: true // Jika set false, panel settings tersembunyi dari UI
};
```
* **Zero-Error Fallback**: State `currentConfig = 'b'` dan `currentModel = 'gemini-3.5-flash'` disimpan independen di memori JS. Jika flag `false`, sistem tetap mengirim nilai default tanpa throw `TypeError: null`.

---

## 4. Welcome State & Quick-Question Chips

* **Layout Welcome Body**: Center-aligned dengan Logo UNSRAT di tengah dan deskripsi singkat layanan AI akademik.
* **Daftar 5 Chips Pertanyaan Cepat**:
  1. `<i data-lucide="book-open"></i>` *"Syarat cuti akademik?"*
  2. `<i data-lucide="compass"></i>` *"Visi dan Misi UNSRAT?"*
  3. `<i data-lucide="layers"></i>` *"Beban SKS semester 1?"*
  4. `<i data-lucide="alert-triangle"></i>` *"Mekanisme evaluasi DO?"*
  5. `<i data-lucide="file-text"></i>` *"Prosedur pengisian KRS?"*
* **Perilaku Klik (Auto-Submit)**: Mengklik chip mana pun langsung mengisi teks dan **otomatis mengirimkan pertanyaan** ke backend secara instan.

---

## 5. State Machine Chat & Stop-Streaming Logic

* **State**: `state.status = 'idle' | 'streaming'`.
* **Single Entry Point**: Handler tombol submit/stop tunggal.
* **Penanganan Stop Streaming**:
  * Memanggil `abortController.abort()`.
  * **Mempertahankan teks parsial** yang sudah ter-generate.
  * **Jika token sudah masuk**: Menambahkan badge amber (`alert-circle` Lucide): *"Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap."*
  * **Jika belum ada token** (fase "Mengetik..."): Menampilkan pesan singkat bahwa pencarian dihentikan sebelum ada jawaban.

---

## 6. Panel Rujukan Dokumen Akademik (Citation Panel)

* **Trigger**: Tombol `book-open` *"Rujukan Dokumen Akademik (N Sumber)"* pada tiap bubble bot.
* **Auto-Expand**: Mengklik rujukan saat modal *Compact* otomatis mengubah mode ke *Expanded (85vw/85vh)* via CSS transition.
* **Responsif Layout**:
  * **Desktop (>=1024px)**: Layout **Side-by-Side** (Chat 60% : Panel Rujukan 40%).
  * **Mobile (<1024px)**: Layout **Overlay Sheet** penuh dengan tombol `arrow-left` *"Kembali ke Chat"*.
* **Konten Rujukan**: Judul Peraturan Rektor, Nomor/Tahun, Badge ID (Bab/Pasal), dan kutipan (*snippet*) teks landasan hukum akademik.

---

## 7. Input Area (`<textarea>` Auto-Grow & Mobile UX)

* Menggantikan `<input type="text">` dengan **`<textarea rows="1">`**.
* **Auto-Grow (`adjustHeight`)**: Tinggi textarea bertambah otomatis sesuai baris teks (max-height `120px`, `overflow-y: auto`). Mengecil kembali saat teks dihapus.
* **Navigasi Key**: `Enter` = Kirim, `Shift + Enter` = Baris Baru.
* **Mobile Viewport**: Menggunakan `100dvh` (*dynamic viewport height*) agar form input tidak tertutup keyboard virtual pada perangkat seluler.

---

## 8. Protokol Verifikasi & Testing (Playwright E2E)

Sebelum klaim selesai, pengujian E2E Playwright dijalankan untuk memverifikasi:
1. Precision layout homepage UNSRAT (1170px width).
2. Transisi mode Compact ↔ Expanded.
3. Auto-Submit *Quick-Question Chips*.
4. Streaming tanpa kedipan (*no blinking*).
5. Slide-in & Side-by-Side *Citation Panel*.
6. Stop streaming & penanganan teks parsial.
7. Feature flag `showConfigModelSelect` (true & false).
