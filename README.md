# Resume Manager

GitHub template repository for building LaTeX/PDF resumes from YAML — no local setup required.

Push your YAML → GitHub Actions compiles → PDF available as artifact.

## Quick Start

1. Click **"Use this template"** → create a **private** repository
2. Copy an example and rename it:
   ```bash
   cp resume-en.example.yml resume-en.yml
   ```
3. Edit `resume-en.yml` with your information
4. Push to `main` → **Actions** tab → download the PDF artifact

> **Keep your repo private.** Resume files contain personal contact information.

## How It Works

The build logic lives entirely in `.github/workflows/build.yml`. The workflow:
1. Installs LaTeX
2. Finds all `*.yml` files in the repo root (ignores `*.example.yml`)
3. Validates each file, renders `template.tex`, compiles a PDF
4. Uploads PDFs as artifacts (90-day retention)

No build script to maintain — just YAML and a template.

## Multiple Resumes

Any `*.yml` file in the root (except `*.example.yml`) is built automatically:

```
resume-en.yml   →  resume_your_name_en.pdf
resume-pt.yml   →  resume_seu_nome_pt.pdf
```

## YAML Schema

```yaml
personal:
  name: Your Name
  title: Your Title
  email: your@email.com
  linkedin_url: https://linkedin.com/in/your-username
  github_url: https://github.com/your-username

font: lmodern  # lmodern | charter | cormorant | fira-sans | source-sans

section_titles:
  experience: Experience
  projects: Projects
  education: Education
  skills: Technical Skills

experience:
  - company: Company Name
    period: { from: Jan 2023, to: Present }
    role: Your Role
    url: https://company.com
    bullets:
      - Built something with **bold** and _italic_ markers.

projects: []  # set to [] to hide the section

skills:
  - label: Backend
    items: TypeScript, Node.js, PostgreSQL

education:
  - institution: University Name
    period: { from: Jan 2020, to: Dec 2024 }
    degree: Bachelor of Science in Computer Science
    location: City, State

output_filename: resume_your_name  # letters, digits, _ and - only
```

## Customizing the Layout

Edit `template.tex` to change margins, fonts, or section order.

## License

MIT
