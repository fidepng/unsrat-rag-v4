# Rencana Implementasi Pembaruan UI/UX RAG Chatbot UNSRAT

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mengganti antarmuka RAG Chatbot UNSRAT saat ini menjadi antarmuka formal akademis premium bertema Maroon Klasik (Variant A) menggunakan Tailwind CSS CDN, Marked.js, dan Lucide Icons dengan 6 fitur UX esensial, panel metadata evaluasi dinamis, dan catatan kaki disclaimer formal bebas emoji dan kategori.

**Architecture:** Antarmuka berbasis Single Page Application (SPA) dual-tab (Chat vs Evaluasi) di mana manipulasi DOM dikelola penuh oleh Vanilla JS. `/api/evaluation` backend FastAPI dimodifikasi secara stateless untuk membagikan parameter pengujian (evaluator, generator, dataset size, last run), dan frontend mengalirkan SSE dengan abort controller.

**Tech Stack:** Tailwind CSS CDN, Google Font Inter, Lucide Icons, Marked.js, Chart.js, FastAPI Backend, Vanilla JS SPA

---

## 🛠️ Daftar Berkas yang Dibuat / Dimodifikasi
*   **Modifikasi**: `app.py` (Pembalikan REST endpoint `/api/evaluation` untuk menyuplai metadata pengujian Ragas)
*   **Modifikasi**: `static/index.html` (Perombakan total struktur layout, DOM, CDN scripts, panel metadata)
*   **Modifikasi**: `static/js/app.js` (Perombakan total logika client-side, SSE streaming, watchdog, render metadata, ekspor clipboard)
*   **Create**: `static/assets/logo-unsrat.png` (Pembuatan folder assets dan logo placeholder)

---

### Task 1: Fondasi Proyek, CDN, & Folder Assets

**Files:**
* Modify: `static/index.html`
* Create: `static/assets/logo-unsrat.png` (placeholder)

- [ ] **Step 1: Buat direktori static/assets dan berkas logo placeholder**
  
  Pastikan folder `static/assets` telah dibuat. Karena logo asli akan diunggah oleh pengguna, buat gambar PNG transparan kosong ukuran 128x128 piksel atau teks placeholder sebagai berkas `logo-unsrat.png`.

- [ ] **Step 2: Muat pustaka eksternal (CDN) di static/index.html**
  
  Buka file `static/index.html`. Hapus seluruh tag `<style>` yang ada (baris 9-92) dan ganti tag `<head>` menjadi struktur bersih dengan memuat Google Font Inter, Tailwind CSS, Lucide Icons, Marked.js, dan Chart.js.

  ```html
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Asisten Informasi Akademik UNSRAT</title>
      <meta name="description" content="Sistem RAG Informasi Regulasi Akademik Universitas Sam Ratulangi">
      <!-- Google Fonts Inter -->
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
      <!-- Tailwind CSS CDN -->
      <script src="https://cdn.tailwindcss.com"></script>
      <!-- Lucide Icons -->
      <script src="https://unpkg.com/lucide@latest"></script>
      <!-- Chart.js -->
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <!-- Marked.js (Markdown Parser UMD) -->
      <script src="https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js"></script>
      
      <script>
          tailwind.config = {
              theme: {
                  extend: {
                      fontFamily: {
                          sans: ['Inter', 'sans-serif'],
                      }
                  }
              }
          }
      </script>
      <style>
          /* Custom scrollbar untuk menyelaraskan dengan estetika premium */
          .custom-scrollbar::-webkit-scrollbar {
              width: 5px;
              height: 5px;
          }
          .custom-scrollbar::-webkit-scrollbar-track {
              background: transparent;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb {
              background: #D1C9BE;
              border-radius: 999px;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb:hover {
              background: #A82040;
          }
          
          /* Custom Markdown parsed lists styling agar Tailwind prose tidak bentrok */
          .parsed-markdown p { margin-bottom: 0.5rem; }
          .parsed-markdown strong { font-weight: 700; color: #4A1515; }
          .parsed-markdown ul { list-style-type: disc; padding-left: 1.25rem; margin-bottom: 0.5rem; }
          .parsed-markdown ol { list-style-type: decimal; padding-left: 1.25rem; margin-bottom: 0.5rem; }
          .parsed-markdown li { margin-bottom: 0.25rem; }
          .parsed-markdown code { font-family: monospace; background-color: #F3F4F6; padding: 2px 4px; border-radius: 4px; font-size: 0.85em; color: #7B2D2D; }
          .parsed-markdown blockquote { border-left: 3px solid #7B2D2D; padding-left: 0.75rem; color: #6B7280; font-style: italic; }
      </style>
  </head>
  ```

- [ ] **Step 3: Commit fondasi aset**
  
  ```bash
  git add static/index.html static/assets/logo-unsrat.png
  git commit -m "style: inisialisasi tailwind cdn, font inter, dan marked.js pada static/index.html"
  ```

---

### Task 2: Implementasi Layout Utama & Sidebar Kontrol

**Files:**
* Modify: `static/index.html`

- [ ] **Step 1: Susun struktur tata letak dual-view di body index.html**
  
  Ganti seluruh elemen `<body>` saat ini dengan grid layout Tailwind yang menampung `<aside>` (sidebar kiri) dan `<main>` (area konten kanan). Pastikan semua emoji telah dibuang dan diganti Lucide Icons.

  ```html
  <body class="h-screen w-screen flex overflow-hidden bg-[#FAF9F6] font-sans antialiased text-gray-800">
      
      <!-- Panel Sidebar Kiri (Maroon Klasik) -->
      <aside class="w-80 bg-gradient-to-b from-[#4A1515] via-[#5B1A1A] to-[#7B2D2D] text-white flex flex-col justify-between p-6 shadow-2xl z-20 flex-shrink-0">
          <div class="space-y-6">
              <!-- Header Brand & Logo Placeholder -->
              <div class="flex items-center space-x-3 pb-4 border-b border-white/10">
                  <div class="bg-white/10 p-2 rounded-xl flex items-center justify-center border border-white/15 w-12 h-12">
                      <img src="/static/assets/logo-unsrat.png" alt="UNSRAT" class="w-8 h-8 object-contain" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 24 24\' stroke=\'white\'><path stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'2\' d=\'M12 14l9-5-9-5-9 5 9 5z\'/><path d=\'M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z\'/></svg>'">
                  </div>
                  <div>
                      <h2 class="font-bold text-base leading-tight uppercase tracking-wider">UNSRAT</h2>
                      <p class="text-white/60 text-[10px] uppercase font-bold tracking-widest">Sistem RAG Penelitian</p>
                  </div>
              </div>

              <!-- Tombol Navigasi SPA (Tab Buttons - Tanpa Emoji) -->
              <nav class="space-y-1.5" id="navigation-tabs">
                  <button id="tab-chat-btn" class="w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 bg-white/15 text-white border-l-4 border-white">
                      <i data-lucide="message-square" class="w-5 h-5"></i>
                      <span class="text-sm">Chatbot Utama</span>
                  </button>
                  <button id="tab-eval-btn" class="w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 text-white/70 border-l-4 border-transparent hover:bg-white/5 hover:text-white">
                      <i data-lucide="bar-chart-3" class="w-5 h-5"></i>
                      <span class="text-sm">Evaluasi Ragas</span>
                  </button>
              </nav>

              <!-- Parameter Config Sidebar -->
              <div class="space-y-4 pt-4 border-t border-white/10">
                  <h3 class="text-[10px] font-bold text-white/40 tracking-widest uppercase flex items-center space-x-2">
                      <i data-lucide="sliders" class="w-3.5 h-3.5"></i>
                      <span>Parameter Sistem</span>
                  </h3>
                  
                  <!-- Config Dropdown -->
                  <div class="space-y-1.5">
                      <label class="text-xs font-semibold text-white/70 flex items-center space-x-2" for="config-select">
                          <i data-lucide="database" class="w-3.5 h-3.5 text-white/50"></i>
                          <span>Konfigurasi Retrieval</span>
                      </label>
                      <div class="relative">
                          <select id="config-select" class="w-full bg-black/20 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-white/30 cursor-pointer appearance-none">
                              <option value="b" class="text-gray-800">Config B - RAG 2000 char</option>
                              <option value="a" class="text-gray-800">Config A - RAG 500 char</option>
                              <option value="c" class="text-gray-800">Config C - BM25 Baseline</option>
                          </select>
                          <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-white/50">
                              <i data-lucide="chevron-down" class="w-4 h-4"></i>
                          </div>
                      </div>
                  </div>

                  <!-- Model Dropdown -->
                  <div class="space-y-1.5">
                      <label class="text-xs font-semibold text-white/70 flex items-center space-x-2" for="model-select">
                          <i data-lucide="cpu" class="w-3.5 h-3.5 text-white/50"></i>
                          <span>Model Generator LLM</span>
                      </label>
                      <div class="relative">
                          <select id="model-select" class="w-full bg-black/20 border border-white/10 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-white/30 cursor-pointer appearance-none">
                              <!-- Dimuat dinamis -->
                          </select>
                          <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-white/50">
                              <i data-lucide="chevron-down" class="w-4 h-4"></i>
                          </div>
                      </div>
                  </div>
              </div>
          </div>

          <!-- Tombol Reset & Info Status -->
          <div class="space-y-3">
              <button id="reset-btn" class="w-full flex items-center justify-center space-x-2 py-3 bg-white/10 hover:bg-white/20 active:bg-white/30 rounded-xl text-xs text-white font-semibold transition duration-200 border border-white/10 active:scale-[0.98]">
                  <i data-lucide="refresh-cw" class="w-4 h-4"></i>
                  <span>Reset Percakapan</span>
              </button>
              <div class="text-[10px] text-white/40 flex items-center justify-center space-x-1.5 border-t border-white/5 pt-2">
                  <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
                  <span id="status-info">Ready</span>
              </div>
          </div>
      </aside>

      <!-- Area Konten Utama -->
      <main class="flex-1 flex flex-col h-full overflow-hidden relative">
          <!-- Header melintang atas -->
          <header class="bg-gradient-to-r from-[#5C1F1F] to-[#7B2D2D] text-white px-8 py-4.5 shadow-md flex items-center justify-between z-10">
              <div class="flex items-center space-x-3.5">
                  <div class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center border border-white/15">
                      <i data-lucide="message-square" class="w-5 h-5 text-white"></i>
                  </div>
                  <div>
                      <h1 class="font-bold text-base tracking-tight">Asisten Informasi Akademik UNSRAT</h1>
                      <p class="text-white/60 text-[10px] font-medium">Sistem Penjawab Regulasi & Profil Kampus berbasis Retrieval-Augmented Generation</p>
                  </div>
              </div>
              <div>
                  <span id="badge-config-display" class="bg-white/15 border border-white/10 px-3.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider text-white">Config B</span>
              </div>
          </header>

          <!-- TAB CONTENT AKAN MASUK DI SINI -->
      </main>
  </body>
  ```

