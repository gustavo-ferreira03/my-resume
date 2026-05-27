#!/usr/bin/env python3
"""Build one or more YAML resumes into LaTeX and PDF files.

Run from the repo root:
    python3 .github/build.py

YAML files at the repo root are discovered automatically (*.example.yml excluded).
Pass paths explicitly to build specific files only.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("Missing dependency: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


DEFAULT_TEMPLATE = Path.cwd() / "template.tex"
DEFAULT_DATA_DIR = Path.cwd()
BEGIN_DOCUMENT = r"\begin{document}"
END_DOCUMENT = r"\end{document}"

FONT_PACKAGES = {
    "lmodern": r"\usepackage{lmodern}",
    "charter": r"\usepackage{charter}",
    "cormorant": r"\usepackage{CormorantGaramond}",
    "fira-sans": r"\usepackage[sfdefault]{FiraSans}",
    "source-sans": r"\usepackage[default]{sourcesanspro}",
}

DEFAULT_SECTION_TITLES = {
    "experience": "Experience",
    "projects": "Projects",
    "skills": "Technical Skills",
    "education": "Education",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build resume PDFs from YAML files.")
    parser.add_argument("data_paths", nargs="*", type=Path, help="YAML resume files to build")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="LaTeX template path")
    parser.add_argument("--output-dir", type=Path, help="Output directory for .pdf files")
    parser.add_argument("--keep-aux", action="store_true", help="Keep pdflatex aux/log files")
    return parser.parse_args()


def discover_data_paths(explicit_paths: list[Path]) -> list[Path]:
    if explicit_paths:
        return explicit_paths

    found = sorted(
        p for p in DEFAULT_DATA_DIR.glob("*.yml")
        if not p.name.endswith(".example.yml")
    )
    if found:
        return found

    print("No resume YAML files found. Add a .yml file to the repo root.", file=sys.stderr)
    sys.exit(1)


def require_mapping(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a mapping")
    return value


def require_list(value: object, name: str) -> list:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    return value


def require_str(mapping: dict, key: str, path: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}.{key} must be a non-empty string")
    return value


def validate_period(value: object, path: str) -> dict[str, str]:
    period = require_mapping(value, path)
    return {
        "from": require_str(period, "from", path),
        "to": require_str(period, "to", path),
    }


def validate_entry(value: object, path: str) -> dict:
    entry = require_mapping(value, path)
    bullets = require_list(entry.get("bullets"), f"{path}.bullets")
    for index, bullet in enumerate(bullets):
        if not isinstance(bullet, str):
            raise ValueError(f"{path}.bullets[{index}] must be a string")
    return {
        "company": require_str(entry, "company", path),
        "period": validate_period(entry.get("period"), f"{path}.period"),
        "role": require_str(entry, "role", path),
        "url": require_str(entry, "url", path),
        "bullets": bullets,
    }


def validate_resume(raw: object, data_path: Path) -> dict:
    data = require_mapping(raw, str(data_path))
    personal = require_mapping(data.get("personal"), "personal")
    font = data.get("font", "lmodern")
    if font not in FONT_PACKAGES:
        allowed = ", ".join(sorted(FONT_PACKAGES))
        raise ValueError(f"font must be one of: {allowed}")

    output_filename = require_str(data, "output_filename", "resume")
    if not re.match(r"^[A-Za-z0-9_-]+$", output_filename):
        raise ValueError("output_filename must only contain letters, digits, _ or -")

    section_titles = {
        **DEFAULT_SECTION_TITLES,
        **require_mapping(data.get("section_titles", {}), "section_titles"),
    }
    for key in DEFAULT_SECTION_TITLES:
        if not isinstance(section_titles.get(key), str) or not section_titles[key].strip():
            raise ValueError(f"section_titles.{key} must be a non-empty string")

    skills = []
    for index, skill in enumerate(require_list(data.get("skills"), "skills")):
        skill_map = require_mapping(skill, f"skills[{index}]")
        skills.append({
            "label": require_str(skill_map, "label", f"skills[{index}]"),
            "items": require_str(skill_map, "items", f"skills[{index}]"),
        })

    education = []
    for index, item in enumerate(require_list(data.get("education"), "education")):
        edu = require_mapping(item, f"education[{index}]")
        education.append({
            "institution": require_str(edu, "institution", f"education[{index}]"),
            "period": validate_period(edu.get("period"), f"education[{index}].period"),
            "degree": require_str(edu, "degree", f"education[{index}]"),
            "location": require_str(edu, "location", f"education[{index}]"),
        })

    return {
        "personal": {
            "name": require_str(personal, "name", "personal"),
            "title": require_str(personal, "title", "personal"),
            "email": require_str(personal, "email", "personal"),
            "linkedin_url": require_str(personal, "linkedin_url", "personal"),
            "github_url": require_str(personal, "github_url", "personal"),
        },
        "font": font,
        "section_titles": section_titles,
        "experience": [
            validate_entry(item, f"experience[{index}]")
            for index, item in enumerate(require_list(data.get("experience"), "experience"))
        ],
        "projects": [
            validate_entry(item, f"projects[{index}]")
            for index, item in enumerate(require_list(data.get("projects", []), "projects"))
        ],
        "skills": skills,
        "education": education,
        "output_filename": output_filename,
    }


def url_to_domain(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    parts = hostname.split(".")
    min_parts = 3 if re.search(r"\.(com|org|net|gov|edu)\.[a-z]{2}$", hostname) else 2
    return ".".join(parts[-min_parts:]) if len(parts) > min_parts else hostname


def profile_username(url: str) -> str:
    path = urlparse(url).path.strip("/")
    return path.split("/")[-1] if path else re.sub(r"^https?://", "", url)


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
    value = get_nested(ctx, key)
    return "" if value is None else str(value)


def render(template: str, ctx: dict) -> str:
    def repl_cond(match: re.Match) -> str:
        key, block = match.group(1), match.group(2)
        value = get_nested(ctx, key)
        truthy = len(value) > 0 if isinstance(value, (list, dict)) else bool(value)
        return render(block, ctx) if truthy else ""

    def repl_loop(match: re.Match) -> str:
        key, block = match.group(1), match.group(2)
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


def build_context(data: dict) -> dict:
    def map_entry(entry: dict) -> dict:
        return {
            "company": entry["company"],
            "role": entry["role"],
            "url": entry["url"],
            "period": f"{entry['period']['from']} -- {entry['period']['to']}",
            "domain": url_to_domain(entry["url"]),
            "bullets": [rich_to_latex(bullet) for bullet in entry["bullets"]],
        }

    return {
        "personal": {
            "name": data["personal"]["name"],
            "title": data["personal"]["title"],
            "email": data["personal"]["email"],
            "linkedin_url": data["personal"]["linkedin_url"],
            "github_url": data["personal"]["github_url"],
            "linkedin_display": profile_username(data["personal"]["linkedin_url"]),
            "github_display": profile_username(data["personal"]["github_url"]),
        },
        "font_package": FONT_PACKAGES[data["font"]],
        "section_titles": data["section_titles"],
        "experience": [map_entry(entry) for entry in data["experience"]],
        "projects": [map_entry(entry) for entry in data["projects"]],
        "skills": data["skills"],
        "education": [
            {
                "institution": item["institution"],
                "degree": item["degree"],
                "location": item["location"],
                "period": f"{item['period']['from']} -- {item['period']['to']}",
            }
            for item in data["education"]
        ],
        "output_filename": data["output_filename"],
    }


def build_resume(data_path: Path, template: str, output_dir: Path | None, keep_aux: bool) -> Path:
    raw = yaml.safe_load(data_path.read_text())
    data = validate_resume(raw, data_path)
    ctx = build_context(data)

    begin_pos = template.index(BEGIN_DOCUMENT)
    end_pos = template.index(END_DOCUMENT)
    tex = (
        render(template[:begin_pos], ctx)
        + BEGIN_DOCUMENT
        + render(template[begin_pos + len(BEGIN_DOCUMENT):end_pos], ctx)
        + END_DOCUMENT
        + "\n"
    )

    target_dir = output_dir or data_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    output_name = data["output_filename"]
    tex_path = target_dir / f"{output_name}.tex"
    pdf_path = target_dir / f"{output_name}.pdf"
    tex_path.write_text(tex)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(target_dir), str(tex_path)],
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdflatex failed for {data_path}")
    if not pdf_path.exists():
        raise RuntimeError(f"PDF not generated: {pdf_path}")

    if not keep_aux:
        for ext in ("aux", "log", "out", "tex"):
            (target_dir / f"{output_name}.{ext}").unlink(missing_ok=True)

    return pdf_path


def main() -> None:
    args = parse_args()
    if not args.template.exists():
        print(f"Template not found: {args.template}", file=sys.stderr)
        sys.exit(1)

    template = args.template.read_text()
    data_paths = discover_data_paths(args.data_paths)

    failed = False
    for path in data_paths:
        try:
            pdf_path = build_resume(path, template, args.output_dir, args.keep_aux)
            print(f"OK: {pdf_path}")
        except Exception as exc:
            print(f"FAILED {path}: {exc}", file=sys.stderr)
            failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
