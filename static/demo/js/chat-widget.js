/**
 * UNSRAT RAG Chatbot Widget Module
 * Encapsulated Namespace - Minimal & Defensif.
 */
const RagChatWidget = {
  state: {
    chatHistory: [],
    isStreaming: false,
    abortController: null,
    currentConfig: 'b',
    currentModel: 'gemini-3.5-flash'
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
      document.body.classList.add('overflow-hidden');
      if (userInput) userInput.focus();
    } else {
      modal.classList.add('hidden');
      if (overlay) overlay.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
      
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

    let isFirstToken = true;

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

      // Render Rujukan Dokumen Akademik (Accordion) jika tersedia
      if (citations.length > 0) {
        this.renderCitations(botBubbleObj.bubbleElem, citations);
      }

      this.state.chatHistory.push({ role: 'user', content: query });
      this.state.chatHistory.push({ role: 'assistant', content: fullAnswer });

    } catch (error) {
      if (error.name !== 'AbortError') {
        botBubbleObj.contentElem.innerHTML = `<span style="color: #dc2626;">Error: ${error.message}</span>`;
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
    div.className = 'rag-msg rag-user-msg';
    div.innerHTML = `<p style="margin: 0;">${this.escapeHtml(text)}</p>`;
    chatMessages.appendChild(div);
  },

  renderBotBubblePlaceholder() {
    const { chatMessages } = this.elements;
    const div = document.createElement('div');
    div.className = 'rag-msg rag-bot-msg';
    div.innerHTML = `
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

    const citId = `cit-${Date.now()}`;
    const headerId = `cit-header-${citId}`;
    const contentId = `cit-content-${citId}`;
    const chevronId = `cit-chevron-${citId}`;

    const citDiv = document.createElement('div');
    citDiv.className = 'rag-citations-container';
    citDiv.innerHTML = `
      <div class="rag-citation-box">
        <button id="${headerId}" type="button" class="rag-citation-header">
          <div class="rag-citation-title">
            <i data-lucide="book-open"></i>
            <span>Rujukan Dokumen Akademik (${sources.length} Sumber)</span>
          </div>
          <i data-lucide="chevron-down" id="${chevronId}" class="rag-chevron"></i>
        </button>
        <div id="${contentId}" class="rag-citation-content hidden">
          ${sources.map((src, index) => {
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
          }).join('')}
        </div>
      </div>
    `;

    containerElem.appendChild(citDiv);
    this.safeCreateIcons();

    const headerBtn = document.getElementById(headerId);
    const contentDiv = document.getElementById(contentId);
    const chevronIcon = document.getElementById(chevronId);

    if (headerBtn && contentDiv) {
      headerBtn.addEventListener('click', () => {
        const isHidden = contentDiv.classList.contains('hidden');
        if (isHidden) {
          contentDiv.classList.remove('hidden');
          if (chevronIcon) chevronIcon.classList.add('rotate-180');
        } else {
          contentDiv.classList.add('hidden');
          if (chevronIcon) chevronIcon.classList.remove('rotate-180');
        }
        this.scrollToBottom();
      });
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