- [ ] **Step 2: Commit layout dasar**
  
  ```bash
  git add static/index.html
  git commit -m "feat: perbarui layout sidebar dan header utama dengan tailwind CSS"
  ```

---

### Task 3: Tab 1 (Chatbot Utama), Form Chat, & Welcome Panel

**Files:**
* Modify: `static/index.html`

- [ ] **Step 1: Tambahkan container Tab 1 (Chat) di bawah header main**
  
  Tambahkan kontainer `div` untuk `#tab-chat` dengan riwayat gelembung chat, welcome panel formal, form input bawah, dan disclaimer kaki tanpa emoji.

  ```html
  <!-- TAB 1: AREA CHATBOT UTAMA -->
  <div id="tab-chat" class="flex-1 flex flex-col h-full overflow-hidden transition-all duration-300">
      
      <!-- Area Riwayat Chat -->
      <div id="chat-messages" class="flex-1 overflow-y-auto px-8 py-6 space-y-6 custom-scrollbar pb-36 bg-[#FAF9F6]">
          <!-- Welcome Message Panel (Automatic) -->
          <div class="flex items-start space-x-4 max-w-4xl opacity-100 transition-all duration-300">
              <div class="bg-[#7B2D2D] text-white p-3 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                  <i data-lucide="award" class="w-5 h-5"></i>
              </div>
              <div class="space-y-2 flex-1">
                  <span class="inline-block bg-[#7B2D2D]/10 border border-[#7B2D2D]/15 text-[#7B2D2D] px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">Selamat Datang</span>
                  <div class="bg-white border border-[#EBE7E1] rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-gray-700 leading-relaxed text-sm">
                      <p class="font-semibold text-gray-900 mb-1">Halo civitas akademika Universitas Sam Ratulangi!</p>
                      <p class="text-gray-600 text-xs md:text-sm">Saya adalah asisten virtual akademik resmi Anda. Silakan tanyakan hal-hal terkait Peraturan Akademik (beban SKS, cuti kuliah, KRS, DO, drop-out, yudisium), kalender akademik, visi misi universitas, sejarah, akreditasi, maupun profil institut.</p>
                      <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                          <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Syarat dan batas pengambilan cuti akademik di UNSRAT?')">
                              <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                              <span class="truncate">Syarat cuti akademik?</span>
                          </button>
                          <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Visi, misi, dan tujuan resmi Universitas Sam Ratulangi.')">
                              <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                              <span class="truncate">Visi misi UNSRAT?</span>
                          </button>
                          <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Berapa beban SKS maksimum untuk mahasiswa baru semester satu?')">
                              <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                              <span class="truncate">Beban SKS semester 1?</span>
                          </button>
                          <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Bagaimana mekanisme evaluasi putus studi atau DO mahasiswa?')">
                              <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                              <span class="truncate">Mekanisme evaluasi DO?</span>
                          </button>
                      </div>
                  </div>
              </div>
          </div>
      </div>

      <!-- Area Form Input Bawah (Floating panel) -->
      <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/95 to-transparent pt-8 pb-6 px-8 flex flex-col items-center z-10">
          <form id="chat-form" class="w-full max-w-4xl flex items-center bg-white border border-[#E4DFD9] rounded-2xl shadow-xl overflow-hidden focus-within:border-[#7B2D2D] focus-within:ring-2 focus-within:ring-[#7B2D2D]/20 transition duration-300">
              <input type="text" id="user-input" placeholder="Ketik pertanyaan akademik Anda di sini (misal: 'berapa batas minimal IPK...')" class="flex-1 px-6 py-4.5 text-sm text-gray-800 focus:outline-none placeholder-gray-400 bg-white" autocomplete="off" required>
              <button type="submit" id="send-btn" class="bg-[#7B2D2D] hover:bg-[#963E3E] active:bg-[#5C1F1F] text-white p-3 rounded-xl mr-3 shadow-md hover:shadow-lg active:scale-95 transition duration-200 flex items-center justify-center w-11 h-11 cursor-pointer">
                  <i data-lucide="send" id="btn-icon" class="w-5 h-5"></i>
              </button>
          </form>
          
          <!-- Catatan Kaki Disclaimer Formal (Section 6) -->
          <div class="flex items-center space-x-1.5 text-[10px] text-gray-400 mt-2.5 text-center">
              <i data-lucide="shield-alert" class="w-3.5 h-3.5 flex-shrink-0 text-gray-400"></i>
              <span>Sistem ini adalah prototipe penelitian berbasis LLM. Tanggapan didasarkan pada dokumen ground-truth peraturan resmi Universitas Sam Ratulangi. Harap verifikasi informasi penting ke sub-bagian akademik fakultas Anda.</span>
          </div>
      </div>
  </div>
  ```

- [ ] **Step 2: Commit Tab 1 layout**
  
  ```bash
  git add static/index.html
  git commit -m "feat: selesaikan tampilan chatbot Tab 1 dengan input bar dan disclaimer formal"
  ```

---

### Task 4: Tab 2 (Dashboard Evaluasi Kuantitatif) & Metadata Panel

