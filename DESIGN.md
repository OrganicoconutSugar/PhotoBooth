# Design System & UI/UX Guidelines — Photobooth App

Dokumen ini menjadi acuan tampilan agar aplikasi terasa seperti photobooth kecil yang hangat, jelas, dan mudah dipakai.

## Prinsip Utama
All UI changes must adhere to these global standards:
1.  **Contrast Ratio**: Minimum 4.5:1 for all text against background.
2.  **Affordance**: Every clickable element MUST have `cursor-pointer`.
3.  **Consistency**: Use the Master + Overrides pattern. Global styles in `base.html`, page-specific overrides in `{% block extra_styles %}`.
4.  **Feedback**: Every interaction (button click, form submit) must have a visual or haptic-like response (scaling, color shift).
5.  **Natural Tone**: Gunakan bahasa manusia yang langsung menjelaskan aksi, bukan istilah futuristik yang terasa seperti template.
6.  **Local Assets First**: Gunakan gambar dari `static/assets/` untuk visual reusable agar mudah diperbarui tanpa mengubah template.

## Visual Specification

### 1. Design Style: "Warm Studio"
Tampilan memakai foto studio lokal sebagai jangkar visual, dengan panel sederhana yang menjaga konten tetap terbaca.
- **Layout**: Gunakan grid rapi untuk kamera, galeri, dan status.
- **Effects**: Pakai blur dan shadow secukupnya. Hindari dekorasi yang tidak membantu pengguna mengambil atau mengelola foto.

### 2. Color Palette
| Element | Dark Mode (Primary) | Light Mode (Primary) | Role |
| :--- | :--- | :--- | :--- |
| **Background** | Foto studio + overlay gelap | Foto studio + overlay terang | Base Canvas |
| **Surface** | `rgba(18,16,18,0.78)` | `rgba(255,250,247,0.82)` | Glass Containers |
| **Accent** | `#d43f3a` | `#b8322f` | Primary Action / Highlights |
| **Text Primary** | `#f8f1ee` | `#201918` | Main Readability |
| **Text Muted** | `rgba(248,241,238,0.72)` | `rgba(32,25,24,0.66)` | Secondary Info |

### 3. Typography
- **Primary Font**: `Plus Jakarta Sans` (via Google Fonts).
- **Headings**: Weight 800, tight tracking, uppercase for small labels.
- **Body**: Weight 400, generous line-height for readability.

## Implementation Checklist
- [ ] Contrast check (WCAG AA).
- [ ] `cursor-pointer` on all buttons/links.
- [ ] Mobile responsiveness verified (grids stack correctly).
- [ ] Transition/Animation consistency (GSAP or CSS ease-in-out).
- [ ] Dark/Light theme synchronization.
- [ ] Toggle theme berada di pojok kanan atas website, di luar navbar.
- [ ] Visual fallback memakai raster image dari `static/assets/`, bukan SVG.
