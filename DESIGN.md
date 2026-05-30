# 🎨 Design System & UI/UX Guidelines — Photobooth App

This document serves as the **Master Design Reference** for the project, implementing the principles from the `UI-UX Pro Max Skill`.

## 🛠️ Core Principles (UI-UX Pro Max)
All UI changes must adhere to these global standards:
1.  **Contrast Ratio**: Minimum 4.5:1 for all text against background.
2.  **Affordance**: Every clickable element MUST have `cursor-pointer`.
3.  **Consistency**: Use the Master + Overrides pattern. Global styles in `base.html`, page-specific overrides in `{% block extra_styles %}`.
4.  **Feedback**: Every interaction (button click, form submit) must have a visual or haptic-like response (scaling, color shift).
5.  **Avoid Anti-patterns**: No confusing navigation, no hidden critical actions, and no over-use of decorative elements that block content.

## 🎨 Visual Specification

### 1. Design Style: "Neon-Glass Bento"
A fusion of **Bento Box Grid** for layout and **Glassmorphism** for elements.
- **Layout**: Use grid-based containers with varied sizes (Bento style) to organize information.
- **Effects**: Heavy use of `backdrop-blur`, subtle white/black borders (1px), and soft glows.

### 2. Color Palette (Vibrant & Professional)
| Element | Dark Mode (Primary) | Light Mode (Primary) | Role |
| :--- | :--- | :--- | :--- |
| **Background** | `#09090b` (Zinc-950) | `#f4f4f5` (Zinc-100) | Base Canvas |
| **Surface** | `rgba(255,255,255,0.03)` | `rgba(0,0,0,0.03)` | Glass Containers |
| **Accent 1** | `#C084FC` (Purple-400) | `#A855F7` (Purple-500) | Primary Action / Highlights |
| **Accent 2** | `#22D3EE` (Cyan-400) | `#0891B2` (Cyan-600) | Secondary Action / Info |
| **Text Primary** | `#f4f4f5` (Zinc-100) | `#09090b` (Zinc-950) | Main Readability |
| **Text Muted** | `#71717a` (Zinc-400) | `#52525b` (Zinc-600) | Secondary Info |

### 3. Typography
- **Primary Font**: `Plus Jakarta Sans` (via Google Fonts).
- **Headings**: Weight 800, tight tracking, uppercase for small labels.
- **Body**: Weight 400, generous line-height for readability.

## 📐 Implementation Checklist (Pre-Delivery)
- [ ] Contrast check (WCAG AA).
- [ ] `cursor-pointer` on all buttons/links.
- [ ] Mobile responsiveness verified (Bento grids stack correctly).
- [ ] Transition/Animation consistency (GSAP or CSS ease-in-out).
- [ ] Dark/Light theme synchronization.
