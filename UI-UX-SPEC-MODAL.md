# Spesifikasi UI/UX Modal Chatbot — Demo UNSRAT

> Dokumen ini adalah pelengkap `IMPLEMENTASI-DEMO-UNSRAT.md` (fokus arsitektur/routing) — khusus mendalami desain interaksi & visual modal chatbot yang menjadi inti fitur penelitian. Ditulis untuk AI coding agent yang akan mengimplementasikan `chat-widget.js` dan `demo-modal.css` versi final.
>
> **Untuk AI coding agent**: dokumen ini membedakan **keputusan final (hard constraint, tidak boleh diubah tanpa konfirmasi user)** vs **area terbuka untuk brainstorming lanjutan (soft/open, silakan diusulkan penyempurnaan)** — ditandai eksplisit di tiap bagian. Ikuti protokol deviasi yang sudah ditetapkan di `IMPLEMENTASI-DEMO-UNSRAT.md` Bagian 7a untuk penyimpangan apa pun.

---

## 1. Token Desain (Palet Warna & Style Dasar)

**[HARD CONSTRAINT]** Palet warna **wajib mengikuti** yang sudah dipakai di `static/index.html` (`/testing`) — bukan warna baru — supaya identitas visual chatbot konsisten antara versi awal dan versi demo. Diverifikasi langsung dari kode `app.js` lama:

| Token                  | Hex                                                   | Penggunaan                                          |
| ------------------------| -------------------------------------------------------| -----------------------------------------------------|
| Primary (maroon)       | `#7B2D2D`                                             | Header modal, bubble user, tombol utama, ikon aktif |
| Primary hover          | `#963E3E`                                             | Hover state tombol/bubble gradient                  |
| Primary active/pressed | `#5C1F1F`                                             | Active/pressed state tombol                         |
| Netral hangat terang   | `#FAF9F6`                                             | Background header citation, area sekunder           |
| Netral hangat border   | `#E4DFD9`                                             | Border pemisah antar section                        |
| Amber (peringatan)     | `amber-700` / `amber-50` (Tailwind default)           | Notifikasi "dibatalkan pengguna"                    |
| Merah (error)          | `red-600` / `red-100` / `red-700` (Tailwind default)  | Bubble error                                        |
| Stone/gray netral      | `gray-700`, `gray-900`, `gray-100` (Tailwind default) | Teks & border umum                                  |

`demo-modal.css` yang sudah ada (menggunakan `#7B2D2D`, `#5A1F1F`, palet stone) **sudah cukup selaras** — hanya perlu penyesuaian kecil: warna active/pressed disamakan persis ke `#5C1F1F` (bukan `#5A1F1F` yang sedikit berbeda dari token asli), dan warna citation header disamakan ke `#FAF9F6`/`#E4DFD9` (bukan `#faf9f6`/`#e7e5e4` generik yang saat ini dipakai — hex-nya sangat mirip tapi sebaiknya persis sama dengan sumber aslinya untuk konsistensi 1:1).

---

## 2. Mode Ukuran Modal: Compact ↔ Expanded

**[HARD CONSTRAINT — sudah difinalkan]**

Dua mode, ditoggle lewat satu tombol expand/collapse di header (bukan navigasi halaman baru, tetap dalam bentuk modal/dialog):

| Mode                  | Ukuran                                                                                                                                                                                    | Kapan aktif                                                                                                |
| -----------------------| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------------------------------------------------------|
| **Compact** (default) | Sesuai `demo-modal.css` saat ini (~420px lebar, 580px tinggi, kanan-bawah)                                                                                                                | State awal saat modal pertama dibuka                                                                       |
| **Expanded**          | 80-90% viewport (lebar & tinggi), tetap sebagai overlay dialog di tengah homepage — **bukan** 100% (homepage tetap terlihat sedikit di tepi atas/bawah/kiri/kanan sebagai konteks visual) | User klik tombol expand, ATAU otomatis saat user membuka panel citation dari mode compact (lihat Bagian 5) |

