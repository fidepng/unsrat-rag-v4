/**
 * UNSRAT RAG Chatbot Widget Module
 * Encapsulated Namespace - Minimal & Defensif.
 */
const FEATURE_FLAGS = {
  showConfigModelSelect: true
};

const RAG_ICONS = {
  send: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>`,
  stop: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/></svg>`,
  expand: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17V7h10"/><path d="M17 17 7 7"/></svg>`,
  minimize: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg>`,
  bookOpen: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6.5 6H20"/></svg>`,
  compass: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>`,
  layers: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.5-8.58 3.91a2 2 0 0 1-1.66 0L3.17 12.5"/><path d="m22 17.5-8.58 3.91a2 2 0 0 1-1.66 0L3.17 17.5"/></svg>`,
  alertTriangle: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  fileText: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>`,
  chevronRight: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>`,
  alertCircle: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
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
      settingsBtn, settingsPanel, chatForm, userInput, sendBtn, 
      configSelect, modelSelect, closeCitationBtn, chatMessages 
    } = this.elements;

    if (triggerBtn) triggerBtn.addEventListener('click', () => this.toggleModal(true));
    if (closeBtn) closeBtn.addEventListener('click', () => this.toggleModal(false));
    if (overlay) overlay.addEventListener('click', () => this.toggleModal(false));
    if (expandBtn) expandBtn.addEventListener('click', () => this.toggleExpand());
    if (resetBtn) resetBtn.addEventListener('click', () => this.resetChat());

    if (settingsBtn) {
      settingsBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (settingsPanel && FEATURE_FLAGS.showConfigModelSelect) {
          settingsPanel.classList.toggle('hidden');
        }
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (settingsPanel && !settingsPanel.classList.contains('hidden')) {
          if (!settingsPanel.contains(e.target) && !settingsBtn.contains(e.target)) {
            settingsPanel.classList.add('hidden');
          }
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
        expandBtn.innerHTML = RAG_ICONS.minimize;
      }
    } else {
      this.state.mode = 'compact';
      modal.classList.remove('rag-modal-expanded');
      modal.classList.add('rag-modal-compact');
      if (expandBtn) {
        expandBtn.setAttribute('title', 'Buka Mode Ukuran Besar');
        expandBtn.innerHTML = RAG_ICONS.expand;
      }
      this.toggleCitationPanel(false);
    }
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
              ${RAG_ICONS.bookOpen}
              <span>Syarat cuti akademik?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Visi dan Misi UNSRAT?">
              ${RAG_ICONS.compass}
              <span>Visi dan Misi UNSRAT?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Beban SKS semester 1?">
              ${RAG_ICONS.layers}
              <span>Beban SKS semester 1?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Mekanisme evaluasi DO?">
              ${RAG_ICONS.alertTriangle}
              <span>Mekanisme evaluasi DO?</span>
            </button>
            <button type="button" class="rag-chip-btn" data-query="Prosedur pengisian KRS?">
              ${RAG_ICONS.fileText}
              <span>Prosedur pengisian KRS?</span>
            </button>
          </div>
        </div>
      `;
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
      sendBtn.innerHTML = RAG_ICONS.stop;
      sendBtn.setAttribute('title', 'Hentikan Pencarian');
    } else {
      sendBtn.innerHTML = RAG_ICONS.send;
      sendBtn.setAttribute('title', 'Kirim Pesan');
    }
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
          warningBadge.innerHTML = `${RAG_ICONS.alertCircle}<span>Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap.</span>`;
          botBubbleObj.bubbleElem.appendChild(warningBadge);
        }
      } else {
        botBubbleObj.contentElem.innerHTML = `<span style="color: #dc2626;">Error: ${error.message}</span>`;
      }
    } finally {
      this.state.status = 'idle';
      this.updateSendButtonState(false);
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

    const wrapper = document.createElement('div');
    wrapper.className = 'rag-msg-wrapper rag-msg-user-wrapper';
    wrapper.innerHTML = `
      <div class="rag-msg-meta-header">
        <span>Anda</span>
        <span>•</span>
        <span>${this.getTimestamp()}</span>
      </div>
      <div class="rag-user-msg">${this.escapeHtml(text)}</div>
    `;
    chatMessages.appendChild(wrapper);
  },

  renderBotBubblePlaceholder() {
    const { chatMessages } = this.elements;
    const wrapper = document.createElement('div');
    wrapper.className = 'rag-msg-wrapper rag-msg-bot-wrapper';
    wrapper.innerHTML = `
      <div class="rag-msg-meta-header">
        <span>Asisten Akademik</span>
        <span>•</span>
        <span>${this.getTimestamp()}</span>
      </div>
      <div class="rag-bot-msg">
        <div class="rag-msg-content" style="color: #78716c;">
          <span>Mengetik...</span>
        </div>
      </div>
    `;
    chatMessages.appendChild(wrapper);
    return {
      bubbleElem: wrapper.querySelector('.rag-bot-msg'),
      contentElem: wrapper.querySelector('.rag-msg-content')
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
            ${RAG_ICONS.bookOpen}
            <span>Rujukan Dokumen Akademik (${sources.length} Sumber)</span>
          </div>
          ${RAG_ICONS.chevronRight}
        </button>
      </div>
    `;

    containerElem.appendChild(citDiv);

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
