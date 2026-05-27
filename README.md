# Resume Manager

> Build professional LaTeX/PDF resumes from YAML files — no local setup required.

Push your YAML → GitHub Actions compiles → PDF artifact ready to download.

![Resume preview](docs/preview.png)

---

## Quick Start

1. [**Use this template**](../../generate) → create a **private** repository
2. Copy an example resume file:
   ```bash
   cp resumes/resume-en.example.yml resumes/resume-en.yml
   ```
3. Edit `resumes/resume-en.yml` with your information
4. Push to `main` → **Actions** tab → download your PDF

> **Keep your repository private.** Resume files contain personal contact information.

---

## How It Works

```
resumes/*.yml  +  template.tex  →  .github/build.py  →  PDF artifact
```

The build script validates your YAML, renders the LaTeX template, and hands the `.tex` off to [xu-cheng/latex-action](https://github.com/xu-cheng/latex-action) for compilation — all in CI, nothing to install locally.

---

## Repository Structure

```
resumes/
  resume-en.example.yml     English example — copy and edit
  resume-ptbr.example.yml   Portuguese example — copy and edit
template.tex                LaTeX layout — edit to change the design
.github/
  build.py                  Build script (YAML → TEX)
  workflows/build.yml       CI pipeline
```

---

## Multiple Resumes

Every `*.yml` file inside `resumes/` (except `*.example.yml`) is compiled automatically on push:

```
resumes/resume-en.yml    →  resume_your_name_en.pdf
resumes/resume-ptbr.yml  →  curriculo_seu_nome_ptbr.pdf
```

---

## YAML Reference

See [`resumes/resume-en.example.yml`](resumes/resume-en.example.yml) for the full schema.

**Available fonts:** `lmodern` · `charter` · `cormorant` · `fira-sans` · `source-sans`

**Bullet formatting:**

| Marker | Output |
|--------|--------|
| `**text**` | **bold** |
| `_text_` | _italic_ |

Set `projects: []` to hide the projects section entirely.

---

## Customizing the Layout

Edit `template.tex` to change margins, colors, fonts, or section order. The template uses plain LaTeX — no framework, no build tooling.

---

## Running Locally

Requires Python 3.10+ and `pdflatex`.

```bash
pip install pyyaml
python3 .github/build.py
```

---

## License

MIT
