// static/js/app.js — Frontend SPA Logic
// PRD Reference: Section 11, FR-27, FR-33

// ── State ─────────────────────────────────────────────────────────────────────
let chatHistory = [];   // [{role: "user"|"assistant", content: "..."}]
let isStreaming = false;
let metricsChartInstance = null;

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
    await loadConfig();
    if (document.getElementById("tab-eval").classList.contains("active")) {
        await loadEvalData();
    }
});

async function loadConfig() {
    try {
        const res = await fetch("/api/config");
        const data = await res.json();
        const modelSelect = document.getElementById("model-select");
        modelSelect.innerHTML = data.available_models
            .map(m => `<option value="${m}">${m}</option>`)
            .join("");
        modelSelect.value = data.active_model;
    } catch (e) {
        console.error("Gagal load config:", e);
    }
}

// ── Tab Switching ─────────────────────────────────────────────────────────────
function switchTab(tab) {
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.getElementById(`tab-${tab}`).classList.add("active");
    document.getElementById(`tab-${tab}-btn`).classList.add("active");
    if (tab === "eval") loadEvalData();
}

// ── Chat Logic ────────────────────────────────────────────────────────────────
function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const query = input.value.trim();
    if (!query || isStreaming) return;

    const config = document.getElementById("config-select").value;
    const model  = document.getElementById("model-select").value;

    input.value = "";
    isStreaming  = true;
    document.getElementById("send-btn").disabled = true;
    document.getElementById("status-info").textContent = "Memproses...";

    // Tampilkan bubble user
    appendBubble("user", query);
    chatHistory.push({ role: "user", content: query });

    // Placeholder bot bubble
    const botBubbleId = `bot-${Date.now()}`;
    const thinkingId  = `thinking-${Date.now()}`;
    appendThinkingBubble(thinkingId);

    let botContent = "";
    let botBubbleCreated = false;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, config, chat_history: chatHistory, model }),
        });

        const reader   = response.body.getReader();
        const decoder  = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const text   = decoder.decode(value, { stream: true });
            const lines  = text.split("\n");

            for (const line of lines) {
                if (!line.startsWith("data:")) continue;
                const jsonStr = line.slice(5).trim();
                if (!jsonStr) continue;

                let event;
                try { event = JSON.parse(jsonStr); } catch { continue; }

                if (event.type === "thinking") {
                    // Thinking indicator sudah tampil — tidak perlu aksi
                } else if (event.type === "token") {
                    removeElement(thinkingId);
                    if (!botBubbleCreated) {
                        createBotBubble(botBubbleId);
                        botBubbleCreated = true;
                    }
                    botContent += event.content;
                    document.getElementById(botBubbleId).textContent = botContent;
                    scrollToBottom();
                } else if (event.type === "citations") {
                    if (event.sources && event.sources.length > 0) {
                        appendCitations(botBubbleId, event.sources);
                    }
                } else if (event.type === "done") {
                    chatHistory.push({ role: "assistant", content: botContent });
                    break;
                } else if (event.type === "error") {
                    removeElement(thinkingId);
                    appendErrorBubble(event.message);
                    break;
                }
            }
        }
    } catch (e) {
        removeElement(thinkingId);
        appendErrorBubble("Gagal terhubung ke server. Pastikan server berjalan.");
        console.error(e);
    } finally {
        isStreaming = false;
        document.getElementById("send-btn").disabled = false;
        document.getElementById("status-info").textContent = "Ready";
    }
}

function resetChat() {
    chatHistory = [];
    document.getElementById("chat-messages").innerHTML = "";
    document.getElementById("status-info").textContent = "Percakapan di-reset.";
    setTimeout(() => document.getElementById("status-info").textContent = "Ready", 1500);
}

// ── DOM Helpers ───────────────────────────────────────────────────────────────
function appendBubble(role, content) {
    const div = document.createElement("div");
    div.className = `bubble ${role}`;
    div.textContent = content;
    document.getElementById("chat-messages").appendChild(div);
    scrollToBottom();
}

function appendThinkingBubble(id) {
    const div = document.createElement("div");
    div.id = id;
    div.className = "bubble thinking";
    div.innerHTML = 'Sedang mencari informasi<span class="thinking-dots"></span>';
    document.getElementById("chat-messages").appendChild(div);
    scrollToBottom();
}

function createBotBubble(id) {
    const div = document.createElement("div");
    div.id = id;
    div.className = "bubble bot";
    document.getElementById("chat-messages").appendChild(div);
}

function appendErrorBubble(message) {
    const div = document.createElement("div");
    div.className = "bubble error";
    div.textContent = `⚠️ ${message}`;
    document.getElementById("chat-messages").appendChild(div);
    scrollToBottom();
}

