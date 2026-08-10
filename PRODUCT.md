# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- **Primary Users**: Civitas akademika Universitas Sam Ratulangi (UNSRAT), including students, lecturers, and academic staff seeking precise information about academic regulations, calendars, and institutional profile.
- **Secondary Users**: Researchers and evaluators (such as the developer/reviewer) who use the standalone `/evaluation` dashboard to analyze RAGAS metrics (Faithfulness, Answer Relevancy, Context Precision, Context Recall), Wilcoxon signed-rank tests, and audit logs.

## Product Purpose
A high-precision RAG (Retrieval-Augmented Generation) chatbot system designed to answer academic queries with high accuracy, backed by official university documents (such as Peraturan Rektor UNSRAT No. 01 Tahun 2025). The application provides a dual experience: an interactive floating modal chatbot on the replica UNSRAT homepage (`/`) and a standalone evaluation dashboard (`/evaluation`).

## Positioning
An institutional AI academic assistant that grounds all answers in authoritative UNSRAT regulations with inline citations and a expandable side-by-side document evidence panel, distinguishing it from general ungrounded chatbots.

## Operating Context
- Scraped replica UNSRAT homepage (`unsrat-ac-id.html`) running on port 8501.
- Dual modal modes: Compact (`420px x 580px` floating bottom-right) and Fullscreen Expanded (`95vw x 92vh` centered overlay).
- Real-time SSE streaming API (`POST /api/chat`) with single submit/stop entry-point and amber abort warning handling.

## Capabilities and Constraints
- **Capabilities**: Auto-submitting Quick-Question Chips, auto-growing input textarea (`max-height: 120px`), floating dropdown settings switcher (Config B / Gemini 3.5 Flash), responsive side-by-side (desktop) & overlay sheet (mobile) citation accordion, standalone RAGAS evaluation page.
- **Constraints**: Scoped `.rag-*` styling to prevent Tailwind/WordPress preflight CSS conflicts with UNSRAT homepage template; zero emojis (100% Lucide SVG icons); Google Inter typography stack.

## Brand Commitments
- **Voice & Tone**: Professional, helpful, academically precise, and authoritative.
- **Visual Identity**: Warm, dignified, and traditional yet clean. Anchored by official Maroon Klasik UNSRAT theme (`#7B2D2D` primary, `#FAF9F6` neutral warm background, `#E4DFD9` borders).
- **Keywords**: Authoritative, Trustworthy, Clean, Seamless.

## Evidence on Hand
- Peraturan Rektor Universitas Sam Ratulangi Nomor 01 Tahun 2025 Tentang Peraturan Akademik.
- Scraped UNSRAT homepage HTML (`unsrat-ac-id.html`) and official logo (`static/assets/logo-unsrat.png`).

## Product Principles
1. **Academic Authority**: The visual styling must command trust. Typography uses Google Inter with distinct weight contrasts and intentional spacing.
2. **Accountability & Integrity**: Answers map directly to source citations with inline badges `[1]` and an expandable side-by-side document evidence panel.
3. **Zero Interruption & High Performance**: Transitions between Compact and Expanded mode are smooth (`0.25s ease-out`) with zero backdrop lag or double scrollbars.

## Accessibility & Inclusion
- **High Contrast**: Text contrast maintains WCAG AA standard against background.
- **Motion Refinement**: Transitions support reduced motion preferences with instant or smooth crossfades.
- **Responsive Layout**: Dynamic viewport units (`dvh`) prevent mobile soft keyboard overlap.
