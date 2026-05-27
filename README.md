# Resume Manager

> Build professional LaTeX/PDF resumes from YAML files — no local setup required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Push your YAML → GitHub Actions compiles → PDF artifact ready to download.

## Features

- **Zero local dependencies** — LaTeX runs entirely in CI via [xu-cheng/latex-action](https://github.com/xu-cheng/latex-action)
- **Data-driven** — resume content lives in plain YAML; the layout is a separate `.tex` template
- **Multi-resume** — every `.yml` file in `resumes/` is compiled automatically on push
- **Multilingual** — comes with English, Spanish, and Portuguese (BR) examples
- **ATS-friendly** — the default template embeds glyph-to-unicode mappings for text extraction

## Quick Start

1. Click [**Use this template**](../../generate) → create a **private** repository

2. Copy an example and rename it:
   ```bash
   cp resumes/resume-en.example.yml resumes/resume-en.yml
   ```

3. Edit `resumes/resume-en.yml` with your information

4. Push to `main` → open the **Actions** tab → download your PDF artifact

> [!IMPORTANT]
> Keep your repository **private**. Resume files contain personal contact information.

## How It Works

```
resumes/*.yml  +  template.tex
       │
       ▼
  .github/build.py          validates YAML, renders template → .tex
       │
       ▼
  xu-cheng/latex-action      compiles .tex → .pdf
       │
       ▼
  GitHub Actions artifact    download from the Actions tab
```

The Python build script runs first and generates intermediate `.tex` files into a `build/` directory. The LaTeX action then compiles them using a pre-built TeX Live Docker image — no `apt-get install texlive` needed.

## Repository Structure

```
resumes/
  resume-en.example.yml       English example
  resume-es.example.yml       Spanish example
  resume-ptbr.example.yml     Portuguese (BR) example
template.tex                  LaTeX layout — edit to change the design
.github/
  build.py                    Build script (YAML → TEX)
  workflows/build.yml         CI pipeline
```

## Multiple Resumes

Every `*.yml` file inside `resumes/` (except `*.example.yml`) is compiled on each push:

```
resumes/resume-en.yml    →  resume_your_name_en.pdf
resumes/resume-es.yml    →  curriculum_su_nombre_es.pdf
resumes/resume-ptbr.yml  →  curriculo_seu_nome_ptbr.pdf
```

> [!TIP]
> Use separate files per language or per job target. Each file compiles independently.

## YAML Reference

See the example files in [`resumes/`](resumes/) for the full schema. Key fields:

| Field | Description |
|---|---|
| `personal` | Name, title, email, LinkedIn and GitHub URLs |
| `font` | `lmodern` · `charter` · `cormorant` · `fira-sans` · `source-sans` |
| `section_titles` | Override section header labels (useful for non-English resumes) |
| `experience` | List of roles with company, period, bullets |
| `projects` | Same structure as experience — set to `[]` to hide |
| `education` | Institution, degree, location, period |
| `skills` | List of `label: items` pairs |
| `output_filename` | PDF file name (letters, digits, `_` and `-` only) |

**Bullet formatting:**

| Marker | Output |
|---|---|
| `**text**` | **bold** |
| `_text_` | _italic_ |

## Customizing the Layout

Edit `template.tex` to change margins, colors, font sizes, or section order. The template is plain LaTeX with a simple `{{placeholder}}` syntax — no framework involved.

## Running Locally

> [!NOTE]
> Local compilation requires Python 3.10+ and a LaTeX distribution with `pdflatex` (e.g. TeX Live or MiKTeX).

```bash
pip install pyyaml
python3 .github/build.py
```

Generated PDFs are written to `build/`.
