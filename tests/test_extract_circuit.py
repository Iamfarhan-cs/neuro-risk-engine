import csv
import gzip
import json
from pathlib import Path

from neuro_risk_engine.extract_circuit import Edge, Node
from neuro_risk_engine.extract_circuit import aggregate_edges, load_annotations, write_outputs


def gz_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with gzip.open(path, "wt", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_annotation_mapping_is_exact(tmp_path: Path) -> None:
    classification = tmp_path / "classification.csv.gz"
    cell_types = tmp_path / "consolidated_cell_types.csv.gz"

    gz_csv(
        classification,
        ["root_id", "side"],
        [{"root_id": "1", "side": "L"}, {"root_id": "2", "side": "R"}],
    )
    gz_csv(
        cell_types,
        ["root_id", "primary_type"],
        [{"root_id": "1", "primary_type": "EPG"}, {"root_id": "2", "primary_type": "PFL2"}],
    )

    config = {
        "dataset": {"version": "v783"},
        "selection": {"cell_type_groups": {"EPG": ["EPG"], "PFL2": ["PFL2"]}},
    }

    nodes, matched = load_annotations(classification, cell_types, config)

    assert set(nodes) == {1, 2}
    assert matched["EPG"] == ["1"]
    assert matched["PFL2"] == ["2"]


def test_edges_aggregate_across_neuropils_and_threshold(tmp_path: Path) -> None:
    connections = tmp_path / "connections.csv.gz"
    rows = [
        {"pre_root_id": "1", "post_root_id": "2", "neuropil": "A", "syn_count": "3"},
        {"pre_root_id": "1", "post_root_id": "2", "neuropil": "B", "syn_count": "2"},
        {"pre_root_id": "1", "post_root_id": "3", "neuropil": "A", "syn_count": "4"},
        {"pre_root_id": "2", "post_root_id": "2", "neuropil": "A", "syn_count": "99"},
        {"pre_root_id": "9", "post_root_id": "2", "neuropil": "A", "syn_count": "100"},
    ]

    gz_csv(
        connections,
        ["pre_root_id", "post_root_id", "neuropil", "syn_count"],
        rows,
    )

    edges = aggregate_edges(connections, {1, 2, 3}, threshold=5, exclude_self_loops=True)

    assert [(edge.source, edge.target, edge.syn_count) for edge in edges] == [(1, 2, 5)]


def test_manifest_contains_hash(tmp_path: Path) -> None:
    nodes = {
        1: Node(1, "EPG", "EPG", "test", "v783"),
        2: Node(2, "PFL2", "PFL2", "test", "v783"),
    }
    edges = [Edge(1, 2, 5)]

    config = {
        "dataset": {"name": "FlyWire FAFB", "version": "v783"},
        "selection": {"cell_type_groups": {"EPG": ["EPG"], "PFL2": ["PFL2"]}},
    }

    write_outputs(
        tmp_path,
        nodes,
        edges,
        config,
        {"EPG": ["1"], "PFL2": ["2"]},
    )

    manifest = json.loads((tmp_path / "topology_manifest.json").read_text())

    assert manifest["graph"]["directed_edges"] == 1
    assert len(manifest["sha256"]) == 64
