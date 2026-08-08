# Frontend Demo Replika UNSRAT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a replica UNSRAT homepage frontend demo at `/`, move existing frontend to `/testing`, create standalone RAGAS evaluation page at `/evaluation`, with zero backend logic changes and isolated CSS/JS scoping.

**Architecture:** FastAPI multi-route static serving (Opsi A) serving scraped `unsrat-ac-id.html` at `/` with an isolated modal widget (`#rag-chatbot-widget`), scoped Tailwind CSS (preflight disabled), and refactored modular vanilla JS (`chat-widget.js` & `eval-standalone.js`).

**Tech Stack:** FastAPI (`FileResponse`), HTML5, Vanilla JavaScript (ES6+ Namespaces), Tailwind CSS via CDN (`preflight: false`), marked.js, Lucide Icons, Chart.js.

---

### File Map

| Path | Action | Description |
|---|---|---|
| `app.py` | Modify | Update static route handlers (`root()`, `/testing`, `/evaluation`) using `FileResponse` |
| `static/demo/index.html` | Create | Scraped UNSRAT homepage + `#rag-chatbot-widget` markup & modal |
| `static/demo/evaluation.html` | Create | Standalone RAGAS evaluation dashboard |
| `static/demo/css/demo-modal.css` | Create | Scoped CSS reset (`box-sizing: border-box`) and custom modal animations |
| `static/demo/js/chat-widget.js` | Create | Refactored chat logic namespace (`RagChatWidget`) extracted from `app.js` |
| `static/demo/js/eval-standalone.js` | Create | Standalone evaluation logic extracted from `app.js` |

---

### Task 1: Setup Workspace & Directory Structure

**Files:**
- Create: `static/demo/css/demo-modal.css` (placeholder)
- Create: `static/demo/js/chat-widget.js` (placeholder)
- Create: `static/demo/js/eval-standalone.js` (placeholder)

- [ ] **Step 1: Create Git Branch**

Run command:
```bash
git checkout -b feature/unsrat-demo-frontend
```
Expected output: `Switched to a new branch 'feature/unsrat-demo-frontend'`

- [ ] **Step 2: Create directory tree and placeholder files**

Create directory `static/demo/css`, `static/demo/js`, `static/demo/assets`.
Create empty placeholder files:
- `static/demo/css/demo-modal.css`
- `static/demo/js/chat-widget.js`
- `static/demo/js/eval-standalone.js`

- [ ] **Step 3: Commit initial structure**

```bash
git add static/demo/
git commit -m "chore: setup folder structure static/demo"
```

---

### Task 2: Update FastAPI Static Route Handlers in `app.py`

**Files:**
- Modify: `app.py:596-608`

- [ ] **Step 1: Modify static routing in `app.py`**

In `app.py`, update imports at top to include `FileResponse` from `fastapi.responses` if not already imported.
Replace lines 596-608 in `app.py` with:

```python
# ── Static Files & Root ────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve demo UNSRAT replica homepage."""
    index_path = Path("static/demo/index.html")
    if not index_path.exists():
        return HTMLResponse("<h1>Frontend demo belum tersedia. Buat static/demo/index.html.</h1>")
    return FileResponse(index_path, media_type="text/html")


@app.get("/testing")
async def testing():
    """Serve initial SPA frontend for testing & debugging."""
    testing_path = Path("static/index.html")
    if not testing_path.exists():
        return HTMLResponse("<h1>Frontend testing tidak ditemukan di static/index.html.</h1>")
    return FileResponse(testing_path, media_type="text/html")


@app.get("/evaluation")
async def evaluation():
    """Serve standalone RAGAS evaluation page."""
    eval_path = Path("static/demo/evaluation.html")
    if not eval_path.exists():
        return HTMLResponse("<h1>Halaman evaluasi belum tersedia. Buat static/demo/evaluation.html.</h1>")
    return FileResponse(eval_path, media_type="text/html")
```

- [ ] **Step 2: Verify server routes startup**

Run command:
```bash
python -c "import app; print('App routes imported successfully')"
```
Expected output: `App routes imported successfully`

- [ ] **Step 3: Commit routing changes**

