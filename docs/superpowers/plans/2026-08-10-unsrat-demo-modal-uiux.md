# Refinsi UI/UX Modal Chatbot UNSRAT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the refined UI/UX modal design specification in `static/demo/index.html`, `static/demo/css/demo-modal.css`, and `static/demo/js/chat-widget.js` with 100% feature parity, zero regression, and Playwright verification.

**Architecture:** Encapsulated `RagChatWidget` state engine with pure rendering views (Header, WelcomeBody, MessagesList, CitationPanel, TextareaForm) and a single entry-point event controller.

**Tech Stack:** Vanilla JS (ES6+), Scoped CSS (`demo-modal.css`), Lucide Icons SVG, Marked.js, Playwright E2E testing.

---

### Task 1: CSS Scoped Styling & Responsive Layout (`demo-modal.css`)

**Files:**
- Modify: `static/demo/css/demo-modal.css`

- [ ] **Step 1: Write updated CSS tokens, mode classes, citation panel, and textarea auto-grow rules**

Write the following complete CSS into `static/demo/css/demo-modal.css`:

```css
/* 
 * Scoped Custom CSS untuk Widget Chatbot UNSRAT
 * Pre-fix: .rag-* (bebas bentrok dengan layout WordPress & Tailwind)
 */

#rag-chatbot-widget,
#rag-chatbot-widget *,
#rag-chatbot-widget *::before,
#rag-chatbot-widget *::after {
  box-sizing: border-box;
}

.rag-widget-root {
  position: relative;
  z-index: 999999;
}

/* Floating Trigger Button */
.rag-trigger {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: #7B2D2D;
  color: #ffffff;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  border: 2px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.rag-trigger:hover {
  background-color: #963E3E;
  transform: scale(1.08);
}

.rag-trigger:active {
  background-color: #5C1F1F;
}

.rag-trigger svg {
  width: 24px;
  height: 24px;
}

/* Modal Overlay Backdrop */
.rag-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Modal Window Base */
.rag-modal-window {
  position: fixed;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid #E4DFD9;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Modal Mode: Compact (Default) */
.rag-modal-compact {
  bottom: 90px;
  right: 24px;
  width: 420px;
  max-width: calc(100vw - 32px);
  height: 580px;
  max-height: calc(100dvh - 110px);
}

/* Modal Mode: Expanded */
.rag-modal-expanded {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 85vw;
  height: 85vh;
  max-width: 1200px;
  max-height: 900px;
}

/* Header Modal */
.rag-modal-header {
  background-color: #7B2D2D;
  color: #ffffff;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #5C1F1F;
}

.rag-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rag-header-title {
  font-weight: 600;
  font-size: 15px;
  color: #ffffff;
}

.rag-header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.rag-icon-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.85);
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.rag-icon-btn:hover {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.15);
}

.rag-icon-btn:active {
  background-color: rgba(255, 255, 255, 0.25);
}

.rag-icon-btn svg {
  width: 18px;
  height: 18px;
}

/* Collapsible Settings Panel */
.rag-settings-panel {
  background-color: #FAF9F6;
  border-bottom: 1px solid #E4DFD9;
  padding: 10px 16px;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rag-setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.rag-setting-item label {
  font-weight: 600;
  color: #44403c;
}

.rag-setting-item select {
  background: #ffffff;
  border: 1px solid #d6d3d1;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 12px;
  outline: none;
}

/* Main Body & Layout Split */
.rag-body-container {
  flex: 1;
  min-height: 0;
  display: flex;
  position: relative;
  overflow: hidden;
  background-color: #FAF9F6;
}

.rag-messages-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overscroll-behavior: contain;
}

/* Welcome State (Center Aligned) */
.rag-welcome-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px 16px;
  margin: auto;
  max-width: 360px;
}

.rag-welcome-logo {
  width: 54px;
  height: 54px;
  object-fit: contain;
  margin-bottom: 12px;
}

.rag-welcome-title {
  font-weight: 700;
  font-size: 16px;
  color: #7B2D2D;
  margin-bottom: 6px;
}

.rag-welcome-desc {
  font-size: 12px;
  color: #78716c;
  line-height: 1.5;
  margin-bottom: 16px;
}

.rag-chips-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.rag-chip-btn {
  background: #ffffff;
  border: 1px solid #E4DFD9;
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 12px;
  color: #44403c;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.rag-chip-btn:hover {
  background-color: #FAF9F6;
  border-color: #7B2D2D;
  color: #7B2D2D;
}

.rag-chip-btn svg {
  width: 14px;
  height: 14px;
  color: #7B2D2D;
  flex-shrink: 0;
}

/* Chat Message Bubbles */
.rag-msg {
  display: flex;
  flex-direction: column;
  max-width: 85%;
}

.rag-msg-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  color: #a8a29e;
  margin-bottom: 4px;
}

.rag-user-msg {
  align-self: flex-end;
  background-color: #7B2D2D;
  color: #ffffff;
  padding: 10px 14px;
  border-radius: 14px 14px 2px 14px;
  font-size: 13px;
  line-height: 1.5;
}

.rag-user-msg .rag-msg-meta {
  justify-content: flex-end;
  color: rgba(255, 255, 255, 0.7);
}

.rag-bot-msg {
  align-self: flex-start;
  background-color: #ffffff;
  border: 1px solid #E4DFD9;
  color: #1c1917;
  padding: 12px 14px;
  border-radius: 14px 14px 14px 2px;
  font-size: 13px;
  line-height: 1.5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* Amber Abort Warning Badge */
.rag-abort-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  padding: 6px 10px;
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 8px;
  font-size: 11px;
  color: #b58105;
  font-weight: 500;
}

.rag-abort-badge svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

/* Accordion & Panel Rujukan Dokumen */
.rag-citations-container {
  margin-top: 10px;
  width: 100%;
}

.rag-citation-box {
  border: 1px solid #E4DFD9;
  border-radius: 10px;
  background-color: #ffffff;
  overflow: hidden;
  font-size: 12px;
}

.rag-citation-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background-color: #FAF9F6;
  border: none;
  border-bottom: 1px solid #E4DFD9;
  cursor: pointer;
  font-weight: 600;
  color: #44403c;
  transition: background-color 0.15s ease;
}

.rag-citation-header:hover {
  background-color: #f5f5f4;
}

.rag-citation-title {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #7B2D2D;
}

.rag-citation-title svg {
  width: 14px;
  height: 14px;
}

.rag-chevron {
  width: 14px;
  height: 14px;
  color: #a8a29e;
  transition: transform 0.2s ease;
}

.rag-chevron.rotate-180 {
  transform: rotate(180deg);
}

/* Side-by-Side & Mobile Overlay Citation Panel */
.rag-side-citation-panel {
  width: 380px;
  max-width: 45%;
  background: #ffffff;
  border-left: 1px solid #E4DFD9;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.rag-side-citation-header {
  padding: 12px 16px;
  background-color: #FAF9F6;
  border-bottom: 1px solid #E4DFD9;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  font-size: 13px;
  color: #7B2D2D;
}

.rag-side-citation-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 1023px) {
  .rag-side-citation-panel {
    position: absolute;
    inset: 0;
    width: 100%;
    max-width: 100%;
    z-index: 10;
  }
}

.rag-citation-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-top: 8px;
  border-top: 1px solid #f5f5f4;
}

.rag-citation-item:first-child {
  padding-top: 0;
  border-top: none;
}

.rag-citation-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: #7B2D2D;
}

.rag-citation-badge {
  background: #f5f5f4;
  border: 1px solid #E4DFD9;
  color: #78716c;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 10px;
}

.rag-citation-snippet {
  font-size: 11px;
  color: #57534e;
  font-style: italic;
  font-family: monospace;
  background-color: #FAF9F6;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #f5f5f4;
  line-height: 1.4;
  word-break: break-word;
}

/* Chat Form & Textarea Auto-Grow */
.rag-chat-form {
  padding: 12px;
  background: #ffffff;
  border-top: 1px solid #E4DFD9;
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.rag-chat-form textarea {
  flex: 1;
  background-color: #f5f5f4;
  border: 1px solid #d6d3d1;
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 13px;
  outline: none;
  resize: none;
  min-height: 38px;
  max-height: 120px;
  line-height: 1.4;
  font-family: inherit;
  overflow-y: auto;
}

.rag-chat-form textarea:focus {
  border-color: #7B2D2D;
  background-color: #ffffff;
}

.rag-send-btn {
  background-color: #7B2D2D;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: background-color 0.15s ease;
}

.rag-send-btn:hover {
  background-color: #963E3E;
}

.rag-send-btn:active {
  background-color: #5C1F1F;
}

.rag-send-btn svg {
  width: 16px;
  height: 16px;
}

.hidden {
  display: none !important;
}

/* Custom Scrollbar */
.rag-messages-body::-webkit-scrollbar,
.rag-side-citation-body::-webkit-scrollbar,
.rag-chat-form textarea::-webkit-scrollbar {
  width: 5px;
}

.rag-messages-body::-webkit-scrollbar-track,
.rag-side-citation-body::-webkit-scrollbar-track,
.rag-chat-form textarea::-webkit-scrollbar-track {
  background: transparent;
}

.rag-messages-body::-webkit-scrollbar-thumb,
.rag-side-citation-body::-webkit-scrollbar-thumb,
.rag-chat-form textarea::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
}
```