**Aturan transisi (asimetris, disengaja):**
- Compact → Expanded bisa terjadi otomatis (dipicu klik citation) maupun manual (tombol expand).
- Expanded → Compact **hanya** terjadi lewat aksi eksplisit user (klik tombol collapse) — sistem tidak pernah mengecilkan modal sendiri, termasuk saat panel citation ditutup. Prinsip: sistem boleh proaktif memberi ruang lebih, tapi tidak boleh mengambilnya kembali tanpa izin.
- Transisi ukuran pakai CSS `transition` pada `width`/`height`/`inset` (durasi ~250-300ms, easing standar), bukan snap instan.
- Backdrop overlay: **[OPEN untuk brainstorming lanjut]** gunakan `backdrop-filter: blur(4px)` pada overlay di mode expanded. **Peringatan performa yang wajib diperhatikan**: `unsrat-ac-id.html` memuat RevSlider dengan autoplay carousel — blur pada elemen yang menutupi konten beranimasi berpotensi menyebabkan repaint mahal tiap frame. Radius blur kecil (4px) dipilih untuk meminimalkan risiko ini, tapi **wajib diuji langsung di perangkat yang dipakai demo** sebelum dianggap final. Opsi lanjutan (opsional, butuh eksplorasi API RevSlider saat implementasi): pause autoplay slider (`revapi.revpause()` jika instance dapat diakses) saat modal dibuka, resume saat ditutup — ini menghilangkan sumber masalah performa sepenuhnya, tapi belum diverifikasi apakah API tersebut accessible dari luar di instance RevSlider halaman ini. Agent silakan eksplorasi dan validasi saat implementasi, laporkan temuan jika API ternyata tidak dapat diakses.

---

## 3. Header Modal

**[HARD CONSTRAINT — urutan & isi sudah difinalkan]**

Urutan tombol aksi di header (kiri ke kanan, sejajar): **Settings (gear) → Reset Percakapan → Expand/Collapse → Close (X)**.

- Judul modal + status badge tetap di sisi kiri header (sesuai desain sekarang).
- **Reset percakapan** ditaruh sejajar tombol lain di header (bukan di dekat form input) — sesuai keputusan eksplisit user.
- Ikon Expand/Collapse berubah sesuai state (`maximize-2` saat compact → `minimize-2` saat expanded, dari lucide).

**Config/Model select — [HARD CONSTRAINT soal keberadaan, OPEN soal detail styling]:**
- Tetap dipertahankan di dalam panel settings (dropdown/accordion dari tombol gear), **bukan dihapus**.
- **Wajib diimplementasikan dengan satu toggle terpusat** supaya mudah disembunyikan kapan pun tanpa harus comment-out banyak baris tersebar. Rekomendasi konkret: satu konstanta di awal `chat-widget.js`, misal:
  ```js
  const FEATURE_FLAGS = {
    showConfigModelSelect: true // set false untuk sembunyikan dari UI publik, tanpa hapus kode
  };
  ```
  lalu render tombol settings & panel-nya secara kondisional berdasar flag ini di `init()`/`cacheElements()`. Ini lebih aman daripada comment manual (satu titik kontrol, tidak ada risiko lupa comment sebagian, mudah di-toggle ulang kapan saja termasuk saat sidang).

---

## 4. State Machine Chat & Perbaikan Stop-Streaming

**[HARD CONSTRAINT — perilaku stop-streaming sudah difinalkan berdasarkan permintaan eksplisit]**

### 4a. Masalah pada kode lama (terverifikasi dari `app.js`, bukan asumsi)

Ditemukan **duplikasi logic abort di dua listener terpisah** (`sendBtn` click handler dan `chatForm` submit handler melakukan hal yang identik) — pelanggaran DRY, rapuh karena bergantung pada urutan event yang implisit. Perbaikan wajib untuk widget baru:

- Satu state eksplisit: `state.status = 'idle' | 'streaming'` (ganti dua boolean terpisah `isStreaming`/`isUserAborted` yang berisiko tidak sinkron).
- **Satu titik masuk** untuk aksi kirim/stop — baik dari submit form maupun klik tombol kirim/stop memanggil fungsi yang sama, tidak ada logic yang ditulis dua kali.
- Tombol kirim/stop sebaiknya `type="button"` (bukan `type="submit"`), submit form murni ditangani lewat satu `submit` listener yang memanggil fungsi tunggal itu — menghilangkan ambiguitas urutan click-vs-submit.

