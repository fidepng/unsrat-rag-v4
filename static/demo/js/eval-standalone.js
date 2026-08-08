/**
 * Standalone RAGAS Evaluation Module
 * Mirrors the exact logic of tab-eval from static/js/app.js
 */
let metricsChartInstance = null;

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str).replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}

function safeCreateIcons() {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons({
      attrs: { 'stroke-width': 1.5 }
    });
  }
}

async function loadEvaluationData() {
  const wilcoxonTable = document.getElementById("wilcoxon-table-body");
  const auditTable = document.getElementById("audit-table-body");
  const metaLastRunB = document.getElementById("meta-last-run-b");
  const metaLastRunC = document.getElementById("meta-last-run-c");
  const dotRunB = document.getElementById("dot-run-b");
  const dotRunC = document.getElementById("dot-run-c");
  const metaDatasetSize = document.getElementById("meta-dataset-size");
  const metaGenerator = document.getElementById("meta-generator-model");
  const metaEvaluator = document.getElementById("meta-evaluator-model");
  const metaEmbedding = document.getElementById("meta-embedding-model");

  try {
    const res = await fetch("/api/evaluation");
    if (!res.ok) throw new Error("Gagal mengambil data evaluasi");
    const data = await res.json();

    // A. Metadata Panel
    if (data.metadata) {
      if (metaLastRunB) metaLastRunB.innerText = data.metadata.last_run_b || "-";
      if (metaLastRunC) metaLastRunC.innerText = data.metadata.last_run_c || "-";

      if (dotRunB) {
        dotRunB.className = data.metadata.last_run_b && data.metadata.last_run_b !== "-"
          ? "w-2 h-2 rounded-full bg-green-500 shadow-sm shadow-green-500/50"
          : "w-2 h-2 rounded-full bg-gray-300";
      }

      if (dotRunC) {
        dotRunC.className = data.metadata.last_run_c && data.metadata.last_run_c !== "-"
          ? "w-2 h-2 rounded-full bg-green-500 shadow-sm shadow-green-500/50"
          : "w-2 h-2 rounded-full bg-gray-300";
      }

      if (metaDatasetSize) metaDatasetSize.innerText = data.metadata.dataset_size || "-";
      if (metaGenerator) metaGenerator.innerText = data.metadata.generator_model || "-";
      if (metaEvaluator) metaEvaluator.innerText = data.metadata.evaluator_model || "-";
      if (metaEmbedding) metaEmbedding.innerText = data.metadata.embedding_model || "-";
    }

    // Warning Banner
    const warningBanner = document.getElementById("consistency-warning-banner");
    if (warningBanner) {
      if (data.consistency_warning && data.consistency_warning.has_warning) {
        const msg = data.consistency_warning.message || "Model generator/evaluator antara Config B dan C tidak identik.";
        const detailsList = (data.consistency_warning.details && data.consistency_warning.details.length)
          ? `<ul class="list-disc list-inside text-[11px] text-amber-700 space-y-0.5 mt-1 font-mono">${data.consistency_warning.details.map(d => `<li>${escapeHtml(d)}</li>`).join("")}</ul>`
          : "";
        warningBanner.className = "bg-amber-50 border border-amber-200 rounded-2xl p-4 text-xs text-amber-800 flex items-start space-x-3 shadow-sm";
        warningBanner.innerHTML = `
          <div class="p-1.5 bg-amber-100 text-amber-700 rounded-xl flex-shrink-0 mt-0.5">
            <i data-lucide="alert-triangle" class="w-4 h-4"></i>
          </div>
          <div class="space-y-0.5 flex-1">
            <div class="font-bold">⚠️ Perhatian: ${escapeHtml(msg)}</div>
            ${detailsList}
          </div>
        `;
        warningBanner.classList.remove("hidden");
      } else {
        warningBanner.classList.add("hidden");
      }
    }

    // B. Wilcoxon Table
    if (wilcoxonTable) {
      if (data.wilcoxon && Object.keys(data.wilcoxon).length > 0) {
        wilcoxonTable.innerHTML = Object.entries(data.wilcoxon).map(([metric, row]) => {
          const sigBadge = row.significant
            ? `<span class="bg-green-50 border border-green-200 text-green-700 px-2 py-0.5 rounded-full text-[9px] font-extrabold uppercase">Signifikan</span>`
            : `<span class="bg-gray-50 border border-gray-200 text-gray-500 px-2 py-0.5 rounded-full text-[9px] font-bold">Tidak Sig.</span>`;
          const winnerStr = row.winner === "Tidak signifikan" ? "Tidak signifikan" : row.winner;
          const formatMetric = metric.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

          return `
            <tr class="hover:bg-gray-50 transition duration-150 text-xs">
              <td class="px-4 py-3 font-bold text-gray-800">${escapeHtml(formatMetric)}</td>
              <td class="px-4 py-3 font-mono text-[10px] text-gray-500">${escapeHtml(parseFloat(row.p_value).toFixed(5))}</td>
              <td class="px-4 py-3">${sigBadge}</td>
              <td class="px-4 py-3 text-right"><span class="font-extrabold text-[#7B2D2D]">${escapeHtml(winnerStr)}</span></td>
            </tr>
          `;
        }).join("");
      } else {
        wilcoxonTable.innerHTML = `<tr><td colspan="4" class="px-4 py-4 text-center text-gray-400">Data uji Wilcoxon tidak tersedia.</td></tr>`;
      }
    }

    // C. Live Audit Table
    if (auditTable) {
      const logs = data.audit_log || [];
      if (logs.length > 0) {
        const reversedLogs = [...logs].reverse();
        auditTable.innerHTML = reversedLogs.map(row => {
          const timestampStr = row.timestamp ? (row.timestamp.includes(" ") ? row.timestamp.split(" ")[1] : row.timestamp) : "-";
          const configName = row.config ? row.config.toUpperCase() : "-";
          return `
            <tr class="hover:bg-gray-50/50 transition duration-150 text-xs">
              <td class="px-4 py-2.5 text-gray-400 font-mono text-[10px]">${escapeHtml(timestampStr)}</td>
              <td class="px-4 py-2.5">
                <span class="bg-[#7B2D2D]/10 text-[#7B2D2D] px-2 py-0.5 rounded text-[8px] font-extrabold border border-[#7B2D2D]/15">${escapeHtml(configName)}</span>
              </td>
              <td class="px-4 py-2.5 font-mono text-[9px] text-gray-400 truncate max-w-[80px]" title="${escapeHtml(row.model_llm || '')}">${escapeHtml(row.model_llm || '-')}</td>
              <td class="px-4 py-2.5 font-semibold text-gray-700 truncate max-w-[150px]" title="${escapeHtml(row.user_query || '')}">${escapeHtml(row.user_query || '')}</td>
              <td class="px-4 py-2.5 text-center font-mono font-bold text-gray-600">${row.chunks_retrieved_count ?? 0}</td>
              <td class="px-4 py-2.5 font-mono font-bold text-[#7B2D2D]">${row.best_similarity_score !== null && row.best_similarity_score !== undefined ? parseFloat(row.best_similarity_score).toFixed(4) : "0.0000"}</td>
              <td class="px-4 py-2.5 font-mono text-amber-600 font-bold">${row.response_time_seconds !== null && row.response_time_seconds !== undefined ? parseFloat(row.response_time_seconds).toFixed(2) + "s" : "-"}</td>
              <td class="px-4 py-2.5 text-right font-mono font-bold text-gray-800">${row.estimated_total_tokens ?? 0}</td>
            </tr>
          `;
        }).join("");
      } else {
        auditTable.innerHTML = `<tr><td colspan="8" class="px-4 py-4 text-center text-gray-400">Belum ada transaksi terekam.</td></tr>`;
      }
    }

    // D. Comparison Table
    const comparisonTable = document.getElementById("comparison-table-body");
    if (comparisonTable && data.configs) {
      const metricsToCompare = [
        { key: "faithfulness", name: "Faithfulness" },
        { key: "answer_relevancy", name: "Answer Relevancy" },
        { key: "context_precision", name: "Context Precision" },
        { key: "context_recall", name: "Context Recall" },
        { key: "response_time_seconds", name: "Response Time", isTime: true }
      ];

      comparisonTable.innerHTML = metricsToCompare.map(m => {
        const valB = data.configs.b && data.configs.b[m.key] ? data.configs.b[m.key].mean : null;
        const valC = data.configs.c && data.configs.c[m.key] ? data.configs.c[m.key].mean : null;

        const displayB = valB !== null ? (m.isTime ? `${parseFloat(valB).toFixed(2)}s` : parseFloat(valB).toFixed(4)) : "-";
        const displayC = valC !== null ? (m.isTime ? `${parseFloat(valC).toFixed(2)}s` : parseFloat(valC).toFixed(4)) : "-";

        let classB = "font-medium text-gray-600";
        let classC = "font-medium text-gray-600";
        if (valB !== null && valC !== null) {
          const isBBetter = m.isTime ? (valB < valC) : (valB > valC);
          if (isBBetter) {
            classB = "font-bold text-[#7B2D2D]";
          } else if (valB !== valC) {
            classC = "font-bold text-gray-800";
          }
        }

        return `
          <tr class="hover:bg-gray-50 transition duration-150 text-xs">
            <td class="px-3 py-2.5 font-bold text-gray-850">${escapeHtml(m.name)}</td>
            <td class="px-3 py-2.5 text-center ${classB}">${escapeHtml(displayB)}</td>
            <td class="px-3 py-2.5 text-center ${classC}">${escapeHtml(displayC)}</td>
          </tr>
        `;
      }).join("");
    }

    renderRagasChart(data.configs);
    safeCreateIcons();
  } catch (err) {
    console.error("Gagal memuat data evaluasi:", err);
  }
}

