// static/js/app.js — Client-Side SPA Controller

document.addEventListener("DOMContentLoaded", () => {
    // Pembungkus aman untuk inisialisasi ikon Lucide
    function safeCreateIcons() {
        try {
            if (typeof lucide !== "undefined" && lucide.createIcons) {
                lucide.createIcons();
            } else {
                console.warn("[RAG Client] Lucide library is not globally available.");
            }
        } catch (e) {
            console.error("[RAG Client] Failed to create Lucide icons:", e);
        }
    }

    safeCreateIcons();

    // ── STATE MANAGEMENT ───────────────────────────────────────────────────────
    let chatHistory = [];
    let isStreaming = false;
    let abortController = null;
    let metricsChartInstance = null;

    // Element Selectors
    const tabChatBtn = document.getElementById("tab-chat-btn");
    const tabEvalBtn = document.getElementById("tab-eval-btn");
    const tabChat    = document.getElementById("tab-chat");
    const tabEval    = document.getElementById("tab-eval");
    const modelSelect = document.getElementById("model-select");
    const configSelect = document.getElementById("config-select");
    const badgeConfig = document.getElementById("badge-config-display");
    const resetBtn = document.getElementById("reset-btn");
    const refreshEvalBtn = document.getElementById("refresh-eval-btn");

    // Form & Input Elements
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("user-input");
    const chatMessages = document.getElementById("chat-messages");
    const sendBtn = document.getElementById("send-btn");
    const btnIcon = document.getElementById("btn-icon");
    const statusInfo = document.getElementById("status-info");

    // Ekspor Clipboard Selectors
    const btnCopyWilcoxon = document.getElementById("btn-copy-wilcoxon");
    const btnCopyAudit = document.getElementById("btn-copy-audit");
    const btnDownloadAudit = document.getElementById("btn-download-audit");

    // Metadata Panel Selectors
    const metaLastRun = document.getElementById("meta-last-run");
    const metaDatasetSize = document.getElementById("meta-dataset-size");
    const metaGenerator = document.getElementById("meta-generator-model");
    const metaEvaluator = document.getElementById("meta-evaluator-model");
    const metaEmbedding = document.getElementById("meta-embedding-model");

    // ── SPA TAB NAVIGATION (Bebas Emoji) ─────────────────────────────────────
    tabChatBtn.addEventListener("click", () => {
        tabChatBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 bg-white/15 text-white border-l-4 border-white";
        tabEvalBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 text-white/70 border-l-4 border-transparent hover:bg-white/5 hover:text-white";
        tabChat.classList.remove("hidden");
        tabEval.classList.add("hidden");
    });

    tabEvalBtn.addEventListener("click", () => {
        tabEvalBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 bg-white/15 text-white border-l-4 border-white";
        tabChatBtn.className = "w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl font-medium transition duration-200 text-white/70 border-l-4 border-transparent hover:bg-white/5 hover:text-white";
        tabEval.classList.remove("hidden");
        tabChat.classList.add("hidden");
        loadEvaluationData();
    });

    // Helper untuk mengisi kueri cepat
    window.fillInput = function(text) {
        chatInput.value = text;
        chatInput.focus();
    };

    // ── SYSTEM CONFIG INGESTION ──────────────────────────────────────────────
    async function loadSystemConfig() {
        try {
            console.log("[RAG Client] Fetching system config from /api/config");
            const res = await fetch("/api/config");
            if (!res.ok) throw new Error("Gagal mengambil konfigurasi awal");
            const data = await res.json();
            
            modelSelect.innerHTML = data.available_models.map(model => 
                `<option value="${model}" ${model === data.active_model ? 'selected' : ''} class="text-gray-800">${model}</option>`
            ).join("");
            
            configSelect.value = "b"; // default Config B
            updateConfigBadge();
        } catch (err) {
            console.error("[RAG Client] Config load failed:", err);
            statusInfo.textContent = "Error load config";
        }
    }

    function updateConfigBadge() {
        if (badgeConfig) {
            const val = configSelect.value.toUpperCase();
            badgeConfig.innerText = `Config ${val}`;
        }
    }

    configSelect.addEventListener("change", () => {
        updateConfigBadge();
        clearChatUI();
    });

    function clearChatUI() {
        chatHistory = [];
        chatMessages.innerHTML = `
            <!-- Welcome Message Panel (Automatic) -->
            <div class="flex items-start space-x-4 max-w-4xl opacity-100 transition-all duration-300">
                <div class="bg-[#7B2D2D] text-white p-3 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                    <i data-lucide="award" class="w-5 h-5"></i>
                </div>
                <div class="space-y-2 flex-1">
                    <span class="inline-block bg-[#7B2D2D]/10 border border-[#7B2D2D]/15 text-[#7B2D2D] px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">Selamat Datang</span>
                    <div class="bg-white border border-[#EBE7E1] rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-gray-700 leading-relaxed text-sm">
                        <p class="font-semibold text-gray-900 mb-1">Halo civitas akademika Universitas Sam Ratulangi!</p>
                        <p class="text-gray-600 text-xs md:text-sm">Saya adalah asisten virtual akademik resmi Anda. Silakan tanyakan hal-hal terkait Peraturan Akademik (beban SKS, cuti kuliah, KRS, DO, drop-out, yudisium), kalender akademik, visi misi universitas, sejarah, akreditasi, maupun profil institut. Konfigurasi ${configSelect.value.toUpperCase()} saat ini aktif.</p>
                        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                            <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Syarat dan batas pengambilan cuti akademik di UNSRAT?')">
                                <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                                <span class="truncate">Syarat cuti akademik?</span>
                            </button>
                            <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Visi, misi, dan tujuan resmi Universitas Sam Ratulangi.')">
                                <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                                <span class="truncate">Visi misi UNSRAT?</span>
                            </button>
                            <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Berapa beban SKS maksimum untuk mahasiswa baru semester satu?')">
                                <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                                <span class="truncate">Beban SKS semester 1?</span>
                            </button>
                            <button class="text-left p-2.5 rounded-xl border border-gray-100 hover:border-[#7B2D2D]/30 hover:bg-[#7B2D2D]/5 transition text-gray-700 font-medium flex items-center space-x-2 cursor-pointer" onclick="fillInput('Bagaimana mekanisme evaluasi putus studi atau DO mahasiswa?')">
                                <i data-lucide="help-circle" class="w-4 h-4 text-[#7B2D2D]/70 flex-shrink-0"></i>
                                <span class="truncate">Mekanisme evaluasi DO?</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        safeCreateIcons();
        console.log("[RAG Client] Conversation cleared and welcome greeting restored.");
    }

    resetBtn.addEventListener("click", clearChatUI);

    if (refreshEvalBtn) {
        refreshEvalBtn.addEventListener("click", loadEvaluationData);
    }

    // Load config on startup
    loadSystemConfig();

    // HELPER AUTO-SCROLL SMOOTH
    function scrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    // ── HELPER FUNCTIONS FOR CHAT STREAMING ───────────────────────────────────
    function getTimestamp() {
        const now = new Date();
        const hh = String(now.getHours()).padStart(2, '0');
        const mm = String(now.getMinutes()).padStart(2, '0');
        return `${hh}:${mm}`;
    }

    function escapeHtml(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    function handleAbort() {
        if (abortController) {
            abortController.abort();
            console.log("[RAG Client] Abort controller triggered.");
        }
        isStreaming = false;
    }

    function handleError(message) {
        const errorBubble = document.createElement("div");
        errorBubble.className = "flex items-start space-x-4 max-w-4xl opacity-0 translate-y-2 transition-all duration-300 w-full";
        errorBubble.innerHTML = `
            <div class="bg-red-600 text-white p-3 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                <i data-lucide="alert-circle" class="w-5 h-5"></i>
            </div>
            <div class="space-y-2 flex-1 flex flex-col items-start max-w-2xl w-full">
                <div class="flex items-center space-x-2">
                    <span class="inline-block bg-red-100 border border-red-200 text-red-700 px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">Error</span>
                    <span class="text-[10px] text-gray-400 font-medium">${getTimestamp()}</span>
                </div>
                <div class="bg-red-50 border border-red-100 rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-red-750 leading-relaxed text-sm w-full font-medium">
                    ${escapeHtml(message)}
                </div>
            </div>
        `;
        chatMessages.appendChild(errorBubble);
        safeCreateIcons();
        
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                errorBubble.classList.remove("opacity-0", "translate-y-2");
                errorBubble.classList.add("opacity-100", "translate-y-0");
            });
        });
        scrollToBottom();
    }

    function renderCitations(botMsgId, sources) {
        const citationsContainer = document.getElementById(`${botMsgId}-citations`);
        if (!citationsContainer || !sources || sources.length === 0) return;
        
        citationsContainer.classList.remove("hidden");
        
        const headerId = `accordion-header-${botMsgId}`;
        const contentId = `accordion-content-${botMsgId}`;
        const chevronId = `chevron-${botMsgId}`;
        
        citationsContainer.innerHTML = `
            <div class="border border-[#E4DFD9] rounded-xl bg-white overflow-hidden text-xs shadow-sm w-full">
                <button id="${headerId}" class="w-full flex items-center justify-between px-4 py-3 bg-[#FAF9F6] hover:bg-gray-50 border-b border-[#E4DFD9] cursor-pointer transition duration-150 font-semibold text-gray-700">
                    <div class="flex items-center space-x-2">
                        <i data-lucide="book-open" class="w-4 h-4 text-[#7B2D2D]"></i>
                        <span>Rujukan Dokumen Akademik (${sources.length} Sumber)</span>
                    </div>
                    <i data-lucide="chevron-down" id="${chevronId}" class="w-4 h-4 text-gray-400 transition-transform duration-200"></i>
                </button>
                <div id="${contentId}" class="hidden p-4 space-y-4 bg-white divide-y divide-gray-100 w-full">
                    ${sources.map((src, index) => {
                        const title = src.title || "Dokumen Akademik";
                        const docId = src.doc_id || "-";
                        const bab = src.bab ? ` | ${src.bab}` : "";
                        const pasal = src.pasal ? ` | ${src.pasal}` : "";
                        const idx = src.index || (index + 1);
                        return `
                            <div class="pt-3 first:pt-0 space-y-1.5 w-full">
                                <div class="flex flex-wrap items-center justify-between gap-1 text-[11px] text-[#7B2D2D] font-semibold w-full">
                                    <span>[${idx}] ${title}</span>
                                    <span class="bg-gray-100 border border-gray-200 text-gray-500 px-1.5 py-0.5 rounded text-[10px] font-mono">ID: ${docId}${bab}${pasal}</span>
                                </div>
                                <div class="text-[11px] text-gray-600 italic font-mono bg-gray-50 p-2.5 rounded-lg border border-gray-100 leading-relaxed break-words w-full">
                                    "${escapeHtml(src.content)}"
                                </div>
                            </div>
                        `;
                    }).join("")}
                </div>
            </div>
        `;
        
        safeCreateIcons();
        
        const headerBtn = document.getElementById(headerId);
        const contentDiv = document.getElementById(contentId);
        const chevronIcon = document.getElementById(chevronId);
        
        if (headerBtn && contentDiv && chevronIcon) {
            headerBtn.addEventListener("click", () => {
                const isHidden = contentDiv.classList.contains("hidden");
                if (isHidden) {
                    contentDiv.classList.remove("hidden");
                    chevronIcon.classList.add("rotate-180");
                } else {
                    contentDiv.classList.add("hidden");
                    chevronIcon.classList.remove("rotate-180");
                }
                scrollToBottom();
            });
        }
    }

    // ── CHAT FORM SUBMIT LISTENER ─────────────────────────────────────────────
    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            if (isStreaming) {
                handleAbort();
                return;
            }
            
            const query = chatInput.value.trim();
            if (!query) return;
            
            // Clean input
            chatInput.value = "";
            
            // Set streaming state
            isStreaming = true;
            abortController = new AbortController();
            
            // Toggle submit button to Red-600 background and Lucide 'square' icon
            if (sendBtn) {
                sendBtn.className = "bg-red-600 hover:bg-red-700 active:bg-red-800 text-white p-3 rounded-xl mr-3 shadow-md hover:shadow-lg active:scale-95 transition duration-200 flex items-center justify-center w-11 h-11 cursor-pointer";
            }
            if (btnIcon) {
                btnIcon.setAttribute("data-lucide", "square");
            }
            safeCreateIcons();
            
            // Create user bubble
            const userMsgId = `user-msg-${Date.now()}`;
            const userTimestamp = getTimestamp();
            const userBubble = document.createElement("div");
            userBubble.id = userMsgId;
            userBubble.className = "flex items-start space-x-4 max-w-4xl opacity-0 translate-y-2 transition-all duration-300 ml-auto justify-end w-full";
            userBubble.innerHTML = `
                <div class="space-y-2 flex flex-col items-end max-w-[70%]">
                    <div class="flex items-center space-x-2">
                        <span class="inline-block bg-gray-200 border border-gray-300 text-gray-700 px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">Mahasiswa</span>
                        <span class="text-[10px] text-gray-400 font-medium">${userTimestamp}</span>
                    </div>
                    <div class="bg-gradient-to-br from-[#7B2D2D] to-[#963E3E] text-white rounded-2xl rounded-tr-none px-5 py-4 shadow-sm text-sm leading-relaxed whitespace-pre-wrap">
                        ${escapeHtml(query)}
                    </div>
                </div>
                <div class="bg-white border border-gray-200 text-gray-700 p-3 rounded-xl flex-shrink-0 mt-1 shadow-sm flex items-center justify-center w-10 h-10">
                    <i data-lucide="user" class="w-5 h-5"></i>
                </div>
            `;
            chatMessages.appendChild(userBubble);
            safeCreateIcons();
            
            // Slide-up animation
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    userBubble.classList.remove("opacity-0", "translate-y-2");
                    userBubble.classList.add("opacity-100", "translate-y-0");
                });
            });
            scrollToBottom();
            
            // Append to chat history
            chatHistory.push({ role: "user", content: query });
            
            // Create bot placeholder
            const botMsgId = `bot-msg-${Date.now()}`;
            const botBubble = document.createElement("div");
            botBubble.id = botMsgId;
            botBubble.className = "flex items-start space-x-4 max-w-4xl opacity-0 translate-y-2 transition-all duration-300 w-full";
            botBubble.innerHTML = `
                <div class="bg-[#7B2D2D] text-white p-3 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                    <i data-lucide="cpu" class="w-5 h-5"></i>
                </div>
                <div class="space-y-2 flex-1 flex flex-col items-start max-w-2xl w-full">
                    <div class="flex items-center space-x-2">
                        <span class="inline-block bg-[#7B2D2D]/10 border border-[#7B2D2D]/15 text-[#7B2D2D] px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">Asisten Akademik</span>
                        <span class="text-[10px] text-gray-400 font-medium" id="${botMsgId}-time">${getTimestamp()}</span>
                    </div>
                    <div class="bg-white border border-[#EBE7E1] rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-gray-700 leading-relaxed text-sm w-full">
                        <div id="${botMsgId}-thinking" class="flex items-center space-x-3 text-[#7B2D2D]">
                            <div class="w-4 h-4 border-2 border-[#7B2D2D] border-t-transparent rounded-full animate-spin"></div>
                            <span class="text-xs font-semibold animate-pulse" id="${botMsgId}-thinking-text">Menghubungkan ke basis data peraturan akademik...</span>
                        </div>
                        <div id="${botMsgId}-content" class="parsed-markdown hidden"></div>
                    </div>
                    <div id="${botMsgId}-citations" class="w-full mt-2 hidden"></div>
                </div>
            `;
            chatMessages.appendChild(botBubble);
            safeCreateIcons();
            
            // Slide-up animation
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    botBubble.classList.remove("opacity-0", "translate-y-2");
                    botBubble.classList.add("opacity-100", "translate-y-0");
                });
            });
            scrollToBottom();
            
            // Thinking indicator interval (1.8 seconds)
            const thinkingPhases = [
                "Menghubungkan ke basis data peraturan akademik...",
                "Menganalisis dan memetakan dokumen rujukan RAG...",
                "Merumuskan jawaban formal menggunakan LLM..."
            ];
            let phaseIndex = 0;
            const thinkingTextEl = document.getElementById(`${botMsgId}-thinking-text`);
            const thinkingInterval = setInterval(() => {
                phaseIndex = (phaseIndex + 1) % thinkingPhases.length;
                if (thinkingTextEl) {
                    thinkingTextEl.textContent = thinkingPhases[phaseIndex];
                }
            }, 1800);
            
            // Watchdog timer (15 seconds)
            let watchdogTimer = setTimeout(() => {
                console.warn("[RAG Client] Watchdog timeout triggered.");
                handleError("Batas waktu koneksi habis (15 detik). Tidak ada respon dari server.");
                handleAbort();
            }, 15000);
            
            let isFirstToken = true;
            let fullResponseText = "";
            
            try {
                statusInfo.textContent = "Streaming...";
                
                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        query: query,
                        config: configSelect.value,
                        model: modelSelect.value,
                        chat_history: chatHistory
                    }),
                    signal: abortController.signal
                });
                
                if (!response.ok) {
                    throw new Error(`Server returned HTTP ${response.status}`);
                }
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let buffer = "";
                
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split("\n");
                    buffer = lines.pop(); // Keep last partial line in buffer
                    
                    for (const line of lines) {
                        const trimmed = line.trim();
                        if (!trimmed) continue;
                        if (!trimmed.startsWith("data:")) continue;
                        
                        const jsonStr = trimmed.slice(5).trim();
                        if (!jsonStr) continue;
                        
                        try {
                            const event = JSON.parse(jsonStr);
                            
                            if (event.type === "token") {
                                // On first token, clear thinking container & watchdog/thinking intervals
                                if (isFirstToken) {
                                    isFirstToken = false;
                                    clearTimeout(watchdogTimer);
                                    clearInterval(thinkingInterval);
                                    
                                    const thinkingContainer = document.getElementById(`${botMsgId}-thinking`);
                                    if (thinkingContainer) {
                                        thinkingContainer.classList.add("hidden");
                                    }
                                    const contentContainer = document.getElementById(`${botMsgId}-content`);
                                    if (contentContainer) {
                                        contentContainer.classList.remove("hidden");
                                    }
                                }
                                
                                fullResponseText += event.content || "";
                                const contentContainer = document.getElementById(`${botMsgId}-content`);
                                if (contentContainer) {
                                    if (typeof marked !== "undefined" && marked.parse) {
                                        contentContainer.innerHTML = marked.parse(fullResponseText);
                                    } else {
                                        contentContainer.innerHTML = escapeHtml(fullResponseText).replace(/\n/g, "<br>");
                                    }
                                }
                                
                                // Display dynamic timestamp
                                const timeEl = document.getElementById(`${botMsgId}-time`);
                                if (timeEl) {
                                    timeEl.textContent = getTimestamp();
                                }
                                
                                scrollToBottom();
                            } else if (event.type === "citations") {
                                if (event.sources && event.sources.length > 0) {
                                    renderCitations(botMsgId, event.sources);
                                }
                            } else if (event.type === "done") {
                                chatHistory.push({ role: "assistant", content: fullResponseText });
                                break;
                            } else if (event.type === "error") {
                                handleError(event.message || "Terjadi kesalahan pada stream server.");
                                handleAbort();
                                break;
                            }
                        } catch (e) {
                            console.error("[RAG Client] Failed to parse event JSON:", e, jsonStr);
                        }
                    }
                }
                
                // Process any leftover content in buffer
                if (buffer.trim()) {
                    const trimmed = buffer.trim();
                    if (trimmed.startsWith("data:")) {
                        const jsonStr = trimmed.slice(5).trim();
                        if (jsonStr) {
                            try {
                                const event = JSON.parse(jsonStr);
                                if (event.type === "token") {
                                    if (isFirstToken) {
                                        isFirstToken = false;
                                        clearTimeout(watchdogTimer);
                                        clearInterval(thinkingInterval);
                                        const thinkingContainer = document.getElementById(`${botMsgId}-thinking`);
                                        if (thinkingContainer) {
                                            thinkingContainer.classList.add("hidden");
                                        }
                                        const contentContainer = document.getElementById(`${botMsgId}-content`);
                                        if (contentContainer) {
                                            contentContainer.classList.remove("hidden");
                                        }
                                    }
                                    
                                    fullResponseText += event.content || "";
                                    const contentContainer = document.getElementById(`${botMsgId}-content`);
                                    if (contentContainer) {
                                        if (typeof marked !== "undefined" && marked.parse) {
                                            contentContainer.innerHTML = marked.parse(fullResponseText);
                                        } else {
                                            contentContainer.innerHTML = escapeHtml(fullResponseText).replace(/\n/g, "<br>");
                                        }
                                    }
                                    const timeEl = document.getElementById(`${botMsgId}-time`);
                                    if (timeEl) {
                                        timeEl.textContent = getTimestamp();
                                    }
                                    scrollToBottom();
                                } else if (event.type === "citations") {
                                    if (event.sources && event.sources.length > 0) {
                                        renderCitations(botMsgId, event.sources);
                                    }
                                } else if (event.type === "done") {
                                    chatHistory.push({ role: "assistant", content: fullResponseText });
                                } else if (event.type === "error") {
                                    handleError(event.message || "Terjadi kesalahan pada stream server.");
                                    handleAbort();
                                }
                            } catch (e) {
                                console.error("[RAG Client] Failed to parse remaining event JSON:", e, jsonStr);
                            }
                        }
                    }
                }
                
            } catch (err) {
                if (err.name === 'AbortError') {
                    const thinkingContainer = document.getElementById(`${botMsgId}-thinking`);
                    if (thinkingContainer) {
                        thinkingContainer.classList.add("hidden");
                    }
                    const contentContainer = document.getElementById(`${botMsgId}-content`);
                    if (contentContainer) {
                        contentContainer.classList.remove("hidden");
                        contentContainer.innerHTML = `<span class="text-amber-700 font-medium bg-amber-50 border border-amber-150 rounded-xl px-4 py-2 block text-xs">Pencarian dan pembuatan jawaban dihentikan oleh pengguna.</span>`;
                    }
                    console.log("[RAG Client] Stream request aborted by user.");
                } else {
                    console.error("[RAG Client] Stream error:", err);
                    handleError("Terjadi kegagalan komunikasi dengan server RAG.");
                }
            } finally {
                isStreaming = false;
                clearTimeout(watchdogTimer);
                clearInterval(thinkingInterval);
                
                // Restore send button background color and send icon
                if (sendBtn) {
                    sendBtn.className = "bg-[#7B2D2D] hover:bg-[#963E3E] active:bg-[#5C1F1F] text-white p-3 rounded-xl mr-3 shadow-md hover:shadow-lg active:scale-95 transition duration-200 flex items-center justify-center w-11 h-11 cursor-pointer";
                }
                if (btnIcon) {
                    btnIcon.setAttribute("data-lucide", "send");
                }
                safeCreateIcons();
                
                if (statusInfo) {
                    statusInfo.textContent = "Ready";
                }
            }
        });
    }

    // ── TAB EVALUASI - LOAD QUANTITATIVE METRICS & METADATA ──────────────────
    async function loadEvaluationData() {
        const wilcoxonTable = document.getElementById("wilcoxon-table-body");
        const auditTable = document.getElementById("audit-table-body");

        try {
            console.log("[RAG Client] Fetching evaluation data from /api/evaluation");
            const res = await fetch("/api/evaluation");
            if (!res.ok) throw new Error("Gagal mengambil data evaluasi");
            const data = await res.json();

            // A. Render Metadata Panel (Section 5.A)
            if (data.metadata) {
                metaLastRun.innerText     = data.metadata.last_run || "-";
                metaDatasetSize.innerText = data.metadata.dataset_size || "-";
                metaGenerator.innerText   = data.metadata.generator_model || "-";
                metaEvaluator.innerText   = data.metadata.evaluator_model || "-";
                metaEmbedding.innerText   = data.metadata.embedding_model || "-";
                console.log("[RAG Client] Dynamic metadata panel populated successfully.");
            }

            // B. Populasi Tabel Wilcoxon
            if (data.wilcoxon && Object.keys(data.wilcoxon).length > 0) {
                wilcoxonTable.innerHTML = Object.entries(data.wilcoxon).map(([metric, row]) => {
                    const sigBadge = row.significant
                        ? `<span class="bg-green-50 border border-green-200 text-green-700 px-2 py-0.5 rounded-full text-[9px] font-extrabold uppercase">Signifikan</span>`
                        : `<span class="bg-gray-50 border border-gray-200 text-gray-500 px-2 py-0.5 rounded-full text-[9px] font-bold">Tidak Sig.</span>`;
                    
                    const winnerStr = row.winner === "Tidak signifikan" ? "Tidak signifikan" : row.winner;

                    // Display metric key nicely (e.g. capitalizing and removing underscores)
                    const formatMetric = metric.split('_')
                        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                        .join(' ');

                    return `
                        <tr class="hover:bg-gray-50 transition duration-150 text-xs">
                            <td class="px-4 py-3 font-bold text-gray-800">${formatMetric}</td>
                            <td class="px-4 py-3 font-mono text-[10px] text-gray-500">${parseFloat(row.p_value).toFixed(5)}</td>
                            <td class="px-4 py-3">${sigBadge}</td>
                            <td class="px-4 py-3 text-right"><span class="font-extrabold text-[#7B2D2D]">${winnerStr}</span></td>
                        </tr>
                    `;
                }).join("");
            } else {
                wilcoxonTable.innerHTML = `<tr><td colspan="4" class="px-4 py-4 text-center text-gray-400">Data uji Wilcoxon tidak tersedia. Silakan jalankan evaluasi offline.</td></tr>`;
            }

            // C. Populasi Live Audit Log
            const logs = data.audit_log || [];
            if (logs.length > 0) {
                const reversedLogs = [...logs].reverse();
                auditTable.innerHTML = reversedLogs.map(row => {
                    const timestampStr = row.timestamp ? (row.timestamp.includes(" ") ? row.timestamp.split(" ")[1] : row.timestamp) : "-";
                    const configName = row.config ? row.config.toUpperCase() : "-";
                    
                    return `
                        <tr class="hover:bg-gray-50/50 transition duration-150 text-xs">
                            <td class="px-4 py-2.5 text-gray-400 font-mono text-[10px]">${timestampStr}</td>
                            <td class="px-4 py-2.5">
                                <span class="bg-[#7B2D2D]/10 text-[#7B2D2D] px-2 py-0.5 rounded text-[8px] font-extrabold border border-[#7B2D2D]/15">${configName}</span>
                            </td>
                            <td class="px-4 py-2.5 font-mono text-[9px] text-gray-400 truncate max-w-[80px]" title="${row.model_llm || ''}">${row.model_llm || '-'}</td>
                            <td class="px-4 py-2.5 font-semibold text-gray-700 truncate max-w-[150px]" title="${row.user_query || ''}">${row.user_query || ''}</td>
                            <td class="px-4 py-2.5 text-center font-mono font-bold text-gray-600">${row.chunks_retrieved_count !== null && row.chunks_retrieved_count !== undefined ? row.chunks_retrieved_count : 0}</td>
                            <td class="px-4 py-2.5 font-mono font-bold text-[#7B2D2D]">${row.best_similarity_score !== null && row.best_similarity_score !== undefined ? parseFloat(row.best_similarity_score).toFixed(4) : "0.0000"}</td>
                            <td class="px-4 py-2.5 font-mono text-amber-600 font-bold">${row.response_time_seconds !== null && row.response_time_seconds !== undefined ? parseFloat(row.response_time_seconds).toFixed(2) + "s" : "-"}</td>
                            <td class="px-4 py-2.5 text-right font-mono font-bold text-gray-800">${row.estimated_total_tokens !== null && row.estimated_total_tokens !== undefined ? row.estimated_total_tokens : 0}</td>
                        </tr>
                    `;
                }).join("");
            } else {
                auditTable.innerHTML = `<tr><td colspan="8" class="px-4 py-4 text-center text-gray-400">Belum ada transaksi terekam di logs/transaksi_chat.csv.</td></tr>`;
            }

            renderRagasChart(data.configs);
            safeCreateIcons();
        } catch (err) {
            console.error("[RAG Client] Failed to load evaluation metrics:", err);
            wilcoxonTable.innerHTML = `<tr><td colspan="4" class="px-4 py-3 text-center text-red-500">Gagal memuat metrik Wilcoxon.</td></tr>`;
            auditTable.innerHTML = `<tr><td colspan="8" class="px-4 py-3 text-center text-red-500">Gagal memuat log transaksi.</td></tr>`;
        }
    }

    function renderRagasChart(configs) {
        const ctx = document.getElementById("metricsChart");
        if (!ctx) return;

        const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"];
        const labels = ["Faithfulness", "Answer Relevancy", "Context Precision", "Context Recall"];

        const dataA = metrics.map(m => configs.a && configs.a[m] ? (configs.a[m].mean !== null && configs.a[m].mean !== undefined ? configs.a[m].mean : 0.0) : 0.0);
        const dataB = metrics.map(m => configs.b && configs.b[m] ? (configs.b[m].mean !== null && configs.b[m].mean !== undefined ? configs.b[m].mean : 0.0) : 0.0);
        const dataC = metrics.map(m => configs.c && configs.c[m] ? (configs.c[m].mean !== null && configs.c[m].mean !== undefined ? configs.c[m].mean : 0.0) : 0.0);

        if (metricsChartInstance) {
            metricsChartInstance.destroy();
        }

        metricsChartInstance = new Chart(ctx.getContext("2d"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Config A (500 char)",
                        data: dataA,
                        backgroundColor: "rgba(123, 45, 45, 0.4)",
                        borderColor: "rgb(123, 45, 45)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Config B (2000 char)",
                        data: dataB,
                        backgroundColor: "rgba(168, 69, 69, 0.9)",
                        borderColor: "rgb(168, 69, 69)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: "Config C (BM25)",
                        data: dataC,
                        backgroundColor: "rgba(156, 163, 175, 0.5)",
                        borderColor: "rgb(156, 163, 175)",
                        borderWidth: 1.5,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1.0,
                        ticks: { font: { family: "Inter", size: 10 } }
                    },
                    x: {
                        ticks: { font: { family: "Inter", size: 10, weight: 600 } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { font: { family: "Inter", size: 10, weight: 600 } }
                    }
                }
            }
        });
    }

    // ── TASK 9: JS Logic — Clipboard Copy & CSV Export ────────────────────────
    function copyTableToClipboard(tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;

        const rows = Array.from(table.querySelectorAll("tr"));
        const text = rows.map(row => {
            const cells = Array.from(row.querySelectorAll("th, td"));
            return cells.map(cell => cell.textContent.trim()).join("\t");
        }).join("\n");

        navigator.clipboard.writeText(text)
            .then(() => {
                alert("Data tabel berhasil disalin ke clipboard! Silakan paste langsung di Excel atau Word.");
            })
            .catch(err => {
                console.error("[RAG Client] Failed to copy table to clipboard:", err);
                alert("Gagal menyalin data ke clipboard.");
            });
    }

    if (btnCopyWilcoxon) {
        btnCopyWilcoxon.addEventListener("click", () => {
            copyTableToClipboard("table-wilcoxon");
        });
    }

    if (btnCopyAudit) {
        btnCopyAudit.addEventListener("click", () => {
            copyTableToClipboard("table-audit");
        });
    }

    if (btnDownloadAudit) {
        btnDownloadAudit.addEventListener("click", () => {
            fetch("/api/evaluation")
                .then(res => {
                    if (!res.ok) throw new Error("Gagal mengambil data evaluasi");
                    return res.json();
                })
                .then(data => {
                    if (data.audit_log && data.audit_log.length > 0) {
                        let csvContent = "Timestamp,Config,Model,Query,ChunksCount,BestScore,Latency,EstTokens\n";
                        const rows = data.audit_log.map(row => {
                            return `"${row.timestamp}","${row.config}","${row.model_llm}","${row.user_query ? row.user_query.replace(/"/g, '""') : ''}",${row.chunks_retrieved_count !== null ? row.chunks_retrieved_count : 0},${row.best_similarity_score !== null ? row.best_similarity_score : 0.0},${row.response_time_seconds !== null ? row.response_time_seconds : 0.0},${row.estimated_total_tokens !== null ? row.estimated_total_tokens : 0}`;
                        });
                        csvContent += rows.join("\n");

                        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
                        const url = URL.createObjectURL(blob);
                        const link = document.createElement("a");
                        link.setAttribute("href", url);
                        link.setAttribute("download", "transaksi_chat.csv");
                        link.style.visibility = "hidden";
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                    } else {
                        alert("Belum ada log transaksi untuk diunduh.");
                    }
                })
                .catch(err => {
                    console.error("[RAG Client] Failed to download CSV:", err);
                    alert("Gagal mengunduh file CSV.");
                });
        });
    }
});

