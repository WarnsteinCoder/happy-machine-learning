"""Build an Obsidian Canvas graph from chapter metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

if __package__:
    from .validate_metadata import MODULES, validate_metadata
else:
    from validate_metadata import MODULES, validate_metadata
import yaml


def _frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    end = lines.index("---", 1)
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid frontmatter mapping: {path}")
    return data


def _canvas_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", value)


def _mastery_color(status: dict[str, int]) -> str:
    average = sum(status[field] for field in ("derivation", "params", "code")) / 3
    if average < 0.67:
        return "1"
    if average < 1.34:
        return "2"
    return "4"


def build_canvas(root: Path, output_path: Path | None = None) -> dict[str, Any]:
    """Create Canvas data and optionally write it to *output_path*."""
    root = Path(root).resolve()
    errors = validate_metadata(root)
    if errors:
        raise ValueError("Metadata validation failed:\n" + "\n".join(errors))

    chapters: dict[str, tuple[Path, dict[str, Any]]] = {}
    for module in MODULES:
        for path in sorted((root / module).rglob("notes.md")):
            metadata = _frontmatter(path)
            chapters[metadata["id"]] = (path, metadata)

    depth_cache: dict[str, int] = {}

    def depth(chapter_id: str) -> int:
        if chapter_id not in depth_cache:
            prerequisites = chapters[chapter_id][1]["prereqs"]
            depth_cache[chapter_id] = 0 if not prerequisites else 1 + max(depth(item) for item in prerequisites)
        return depth_cache[chapter_id]

    ordered_ids = sorted(chapters, key=lambda item: (depth(item), item))
    depth_counts: dict[int, int] = {}
    nodes: list[dict[str, Any]] = []
    for chapter_id in ordered_ids:
        path, metadata = chapters[chapter_id]
        layer = depth(chapter_id)
        row = depth_counts.get(layer, 0)
        depth_counts[layer] = row + 1
        nodes.append({
            "id": _canvas_id(chapter_id),
            "type": "file",
            "file": path.relative_to(root).as_posix(),
            "x": layer * 360,
            "y": row * 180,
            "width": 280,
            "height": 120,
            "color": _mastery_color(metadata["status"]),
        })

    edges = []
    for chapter_id in ordered_ids:
        for index, prerequisite in enumerate(chapters[chapter_id][1]["prereqs"]):
            edges.append({
                "id": _canvas_id(f"{prerequisite}-{chapter_id}-{index}"),
                "fromNode": _canvas_id(prerequisite),
                "fromSide": "right",
                "toNode": _canvas_id(chapter_id),
                "toSide": "left",
                "label": "prerequisite",
            })
    canvas = {"nodes": nodes, "edges": edges}
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(canvas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    parser.add_argument("--output", type=Path, help="output Canvas path (default: <root>/knowledge_graph.canvas)")
    args = parser.parse_args()
    output = args.output or args.root / "knowledge_graph.canvas"
    try:
        build_canvas(args.root, output)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Canvas written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