- [ ] **Step 2: Commit CSS updates**

```bash
git add static/demo/css/demo-modal.css
git commit -m "style(demo): perbarui CSS scoped demo-modal.css untuk mode compact/expanded dan citation panel"
```

---

### Task 2: HTML Structure Refactoring (`static/demo/index.html`)

**Files:**
- Modify: `static/demo/index.html` via scratch script or direct replace.

- [ ] **Step 1: Update `#rag-chatbot-widget` HTML structure in `static/demo/index.html`**

Update the injected widget HTML to match the refined header layout, welcome body with UNSRAT logo and chips, and `<textarea>` input form:

```html
<!-- RAG Chatbot Widget Container (Minimal & Scoped) -->
<div id="rag-chatbot-widget" class="rag-widget-root">
  <!-- Trigger Button -->
  <button id="rag-trigger-btn" aria-label="Buka Chatbot UNSRAT" class="rag-trigger">
    <i data-lucide="message-square"></i>
  </button>

  <!-- Modal Overlay -->
  <div id="rag-modal-overlay" class="rag-overlay hidden"></div>

  <!-- Chat Modal Window -->
  <div id="rag-modal" class="rag-modal-window rag-modal-compact hidden">
    <!-- Modal Header -->
    <div class="rag-modal-header">
      <div class="rag-header-left">
        <button id="rag-expand-btn" type="button" class="rag-icon-btn" title="Buka / Mengecilkan Mode Ukuran">
          <i data-lucide="maximize-2"></i>
        </button>
        <span class="rag-header-title">Asisten Akademik UNSRAT</span>
      </div>
      <div class="rag-header-actions">
        <button id="rag-settings-btn" type="button" class="rag-icon-btn" title="Pengaturan"><i data-lucide="settings"></i></button>
        <button id="rag-reset-btn" type="button" class="rag-icon-btn" title="Reset Percakapan"><i data-lucide="rotate-ccw"></i></button>
        <button id="rag-modal-close" type="button" class="rag-icon-btn" title="Tutup"><i data-lucide="x"></i></button>
      </div>
    </div>

    <!-- Collapsible Settings Panel -->
    <div id="rag-settings-panel" class="rag-settings-panel hidden">
      <div class="rag-setting-item">
        <label for="rag-config-select">Profil Config:</label>
        <select id="rag-config-select">
          <option value="b">Config B (Default)</option>
          <option value="c">Config C (Precise)</option>
        </select>
      </div>
      <div class="rag-setting-item">
        <label for="rag-model-select">Model Gemini:</label>
        <select id="rag-model-select">
          <option value="gemini-3.5-flash">Gemini 3.5 Flash</option>
        </select>
      </div>
    </div>

    <!-- Main Content & Side Panel Split Container -->
    <div class="rag-body-container">
      <!-- Chat Messages List -->
      <div id="rag-chat-messages" class="rag-messages-body">
        <!-- Welcome State (Center-Aligned) -->
        <div id="rag-welcome-state" class="rag-welcome-card">
          <img src="/static/assets/logo-unsrat.png" alt="UNSRAT Logo" class="rag-welcome-logo" />
          <h4 class="rag-welcome-title">Asisten Layanan Akademik UNSRAT</h4>
          <p class="rag-welcome-desc">Selamat datang! Silakan tanyakan informasi akademik atau pilih contoh pertanyaan cepat di bawah ini.</p>
          <div class="rag-chips-grid">
            <button type="button" class="rag-chip-btn" data-query="Syarat cuti akademik?">
              <i data-lucide="book-open"></i>
              <span>Syarat cuti akademik?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Visi dan Misi UNSRAT?">
              <i data-lucide="compass"></i>
              <span>Visi dan Misi UNSRAT?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Beban SKS semester 1?">
              <i data-lucide="layers"></i>
              <span>Beban SKS semester 1?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Mekanisme evaluasi DO?">
              <i data-lucide="alert-triangle"></i>
              <span>Mekanisme evaluasi DO?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Prosedur pengisian KRS?">
              <i data-lucide="file-text"></i>
              <span>Prosedur pengisian KRS?</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Side-by-Side / Mobile Overlay Citation Panel -->
      <div id="rag-side-citation-panel" class="rag-side-citation-panel hidden">
        <div class="rag-side-citation-header">
          <div class="flex items-center gap-2">
            <i data-lucide="book-open" class="w-4 h-4"></i>
            <span>Rujukan Dokumen Akademik</span>
          </div>
          <button id="rag-close-citation-btn" type="button" class="rag-icon-btn" style="color: #44403c;" title="Tutup Rujukan">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>
        <div id="rag-side-citation-body" class="rag-side-citation-body">
        </div>
      </div>
    </div>

    <!-- Input Form (Textarea Auto-Grow) -->
    <form id="rag-chat-form" class="rag-chat-form">
      <textarea id="rag-user-input" rows="1" placeholder="Ketik pertanyaan akademik..." autocomplete="off"></textarea>
      <button id="rag-send-btn" type="button" class="rag-send-btn" title="Kirim Pesan">
        <i data-lucide="send"></i>
      </button>
    </form>
  </div>
</div>

<script src="/static/demo/js/chat-widget.js"></script>
```

