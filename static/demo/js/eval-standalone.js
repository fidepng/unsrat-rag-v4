document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  const refreshBtn = document.getElementById('refresh-eval-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', loadEvaluationData);
  }

  loadEvaluationData();
});

async function loadEvaluationData() {
  const summaryElem = document.getElementById('eval-metrics-summary');
  if (summaryElem) summaryElem.innerHTML = 'Memuat data evaluasi...';

  try {
    const res = await fetch('/api/evaluation');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    renderChart(data);

    if (summaryElem) {
      summaryElem.innerHTML = `
        <div class="space-y-2">
          <div class="flex justify-between border-b pb-1"><span>Faithfulness:</span> <strong class="text-stone-800">${data.faithfulness ?? 'N/A'}</strong></div>
          <div class="flex justify-between border-b pb-1"><span>Answer Relevancy:</span> <strong class="text-stone-800">${data.answer_relevancy ?? 'N/A'}</strong></div>
          <div class="flex justify-between border-b pb-1"><span>Context Precision:</span> <strong class="text-stone-800">${data.context_precision ?? 'N/A'}</strong></div>
          <div class="flex justify-between border-b pb-1"><span>Context Recall:</span> <strong class="text-stone-800">${data.context_recall ?? 'N/A'}</strong></div>
        </div>
      `;
    }
  } catch (err) {
    if (summaryElem) {
      summaryElem.innerHTML = `<span class="text-red-600">Gagal memuat data evaluasi: ${err.message}</span>`;
    }
  }
}

function renderChart(data) {
  const ctx = document.getElementById('ragasChart');
  if (!ctx) return;

  if (window.myRagasChart) {
    window.myRagasChart.destroy();
  }

  window.myRagasChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Faithfulness', 'Answer Relevancy', 'Context Precision', 'Context Recall'],
      datasets: [{
        label: 'Skor RAGAS',
        data: [
          data.faithfulness || 0,
          data.answer_relevancy || 0,
          data.context_precision || 0,
          data.context_recall || 0
        ],
        backgroundColor: 'rgba(123, 45, 45, 0.2)',
        borderColor: '#7B2D2D',
        pointBackgroundColor: '#7B2D2D'
      }]
    },
    options: {
      scales: {
        r: { min: 0, max: 1 }
      }
    }
  });
}
