# Watchdog Timer Removal and Abort Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the 30-second client-side watchdog timer from the RAG UI and fix the bug where \"Aliran jawaban dihentikan oleh pengguna\" false-positively appears after normal completion.

**Architecture:** We will introduce a global state flag `isUserAborted` in the UI controller script (`static/js/app.js`) to track whether an abort is explicitly user-initiated. Then, we will remove all references to the watchdog timer and adjust the `AbortError` catch block to only render stop alerts if `isUserAborted` is true.

**Tech Stack:** JavaScript (ES6), HTML5 (SSE)

---

### Task 1: Introduce `isUserAborted` State and Event Listeners

**Files:**
- Modify: `static/js/app.js:20-25` (State definition)
- Modify: `static/js/app.js:345-365` (Click and submit abort events)
- Modify: `static/js/app.js:370-380` (Initialize query send)

- [ ] **Step 1.1: Add `isUserAborted` state variable**
  Add the variable `let isUserAborted = false;` under state management.
  ```javascript
      // ── STATE MANAGEMENT ───────────────────────────────────────────────────────
      let chatHistory = [];
      let isStreaming = false;
      let abortController = null;
      let metricsChartInstance = null;
      let isUserAborted = false;
  ```

- [ ] **Step 1.2: Set `isUserAborted` to true on user abort clicks**
  In the `sendBtn` click listener and `chatForm` submit listener, set `isUserAborted = true` before aborting.
  ```javascript
      if (sendBtn) {
          sendBtn.addEventListener("click", (e) => {
              if (isStreaming) {
                  e.preventDefault();
                  isUserAborted = true;
                  handleAbort();
              }
          });
      }
  
      if (chatForm) {
          chatForm.addEventListener("submit", async (e) => {
              e.preventDefault();
              
              if (isStreaming) {
                  isUserAborted = true;
                  handleAbort();
                  return;
              }
  ```

- [ ] **Step 1.3: Reset `isUserAborted` on new message submission**
  Inside the `chatForm` submit handler (around line 372), set `isUserAborted = false` when starting a new stream request.
  ```javascript
              const query = chatInput.value.trim();
              if (!query) return;
              
              isUserAborted = false;
              // Clean input
              chatInput.value = "";
  ```

- [ ] **Step 1.4: Commit Task 1**
  ```bash
  git add static/js/app.js
  git commit -m "feat: introduce isUserAborted state and hook abort events"
  ```

---

### Task 2: Remove watchdogTimer Logic

**Files:**
- Modify: `static/js/app.js:455-470` (Watchdog definition)
- Modify: `static/js/app.js:510-530` (First token handler)
- Modify: `static/js/app.js:570-590` (Buffer processor)
- Modify: `static/js/app.js:640-660` (Finally block)

- [ ] **Step 2.1: Delete `watchdogTimer` initialization**
  Remove the `setTimeout` watchdog block completely.
  ```javascript
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
              
              let isFirstToken = true;
              let fullResponseText = "";
  ```

- [ ] **Step 2.2: Delete `clearTimeout(watchdogTimer)` from the token event handler**
  Remove `clearTimeout(watchdogTimer);` inside `if (isFirstToken)`.
  ```javascript
                              if (event.type === "token") {
                                  if (isFirstToken) {
                                      isFirstToken = false;
                                      clearInterval(thinkingInterval);
  ```

- [ ] **Step 2.3: Delete `clearTimeout(watchdogTimer)` from the buffer event handler**
  Remove `clearTimeout(watchdogTimer);` inside `if (isFirstToken)` of the buffer leftover handler.
  ```javascript
                                  if (event.type === "token") {
                                      if (isFirstToken) {
                                          isFirstToken = false;
                                          clearInterval(thinkingInterval);
  ```

- [ ] **Step 2.4: Delete `clearTimeout(watchdogTimer)` from `finally`**
  Remove `clearTimeout(watchdogTimer);` from the `finally` cleanup block.
  ```javascript
              } finally {
                  clearInterval(thinkingInterval);
                  setStreamingState(false);
  ```

