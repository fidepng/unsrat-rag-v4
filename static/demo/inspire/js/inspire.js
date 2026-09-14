/**
 * UNSRAT RAG Chatbot Widget Module
 * Encapsulated Namespace - Minimal & Defensif.
 */
const FEATURE_FLAGS = {
  showConfigModelSelect: true,
  showModelSelect: false
};

const RAG_ICONS = {
  send: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>`,
  stop: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/></svg>`,
  expand: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17V7h10"/><path d="M17 17 7 7"/></svg>`,
  minimize: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg>`,
  bookOpen: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6.5 6H20"/></svg>`,
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

    this.stripButtonTitles();
    this.bindEvents();
    this.applyFeatureFlags();
    this.loadSystemConfig();
  },

  stripButtonTitles() {
    if (this.elements.widget) {
      this.elements.widget.querySelectorAll('button[title]').forEach(btn => btn.removeAttribute('title'));
    }
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
      headerGuideBtn: document.getElementById('rag-header-guide-btn'),
      settingsPanel: document.getElementById('rag-settings-panel'),
      modelMenuItem: document.getElementById('rag-model-menu-item'),
      chatMessages: document.getElementById('rag-chat-messages'),
      welcomeState: document.getElementById('rag-welcome-state'),
      chatForm: document.getElementById('rag-chat-form'),
      userInput: document.getElementById('rag-user-input'),
      sendBtn: document.getElementById('rag-send-btn'),
      sideCitationPanel: document.getElementById('rag-side-citation-panel'),
      sideCitationBody: document.getElementById('rag-side-citation-body'),
      closeCitationBtn: document.getElementById('rag-close-citation-btn'),
      sheetBackdrop: document.getElementById('rag-sheet-backdrop')
    };

    if (this.elements.welcomeState) {
      this.welcomeStateHTML = this.elements.welcomeState.outerHTML;
    }
  },

  applyFeatureFlags() {
    const { settingsBtn, settingsPanel, modelMenuItem } = this.elements;

    if (!FEATURE_FLAGS.showConfigModelSelect) {
      if (settingsBtn) settingsBtn.classList.add('hidden');
      if (settingsPanel) settingsPanel.classList.add('hidden');
    } else {
      if (settingsBtn) settingsBtn.classList.remove('hidden');

      if (settingsPanel) {
        if (!FEATURE_FLAGS.showModelSelect) {
          settingsPanel.classList.add('rag-settings-flat');
          if (modelMenuItem) modelMenuItem.classList.add('hidden');
        } else {
          settingsPanel.classList.remove('rag-settings-flat');
          if (modelMenuItem) modelMenuItem.classList.remove('hidden');
        }
      }
    }
  },

  bindEvents() {
    const { 
      triggerBtn, closeBtn, expandBtn, resetBtn, overlay, 
      settingsBtn, settingsPanel, chatForm, userInput, sendBtn, 
      closeCitationBtn, chatMessages, sheetBackdrop 
    } = this.elements;

    if (triggerBtn) triggerBtn.addEventListener('click', () => this.toggleModal());
    if (closeBtn) closeBtn.addEventListener('click', () => this.toggleModal(false));
    if (overlay) overlay.addEventListener('click', () => this.toggleModal(false));
    if (expandBtn) expandBtn.addEventListener('click', () => this.toggleExpand());

    // Reset confirmation popover controls
    const resetConfirmPopover = document.getElementById('rag-reset-confirm');
    const resetCancelBtn = document.getElementById('rag-reset-cancel-btn');
    const resetProceedBtn = document.getElementById('rag-reset-proceed-btn');

    const hideResetConfirm = () => {
      if (resetConfirmPopover) resetConfirmPopover.classList.add('hidden');
    };

    if (resetBtn) {
      resetBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const welcomeState = document.getElementById('rag-welcome-state');
        const isWelcomeActive = welcomeState && !welcomeState.classList.contains('hidden');
        
        // If already on welcome screen without active messages, reset immediately
        if (isWelcomeActive) {
          this.resetChat();
          hideResetConfirm();
          return;
        }

        // Active chat: toggle confirmation safety popover
        if (resetConfirmPopover) {
          resetConfirmPopover.classList.toggle('hidden');
        }
      });
    }

    if (resetCancelBtn) {
      resetCancelBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        hideResetConfirm();
      });
    }

    if (resetProceedBtn) {
      resetProceedBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.resetChat();
        hideResetConfirm();
      });
    }

    // Dismiss reset confirm popover on outside click
    document.addEventListener('click', (e) => {
      if (resetConfirmPopover && !resetConfirmPopover.classList.contains('hidden')) {
        if (!resetConfirmPopover.contains(e.target) && !resetBtn.contains(e.target)) {
          hideResetConfirm();
        }
      }
    });

    if (settingsBtn) {
      settingsBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        hideResetConfirm();
        if (settingsPanel && FEATURE_FLAGS.showConfigModelSelect) {
          settingsPanel.classList.toggle('hidden');
          // Reset active submenus when toggling settings panel
          settingsPanel.querySelectorAll('.rag-menu-item').forEach(item => item.classList.remove('active'));
        }
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (settingsPanel && !settingsPanel.classList.contains('hidden')) {
          if (!settingsPanel.contains(e.target) && !settingsBtn.contains(e.target)) {
            settingsPanel.classList.add('hidden');
            settingsPanel.querySelectorAll('.rag-menu-item').forEach(item => item.classList.remove('active'));
          }
        }
      });
    }

    if (settingsPanel) {
      settingsPanel.addEventListener('click', (e) => {
        e.stopPropagation();

        // Touch/Tap Toggle for Submenu labels
        const menuLabel = e.target.closest('.rag-menu-label');
        if (menuLabel) {
          const parentItem = menuLabel.closest('.rag-menu-item');
          if (parentItem) {
            const wasActive = parentItem.classList.contains('active');
            settingsPanel.querySelectorAll('.rag-menu-item').forEach(item => item.classList.remove('active'));
            if (!wasActive) {
              parentItem.classList.add('active');
            }
          }
          return;
        }

        const optionBtn = e.target.closest('.rag-submenu-option');
        if (optionBtn) {
          const type = optionBtn.getAttribute('data-type');
          const val = optionBtn.getAttribute('data-value');
          if (!type || !val) return;

          if (type === 'config') {
            this.state.currentConfig = val;
          } else if (type === 'model') {
            this.state.currentModel = val;
          }

          const parentSubmenu = optionBtn.closest('.rag-submenu');
          if (parentSubmenu) {
            parentSubmenu.querySelectorAll('.rag-submenu-option').forEach(btn => {
              const isMatch = btn.getAttribute('data-value') === val;
              btn.classList.toggle('active', isMatch);
            });
          }

          // Close submenu on selection
          const parentItem = optionBtn.closest('.rag-menu-item');
          if (parentItem) parentItem.classList.remove('active');
          if (settingsPanel) settingsPanel.classList.add('hidden');
        }
      });
    }

    if (closeCitationBtn) {
      closeCitationBtn.addEventListener('click', () => this.toggleCitationPanel(false));
    }

    if (sheetBackdrop) {
      sheetBackdrop.addEventListener('click', () => this.toggleCitationPanel(false));
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

    // Guide Popup Modal Controls
    const guideModal = document.getElementById('rag-guide-modal');
    const guideCloseBtn = document.getElementById('rag-guide-modal-close');
    const guideBackdrop = document.getElementById('rag-guide-modal-backdrop');
    const { headerGuideBtn } = this.elements;

    const openGuideModal = () => {
      if (guideModal) {
        guideModal.classList.remove('hidden');
        void guideModal.offsetWidth; // Force reflow for smooth transition
        guideModal.classList.add('active');
        const trigger = document.getElementById('rag-guide-toggle-btn');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
        if (headerGuideBtn) {
          headerGuideBtn.setAttribute('aria-expanded', 'true');
          headerGuideBtn.classList.add('rag-header-btn-active');
        }
      }
    };

    const closeGuideModal = () => {
      if (guideModal) {
        guideModal.classList.remove('active');
        const trigger = document.getElementById('rag-guide-toggle-btn');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
        if (headerGuideBtn) {
          headerGuideBtn.setAttribute('aria-expanded', 'false');
          headerGuideBtn.classList.remove('rag-header-btn-active');
        }
        setTimeout(() => {
          if (!guideModal.classList.contains('active')) {
            guideModal.classList.add('hidden');
          }
        }, 240);
      }
    };

    const toggleGuideModal = () => {
      if (!guideModal) return;
      const isOpen = guideModal.classList.contains('active');
      if (isOpen) {
        closeGuideModal();
      } else {
        openGuideModal();
      }
    };

    if (guideCloseBtn) guideCloseBtn.addEventListener('click', closeGuideModal);
    if (guideBackdrop) guideBackdrop.addEventListener('click', closeGuideModal);
    if (headerGuideBtn) headerGuideBtn.addEventListener('click', toggleGuideModal);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (guideModal && guideModal.classList.contains('active')) {
          closeGuideModal();
        } else if (this.elements.sideCitationPanel && !this.elements.sideCitationPanel.classList.contains('hidden')) {
          this.toggleCitationPanel(false);
        }
      }
    });

    // Delegated interactions on chatMessages (Guide Open & Topic Chip Pre-Fill)
    if (chatMessages) {
      chatMessages.addEventListener('click', (e) => {
        // 1. Toggle Guide Popup Modal
        const guideToggleBtn = e.target.closest('#rag-guide-toggle-btn');
        if (guideToggleBtn) {
          toggleGuideModal();
          return;
        }

        // 2. Pre-fill Topic Chip (Fill textarea & focus, do NOT auto-submit)
        const topicChip = e.target.closest('.rag-topic-chip');
        if (topicChip) {
          const template = topicChip.getAttribute('data-template');
          if (template && userInput) {
            userInput.value = template;
            this.adjustTextareaHeight();
            userInput.focus();
            userInput.classList.add('rag-pulse-focus');
            setTimeout(() => userInput.classList.remove('rag-pulse-focus'), 500);
          }
          return;
        }

        // Backward compatibility
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

  toggleModal(forceState) {
    const { modal, overlay, userInput, triggerBtn } = this.elements;
    if (!modal) return;

    const isCurrentlyOpen = !modal.classList.contains('hidden') && modal.classList.contains('rag-modal-open');
    const shouldShow = forceState !== undefined ? forceState : !isCurrentlyOpen;

    if (this.modalCloseTimeout) {
      clearTimeout(this.modalCloseTimeout);
      this.modalCloseTimeout = null;
    }

    if (shouldShow) {
      modal.classList.remove('hidden');
      if (overlay) {
        overlay.classList.remove('hidden');
        void overlay.offsetWidth;
        overlay.classList.add('active');
        if (this.state.mode === 'expanded') {
          overlay.classList.add('rag-overlay-expanded');
        }
      }
      if (triggerBtn) triggerBtn.classList.add('rag-trigger-hidden');
      void modal.offsetWidth; // Force reflow for smooth transition
      modal.classList.add('rag-modal-open');
      if (userInput) userInput.focus();
    } else {
      modal.classList.remove('rag-modal-open');
      if (overlay) {
        overlay.classList.remove('active');
        overlay.classList.remove('rag-overlay-expanded');
      }
      if (triggerBtn) triggerBtn.classList.remove('rag-trigger-hidden');
      
      if (this.state.status === 'streaming' && this.state.abortController) {
        this.state.abortController.abort();
      }

      this.modalCloseTimeout = setTimeout(() => {
        if (!modal.classList.contains('rag-modal-open')) {
          modal.classList.add('hidden');
          if (overlay) overlay.classList.add('hidden');
        }
        this.modalCloseTimeout = null;
      }, 300);
    }
  },

  toggleExpand(forceState) {
    const { modal, expandBtn, overlay } = this.elements;
    if (!modal) return;

    const shouldExpand = forceState !== undefined ? forceState : this.state.mode === 'compact';
    if (shouldExpand) {
      this.state.mode = 'expanded';
      modal.classList.remove('rag-modal-compact');
      modal.classList.add('rag-modal-expanded');
      if (overlay && modal.classList.contains('rag-modal-open')) {
        overlay.classList.add('rag-overlay-expanded');
      }
      if (expandBtn) {
        expandBtn.innerHTML = RAG_ICONS.minimize;
      }
    } else {
      this.state.mode = 'compact';
      modal.classList.remove('rag-modal-expanded');
      modal.classList.add('rag-modal-compact');
      if (overlay) {
        overlay.classList.remove('rag-overlay-expanded');
      }
      if (expandBtn) {
        expandBtn.innerHTML = RAG_ICONS.expand;
      }
      this.toggleCitationPanel(false);
    }
  },

  adjustTextareaHeight() {
    const { userInput } = this.elements;
    if (!userInput) return;
    userInput.style.height = 'auto';
    const scrollH = userInput.scrollHeight;
    if (scrollH > 120) {
      userInput.style.height = '120px';
      userInput.style.overflowY = 'auto';
    } else {
      userInput.style.height = `${Math.max(scrollH, 42)}px`;
      userInput.style.overflowY = 'hidden';
    }
  },

  resetChat() {
    const { chatMessages, headerGuideBtn } = this.elements;
    if (this.state.status === 'streaming' && this.state.abortController) {
      this.state.abortController.abort();
    }
    this.state.chatHistory = [];
    this.state.status = 'idle';
    this.toggleCitationPanel(false);

    if (headerGuideBtn) {
      headerGuideBtn.classList.add('rag-header-btn-hidden');
    }

    if (chatMessages && this.welcomeStateHTML) {
      chatMessages.innerHTML = this.welcomeStateHTML;
    }
  },

  async loadSystemConfig() {
    try {
      const res = await fetch('/api/config');
      if (res.ok) {
        const data = await res.json();
        const modelSubmenu = document.getElementById('rag-model-submenu');
        if (data.available_models && modelSubmenu) {
          modelSubmenu.innerHTML = data.available_models.map((m, idx) => `
            <button type="button" class="rag-submenu-option ${idx === 0 ? 'active' : ''}" data-type="model" data-value="${m}">${m}</button>
          `).join('');
        }
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
    const { headerGuideBtn } = this.elements;
    if (headerGuideBtn) {
      headerGuideBtn.classList.remove('rag-header-btn-hidden');
    }
  },

  updateSendButtonState(isStreaming) {
    const { sendBtn } = this.elements;
    if (!sendBtn) return;
    if (isStreaming) {
      sendBtn.innerHTML = RAG_ICONS.stop;
    } else {
      sendBtn.innerHTML = RAG_ICONS.send;
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
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Pertahankan baris parsial yang belum lengkap

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;

          const dataStr = trimmed.slice(6).trim();
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
            console.warn('Gagal parse JSON SSE line:', dataStr, e);
          }
        }
      }

      if (buffer && buffer.trim().startsWith('data: ')) {
        const dataStr = buffer.trim().slice(6).trim();
        try {
          const parsed = JSON.parse(dataStr);
          if (parsed.type === 'token') {
            fullAnswer += parsed.content;
            botBubbleObj.contentElem.innerHTML = window.marked ? window.marked.parse(fullAnswer) : this.escapeHtml(fullAnswer);
          } else if (parsed.type === 'citations') {
            citations = parsed.sources || [];
          }
        } catch (e) {
          // ignore
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
        <div class="rag-msg-content">
          <div class="rag-typing-dots">
            <span class="rag-dot"></span>
            <span class="rag-dot"></span>
            <span class="rag-dot"></span>
          </div>
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
            <span>${sources.length} Sumber Rujukan</span>
          </div>
          ${RAG_ICONS.chevronRight}
        </button>
      </div>
    `;

    containerElem.appendChild(citDiv);

    const headerBtn = citDiv.querySelector('.rag-citation-header');
    if (headerBtn) {
      headerBtn.addEventListener('click', () => {
        const isMobile = window.innerWidth <= 768;
        if (!isMobile && this.state.mode === 'compact') {
          this.toggleExpand(true);
        }
        this.openSideCitationPanel(sources);
      });
    }
  },

  openSideCitationPanel(sources) {
    const { sideCitationPanel, sideCitationBody, sheetBackdrop } = this.elements;
    if (!sideCitationPanel || !sideCitationBody) return;

    this.state.activeCitations = sources;
    sideCitationBody.innerHTML = sources.map((src, index) => {
      const title = src.title || "Dokumen Akademik UNSRAT";
      const docId = src.doc_id ? `ID: ${src.doc_id}` : "";
      const bab = src.bab ? `${src.bab}` : "";
      const bagian = src.bagian ? `${src.bagian}` : "";
      const pasal = src.pasal ? (String(src.pasal).toLowerCase().startsWith('pasal') ? `${src.pasal}` : `Pasal ${src.pasal}`) : "";
      const breadcrumbList = [bab, bagian, pasal].filter(Boolean);
      const breadcrumbsHTML = breadcrumbList.length > 0 
        ? `<div class="rag-citation-breadcrumbs">${breadcrumbList.map(b => `<span>${this.escapeHtml(b)}</span>`).join('<span class="rag-dot-sep">•</span>')}</div>`
        : '';
      const idx = src.index || (index + 1);

      return `
        <div class="rag-citation-item">
          <div class="rag-citation-topbar">
            <span class="rag-citation-idx-badge">[${this.escapeHtml(idx)}]</span>
            ${docId ? `<span class="rag-citation-docid-badge">${this.escapeHtml(docId)}</span>` : ''}
          </div>
          <h5 class="rag-citation-title-text">${this.escapeHtml(title)}</h5>
          ${breadcrumbsHTML}
          <div class="rag-citation-snippet">${this.escapeHtml(src.content)}</div>
        </div>
      `;
    }).join('');

    sideCitationPanel.classList.remove('hidden');

    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      void sideCitationPanel.offsetWidth;
      sideCitationPanel.classList.add('rag-sheet-open');
      if (sheetBackdrop) {
        sheetBackdrop.classList.remove('hidden');
        void sheetBackdrop.offsetWidth;
        sheetBackdrop.classList.add('active');
      }
    }
  },

  toggleCitationPanel(show) {
    const { sideCitationPanel, sheetBackdrop } = this.elements;
    if (!sideCitationPanel) return;

    if (show) {
      this.openSideCitationPanel(this.state.activeCitations);
      return;
    }

    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      sideCitationPanel.classList.remove('rag-sheet-open');
      if (sheetBackdrop) {
        sheetBackdrop.classList.remove('active');
        setTimeout(() => {
          if (!sheetBackdrop.classList.contains('active')) {
            sheetBackdrop.classList.add('hidden');
          }
        }, 240);
      }
      setTimeout(() => {
        if (!sideCitationPanel.classList.contains('rag-sheet-open')) {
          sideCitationPanel.classList.add('hidden');
        }
      }, 280);
    } else {
      sideCitationPanel.classList.remove('rag-sheet-open');
      sideCitationPanel.classList.add('hidden');
      if (sheetBackdrop) {
        sheetBackdrop.classList.remove('active');
        sheetBackdrop.classList.add('hidden');
      }
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
