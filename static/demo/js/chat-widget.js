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
              } else if (parsed.type === 'citation') {
                citations = parsed.citations || [];
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

  renderCitations(containerElem, citations) {
    const citDiv = document.createElement('div');
    citDiv.style.marginTop = '8px';
    citDiv.style.paddingTop = '8px';
    citDiv.style.borderTop = '1px solid #e7e5e4';
    citDiv.style.fontSize = '11px';
    citDiv.style.color = '#78716c';
    citDiv.innerHTML = `
      <strong style="color: #44403c;">Sumber Referensi:</strong>
      <ul style="padding-left: 16px; margin-top: 4px; margin-bottom: 0;">
        ${citations.map(c => `<li>${this.escapeHtml(c.title || c.source)}</li>`).join('')}
      </ul>
    `;
    containerElem.querySelector('.rag-msg-content').appendChild(citDiv);
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