```bash
git add app.py
git commit -m "feat(routing): tambah route /testing dan /evaluation, alihkan / ke demo"
```

---

### Task 3: Build Replica Homepage & Scoped Modal Markup (`static/demo/index.html`)

**Files:**
- Create: `static/demo/index.html` (copy from `unsrat-ac-id.html` + insert `#rag-chatbot-widget`)

- [ ] **Step 1: Copy `unsrat-ac-id.html` to `static/demo/index.html`**

Copy `unsrat-ac-id.html` into `static/demo/index.html`.

- [ ] **Step 2: Inject Scoped Tailwind CDN Config & Dependencies**

Before `</head>` in `static/demo/index.html`, insert:
```html
<!-- Tailwind CDN dengan Preflight NONAKTIF untuk mencegah kontaminasi CSS WordPress -->
<script>
  tailwind.config = {
    corePlugins: { preflight: false },
    theme: {
      extend: {
        colors: {
          unsrat: {
            maroon: '#7B2D2D',
            'maroon-dark': '#5A1F1F',
            gold: '#D4AF37',
            light: '#F8F9FA'
          }
        }
      }
    }
  }
</script>
<script src="https://cdn.tailwindcss.com"></script>

<!-- Vendor CDN (marked.js & lucide) -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>

<!-- Scoped Custom CSS -->
<link rel="stylesheet" href="/static/demo/css/demo-modal.css">
```

- [ ] **Step 3: Inject Chatbot Widget Markup (`#rag-chatbot-widget`)**

Directly before `</body>` in `static/demo/index.html`, insert the `#rag-chatbot-widget` wrapper containing trigger button, overlay, and modal:

```html
<!-- RAG Chatbot Widget Container -->
<div id="rag-chatbot-widget" class="relative z-[999999]">
  <!-- Floating Trigger Button -->
  <button id="rag-trigger-btn" 
          aria-label="Buka Chatbot UNSRAT"
          class="fixed bottom-6 right-6 bg-[#7B2D2D] hover:bg-[#5A1F1F] text-white p-4 rounded-full shadow-2xl transition-all duration-300 transform hover:scale-110 flex items-center justify-center border-2 border-white/20 focus:outline-none cursor-pointer">
    <i data-lucide="message-square" class="w-7 h-7"></i>
  </button>

  <!-- Modal Overlay -->
  <div id="rag-modal-overlay" class="fixed inset-0 bg-black/50 backdrop-blur-xs hidden transition-opacity duration-300"></div>

  <!-- Chat Modal Window -->
  <div id="rag-modal" 
       class="fixed bottom-24 right-6 w-[92vw] max-w-[440px] h-[600px] max-h-[82vh] bg-white rounded-2xl shadow-2xl flex flex-col hidden overflow-hidden border border-gray-200 transition-all duration-300 transform scale-95 opacity-0">
    
    <!-- Modal Header -->
    <div class="bg-[#7B2D2D] text-white px-5 py-4 flex items-center justify-between shadow-md">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center border border-white/20">
          <i data-lucide="bot" class="w-5 h-5 text-amber-300"></i>
        </div>
        <div>
          <h3 class="font-bold text-base leading-tight">Asisten Layanan UNSRAT</h3>
          <span class="inline-flex items-center text-xs text-emerald-300 font-medium">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse mr-1.5"></span> Online
          </span>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <!-- Settings Toggle (Gear Icon) -->
        <button id="rag-settings-btn" title="Pengaturan Model & Config" class="text-white/80 hover:text-white p-1.5 rounded-lg hover:bg-white/10 transition-colors">
          <i data-lucide="settings" class="w-5 h-5"></i>
        </button>
        <!-- Close Button -->
        <button id="rag-modal-close" title="Tutup Modal" class="text-white/80 hover:text-white p-1.5 rounded-lg hover:bg-white/10 transition-colors">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
    </div>

    <!-- Collapsible Settings Panel (Hidden by Default) -->
    <div id="rag-settings-panel" class="hidden bg-stone-100 border-b border-stone-200 p-3 text-xs space-y-2">
      <div class="flex items-center justify-between gap-2">
        <label for="rag-config-select" class="font-semibold text-stone-700">Profil Config:</label>
        <select id="rag-config-select" class="bg-white border border-stone-300 rounded px-2 py-1 text-xs focus:ring-1 focus:ring-[#7B2D2D]">
          <option value="rag_gemini_default">RAG Gemini (Default)</option>
          <option value="rag_gemini_precise">RAG Gemini (Precise)</option>
        </select>
      </div>
      <div class="flex items-center justify-between gap-2">
        <label for="rag-model-select" class="font-semibold text-stone-700">Model Gemini:</label>
        <select id="rag-model-select" class="bg-white border border-stone-300 rounded px-2 py-1 text-xs focus:ring-1 focus:ring-[#7B2D2D]">
          <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
        </select>
      </div>
    </div>

    <!-- Chat Messages Container -->
    <div id="rag-chat-messages" class="flex-1 min-h-0 overflow-y-auto p-4 space-y-4 bg-stone-50/50">
      <!-- Welcome Message Bubble -->
      <div class="flex items-start space-x-3">
        <div class="w-8 h-8 rounded-full bg-[#7B2D2D] text-white flex items-center justify-center shrink-0">
          <i data-lucide="bot" class="w-4 h-4"></i>
        </div>
        <div class="bg-white border border-stone-200 rounded-2xl rounded-tl-none p-3.5 shadow-xs max-w-[85%] text-stone-800 text-sm">
          <p class="font-semibold mb-1">Selamat datang!</p>
          <p class="text-xs text-stone-600 leading-relaxed">Saya asisten AI Akademik Universitas Sam Ratulangi. Silakan tanyakan informasi terkait UKT, KRS, wisuda, atau fasilitas kampus.</p>
        </div>
      </div>
    </div>

    <!-- Chat Form Input -->
    <form id="rag-chat-form" class="p-3 bg-white border-t border-stone-200 flex items-center gap-2">
      <input id="rag-user-input" 
             type="text" 
             placeholder="Ketik pertanyaan akademik..." 
             autocomplete="off"
             class="flex-1 bg-stone-100 border border-stone-300 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#7B2D2D]/30 focus:border-[#7B2D2D] transition-all">
      <button id="rag-send-btn" 
              type="submit" 
              class="bg-[#7B2D2D] hover:bg-[#5A1F1F] text-white p-2.5 rounded-xl shadow-xs transition-colors flex items-center justify-center cursor-pointer">
        <i data-lucide="send" class="w-4 h-4"></i>
      </button>
    </form>
  </div>
</div>

<!-- Chat Logic Script -->
<script src="/static/demo/js/chat-widget.js"></script>
```