- [ ] **Step 2: Commit HTML updates**

```bash
git add static/demo/index.html
git commit -m "feat(demo): perbarui struktur HTML modal dengan logo UNSRAT, Lucide icons, dan textarea"
```

---

### Task 3: JS Logic Engine Refactoring (`chat-widget.js`)

**Files:**
- Modify: `static/demo/js/chat-widget.js`

- [ ] **Step 1: Write complete `chat-widget.js` with State Machine, Auto-Submit Chips, Abort Warning, and Textarea Auto-Grow**

Write the following full implementation into `static/demo/js/chat-widget.js`:

```javascript
/**
 * UNSRAT RAG Chatbot Widget Module
 * Encapsulated Namespace - Minimal & Defensif.
 */
const FEATURE_FLAGS = {
  showConfigModelSelect: true
};

const RagChatWidget = {
  state: {
    chatHistory: [],
    status: 'idle', // 'idle' | 'streaming'
    mode: 'compact', // 'compact' | 'expanded'
    abortController: null,
    currentConfig: 'b',
    currentModel: 'gemini-3.5-flash',
    activeCitations: []
  },

  elements: {},

  init() {
    this.cacheElements();
    if (!this.elements.widget) return;

    this.bindEvents();
    this.applyFeatureFlags();
    this.safeCreateIcons();
    this.loadSystemConfig();
  },

  cacheElements() {
    this.elements = {
      widget: document.getElementById('rag-chatbot-widget'),
      triggerBtn: document.getElementById('rag-trigger-btn'),
      modal: document.getElementById('rag-modal'),
      overlay: document.getElementById('rag-modal-overlay'),
      closeBtn: document.getElementById('rag-modal-close'),
      expandBtn: document.getElementById('rag-expand-btn'),
      resetBtn: document.getElementById('rag-reset-btn'),
      settingsBtn: document.getElementById('rag-settings-btn'),
      settingsPanel: document.getElementById('rag-settings-panel'),
      configSelect: document.getElementById('rag-config-select'),
      modelSelect: document.getElementById('rag-model-select'),
      chatMessages: document.getElementById('rag-chat-messages'),
      welcomeState: document.getElementById('rag-welcome-state'),
      chatForm: document.getElementById('rag-chat-form'),
      userInput: document.getElementById('rag-user-input'),
      sendBtn: document.getElementById('rag-send-btn'),
      sideCitationPanel: document.getElementById('rag-side-citation-panel'),
      sideCitationBody: document.getElementById('rag-side-citation-body'),
      closeCitationBtn: document.getElementById('rag-close-citation-btn')
    };
  },

  applyFeatureFlags() {
    const { settingsBtn, settingsPanel } = this.elements;
    if (!FEATURE_FLAGS.showConfigModelSelect) {
      if (settingsBtn) settingsBtn.classList.add('hidden');
      if (settingsPanel) settingsPanel.classList.add('hidden');
    }
  },

  bindEvents() {
    const { 
      triggerBtn, closeBtn, expandBtn, resetBtn, overlay, 
      settingsBtn, chatForm, userInput, sendBtn, 
      configSelect, modelSelect, closeCitationBtn, chatMessages 
    } = this.elements;

    if (triggerBtn) triggerBtn.addEventListener('click', () => this.toggleModal(true));
    if (closeBtn) closeBtn.addEventListener('click', () => this.toggleModal(false));
    if (overlay) overlay.addEventListener('click', () => this.toggleModal(false));
    if (expandBtn) expandBtn.addEventListener('click', () => this.toggleExpand());
    if (resetBtn) resetBtn.addEventListener('click', () => this.resetChat());

    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => {
        if (this.elements.settingsPanel && FEATURE_FLAGS.showConfigModelSelect) {
          this.elements.settingsPanel.classList.toggle('hidden');
        }
      });
    }

    if (configSelect) {
      configSelect.addEventListener('change', (e) => {
        this.state.currentConfig = e.target.value;
      });
    }

    if (modelSelect) {
      modelSelect.addEventListener('change', (e) => {
        this.state.currentModel = e.target.value;
      });
    }

    if (closeCitationBtn) {
      closeCitationBtn.addEventListener('click', () => this.toggleCitationPanel(false));
    }

    // Single Entry Handler for Send / Stop Button
    if (sendBtn) {
      sendBtn.addEventListener('click', () => this.handleActionClick());
    }

    if (chatForm) {
      chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleActionClick();
      });
    }

    if (userInput) {
      userInput.addEventListener('input', () => this.adjustTextareaHeight());
      userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.handleActionClick();
        }
      });
    }

    // Quick-Question Chips Delegation (Auto-Submit)
    if (chatMessages) {
      chatMessages.addEventListener('click', (e) => {
        const chipBtn = e.target.closest('.rag-chip-btn');
        if (chipBtn) {
          const query = chipBtn.getAttribute('data-query');
          if (query) {
            this.submitQueryDirectly(query);
          }
        }
      });
    }
  },

  toggleModal(show) {
    const { modal, overlay, userInput } = this.elements;
    if (!modal) return;

    if (show) {
      modal.classList.remove('hidden');
      if (overlay) overlay.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
      if (userInput) userInput.focus();
    } else {
      modal.classList.add('hidden');
      if (overlay) overlay.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
      
      if (this.state.status === 'streaming' && this.state.abortController) {
        this.state.abortController.abort();
      }
    }
  },

  toggleExpand(forceState) {
    const { modal, expandBtn } = this.elements;
    if (!modal) return;

    const shouldExpand = forceState !== undefined ? forceState : this.state.mode === 'compact';
    if (shouldExpand) {
      this.state.mode = 'expanded';
      modal.classList.remove('rag-modal-compact');
      modal.classList.add('rag-modal-expanded');
      if (expandBtn) {
        expandBtn.setAttribute('title', 'Mengecilkan Mode Ukuran');
        expandBtn.innerHTML = '<i data-lucide="minimize-2"></i>';
      }
    } else {
      this.state.mode = 'compact';
      modal.classList.remove('rag-modal-expanded');
      modal.classList.add('rag-modal-compact');
      if (expandBtn) {
        expandBtn.setAttribute('title', 'Buka Mode Ukuran Besar');
        expandBtn.innerHTML = '<i data-lucide="maximize-2"></i>';
      }
      this.toggleCitationPanel(false);
    }
    this.safeCreateIcons();
  },

  adjustTextareaHeight() {
    const { userInput } = this.elements;
    if (!userInput) return;
    userInput.style.height = 'auto';
    userInput.style.height = `${Math.min(userInput.scrollHeight, 120)}px`;
  },

  resetChat() {
    const { chatMessages } = this.elements;
    if (this.state.status === 'streaming' && this.state.abortController) {
      this.state.abortController.abort();
    }
    this.state.chatHistory = [];
    this.state.status = 'idle';
    this.toggleCitationPanel(false);

    if (chatMessages) {
      chatMessages.innerHTML = `
        <div id="rag-welcome-state" class="rag-welcome-card">
          <img src="/static/assets/logo-unsrat.png" alt="UNSRAT Logo" class="rag-welcome-logo" />
          <h4 class="rag-welcome-title">Asisten Layanan Akademik UNSRAT</h4>
          <p class="rag-welcome-desc">Selamat datang! Silakan tanyakan informasi akademik atau pilih contoh pertanyaan cepat di bawah ini.</p>
          <div class="rag-chips-grid">
            <button type="button" class="rag-chip-btn" data-query="Syarat cuti akademik?">
              <i data-lucide="book-open"></i>
              <span>Syarat cuti akademik?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Visi dan Misi UNSRAT?">
              <i data-lucide="compass"></i>
              <span>Visi dan Misi UNSRAT?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Beban SKS semester 1?">
              <i data-lucide="layers"></i>
              <span>Beban SKS semester 1?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Mekanisme evaluasi DO?">
              <i data-lucide="alert-triangle"></i>
              <span>Mekanisme evaluasi DO?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Prosedur pengisian KRS?">
              <i data-lucide="file-text"></i>
              <span>Prosedur pengisian KRS?</span>
            </button>
          </div>
        </div>
      `;
    }
    this.safeCreateIcons();
  },

  safeCreateIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons({
        attrs: { 'stroke-width': 1.5 }
      });
    }
  },

  async loadSystemConfig() {
    try {
      const res = await fetch('/api/config');
      if (res.ok) {
        const data = await res.json();
        if (data.available_models && this.elements.modelSelect) {
          this.elements.modelSelect.innerHTML = data.available_models.map(m => 
            `<option value="${m}">${m}</option>`
          ).join('');
        }
      }
    } catch (err) {
      console.warn('Gagal memuat config backend:', err);
    }
  },

  handleActionClick() {
    if (this.state.status === 'streaming') {
      if (this.state.abortController) {
        this.state.abortController.abort();
      }
      return;
    }

    const { userInput } = this.elements;
    if (!userInput) return;
    const query = userInput.value.trim();
    if (!query) return;

    userInput.value = '';
    this.adjustTextareaHeight();
    this.submitQueryDirectly(query);
  },

  submitQueryDirectly(query) {
    if (this.state.status === 'streaming') return;

    this.hideWelcomeState();
    this.renderUserBubble(query);

    this.state.status = 'streaming';
    this.updateSendButtonState(true);
    this.state.abortController = new AbortController();

    const botBubbleObj = this.renderBotBubblePlaceholder();
    this.scrollToBottom();

    this.executeStreamFetch(query, botBubbleObj);
  },

  hideWelcomeState() {
    const welcome = document.getElementById('rag-welcome-state');
    if (welcome) welcome.remove();
  },

  updateSendButtonState(isStreaming) {
    const { sendBtn } = this.elements;
    if (!sendBtn) return;
    if (isStreaming) {
      sendBtn.innerHTML = '<i data-lucide="square"></i>';
      sendBtn.setAttribute('title', 'Hentikan Pencarian');
    } else {
      sendBtn.innerHTML = '<i data-lucide="send"></i>';
      sendBtn.setAttribute('title', 'Kirim Pesan');
    }
    this.safeCreateIcons();
  },

  async executeStreamFetch(query, botBubbleObj) {
    let isFirstToken = true;
    let fullAnswer = '';
    let citations = [];

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: this.state.abortController.signal,
        body: JSON.stringify({
          query: query,
          config: this.state.currentConfig,
          model: this.state.currentModel,
          chat_history: this.state.chatHistory
        })
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim();
            if (!dataStr) continue;

            try {
              const parsed = JSON.parse(dataStr);
              if (parsed.type === 'token') {
                if (isFirstToken) {
                  isFirstToken = false;
                  botBubbleObj.contentElem.innerHTML = '';
                }
                fullAnswer += parsed.content;
                botBubbleObj.contentElem.innerHTML = window.marked ? window.marked.parse(fullAnswer) : this.escapeHtml(fullAnswer);
                this.scrollToBottom();
              } else if (parsed.type === 'citations') {
                citations = parsed.sources || [];
              }
            } catch (e) {
              if (isFirstToken) {
                isFirstToken = false;
                botBubbleObj.contentElem.innerHTML = '';
              }
              fullAnswer += dataStr;
              botBubbleObj.contentElem.innerHTML = window.marked ? window.marked.parse(fullAnswer) : this.escapeHtml(fullAnswer);
              this.scrollToBottom();
            }
          }
        }
      }

      if (citations.length > 0) {
        this.renderCitations(botBubbleObj.bubbleElem, citations);
      }

      this.state.chatHistory.push({ role: 'user', content: query });
      this.state.chatHistory.push({ role: 'assistant', content: fullAnswer });

    } catch (error) {
      if (error.name === 'AbortError') {
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '<span style="color: #b58105; font-size: 12px; font-style: italic;">Pencarian dihentikan sebelum ada jawaban.</span>';
        } else {
          const warningBadge = document.createElement('div');
          warningBadge.className = 'rag-abort-badge';
          warningBadge.innerHTML = '<i data-lucide="alert-circle"></i><span>Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap.</span>';
          botBubbleObj.bubbleElem.appendChild(warningBadge);
          this.safeCreateIcons();
        }
      } else {
        botBubbleObj.contentElem.innerHTML = `<span style="color: #dc2626;">Error: ${error.message}</span>`;
      }
    } finally {
      this.state.status = 'idle';
      this.updateSendButtonState(false);
      this.safeCreateIcons();
    }
  },

  getTimestamp() {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    return `${hh}:${mm}`;
  },

  renderUserBubble(text) {
    const { chatMessages } = this.elements;
    if (!chatMessages) return;

    const div = document.createElement('div');
    div.className = 'rag-msg rag-user-msg';
    div.innerHTML = `
      <div class="rag-msg-meta">
        <span>${this.getTimestamp()}</span>
      </div>
      <p style="margin: 0;">${this.escapeHtml(text)}</p>
    `;
    chatMessages.appendChild(div);
  },

  renderBotBubblePlaceholder() {
    const { chatMessages } = this.elements;
    const div = document.createElement('div');
    div.className = 'rag-msg rag-bot-msg';
    div.innerHTML = `
      <div class="rag-msg-meta">
        <span>Asisten Akademik</span>
        <span>•</span>
        <span>${this.getTimestamp()}</span>
      </div>
      <div class="rag-msg-content" style="color: #78716c;">
        <span>Mengetik...</span>
      </div>
    `;
    chatMessages.appendChild(div);
    return {
      bubbleElem: div,
      contentElem: div.querySelector('.rag-msg-content')
    };
  },

  renderCitations(containerElem, sources) {
    if (!containerElem || !sources || sources.length === 0) return;

    const citDiv = document.createElement('div');
    citDiv.className = 'rag-citations-container';
    citDiv.innerHTML = `
      <div class="rag-citation-box">
        <button type="button" class="rag-citation-header">
          <div class="rag-citation-title">
            <i data-lucide="book-open"></i>
            <span>Rujukan Dokumen Akademik (${sources.length} Sumber)</span>
          </div>
          <i data-lucide="chevron-right" class="rag-chevron"></i>
        </button>
      </div>
    `;

    containerElem.appendChild(citDiv);
    this.safeCreateIcons();

    const headerBtn = citDiv.querySelector('.rag-citation-header');
    if (headerBtn) {
      headerBtn.addEventListener('click', () => {
        if (this.state.mode === 'compact') {
          this.toggleExpand(true);
        }
        this.openSideCitationPanel(sources);
      });
    }
  },

  openSideCitationPanel(sources) {
    const { sideCitationPanel, sideCitationBody } = this.elements;
    if (!sideCitationPanel || !sideCitationBody) return;

    this.state.activeCitations = sources;
    sideCitationBody.innerHTML = sources.map((src, index) => {
      const title = src.title || "Dokumen Akademik";
      const docId = src.doc_id || "-";
      const bab = src.bab ? ` | ${src.bab}` : "";
      const pasal = src.pasal ? ` | ${src.pasal}` : "";
      const idx = src.index || (index + 1);

      return `
        <div class="rag-citation-item">
          <div class="rag-citation-meta">
            <span class="rag-citation-name">[${this.escapeHtml(idx)}] ${this.escapeHtml(title)}</span>
            <span class="rag-citation-badge">ID: ${this.escapeHtml(docId)}${this.escapeHtml(bab)}${this.escapeHtml(pasal)}</span>
          </div>
          <div class="rag-citation-snippet">
            "${this.escapeHtml(src.content)}"
          </div>
        </div>
      `;
    }).join('');

    sideCitationPanel.classList.remove('hidden');
    this.safeCreateIcons();
  },

  toggleCitationPanel(show) {
    const { sideCitationPanel } = this.elements;
    if (!sideCitationPanel) return;
    if (show) {
      sideCitationPanel.classList.remove('hidden');
    } else {
      sideCitationPanel.classList.add('hidden');
    }
  },

  scrollToBottom() {
    const { chatMessages } = this.elements;
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  },

  escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, match => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[match]);
  }
};

document.addEventListener('DOMContentLoaded', () => RagChatWidget.init());
```

