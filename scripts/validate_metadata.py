"""Validate chapter frontmatter and prerequisite links."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
import sys
from typing import Any

import yaml


MODULES = (
    "00_math_foundations",
    "01_supervised",
    "02_unsupervised",
    "03_deep_learning",
    "04_reinforcement_learning",
)
STATUS_FIELDS = ("derivation", "params", "code")
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def _read_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"cannot read file: {exc}"
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing YAML frontmatter opening delimiter"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "missing YAML frontmatter closing delimiter"
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping"
    return data, None


def validate_metadata(root: Path) -> list[str]:
    """Return all metadata and prerequisite issues found under *root*."""
    root = Path(root)
    errors: list[str] = []
    chapters: list[tuple[Path, dict[str, Any]]] = []
    by_id: dict[str, Path] = {}

    for module in MODULES:
        module_dir = root / module
        if not module_dir.is_dir():
            continue
        for path in sorted(module_dir.rglob("notes.md")):
            data, parse_error = _read_frontmatter(path)
            if parse_error:
                errors.append(f"{path.relative_to(root)}: {parse_error}")
                continue
            assert data is not None
            chapters.append((path, data))
            relative = path.relative_to(root)

            for field in ("id", "module", "title", "prereqs", "status", "last_reviewed"):
                if field not in data:
                    errors.append(f"{relative}: missing required field '{field}'")

            chapter_id = data.get("id")
            if not isinstance(chapter_id, str) or not chapter_id.strip() or not ID_PATTERN.fullmatch(chapter_id):
                errors.append(f"{relative}: id must be a non-empty identifier using letters, digits, '_' or '-'")
            elif chapter_id in by_id:
                errors.append(f"{relative}: duplicate id '{chapter_id}' (also in {by_id[chapter_id].relative_to(root)})")
            else:
                by_id[chapter_id] = path

            if data.get("module") not in MODULES:
                errors.append(f"{relative}: module must be one of {', '.join(MODULES)}")
            elif data["module"] != path.relative_to(root).parts[0]:
                errors.append(f"{relative}: module does not match containing module directory")

            if not isinstance(data.get("title"), str) or not data["title"].strip():
                errors.append(f"{relative}: title must be a non-empty string")

            prereqs = data.get("prereqs")
            if not isinstance(prereqs, list) or any(not isinstance(item, str) or not item.strip() for item in prereqs):
                errors.append(f"{relative}: prereqs must be a list of non-empty chapter IDs")
            elif len(prereqs) != len(set(prereqs)):
                errors.append(f"{relative}: prereqs must not contain duplicates")

            status = data.get("status")
            if not isinstance(status, dict):
                errors.append(f"{relative}: status must be a mapping")
            else:
                for field in STATUS_FIELDS:
                    value = status.get(field)
                    if isinstance(value, bool) or not isinstance(value, int) or value not in (0, 1, 2):
                        errors.append(f"{relative}: status.{field} must be an integer from 0 to 2")

            reviewed = data.get("last_reviewed")
            if reviewed is not None and not isinstance(reviewed, date):
                valid_string = isinstance(reviewed, str)
                if valid_string:
                    try:
                        datetime.strptime(reviewed, "%Y-%m-%d")
                    except ValueError:
                        valid_string = False
                if not valid_string:
                    errors.append(f"{relative}: last_reviewed must be an ISO date (YYYY-MM-DD) or null")

    graph: dict[str, list[str]] = {}
    for path, data in chapters:
        chapter_id = data.get("id")
        if not isinstance(chapter_id, str) or chapter_id not in by_id or by_id[chapter_id] != path:
            continue
        prereqs = data.get("prereqs")
        if not isinstance(prereqs, list) or any(not isinstance(item, str) for item in prereqs):
            continue
        graph[chapter_id] = prereqs
        for prerequisite in prereqs:
            if prerequisite not in by_id:
                errors.append(f"{path.relative_to(root)}: prereq '{prerequisite}' does not match any chapter id")
            elif prerequisite == chapter_id:
                errors.append(f"{path.relative_to(root)}: chapter cannot require itself")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(chapter_id: str, chain: list[str]) -> None:
        if chapter_id in visiting:
            cycle = chain[chain.index(chapter_id):] + [chapter_id]
            errors.append("prerequisite cycle: " + " -> ".join(cycle))
            return
        if chapter_id in visited:
            return
        visiting.add(chapter_id)
        for prerequisite in graph.get(chapter_id, []):
            if prerequisite in graph:
                visit(prerequisite, chain + [prerequisite])
        visiting.remove(chapter_id)
        visited.add(chapter_id)

    for chapter_id in graph:
        if chapter_id not in visited:
            visit(chapter_id, [chapter_id])
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    args = parser.parse_args()
    errors = validate_metadata(args.root)
    if errors:
        print("Metadata validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Metadata validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
