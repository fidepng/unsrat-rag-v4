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
