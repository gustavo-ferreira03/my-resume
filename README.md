# resume-ci

Build PDF resumes from YAML. Write your resume once, push to GitHub, and download the PDF from Releases.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`resume-ci` is for people who want a clean LaTeX resume without having to install complex dependencies. Your content lives in `resumes/*.yml`. The design lives in `template.tex`. GitHub Actions does the build.

## What You Get

- Resume content in plain YAML
- One LaTeX template for the design
- Automatic builds for every `.yml` file in `resumes/`
- English, Spanish, and Portuguese (BR) examples
- Text-extractable PDFs that work better with ATS parsers

## Quick Start

For a public repo, [fork this repository](../../fork).

For a private repo, create an empty private repository on GitHub, then run:

```bash
git clone https://github.com/gustavo-ferreira03/resume-ci.git
cd resume-ci
git remote rename origin upstream
git remote add origin https://github.com/YOUR_USERNAME/YOUR_PRIVATE_REPO.git
git push -u origin main
```

Then add your resume:

```bash
cp resumes/resume-en.example.yml resumes/resume-en.yml
```

Edit `resumes/resume-en.yml`, push to `main`, and download the PDF from the Releases tab.

## Pulling Updates

When this template changes, pull the latest version into your repo:

```bash
git fetch upstream
git merge upstream/main
```

Your own resume files should not conflict with upstream changes unless you edit the same example files or template files.

## How It Works

```text
resumes/*.yml + template.tex
        |
        v
.github/resume_ci.py  validates YAML and writes build/*.tex
        |
        v
xu-cheng/latex-action  compiles build/*.tex to PDF
        |
        v
GitHub Releases        publishes each PDF as a downloadable asset
```

The workflow validates each resume file, renders a `.tex` file into `build/`, and compiles it inside a TeX Live Docker image.

You do not need a local TeX install. You do not need `apt-get install texlive` in the workflow.

## Repository Structure

```text
resumes/
  resume-en.example.yml       English example
  resume-es.example.yml       Spanish example
  resume-ptbr.example.yml     Portuguese (BR) example
template.tex                  LaTeX layout
.github/
  workflows/build.yml         GitHub Actions workflow
  resume_ci.py                YAML to TEX builder
```

## Multiple Resumes

Add one YAML file per version. The workflow compiles every `*.yml` file in `resumes/`.

```text
resumes/resume-en.yml    ->  resume_your_name_en.pdf
resumes/resume-es.yml    ->  curriculum_su_nombre_es.pdf
resumes/resume-ptbr.yml  ->  curriculo_seu_nome_ptbr.pdf
```

Use separate files for languages, job targets, or resume lengths. Each file builds on its own.

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
python3 .github/resume_ci.py
```

Generated PDFs are written to `build/`.