**Files:**
* Modify: `static/index.html`

- [ ] **Step 1: Tambahkan kontainer Tab 2 (Dashboard Evaluasi) di bawah Tab 1**
  
  Buat struktur `#tab-eval` tersembunyi (`hidden`) secara default. Tambahkan **Metadata Panel** di atas grid untuk menyajikan informasi parameter uji belakang layar (last run, dataset size, active models). Susun grid Wilcoxon, Chart.js, dan Live Log di bawahnya.

  ```html
  <!-- TAB 2: AREA DASHBOARD EVALUASI RAGAS -->
  <div id="tab-eval" class="hidden flex-1 flex flex-col h-full overflow-y-auto px-8 py-6 space-y-6 custom-scrollbar pb-10">
      <div class="flex items-center justify-between border-b border-gray-200 pb-3">
          <div>
              <h2 class="font-bold text-xl text-gray-850 tracking-tight flex items-center space-x-2">
                  <i data-lucide="line-chart" class="w-5 h-5 text-[#7B2D2D]"></i>
                  <span>Laporan Pengujian & Evaluasi Kuantitatif Ragas</span>
              </h2>
              <p class="text-xs text-gray-500 mt-0.5">Komparasi performa sistem berbasis data ground-truth regulasi akademik Universitas Sam Ratulangi.</p>
          </div>
          <button id="refresh-eval-btn" class="flex items-center space-x-2 px-3.5 py-2 border border-[#E4DFD9] bg-white hover:bg-[#7B2D2D]/5 hover:border-[#7B2D2D]/20 text-[#7B2D2D] rounded-xl text-xs font-semibold transition duration-150 shadow-sm cursor-pointer active:scale-98">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Muat Ulang Data</span>
          </button>
      </div>

      <!-- PANEL METADATA EVALUASI -->
      <div class="bg-white border border-[#EBE7E1] rounded-2xl p-4.5 shadow-sm grid grid-cols-2 md:grid-cols-5 gap-4">
          <div class="space-y-1">
              <div class="text-[9px] font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-1">
                  <i data-lucide="calendar" class="w-3 h-3"></i>
                  <span>Terakhir Dijalankan</span>
              </div>
              <div class="text-xs font-bold text-gray-800" id="meta-last-run">-</div>
          </div>
          <div class="space-y-1 border-l border-gray-100 pl-3">
              <div class="text-[9px] font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-1">
                  <i data-lucide="database" class="w-3 h-3"></i>
                  <span>Dataset Ground-Truth</span>
              </div>
              <div class="text-xs font-bold text-gray-800" id="meta-dataset-size">-</div>
          </div>
          <div class="space-y-1 border-l border-gray-100 pl-3">
              <div class="text-[9px] font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-1">
                  <i data-lucide="cpu" class="w-3 h-3"></i>
                  <span>Generator LLM</span>
              </div>
              <div class="text-xs font-bold text-gray-800 truncate" id="meta-generator-model">-</div>
          </div>
          <div class="space-y-1 border-l border-gray-100 pl-3">
              <div class="text-[9px] font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-1">
                  <i data-lucide="award" class="w-3 h-3"></i>
                  <span>Evaluator LLM</span>
              </div>
              <div class="text-xs font-bold text-gray-800 truncate" id="meta-evaluator-model">-</div>
          </div>
          <div class="space-y-1 border-l border-gray-100 pl-3">
              <div class="text-[9px] font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-1">
                  <i data-lucide="fingerprint" class="w-3 h-3"></i>
                  <span>Model Embedding</span>
              </div>
              <div class="text-xs font-bold text-gray-800 truncate" id="meta-embedding-model">-</div>
          </div>
      </div>

      <!-- Grid Dashboard Utama -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <!-- Card Grafik Metrik Ragas -->
          <div class="bg-white border border-[#EBE7E1] rounded-2xl p-5 shadow-sm space-y-4 flex flex-col">
              <div class="flex items-center justify-between">
                  <h3 class="font-bold text-xs md:text-sm text-gray-800 flex items-center space-x-2">
                      <span class="w-2.5 h-2.5 rounded-full bg-[#7B2D2D]"></span>
                      <span>Visualisasi Metrik Performa Ragas</span>
                  </h3>
                  <span class="text-[9px] bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full font-bold border border-amber-100">Nilai Lebih Tinggi = Lebih Baik</span>
              </div>
              <div class="relative h-72 flex-1 flex items-center justify-center">
                  <canvas id="metricsChart"></canvas>
              </div>
          </div>

          <!-- Card Hasil Uji Statistik Wilcoxon (Dengan Clipboard Copy) -->
          <div class="bg-white border border-[#EBE7E1] rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between">
              <div class="space-y-3">
                  <div class="flex items-center justify-between">
                      <h3 class="font-bold text-xs md:text-sm text-gray-800 flex items-center space-x-2">
                          <span class="w-2.5 h-2.5 rounded-full bg-[#7B2D2D]"></span>
                          <span>Signifikansi Statistik Wilcoxon (Config A vs B)</span>
                      </h3>
                      <div class="flex items-center space-x-1.5">
                          <span class="text-[9px] bg-green-50 text-green-700 px-2 py-0.5 rounded-full font-bold border border-green-100">Alpha = 0.05</span>
                          <button id="btn-copy-wilcoxon" class="p-1.5 text-gray-400 hover:text-[#7B2D2D] hover:bg-gray-50 border border-gray-100 hover:border-gray-200 rounded-lg transition cursor-pointer" title="Salin data ke Excel/Word">
                              <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                          </button>
                      </div>
                  </div>
                  
                  <div class="overflow-x-auto border border-gray-100 rounded-xl">
                      <table class="w-full text-xs text-left text-gray-600" id="table-wilcoxon">
                          <thead class="bg-[#FAF9F6] text-gray-800 font-bold uppercase text-[9px] border-b border-gray-100">
                              <tr>
                                  <th class="px-4 py-3">Metrik Evaluasi</th>
                                  <th class="px-4 py-3">P-Value</th>
                                  <th class="px-4 py-3">Hasil Signifikansi</th>
                                  <th class="px-4 py-3 text-right">Model Unggul</th>
                              </tr>
                          </thead>
                          <tbody id="wilcoxon-table-body" class="divide-y divide-gray-100">
                              <!-- Dimuat dinamis via JS -->
                          </tbody>
                      </table>
                  </div>
              </div>
              <div class="bg-[#FAF9F6] border border-gray-150 rounded-xl p-3 text-[10px] text-gray-500 leading-relaxed">
                  <strong>Analisis Kuantitatif Bab IV:</strong> Uji Wilcoxon signed-rank membuktikan secara statistik apakah penambahan ukuran chunk (Config B) secara nyata meningkatkan pemahaman konteks dibandingkan dengan Config A.
              </div>
          </div>
      </div>

      <!-- Live Audit Log Kuantitatif (Dengan Clipboard Copy & CSV Export) -->
      <div class="bg-white border border-[#EBE7E1] rounded-2xl p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-gray-100 pb-3">
              <div class="flex items-center space-x-2">
                  <i data-lucide="terminal" class="w-4 h-4 text-[#7B2D2D]"></i>
                  <h3 class="font-bold text-xs md:text-sm text-gray-800">Live Audit Log Transaksi Chat (Kuantitatif Real-Time)</h3>
              </div>
              <div class="flex items-center space-x-2">
                  <span class="text-[9px] bg-gray-100 text-gray-500 px-2 py-0.5 rounded font-mono border border-gray-250">logs/transaksi_chat.csv</span>
                  <button id="btn-copy-audit" class="p-1.5 text-gray-400 hover:text-[#7B2D2D] hover:bg-gray-50 border border-gray-100 hover:border-gray-200 rounded-lg transition cursor-pointer" title="Salin data log">
                      <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                  </button>
                  <button id="btn-download-audit" class="p-1.5 text-gray-400 hover:text-[#7B2D2D] hover:bg-gray-50 border border-gray-100 hover:border-gray-200 rounded-lg transition cursor-pointer" title="Unduh CSV Lengkap">
                      <i data-lucide="download" class="w-3.5 h-3.5"></i>
                  </button>
              </div>
          </div>
          <div class="overflow-x-auto border border-gray-100 rounded-xl">
              <table class="w-full text-xs text-left text-gray-600" id="table-audit">
                  <thead class="bg-[#FAF9F6] text-gray-800 font-bold uppercase text-[9px] border-b border-gray-100">
                      <tr>
                          <th class="px-4 py-3">Waktu</th>
                          <th class="px-4 py-3">Config</th>
                          <th class="px-4 py-3">Model</th>
                          <th class="px-4 py-3">Pertanyaan</th>
                          <th class="px-4 py-3 text-center">Chunks</th>
                          <th class="px-4 py-3">Best Score</th>
                          <th class="px-4 py-3">Latency</th>
                          <th class="px-4 py-3 text-right">Est. Tokens</th>
                      </tr>
                  </thead>
                  <tbody id="audit-table-body" class="divide-y divide-gray-100">
                      <!-- Dimuat dinamis via JS -->
                  </tbody>
              </table>
          </div>
      </div>
      
      <!-- Kaki Halaman Disclaimer Evaluasi -->
      <div class="flex items-center justify-center space-x-1.5 text-[9px] text-gray-400 pt-2 border-t border-gray-150">
          <i data-lucide="info" class="w-3.5 h-3.5 text-gray-400"></i>
          <span>Data di atas diperbarui secara langsung berdasarkan log file transaksi lokal dan hasil pengujian offline evaluasi Ragas.</span>
      </div>
  </div>
  ```