function appendCitations(bubbleId, sources) {
    const bubble = document.getElementById(bubbleId);
    if (!bubble) return;
    const panel = document.createElement("div");
    panel.className = "citations";
    panel.innerHTML = `<h4>📚 Sumber Referensi</h4>` +
        sources.map(s =>
            `<div class="citation-item"><strong>[${s.index}] ${s.title}</strong> — ${s.bab || ""} ${s.bagian || ""}<br><small>${s.preview || ""}</small></div>`
        ).join("");
    bubble.appendChild(panel);
    scrollToBottom();
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ── Tab 2 — Evaluasi ──────────────────────────────────────────────────────────
function scrollToBottom() {
    const msgs = document.getElementById("chat-messages");
    msgs.scrollTop = msgs.scrollHeight;
}

// ── Evaluation Tab ────────────────────────────────────────────────────────────
async function loadEvalData() {
    try {
        const res  = await fetch("/api/evaluation");
        const data = await res.json();
        renderMetricsTable(data.configs);
        renderChart(data.configs);
        renderWilcoxon(data.wilcoxon);
        renderAuditLog(data.audit_log);
    } catch (e) {
        console.error("Gagal load evaluation data:", e);
    }
}

function renderMetricsTable(configs) {
    const container = document.getElementById("metrics-table-container");
    if (!configs || Object.keys(configs).length === 0) {
        container.innerHTML = '<p class="empty-state">Belum ada hasil evaluasi.</p>';
        return;
    }
    const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "response_time_seconds"];
    const configLabels = { a: "Config A (500)", b: "Config B (2000)", c: "Config C (BM25)" };
    let html = `<table><tr><th>Metrik</th>${Object.keys(configs).map(k => `<th>${configLabels[k] || k}</th>`).join("")}</tr>`;
    for (const m of metrics) {
        html += `<tr><td><strong>${m}</strong></td>`;
        for (const cfg of Object.keys(configs)) {
            const s = configs[cfg][m];
            html += s ? `<td>${s.mean.toFixed(3)} ± ${s.std.toFixed(3)}</td>` : "<td>—</td>";
        }
        html += "</tr>";
    }
    html += "</table>";
    container.innerHTML = html;
}

function renderChart(configs) {
    const ctx = document.getElementById("metricsChart").getContext("2d");
    if (metricsChartInstance) metricsChartInstance.destroy();
    if (!configs || Object.keys(configs).length === 0) return;

    const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"];
    const colors  = { a: "#800000", b: "#c9a227", c: "#4a4a4a" };
    const labels  = { a: "Config A", b: "Config B", c: "Config C (BM25)" };

    const datasets = Object.entries(configs).map(([cfg, stats]) => ({
        label: labels[cfg] || cfg,
        data: metrics.map(m => stats[m]?.mean || 0),
        backgroundColor: colors[cfg] || "#999",
    }));

    metricsChartInstance = new Chart(ctx, {
        type: "bar",
        data: { labels: metrics, datasets },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, max: 1 } },
            plugins: { legend: { position: "top" } },
        },
    });
}

function renderWilcoxon(wilcoxon) {
    const container = document.getElementById("wilcoxon-table-container");
    if (!wilcoxon || Object.keys(wilcoxon).length === 0) {
        container.innerHTML = '<p class="empty-state">Jalankan: <code>python evaluation.py --stats</code></p>';
        return;
    }
    let html = `<table><tr><th>Metrik</th><th>Statistik</th><th>p-value</th><th>Signifikan (p<0.05)</th><th>Winner</th></tr>`;
    for (const [metric, stat] of Object.entries(wilcoxon)) {
        html += `<tr><td>${metric}</td><td>${stat.statistic}</td><td>${stat.p_value}</td><td>${stat.significant ? "✅ Ya" : "❌ Tidak"}</td><td>${stat.winner || "—"}</td></tr>`;
    }
    html += "</table>";
    container.innerHTML = html;
}

function renderAuditLog(logs) {
    const container = document.getElementById("audit-log-container");
    if (!logs || logs.length === 0) {
        container.innerHTML = '<p class="empty-state">Belum ada transaksi.</p>';
        return;
    }
    let html = `<table><tr><th>Waktu</th><th>Config</th><th>Query</th><th>Chunks</th><th>Latency</th></tr>`;
    for (const log of logs) {
        html += `<tr><td>${log.timestamp || "—"}</td><td>${log.config || "—"}</td><td>${(log.user_query || "").substring(0, 40)}...</td><td>${log.chunks_retrieved_count || 0}</td><td>${log.response_time_seconds || "—"}s</td></tr>`;
    }
    html += "</table>";
    container.innerHTML = html;
}
