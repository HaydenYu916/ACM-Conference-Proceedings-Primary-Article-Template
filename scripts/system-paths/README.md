# Figure 1 (images/system-paths.pdf)

Concept figure: (a) image offloading, (b) split inference, (c) policy-aligned feature streaming.

- `make_figure.py OUT.html thumbs.json` writes the HTML artboard (1504 x 464 px).
  `thumbs.json` holds the three RoboCasa camera views (episode 165, upload 18; from `paper_fig1/heat_fig1.npz`).
- `mkprint.py FONTDIR` swaps the Google-Fonts link for static Source Sans 3 files
  (npm `@fontsource/source-sans-3`) so the PDF embeds TrueType fonts, not Type 3 (ACM TAPS rejects Type 3).
- `node pdf.js print.html images/system-paths.pdf` exports the vector PDF with Playwright/Chromium.
- Colours: yellow = image codec, pink = vision encoder, orange = frozen VLA policy, blue = ours.
