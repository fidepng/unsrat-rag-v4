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
    let systemStatus = null;
    let currentChunkConfig = "B";
    let currentRetrievalConfig = "B";

    // Selectors Section 1
    const keyGoogleStatus = document.getElementById("key-google-status");
    const keyNimStatus = document.getElementById("key-nim-status");
    const statusGenerator = document.getElementById("status-generator-model");
    const statusEvaluator = document.getElementById("status-evaluator-model");
    const statusEmbedding = document.getElementById("status-embedding-model");
    const chromaChunksCount = document.getElementById("chroma-chunks-count");
    const chromaMetaInfo = document.getElementById("chroma-meta-info");
    const bm25Status = document.getElementById("bm25-status");
    const refreshStatusBtn = document.getElementById("refresh-status-btn");

    // Selectors Section 2 (Model Tester)
    const modelSelect = document.getElementById("model-select");
    const testModelBtn = document.getElementById("test-model-btn");
    const setActiveModelBtn = document.getElementById("set-active-model-btn");
    const modelTestResult = document.getElementById("model-test-result");

    // Selectors Section 3 (Chunk Viewer)
    const chunkPrevBtn = document.getElementById("chunk-prev-btn");
    const chunkNextBtn = document.getElementById("chunk-next-btn");
    const chunkIndexInput = document.getElementById("chunk-index-input");
    const chunkConfigB = document.getElementById("chunk-config-b");
    const chunkConfigC = document.getElementById("chunk-config-c");
    const chunkLoadBtn = document.getElementById("chunk-load-btn");
    const chunkMetadata = document.getElementById("chunk-metadata");
    const chunkContentDisplay = document.getElementById("chunk-content-display");

    // Selectors Section 4 (Retrieval)
    const retrievalQueryInput = document.getElementById("retrieval-query-input");
    const retrievalConfigB = document.getElementById("retrieval-config-b");
    const retrievalConfigC = document.getElementById("retrieval-config-c");
    const retrievalSearchBtn = document.getElementById("retrieval-search-btn");
    const retrievalResultsContainer = document.getElementById("retrieval-results-container");
    const retrievalResultsList = document.getElementById("retrieval-results-list");
    const retrievalTimeBadge = document.getElementById("retrieval-time-badge");

    // Selectors Section 5 (Runs)
    const runsTableBody = document.getElementById("runs-table-body");
    const devConsistencyAlert = document.getElementById("dev-consistency-alert");
    const refreshRunsBtn = document.getElementById("refresh-runs-btn");

    // Selectors Section 6 (Terminal)
    const terminalBox = document.getElementById("terminal-box");
    const logFilterAll = document.getElementById("log-filter-all");
    const logFilterError = document.getElementById("log-filter-error");
    const manualRefreshLogsBtn = document.getElementById("manual-refresh-logs");

    // Helper: Escape HTML
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

    // ── SECTION 1: SYSTEM STATUS ─────────────────────────────────────────────
    async function fetchSystemStatus() {
        try {
            const res = await fetch("/api/dev/status");
            if (!res.ok) throw new Error("Gagal mengambil status sistem");
            const data = await res.json();
            systemStatus = data;

            // API Keys
            if (keyGoogleStatus) {
                if (data.google_api_key_present) {
                    keyGoogleStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-100 text-emerald-700 border border-emerald-200";
                    keyGoogleStatus.innerText = "Connected";
                } else {
                    keyGoogleStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-100 text-rose-600 border border-rose-200";
                    keyGoogleStatus.innerText = "Missing";
                }
            }

            if (keyNimStatus) {
                if (data.nvidia_nim_api_key_present) {
                    keyNimStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-100 text-emerald-700 border border-emerald-200";
                    keyNimStatus.innerText = "Connected";
                } else {
                    keyNimStatus.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-100 text-rose-600 border border-rose-200";
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
                        <div>Total PDF: <span class="text-slate-700 font-bold">${escapeHtml(m.total_files || '-')}</span> | Total Karakter: <span class="text-slate-700 font-bold">${(m.total_characters || 0).toLocaleString()}</span></div>
                        <div>Tgl Ingestion: <span class="text-slate-700 font-mono">${escapeHtml(m.ingested_at || '-')}</span></div>
                    `;
                } else {
                    chromaMetaInfo.innerHTML = `<div>Meta: File .ingestion_meta.json belum tersedia</div>`;
                }
            }

            // BM25
            if (bm25Status) {
                if (data.bm25_index_present) {
                    bm25Status.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-100 text-emerald-700 border border-emerald-200";
                    bm25Status.innerText = "Active";
                } else {
                    bm25Status.className = "px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-100 text-amber-700 border border-amber-200";
                    bm25Status.innerText = "Missing";
                }
            }

            // Update model select if active matches options
            if (modelSelect && data.active_generator) {
                let found = false;
                for (let i=0; i<modelSelect.options.length; i++) {
                    if (modelSelect.options[i].value === data.active_generator) {
                        modelSelect.selectedIndex = i;
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    const opt = document.createElement("option");
                    opt.value = data.active_generator;
                    opt.text = data.active_generator;
                    modelSelect.appendChild(opt);
                    modelSelect.value = data.active_generator;
                }
            }

            safeCreateIcons();
        } catch (err) {
            console.error("[Dev JS] Error fetching status:", err);
        }
    }

    if (refreshStatusBtn) {
        refreshStatusBtn.addEventListener("click", () => {
            const icon = refreshStatusBtn.querySelector("i");
            if (icon) icon.classList.add("animate-spin");
            fetchSystemStatus().finally(() => {
                if (icon) icon.classList.remove("animate-spin");
            });
        });
    }

    // ── SECTION 2: MODEL TESTER & SWITCHER ───────────────────────────────────
    if (testModelBtn) {
        testModelBtn.addEventListener("click", async () => {
            if (!modelSelect || !modelTestResult) return;
            const modelName = modelSelect.value;
            
            testModelBtn.disabled = true;
            const originalHtml = testModelBtn.innerHTML;
            testModelBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Testing...`;
            safeCreateIcons();
            
            modelTestResult.classList.remove("hidden");
            modelTestResult.className = "rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm font-mono text-slate-700 whitespace-pre-wrap max-h-64 overflow-y-auto custom-scrollbar";
            modelTestResult.innerHTML = `Mengirim prompt uji ke <span class="font-bold text-rose-600">${escapeHtml(modelName)}</span>...`;

            try {
                const res = await fetch("/api/dev/test_model", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ model_name: modelName })
                });
                const data = await res.json();
                
                if (res.ok) {
                    const latency = data.latency_ms ? `[${data.latency_ms}ms]` : "";
                    modelTestResult.innerHTML = `<div class="text-emerald-600 font-bold mb-2 border-b border-emerald-100 pb-2">✓ Test Berhasil ${latency}</div><div>${escapeHtml(data.response || "No response")}</div>`;
                    modelTestResult.classList.add("bg-emerald-50", "border-emerald-200");
                    modelTestResult.classList.remove("bg-slate-50", "border-slate-200", "bg-rose-50", "border-rose-200");
                } else {
                    modelTestResult.innerHTML = `<div class="text-rose-600 font-bold mb-2 border-b border-rose-100 pb-2">✗ Test Gagal</div><div>${escapeHtml(data.detail || JSON.stringify(data))}</div>`;
                    modelTestResult.classList.add("bg-rose-50", "border-rose-200");
                    modelTestResult.classList.remove("bg-slate-50", "border-slate-200", "bg-emerald-50", "border-emerald-200");
                }
            } catch (err) {
                modelTestResult.innerHTML = `<div class="text-rose-600 font-bold mb-2 border-b border-rose-100 pb-2">✗ Request Error</div><div>${escapeHtml(err.message)}</div>`;
                modelTestResult.classList.add("bg-rose-50", "border-rose-200");
                modelTestResult.classList.remove("bg-slate-50", "border-slate-200", "bg-emerald-50", "border-emerald-200");
            } finally {
                testModelBtn.disabled = false;
                testModelBtn.innerHTML = originalHtml;
                safeCreateIcons();
            }
        });
    }

    if (setActiveModelBtn) {
        setActiveModelBtn.addEventListener("click", async () => {
            if (!modelSelect) return;
            const modelName = modelSelect.value;
            
            if (!confirm(`Ubah model generator aktif ke ${modelName}?`)) return;

            setActiveModelBtn.disabled = true;
            const originalHtml = setActiveModelBtn.innerHTML;
            setActiveModelBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Loading...`;
            safeCreateIcons();

            try {
                const res = await fetch("/api/dev/set_model", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ model_name: modelName })
                });
                
                if (res.ok) {
                    alert(`Model berhasil diubah ke ${modelName}`);
                    await fetchSystemStatus();
                } else {
                    const err = await res.json();
                    alert(`Gagal mengubah model: ${err.detail || 'Unknown error'}`);
                }
            } catch (err) {
                alert(`Gagal mengubah model: ${err.message}`);
            } finally {
                setActiveModelBtn.disabled = false;
                setActiveModelBtn.innerHTML = originalHtml;
                safeCreateIcons();
            }
        });
    }

    // ── SECTION 3: RAW CHUNK VIEWER ──────────────────────────────────────────
    function setChunkConfigUI() {
        if (currentChunkConfig === "B") {
            chunkConfigB.className = "flex-1 px-2 py-1.5 text-xs font-bold rounded-lg bg-white shadow-sm text-slate-800 transition";
            chunkConfigC.className = "flex-1 px-2 py-1.5 text-xs font-medium rounded-lg text-slate-500 hover:text-slate-700 transition";
        } else {
            chunkConfigC.className = "flex-1 px-2 py-1.5 text-xs font-bold rounded-lg bg-white shadow-sm text-slate-800 transition";
            chunkConfigB.className = "flex-1 px-2 py-1.5 text-xs font-medium rounded-lg text-slate-500 hover:text-slate-700 transition";
        }
    }

    if (chunkConfigB) chunkConfigB.addEventListener("click", () => { currentChunkConfig = "B"; setChunkConfigUI(); });
    if (chunkConfigC) chunkConfigC.addEventListener("click", () => { currentChunkConfig = "C"; setChunkConfigUI(); });

    if (chunkPrevBtn) chunkPrevBtn.addEventListener("click", () => {
        if (chunkIndexInput) {
            let val = parseInt(chunkIndexInput.value) || 0;
            if (val > 0) {
                chunkIndexInput.value = val - 1;
                loadChunk(val - 1);
            }
        }
    });

    if (chunkNextBtn) chunkNextBtn.addEventListener("click", () => {
        if (chunkIndexInput) {
            let val = parseInt(chunkIndexInput.value) || 0;
            chunkIndexInput.value = val + 1;
            loadChunk(val + 1);
        }
    });

    if (chunkLoadBtn) chunkLoadBtn.addEventListener("click", () => {
        let val = parseInt(chunkIndexInput.value) || 0;
        loadChunk(val);
    });

    async function loadChunk(index) {
        if (!chunkContentDisplay || !chunkMetadata) return;
        
        chunkLoadBtn.disabled = true;
        chunkLoadBtn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> Memuat...`;
        safeCreateIcons();
        chunkContentDisplay.innerText = "Memuat...";
        chunkMetadata.innerHTML = "";

        try {
            const res = await fetch(`/api/dev/chunks?index=${index}&config=${currentChunkConfig.toLowerCase()}`);
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Not found");
            }
            const data = await res.json();
            
            chunkContentDisplay.innerText = data.content || "";
            
            if (data.metadata) {
                const metaList = Object.entries(data.metadata).map(([k, v]) => {
                    return `<span class="px-2 py-1 bg-slate-100 text-slate-600 rounded-md text-[10px] font-mono border border-slate-200 whitespace-nowrap"><span class="font-bold text-slate-700">${escapeHtml(k)}:</span> ${escapeHtml(v)}</span>`;
                }).join("");
                chunkMetadata.innerHTML = metaList;
            }
        } catch (err) {
            chunkContentDisplay.innerText = `Error: ${err.message}`;
            chunkMetadata.innerHTML = "";
        } finally {
            chunkLoadBtn.disabled = false;
            chunkLoadBtn.innerHTML = `<i data-lucide="download" class="w-3.5 h-3.5"></i> Load Chunk`;
            safeCreateIcons();
        }
    }

    // ── SECTION 4: RETRIEVAL PLAYGROUND ──────────────────────────────────────
    function setRetrievalConfigUI() {
        if (currentRetrievalConfig === "B") {
            retrievalConfigB.className = "px-3 py-1.5 text-xs font-bold rounded-lg bg-white shadow-sm text-slate-800 transition";
            retrievalConfigC.className = "px-3 py-1.5 text-xs font-medium rounded-lg text-slate-500 hover:text-slate-700 transition";
        } else {
            retrievalConfigC.className = "px-3 py-1.5 text-xs font-bold rounded-lg bg-white shadow-sm text-slate-800 transition";
            retrievalConfigB.className = "px-3 py-1.5 text-xs font-medium rounded-lg text-slate-500 hover:text-slate-700 transition";
        }
    }

    if (retrievalConfigB) retrievalConfigB.addEventListener("click", () => { currentRetrievalConfig = "B"; setRetrievalConfigUI(); });
    if (retrievalConfigC) retrievalConfigC.addEventListener("click", () => { currentRetrievalConfig = "C"; setRetrievalConfigUI(); });

    if (retrievalSearchBtn) {
        retrievalSearchBtn.addEventListener("click", async () => {
            if (!retrievalQueryInput || !retrievalResultsContainer || !retrievalResultsList) return;
            const query = retrievalQueryInput.value.trim();
            if (!query) return;

            retrievalSearchBtn.disabled = true;
            const originalHtml = retrievalSearchBtn.innerHTML;
            retrievalSearchBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i>`;
            safeCreateIcons();

            retrievalResultsContainer.classList.remove("hidden");
            retrievalResultsList.innerHTML = `<div class="text-sm text-slate-500 text-center py-4">Mencari dokumen...</div>`;
            if(retrievalTimeBadge) retrievalTimeBadge.classList.add("hidden");

            try {
                const start = performance.now();
                const res = await fetch(`/api/dev/retrieval_test?query=${encodeURIComponent(query)}&config=${currentRetrievalConfig.toLowerCase()}`);
                const end = performance.now();
                
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Request failed");
                }
                const data = await res.json();
                
                if(retrievalTimeBadge) {
                    retrievalTimeBadge.innerText = `${(end - start).toFixed(0)} ms`;
                    retrievalTimeBadge.classList.remove("hidden");
                }

                const results = data.results || [];
                if (results.length === 0) {
                    retrievalResultsList.innerHTML = `<div class="text-sm text-slate-500 bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">Tidak ada hasil ditemukan.</div>`;
                } else {
                    retrievalResultsList.innerHTML = results.map((r, idx) => {
                        const title = r.title || r.metadata?.title || `Document ${idx+1}`;
                        const score = r.score !== undefined ? parseFloat(r.score).toFixed(4) : (r.distance !== undefined ? parseFloat(r.distance).toFixed(4) : "-");
                        const scoreLabel = currentRetrievalConfig === "B" ? "Distance" : "Score";
                        const content = r.content || r.text || "";
                        
                        return `
                            <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 hover:border-slate-300 transition">
                                <div class="flex justify-between items-start mb-2 gap-4">
                                    <h4 class="font-bold text-slate-800 text-sm line-clamp-1 flex-1" title="${escapeHtml(title)}">${escapeHtml(title)}</h4>
                                    <span class="px-2 py-0.5 bg-rose-50 text-rose-600 rounded text-[10px] font-mono border border-rose-100 whitespace-nowrap">${scoreLabel}: ${escapeHtml(score)}</span>
                                </div>
                                <p class="text-xs text-slate-600 font-mono line-clamp-3 bg-white p-2 border border-slate-100 rounded">${escapeHtml(content)}</p>
                            </div>
                        `;
                    }).join("");
                }
            } catch (err) {
                retrievalResultsList.innerHTML = `<div class="text-sm text-rose-600 bg-rose-50 border border-rose-200 rounded-xl p-4">Error: ${escapeHtml(err.message)}</div>`;
            } finally {
                retrievalSearchBtn.disabled = false;
                retrievalSearchBtn.innerHTML = originalHtml;
                safeCreateIcons();
            }
        });
    }

    if (retrievalQueryInput) {
        retrievalQueryInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                retrievalSearchBtn.click();
            }
        });
    }

    // ── SECTION 5: EVALUATION RUNS MANAGER ──────────────────────────────────
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
                runsTableBody.innerHTML = `<tr><td colspan="9" class="px-4 py-6 text-center text-rose-500 font-medium">Gagal memuat daftar runs evaluasi.</td></tr>`;
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
                    devConsistencyAlert.className = "bg-amber-50 border border-amber-200 rounded-xl p-4 text-xs text-amber-800 space-y-1 shadow-sm";
                    devConsistencyAlert.innerHTML = `
                        <div class="font-bold flex items-center space-x-2 text-amber-700">
                            <i data-lucide="alert-triangle" class="w-4 h-4 text-amber-500"></i>
                            <span>⚠️ Consistency Warning: Active Config B & C Runs Differ!</span>
                        </div>
                        <p class="text-[11px] text-amber-700/80 mt-1">Perbandingan performa antara Config B dan Config C mungkin tidak sebanding secara ilmiah karena terdapat ketidaksesuaian parameter berikut:</p>
                        <ul class="list-disc list-inside text-[11px] font-mono text-amber-800 space-y-0.5 mt-2">
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
                ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-600 border border-rose-200 whitespace-nowrap">${failedCount} errors</span>`
                : `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700 border border-emerald-200 whitespace-nowrap">0</span>`;

            const activeBadge = run.is_active
                ? `<span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase bg-emerald-100 text-emerald-700 border border-emerald-200 flex items-center space-x-1 justify-center whitespace-nowrap"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span><span>Active</span></span>`
                : `<span class="px-2.5 py-1 rounded-full text-[10px] font-medium bg-slate-100 text-slate-500 border border-slate-200 block text-center whitespace-nowrap">Inactive</span>`;

            const starBadge = isStar
                ? `<span class="inline-flex items-center text-amber-500 ml-1" title="Highest Faithfulness (0 Errors)">⭐</span>`
                : "";

            const actionBtn = run.is_active
                ? `<span class="text-slate-400 text-[11px] font-mono italic whitespace-nowrap">Dipakai</span>`
                : `<button onclick="activateRun('${escapeHtml(run.run_id)}')" class="px-3 py-1.5 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 active:bg-slate-100 text-slate-700 rounded-lg text-[11px] font-bold transition shadow-sm whitespace-nowrap">Set Active</button>`;

            const configUpper = String(run.config || "B").toUpperCase();

            return `
                <tr class="hover:bg-slate-50 transition">
                    <td class="px-4 py-3 font-bold text-slate-800">
                        <span class="px-2 py-0.5 rounded bg-slate-100 border border-slate-200 text-xs font-mono">${escapeHtml(configUpper)}</span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="font-mono text-xs font-bold text-slate-800 flex items-center whitespace-nowrap">
                            <span>${escapeHtml(run.run_id)}</span>
                            ${starBadge}
                        </div>
                        <div class="text-[10px] text-slate-500 mt-0.5 whitespace-nowrap">${escapeHtml(run.timestamp || '-')}</div>
                    </td>
                    <td class="px-4 py-3 font-mono text-[11px] text-slate-600 truncate max-w-[140px]" title="${escapeHtml(run.generator_model || '')}">${escapeHtml(run.generator_model || '-')}</td>
                    <td class="px-4 py-3 font-mono text-[11px] text-slate-600 truncate max-w-[140px]" title="${escapeHtml(run.evaluator_model || '')}">${escapeHtml(run.evaluator_model || '-')}</td>
                    <td class="px-4 py-3 text-center font-mono font-bold ${isStar ? 'text-amber-600' : 'text-slate-800'}">${escapeHtml(faithfulnessStr)}</td>
                    <td class="px-4 py-3 text-center font-mono font-bold text-slate-800">${escapeHtml(relevancyStr)}</td>
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
        refreshRunsBtn.addEventListener("click", (e) => {
            e.stopPropagation(); // prevent details toggling
            const icon = refreshRunsBtn.querySelector("i");
            if (icon) icon.classList.add("animate-spin");
            fetchRuns().finally(() => {
                if (icon) icon.classList.remove("animate-spin");
            });
        });
    }

    // ── SECTION 6: LIVE LOG TERMINAL ─────────────────────────────────────────
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
            terminalBox.innerHTML = `<div class="text-slate-500 italic px-2 py-4">[Tidak ada log ${logFilter === "error" ? "error/warning" : ""} ditemukan]</div>`;
            return;
        }

        // Prevent full re-render if count is same and it's not a filter change? 
        // For simplicity, re-render, but manage scroll position carefully.
        const isScrolledToBottom = terminalBox.scrollHeight - terminalBox.clientHeight <= terminalBox.scrollTop + 20;

        terminalBox.innerHTML = filtered.map((line, idx) => {
            const upper = line.toUpperCase();
            let colorClass = "text-slate-300";
            if (upper.includes("ERROR") || upper.includes("CRITICAL") || upper.includes("EXCEPTION")) {
                colorClass = "text-rose-400 font-bold bg-rose-950/40 px-1.5 py-0.5 rounded";
            } else if (upper.includes("WARNING") || upper.includes("WARN")) {
                colorClass = "text-amber-300 font-medium";
            } else if (upper.includes("POST /") || upper.includes("GET /")) {
                colorClass = "text-cyan-400 font-medium";
            } else if (upper.includes("INFO")) {
                colorClass = "text-slate-300";
            }

            return `
                <div class="flex items-start space-x-3 leading-relaxed hover:bg-slate-800/50 px-2 py-0.5 rounded transition-colors">
                    <span class="text-slate-600/70 text-[10px] select-none w-8 text-right flex-shrink-0 pt-0.5">${idx + 1}</span>
                    <span class="${colorClass} break-all">${escapeHtml(line)}</span>
                </div>
            `;
        }).join("");

        // Auto-scroll to bottom if it was previously at the bottom
        if (isScrolledToBottom) {
            terminalBox.scrollTop = terminalBox.scrollHeight;
        }
    }

    if (logFilterAll) {
        logFilterAll.addEventListener("click", () => {
            logFilter = "all";
            logFilterAll.className = "px-3 py-1 rounded-lg text-slate-800 bg-slate-100 font-semibold transition";
            logFilterError.className = "px-3 py-1 rounded-lg text-slate-500 hover:text-slate-700 font-medium transition";
            renderLogs(logLinesData);
            terminalBox.scrollTop = terminalBox.scrollHeight;
        });
    }

    if (logFilterError) {
        logFilterError.addEventListener("click", () => {
            logFilter = "error";
            logFilterError.className = "px-3 py-1 rounded-lg text-rose-700 bg-rose-100 font-semibold transition";
            logFilterAll.className = "px-3 py-1 rounded-lg text-slate-500 hover:text-slate-700 font-medium transition";
            renderLogs(logLinesData);
            terminalBox.scrollTop = terminalBox.scrollHeight;
        });
    }

    if (manualRefreshLogsBtn) {
        manualRefreshLogsBtn.addEventListener("click", () => {
            const icon = manualRefreshLogsBtn.querySelector("i");
            if (icon) icon.classList.add("animate-spin");
            fetchLogs().finally(() => {
                if (icon) icon.classList.remove("animate-spin");
                terminalBox.scrollTop = terminalBox.scrollHeight;
            });
        });
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