- [ ] **Step 2.5: Commit Task 2**
  ```bash
  git add static/js/app.js
  git commit -m "chore: remove watchdogTimer definition and clearances"
  ```

---

### Task 3: Refactor catch Block for `isUserAborted`

**Files:**
- Modify: `static/js/app.js:615-645` (Catch block logic)

- [ ] **Step 3.1: Update AbortError handling conditions**
  Modify the `catch` block to check `isUserAborted` before rendering the stop alerts.
  ```javascript
              } catch (err) {
                  if (err.name === 'AbortError') {
                      const thinkingContainer = document.getElementById(`${botMsgId}-thinking`);
                      if (thinkingContainer) {
                          thinkingContainer.classList.add("hidden");
                      }
                      const contentContainer = document.getElementById(`${botMsgId}-content`);
                      if (contentContainer) {
                          contentContainer.classList.remove("hidden");
                          if (isUserAborted && !isFirstToken && fullResponseText.trim() !== "") {
                              if (typeof marked !== "undefined" && marked.parse) {
                                  contentContainer.innerHTML = marked.parse(fullResponseText) + `<p class="text-amber-700 text-xs italic mt-2.5 font-medium flex items-center"><i data-lucide="info" class="w-3.5 h-3.5 inline mr-1 flex-shrink-0"></i><span>[Aliran jawaban dihentikan oleh pengguna]</span></p>`;
                              } else {
                                  contentContainer.innerHTML = escapeHtml(fullResponseText).replace(/\n/g, "<br>") + `<p class="text-amber-700 text-xs italic mt-2.5 font-medium flex items-center"><i data-lucide="info" class="w-3.5 h-3.5 inline mr-1 flex-shrink-0"></i><span>[Aliran jawaban dihentikan oleh pengguna]</span></p>`;
                              }
                              chatHistory.push({ role: "assistant", content: fullResponseText });
                              safeCreateIcons();
                          } else if (isUserAborted) {
                              contentContainer.innerHTML = `<span class="text-amber-700 font-medium bg-amber-50 border border-amber-150 rounded-xl px-4 py-2 block text-xs">Pencarian dan pembuatan jawaban dihentikan oleh pengguna.</span>`;
                          } else {
                              console.log("[RAG Client] Programmatic done/error abort handled silently.");
                          }
                      }
                      console.log("[RAG Client] Stream request aborted.");
                  } else {
                      console.error("[RAG Client] Stream error:", err);
                      handleError("Terjadi kegagalan komunikasi dengan server RAG.");
                  }
              }
  ```

- [ ] **Step 3.2: Commit Task 3**
  ```bash
  git add static/js/app.js
  git commit -m "fix: make abort warnings conditional on isUserAborted"
  ```

---

### Task 4: Documentation Update and Integration Verification

**Files:**
- Modify: `docs/implementation_status.md`

- [ ] **Step 4.1: Update `docs/implementation_status.md`**
  Add a summary of the watchdog removal and user abort lifecycle fix under Phase 2 in [docs/implementation_status.md](file:///D:/Kuliah/Skripsi%20Repository/unsrat-rag-v4-28.05.2026/docs/implementation_status.md).

- [ ] **Step 4.2: Start the application locally**
  Run: `conda run -n unsrat-rag python app.py`

- [ ] **Step 4.3: Verify normal streaming completion**
  Ask a question in the UI (e.g. "Berapa SKS maksimal semester satu?"). Wait until LLM completes and verify **no** stop message appears.

- [ ] **Step 4.4: Verify manual abort**
  Ask a question, and click the stop button during generation. Verify that the generated text up to the stopped token remains visible and the warning footnote appears.

- [ ] **Step 4.5: Commit Task 4**
  ```bash
  git add docs/implementation_status.md
  git commit -m "docs: document watchdog removal and user abort fix"
  ```