- [ ] **Step 2: Commit Tab 2 layout**
  
  ```bash
  git add static/index.html
  git commit -m "feat: tambah panel metadata evaluasi dan visualisasi perbandingan pada Tab 2"
  ```

---

### Task 5: Backend API — Pemaparan Parameter Uji (Metadata)

**Files:**
* Modify: `app.py:83-140`

- [ ] **Step 1: Modifikasi GET /api/evaluation di app.py secara aman**
  
  Buka `app.py`. Modifikasi fungsi `get_evaluation()` secara sangat aman (drop-in replacement). Masukkan try-except block lokal dan pertahankan logic NaN-to-None (`df_audit.astype(object).where(pd.notnull(df_audit), None)`) untuk mencegah JSON NaN serialization error.

  ```python
  @app.get("/api/evaluation")
  async def get_evaluation():
      """
      Baca dan kembalikan statistik evaluasi dari CSV hasil.
  
      Mengembalikan mean, std per metrik per config beserta metadata parameter uji.
      """
      import os
      from datetime import datetime
      from src.config import (
          EVAL_DATASET_PATH, EVALUATOR_MODEL_NAME, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME
      )
  
      result = {"configs": {}, "wilcoxon": {}, "metadata": {}}
  
      # Ekstrak data metadata parameter pengujian untuk laporan skripsi
      dataset_size = 0
      if EVAL_DATASET_PATH.exists():
          try:
              df_gt = pd.read_csv(EVAL_DATASET_PATH)
              dataset_size = len(df_gt)
          except Exception:
              pass
  
      last_run = "-"
      wilcoxon_path = EVAL_RESULTS_DIR / "statistical_test.csv"
      if wilcoxon_path.exists():
          try:
              mtime = os.path.getmtime(wilcoxon_path)
              last_run = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
          except Exception:
              pass
  
      result["metadata"] = {
          "last_run":        last_run,
          "dataset_size":    f"{dataset_size} Pertanyaan",
          "generator_model":  LLM_MODEL_NAME,
          "evaluator_model":  EVALUATOR_MODEL_NAME,
          "embedding_model":  EMBEDDING_MODEL_NAME
      }
  
      for config_label in ["a", "b", "c"]:
          csv_path = EVAL_RESULTS_DIR / f"hasil_config_{config_label}.csv"
          if csv_path.exists():
              df = pd.read_csv(csv_path)
              metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "response_time_seconds"]
              stats = {}
              for m in metrics:
                  if m in df.columns:
                      mean_val = df[m].mean()
                      std_val = df[m].std()
                      min_val = df[m].min()
                      max_val = df[m].max()
                      
                      stats[m] = {
                          "mean": None if pd.isna(mean_val) else round(mean_val, 4),
                          "std":  None if pd.isna(std_val) else round(std_val, 4),
                          "min":  None if pd.isna(min_val) else round(min_val, 4),
                          "max":  None if pd.isna(max_val) else round(max_val, 4),
                      }
              result["configs"][config_label] = stats
  
      # Wilcoxon results
      if wilcoxon_path.exists():
          df_w = pd.read_csv(wilcoxon_path)
          for _, row in df_w.iterrows():
              stat_val = row.get("wilcoxon_statistic")
              p_val = row.get("p_value")
              winner_val = row.get("winner")
              sig_val = row.get("significant_at_0.05")
              
              result["wilcoxon"][row["metric"]] = {
                  "statistic": None if pd.isna(stat_val) else stat_val,
                  "p_value":   None if pd.isna(p_val) else p_val,
                  "significant": False if pd.isna(sig_val) else bool(sig_val),
                  "winner":    "Tidak signifikan" if pd.isna(winner_val) or winner_val == "Tidak signifikan" else winner_val,
              }
  
      # Audit log (5 transaksi terakhir)
      from src.config import CHAT_LOG_PATH
      if CHAT_LOG_PATH.exists():
          df_audit = pd.read_csv(CHAT_LOG_PATH)
          # Mengganti NaN dengan None agar tidak merusak serialisasi JSON (D-A7)
          df_audit = df_audit.astype(object).where(pd.notnull(df_audit), None)
          result["audit_log"] = df_audit.tail(5).to_dict(orient="records")
      else:
          result["audit_log"] = []
  
      return JSONResponse(result)
  ```

- [ ] **Step 2: Commit backend app.py**
  
  ```bash
  git add app.py
  git commit -m "feat: perbarui endpoint /api/evaluation di app.py untuk menyuplai metadata pengujian"
  ```

---

### Task 6: JS Logic — Navigasi & Welcome Message

**Files:**
* Modify: `static/js/app.js`

