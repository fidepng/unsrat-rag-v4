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
        // loadEvaluationData(); // Akan dipanggil dinamis di tugas selanjutnya
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
            <!-- Welcome Panel (Tanpa Emoji) -->
            <div class="flex items-start space-x-4 max-w-4xl opacity-100 transition-all duration-300">
                <div class="bg-[#7B2D2D] text-white p-3 rounded-xl flex-shrink-0 mt-1 shadow-md flex items-center justify-center w-10 h-10">
                    <i data-lucide="award" class="w-5 h-5"></i>
                </div>
                <div class="space-y-2 flex-1">
                    <span class="inline-block bg-[#7B2D2D]/10 border border-[#7B2D2D]/15 text-[#7B2D2D] px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider">SYSTEM</span>
                    <div class="bg-white border border-[#EBE7E1] rounded-2xl rounded-tl-none px-5 py-4 shadow-sm text-gray-700 leading-relaxed text-sm">
                        Riwayat percakapan telah dibersihkan. Konfigurasi ${configSelect.value.toUpperCase()} aktif. Silakan ajukan pertanyaan regulasi akademik Anda.
                    </div>
                </div>
            </div>
        `;
        safeCreateIcons();
        console.log("[RAG Client] Conversation cleared.");
    }

    resetBtn.addEventListener("click", clearChatUI);

    // Load config on startup
    loadSystemConfig();

    // HELPER AUTO-SCROLL SMOOTH
    function scrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    // Catatan: Karena pengerjaan bertahap, kita tambahkan stub kosong sementara untuk chatForm submit agar tidak terjadi error
    if (chatForm) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            console.log("[RAG Client] Submit stub triggered. Full logic implemented in next task.");
        });
    }
});
