# Filippo Masi — Quarto Academic Pages layout

This project reproduces the Academic Pages/Jeremy Bleyer-style layout in Quarto: the same top navigation, persistent author profile, proportions, colour palette, and no right-side “On this page” panel.

## Preview locally

```bash
cd filippo-quarto-academicpages
quarto preview
```

The project automatically runs:

```bash
python3 tools/build_bibliography.py
```

before each Quarto render. This generates the visible lists and video cards from the BibTeX files.

## Eclipse

Use **File → Import → General → Existing Projects into Workspace** and choose this directory. The `.project` file is included.

## Bibliography-driven content

- `bibliography/publications.bib`: journal articles and book chapters.
- `bibliography/conferences.bib`: reviewed conferences, national conferences, posters, and conference communications.
- `bibliography/talks.bib`: recorded talks and lectures. Add the YouTube video ID using `youtube = {VIDEO_ID}`.
- `tools/build_bibliography.py`: dependency-free generator.
- `generated/`: generated Markdown; do not edit these files directly.

After editing a `.bib` file, Quarto normally regenerates the page automatically. You can also run the generator manually:

```bash
python3 tools/build_bibliography.py
```

## Main site files

- `_quarto.yml`: navigation and Quarto settings.
- `assets/css/academic-pages.scss`: layout, palette, bibliography styling, and video cards.
- `_profile.qmd`: author panel shown on each page.
- `index.qmd`: homepage.
- `research.qmd`, `publications.qmd`, `conferences.qmd`, `talks.qmd`, `teaching.qmd`, `software.qmd`, `contact.qmd`: main pages.
- `files/FM_CV.pdf`: current PDF from the previous website.

## Items to update

1. Replace `filippo.masi@sydney.edu.au` in `_profile.qmd` and `contact.qmd` when appropriate.
2. Replace the PDF CV when the current version is ready.
3. Verify the final details of entries still marked “in press” in the original website.
4. Add recent publications and conference contributions to the BibTeX files.

## YouTube embed implementation

The generated Talks page wraps its card markup in a Pandoc raw HTML block. This prevents the indented `<iframe>` elements from being interpreted as Markdown code blocks. Edit `bibliography/talks.bib`; the pre-render script regenerates `generated/talks.md` automatically.
