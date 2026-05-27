# resume-ci

Build PDF resumes from YAML. Edit the content, push to GitHub, and download the finished PDF from Releases.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is for people who want a clean LaTeX resume without installing LaTeX. Your resume data stays in `resumes/*.yml`. The layout stays in `template.tex`. GitHub Actions handles the compile step.

## What You Get

- Resume content in plain YAML
- One LaTeX template for the whole design
- Automatic builds for every `.yml` file in `resumes/`
- English, Spanish, and Portuguese (BR) examples
- Text-extractable PDFs that work better with ATS parsers

## Quick Start

1. Create a new **private** repository on GitHub (do not initialize it).
2. Clone and rewire this repo to your private one:

   ```bash
   git clone https://github.com/gustavo-ferreira03/resume-ci.git
   cd resume-ci
   git remote rename origin upstream
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_PRIVATE_REPO.git
   git push -u origin main
   ```

3. Copy an example file and edit it with your details:

   ```bash
   cp resumes/resume-en.example.yml resumes/resume-en.yml
   ```

4. Push to `main`.
5. Go to the **Releases** tab and download your PDF.

> [!IMPORTANT]
> Keep your repository **private**. Resume files contain personal contact information.

## Pulling Upstream Updates

When the template or workflow is improved, sync your repository:

```bash
git fetch upstream
git merge upstream/main
```

Your files in `resumes/` are not part of this repository, so merges will be conflict-free.

## How It Works

```text
resumes/*.yml + template.tex
        |
        v
.github/build.py       validates YAML and writes build/*.tex
        |
        v
xu-cheng/latex-action  compiles build/*.tex to PDF
        |
        v
GitHub Releases        publishes each PDF as a downloadable asset
```

The workflow runs in two steps. First, `.github/build.py` validates each resume file and renders a `.tex` file into `build/`. Then `xu-cheng/latex-action` compiles those `.tex` files inside a TeX Live Docker image.

You do not need to install TeX locally or add `apt-get install texlive` to the workflow.

## Repository Structure

```text
resumes/
  resume-en.example.yml       English example
  resume-es.example.yml       Spanish example
  resume-ptbr.example.yml     Portuguese (BR) example
template.tex                  LaTeX layout
.github/
  build.py                    YAML to TEX builder
  workflows/build.yml         GitHub Actions workflow
```

## Multiple Resumes

Add one YAML file per version. The workflow compiles every `*.yml` file in `resumes/`.

```text
resumes/resume-en.yml    ->  resume_your_name_en.pdf
resumes/resume-es.yml    ->  curriculum_su_nombre_es.pdf
resumes/resume-ptbr.yml  ->  curriculo_seu_nome_ptbr.pdf
```

Use this for different languages, job targets, or resume lengths. Each file builds on its own.

## YAML Reference

Start with one of the example files in [`resumes/`](resumes/). These are the main fields:

| Field | What it controls |
|---|---|
| `personal` | Name, title, email, LinkedIn URL, and GitHub URL |
| `font` | One of `lmodern`, `charter`, `cormorant`, `fira-sans`, or `source-sans` |
| `section_titles` | Section labels, useful for non-English resumes |
| `experience` | Roles with company, period, URL, and bullets |
| `projects` | Same shape as `experience`; set it to `[]` to hide the section |
| `education` | Institution, degree, location, and period |
| `skills` | List of `label` and `items` pairs |
| `output_filename` | PDF file name without the `.pdf` extension |

Use only letters, digits, `_`, and `-` in `output_filename`.

## Bullet Formatting

The builder supports two Markdown-style markers inside resume bullets:

| Marker | PDF output |
|---|---|
| `**text**` | bold text |
| `_text_` | italic text |

## Customizing The Layout

Edit `template.tex` to change margins, colors, font sizes, or section order.

The template uses simple `{{placeholder}}` tags. There is no template framework to learn.

## Running Locally

Local builds need Python 3.10+ and a LaTeX distribution with `pdflatex`, such as TeX Live or MiKTeX.

```bash
pip install pyyaml
python3 .github/build.py
```

Generated PDFs are written to `build/`.
