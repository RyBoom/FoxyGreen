# Foxy Green Home Services: Sticky Mule spec pitch

Live concept: https://foxygreen.stickymule.com (Worker `foxygreen-concept`, backup https://foxygreen-concept.white-mode-9816.workers.dev/)

- `src/index.html` + `src/assets/`: editable source
- `scripts/build.py`: inlines images into `dist/foxygreen-concept.html` (one self-contained file)
- `proposal/`: one-page proposal (HTML source + PDF)

## Swapping in his real before and after photos

Gallery photos in `src/assets/work/` are Unsplash samples. Replace them with his photos under the same names
(WebP, before and after cropped to the same frame):

| Slot | Files | Size |
|---|---|---|
| Featured (16:9) | `kitchen-before.webp`, `kitchen-after.webp` | 1600x900 |
| Small (4:3) | `bath-*`, `halfbath-*`, `backsplash-*` | 960x720 |
| Hero | `hero-after.webp` (920x1069), `hero-before.webp` (440x330) | |

Then update the captions and alt text in `src/index.html`, and remove the "Concept note" pill and the
"Gallery photos are samples" line once every photo is his.

## Update the live page

    python3 scripts/build.py
    python3 <sticky-mule-website skill>/scripts/deploy_pitch.py dist/foxygreen-concept.html foxygreen-concept