### 4b. Perilaku stop-streaming yang diminta

Saat user menekan stop di tengah streaming:
1. Stream di-abort (`abortController.abort()`).
2. **Teks yang sudah ter-generate sampai token terakhir TETAP ditampilkan** — tidak dihapus/dikosongkan.
3. Tambahkan **keterangan eksplisit** di bawah teks yang sudah ada bahwa jawaban dibatalkan pengguna (bukan error, bukan jawaban tidak lengkap yang tidak dijelaskan).

Ini **persis pola yang sudah ada di `app.js` lama** (baris ~620-646, blok `catch (err) { if (err.name === 'AbortError') ... }`) — kode itu sudah menangani ini dengan benar: mempertahankan `fullResponseText` yang sudah ter-generate, lalu append keterangan italic beraksen amber ("Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap."). **Port logic ini apa adanya ke `chat-widget.js`**, sesuaikan class ke skema class widget baru (`rag-` prefix), jangan ditulis ulang dari nol — perilakunya sudah benar dan sesuai permintaan Anda.

Bedakan juga dua sub-kasus (sudah tercakup di kode lama, pastikan tetap ada di widget baru):
- **Abort setelah ada token masuk**: tampilkan teks parsial + keterangan dibatalkan (seperti dijelaskan di atas).
- **Abort sebelum token pertama masuk** (masih fase "mengetik...212"): tampilkan pesan singkat bahwa pencarian dihentikan sebelum ada jawaban, tanpa teks kosong yang membingungkan.

---

## 5. Panel Rujukan Dokumen (Citation)

**[HARD CONSTRAINT — interpretasi & trigger sudah difinalkan]**

- Interpretasi **(b)**: tiap bubble jawaban punya tombol/trigger sendiri ("Lihat N Rujukan"), membuka **satu panel yang sama** di sisi kanan modal (bukan satu panel global lepas dari konteks jawaban).
- **Trigger otomatis expand**: jika modal masih dalam mode compact saat tombol rujukan diklik, modal otomatis pindah ke mode Expanded terlebih dahulu (dengan transisi smooth, lihat Bagian 2), baru panel citation slide-in dari kanan. Kalau modal sudah dalam mode Expanded, citation panel langsung terbuka tanpa resize tambahan.
- Panel citation slide-in/out dengan transisi CSS (`transform: translateX()`), bisa ditutup lewat tombol close di panel itu sendiri atau klik di luar panel (dalam area modal, bukan overlay luar modal).
- **[OPEN untuk brainstorming lanjut]**: apakah panel citation menggantikan total lebar chat area (overlay di atasnya) atau chat area menyempit menyisakan ruang untuk panel side-by-side? Dua pola ini sama-sama valid (gaya Claude.com condong ke side-by-side dengan chat menyempit). Rekomendasi awal: side-by-side (chat area menyempit) di mode Expanded karena ruang sudah cukup lebar (80-90vw) untuk menampung keduanya tanpa terasa sempit — tapi ini area yang boleh disempurnakan agent saat implementasi berdasarkan hasil uji visual nyata.

---

## 6. Detail Bubble Pesan

**[HARD CONSTRAINT]**

Port dari pola `app.js` lama, elemen per bubble (user maupun bot):
- **Timestamp** di setiap bubble (format `HH:MM`, fungsi `getTimestamp()` — port apa adanya, sudah benar dan sederhana).
- Bubble bot: avatar ikon di kiri (icon `award` atau serupa, background primary).
- Bubble user: avatar ikon di kanan (icon `user`, background putih/border netral), rata kanan.
- Animasi masuk halus (`opacity` + `translate-y` transition saat bubble baru ditambahkan) — sudah ada polanya di kode lama, pertahankan.

---

## 7. Input Area (Textarea Auto-Grow)

**[HARD CONSTRAINT soal port logic, OPEN soal max-height persis]**

