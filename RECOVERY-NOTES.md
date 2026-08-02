# Recovery notes

This source project was reconstructed from `website.zip`.

Recovered directly from the Quarto cache/build:

- all eight `.qmd` pages from `.quarto/idx/*.qmd.json`;
- generated publications, conference, and talk fragments;
- the complete BibTeX files;
- all published images, logos, and the CV;
- the rendered project metadata used to reconstruct `_quarto.yml`;
- the latest compiled user SCSS rules and variables.

Reconstructed from the rendered HTML and the previous clean source:

- `_profile.qmd`;
- `tools/build_bibliography.py` and `includes/profile-script.html`.

The output folder and Quarto cache are intentionally excluded. Run:

```bash
python3 tools/build_bibliography.py
quarto preview
```

After confirming the result, initialize Git and commit immediately.
