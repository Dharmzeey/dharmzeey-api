"""One-off seed: import existing markdown projects and hardcoded skills.

Run:  python seed.py
Safe to re-run — uses update_or_create keyed on slug/label.
"""
import os
import re
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")
django.setup()

from projects.models import Project  # noqa: E402
from skills.models import Skill, SkillCategory  # noqa: E402

MD_DIR = Path(__file__).resolve().parent / "seed_data" / "completed"


def parse_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            data[key] = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",") if v.strip()]
        else:
            data[key] = value.strip('"').strip("'")
    return data


def seed_projects():
    files = sorted(MD_DIR.glob("*.md"))
    for i, f in enumerate(files):
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        if not fm.get("title"):
            continue
        project, created = Project.objects.update_or_create(
            slug=fm.get("slug") or fm["title"].lower().replace(" ", "-"),
            defaults={
                "title": fm["title"],
                "category": fm.get("category", ""),
                "intro": fm.get("intro", ""),
                "summary": fm.get("summary", ""),
                "url": fm.get("url", ""),
                "github": fm.get("github", ""),
                "github_api": fm.get("github_api", ""),
                "stack": fm.get("stack", []),
                "is_published": True,
                "sort_order": i,
            },
        )
        print(f"{'Created' if created else 'Updated'} project: {project.title}")


SKILLS = [
    ("// frontend", ["Next.js / App Router", "React + TypeScript", "Tailwind CSS", "Accessibility / SEO"]),
    ("// backend", ["Django / DRF", "Django Channels", "Celery / Redis", "REST & WebSockets"]),
    ("// data", ["PostgreSQL", "PostGIS", "Redis", "Query optimisation"]),
    ("// infra & security", ["Docker / Compose", "GitHub Actions CI/CD", "Nginx / AWS", "Auth & hardening"]),
]


def seed_skills():
    for i, (label, skills) in enumerate(SKILLS):
        cat, _ = SkillCategory.objects.update_or_create(label=label, defaults={"sort_order": i})
        for j, name in enumerate(skills):
            Skill.objects.update_or_create(category=cat, name=name, defaults={"sort_order": j})
        print(f"Seeded category: {label} ({len(skills)} skills)")


if __name__ == "__main__":
    seed_projects()
    seed_skills()
    print("Done.")
