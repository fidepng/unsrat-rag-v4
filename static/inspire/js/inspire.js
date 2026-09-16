/**
 * UNSRAT RAG Chatbot Widget Module
 * Encapsulated Namespace - Minimal & Defensif.
 */
const FEATURE_FLAGS = {
  showConfigModelSelect: false,
  showModelSelect: false
};

const RAG_ICONS = {
  send: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>`,
  stop: `<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" stroke="none"><rect width="14" height="14" x="5" y="5" rx="3"/></svg>`,
  expand: `<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 3 3 3 3 9"/><line x1="3" x2="10" y1="3" y2="10"/><polyline points="15 21 21 21 21 15"/><line x1="21" x2="14" y1="21" y2="14"/></svg>`,
  minimize: `<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 10 10 10 10 4"/><line x1="10" y1="10" x2="3" y2="3"/><polyline points="20 14 14 14 14 20"/><line x1="14" y1="14" x2="21" y2="21"/></svg>`,
  bookOpen: `<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`,
  chevronRight: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>`,
  alertCircle: `<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>`
};

const RagChatWidget = {
  state: {
    chatHistory: [],
    status: 'idle', // 'idle' | 'streaming'
    mode: 'compact', // 'compact' | 'expanded'
    abortController: null,
    currentConfig: 'b',
    currentModel: 'gemini-3.5-flash',
    activeCitations: [],
    displayedMsgId: null,
    messageSourcesMap: new Map(),
    lastQuery: '',
    isTimedOut: false
  },

  elements: {},

  init() {
    this.cacheElements();
    if (!this.elements.widget) return;

    if (this.elements.bgIframe && window.location.search) {
      this.elements.bgIframe.src = '/static/inspire/background.html' + window.location.search;
    }

    if (window.marked && typeof window.marked.use === 'function') {
      window.marked.use({
        gfm: true,
        breaks: true,
        async: false
      });
    } else if (window.marked && typeof window.marked.setOptions === 'function') {
      window.marked.setOptions({
        breaks: true,
        gfm: true
      });
    }

    this.bindEvents();
    this.setupSheetGesture();
    this.bindNetworkEvents();
    this.applyFeatureFlags();
    this.loadSystemConfig();
    this.initOnboarding();
  },

  initOnboarding() {
    const { onboardModal } = this.elements;
    if (!onboardModal) return;
    onboardModal.classList.remove('hidden');
  },

  dismissOnboarding(openChat = false) {
    const { onboardModal } = this.elements;
    if (onboardModal) {
      onboardModal.classList.add('hidden');
    }

    if (openChat) {
      this.toggleModal(true);
    }
  },

  bindNetworkEvents() {
    window.addEventListener('online', () => this.handleNetworkChange());
    window.addEventListener('offline', () => this.handleNetworkChange());
    this.handleNetworkChange();
  },

  handleNetworkChange() {
    const isOffline = typeof navigator !== 'undefined' && !navigator.onLine;
    const { offlineBanner } = this.elements;
    if (offlineBanner) {
      offlineBanner.classList.toggle('hidden', !isOffline);
    }
  },

  retryLastQuery() {
    if (!this.state.lastQuery || this.state.status === 'streaming') return;
    this.submitQueryDirectly(this.state.lastQuery);
  },

  cacheElements() {
    this.elements = {
      widget: document.getElementById('rag-chatbot-widget'),
      triggerBtn: document.getElementById('rag-trigger-btn'),
      triggerCallout: document.getElementById('rag-trigger-callout'),
      calloutDismissBtn: document.getElementById('rag-callout-dismiss'),
      onboardModal: document.getElementById('rag-onboard-modal'),
      onboardBackdrop: document.getElementById('rag-onboard-backdrop'),
      onboardCloseBtn: document.getElementById('rag-onboard-close'),
      onboardStartBtn: document.getElementById('rag-onboard-start-btn'),
      onboardExploreBtn: document.getElementById('rag-onboard-explore-btn'),
      scopeToggleBtn: document.getElementById('rag-scope-accordion-toggle'),
      scopeContent: document.getElementById('rag-scope-accordion-content'),
      bgIframe: document.getElementById('rag-bg-iframe'),
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
      sheetBackdrop: document.getElementById('rag-sheet-backdrop'),
      sheetDragHandle: document.querySelector('.rag-sheet-drag-handle'),
      guideAckBtn: document.getElementById('rag-guide-ack-btn'),
      offlineBanner: document.getElementById('rag-offline-banner'),
      chipsContainer: document.getElementById('rag-chips-container'),
      chipsThumb: document.getElementById('rag-chips-thumb')
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
      triggerBtn, triggerCallout, calloutDismissBtn,
      onboardCloseBtn, onboardBackdrop, onboardStartBtn, onboardExploreBtn,
      closeBtn, expandBtn, resetBtn, overlay, 
      settingsBtn, settingsPanel, chatForm, userInput, sendBtn, 
      closeCitationBtn, chatMessages, sheetBackdrop 
    } = this.elements;

    if (onboardStartBtn) {
      onboardStartBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.dismissOnboarding(true);
      });
    }

    if (onboardExploreBtn) {
      onboardExploreBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.dismissOnboarding(false);
      });
    }

    if (onboardCloseBtn) {
      onboardCloseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.dismissOnboarding(false);
      });
    }

    if (onboardBackdrop) {
      onboardBackdrop.addEventListener('click', (e) => {
        e.stopPropagation();
        this.dismissOnboarding(false);
      });
    }

    const { scopeToggleBtn, scopeContent } = this.elements;
    if (scopeToggleBtn && scopeContent) {
      scopeToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isExpanded = scopeContent.classList.contains('expanded');
        scopeContent.classList.toggle('expanded', !isExpanded);
        scopeToggleBtn.setAttribute('aria-expanded', String(!isExpanded));
      });
    }

    if (triggerBtn) triggerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleModal();
    });

    if (calloutDismissBtn) {
      calloutDismissBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.calloutDismissed = true;
        if (triggerCallout) {
          triggerCallout.classList.add('hidden');
        }
      });
    }

    if (closeBtn) closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleModal(false);
    });
    if (overlay) overlay.addEventListener('click', (e) => {
      e.stopPropagation();
      const isCitationOpen = this.elements.sideCitationPanel && !this.elements.sideCitationPanel.classList.contains('hidden');
      if (isCitationOpen) {
        this.toggleCitationPanel(false);
      } else {
        this.toggleModal(false);
      }
    });
    if (expandBtn) expandBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleExpand();
    });

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
        if (settingsPanel) settingsPanel.classList.add('hidden');
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
      closeCitationBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleCitationPanel(false);
      });
    }

    if (sheetBackdrop) {
      sheetBackdrop.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleCitationPanel(false);
      });
    }

    // Single Entry Handler for Send / Stop Button
    if (sendBtn) {
      sendBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.handleActionClick();
      });
    }

    if (chatForm) {
      chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        e.stopPropagation();
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

    if (guideCloseBtn) guideCloseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeGuideModal();
    });
    if (guideBackdrop) guideBackdrop.addEventListener('click', (e) => {
      e.stopPropagation();
      closeGuideModal();
    });
    if (this.elements.guideAckBtn) this.elements.guideAckBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeGuideModal();
    });
    if (headerGuideBtn) headerGuideBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleGuideModal();
    });

    // Universal outside-click dismiss for main modal window (Hardened against detached node bubbling)
    document.addEventListener('click', (e) => {
      const { modal, triggerBtn } = this.elements;
      if (!modal || modal.classList.contains('hidden') || !modal.classList.contains('rag-modal-open')) return;

      // 1. If click originated inside modal, do not dismiss
      const path = e.composedPath ? e.composedPath() : [];
      if (path.includes(modal) || modal.contains(e.target)) return;

      // 2. If click was on trigger button or callout, ignore here (handled by their own listener)
      if (triggerBtn && (path.includes(triggerBtn) || triggerBtn.contains(e.target))) return;
      const { triggerCallout } = this.elements;
      if (triggerCallout && (path.includes(triggerCallout) || triggerCallout.contains(e.target))) return;

      // 3. If element was detached from the DOM during event dispatch (e.g. innerHTML swaps or welcome card removal), ignore
      if (e.target && !document.body.contains(e.target)) return;

      // 4. Don't close main modal if guide dialog is active or clicked
      if (guideModal && guideModal.classList.contains('active')) return;
      if (e.target.closest && e.target.closest('#rag-guide-modal')) return;

      // Valid outside click: dismiss modal
      this.toggleModal(false);
    });

    // Hierarchical keyboard Escape handler
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (this.elements.onboardModal && !this.elements.onboardModal.classList.contains('hidden')) {
          this.dismissOnboarding(false);
        } else if (guideModal && guideModal.classList.contains('active')) {
          closeGuideModal();
        } else if (resetConfirmPopover && !resetConfirmPopover.classList.contains('hidden')) {
          hideResetConfirm();
        } else if (settingsPanel && !settingsPanel.classList.contains('hidden')) {
          settingsPanel.classList.add('hidden');
        } else if (this.elements.sideCitationPanel && !this.elements.sideCitationPanel.classList.contains('hidden')) {
          this.toggleCitationPanel(false);
        } else if (this.elements.modal && !this.elements.modal.classList.contains('hidden') && this.elements.modal.classList.contains('rag-modal-open')) {
          this.toggleModal(false);
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

        // 3. Inline Citation Click ([1], [2], etc.) - Scoped to containing message
        const inlineCitationBtn = e.target.closest('.rag-inline-citation');
        if (inlineCitationBtn) {
          const citIdx = inlineCitationBtn.getAttribute('data-cit-idx');
          let msgId = inlineCitationBtn.getAttribute('data-msg-id');

          const botMsg = inlineCitationBtn.closest('.rag-bot-msg');
          const msgWrapper = inlineCitationBtn.closest('.rag-msg-wrapper');
          if (!msgId) {
            msgId = (botMsg && botMsg.dataset.msgId) || 
                    (msgWrapper && msgWrapper.dataset.msgId) || 
                    null;
          }

          let targetSources = null;
          // Priority 1: Direct lookup by data-msg-id in messageSourcesMap
          if (msgId && this.state.messageSourcesMap && this.state.messageSourcesMap.has(msgId)) {
            targetSources = this.state.messageSourcesMap.get(msgId);
          }

          // Priority 2: DOM traversal to parent message bubble or wrapper
          if (!targetSources || targetSources.length === 0) {
            targetSources = (botMsg && botMsg._ragSources) || 
                            (msgWrapper && msgWrapper._ragSources);

            if ((!targetSources || targetSources.length === 0) && msgWrapper && msgWrapper.dataset.msgId) {
              targetSources = this.state.messageSourcesMap && this.state.messageSourcesMap.get(msgWrapper.dataset.msgId);
              if (!msgId) msgId = msgWrapper.dataset.msgId;
            }
          }

          // Fallback: activeCitations (for single query context)
          if (!targetSources || targetSources.length === 0) {
            targetSources = this.state.activeCitations;
          }

          if (citIdx) {
            this.handleInlineCitationClick(citIdx, targetSources, msgId);
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

      // Capturing scroll listener for horizontal chips track indicator
      chatMessages.addEventListener('scroll', (e) => {
        if (e.target && (e.target.id === 'rag-chips-container' || e.target.classList.contains('rag-chips-horizontal'))) {
          this.updateChipsIndicator();
        }
      }, { capture: true, passive: true });

      // Interactive Pointer/Touch Drag & Click on Chips Slider Track
      const trackWrapper = document.getElementById('rag-chips-track-wrapper');
      const track = document.querySelector('.rag-chips-track');
      if (trackWrapper && track) {
        let isDraggingTrack = false;

        const handleTrackScroll = (clientX, smooth = false) => {
          const container = document.getElementById('rag-chips-container') || document.querySelector('.rag-chips-horizontal');
          if (!container) return;
          const rect = track.getBoundingClientRect();
          if (rect.width <= 0) return;
          const offsetX = Math.max(0, Math.min(rect.width, clientX - rect.left));
          const progress = offsetX / rect.width;
          const maxScroll = container.scrollWidth - container.clientWidth;
          if (maxScroll > 0) {
            container.scrollTo({
              left: progress * maxScroll,
              behavior: smooth ? 'smooth' : 'auto'
            });
          }
        };

        trackWrapper.addEventListener('pointerdown', (e) => {
          isDraggingTrack = true;
          track.classList.add('rag-dragging');
          trackWrapper.setPointerCapture(e.pointerId);
          handleTrackScroll(e.clientX, false);
        });

        trackWrapper.addEventListener('pointermove', (e) => {
          if (isDraggingTrack) {
            handleTrackScroll(e.clientX, false);
          }
        });

        const stopDragging = (e) => {
          if (isDraggingTrack) {
            isDraggingTrack = false;
            track.classList.remove('rag-dragging');
            try {
              trackWrapper.releasePointerCapture(e.pointerId);
            } catch (err) {}
          }
        };

        trackWrapper.addEventListener('pointerup', stopDragging);
        trackWrapper.addEventListener('pointercancel', stopDragging);
      }
    }
  },

  updateChipsIndicator() {
    const container = document.getElementById('rag-chips-container') || document.querySelector('.rag-chips-horizontal');
    const thumb = document.getElementById('rag-chips-thumb');
    if (!container || !thumb) return;
    const maxScroll = container.scrollWidth - container.clientWidth;
    if (maxScroll > 2) {
      const track = thumb.parentElement;
      const trackWidth = track ? track.clientWidth : 46;
      const thumbWidth = thumb.clientWidth || 16;
      const maxThumbMove = Math.max(0, trackWidth - thumbWidth);
      const progress = Math.max(0, Math.min(1, container.scrollLeft / maxScroll));
      thumb.style.transform = `translate3d(${progress * maxThumbMove}px, 0, 0)`;
      thumb.style.webkitTransform = `translate3d(${progress * maxThumbMove}px, 0, 0)`;
    }
  },

  toggleModal(forceState) {
    const { modal, overlay, userInput, triggerBtn, triggerCallout } = this.elements;
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
      if (triggerCallout) triggerCallout.classList.add('hidden');
      void modal.offsetWidth; // Force reflow for smooth transition
      modal.classList.add('rag-modal-open');
      const isTouchOrMobile = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (window.innerWidth <= 768);
      if (userInput && !isTouchOrMobile) {
        userInput.focus();
      }
    } else {
      modal.classList.remove('rag-modal-open');
      if (overlay) {
        overlay.classList.remove('active');
        overlay.classList.remove('rag-overlay-expanded');
      }
      if (triggerBtn) triggerBtn.classList.remove('rag-trigger-hidden');
      if (triggerCallout && !this.calloutDismissed) triggerCallout.classList.remove('hidden');
      
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
    this.state.activeCitations = [];
    this.state.displayedMsgId = null;
    if (this.elements.sideCitationPanel) {
      delete this.elements.sideCitationPanel.dataset.activeMsgId;
    }
    if (this.state.messageSourcesMap) {
      this.state.messageSourcesMap.clear();
    }
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

    this.state.lastQuery = query;
    this.state.isTimedOut = false;

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
    let renderRafId = null;
    let timeoutId = null;
    let fetchSignal;

    // Timeout guard: 45s maximum duration (Context7 MDN Web Docs best practice)
    if (typeof AbortSignal.timeout === 'function' && typeof AbortSignal.any === 'function') {
      try {
        const timeoutSignal = AbortSignal.timeout(45000);
        fetchSignal = AbortSignal.any([this.state.abortController.signal, timeoutSignal]);
      } catch (e) {
        fetchSignal = this.state.abortController.signal;
      }
    } else {
      fetchSignal = this.state.abortController.signal;
      timeoutId = setTimeout(() => {
        this.state.isTimedOut = true;
        if (this.state.abortController) {
          this.state.abortController.abort();
        }
      }, 45000);
    }

    const flushRender = () => {
      const { chatMessages } = this.elements;
      // 1. Read phase BEFORE DOM mutation (Google web.dev: avoid forced synchronous layout)
      const wasNearBottom = chatMessages 
        ? (chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight) < 120
        : true;

      // 2. DOM write phase
      if (isFirstToken && fullAnswer.length > 0) {
        isFirstToken = false;
        botBubbleObj.contentElem.innerHTML = '';
      }
      if (fullAnswer.length > 0) {
        let html = window.marked 
          ? window.marked.parse(fullAnswer) 
          : this.escapeHtml(fullAnswer);
        const msgIdAttr = (botBubbleObj && botBubbleObj.msgId) ? ` data-msg-id="${botBubbleObj.msgId}"` : '';
        html = html.replace(/\[(\d+)\]/g, `<button type="button" class="rag-inline-citation" data-cit-idx="$1"${msgIdAttr} title="Lihat Sumber Rujukan [$1]">[$1]</button>`);
        botBubbleObj.contentElem.innerHTML = html;
      }
      
      // 3. Batched scroll write phase
      if (chatMessages && (wasNearBottom || isFirstToken)) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    };

    const scheduleRender = () => {
      if (!renderRafId) {
        renderRafId = requestAnimationFrame(() => {
          renderRafId = null;
          flushRender();
        });
      }
    };

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: fetchSignal,
        body: JSON.stringify({
          query: query,
          config: this.state.currentConfig,
          model: this.state.currentModel,
          chat_history: (this.state.chatHistory || []).slice(-10)
        })
      });

      if (!response.ok) {
        let errMessage = `HTTP error! status: ${response.status}`;
        try {
          const errJson = await response.json();
          if (errJson && errJson.detail) {
            errMessage = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
          }
        } catch (e) {
          // ignore
        }
        const err = new Error(errMessage);
        err.status = response.status;
        throw err;
      }

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
            if (parsed.type === 'thinking') {
              if (isFirstToken && botBubbleObj.statusElem) {
                botBubbleObj.statusElem.textContent = parsed.content || 'Mencari rujukan akademik...';
              }
            } else if (parsed.type === 'token') {
              fullAnswer += parsed.content;
              scheduleRender();
            } else if (parsed.type === 'citations') {
              citations = parsed.sources || [];
              if (citations.length > 0 && botBubbleObj && botBubbleObj.msgId) {
                this.state.messageSourcesMap.set(botBubbleObj.msgId, citations);
                if (botBubbleObj.wrapperElem) botBubbleObj.wrapperElem._ragSources = citations;
                if (botBubbleObj.bubbleElem) botBubbleObj.bubbleElem._ragSources = citations;
              }
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
          } else if (parsed.type === 'citations') {
            citations = parsed.sources || [];
            if (citations.length > 0 && botBubbleObj && botBubbleObj.msgId) {
              this.state.messageSourcesMap.set(botBubbleObj.msgId, citations);
              if (botBubbleObj.wrapperElem) botBubbleObj.wrapperElem._ragSources = citations;
              if (botBubbleObj.bubbleElem) botBubbleObj.bubbleElem._ragSources = citations;
            }
          }
        } catch (e) {
          // ignore
        }
      }

      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }

      // Final synchronous flush to ensure 100% of tokens are rendered
      if (renderRafId) {
        cancelAnimationFrame(renderRafId);
        renderRafId = null;
      }
      flushRender();

      if (citations.length > 0) {
        if (botBubbleObj && botBubbleObj.msgId) {
          this.state.messageSourcesMap.set(botBubbleObj.msgId, citations);
          if (botBubbleObj.wrapperElem) botBubbleObj.wrapperElem._ragSources = citations;
          if (botBubbleObj.bubbleElem) botBubbleObj.bubbleElem._ragSources = citations;
        }
        this.renderCitations(botBubbleObj.bubbleElem, citations, botBubbleObj.msgId);
      }

      this.state.chatHistory.push({ role: 'user', content: query });
      this.state.chatHistory.push({ role: 'assistant', content: fullAnswer });

    } catch (error) {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
      if (renderRafId) {
        cancelAnimationFrame(renderRafId);
        renderRafId = null;
      }

      const isAbortByUser = error.name === 'AbortError' && !this.state.isTimedOut;
      const isTimeout = error.name === 'TimeoutError' || this.state.isTimedOut || error.message.includes('504') || error.message.includes('timeout');
      const isRateLimit = error.status === 429 || error.message.includes('429') || error.message.toLowerCase().includes('rate limit') || error.message.toLowerCase().includes('terlalu banyak');
      const isValidationError = error.status === 422 || error.message.includes('422') || error.message.toLowerCase().includes('1000') || error.message.toLowerCase().includes('karakter');
      const isOffline = (typeof navigator !== 'undefined' && !navigator.onLine) || error.message.includes('Failed to fetch') || error.message.includes('NetworkError');

      if (isAbortByUser) {
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '<span style="color: var(--rag-warning); font-size: 12px; font-style: italic;">Pencarian dihentikan sebelum ada jawaban.</span>';
        } else {
          flushRender();
          const warningBadge = document.createElement('div');
          warningBadge.className = 'rag-abort-badge';
          warningBadge.innerHTML = `${RAG_ICONS.alertCircle}<span>Pencarian dihentikan oleh pengguna. Informasi di atas mungkin tidak lengkap.</span>`;
          botBubbleObj.bubbleElem.appendChild(warningBadge);
        }
      } else if (isRateLimit) {
        if (!isFirstToken) flushRender();
        const errCard = document.createElement('div');
        errCard.className = 'rag-error-card rag-error-ratelimit';
        errCard.innerHTML = `
          <div class="rag-error-header">
            ${RAG_ICONS.alertCircle}
            <span>Batas Permintaan Tercapai</span>
          </div>
          <p>Anda telah mencapai batas pengiriman pertanyaan (maksimal 5 pesan/menit). Mohon tunggu beberapa saat sebelum mengirim pertanyaan berikutnya.</p>
          <button type="button" class="rag-retry-btn" onclick="RagChatWidget.retryLastQuery()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            <span>Kirim Ulang</span>
          </button>
        `;
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '';
          botBubbleObj.contentElem.appendChild(errCard);
        } else {
          botBubbleObj.bubbleElem.appendChild(errCard);
        }
      } else if (isValidationError) {
        if (!isFirstToken) flushRender();
        const errCard = document.createElement('div');
        errCard.className = 'rag-error-card rag-error-validation';
        const isCharLimit = error.message.toLowerCase().includes('1000') || error.message.toLowerCase().includes('karakter') || error.message.toLowerCase().includes('query');
        const errorTitle = isCharLimit ? 'Pertanyaan Terlalu Panjang' : 'Format Pertanyaan Tidak Sesuai';
        const errorDesc = isCharLimit 
          ? 'Pertanyaan melebihi batas maksimal 1.000 karakter. Mohon perpendek pertanyaan agar asisten akademik dapat menganalisis secara optimal.'
          : (error.message && !error.message.includes('422') ? error.message : 'Parameter pertanyaan tidak sesuai dengan format yang diizinkan. Silakan muat ulang atau coba lagi.');

        errCard.innerHTML = `
          <div class="rag-error-header">
            ${RAG_ICONS.alertCircle}
            <span>${this.escapeHtml(errorTitle)}</span>
          </div>
          <p>${this.escapeHtml(errorDesc)}</p>
        `;
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '';
          botBubbleObj.contentElem.appendChild(errCard);
        } else {
          botBubbleObj.bubbleElem.appendChild(errCard);
        }
      } else if (isTimeout) {
        if (!isFirstToken) flushRender();
        const errCard = document.createElement('div');
        errCard.className = 'rag-error-card rag-error-timeout';
        errCard.innerHTML = `
          <div class="rag-error-header">
            ${RAG_ICONS.alertCircle}
            <span>Waktu Permintaan Habis (Request Timeout)</span>
          </div>
          <p>Asisten membutuhkan waktu lebih dari 45 detik untuk merespons karena beban server atau antrean model AI. Pertanyaan Anda tersimpan.</p>
          <button type="button" class="rag-retry-btn" onclick="RagChatWidget.retryLastQuery()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            <span>Kirim Ulang</span>
          </button>
        `;
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '';
          botBubbleObj.contentElem.appendChild(errCard);
        } else {
          botBubbleObj.bubbleElem.appendChild(errCard);
        }
      } else if (isOffline) {
        if (!isFirstToken) flushRender();
        const errCard = document.createElement('div');
        errCard.className = 'rag-error-card rag-error-offline';
        errCard.innerHTML = `
          <div class="rag-error-header">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/><path d="M10.71 5.05A16 16 0 0 1 22.58 9"/><path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
            <span>Koneksi Internet Terputus</span>
          </div>
          <p>Tidak dapat terhubung ke server Portal INSPIRE. Pastikan koneksi internet aktif, lalu coba lagi.</p>
          <button type="button" class="rag-retry-btn" onclick="RagChatWidget.retryLastQuery()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            <span>Coba Lagi</span>
          </button>
        `;
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '';
          botBubbleObj.contentElem.appendChild(errCard);
        } else {
          botBubbleObj.bubbleElem.appendChild(errCard);
        }
      } else {
        if (!isFirstToken) flushRender();
        const errCard = document.createElement('div');
        errCard.className = 'rag-error-card';
        errCard.innerHTML = `
          <div class="rag-error-header">
            ${RAG_ICONS.alertCircle}
            <span>Layanan Mengalami Kendala</span>
          </div>
          <p>Terjadi kendala teknis saat memproses respons (${RagChatWidget.escapeHtml(error.message)}). Silakan coba sesaat lagi.</p>
          <button type="button" class="rag-retry-btn" onclick="RagChatWidget.retryLastQuery()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            <span>Coba Lagi</span>
          </button>
        `;
        if (isFirstToken) {
          botBubbleObj.contentElem.innerHTML = '';
          botBubbleObj.contentElem.appendChild(errCard);
        } else {
          botBubbleObj.bubbleElem.appendChild(errCard);
        }
      }
    } finally {
      this.state.status = 'idle';
      this.updateSendButtonState(false);
      this.scrollToBottom();
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
        <span class="rag-meta-sender">Anda</span>
        <span class="rag-meta-dot">•</span>
        <span class="rag-meta-time">${this.getTimestamp()}</span>
      </div>
      <div class="rag-user-msg">${this.escapeHtml(text)}</div>
    `;
    chatMessages.appendChild(wrapper);
  },

  renderBotBubblePlaceholder() {
    const { chatMessages } = this.elements;
    const msgId = `rag-msg-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
    const wrapper = document.createElement('div');
    wrapper.className = 'rag-msg-wrapper rag-msg-bot-wrapper';
    wrapper.dataset.msgId = msgId;
    wrapper.innerHTML = `
      <div class="rag-msg-meta-header">
        <span class="rag-meta-sender">Asisten Akademik</span>
        <span class="rag-meta-dot">•</span>
        <span class="rag-meta-time">${this.getTimestamp()}</span>
      </div>
      <div class="rag-bot-msg" data-msg-id="${msgId}">
        <div class="rag-msg-content">
          <div class="rag-typing-dots">
            <div class="rag-dot-group">
              <span class="rag-dot"></span>
              <span class="rag-dot"></span>
              <span class="rag-dot"></span>
            </div>
            <span class="rag-typing-text">Mencari rujukan akademik...</span>
          </div>
        </div>
      </div>
    `;
    chatMessages.appendChild(wrapper);
    return {
      msgId: msgId,
      wrapperElem: wrapper,
      bubbleElem: wrapper.querySelector('.rag-bot-msg'),
      contentElem: wrapper.querySelector('.rag-msg-content'),
      statusElem: wrapper.querySelector('.rag-typing-text')
    };
  },

  renderCitations(containerElem, sources, msgId = null) {
    if (!containerElem || !sources || sources.length === 0) return;
    // CRITICAL FIX: DO NOT mutate this.state.activeCitations here!
    // renderCitations() is called when a chat response finishes streaming.
    // Overwriting activeCitations here causes a desync bug if a citation panel
    // from a previous message is still open in the DOM.
    if (msgId) {
      this.state.messageSourcesMap.set(msgId, sources);
    }
    containerElem._ragSources = sources;
    const msgWrapper = containerElem.closest('.rag-msg-wrapper');
    if (msgWrapper) {
      msgWrapper._ragSources = sources;
      if (msgId && !msgWrapper.dataset.msgId) {
        msgWrapper.dataset.msgId = msgId;
      }
    }

    const citDiv = document.createElement('div');
    citDiv.className = 'rag-citations-container';
    if (msgId) {
      citDiv.dataset.msgId = msgId;
    }
    citDiv.innerHTML = `
      <div class="rag-citation-box">
        <button type="button" class="rag-citation-header" ${msgId ? `data-msg-id="${msgId}"` : ''}>
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
        const { sideCitationPanel } = this.elements;
        const isPanelOpen = sideCitationPanel && 
          !sideCitationPanel.classList.contains('hidden') && 
          (sideCitationPanel.classList.contains('rag-sheet-open') || window.innerWidth > 768);
        
        const isCurrentlyDisplayed = isPanelOpen && (
          (msgId && this.state.displayedMsgId === msgId) ||
          (!msgId && this.state.activeCitations === sources)
        );

        if (isCurrentlyDisplayed) {
          this.toggleCitationPanel(false);
          return;
        }

        const isMobile = window.innerWidth <= 768;
        if (!isMobile && this.state.mode === 'compact') {
          this.toggleExpand(true);
        }
        this.openSideCitationPanel(sources, msgId);
      });
    }
  },

  openSideCitationPanel(sources, msgId = null) {
    const { sideCitationPanel, sideCitationBody, sheetBackdrop } = this.elements;
    if (!sideCitationPanel || !sideCitationBody || !sources) return;

    this.state.activeCitations = sources;
    this.state.displayedMsgId = msgId || (sources && sources[0] && sources[0]._msgId) || null;
    if (this.state.displayedMsgId) {
      sideCitationPanel.dataset.activeMsgId = this.state.displayedMsgId;
    } else {
      delete sideCitationPanel.dataset.activeMsgId;
    }

    sideCitationBody.innerHTML = sources.map((src, index) => {
      const rawTitle = src.title || "Peraturan Rektor UNSRAT";
      const title = rawTitle.replace(/\s+/g, ' ').trim();
      const docId = src.doc_id ? `${src.doc_id}` : "";
      
      // Clean and normalize metadata strings
      const rawBab = (src.bab || "").replace(/\s+/g, ' ').trim();
      const rawBagian = (src.bagian || "").replace(/\s+/g, ' ').trim();
      let rawPasal = (src.pasal || "").replace(/\s+/g, ' ').trim();
      if (rawPasal && !rawPasal.toLowerCase().startsWith('pasal')) {
        rawPasal = `Pasal ${rawPasal}`;
      }

      const idx = src.index || (index + 1);

      // Build natural fluid inline breadcrumb (fills horizontal width naturally without rigid blocks)
      const pathChunks = [];
      if (rawBab) pathChunks.push(`<span class="rag-path-segment rag-path-bab">${this.escapeHtml(rawBab)}</span>`);
      if (rawBagian) pathChunks.push(`<span class="rag-path-segment rag-path-bagian">${this.escapeHtml(rawBagian)}</span>`);
      if (rawPasal) pathChunks.push(`<span class="rag-path-segment rag-path-pasal-pill">${this.escapeHtml(rawPasal)}</span>`);

      const pathHTML = pathChunks.length > 0 
        ? `<div class="rag-editorial-path">${pathChunks.join('<span class="rag-path-sep">/</span>')}</div>`
        : '';

      return `
        <div class="rag-citation-editorial-item" id="rag-cit-item-${idx}" data-idx="${idx}">
          <div class="rag-editorial-header">
            <div class="rag-editorial-meta-left">
              <span class="rag-citation-idx-badge">[${this.escapeHtml(idx)}]</span>
              <h5 class="rag-editorial-title">${this.escapeHtml(title)}</h5>
            </div>
            ${docId ? `<span class="rag-editorial-docid">${this.escapeHtml(docId)}</span>` : ''}
          </div>
          ${pathHTML}
          <div class="rag-editorial-passage">${this.escapeHtml(src.content)}</div>
        </div>
      `;
    }).join('');

    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      sideCitationPanel.style.removeProperty('height');
      sideCitationPanel.style.removeProperty('transform');
      sideCitationPanel.style.removeProperty('transition');
      sideCitationPanel.classList.remove('rag-sheet-expanded');
      sideCitationPanel.classList.remove('hidden');
      void sideCitationPanel.offsetHeight;
      requestAnimationFrame(() => {
        sideCitationPanel.classList.add('rag-sheet-open');
      });
      if (sheetBackdrop) {
        sheetBackdrop.style.removeProperty('opacity');
        sheetBackdrop.style.removeProperty('transition');
        sheetBackdrop.classList.remove('hidden');
        void sheetBackdrop.offsetHeight;
        requestAnimationFrame(() => {
          sheetBackdrop.classList.add('active');
        });
      }
      if (this.elements.overlay) {
        this.elements.overlay.style.removeProperty('background-color');
        this.elements.overlay.style.removeProperty('transition');
        this.elements.overlay.classList.add('rag-citations-active');
      }
    } else {
      sideCitationPanel.classList.remove('hidden');
    }
  },

  handleInlineCitationClick(citIdx, sources = null, msgId = null) {
    const targetSources = sources || (msgId && this.state.messageSourcesMap.get(msgId)) || this.state.activeCitations;
    if (!targetSources || targetSources.length === 0) return;

    const isMobile = window.innerWidth <= 768;
    const wasCompact = !isMobile && (this.state.mode === 'compact');
    if (wasCompact) {
      this.toggleExpand(true);
    }

    const { sideCitationPanel, sideCitationBody } = this.elements;
    const isPanelCurrentlyOpen = sideCitationPanel && 
      !sideCitationPanel.classList.contains('hidden') &&
      (isMobile ? sideCitationPanel.classList.contains('rag-sheet-open') : true);

    // Strict state comparison: must match both active open panel AND message ID
    const isAlreadyDisplayingSameSources = isPanelCurrentlyOpen && (
      (msgId && this.state.displayedMsgId === msgId) ||
      (!msgId && this.state.activeCitations === targetSources)
    );

    if (!isAlreadyDisplayingSameSources) {
      this.openSideCitationPanel(targetSources, msgId);
    }

    // Cancel any previous pending highlight/scroll timers to prevent animation clashes
    if (this._citationHighlightTimer) {
      clearTimeout(this._citationHighlightTimer);
      this._citationHighlightTimer = null;
    }
    if (this._citationScrollTimer) {
      clearTimeout(this._citationScrollTimer);
      this._citationScrollTimer = null;
    }

    const executeScrollAndNudge = () => {
      const { sideCitationBody } = this.elements;
      if (!sideCitationBody) return;

      // Defensive matching: exact data-idx, or fallback to first available citation item
      let targetItem = sideCitationBody.querySelector(`[data-idx="${citIdx}"]`);
      if (!targetItem) {
        targetItem = sideCitationBody.querySelector('.rag-citation-editorial-item');
      }
      if (!targetItem) return;

      // Remove existing highlighted items across panel
      sideCitationBody.querySelectorAll('.rag-citation-highlighted').forEach(el => {
        el.classList.remove('rag-citation-highlighted');
      });

      const triggerNudge = () => {
        targetItem.classList.remove('rag-citation-highlighted');
        void targetItem.offsetWidth; // Force layout reflow for animation restart
        targetItem.classList.add('rag-citation-highlighted');
      };

      // For citation [1], ALWAYS scroll smoothly to the very top (scrollTop: 0)
      // For citation [N], compute exact offset position relative to scroll container
      const isFirstCitation = (String(citIdx).trim() === '1');
      let targetScrollTop = 0;
      if (!isFirstCitation) {
        const containerRect = sideCitationBody.getBoundingClientRect();
        const itemRect = targetItem.getBoundingClientRect();
        targetScrollTop = Math.max(0, (itemRect.top - containerRect.top) + sideCitationBody.scrollTop - 12);
      }

      const currentScroll = sideCitationBody.scrollTop;
      const isAlreadyAtTarget = Math.abs(currentScroll - targetScrollTop) <= 4;

      if (isAlreadyAtTarget) {
        // Already at target position: trigger tactile nudge immediately
        triggerNudge();
      } else {
        // Need to scroll: initiate smooth scroll to exact target position
        sideCitationBody.scrollTo({ top: targetScrollTop, behavior: 'smooth' });

        let scrollHandled = false;
        const onScrollEnd = () => {
          if (scrollHandled) return;
          scrollHandled = true;
          sideCitationBody.removeEventListener('scrollend', onScrollEnd);
          if (this._citationScrollTimer) {
            clearTimeout(this._citationScrollTimer);
            this._citationScrollTimer = null;
          }
          // Micro-pause (40ms) after scroll settles, then play tactile nudge animation
          setTimeout(triggerNudge, 40);
        };

        if ('onscrollend' in window) {
          sideCitationBody.addEventListener('scrollend', onScrollEnd, { once: true });
        }

        // Adaptive fallback timer in case scrollend is delayed or unsupported
        const scrollDist = Math.abs(currentScroll - targetScrollTop);
        const fallbackMs = Math.min(800, Math.max(350, Math.round(scrollDist * 0.8)));
        this._citationScrollTimer = setTimeout(onScrollEnd, fallbackMs);
      }
    };

    if (isAlreadyDisplayingSameSources && !wasCompact) {
      executeScrollAndNudge();
    } else {
      // Allow browser to complete paint and layout reflow (especially on split expand)
      const renderDelay = wasCompact ? 140 : 60;
      this._citationHighlightTimer = setTimeout(executeScrollAndNudge, renderDelay);
    }
  },

  setupSheetGesture() {
    const { sideCitationPanel, sheetBackdrop, overlay } = this.elements;
    if (!sideCitationPanel) return;

    const dragHandle = sideCitationPanel.querySelector('.rag-sheet-drag-handle');
    const header = sideCitationPanel.querySelector('.rag-side-citation-header');
    if (!dragHandle) return;

    let isDragging = false;
    let startY = 0;
    let currentDeltaY = 0;
    let startHeight = 0;
    let isExpanded = false;
    let activePointerId = null;

    const onPointerDown = (e) => {
      // Gesture only applies on mobile viewports (<= 768px)
      if (window.innerWidth > 768) return;
      if (!e.isPrimary) return;
      if (e.target.closest && e.target.closest('#rag-close-citation-btn')) return;

      isDragging = true;
      activePointerId = e.pointerId;
      startY = e.clientY;
      currentDeltaY = 0;
      isExpanded = sideCitationPanel.classList.contains('rag-sheet-expanded');
      
      const panelRect = sideCitationPanel.getBoundingClientRect();
      startHeight = panelRect.height;

      dragHandle.classList.add('rag-dragging');
      try {
        e.currentTarget.setPointerCapture(e.pointerId);
      } catch (_) {}

      // Disable transition for instantaneous 1:1 tactile drag response
      sideCitationPanel.style.setProperty('transition', 'none', 'important');
      if (sheetBackdrop) {
        sheetBackdrop.style.setProperty('transition', 'none', 'important');
      }
      if (overlay) {
        overlay.style.setProperty('transition', 'none', 'important');
      }
    };

    const onPointerMove = (e) => {
      if (!isDragging || e.pointerId !== activePointerId) return;

      const deltaY = e.clientY - startY;
      currentDeltaY = deltaY;

      // Available maximum height inside mobile viewport / modal
      const maxHeight = window.innerHeight - 54;
      const defaultHeight = window.innerHeight * 0.75;

      if (deltaY < 0) {
        // PULLING UP: User expands the drawer to read more passages!
        // We dynamically grow height from bottom: 0 so the passage container expands
        // and the header stays fixed at the top of the expanding panel.
        let targetHeight = startHeight + (-deltaY);
        if (targetHeight > maxHeight) {
          const over = targetHeight - maxHeight;
          targetHeight = maxHeight + (over * 0.18); // soft rubber-band ceiling
        }

        sideCitationPanel.style.setProperty('height', `${targetHeight}px`, 'important');
        sideCitationPanel.style.setProperty('transform', 'translateY(0)', 'important');

        if (sheetBackdrop) sheetBackdrop.style.setProperty('opacity', '1', 'important');
        if (overlay) overlay.style.setProperty('background-color', 'rgba(15, 12, 10, 0.64)', 'important');

      } else {
        // PULLING DOWN:
        if (isExpanded) {
          // If was expanded, pulling down first shrinks height towards default 75vh
          let targetHeight = startHeight - deltaY;
          if (targetHeight >= defaultHeight) {
            sideCitationPanel.style.setProperty('height', `${targetHeight}px`, 'important');
            sideCitationPanel.style.setProperty('transform', 'translateY(0)', 'important');
          } else {
            // Reached default height, now translate down towards close
            const extraTranslate = defaultHeight - targetHeight;
            sideCitationPanel.style.setProperty('height', `${defaultHeight}px`, 'important');
            sideCitationPanel.style.setProperty('transform', `translateY(${extraTranslate}px)`, 'important');

            const progress = Math.max(0, Math.min(1, 1 - (extraTranslate / 220)));
            if (sheetBackdrop) sheetBackdrop.style.setProperty('opacity', progress.toFixed(2), 'important');
            if (overlay) {
              const baseAlpha = 0.48;
              const currentAlpha = baseAlpha + (0.16 * progress);
              overlay.style.setProperty('background-color', `rgba(15, 12, 10, ${currentAlpha.toFixed(3)})`, 'important');
            }
          }
        } else {
          // In standard mode, pulling down translates panel down towards dismissal
          sideCitationPanel.style.setProperty('transform', `translateY(${deltaY}px)`, 'important');

          const progress = Math.max(0, Math.min(1, 1 - (deltaY / 240)));
          if (sheetBackdrop) sheetBackdrop.style.setProperty('opacity', progress.toFixed(2), 'important');
          if (overlay) {
            const baseAlpha = 0.48;
            const currentAlpha = baseAlpha + (0.16 * progress);
            overlay.style.setProperty('background-color', `rgba(15, 12, 10, ${currentAlpha.toFixed(3)})`, 'important');
          }
        }
      }
    };

    const onPointerEnd = (e) => {
      if (!isDragging || e.pointerId !== activePointerId) return;
      isDragging = false;
      dragHandle.classList.remove('rag-dragging');

      try {
        e.currentTarget.releasePointerCapture(e.pointerId);
      } catch (_) {}

      // Re-enable smooth spring transitions
      sideCitationPanel.style.setProperty('transition', 'transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), height 0.3s cubic-bezier(0.16, 1, 0.3, 1)', 'important');
      if (sheetBackdrop) {
        sheetBackdrop.style.removeProperty('transition');
        sheetBackdrop.style.removeProperty('opacity');
      }
      if (overlay) {
        overlay.style.removeProperty('transition');
        overlay.style.removeProperty('background-color');
      }

      if (currentDeltaY < -40) {
        // Pulled UP significantly -> Snap to Expanded Full Height!
        sideCitationPanel.classList.add('rag-sheet-expanded');
        sideCitationPanel.style.removeProperty('height');
        sideCitationPanel.style.setProperty('transform', 'translateY(0)', 'important');
      } else if (currentDeltaY > 80) {
        // Pulled DOWN significantly
        if (isExpanded && currentDeltaY < 180) {
          // If was expanded and pulled down moderately, collapse back to 75vh default mode
          sideCitationPanel.classList.remove('rag-sheet-expanded');
          sideCitationPanel.style.removeProperty('height');
          sideCitationPanel.style.setProperty('transform', 'translateY(0)', 'important');
        } else {
          // Dismiss the sheet
          sideCitationPanel.style.removeProperty('height');
          sideCitationPanel.style.removeProperty('transform');
          this.toggleCitationPanel(false);
        }
      } else {
        // Snap back to current resting mode
        sideCitationPanel.style.removeProperty('height');
        sideCitationPanel.style.setProperty('transform', 'translateY(0)', 'important');
      }

      setTimeout(() => {
        sideCitationPanel.style.removeProperty('transform');
        sideCitationPanel.style.removeProperty('transition');
      }, 320);

      currentDeltaY = 0;
      activePointerId = null;
    };

    // Attach listeners
    dragHandle.addEventListener('pointerdown', onPointerDown);
    dragHandle.addEventListener('pointermove', onPointerMove);
    dragHandle.addEventListener('pointerup', onPointerEnd);
    dragHandle.addEventListener('pointercancel', onPointerEnd);

    if (header) {
      header.addEventListener('pointerdown', onPointerDown);
      header.addEventListener('pointermove', onPointerMove);
      header.addEventListener('pointerup', onPointerEnd);
      header.addEventListener('pointercancel', onPointerEnd);
    }
  },

  toggleCitationPanel(show) {
    const { sideCitationPanel, sheetBackdrop, overlay } = this.elements;
    if (!sideCitationPanel) return;

    if (show) {
      this.openSideCitationPanel(this.state.activeCitations, this.state.displayedMsgId);
      return;
    }

    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      sideCitationPanel.style.removeProperty('height');
      sideCitationPanel.style.removeProperty('transform');
      sideCitationPanel.style.removeProperty('transition');
      sideCitationPanel.classList.remove('rag-sheet-open');
      sideCitationPanel.classList.remove('rag-sheet-expanded');
      if (overlay) {
        overlay.style.removeProperty('background-color');
        overlay.style.removeProperty('transition');
        overlay.classList.remove('rag-citations-active');
      }
      if (sheetBackdrop) {
        sheetBackdrop.style.removeProperty('opacity');
        sheetBackdrop.style.removeProperty('transition');
        sheetBackdrop.classList.remove('active');
        setTimeout(() => {
          if (!sheetBackdrop.classList.contains('active')) {
            sheetBackdrop.classList.add('hidden');
          }
        }, 320);
      }
      setTimeout(() => {
        if (!sideCitationPanel.classList.contains('rag-sheet-open')) {
          sideCitationPanel.classList.add('hidden');
        }
      }, 330);
    } else {
      sideCitationPanel.style.removeProperty('height');
      sideCitationPanel.style.removeProperty('transform');
      sideCitationPanel.style.removeProperty('transition');
      sideCitationPanel.classList.remove('rag-sheet-open');
      sideCitationPanel.classList.remove('rag-sheet-expanded');
      sideCitationPanel.classList.add('hidden');
      if (overlay) {
        overlay.classList.remove('rag-citations-active');
      }
      if (sheetBackdrop) {
        sheetBackdrop.style.removeProperty('opacity');
        sheetBackdrop.style.removeProperty('transition');
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
