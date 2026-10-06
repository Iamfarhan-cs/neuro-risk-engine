from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


class ValidationError(ValueError):
    """Raised when an extracted topology violates a frozen invariant."""


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _sha256_files(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode("utf-8"))
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def validate_topology(nodes_path: Path, edges_path: Path, manifest_path: Path) -> dict:
    nodes = _read_csv(nodes_path)
    edges = _read_csv(edges_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    required_nodes = {"root_id", "cell_type", "group", "inclusion_reason", "source_version"}
    required_edges = {"source", "target", "syn_count"}
    if not required_nodes.issubset(set(nodes[0]) if nodes else set()):
        errors.append("nodes.csv is missing required columns")
    if not required_edges.issubset(set(edges[0]) if edges else set()):
        errors.append("edges.csv is missing required columns")

    node_ids = []
    for row in nodes:
        try:
            node_ids.append(int(row["root_id"]))
        except (KeyError, ValueError):
            errors.append(f"invalid node root_id: {row.get('root_id')!r}")

    duplicates = [rid for rid, count in Counter(node_ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate node IDs: {duplicates[:5]}")

    node_set = set(node_ids)
    parsed_edges = []
    for row in edges:
        try:
            source, target, syn_count = int(row["source"]), int(row["target"]), int(row["syn_count"])
        except (KeyError, ValueError):
            errors.append(f"invalid edge row: {row}")
            continue
        parsed_edges.append((source, target, syn_count))
        if source not in node_set or target not in node_set:
            errors.append(f"edge endpoint missing from node set: {source}->{target}")
        if source == target:
            errors.append(f"self-loop present: {source}->{target}")
        if syn_count <= 0:
            errors.append(f"non-positive synapse count: {source}->{target}={syn_count}")

    threshold = int(manifest.get("selection", {}).get("synapse_threshold", 0))
    below_threshold = [edge for edge in parsed_edges if edge[2] < threshold]
    if below_threshold:
        errors.append(f"{len(below_threshold)} edges are below frozen threshold {threshold}")

    ordered_nodes = [int(row["root_id"]) for row in nodes if row.get("root_id", "").isdigit()]
    if ordered_nodes != sorted(ordered_nodes):
        errors.append("nodes.csv is not deterministically sorted by root_id")

    ordered_edges = [(int(row["source"]), int(row["target"])) for row in edges
                     if row.get("source", "").isdigit() and row.get("target", "").isdigit()]
    if ordered_edges != sorted(ordered_edges):
        errors.append("edges.csv is not deterministically sorted by source,target")

    expected_groups = set(manifest.get("selection", {}).get("cell_type_groups", {}))
    actual_groups = {row.get("group") for row in nodes}
    missing_groups = sorted(expected_groups - actual_groups)
    if missing_groups:
        errors.append(f"missing expected node groups: {missing_groups}")

    outputs = manifest.get("outputs", {})
    if outputs.get("nodes") != nodes_path.name:
        errors.append("manifest node output name does not match nodes.csv")
    if outputs.get("edges") != edges_path.name:
        errors.append("manifest edge output name does not match edges.csv")

    graph = manifest.get("graph", {})
    if graph.get("selected_nodes") != len(nodes):
        errors.append("manifest selected_nodes does not match nodes.csv")
    if graph.get("directed_edges") != len(edges):
        errors.append("manifest directed_edges does not match edges.csv")

    active = {node for edge in parsed_edges for node in edge[:2]}
    if graph.get("active_nodes") != len(active):
        errors.append("manifest active_nodes does not match edge endpoints")
    if graph.get("isolated_nodes") != len(nodes) - len(active):
        errors.append("manifest isolated_nodes does not match node/edge structure")

    actual_hash = _sha256_files([nodes_path, edges_path])
    if manifest.get("sha256") != actual_hash:
        errors.append("topology SHA-256 does not match exported node/edge files")

    result = {
        "valid": not errors,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "active_node_count": len(active),
        "isolated_node_count": len(nodes) - len(active),
        "sha256": actual_hash,
        "errors": errors,
    }
    if errors:
        raise ValidationError("; ".join(errors))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a frozen Neuro-Risk Engine topology export.")
    parser.add_argument("--nodes", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(validate_topology(args.nodes, args.edges, args.manifest), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
