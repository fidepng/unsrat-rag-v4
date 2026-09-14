# Mobile-First & Adaptive Hybrid Chatbot Widget Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mengubah arsitektur chatbot widget pada Portal INSPIRE (`/`) dari Desktop-First menjadi Mobile-First App Shell yang responsif, dilengkapi Bottom Sheet Drawer untuk Sumber Rujukan, pill scroll untuk topik mobile, dan perbaikan tata letak desktop compact.

**Architecture:** Menerapkan CSS breakpoint mobile (`max-width: 768px`) untuk menjadikan widget fullscreen 100dvh dan menyembunyikan trigger button saat modal aktif. Mengimplementasikan Bottom Sheet Drawer adaptif di mobile tanpa merusak mode split side-by-side di desktop. Mempertahankan isolasi 100% pada endpoint `/unsratacid`.

**Tech Stack:** Vanilla JavaScript (ES6+), Modern Scoped CSS (`.rag-*`), HTML5 Semantic Elements, Marked.js, Playwright MCP / Pytest.

**Spec:** [`docs/superpowers/specs/2026-09-14-inspire-mobile-first-design.md`](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/docs/superpowers/specs/2026-09-14-inspire-mobile-first-design.md)

## Global Constraints

- **Scope:** Hanya memodifikasi `static/demo/index.html`, `static/demo/inspire/css/inspire.css`, dan `static/demo/inspire/js/inspire.js`.
- **Strict Untouched:** Endpoint `/unsratacid` (`static/demo/unsratacid.html` dan direktori `static/demo/unsratacid/`) **100% tidak boleh disentuh**.
- **No Backend / Pipeline Breakage:** Pipeline RAG, konfigurasi prompt, model, dan evaluasi RAGAS tidak diubah.
- **Brand Identity:** Pertahankan palet Maroon Klasik (`#7B2D2D`, `#8C3232`), Canvas Warm Neutral (`#FAF9F6`), dan tipografi Inter.

---

### Task 1: Mobile-First Fullscreen Shell & Trigger Button Lifecycle

**Files:**
- Modify: `static/demo/inspire/css/inspire.css`
- Modify: `static/demo/inspire/js/inspire.js`

**Interfaces:**
- Consumes: `#rag-chatbot-widget`, `#rag-modal`, `#rag-trigger-btn`, `#rag-expand-btn`
- Produces: CSS class `.rag-trigger-hidden`, media query `@media (max-width: 768px)` untuk fullscreen modal dan auto-hide trigger.

- [ ] **Step 1: Tambahkan CSS styling untuk Mobile Fullscreen Shell dan Trigger Visibility**

Di `static/demo/inspire/css/inspire.css`:
```css
/* Trigger visibility control */
.rag-trigger.rag-trigger-hidden {
  opacity: 0 !important;
  pointer-events: none !important;
  transform: scale(0.6) !important;
  transition: opacity 0.18s ease, transform 0.18s ease;
}

/* Mobile-First Fullscreen Shell (<= 768px) */
@media (max-width: 768px) {
  .rag-modal-window.rag-modal-compact,
  .rag-modal-window.rag-modal-expanded {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    height: 100% !important;
    height: 100dvh !important;
    max-width: 100vw !important;
    max-height: 100dvh !important;
    border-radius: 0 !important;
    border: none !important;
    box-shadow: none !important;
    transform: none !important;
  }

  /* Sembunyikan tombol expand di mobile */
  #rag-expand-btn {
    display: none !important;
  }

  /* Safe-area insets pada input form mobile */
  .rag-chat-form {
    padding-bottom: max(14px, env(safe-area-inset-bottom)) !important;
  }
}
```

- [ ] **Step 2: Perbarui `toggleModal()` pada `inspire.js` untuk mengontrol visibilitas `#rag-trigger-btn`**

Di `static/demo/inspire/js/inspire.js`:
```javascript
toggleModal(forceState) {
  const { modal, overlay, userInput, triggerBtn } = this.elements;
  if (!modal) return;

  const isCurrentlyHidden = modal.classList.contains('hidden');
  const shouldShow = forceState !== undefined ? forceState : isCurrentlyHidden;

  if (shouldShow) {
    modal.classList.remove('hidden');
    if (overlay) overlay.classList.remove('hidden');
    if (triggerBtn) triggerBtn.classList.add('rag-trigger-hidden');
    if (userInput) userInput.focus();
  } else {
    modal.classList.add('hidden');
    if (overlay) overlay.classList.add('hidden');
    if (triggerBtn) triggerBtn.classList.remove('rag-trigger-hidden');
    
    if (this.state.status === 'streaming' && this.state.abortController) {
      this.state.abortController.abort();
    }
  }
},
```