- [ ] **Step 1: Bersihkan total berkas app.js dan inisialisasi state awal**
  
  Buka file `static/js/app.js`. Kita akan merombak total seluruh logika client-side menggunakan Vanilla JS murni. Terapkan state management yang andal tanpa category.

  ```javascript
  // static/js/app.js — Client-Side SPA Controller
  
  document.addEventListener("DOMContentLoaded", () => {
      // Pembungkus aman untuk inisialisasi ikon Lucide
      function safeCreateIcons() {
          try {
              if (typeof lucide !== "undefined" && lucide.createIcons) {
                  lucide.createIcons();
              } else {
                  console.warn("[RAG Client] Lucide library is not globally available.");
              }
          } catch (e) {
              console.error("[RAG Client] Failed to create Lucide icons:", e);
          }
      }
  
      safeCreateIcons();
  
      // ── STATE MANAGEMENT ───────────────────────────────────────────────────────
      let chatHistory = [];
      let isStreaming = false;
      let abortController = null;
      let metricsChartInstance = null;
  
      // Element Selectors
      const tabChatBtn = document.getElementById("tab-chat-btn");
      const tabEvalBtn = document.getElementById("tab-eval-btn");
      const tabChat    = document.getElementById("tab-chat");
      const tabEval    = document.getElementById("tab-eval");
      const modelSelect = document.getElementById("model-select");
      const configSelect = document.getElementById("config-select");
      const badgeConfig = document.getElementById("badge-config-display");
      const resetBtn = document.getElementById("reset-btn");
      const refreshEvalBtn = document.getElementById("refresh-eval-btn");
  
      // Form & Input Elements
      const chatForm = document.getElementById("chat-form");
      const chatInput = document.getElementById("user-input");
      const chatMessages = document.getElementById("chat-messages");
      const sendBtn = document.getElementById("send-btn");
      const btnIcon = document.getElementById("btn-icon");
      const statusInfo = document.getElementById("status-info");
  
      // Ekspor Clipboard Selectors
      const btnCopyWilcoxon = document.getElementById("btn-copy-wilcoxon");
      const btnCopyAudit = document.getElementById("btn-copy-audit");
      const btnDownloadAudit = document.getElementById("btn-download-audit");
  
      // Metadata Panel Selectors
      const metaLastRun = document.getElementById("meta-last-run");
      const metaDatasetSize = document.getElementById("meta-dataset-size");
      const metaGenerator = document.getElementById("meta-generator-model");
      const metaEvaluator = document.getElementById("meta-evaluator-model");
      const metaEmbedding = document.getElementById("meta-embedding-model");
  
      // ── SPA TAB NAVIGATION (Bebas Emoji) ─────────────────────────────────────
      tabChatBtn.addEventListener("click", () => {
          tabChatBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 bg-white/15 text-white border-l-4 border-white";
          tabEvalBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 text-white/70 border-l-4 border-transparent hover:bg-white/5 hover:text-white";
          tabChat.classList.remove("hidden");
          tabEval.classList.add("hidden");
      });
  
      tabEvalBtn.addEventListener("click", () => {
          tabEvalBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 bg-white/15 text-white border-l-4 border-white";
          tabChatBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 text-white/70 border-l-4 border-transparent hover:bg-white/5 hover:text-white";
          tabEval.classList.remove("hidden");
          tabChat.classList.add("hidden");
          loadEvaluationData();
      });
  
      refreshEvalBtn.addEventListener("click", loadEvaluationData);
  
      // Helper untuk mengisi kueri cepat
      window.fillInput = function(text) {
          chatInput.value = text;
          chatInput.focus();
      };
  
      // ── SYSTEM CONFIG INGESTION ──────────────────────────────────────────────
      async function loadSystemConfig() {
          try {
              console.log("[RAG Client] Fetching system config from /api/config");
              const res = await fetch("/api/config");
              if (!res.ok) throw new Error("Gagal mengambil konfigurasi awal");
              const data = await res.json();
              
              modelSelect.innerHTML = data.available_models.map(model => 
                  `<option value="${model}" ${model === data.active_model ? 'selected' : ''} class="text-gray-800">${model}</option>`
              ).join("");
              
              configSelect.value = "b"; // default Config B
              updateConfigBadge();
          } catch (err) {
              console.error("[RAG Client] Config load failed:", err);
              statusInfo.textContent = "Error load config";
          }
      }
  
      function updateConfigBadge() {
          if (badgeConfig) {
              const val = configSelect.value.toUpperCase();
              badgeConfig.innerText = `Config ${val}`;
          }
      }
  
      configSelect.addEventListener("change", () => {
          updateConfigBadge();
          clearChatUI();
      });
  
      function clearChatUI() {
          chatHistory = [];
          chatMessages.innerHTML = `
              <!-- Welcome Panel (Tanpa Emoji) -->
              <div class="flex items-start space-x-4 max-w-4xl opacity-100 transition-all duration-300">
                  <div class="bg-[#7B2D2D] text-white p-3 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                      <i data-lucide="award" class="w-5 h-5"></i>
                  </div>
                  <div class="space-y-2 flex-1">
                      <span class="inline-block bg-[#7B2D2D]/10 border border-[#7B2D2D]/15 text-[#7B2D2D] px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">SYSTEM</span>
                      <div class="bg-white border border-[#EBE7E1] rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-gray-700 leading-relaxed text-sm">
                          Riwayat percakapan telah dibersihkan. Konfigurasi ${configSelect.value.toUpperCase()} aktif. Silakan ajukan pertanyaan regulasi akademik Anda.
                      </div>
                  </div>
              </div>
          `;
          safeCreateIcons();
          console.log("[RAG Client] Conversation cleared.");
      }
  
      resetBtn.addEventListener("click", clearChatUI);
  
      // Load config on startup
      loadSystemConfig();
  
      // HELPER AUTO-SCROLL SMOOTH
      function scrollToBottom() {
          chatMessages.scrollTo({
              top: chatMessages.scrollHeight,
              behavior: 'smooth'
          });
      }
  ```

- [ ] **Step 2: Commit inisialisasi JS**
  
  ```bash
  git add static/js/app.js
  git commit -m "feat: selesaikan logika inisialisasi state, config loader, dan tab navigasi di app.js"
  ```

---

### Task 7: JS Logic — Streaming SSE, Cancel Stream, & Timestamps

**Files:**
* Modify: `static/js/app.js`