- [ ] **Step 4: Commit `index.html` changes**

```bash
git add static/demo/index.html
git commit -m "feat(demo): tambah homepage replika unsrat dengan tombol trigger dan kerangka modal"
```

---

### Task 4: Scoped Modal Styling (`static/demo/css/demo-modal.css`)

**Files:**
- Modify: `static/demo/css/demo-modal.css`

- [ ] **Step 1: Write `demo-modal.css` with Scoped Box-Sizing & Modal Animations**

Write to `static/demo/css/demo-modal.css`:

```css
/* 
 * Scoped CSS Reset untuk Widget Chat UNSRAT
 * Mencegah kebocoran style ke tema WordPress dan sebaliknya.
 */

#rag-chatbot-widget,
#rag-chatbot-widget *,
#rag-chatbot-widget *::before,
#rag-chatbot-widget *::after {
  box-sizing: border-box;
}

/* Modal Open Animation & Display Helpers */
#rag-modal.active {
  display: flex !important;
  opacity: 1 !important;
  transform: scale(1) !important;
}

#rag-modal-overlay.active {
  display: block !important;
  opacity: 1 !important;
}

/* Prevent scroll bleeding from modal messages to host window */
#rag-chat-messages {
  overscroll-behavior: contain;
  scroll-behavior: smooth;
}

/* Custom Scrollbar for Chat Messages */
#rag-chat-messages::-webkit-scrollbar {
  width: 5px;
}

#rag-chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

#rag-chat-messages::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 10px;
}

#rag-chat-messages::-webkit-scrollbar-thumb:hover {
  background: #9CA3AF;
}

/* Markdown prose rendering inside chat bubbles */
.rag-prose p {
  margin-bottom: 0.5rem;
}

.rag-prose p:last-child {
  margin-bottom: 0;
}

.rag-prose ul {
  list-style-type: disc;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
}

.rag-prose ol {
  list-style-type: decimal;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
}

.rag-prose code {
  background-color: #F3F4F6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.85em;
}
```