- [ ] **Step 3: Uji fungsionalitas fullscreen dan auto-hide trigger di Playwright (375x667)**
Verifikasi bahwa saat modal dibuka di viewport 375x667:
1. Modal memenuhi seluruh layar tanpa margin 24px/96px.
2. Tombol `#rag-trigger-btn` memiliki class `.rag-trigger-hidden` dan tidak menimpa `#rag-send-btn`.
3. Tombol `#rag-expand-btn` tidak tampak.

---

### Task 2: Adaptive Welcome State (Horizontal Pill Scroll di Mobile & Uniform Cards di Desktop)

**Files:**
- Modify: `static/demo/index.html`
- Modify: `static/demo/inspire/css/inspire.css`

**Interfaces:**
- Consumes: `#rag-welcome-state`, `.rag-chips-horizontal`, `.rag-chip-btn`, `.rag-welcome-logo`
- Produces: Responsif layout: swipeable pill scroll di `max-width: 768px`, uniform 100% width cards di desktop compact.

- [ ] **Step 1: Perbarui CSS untuk Topic Chips Desktop Compact (Uniform 100% Width Cards)**

Di `static/demo/inspire/css/inspire.css`:
```css
/* Desktop Compact Mode: Uniform Full-Width Cards (Bukan fit-content bergerigi) */
.rag-modal-compact .rag-chips-horizontal {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
  width: 100%;
  max-width: 360px;
}

.rag-modal-compact .rag-chip-btn {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box;
  padding: 10px 14px;
  font-size: 12.5px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

- [ ] **Step 2: Tambahkan CSS Mobile Media Query untuk Horizontal Pill Scroll**

Di `static/demo/inspire/css/inspire.css` di dalam `@media (max-width: 768px)`:
```css
  /* Mobile Welcome State Scale */
  .rag-welcome-card {
    padding: 16px 14px 12px 14px !important;
    gap: 14px !important;
  }

  .rag-welcome-logo {
    width: 52px !important;
    height: 52px !important;
    margin-bottom: 8px !important;
  }

  .rag-welcome-title {
    font-size: 16px !important;
    margin-bottom: 4px !important;
  }

  .rag-welcome-desc {
    font-size: 12px !important;
    max-width: 320px !important;
  }

  .rag-guide-inline-btn {
    margin-top: 8px !important;
    padding: 4px 12px !important;
    font-size: 11px !important;
  }

  /* 5 Topic Pill Chips Horizontal Scrollable */
  .rag-welcome-bottom {
    width: 100% !important;
    gap: 8px !important;
  }

  .rag-chips-horizontal {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    scrollbar-width: none !important;
    gap: 8px !important;
    width: 100% !important;
    max-width: 100% !important;
    padding: 4px 12px 8px 12px !important;
  }

  .rag-chips-horizontal::-webkit-scrollbar {
    display: none !important;
  }

  .rag-chip-btn {
    flex: 0 0 auto !important;
    width: auto !important;
    border-radius: 9999px !important;
    white-space: nowrap !important;
    padding: 8px 14px !important;
    font-size: 12px !important;
    min-height: 40px !important;
  }
```

- [ ] **Step 3: Uji fungsionalitas dan layout Welcome State**
Verifikasi via Playwright:
1. Di viewport 375px: Topik tampil sebagai pill horizontal scrollable, logo 52px, teks rapi tidak terpotong.
2. Di viewport 1280px: Topik tampil sebagai vertical cards berlebar seragam 100%, logo 72px.
3. Klik pada pill/card tetap mengisi textarea dan memfokuskan kursor.

---

### Task 3: Mobile Native Bottom Sheet Drawer untuk "Sumber Rujukan" (Opsi A)

**Files:**
- Modify: `static/demo/index.html`
- Modify: `static/demo/inspire/css/inspire.css`
- Modify: `static/demo/inspire/js/inspire.js`

**Interfaces:**
- Consumes: `.rag-citation-header`, `#rag-side-citation-panel`, `#rag-close-citation-btn`
- Produces: Bottom sheet drawer UI (`.rag-sheet-open`, `.rag-sheet-backdrop`, drag handle).

- [ ] **Step 1: Tambahkan Drag Handle & Backdrop Sheet di `static/demo/index.html`**

