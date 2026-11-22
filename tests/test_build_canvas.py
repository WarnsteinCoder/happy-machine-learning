import json
from pathlib import Path

from scripts.build_canvas import build_canvas
from tests.test_validate_metadata import write_chapter


def test_canvas_nodes_edges_layout_and_mastery_colors(tmp_path):
    write_chapter(tmp_path, "00_math_foundations", "linear-algebra", "linear_algebra", status={"derivation": 2, "params": 2, "code": 2})
    write_chapter(tmp_path, "01_supervised", "perceptron", "perceptron", ["linear_algebra"], {"derivation": 1, "params": 0, "code": 1})
    output = tmp_path / "knowledge_graph.canvas"

    canvas = build_canvas(tmp_path, output)

    assert output.is_file()
    assert json.loads(output.read_text(encoding="utf-8")) == canvas
    nodes = {node["id"]: node for node in canvas["nodes"]}
    assert nodes["linear_algebra"]["color"] == "4"
    assert nodes["linear_algebra"]["x"] < nodes["perceptron"]["x"]
    assert nodes["perceptron"]["file"] == "01_supervised/perceptron/notes.md"
    assert canvas["edges"] == [{
        "id": "linear_algebra-perceptron-0",
        "fromNode": "linear_algebra",
        "fromSide": "right",
        "toNode": "perceptron",
        "toSide": "left",
        "label": "prerequisite",
    }]


def test_canvas_refuses_invalid_metadata(tmp_path):
    write_chapter(tmp_path, "01_supervised", "perceptron", "perceptron", ["absent"])

    try:
        build_canvas(tmp_path)
    except ValueError as exc:
        assert "does not match any chapter id" in str(exc)
    else:
        raise AssertionError("invalid metadata should prevent Canvas generation")