- [ ] **Step 2: Commit CSS styling**

```bash
git add static/demo/css/demo-modal.css
git commit -m "style(demo): styling modal dan scoping tailwind"
```

---

### Task 5: Modular JS Extraction (`static/demo/js/chat-widget.js`)

**Files:**
- Modify: `static/demo/js/chat-widget.js`

- [ ] **Step 1: Write `chat-widget.js` namespace**

Write `static/demo/js/chat-widget.js` containing full state management, SSE streaming parser for `/api/chat`, modal toggle, scroll lock, settings panel toggle, and citation renderer:

```javascript
/**
 * UNSRAT RAG Chatbot Widget Module
 * Encapsulated Namespace to avoid global scope pollution.
 */
const RagChatWidget = {
  state: {
    chatHistory: [],
    isStreaming: false,
    abortController: null,
    currentConfig: 'rag_gemini_default',
    currentModel: 'gemini-2.5-flash'
  },

  elements: {},

  init() {
    this.cacheElements();
    if (!this.elements.widget) return;

    this.bindEvents();
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
      settingsBtn: document.getElementById('rag-settings-btn'),
      settingsPanel: document.getElementById('rag-settings-panel'),
      configSelect: document.getElementById('rag-config-select'),
      modelSelect: document.getElementById('rag-model-select'),
      chatMessages: document.getElementById('rag-chat-messages'),
      chatForm: document.getElementById('rag-chat-form'),
      userInput: document.getElementById('rag-user-input'),
      sendBtn: document.getElementById('rag-send-btn')
    };
  },

  bindEvents() {
    const { triggerBtn, closeBtn, overlay, settingsBtn, chatForm, configSelect, modelSelect } = this.elements;

    if (triggerBtn) triggerBtn.addEventListener('click', () => this.toggleModal(true));
    if (closeBtn) closeBtn.addEventListener('click', () => this.toggleModal(false));
    if (overlay) overlay.addEventListener('click', () => this.toggleModal(false));
    
    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => {
        if (this.elements.settingsPanel) {
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

    if (chatForm) {
      chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleFormSubmit();
      });
    }
  },

  toggleModal(show) {
    const { modal, overlay, userInput } = this.elements;
    if (!modal) return;

    if (show) {
      modal.classList.remove('hidden');
      if (overlay) overlay.classList.remove('hidden');
      setTimeout(() => {
        modal.classList.add('active');
        if (overlay) overlay.classList.add('active');
      }, 10);
      document.body.classList.add('overflow-hidden');
      if (userInput) userInput.focus();
    } else {
      modal.classList.remove('active');
      if (overlay) overlay.classList.remove('active');
      setTimeout(() => {
        modal.classList.add('hidden');
        if (overlay) overlay.classList.add('hidden');
      }, 300);
      document.body.classList.remove('overflow-hidden');
      
      // Abort ongoing stream on modal close
      if (this.state.isStreaming && this.state.abortController) {
        this.state.abortController.abort();
      }
    }
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

  async handleFormSubmit() {
    const { userInput } = this.elements;
    if (!userInput) return;

    const query = userInput.value.trim();
    if (!query || this.state.isStreaming) return;

    userInput.value = '';
    this.renderUserBubble(query);

    this.state.isStreaming = true;
    this.state.abortController = new AbortController();

    const botBubbleObj = this.renderBotBubblePlaceholder();
    this.scrollToBottom();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: this.state.abortController.signal,
        body: JSON.stringify({
          message: query,
          config: this.state.currentConfig,
          history: this.state.chatHistory
        })
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullAnswer = '';
      let citations = [];

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
                fullAnswer += parsed.content;
                botBubbleObj.contentElem.innerHTML = marked.parse(fullAnswer);
                this.scrollToBottom();
              } else if (parsed.type === 'citation') {
                citations = parsed.citations || [];
              }
            } catch (e) {
              // Plain string token fallback
              fullAnswer += dataStr;
              botBubbleObj.contentElem.innerHTML = marked.parse(fullAnswer);
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
      if (error.name !== 'AbortError') {
        botBubbleObj.contentElem.innerHTML = `<span class="text-red-600">Error: ${error.message}</span>`;
      }
    } finally {
      this.state.isStreaming = false;
      this.safeCreateIcons();
    }
  },

  renderUserBubble(text) {
    const { chatMessages } = this.elements;
    if (!chatMessages) return;

    const div = document.createElement('div');
    div.className = 'flex items-start justify-end space-x-3';
    div.innerHTML = `
      <div class="bg-[#7B2D2D] text-white rounded-2xl rounded-tr-none p-3.5 shadow-xs max-w-[85%] text-sm">
        <p class="leading-relaxed">${this.escapeHtml(text)}</p>
      </div>
    `;
    chatMessages.appendChild(div);
  },

  renderBotBubblePlaceholder() {
    const { chatMessages } = this.elements;
    const div = document.createElement('div');
    div.className = 'flex items-start space-x-3';
    div.innerHTML = `
      <div class="w-8 h-8 rounded-full bg-[#7B2D2D] text-white flex items-center justify-center shrink-0">
        <i data-lucide="bot" class="w-4 h-4"></i>
      </div>
      <div class="bg-white border border-stone-200 rounded-2xl rounded-tl-none p-3.5 shadow-xs max-w-[85%] text-stone-800 text-sm rag-prose">
        <div class="bot-content text-stone-600 animate-pulse">Mengetik...</div>
      </div>
    `;
    chatMessages.appendChild(div);
    return {
      bubbleElem: div,
      contentElem: div.querySelector('.bot-content')
    };
  },

  renderCitations(containerElem, citations) {
    const citDiv = document.createElement('div');
    citDiv.className = 'mt-2 pt-2 border-t border-stone-200 text-xs text-stone-500 space-y-1';
    citDiv.innerHTML = `
      <div class="font-semibold text-stone-700">Sumber Referensi:</div>
      <ul class="list-disc pl-4 space-y-0.5">
        ${citations.map(c => `<li>${this.escapeHtml(c.title || c.source)}</li>`).join('')}
      </ul>
    `;
    containerElem.querySelector('.rag-prose').appendChild(citDiv);
  },

  scrollToBottom() {
    const { chatMessages } = this.elements;
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  },

  escapeHtml(str) {
    return str.replace(/[&<>"']/g, match => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[match]);
  }
};

document.addEventListener('DOMContentLoaded', () => RagChatWidget.init());
```

