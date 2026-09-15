# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Mahasiswa, Dosen, dan Civitas Akademika Universitas Sam Ratulangi yang mengakses Portal INSPIRE UNSRAT (`portal.unsrat.ac.id`) untuk menanyakan informasi regulasi akademik (KRS, Cuti Akademik, Kelulusan, Yudisium, Beban SKS, MBKM, dll.).

## Product Purpose
Asisten AI Akademik terpercaya yang disematkan langsung pada Portal INSPIRE UNSRAT untuk menjawab pertanyaan seputar peraturan rektor dan pedoman akademik secara presisi berbasis RAG (Retrieval-Augmented Generation) berdasar dokumen hukum resmi tanpa halusinasi.

## Positioning
Asisten akademik terintegrasi institusi yang menyediakan grounding regulasi faktual dengan sitasi inline interaktif (`[1]`, `[2]`) dan panel dokumen rujukan side-by-side (desktop) atau native bottom sheet drawer (mobile), membedakannya dari chatbot umum yang tidak memiliki rujukan regulasi terverifikasi.

## Operating Context
- Live Portal INSPIRE homepage (`/`) berjalan di port 8080 dengan background portal akademik mahasiswa (IPK, SKS, KRS, Jadwal Kuliah) dan preservasi mockup legacy UNSRAT homepage (`/unsratacid`).
- Mode Desktop: Compact (`420px x 600px` floating bottom-right dengan margin 36px) dan Fullscreen Expanded (`min(92vw, 1360px) x min(90vh, 900px)` modal terpusat).
- Mode Mobile: Mobile Peek-Through Sheet (`top: calc(env(safe-area-inset-top, 0px) + 54px)`, `border-radius: 20px 20px 0 0`) yang tetap memperlihatkan navbar Portal INSPIRE di bagian atas demi kejelasan demonstrasi dan sidang skripsi.
- SSE real-time streaming API (`POST /api/chat`) dengan single submit/stop lifecycle, auto-scrolling batched rendering (RAF), dan fallback 45s RTO error recovery.

## Capabilities and Constraints
- **Capabilities**: Pre-RAG Intent Routing untuk sapaan dan identitas bot ($\le 5\text{ms}$), topic suggestion pills/cards adaptif, auto-growing input textarea (`max-height: 120px`), floating dropdown settings switcher (Config B / Gemini Flash), interactive inline citations (`[1]`, `[2]`), Option B Borderless Editorial Legal Flow citations dengan fluid breadcrumb (`BAB > Bagian > Pasal`), multi-turn scoped citation sync, tactile micro-nudge animation, mobile swipe-down gesture dismiss, dan dual-snap height expansion ($75\text{vh} \leftrightarrow 95\text{vh}$).
- **Constraints**: Scoped styling `.rag-*` untuk mencegah konflik CSS template portal; zero emojis (100% Lucide SVG icons); Google Inter typography stack; borderless elevation untuk mencegah visual crowding; preservasi 100% untouched pada mockup legacy `/unsratacid`.

## Brand Commitments
- **Voice & Tone**: Profesional, lugas, presisi secara akademik, ramah, dan berwibawa.
- **Visual Identity**: Warm, dignified, dan modern. Berakar pada palet resmi Maroon Klasik UNSRAT (`#7B2D2D` primary, `#FAF9F6` neutral warm background, `#E4DFD9` divider line, ambient multi-stop shadow).
- **Keywords**: Authoritative, Trustworthy, Clean, Seamless, Impeccable.

## Evidence on Hand
- Peraturan Rektor Universitas Sam Ratulangi Nomor 01 Tahun 2025 Tentang Peraturan Akademik.
- Portal INSPIRE UNSRAT template HTML (`static/demo/index.html`) dan logo resmi UNSRAT (`static/assets/logo-unsrat.png`).
- 21 commit terverifikasi pada branch `revisi/migrasi-ui-inspire`.

## Product Principles
1. **Academic Authority & Grounding**: Jawaban selalu berlandaskan dokumen peraturan rektor nyata dengan sitasi inline dan panel bukti yang dapat ditelusuri.
2. **Context-Aware Integration**: Tampilan asisten menyatu secara harmonis dengan Portal INSPIRE tanpa mengaburkan identitas portal kampus (didukung Mobile Peek-Through).
3. **Zero Interruption & Fluid Morphing**: Transisi antar mode (Compact, Expanded, Mobile Sheet) menggunakan interpolasi geometri halus `cubic-bezier(0.16, 1, 0.3, 1)` tanpa lonjakan tata letak yang kaku.
4. **Universal Open/Exit Lifecycle**: Setiap interaksi (modal, settings, reset popover, guide dialog, citation panel) memiliki gestur keluar yang jelas (tombol close, Escape key, swipe-down, click outside).

## Accessibility & Inclusion
- **High Contrast**: Rasio kontras teks memenuhi standar WCAG AA terhadap background hangat.
- **Motion Refinement**: Mendukung preferensi `@media (prefers-reduced-motion: reduce)`.
- **Responsive Ergonomics**: Dynamic viewport units (`100dvh`, `75vh`, `95vh`) dan safe-area insets (`env(safe-area-inset-bottom)`) mencegah tumpang tindih keyboard mobile.