- [ ] **Step 2: Commit JS updates**

```bash
git add static/demo/js/chat-widget.js
git commit -m "feat(demo): refaktor chat-widget.js dengan state machine, auto-submit chips, abort warning, dan auto-grow textarea"
```

---

### Task 4: Playwright E2E Automated Verification & Visual Audit

**Files:**
- Test: `.playwright-mcp/` visual screenshots & DOM checks via `browser_evaluate` / `browser_take_screenshot`.

- [ ] **Step 1: Verify homepage layout precision (1170px width)**

Run Playwright navigation to `http://127.0.0.1:8501/` and evaluate `.container` width:
```js
await page.goto('http://127.0.0.1:8501/');
const containerBox = await page.evaluate(() => {
  const c = document.querySelector('.container');
  return { width: window.getComputedStyle(c).width };
});
// Expected: containerBox.width === '1170px'
```

- [ ] **Step 2: Test trigger button click & compact modal initial render**

Click `#rag-trigger-btn` and verify `#rag-modal` has `.rag-modal-compact` class and is visible.

- [ ] **Step 3: Test Quick-Question Chip auto-submitting**

Click first chip (`Syarat cuti akademik?`) and verify:
1. `#rag-welcome-state` is removed.
2. User bubble is appended with text "Syarat cuti akademik?".
3. SSE streaming starts and returns tokens without blinking.

- [ ] **Step 4: Test Modal Expansion & Citation Side-by-Side Panel**

1. Click `book-open` citation button inside bot bubble.
2. Verify modal automatically transitions to `.rag-modal-expanded` (85vw/85vh).
3. Verify `#rag-side-citation-panel` opens in Side-by-Side layout.
4. Take Playwright screenshot.

- [ ] **Step 5: Test Stop-Streaming Button Abort Handling**

Submit a query, click `#rag-send-btn` while streaming to abort, and verify:
1. `.rag-abort-badge` is appended with amber warning text.
2. Partial response text is preserved.

- [ ] **Step 6: Final commit and cleanup**

```bash
git status
git commit -m "chore(demo): verifikasi Playwright E2E sukses untuk UI/UX modal final"
```
