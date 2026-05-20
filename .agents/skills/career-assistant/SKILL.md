---
name: career-assistant
description: Resume manager assistant for maintaining YAML resume data and generating LaTeX/PDF outputs
---

# Resume Manager Assistant

This project is only a resume manager. Keep work focused on the YAML resume data, LaTeX template, and PDF generation pipeline.

## Core Rule

Never edit generated `.tex` files directly.

Edit:

```txt
data/output/latex/resume-data.yml
```

Then run:

```bash
pnpm run build-resume
```

## Files

```txt
data/output/latex/resume-data.yml       Source data
templates/output/latex/curriculo_template.tex  Template
scripts/build-resume.ts                 Renderer/compiler
data/output/latex/[name].tex            Generated
data/output/latex/[name].pdf            Generated
```

## Workflow

1. Read `data/output/latex/resume-data.yml`.
2. Edit YAML content only.
3. Run `pnpm run build-resume`.
4. Confirm the PDF path.

## Schema

```yaml
personal:
  name: string
  title: string
  email: string
  linkedin_url: string
  github_url: string

experience:
  - company: string
    period:
      from: string
      to: string
    role: string
    url: string
    bullets:
      - string

projects: []

skills:
  - label: string
    items: string

education:
  - institution: string
    period:
      from: string
      to: string
    degree: string
    location: string

output_filename: string
```

## Rich Text

Use markers in YAML bullets:

| Marker | Rendered as |
|---|---|
| `**text**` | `\textbf{text}` |
| `_text_` | `\textit{text}` |

Do not write raw LaTeX commands in YAML bullets.

## Writing Quality

For Portuguese resume bullets, use natural Brazilian Portuguese with articles and prepositions. Avoid telegraphic English-style fragments.

Use action verbs in first person implicit past tense, such as `Implementei`, `Desenvolvi`, `Arquitetei`, `Automatizei`, `Integrei`, and `Otimizei`.

Prefer specific achievements, technologies, scale, and measurable impact when the source data supports it.
