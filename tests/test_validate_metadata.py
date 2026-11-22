from pathlib import Path

from scripts.validate_metadata import validate_metadata


def write_chapter(root: Path, module: str, name: str, chapter_id: str, prereqs=None, status=None) -> Path:
    folder = root / module / name
    folder.mkdir(parents=True, exist_ok=True)
    prereqs = prereqs or []
    status = status or {"derivation": 0, "params": 0, "code": 0}
    (folder / "notes.md").write_text(
        "---\n"
        f"id: {chapter_id}\nmodule: {module}\ntitle: {name}\n"
        f"prereqs: {prereqs!r}\nstatus:\n  derivation: {status['derivation']}\n"
        f"  params: {status['params']}\n  code: {status['code']}\n"
        "last_reviewed: null\n---\n\n# Chapter\n",
        encoding="utf-8",
    )
    return folder / "notes.md"


def test_valid_metadata_and_prerequisite_pass(tmp_path):
    write_chapter(tmp_path, "00_math_foundations", "linear-algebra", "linear_algebra")
    write_chapter(tmp_path, "01_supervised", "perceptron", "perceptron", ["linear_algebra"])

    assert validate_metadata(tmp_path) == []


def test_missing_prerequisite_is_reported(tmp_path):
    path = write_chapter(tmp_path, "01_supervised", "perceptron", "perceptron", ["missing"])

    errors = validate_metadata(tmp_path)

    assert any("prereq 'missing'" in error for error in errors)
    assert any(str(path.relative_to(tmp_path)) in error for error in errors)


def test_status_range_and_dependency_cycle_are_reported(tmp_path):
    write_chapter(tmp_path, "01_supervised", "first", "first", ["second"], {"derivation": 3, "params": 0, "code": 0})
    write_chapter(tmp_path, "01_supervised", "second", "second", ["first"])

    errors = validate_metadata(tmp_path)

    assert any("status.derivation" in error for error in errors)
    assert any("prerequisite cycle" in error for error in errors)