Di `static/demo/index.html`:
Tambahkan `.rag-sheet-backdrop` dan drag handle bar di dalam struktur `#rag-side-citation-panel`:
```html
        <!-- Backdrop khusus Mobile Bottom Sheet Rujukan -->
        <div id="rag-sheet-backdrop" class="rag-sheet-backdrop hidden"></div>

        <!-- Side-by-Side (Desktop) / Bottom Sheet Drawer (Mobile) Citation Panel -->
        <div id="rag-side-citation-panel" class="rag-side-citation-panel hidden">
          <div class="rag-sheet-drag-handle"></div>
          <div class="rag-side-citation-header">
            ...
```

- [ ] **Step 2: Tambahkan CSS Bottom Sheet Drawer untuk Mobile**

Di `static/demo/inspire/css/inspire.css`:
```css
/* Drag handle (hanya muncul di mobile) */
.rag-sheet-drag-handle {
  display: none;
}

.rag-sheet-backdrop {
  display: none;
}

@media (max-width: 768px) {
  .rag-sheet-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background-color: rgba(15, 12, 10, 0.4);
    z-index: 100001;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.24s ease;
  }

  .rag-sheet-backdrop.active {
    opacity: 1;
    pointer-events: auto;
  }

  .rag-side-citation-panel {
    position: fixed !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    height: 80vh !important;
    max-height: 85dvh !important;
    border-radius: 20px 20px 0 0 !important;
    background: #FAF9F6 !important;
    box-shadow: 0 -12px 36px rgba(0, 0, 0, 0.2) !important;
    border: 1px solid #E4DFD9 !important;
    border-bottom: none !important;
    z-index: 100002 !important;
    transform: translateY(100%);
    transition: transform 0.28s cubic-bezier(0.32, 0.72, 0, 1) !important;
  }

  .rag-side-citation-panel.rag-sheet-open {
    transform: translateY(0) !important;
    display: flex !important;
  }

  .rag-sheet-drag-handle {
    display: block;
    width: 36px;
    height: 4px;
    border-radius: 2px;
    background: #D6D0C7;
    margin: 8px auto 4px auto;
    flex-shrink: 0;
  }
}
```

- [ ] **Step 3: Sesuaikan Logic JS pada `inspire.js` untuk Adaptive Citations**

Di `static/demo/inspire/js/inspire.js`:
1. Cache `#rag-sheet-backdrop`.
2. Di event click `.rag-citation-header`:
```javascript
const isMobile = window.innerWidth <= 768;
if (!isMobile && this.state.mode === 'compact') {
  this.toggleExpand(true);
}
this.openSideCitationPanel(sources);
```
3. Di `openSideCitationPanel()` & `toggleCitationPanel()`:
- Jika mobile: tambahkan/hapus class `.rag-sheet-open` pada `sideCitationPanel` dan `.active` pada `sheetBackdrop`.
- Backdrop click event menutup rujukan.
- Chat scroll position di latar belakang tetap terjaga.

- [ ] **Step 4: Uji interaksi Bottom Sheet Drawer di Playwright**
Verifikasi via Playwright:
1. Kirim pertanyaan di mobile (375px), tunggu respons asisten.
2. Klik tombol "N Sumber Rujukan".
3. Verifikasi bottom sheet meluncur dari bawah, menutupi 80dvh, drag handle tampak, backdrop semi-gelap tampak, dan chat tidak terdistorsi.
4. Klik backdrop atau tombol close: sheet menutup mulus dan posisi chat tetap utuh.
5. Uji di desktop (1280px): klik rujukan tetap membuka mode split side-by-side.

---

### Task 4: End-to-End Verification & Non-Regression Gate

**Files:**
- Test: `tests/integration/test_demo_serving.py`
- Verification: Playwright E2E across Desktop & Mobile

- [ ] **Step 1: Jalankan pytest suite**
Run: `conda run -n unsrat-rag pytest tests/integration/test_demo_serving.py`
Expected: 3 passed

- [ ] **Step 2: Jalankan visual regression check via Playwright**
Capture screenshots:
- `mobile_fullscreen_welcome.png` (375x667)
- `mobile_active_chat_no_trigger.png` (375x667)
- `mobile_citations_bottom_sheet.png` (375x667)
- `desktop_compact_uniform_cards.png` (1280x800)
- `desktop_expanded_split.png` (1280x800)

- [ ] **Step 3: Verifikasi endpoint `/unsratacid`**
Pastikan portal legacy tetap 100% utuh tanpa perubahan CSS/JS.