- [ ] **Step 2: Commit JS module**

```bash
git add static/demo/js/chat-widget.js
git commit -m "feat(demo): ekstraksi chat-widget.js dari app.js"
```

---

### Task 6: Standalone RAGAS Evaluation Page (`static/demo/evaluation.html` & `eval-standalone.js`)

**Files:**
- Create: `static/demo/evaluation.html`
- Create: `static/demo/js/eval-standalone.js`

- [ ] **Step 1: Write `evaluation.html`**

Write `static/demo/evaluation.html` (standalone evaluation dashboard with clean navbar and Chart.js):

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Evaluasi RAGAS | Chatbot UNSRAT</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-stone-100 min-h-screen text-stone-800">
  <!-- Standalone Top Bar -->
  <header class="bg-[#7B2D2D] text-white shadow-md py-4 px-6 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <h1 class="text-xl font-bold">Evaluasi Kinerja RAGAS - Chatbot UNSRAT</h1>
    </div>
    <a href="/" class="text-xs bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg border border-white/20 transition-colors">
      Kembali ke Demo Utama
    </a>
  </header>

  <!-- Main Content -->
  <main class="max-w-6xl mx-auto p-6 space-y-6">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-stone-200 flex justify-between items-center">
      <div>
        <h2 class="text-lg font-semibold">Hasil Evaluasi Metrik RAGAS</h2>
        <p class="text-sm text-stone-500">Evaluasi otomatis kuantitatif pipeline RAG menggunakan framework RAGAS.</p>
      </div>
      <button id="refresh-eval-btn" class="bg-[#7B2D2D] hover:bg-[#5A1F1F] text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors flex items-center gap-2">
        <i data-lucide="refresh-cw" class="w-4 h-4"></i> Muat Ulang Data
      </button>
    </div>

    <!-- Chart & Table Container -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
        <h3 class="font-semibold mb-4">Grafik Skor RAGAS</h3>
        <canvas id="ragasChart"></canvas>
      </div>
      
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 space-y-4">
        <h3 class="font-semibold">Ringkasan Metrik</h3>
        <div id="eval-metrics-summary" class="text-sm text-stone-600 leading-relaxed">
          Memuat data evaluasi...
        </div>
      </div>
    </div>
  </main>

  <script src="/static/demo/js/eval-standalone.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write `eval-standalone.js`**

