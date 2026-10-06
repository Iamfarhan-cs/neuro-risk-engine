from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

REQUIRED_CONNECTION_COLUMNS = {"pre_root_id", "post_root_id", "syn_count"}


@dataclass(frozen=True)
class Node:
    root_id: int
    cell_type: str
    group: str
    inclusion_reason: str
    source_version: str


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    syn_count: int


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _read_gzip_csv(path: Path) -> Iterable[dict[str, str]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as fh:
        yield from csv.DictReader(fh)


def _read_plain_or_gzip_csv(path: Path) -> Iterable[dict[str, str]]:
    if path.suffix == ".gz":
        yield from _read_gzip_csv(path)
    else:
        with path.open("r", encoding="utf-8", newline="") as fh:
            yield from csv.DictReader(fh)


def load_annotations(
    classification_path: Path, cell_types_path: Path, config: dict
) -> tuple[dict[int, Node], dict[str, list[str]]]:
    groups = config["selection"]["cell_type_groups"]
    aliases: dict[str, str] = {}
    for group, values in groups.items():
        for value in values:
            aliases[value.strip().casefold()] = group

    cell_types: dict[int, str] = {}
    for row in _read_plain_or_gzip_csv(cell_types_path):
        rid = int(row["root_id"])
        value = (row.get("primary_type") or row.get("cell_type") or "").strip()
        if value:
            cell_types[rid] = value

    # Read the classification export to validate its schema and root IDs.
    # Selection itself is driven only by the explicitly configured cell types.
    for row in _read_plain_or_gzip_csv(classification_path):
        int(row["root_id"])

    nodes: dict[int, Node] = {}
    matched: dict[str, list[str]] = defaultdict(list)

    for rid, cell_type in cell_types.items():
        group = aliases.get(cell_type.casefold())
        if group is None:
            continue

        nodes[rid] = Node(
            root_id=rid,
            cell_type=cell_type,
            group=group,
            inclusion_reason=f"pre-registered cell-type group: {group}",
            source_version=config["dataset"]["version"],
        )
        matched[group].append(str(rid))

    return nodes, matched


def aggregate_edges(
    connection_path: Path,
    node_ids: set[int],
    threshold: int,
    exclude_self_loops: bool,
) -> list[Edge]:
    pair_counts: defaultdict[tuple[int, int], int] = defaultdict(int)

    for row in _read_plain_or_gzip_csv(connection_path):
        if not REQUIRED_CONNECTION_COLUMNS.issubset(row):
            missing = sorted(REQUIRED_CONNECTION_COLUMNS - set(row))
            raise ValueError(f"Connection file missing required columns: {missing}")

        source = int(row["pre_root_id"])
        target = int(row["post_root_id"])

        if source not in node_ids or target not in node_ids:
            continue
        if exclude_self_loops and source == target:
            continue

        pair_counts[(source, target)] += int(row["syn_count"])

    return [
        Edge(source, target, count)
        for (source, target), count in sorted(pair_counts.items())
        if count >= threshold
    ]


def graph_stats(nodes: dict[int, Node], edges: list[Edge]) -> dict:
    active = {
        node.root_id
        for node in nodes.values()
        if any(edge.source == node.root_id or edge.target == node.root_id for edge in edges)
    }

    indegree = Counter(edge.target for edge in edges)
    outdegree = Counter(edge.source for edge in edges)
    degrees = [indegree[node] + outdegree[node] for node in active]

    n = len(active)
    density = len(edges) / (n * (n - 1)) if n > 1 else 0.0

    undirected: defaultdict[int, set[int]] = defaultdict(set)
    for edge in edges:
        undirected[edge.source].add(edge.target)
        undirected[edge.target].add(edge.source)

    seen: set[int] = set()
    components: list[int] = []

    for start in sorted(active):
        if start in seen:
            continue

        stack = [start]
        seen.add(start)
        size = 0

        while stack:
            current = stack.pop()
            size += 1
            for nxt in undirected[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)

        components.append(size)

    def summary(values: list[int]) -> dict:
        if not values:
            return {"min": 0, "max": 0, "mean": 0.0, "median": 0.0}

        ordered = sorted(values)
        mid = len(ordered) // 2
        median = (
            ordered[mid]
            if len(ordered) % 2
            else (ordered[mid - 1] + ordered[mid]) / 2
        )

        return {
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "median": median,
        }

    return {
        "selected_nodes": len(nodes),
        "active_nodes": len(active),
        "isolated_nodes": len(nodes) - len(active),
        "directed_edges": len(edges),
        "density_active_graph": density,
        "in_degree": summary([indegree[node] for node in active]),
        "out_degree": summary([outdegree[node] for node in active]),
        "total_degree": summary(degrees),
        "weak_component_count": len(components),
        "largest_weak_component": max(components, default=0),
    }


def sha256_files(paths: list[Path]) -> str:
    digest = hashlib.sha256()

    for path in paths:
        digest.update(path.name.encode("utf-8"))
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(chunk)

    return digest.hexdigest()


def write_outputs(
    output_dir: Path,
    nodes: dict[int, Node],
    edges: list[Edge],
    config: dict,
    matched: dict[str, list[str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    node_path = output_dir / "nodes.csv"
    edge_path = output_dir / "edges.csv"

    with node_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "root_id",
                "cell_type",
                "group",
                "inclusion_reason",
                "source_version",
            ],
        )
        writer.writeheader()

        for node in sorted(nodes.values(), key=lambda item: item.root_id):
            writer.writerow(asdict(node))

    with edge_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["source", "target", "syn_count"])
        writer.writeheader()

        for edge in edges:
            writer.writerow(asdict(edge))

    manifest = {
        "schema_version": 1,
        "dataset": config["dataset"],
        "selection": config["selection"],
        "mapping": {
            "matched_groups": {
                key: len(value) for key, value in sorted(matched.items())
            },
            "matched_root_ids": {
                key: sorted(map(int, value))
                for key, value in sorted(matched.items())
            },
        },
        "graph": graph_stats(nodes, edges),
        "outputs": {
            "nodes": node_path.name,
            "edges": edge_path.name,
        },
        "sha256": sha256_files([node_path, edge_path]),
    }

    with (output_dir / "topology_manifest.json").open(
        "w", encoding="utf-8"
    ) as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")


def extract(
    config_path: Path,
    classification_path: Path,
    cell_types_path: Path,
    connections_path: Path,
    output_dir: Path,
) -> None:
    config = load_config(config_path)

    nodes, matched = load_annotations(
        classification_path,
        cell_types_path,
        config,
    )

    expected = set(config["selection"]["cell_type_groups"])
    missing = sorted(expected - set(matched))

    if missing:
        raise ValueError(
            "Frozen circuit mapping is incomplete. Missing cell-type groups: "
            + ", ".join(missing)
            + ". Add a source-verified FlyWire v783 annotation mapping; "
            "do not infer it from financial performance."
        )

    edges = aggregate_edges(
        connections_path,
        set(nodes),
        int(config["selection"]["synapse_threshold"]),
        bool(config["selection"]["exclude_self_loops"]),
    )

    write_outputs(output_dir, nodes, edges, config, matched)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract the frozen Neuro-Risk Engine FlyWire FAFB v783 topology."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/circuit_selection_v783.json"),
    )
    parser.add_argument("--classification", type=Path, required=True)
    parser.add_argument("--cell-types", type=Path, required=True)
    parser.add_argument("--connections", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/flywire_v783_circuit"),
    )
    args = parser.parse_args()

    extract(
        args.config,
        args.classification,
        args.cell_types,
        args.connections,
        args.output,
    )


if __name__ == "__main__":
    main()