function renderRagasChart(configs) {
  const ctx = document.getElementById("metricsChart");
  if (!ctx || !configs) return;

  const metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"];
  const labels = ["Faithfulness", "Answer Relevancy", "Context Precision", "Context Recall"];

  const dataB = metrics.map(m => configs.b && configs.b[m] ? (configs.b[m].mean ?? 0.0) : 0.0);
  const dataC = metrics.map(m => configs.c && configs.c[m] ? (configs.c[m].mean ?? 0.0) : 0.0);

  if (metricsChartInstance) {
    metricsChartInstance.destroy();
  }

  metricsChartInstance = new Chart(ctx.getContext("2d"), {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Config B",
          data: dataB,
          backgroundColor: "rgba(168, 69, 69, 0.9)",
          borderColor: "rgb(168, 69, 69)",
          borderWidth: 1.5,
          borderRadius: 6
        },
        {
          label: "Config C",
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

document.addEventListener("DOMContentLoaded", () => {
  loadEvaluationData();

  const refreshBtn = document.getElementById("refresh-eval-btn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      loadEvaluationData();
    });
  }

  const btnCopyWilcoxon = document.getElementById("btn-copy-wilcoxon");
  if (btnCopyWilcoxon) {
    btnCopyWilcoxon.addEventListener("click", () => {
      const table = document.getElementById("table-wilcoxon");
      if (!table) return;
      const rows = Array.from(table.querySelectorAll("tr"));
      const text = rows.map(row => {
        return Array.from(row.querySelectorAll("th, td")).map(cell => cell.textContent.trim()).join("\t");
      }).join("\n");
      navigator.clipboard.writeText(text).then(() => alert("Data tabel disalin!")).catch(() => alert("Gagal menyalin!"));
    });
  }
});