- [ ] **Step 1: Implementasi event submit form chat dengan AbortController & marked.parse**
  
  Tambahkan fungsi pengiriman pesan dengan parser streaming SSE terstruktur. Pasang AbortController, transisi tombol send $\rightarrow$ stop, penanda timestamp (`HH:MM`), dan custom CSS slide-up/fade-in.

  ```javascript
      // ── LOGIKA CHAT STREAMING (Abortable) ────────────────────────────────────
      chatForm.addEventListener("submit", async (e) => {
          e.preventDefault();
          const query = chatInput.value.trim();
          if (!query) return;
  
          // Jika sedang streaming, klik tombol bertindak sebagai pembatalan (Stop)
          if (isStreaming) {
              handleAbort();
              return;
          }
  
          chatInput.value = "";
          isStreaming = true;
          abortController = new AbortController();
  
          // Transisi Visual Tombol ke Stop (Ikon Square)
          sendBtn.className = "bg-red-600 hover:bg-red-700 active:bg-red-800 text-white p-3 rounded-xl mr-3 shadow-md hover:shadow-lg active:scale-95 transition duration-200 flex items-center justify-center w-11 h-11 cursor-pointer";
          btnIcon.setAttribute("data-lucide", "square");
          safeCreateIcons();
          statusInfo.textContent = "Processing...";
  
          const now = new Date();
          const timestamp = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  
          // 1. Tampilkan Bubble User (Slide-up & Fade-in)
          const userBubbleId = `user-msg-${Date.now()}`;
          chatMessages.innerHTML += `
              <div class="flex items-start justify-end space-x-4 max-w-4xl ml-auto opacity-0 translate-y-2 transition-all duration-300 ease-out transform" id="${userBubbleId}">
                  <div class="space-y-1 flex flex-col items-end">
                      <span class="inline-block bg-gray-200 text-gray-600 px-2.5 py-0.5 rounded-full text-[8px] font-bold tracking-wider uppercase">Mahasiswa</span>
                      <div class="bg-gradient-to-r from-[#6B2222] to-[#7B2D2D] text-white rounded-2xl rounded-tr-none px-5 py-3.5 shadow-md leading-relaxed text-sm">
                          ${query}
                      </div>
                      <span class="text-[9px] text-gray-400 font-medium">${timestamp}</span>
                  </div>
                  <div class="bg-gray-150 border border-gray-200 text-gray-500 p-2.5 rounded-xl flex-shrink-0 mt-1 shadow-sm flex items-center justify-center font-bold text-xs w-10 h-10">
                      U
                  </div>
              </div>
          `;
          
          requestAnimationFrame(() => {
              const el = document.getElementById(userBubbleId);
              if (el) {
                  el.classList.remove("opacity-0", "translate-y-2");
                  el.classList.add("opacity-100", "translate-y-0");
              }
          });
          scrollToBottom();
  
          chatHistory.push({ "role": "user", "content": query });
  
          // 2. Siapkan Bubble Bot Kosong (Typing Indicator/Skeleton Card)
          const botMsgId = `bot-msg-${Date.now()}`;
          const botBubbleId = `bot-bubble-${botMsgId}`;
          const sourcesId = `sources-${botMsgId}`;
          
          chatMessages.innerHTML += `
              <div class="flex items-start space-x-4 max-w-4xl opacity-0 translate-y-2 transition-all duration-300 ease-out transform" id="${botMsgId}">
                  <div class="bg-[#7B2D2D] text-white p-2.5 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                      <i data-lucide="shield-check" class="w-5 h-5"></i>
                  </div>
                  <div class="space-y-2 flex-1">
                      <span class="inline-block bg-[#7B2D2D]/10 border border-[#7B2D2D]/15 text-[#7B2D2D] px-2.5 py-0.5 rounded-full text-[9px] font-bold tracking-wider uppercase">Asisten RAG</span>
                      <div class="bg-white border border-[#EBE7E1] rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-gray-800 leading-relaxed text-sm parsed-markdown" id="${botBubbleId}">
                          <div class="flex items-center space-x-3 text-gray-400 font-medium py-1 animate-pulse" id="thinking-loader-${botMsgId}">
                              <i data-lucide="loader" class="w-4 h-4 animate-spin text-[#7B2D2D]"></i>
                              <span id="thinking-text-${botMsgId}">Menghubungkan ke basis data peraturan akademik...</span>
                          </div>
                      </div>
                      <div id="${sourcesId}" class="space-y-2.5 hidden"></div>
                      <span class="text-[9px] text-gray-400 font-medium block" id="time-${botMsgId}"></span>
                  </div>
              </div>
          `;
          
          requestAnimationFrame(() => {
              const el = document.getElementById(botMsgId);
              if (el) {
                  el.classList.remove("opacity-0", "translate-y-2");
                  el.classList.add("opacity-100", "translate-y-0");
              }
          });
          scrollToBottom();
          safeCreateIcons();
  
          const botTime = document.getElementById(`time-${botMsgId}`);
  
          // Watchdog timer 15 detik
          let firstTokenReceived = false;
          const watchdog = setTimeout(() => {
              if (!firstTokenReceived) {
                  console.warn("[RAG Client] Watchdog timeout triggered - no response in 15s");
                  handleError("Koneksi LLM timeout. Aliran data terhenti terlalu lama.");
                  handleAbort();
              }
          }, 15000);
  
          // Thinking indicator transition intervals
          const thinkingTextEl = document.getElementById(`thinking-text-${botMsgId}`);
          let thinkingPhase = 1;
          const thinkingInterval = setInterval(() => {
              if (firstTokenReceived) {
                  clearInterval(thinkingInterval);
                  return;
              }
              if (thinkingPhase === 1) {
                  thinkingTextEl.innerText = "Menganalisis dan memetakan dokumen rujukan RAG...";
                  thinkingPhase = 2;
              } else if (thinkingPhase === 2) {
                  thinkingTextEl.innerText = "Merumuskan jawaban formal menggunakan LLM...";
                  thinkingPhase = 3;
              }
          }, 1800);
  
          const botBubble = document.getElementById(botBubbleId);
          let fullResponseText = "";
  
          try {
              const payload = {
                  query: query,
                  config: configSelect.value,
                  model: modelSelect.value,
                  chat_history: chatHistory.slice(0, -1)
              };
  
              console.log("[RAG Client] Sending POST /api/chat payload:", payload);
              const response = await fetch("/api/chat", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(payload),
                  signal: abortController.signal
              });
  
              if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
  
              const reader = response.body.getReader();
              const decoder = new TextDecoder();
  
              while (true) {
                  const { value, done } = await reader.read();
                  if (done) break;
  
                  const chunk = decoder.decode(value, { stream: true });
                  const lines = chunk.split("\n");
  
                  for (const line of lines) {
                      if (!line.startsWith("data:")) continue;
                      const jsonStr = line.slice(5).trim();
                      if (!jsonStr) continue;
  
                      let event;
                      try { event = JSON.parse(jsonStr); } catch { continue; }
  
                      if (event.type === "thinking") {
                          // Handled by client timing loader
                      } else if (event.type === "token") {
                          if (!firstTokenReceived) {
                              firstTokenReceived = true;
                              clearTimeout(watchdog);
                              clearInterval(thinkingInterval);
                              botBubble.innerHTML = "";
                              
                              const nowBot = new Date();
                              botTime.innerText = `${String(nowBot.getHours()).padStart(2, '0')}:${String(nowBot.getMinutes()).padStart(2, '0')}`;
                          }
                          fullResponseText += event.content;
                          botBubble.innerHTML = typeof marked !== "undefined"
                              ? marked.parse(fullResponseText)
                              : fullResponseText.replace(/\n/g, "<br>");
                          scrollToBottom();
                      } else if (event.type === "citations") {
                          if (event.sources && event.sources.length > 0) {
                              renderCitations(sourcesId, event.sources, botMsgId);
                          }
                      } else if (event.type === "done") {
                          chatHistory.push({ "role": "assistant", "content": fullResponseText });
                          break;
                      } else if (event.type === "error") {
                          clearTimeout(watchdog);
                          clearInterval(thinkingInterval);
                          handleError(event.message);
                          handleAbort();
                          break;
                      }
                  }
              }
          } catch (err) {
              clearTimeout(watchdog);
              clearInterval(thinkingInterval);
              if (err.name === "AbortError") {
                  console.warn("[RAG Client] Stream aborted by client.");
                  botBubble.innerHTML += `<p class="text-amber-600 font-semibold text-xs mt-2 border-t border-amber-100 pt-2 flex items-center"><i data-lucide="alert-circle" class="w-3.5 h-3.5 inline mr-1"></i> Aliran jawaban dibatalkan oleh pengguna.</p>`;
                  safeCreateIcons();
              } else {
                  console.error("[RAG Client] Stream error:", err);
                  handleError("Terjadi kegagalan komunikasi dengan server RAG.");
              }
          } finally {
              isStreaming = false;
              clearTimeout(watchdog);
              clearInterval(thinkingInterval);
              
              sendBtn.className = "bg-[#7B2D2D] hover:bg-[#963E3E] active:bg-[#5C1F1F] text-white p-3 rounded-xl mr-3 shadow-md hover:shadow-lg active:scale-95 transition duration-200 flex items-center justify-center w-11 h-11 cursor-pointer";
              btnIcon.setAttribute("data-lucide", "send");
              safeCreateIcons();
              statusInfo.textContent = "Ready";
          }
      });
  
      function handleAbort() {
          if (abortController) {
              abortController.abort();
              isStreaming = false;
          }
      }
  
      function handleError(message) {
          const errorBubbleId = `error-${Date.now()}`;
          chatMessages.innerHTML += `
              <div class="flex items-start space-x-4 max-w-4xl opacity-0 translate-y-2 transition-all duration-300 ease-out transform" id="${errorBubbleId}">
                  <div class="bg-red-100 border border-red-200 text-red-700 p-2.5 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                      <i data-lucide="shield-alert" class="w-5 h-5 text-red-600"></i>
                  </div>
                  <div class="space-y-1 flex-1">
                      <span class="inline-block bg-red-100 border border-red-200 text-red-800 px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">ERROR</span>
                      <div class="bg-red-50 border border-red-150 rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-red-700 font-semibold text-xs leading-relaxed">
                          Gagal memuat respons: ${message}
                      </div>
                  </div>
              </div>
          `;
          
          requestAnimationFrame(() => {
              const el = document.getElementById(errorBubbleId);
              if (el) {
                  el.classList.remove("opacity-0", "translate-y-2");
                  el.classList.add("opacity-100", "translate-y-0");
              }
          });
          scrollToBottom();
          safeCreateIcons();
      }
  ```

