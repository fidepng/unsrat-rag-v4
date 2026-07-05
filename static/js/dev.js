// static/js/dev.js — Developer Panel Frontend Logic

document.addEventListener("DOMContentLoaded", () => {
    function safeCreateIcons() {
        try {
            if (typeof lucide !== "undefined" && lucide.createIcons) {
                lucide.createIcons();
            }
        } catch (e) {
            console.error("[Dev JS] Failed to create Lucide icons:", e);
        }
    }

    safeCreateIcons();

    // ── STATE ────────────────────────────────────────────────────────────────
    let logFilter = "all"; // "all" | "error"
    let logInterval = null;
    let runsData = [];
    let logLinesData = [];

    // Selectors
    const keyGoogleStatus = document.getElementById("key-google-status");
    const keyNimStatus = document.getElementById("key-nim-status");
    const statusGenerator = document.getElementById("status-generator-model");
    const statusEvaluator = document.getElementById("status-evaluator-model");
    const statusEmbedding = document.getElementById("status-embedding-model");
    const chromaChunksCount = document.getElementById("chroma-chunks-count");
    const chromaMetaInfo = document.getElementById("chroma-meta-info");
    const bm25Status = document.getElementById("bm25-status");

    const refreshStatusBtn = document.getElementById("refresh-status-btn");
    const runPreflightBtn = document.getElementById("run-preflight-btn");
    const refreshRunsBtn = document.getElementById("refresh-runs-btn");
    const manualRefreshLogsBtn = document.getElementById("manual-refresh-logs");

    const pfGoogleBadge = document.getElementById("pf-google-badge");
    const pfGoogleDetails = document.getElementById("pf-google-details");
    const pfGeneratorBadge = document.getElementById("pf-generator-badge");
    const pfGeneratorDetails = document.getElementById("pf-generator-details");
    const pfEvaluatorBadge = document.getElementById("pf-evaluator-badge");
    const pfEvaluatorDetails = document.getElementById("pf-evaluator-details");

    const runsTableBody = document.getElementById("runs-table-body");
    const devConsistencyAlert = document.getElementById("dev-consistency-alert");

    const terminalBox = document.getElementById("terminal-box");
    const logFilterAll = document.getElementById("log-filter-all");
    const logFilterError = document.getElementById("log-filter-error");

    // ── SECTION 1: SYSTEM STATUS ─────────────────────────────────────────────
    async function fetchSystemStatus() {
        try {
            const res = await fetch("/api/dev/status");
            if (!res.ok) throw new Error("Gagal mengambil status sistem");
            const data = await res.json();

            // API Keys
            if (keyGoogleStatus) {
                if (data.google_api_key_present) {
                    keyGoogleStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                    keyGoogleStatus.innerText = "Connected";
                } else {
                    keyGoogleStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                    keyGoogleStatus.innerText = "Missing";
                }
            }

            if (keyNimStatus) {
                if (data.nvidia_nim_api_key_present) {
                    keyNimStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                    keyNimStatus.innerText = "Connected";
                } else {
                    keyNimStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                    keyNimStatus.innerText = "Missing";
                }
            }

            // Models
            if (statusGenerator) statusGenerator.innerText = data.active_generator || "-";
            if (statusEvaluator) statusEvaluator.innerText = data.active_evaluator || "-";
            if (statusEmbedding) statusEmbedding.innerText = data.active_embedding || "-";

            // ChromaDB
            if (chromaChunksCount) chromaChunksCount.innerText = (data.chromadb_config_b_chunks || 0).toLocaleString();
            if (chromaMetaInfo) {
                if (data.chromadb_config_b_meta) {
                    const m = data.chromadb_config_b_meta;
                    chromaMetaInfo.innerHTML = `
                        <div>Total PDF: <span class="text-slate-300 font-bold">${escapeHtml(m.total_files || '-')}</span> | Total Karakter: <span class="text-slate-300 font-bold">${(m.total_characters || 0).toLocaleString()}</span></div>
                        <div>Tgl Ingestion: <span class="text-slate-300 font-mono">${escapeHtml(m.ingested_at || '-')}</span></div>
                    `;
                } else {
                    chromaMetaInfo.innerHTML = `<div>Meta: File .ingestion_meta.json belum tersedia</div>`;
                }
            }

            // BM25
            if (bm25Status) {
                if (data.bm25_index_present) {
                    bm25Status.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                    bm25Status.innerText = "Active";
                } else {
                    bm25Status.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20";
                    bm25Status.innerText = "Missing";
                }
            }

            safeCreateIcons();
        } catch (err) {
            console.error("[Dev JS] Error fetching status:", err);
        }
    }

    if (refreshStatusBtn) {
        refreshStatusBtn.addEventListener("click", fetchSystemStatus);
    }

    // ── SECTION 2: LIVE API PRE-FLIGHT CHECK ─────────────────────────────────
    async function runPreflight() {
        if (!runPreflightBtn) return;

        runPreflightBtn.disabled = true;
        runPreflightBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Testing APIs...</span>`;
        safeCreateIcons();

        // Set pending status
        [pfGoogleBadge, pfGeneratorBadge, pfEvaluatorBadge].forEach(b => {
            if (b) {
                b.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 animate-pulse";
                b.innerText = "Testing...";
            }
        });

        try {
            const res = await fetch("/api/dev/preflight");
            if (!res.ok) throw new Error("Gagal menjalankan preflight check");
            const data = await res.json();

            // Google API
            if (data.google_api) {
                const g = data.google_api;
                if (g.status === "ok") {
                    pfGoogleBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                    pfGoogleBadge.innerText = "OK (" + (g.latency_ms || 0) + "ms)";
                    pfGoogleDetails.innerHTML = `<span class="text-emerald-400 font-medium">Respon normal.</span> Latensi: <span class="font-mono font-bold text-slate-200">${escapeHtml(g.latency_ms || 0)}ms</span>`;
                } else {
                    pfGoogleBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                    pfGoogleBadge.innerText = "ERROR";
                    pfGoogleDetails.innerHTML = `<span class="text-rose-400 font-medium">${escapeHtml(g.error || "Gagal terkoneksi ke Google API")}</span>`;
                }
            }

            // Generator LLM
            if (data.generator_model) {
                const gen = data.generator_model;
                if (gen.status === "ok") {
                    pfGeneratorBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                    pfGeneratorBadge.innerText = "OK (" + (gen.latency_ms || 0) + "ms)";
                    pfGeneratorDetails.innerHTML = `<div class="font-mono text-slate-300 font-bold truncate">${escapeHtml(gen.model || '')}</div><div class="text-emerald-400 text-[11px]">Respon normal. Latensi: ${escapeHtml(gen.latency_ms || 0)}ms</div>`;
                } else {
                    pfGeneratorBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                    pfGeneratorBadge.innerText = "ERROR";
                    pfGeneratorDetails.innerHTML = `<div class="font-mono text-slate-300 font-bold truncate">${escapeHtml(gen.model || '')}</div><div class="text-rose-400 text-[11px]">${escapeHtml(gen.error || "Gagal menguji generator LLM")}</div>`;
                }
            }

            // Evaluator LLM
            if (data.evaluator_model) {
                const ev = data.evaluator_model;
                if (ev.status === "ok") {
                    pfEvaluatorBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                    pfEvaluatorBadge.innerText = "OK (" + (ev.latency_ms || 0) + "ms)";
                    pfEvaluatorDetails.innerHTML = `<div class="font-mono text-slate-300 font-bold truncate">${escapeHtml(ev.model || '')}</div><div class="text-emerald-400 text-[11px]">Respon normal. Latensi: ${escapeHtml(ev.latency_ms || 0)}ms</div>`;
                } else {
                    pfEvaluatorBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                    pfEvaluatorBadge.innerText = "ERROR";
                    pfEvaluatorDetails.innerHTML = `<div class="font-mono text-slate-300 font-bold truncate">${escapeHtml(ev.model || '')}</div><div class="text-rose-400 text-[11px]">${escapeHtml(ev.error || "Gagal menguji evaluator LLM")}</div>`;
                }
            }

        } catch (err) {
            console.error("[Dev JS] Preflight failed:", err);
            [pfGoogleBadge, pfGeneratorBadge, pfEvaluatorBadge].forEach(b => {
                if (b) {
                    b.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                    b.innerText = "FAILED";
                }
            });
        } finally {
            runPreflightBtn.disabled = false;
            runPreflightBtn.innerHTML = `<i data-lucide="play-circle" class="w-4 h-4"></i><span>Run Pre-flight Check</span>`;
            safeCreateIcons();
        }
    }

    if (runPreflightBtn) {
        runPreflightBtn.addEventListener("click", runPreflight);
    }

    // ── SECTION 3: EVALUATION RUNS MANAGER ──────────────────────────────────
    async function fetchRuns() {
        try {
            const res = await fetch("/api/dev/runs");
            if (!res.ok) throw new Error("Gagal membaca manifest runs");
            const data = await res.json();
            runsData = data.runs || [];
            renderRunsTable(runsData);
        } catch (err) {
            console.error("[Dev JS] Failed to fetch runs:", err);
            if (runsTableBody) {
                runsTableBody.innerHTML = `<tr><td colspan="9" class="px-4 py-6 text-center text-rose-400">Gagal memuat daftar runs evaluasi.</td></tr>`;
            }
        }
    }

    function renderRunsTable(runs) {
        if (!runsTableBody) return;

        if (runs.length === 0) {
            runsTableBody.innerHTML = `<tr><td colspan="9" class="px-4 py-6 text-center text-slate-500">Belum ada pengujian evaluasi yang diarsip di manifest.</td></tr>`;
            if (devConsistencyAlert) devConsistencyAlert.classList.add("hidden");
            return;
        }

        // Find highest faithfulness run among runs with 0 failed evals
        let maxFaithfulness = -1;
        let starRunId = null;

        runs.forEach(run => {
            const summary = run.metrics_summary || {};
            const failedCount = summary.failed_evals_count || 0;
            const faithfulness = parseFloat(summary.faithfulness) || 0;

            if (failedCount === 0 && faithfulness > maxFaithfulness) {
                maxFaithfulness = faithfulness;
                starRunId = run.run_id;
            }
        });

        // Consistency check between active Config B and Config C
        let activeB = runs.find(r => r.is_active && String(r.config).toLowerCase() === "b");
        let activeC = runs.find(r => r.is_active && String(r.config).toLowerCase() === "c");

        if (devConsistencyAlert) {
            if (activeB && activeC) {
                const diffs = [];
                if (activeB.generator_model !== activeC.generator_model) {
                    diffs.push(`Model Generator berbeda: Config B (${activeB.generator_model}) vs Config C (${activeC.generator_model})`);
                }
                if (activeB.evaluator_model !== activeC.evaluator_model) {
                    diffs.push(`Model Evaluator berbeda: Config B (${activeB.evaluator_model}) vs Config C (${activeC.evaluator_model})`);
                }
                if (activeB.ground_truth_hash !== activeC.ground_truth_hash) {
                    diffs.push(`Ground Truth Hash berbeda: Config B (${activeB.ground_truth_hash}) vs Config C (${activeC.ground_truth_hash})`);
                }

                if (diffs.length > 0) {
                    devConsistencyAlert.className = "bg-amber-950/60 border border-amber-700/60 rounded-2xl p-4 text-xs text-amber-200 space-y-1 shadow-lg";
                    devConsistencyAlert.innerHTML = `
                        <div class="font-bold flex items-center space-x-2 text-amber-300">
                            <i data-lucide="alert-triangle" class="w-4 h-4 text-amber-400"></i>
                            <span>⚠️ Consistency Warning: Active Config B & C Runs Differ!</span>
                        </div>
                        <p class="text-[11px] text-amber-300/80">Perbandingan performa antara Config B dan Config C mungkin tidak sebanding secara ilmiah karena terdapat ketidaksesuaian parameter berikut:</p>
                        <ul class="list-disc list-inside text-[11px] font-mono text-amber-200/90 space-y-0.5">
                            ${diffs.map(d => `<li>${escapeHtml(d)}</li>`).join("")}
                        </ul>
                    `;
                    devConsistencyAlert.classList.remove("hidden");
                } else {
                    devConsistencyAlert.classList.add("hidden");
                }
            } else {
                devConsistencyAlert.classList.add("hidden");
            }
        }

        runsTableBody.innerHTML = runs.map(run => {
            const isStar = run.run_id === starRunId;
            const summary = run.metrics_summary || {};
            const faithfulnessStr = summary.faithfulness !== undefined && summary.faithfulness !== null ? parseFloat(summary.faithfulness).toFixed(4) : "-";
            const relevancyStr = summary.answer_relevancy !== undefined && summary.answer_relevancy !== null ? parseFloat(summary.answer_relevancy).toFixed(4) : "-";
            const failedCount = summary.failed_evals_count || 0;
            const failedBadge = failedCount > 0
                ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">${failedCount} errors</span>`
                : `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">0</span>`;

            const activeBadge = run.is_active
                ? `<span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex items-center space-x-1 justify-center"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span><span>Active</span></span>`
                : `<span class="px-2.5 py-1 rounded-full text-[10px] font-medium bg-slate-800 text-slate-400 border border-slate-700 block text-center">Inactive</span>`;

            const starBadge = isStar
                ? `<span class="inline-flex items-center text-amber-400 ml-1" title="Highest Faithfulness (0 Errors)">⭐</span>`
                : "";

            const actionBtn = run.is_active
                ? `<span class="text-slate-500 text-[11px] font-mono italic">Dipakai</span>`
                : `<button onclick="activateRun('${escapeHtml(run.run_id)}')" class="px-3 py-1 bg-rose-600 hover:bg-rose-500 active:bg-rose-700 text-white rounded-lg text-xs font-bold transition shadow-sm">Set Active</button>`;

            const configUpper = String(run.config || "B").toUpperCase();

            return `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="px-4 py-3 font-bold text-slate-200">
                        <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-xs font-mono">${escapeHtml(configUpper)}</span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="font-mono text-xs font-bold text-slate-200 flex items-center">
                            <span>${escapeHtml(run.run_id)}</span>
                            ${starBadge}
                        </div>
                        <div class="text-[10px] text-slate-400">${escapeHtml(run.timestamp || '-')}</div>
                    </td>
                    <td class="px-4 py-3 font-mono text-[11px] text-slate-300 truncate max-w-[140px]" title="${escapeHtml(run.generator_model || '')}">${escapeHtml(run.generator_model || '-')}</td>
                    <td class="px-4 py-3 font-mono text-[11px] text-slate-300 truncate max-w-[140px]" title="${escapeHtml(run.evaluator_model || '')}">${escapeHtml(run.evaluator_model || '-')}</td>
                    <td class="px-4 py-3 text-center font-mono font-bold ${isStar ? 'text-amber-400' : 'text-slate-200'}">${escapeHtml(faithfulnessStr)}</td>
                    <td class="px-4 py-3 text-center font-mono font-bold text-slate-200">${escapeHtml(relevancyStr)}</td>
                    <td class="px-4 py-3 text-center">${failedBadge}</td>
                    <td class="px-4 py-3 text-center">${activeBadge}</td>
                    <td class="px-4 py-3 text-right">${actionBtn}</td>
                </tr>
            `;
        }).join("");

        safeCreateIcons();
    }

    window.activateRun = async function(runId) {
        if (!confirm(`Aktifkan hasil pengujian run '${runId}'? Ini akan menggantikan file CSV aktif.`)) {
            return;
        }

        try {
            const res = await fetch("/api/dev/runs/activate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ run_id: runId })
            });

            if (!res.ok) {
                let errorMsg = `HTTP Error ${res.status}`;
                try {
                    const errJson = await res.json();
                    if (errJson && errJson.detail) {
                        errorMsg = errJson.detail;
                    }
                } catch (e) {
                    const text = await res.text().catch(() => "");
                    if (text) errorMsg = text;
                }
                throw new Error(errorMsg);
            }

            console.log(`[Dev JS] Successfully activated run: ${runId}`);
            await fetchRuns();
            await fetchSystemStatus();
        } catch (err) {
            console.error("[Dev JS] Error activating run:", err);
            alert(`Gagal mengaktifkan run: ${err.message}`);
        }
    };

    if (refreshRunsBtn) {
        refreshRunsBtn.addEventListener("click", fetchRuns);
    }

    // ── SECTION 4: LIVE LOG TERMINAL ─────────────────────────────────────────
    async function fetchLogs() {
        try {
            const res = await fetch("/api/dev/logs?lines=100");
            if (!res.ok) throw new Error("Gagal mengambil log sistem");
            const data = await res.json();
            logLinesData = data.lines || [];
            renderLogs(logLinesData);
        } catch (err) {
            console.error("[Dev JS] Error fetching logs:", err);
        }
    }

    function renderLogs(lines) {
        if (!terminalBox) return;

        let filtered = lines;
        if (logFilter === "error") {
            filtered = lines.filter(line => {
                const upper = line.toUpperCase();
                return upper.includes("ERROR") || upper.includes("WARN") || upper.includes("CRITICAL") || upper.includes("EXCEPTION") || upper.includes("FAILED");
            });
        }

        if (filtered.length === 0) {
            terminalBox.innerHTML = `<div class="text-slate-500 italic">[Tidak ada log ${logFilter === "error" ? "error/warning" : ""} ditemukan]</div>`;
            return;
        }

        terminalBox.innerHTML = filtered.map((line, idx) => {
            const upper = line.toUpperCase();
            let colorClass = "text-slate-300";
            if (upper.includes("ERROR") || upper.includes("CRITICAL") || upper.includes("EXCEPTION")) {
                colorClass = "text-rose-400 font-bold bg-rose-950/30 px-1 rounded";
            } else if (upper.includes("WARNING") || upper.includes("WARN")) {
                colorClass = "text-amber-300 font-medium";
            } else if (upper.includes("POST /") || upper.includes("GET /")) {
                colorClass = "text-cyan-400 font-medium";
            } else if (upper.includes("INFO")) {
                colorClass = "text-slate-300";
            }

            return `
                <div class="flex items-start space-x-3 leading-relaxed hover:bg-slate-900/50 px-1 rounded">
                    <span class="text-slate-600 text-[10px] select-none w-8 text-right flex-shrink-0">${idx + 1}</span>
                    <span class="${colorClass} break-all">${escapeHtml(line)}</span>
                </div>
            `;
        }).join("");

        // Auto-scroll to bottom
        terminalBox.scrollTop = terminalBox.scrollHeight;
    }

    function escapeHtml(str) {
        if (str === null || str === undefined) return "";
        return String(str).replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    if (logFilterAll) {
        logFilterAll.addEventListener("click", () => {
            logFilter = "all";
            logFilterAll.className = "px-3 py-1 rounded-lg text-slate-200 bg-slate-800 font-semibold transition";
            logFilterError.className = "px-3 py-1 rounded-lg text-slate-400 hover:text-slate-200 font-medium transition";
            renderLogs(logLinesData);
        });
    }

    if (logFilterError) {
        logFilterError.addEventListener("click", () => {
            logFilter = "error";
            logFilterError.className = "px-3 py-1 rounded-lg text-rose-400 bg-rose-950/60 border border-rose-800/50 font-semibold transition";
            logFilterAll.className = "px-3 py-1 rounded-lg text-slate-400 hover:text-slate-200 font-medium transition";
            renderLogs(logLinesData);
        });
    }

    if (manualRefreshLogsBtn) {
        manualRefreshLogsBtn.addEventListener("click", fetchLogs);
    }

    function startLogPolling() {
        if (logInterval) clearInterval(logInterval);
        fetchLogs();
        logInterval = setInterval(fetchLogs, 5000); // 5s auto-refresh
    }

    // ── INITIALIZATION ───────────────────────────────────────────────────────
    fetchSystemStatus();
    fetchRuns();
    startLogPolling();
});
