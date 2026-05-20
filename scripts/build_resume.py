#!/usr/bin/env python3
import re
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic import ConfigDict

ROOT = Path(__file__).parent.parent
LATEX_DIR = ROOT / "data/output/latex"
TEMPLATE_PATH = ROOT / "templates/output/latex/curriculo_template.tex"
DATA_PATH = LATEX_DIR / "resume-data.yml"
BEGIN_DOCUMENT = r"\begin{document}"
END_DOCUMENT = r"\end{document}"


class Period(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    from_: str = Field(alias="from")
    to: str


class Entry(BaseModel):
    company: str
    period: Period
    role: str
    url: str
    bullets: list[str]


class Personal(BaseModel):
    name: str
    title: str
    email: str
    linkedin_url: str
    github_url: str


class SkillGroup(BaseModel):
    label: str
    items: str


class Education(BaseModel):
    institution: str
    period: Period
    degree: str
    location: str


class ResumeData(BaseModel):
    personal: Personal
    experience: list[Entry]
    projects: list[Entry]
    skills: list[SkillGroup]
    education: list[Education]
    output_filename: str

    @field_validator("output_filename")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        if not re.match(r"^[A-Za-z0-9_-]+$", v):
            raise ValueError("output_filename must only contain letters, digits, _ or -")
        return v


def url_to_display(url: str) -> str:
    return re.sub(r"^https?://", "", url)


def url_to_domain(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    parts = hostname.split(".")
    min_parts = 3 if re.search(r"\.(com|org|net|gov|edu)\.[a-z]{2}$", hostname) else 2
    return ".".join(parts[-min_parts:]) if len(parts) > min_parts else hostname


def rich_to_latex(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"_(.+?)_", r"\\textit{\1}", text)
    return text


def get_nested(obj: object, key: str) -> object:
    for part in key.strip().split("."):
        if isinstance(obj, dict):
            obj = obj.get(part)
        else:
            return None
    return obj


def val(ctx: dict, key: str) -> str:
    v = get_nested(ctx, key)
    return "" if v is None else str(v)


def render(template: str, ctx: dict) -> str:
    def repl_cond(m: re.Match) -> str:
        key, block = m.group(1), m.group(2)
        v = get_nested(ctx, key)
        truthy = len(v) > 0 if isinstance(v, (list, dict)) else bool(v)
        return render(block, ctx) if truthy else ""

    def repl_loop(m: re.Match) -> str:
        key, block = m.group(1), m.group(2)
        items = get_nested(ctx, key)
        if not isinstance(items, list):
            return ""
        parts = []
        for item in items:
            if isinstance(item, str):
                parts.append(block.replace("{{.}}", item))
            elif isinstance(item, dict):
                parts.append(render(block, {**ctx, **item}))
        return "".join(parts)

    template = re.sub(r"\{\{\?(\w+)\}\}([\s\S]*?)\{\{\?/\1\}\}", repl_cond, template)
    template = re.sub(r"\{\{#(\w+)\}\}([\s\S]*?)\{\{/\1\}\}", repl_loop, template)
    template = re.sub(r"\{\{\{([^}]+)\}\}\}", lambda m: "{" + val(ctx, m.group(1)) + "}", template)
    template = re.sub(r"\{\{([^#/?{][^}]*)\}\}", lambda m: val(ctx, m.group(1)), template)
    return template


def build_context(data: ResumeData) -> dict:
    def map_entry(entry: Entry) -> dict:
        return {
            "company": entry.company,
            "role": entry.role,
            "url": entry.url,
            "period": f"{entry.period.from_} -- {entry.period.to}",
            "domain": url_to_domain(entry.url),
            "bullets": [rich_to_latex(b) for b in entry.bullets],
        }

    return {
        "personal": {
            "name": data.personal.name,
            "title": data.personal.title,
            "email": data.personal.email,
            "linkedin_url": data.personal.linkedin_url,
            "github_url": data.personal.github_url,
            "linkedin_display": url_to_display(data.personal.linkedin_url),
            "github_display": url_to_display(data.personal.github_url),
        },
        "experience": [map_entry(e) for e in data.experience],
        "projects": [map_entry(e) for e in data.projects],
        "skills": [{"label": s.label, "items": s.items} for s in data.skills],
        "education": [
            {
                "institution": e.institution,
                "degree": e.degree,
                "location": e.location,
                "period": f"{e.period.from_} -- {e.period.to}",
            }
            for e in data.education
        ],
        "output_filename": data.output_filename,
    }


def main() -> None:
    raw = yaml.safe_load(DATA_PATH.read_text())
    try:
        data = ResumeData.model_validate(raw)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    template = TEMPLATE_PATH.read_text()
    begin_pos = template.index(BEGIN_DOCUMENT)
    end_pos = template.index(END_DOCUMENT)

    ctx = build_context(data)
    body = render(template[begin_pos + len(BEGIN_DOCUMENT) : end_pos], ctx)
    tex = template[:begin_pos] + BEGIN_DOCUMENT + body + END_DOCUMENT + "\n"

    output_name = data.output_filename
    tex_path = LATEX_DIR / f"{output_name}.tex"
    pdf_path = LATEX_DIR / f"{output_name}.pdf"

    tex_path.write_text(tex)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(LATEX_DIR), str(tex_path)],
    )

    if result.returncode != 0 and not pdf_path.exists():
        sys.exit(1)

    if not pdf_path.exists():
        print(f"PDF nao gerado: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    for ext in ("aux", "log", "out"):
        (LATEX_DIR / f"{output_name}.{ext}").unlink(missing_ok=True)

    print(f"PDF gerado: {pdf_path}")


if __name__ == "__main__":
    main()
