# Spesifikasi Desain: Penghapusan watchdogTimer dan Perbaikan Bug Aliran Jawaban (User Abort)

> **Topik:** Pembersihan logika pembatasan waktu (*timeout*) dan perbaikan daur hidup (*lifecycle*) klien chat di [static/js/app.js](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/static/js/app.js).  
> **Tanggal:** 3 Juni 2026

---

## 1. Konteks & Deskripsi Bug

### A. Fitur `watchdogTimer`
Sebelumnya terdapat fitur `watchdogTimer` berbasis waktu klien (*client-side timeout*) selama 30 detik. Fungsi utama dari timer ini adalah membatalkan (*abort*) koneksi secara paksa jika token pertama dari stream `/api/chat` tidak diterima dalam 30 detik. Evaluasi menunjukkan bahwa timer ini mengganggu saat model eksternal (NVIDIA NIM) mengalami latensi antrean, serta redundan karena sudah ada tombol pembatalan manual ("Hentikan Jawaban").

### B. Bug Pesan "Aliran jawaban dihentikan oleh pengguna" (False-Positive Abort)
Ditemukan bug di mana catatan merah/kuning `[Aliran jawaban dihentikan oleh pengguna]` tetap muncul di bagian bawah jawaban chatbot sekalipun LLM telah menyelesaikan penulisan secara normal dan sukses (`event.type === "done"`).
* **Penyebab**: Ketika server mengirimkan event `done`, klien memproses event tersebut, menyimpan jawaban ke `chatHistory`, dan secara terprogram memanggil `handleAbort()`. Di dalam `handleAbort()`, sistem memanggil `abortController.abort()`. Hal ini memicu pelemparan pengecualian `AbortError` pada pembacaan stream (`reader.read()`).
* Blok penangkap eror (`catch`) klien mendeteksi `err.name === 'AbortError'` dan berasumsi bahwa pembatalan dilakukan oleh pengguna secara manual, sehingga secara salah menuliskan catatan kaki peringatan pembatalan dan melakukan `chatHistory.push()` untuk kedua kalinya.

---

## 2. Rancangan Perbaikan (Proposed Changes)

Untuk memperbaiki kedua masalah di atas secara tuntas, kita akan melakukan perubahan berikut pada [static/js/app.js](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/static/js/app.js):

### A. Menambahkan Flag `isUserAborted` pada State Global Klien
* Mendeklarasikan variabel `let isUserAborted = false;` di awal berkas dalam cakupan manajemen status (*state management*) klien (di samping `isStreaming`, `chatHistory`, dll.).

### B. Penandaan Aksi Pembatalan oleh Pengguna
* Pada event listener tombol kirim (`sendBtn` click) saat sedang streaming:
  ```javascript
  isUserAborted = true;
  handleAbort();
  ```
* Pada event listener form chat (`chatForm` submit) saat sedang streaming:
  ```javascript
  isUserAborted = true;
  handleAbort();
  ```
* Pada inisialisasi awal pengiriman kueri baru (di dalam `chatForm` submit handler, sebelum fetch):
  ```javascript
  isUserAborted = false;
  ```

### C. Menghapus Seluruh Logika `watchdogTimer`
* Menghapus deklarasi `let watchdogTimer = setTimeout(...)` di baris 459-464.
* Menghapus seluruh fungsi `clearTimeout(watchdogTimer)` pada baris 517, 577, dan 649.

### D. Penyesuaian Blok Penangkap Eror (`catch`)
* Memodifikasi penanganan `AbortError` untuk membedakan antara pembatalan manual oleh pengguna dengan pembatalan terprogram oleh sistem:
  ```javascript
  if (err.name === 'AbortError') {
      const thinkingContainer = document.getElementById(`${botMsgId}-thinking`);
      if (thinkingContainer) {
          thinkingContainer.classList.add("hidden");
      }
      const contentContainer = document.getElementById(`${botMsgId}-content`);
      if (contentContainer) {
          contentContainer.classList.remove("hidden");
          if (isUserAborted && !isFirstToken && fullResponseText.trim() !== "") {
              // Hanya tuliskan peringatan jika benar-benar dibatalkan secara manual oleh user
              contentContainer.innerHTML = marked.parse(fullResponseText) + `<p class="text-amber-700 text-xs italic mt-2.5 font-medium flex items-center"><i data-lucide="info" class="w-3.5 h-3.5 inline mr-1 flex-shrink-0"></i><span>[Aliran jawaban dihentikan oleh pengguna]</span></p>`;
              chatHistory.push({ role: "assistant", content: fullResponseText });
              safeCreateIcons();
          } else if (isUserAborted) {
              // Dibatalkan saat masih fase thinking oleh user
              contentContainer.innerHTML = `<span class="text-amber-700 font-medium bg-amber-50 border border-amber-150 rounded-xl px-4 py-2 block text-xs">Pencarian dan pembuatan jawaban dihentikan oleh pengguna.</span>`;
          } else {
              // Pembatalan terprogram oleh event "done" atau "error", tidak melakukan apa-apa karena data chatHistory sudah disimpan saat event "done"
              console.log("[RAG Client] Programmatic stream end completed.");
          }
      }
  }
  ```

---

## 3. Rencana Verifikasi & Pengujian
* **Uji Alur Sukses**: Kirim pertanyaan, tunggu hingga selesai otomatis, pastikan catatan kaki pembatalan tidak muncul dan jawaban disimpan tepat satu kali di riwayat obrolan.
* **Uji Pembatalan Manual**: Tekan tombol stop selama streaming dan pastikan teks peringatan kuning berikon Lucide muncul dengan tepat.
* **Uji Tanpa Watchdog**: Pastikan tidak ada referensi timer yang tersisa di kode klien.
