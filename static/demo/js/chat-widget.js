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