Write `static/demo/js/eval-standalone.js`:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  const refreshBtn = document.getElementById('refresh-eval-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', loadEvaluationData);
  }

  loadEvaluationData();
});

async function loadEvaluationData() {
  const summaryElem = document.getElementById('eval-metrics-summary');
  if (summaryElem) summaryElem.innerHTML = 'Memuat data evaluasi...';

  try {
    const res = await fetch('/api/evaluation');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    renderChart(data);

    if (summaryElem) {
      summaryElem.innerHTML = `
        <div class="space-y-2">
          <div class="flex justify-between border-b pb-1"><span>Faithfulness:</span> <strong class="text-stone-800">${data.faithfulness ?? 'N/A'}</strong></div>
          <div class="flex justify-between border-b pb-1"><span>Answer Relevancy:</span> <strong class="text-stone-800">${data.answer_relevancy ?? 'N/A'}</strong></div>
          <div class="flex justify-between border-b pb-1"><span>Context Precision:</span> <strong class="text-stone-800">${data.context_precision ?? 'N/A'}</strong></div>
          <div class="flex justify-between border-b pb-1"><span>Context Recall:</span> <strong class="text-stone-800">${data.context_recall ?? 'N/A'}</strong></div>
        </div>
      `;
    }
  } catch (err) {
    if (summaryElem) {
      summaryElem.innerHTML = `<span class="text-red-600">Gagal memuat data evaluasi: ${err.message}</span>`;
    }
  }
}

function renderChart(data) {
  const ctx = document.getElementById('ragasChart');
  if (!ctx) return;

  if (window.myRagasChart) {
    window.myRagasChart.destroy();
  }

  window.myRagasChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Faithfulness', 'Answer Relevancy', 'Context Precision', 'Context Recall'],
      datasets: [{
        label: 'Skor RAGAS',
        data: [
          data.faithfulness || 0,
          data.answer_relevancy || 0,
          data.context_precision || 0,
          data.context_recall || 0
        ],
        backgroundColor: 'rgba(123, 45, 45, 0.2)',
        borderColor: '#7B2D2D',
        pointBackgroundColor: '#7B2D2D'
      }]
    },
    options: {
      scales: {
        r: { min: 0, max: 1 }
      }
    }
  });
}
```

- [ ] **Step 3: Commit evaluation files**

```bash
git add static/demo/evaluation.html static/demo/js/eval-standalone.js
git commit -m "feat(demo): implementasi halaman evaluasi standalone"
```

---

### Task 7: Comprehensive Regression Check & File Integrity Audit

- [ ] **Step 1: Check git status to ensure baseline files are UNTOUCHED**

Run:
```bash
git status
```
Verify that NONE of the following files were modified:
- `static/index.html`
- `static/js/app.js`
- `static/js/dev.js`
- `static/dev.html`
- Any files under `src/`

- [ ] **Step 2: Start server and test all endpoints**

Run command:
```bash
python app.py
```
Test routes via browser or curl:
- `http://localhost:8000/` -> Serves UNSRAT replica homepage
- `http://localhost:8000/testing` -> Serves original SPA frontend
- `http://localhost:8000/evaluation` -> Serves standalone RAGAS dashboard
- `http://localhost:8000/dev` -> Serves dev dashboard

- [ ] **Step 3: Commit testing documentation**

```bash
git commit -m "test: verifikasi manual seluruh route dan fitur" --allow-empty
```
