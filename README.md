# Tega — Adaptive Learning Companion (static prototype)

This is a lightweight, single‑page HTML/CSS/JS prototype of the UI screens shown in the mockups:

- Landing page with three role cards
- Sign‑up form (name, optional email, password)
- 4‑question personalization quiz with progress and selectable options

## How to run

No build step is required.

1. Open the `index.html` file in your browser.
2. Click a role to proceed to sign‑up. After filling the form, continue to the quiz.

## Files

- `index.html` — markup for three screens.
- `styles.css` — responsive styles, gradients, cards, buttons, and quiz components.
- `app.js` — simple SPA routing + quiz logic and basic form validation.

## Notes

- All assets are emoji/HTML/CSS, no external images required. A Google Font (Poppins) is loaded for better typography.
- The quiz stores answers in memory only (no backend). On completion, a summary is rendered with your selected choices.

Feel free to tweak the palette in `:root` CSS variables and the `questions`/`choices` arrays in `app.js`.