- Ganti elemen input dari `<input type="text">` (kondisi `chat-widget.js` saat ini) menjadi **`<textarea rows="1">`**.
- Port logic `adjustHeight()` dari `app.js` lama apa adanya (reset ke `auto` sebelum baca `scrollHeight` — pola yang sudah benar, memastikan textarea bisa mengecil lagi saat teks dihapus).
- Enter untuk submit, Shift+Enter untuk baris baru — port apa adanya.
- **Tambahan wajib** (belum ada di kode lama, spesifik untuk konteks modal yang ruang vertikalnya terbatas dibanding SPA penuh): cap `max-height` (rekomendasi awal `120px`, **OPEN untuk disesuaikan** agent berdasar hasil uji visual) dengan `overflow-y: auto` setelah mencapai batas, supaya textarea tidak mendorong tombol kirim/header keluar area modal saat user mengetik paragraf panjang.

---

## 8. Welcome State

**[OPEN untuk brainstorming lanjut — placeholder disediakan, isi final didiskusikan lagi]**

- Welcome message **center-aligned** secara visual (sesuai usulan awal user), berbeda dari kondisi lama yang left-aligned mengikuti alur bubble percakapan biasa — welcome state secara konsep bukan "pesan dari bot" melainkan layar sambutan, jadi wajar diperlakukan sebagai blok tersendiri di tengah area chat.
- **Quick-question chips** — 4 placeholder awal (diambil dari `clearChatUI()` kode lama, baris 167-182, sudah terbukti relevan secara akademik):
  1. "Syarat cuti akademik?"
  2. "Visi dan Misi UNSRAT?"
  3. "Beban SKS semester 1?"
  4. "Mekanisme evaluasi DO?"
  
  **Rekomendasi dari saya (silakan disesuaikan)**: pertimbangkan menambah 1-2 chip yang lebih spesifik ke skenario "layanan informasi akademik" sesuai judul skripsi Anda — misal soal KRS atau kalender akademik — supaya cakupan contoh pertanyaan merepresentasikan lebih luas kategori yang didukung sistem, bukan hanya seputar cuti/DO/SKS. Ini murni saran, bukan keharusan.
- Klik chip mengisi textarea (port fungsi `fillInput` lama) — **[OPEN]**: apakah klik chip langsung auto-submit pertanyaan, atau hanya mengisi textarea dan user masih perlu menekan kirim (perilaku saat ini)? Pola lama hanya mengisi, tidak auto-submit. Direkomendasikan tetap begitu (memberi user kesempatan mengedit/membatalkan sebelum terkirim), tapi ini bisa didiskusikan lagi kalau Anda menginginkan interaksi lebih cepat.

---

## 9. Non-Goals (Eksplisit Di Luar Scope Tahap Ini)

Supaya AI coding agent tidak scope-creep saat "menyempurnakan" desain:
- Animasi indikator mengetik 3-dot-bounce: menarik, **tapi bukan prioritas sekarang** (dikonfirmasi user) — indikator teks sederhana ("Mengetik...") sudah cukup untuk versi ini.
- Tombol copy jawaban, regenerate jawaban: tidak diminta, jangan ditambahkan tanpa konfirmasi.
- Voice input, feedback thumbs up/down, sessionStorage persistence: sudah diputuskan di luar scope pada iterasi brainstorming sebelumnya, tetap berlaku.
- Mengubah field/endpoint backend: tetap terlarang keras sesuai `IMPLEMENTASI-DEMO-UNSRAT.md` Bagian 7.

---

## 10. Ringkasan untuk Agent: Apa yang Boleh Disempurnakan Lebih Lanjut

Bagian yang ditandai **[OPEN]** di atas (radius/pendekatan blur backdrop, layout side-by-side vs overlay untuk panel citation, angka persis `max-height` textarea, isi akhir quick-question chips, perilaku auto-submit chip) adalah area sah untuk agent mengusulkan penyempurnaan berdasarkan hasil implementasi & uji visual nyata — **dengan syarat**: usulan didokumentasikan (commit message atau `CHANGES.md`, sesuai protokol Bagian 7a di dokumen implementasi utama) dan tidak melanggar bagian **[HARD CONSTRAINT]** mana pun di dokumen ini tanpa konfirmasi eksplisit dari user terlebih dahulu.