- [ ] **Step 2: Tambahkan fungsi render sitasi rujukan (collapsible accordion)**
  
  Buat rendering sitasi di bawah gelembung jawaban bot sebagai tombol collapsible bersih bebas emoji.

  ```javascript
      function renderCitations(containerId, sources, botMsgId) {
          const container = document.getElementById(containerId);
          if (!container || sources.length === 0) return;
  
          let html = `
              <!-- Tombol Collapsible Accordion Rujukan (Tanpa Emoji) -->
              <button id="btn-toggle-${botMsgId}" class="w-full flex items-center justify-between px-4 py-3 bg-[#FAF9F6] border border-[#EBE7E1] hover:bg-[#7B2D2D]/5 hover:border-[#7B2D2D]/20 text-[#7B2D2D] rounded-xl text-xs font-bold transition duration-200 cursor-pointer mt-4 shadow-sm active:scale-[0.99] focus:outline-none">
                  <div class="flex items-center space-x-2">
                      <i data-lucide="book-open" class="w-4 h-4 text-[#7B2D2D]/75"></i>
                      <span>Lihat ${sources.length} Rujukan Dokumen Peraturan</span>
                  </div>
                  <i data-lucide="chevron-down" id="icon-toggle-${botMsgId}" class="w-4 h-4 transition-transform duration-200"></i>
              </button>
              
              <!-- Konten Rujukan (Collapsible) -->
              <div id="content-sources-${botMsgId}" class="hidden space-y-2.5 mt-2.5 transition-all duration-300">
                  <div class="grid grid-cols-1 gap-2.5">
          `;
  
          sources.forEach((src) => {
              html += `
                  <div class="bg-[#FAF9F6] border border-[#EBE7E1] hover:border-[#7B2D2D]/20 rounded-xl p-3.5 text-xs transition duration-150 shadow-sm space-y-1.5">
                      <div class="font-bold text-[#7B2D2D] flex items-center justify-between">
                          <span class="truncate max-w-[200px]">Doc: ${src.title}</span>
                          <span class="bg-[#7B2D2D]/10 text-[#7B2D2D] border border-[#7B2D2D]/15 px-2 py-0.5 rounded text-[8px] uppercase tracking-wider font-extrabold">Sumber [${src.index}]</span>
                      </div>
                      <div class="text-[9px] text-gray-400 font-semibold uppercase tracking-wider flex items-center space-x-2">
                          <span>Doc ID: ${src.doc_id}</span>
                          <span>•</span>
                          <span>Bab: ${src.bab || '-'}</span>
                          <span>•</span>
                          <span>Pasal: ${src.pasal || '-'}</span>
                      </div>
                      <div class="text-gray-600 bg-white border border-gray-50 rounded-lg p-2.5 italic pl-3 border-l-2 border-l-[#7B2D2D]/40 font-mono text-[10px] leading-normal">
                          "...${src.preview}..."
                      </div>
                  </div>
              `;
          });
  
          html += `
                  </div>
              </div>
          `;
  
          container.innerHTML = html;
          container.classList.remove("hidden");
          safeCreateIcons();
  
          const toggleBtn = document.getElementById(`btn-toggle-${botMsgId}`);
          const toggleContent = document.getElementById(`content-sources-${botMsgId}`);
          const toggleIcon = document.getElementById(`icon-toggle-${botMsgId}`);
  
          toggleBtn.addEventListener("click", () => {
              const isHidden = toggleContent.classList.contains("hidden");
              if (isHidden) {
                  toggleContent.classList.remove("hidden");
                  toggleContent.classList.add("opacity-100");
                  toggleIcon.style.transform = "rotate(180deg)";
                  toggleBtn.classList.add("bg-[#7B2D2D]/5", "border-[#7B2D2D]/20");
              } else {
                  toggleContent.classList.add("hidden");
                  toggleContent.classList.remove("opacity-100");
                  toggleIcon.style.transform = "rotate(0deg)";
                  toggleBtn.classList.remove("bg-[#7B2D2D]/5", "border-[#7B2D2D]/20");
              }
              scrollToBottom();
          });
      }
  ```

- [ ] **Step 3: Commit streaming logic**
  
  ```bash
  git add static/js/app.js
  git commit -m "feat: selesaikan logika chat stream, abort stream, watchdog timer, dan marked.js"
  ```

---

### Task 8: JS Logic — Render Panel Metadata & Dashboard Evaluasi

**Files:**
* Modify: `static/js/app.js`

- [ ] **Step 1: Modifikasi loadEvaluationData() untuk merender metadata panel**
  
  Hubungkan data API `/api/evaluation` yang baru (hasil Task 5) untuk mengisi teks dinamis panel metadata evaluasi di frontend, lalu selesaikan rendering grafik Chart.js dan tabel Wilcoxon.

  ```javascript
      // ── TAB EVALUASI - LOAD QUANTITATIVE METRICS & METADATA ──────────────────
      async function loadEvaluationData() {
          const wilcoxonTable = document.getElementById("wilcoxon-table-body");
          const auditTable = document.getElementById("audit-table-body");
  
          try {
              console.log("[RAG Client] Fetching evaluation data from /api/evaluation");
              const res = await fetch("/api/evaluation");
              if (!res.ok) throw new Error("Gagal mengambil data evaluasi");
              const data = await res.json();
  
              // A. Render Metadata Panel (Section 5.A)
              if (data.metadata) {
                  metaLastRun.innerText     = data.metadata.last_run || "-";
                  metaDatasetSize.innerText = data.metadata.dataset_size || "-";
                  metaGenerator.innerText   = data.metadata.generator_model || "-";
                  metaEvaluator.innerText   = data.metadata.evaluator_model || "-";
                  metaEmbedding.innerText   = data.metadata.embedding_model || "-";
                  console.log("[RAG Client] Dynamic metadata panel populated successfully.");
              }
  
              // B. Populasi Tabel Wilcoxon
              if (data.wilcoxon && Object.keys(data.wilcoxon).length > 0) {
                  wilcoxonTable.innerHTML = Object.entries(data.wilcoxon).map(([metric, row]) => {
                      const sigBadge = row.significant
                          ? `<span class="bg-green-50 border border-green-200 text-green-700 px-2 py-0.5 rounded-full text-[9px] font-extrabold uppercase">Signifikan</span>`
                          : `<span class="bg-gray-50 border border-gray-200 text-gray-500 px-2 py-0.5 rounded-full text-[9px] font-bold">Tidak Sig.</span>`;
                      
                      const winnerStr = row.winner === "Tidak signifikan" ? "Tidak signifikan" : row.winner;
  
                      return `
                          <tr class="hover:bg-gray-50 transition duration-150 text-xs">
                              <td class="px-4 py-3 font-bold text-gray-800">${metric}</td>
                              <td class="px-4 py-3 font-mono text-[10px] text-gray-500">${parseFloat(row.p_value).toFixed(5)}</td>
                              <td class="px-4 py-3">${sigBadge}</td>
                              <td class="px-4 py-3 text-right font-extrabold text-[#7B2D2D]">${winnerStr}</td>
                          </tr>
                      `;
                  }).join("");
              } else {
                  wilcoxonTable.innerHTML = `<tr><td colspan="4" class="px-4 py-4 text-center text-gray-400">Data uji Wilcoxon tidak tersedia. Silakan jalankan evaluasi offline.</td></tr>`;
              }
  
              // C. Populasi Live Audit Log
              const logs = data.audit_log || [];
              if (logs.length > 0) {
                  const reversedLogs = [...logs].reverse();
                  auditTable.innerHTML = reversedLogs.map(row => {
                      const timestampStr = row.timestamp ? row.timestamp.split(" ")[1] || row.timestamp : "-";
                      const configName = row.config ? row.config.toUpperCase() : "-";
                      
                      return `
                          <tr class="hover:bg-gray-50/50 transition duration-150 text-xs">
                              <td class="px-4 py-2.5 text-gray-400 font-mono text-[10px]">${timestampStr}</td>
                              <td class="px-4 py-2.5">
                                  <span class="bg-[#7B2D2D]/10 text-[#7B2D2D] px-2 py-0.5 rounded text-[8px] font-extrabold border border-[#7B2D2D]/15">${configName}</span>
                              </td>
                              <td class="px-4 py-2.5 font-mono text-[9px] text-gray-400 truncate max-w-[80px]">${row.model_llm || '-'}</td>
                              <td class="px-4 py-2.5 font-semibold text-gray-700 truncate max-w-[150px]" title="${row.user_query}">${row.user_query}</td>
                              <td class="px-4 py-2.5 text-center font-mono font-bold text-gray-600">${row.chunks_retrieved_count}</td>
                              <td class="px-4 py-2.5 font-mono font-semibold text-[#7B2D2D]">${parseFloat(row.best_similarity_score).toFixed(4)}</td>
                              <td class="px-4 py-2.5 font-mono text-amber-600">${parseFloat(row.response_time_seconds).toFixed(2)}s</td>
                              <td class="px-4 py-2.5 text-right font-mono font-bold text-gray-800">${row.estimated_total_tokens || 0}</td>
                          </tr>
                      `;
                  }).join("");
              } else {
                  auditTable.innerHTML = `<tr><td colspan="8" class="px-4 py-4 text-center text-gray-400">Belum ada transaksi terekam di logs/transaksi_chat.csv.</td></tr>`;
              }
  
              renderRagasChart(data.configs);
              safeCreateIcons();
          } catch (err) {
              console.error("[RAG Client] Failed to load evaluation metrics:", err);
              wilcoxonTable.innerHTML = `<tr><td colspan="4" class="px-4 py-3 text-center text-red-500">Gagal memuat metrik Wilcoxon.</td></tr>`;
              auditTable.innerHTML = `<tr><td colspan="8" class="px-4 py-3 text-center text-red-500">Gagal memuat log transaksi.</td></tr>`;
          }
      }
  
      function renderRagasChart(configs) {
          const ctx = document.getElementById("metricsChart");
          if (!ctx) return;
  
          const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"];
          const labels = ["Faithfulness", "Answer Relevancy", "Context Precision", "Context Recall"];
  
          const dataA = metrics.map(m => configs.a && configs.a[m] ? configs.a[m].mean : 0.0);
          const dataB = metrics.map(m => configs.b && configs.b[m] ? configs.b[m].mean : 0.0);
          const dataC = metrics.map(m => configs.c && configs.c[m] ? configs.c[m].mean : 0.0);
  
          if (metricsChartInstance) {
              metricsChartInstance.destroy();
          }
  
          metricsChartInstance = new Chart(ctx.getContext("2d"), {
              type: "bar",
              data: {
                  labels: labels,
                  datasets: [
                      {
                          label: "Config A (500 char)",
                          data: dataA,
                          backgroundColor: "rgba(123, 45, 45, 0.4)",
                          borderColor: "rgb(123, 45, 45)",
                          borderWidth: 1.5,
                          borderRadius: 6
                      },
                      {
                          label: "Config B (2000 char)",
                          data: dataB,
                          backgroundColor: "rgba(168, 69, 69, 0.9)",
                          borderColor: "rgb(168, 69, 69)",
                          borderWidth: 1.5,
                          borderRadius: 6
                      },
                      {
                          label: "Config C (BM25)",
                          data: dataC,
                          backgroundColor: "rgba(156, 163, 175, 0.5)",
                          borderColor: "rgb(156, 163, 175)",
                          borderWidth: 1.5,
                          borderRadius: 6
                      }
                  ]
              },
              options: {
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                      y: {
                          beginAtZero: true,
                          max: 1.0,
                          ticks: { font: { family: "Inter", size: 10 } }
                      },
                      x: {
                          ticks: { font: { family: "Inter", size: 10, weight: 600 } }
                      }
                  },
                  plugins: {
                      legend: {
                          labels: { font: { family: "Inter", size: 10, weight: 600 } }
                      }
                  }
              }
          });
      }
  ```

