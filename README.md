# Foxy Green Home Services: Sticky Mule spec pitch

Live concept: https://foxygreen.stickymule.com (Worker `foxygreen-concept`, backup https://foxygreen-concept.white-mode-9816.workers.dev/)

- `src/index.html` + `src/assets/`: editable source
- `scripts/build.py`: inlines images into `dist/foxygreen-concept.html` (one self-contained file)
- `proposal/`: one-page proposal (HTML source + PDF)

Update the live page:

    python3 scripts/build.py
    python3 <sticky-mule-website skill>/scripts/deploy_pitch.py dist/foxygreen-concept.html foxygreen-concept
