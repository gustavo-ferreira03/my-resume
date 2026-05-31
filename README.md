# my-resume

Personal resume repository built from YAML with Typst.

Resume content lives in `resumes/*.yml`; generated PDFs are written to `build/`.

## Build Locally

Install the local tooling:

```bash
make setup
```

Build all resumes:

```bash
make build
```

Build one resume:

```bash
make build ARGS="resumes/gustavo_cosme_fullstackdev_en.yml"
```

Watch while editing:

```bash
make watch
```

## Resume Files

```text
resumes/gustavo_cosme_fullstackdev_en.yml  -> build/resume_gustavo_cosme_fullstack_en.pdf
resumes/gustavo_cosme_fullstackdev_pt.yml  -> build/curriculo_gustavo_cosme_fullstack_ptbr.pdf
```

## YAML Structure

Build and presentation settings live under `meta`:

```yaml
meta:
  template: default
  font: New Computer Modern
  output_filename: resume_gustavo_cosme_fullstack_en
  section_titles:
    experience: Professional Experience
    projects: Projects
    education: Education
    skills: Skills
```

Main content sections:

```yaml
personal:
  name: Gustavo Ferreira Cosme
  title: Mid-Level Full Stack Developer
  email: gustavo.ferreiracosme03@gmail.com

experience: []
projects: []
certifications: []
education: []
skills: []
```

Use `[]` to hide a list-backed section.

## Templates

Templates are single Typst files in `templates/`:

```text
templates/default.typ
```

Set the template in YAML with `meta.template`, without the `.typ` extension.

## GitHub Actions

The workflow builds PDFs on pushes to `main` when resume, template, or builder files change.

On push, generated PDFs are uploaded as workflow artifacts. On manual workflow runs, the workflow also creates a GitHub Release with the generated PDFs.