- [ ] **Step 2: Commit metadata panel JS**
  
  ```bash
  git add static/js/app.js
  git commit -m "feat: hubungkan data metrik dan render panel metadata dinamis di tab evaluasi"
  ```

---

### Task 9: JS Logic — Clipboard Copy & CSV Export

**Files:**
* Modify: `static/js/app.js`

- [ ] **Step 1: Implementasi ekspor Salin Clipboard (TSV) & Ekspor CSV**
  
  Tambahkan fungsi salin data tabel ke clipboard untuk kemudahan pengisian lampiran Bab IV skripsi, dan fungsi download logs/transaksi_chat.csv.

  ```javascript
      // ── EXPORT CLIPBOARD & CSV UTILITIES (Section 5.C) ────────────────────────
      function copyTableToClipboard(tableId) {
          const table = document.getElementById(tableId);
          if (!table) return;
  
          let text = "";
          const rows = table.querySelectorAll("tr");
          rows.forEach(row => {
              const cols = row.querySelectorAll("th, td");
              const rowData = Array.from(cols).map(col => col.innerText.trim()).join("\t");
              text += rowData + "\n";
          });
  
          navigator.clipboard.writeText(text)
              .then(() => {
                  alert("Data tabel berhasil disalin ke clipboard! Silakan paste langsung di Excel atau Word.");
              })
              .catch(err => {
                  console.error("[RAG Client] Clipboard copy failed:", err);
                  alert("Gagal menyalin data ke clipboard.");
              });
      }
  
      btnCopyWilcoxon.addEventListener("click", () => copyTableToClipboard("table-wilcoxon"));
      btnCopyAudit.addEventListener("click", () => copyTableToClipboard("table-audit"));
  
      btnDownloadAudit.addEventListener("click", () => {
          console.log("[RAG Client] Initiating file download for logs/transaksi_chat.csv");
          const link = document.createElement("a");
          fetch("/api/evaluation")
              .then(res => res.json())
              .then(data => {
                  if (data.audit_log && data.audit_log.length > 0) {
                      const csvHeader = "Timestamp,Config,Model,Query,ChunksCount,BestScore,Latency,EstTokens\n";
                      const csvRows = data.audit_log.map(row => 
                          `"${row.timestamp}","${row.config}","${row.model_llm}","${row.user_query.replace(/"/g, '""')}",${row.chunks_retrieved_count},${row.best_similarity_score},${row.response_time_seconds},${row.estimated_total_tokens}`
                      ).join("\n");
                      
                      const blob = new Blob([csvHeader + csvRows], { type: "text/csv;charset=utf-8;" });
                      const url = URL.createObjectURL(blob);
                      link.setAttribute("href", url);
                      link.setAttribute("download", "transaksi_chat.csv");
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                  } else {
                      alert("Belum ada log transaksi untuk diunduh.");
                  }
              })
              .catch(err => {
                  console.error("[RAG Client] Failed to download CSV:", err);
                  alert("Gagal mengunduh file CSV.");
              });
      });
  });
  ```

- [ ] **Step 2: Commit utility actions**
  
  ```bash
  git add static/js/app.js
  git commit -m "feat: selesaikan utilitas salin clipboard dan unduh CSV transaksi chat"
  ```

---

### Task 10: Protokol Verifikasi & Menjalankan Aplikasi

- [ ] **Step 1: Jalankan server aplikasi FastAPI secara lokal**
  
  Jalankan server menggunakan uvicorn di command line:
  ```powershell
  python app.py
  ```
  Expected Output: *Memulai server UNSRAT RAG di http://localhost:8000* atau host/port aktif.

- [ ] **Step 2: Jalankan Protokol Verifikasi Manual (UT-01 s.d. UT-07)**
  
  Buka `http://localhost:8000` di peramban (browser) dan lakukan checklist verifikasi:
  1. **UT-01**: Klik tombol quick query "Visi misi UNSRAT?". Respons harus mengalir lancar dengan pembeda bubble user maroon dan bot putih.
  2. **UT-02**: Saat jawaban mengalir, pastikan tombol kirim berubah menjadi ikon stop (kotak) berwarna merah. Klik tombol Stop. Aliran token harus berhenti seketika dan input kembali aktif.
  3. **UT-03**: Pastikan di kaki halaman terdapat disclaimer formal tanpa emoji dan didampingi ikon Lucide `shield-alert`.
  4. **UT-04**: Pindah ke Tab "Evaluasi Ragas". Pastikan visualisasi Chart.js, tabel Wilcoxon, dan log transaksi terisi dengan benar.
  5. **UT-05**: Klik tombol Salin (ikon clipboard) pada Wilcoxon Table dan tempel (paste) di Word atau Excel. Pastikan data tersalin rapi dalam kolom-kolom terpisah.
  6. **UT-06**: Pastikan tidak ada sisa emoji teks di label, navigasi tab, atau badge visual.
  7. **UT-07**: Pastikan **Metadata Panel** menyajikan informasi parameter uji belakang layar (last run, dataset size, active models) secara dinamis dari server.
