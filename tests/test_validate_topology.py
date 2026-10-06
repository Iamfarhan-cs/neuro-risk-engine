import csv
import hashlib
import json
from pathlib import Path

import pytest

from neuro_risk_engine.validate_topology import ValidationError, validate_topology


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fixture(tmp_path: Path):
    nodes = tmp_path / "nodes.csv"
    edges = tmp_path / "edges.csv"
    manifest = tmp_path / "topology_manifest.json"
    write_csv(nodes, ["root_id", "cell_type", "group", "inclusion_reason", "source_version"], [
        {"root_id": "1", "cell_type": "EPG", "group": "EPG", "inclusion_reason": "test", "source_version": "v783"},
        {"root_id": "2", "cell_type": "PFL2", "group": "PFL2", "inclusion_reason": "test", "source_version": "v783"},
        {"root_id": "3", "cell_type": "DNa02", "group": "DNa02", "inclusion_reason": "test", "source_version": "v783"},
    ])
    write_csv(edges, ["source", "target", "syn_count"], [{"source": "1", "target": "2", "syn_count": "5"}])
    digest = hashlib.sha256()
    for path in (nodes, edges):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    manifest.write_text(json.dumps({
        "selection": {"synapse_threshold": 5, "cell_type_groups": {
            "EPG": ["EPG"], "PFL2": ["PFL2"], "DNa02": ["DNa02"]}},
        "graph": {"selected_nodes": 3, "active_nodes": 2, "isolated_nodes": 1, "directed_edges": 1},
        "outputs": {"nodes": "nodes.csv", "edges": "edges.csv"},
        "sha256": digest.hexdigest(),
    }), encoding="utf-8")
    return nodes, edges, manifest


def test_valid_topology_passes(tmp_path: Path):
    nodes, edges, manifest = fixture(tmp_path)
    result = validate_topology(nodes, edges, manifest)
    assert result["valid"] is True
    assert result["node_count"] == 3
    assert result["active_node_count"] == 2
    assert result["isolated_node_count"] == 1


@pytest.mark.parametrize(("field", "value"), [("syn_count", "4"), ("target", "99")])
def test_invalid_edge_fails(tmp_path: Path, field: str, value: str):
    nodes, edges, manifest = fixture(tmp_path)
    rows = list(csv.DictReader(edges.open(encoding="utf-8")))
    rows[0][field] = value
    write_csv(edges, ["source", "target", "syn_count"], rows)
    with pytest.raises(ValidationError):
        validate_topology(nodes, edges, manifest)


def test_self_loop_fails(tmp_path: Path):
    nodes, edges, manifest = fixture(tmp_path)
    write_csv(edges, ["source", "target", "syn_count"],
              [{"source": "2", "target": "2", "syn_count": "5"}])
    with pytest.raises(ValidationError):
        validate_topology(nodes, edges, manifest)
