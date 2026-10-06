from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .validate_topology import validate_topology

@dataclass(frozen=True)
class ArchitectureNode:
    root_id: int
    cell_type: str
    group: str
    computational_role: str
    active: bool

@dataclass(frozen=True)
class ArchitectureEdge:
    source: int
    target: int
    syn_count: int

def load_architecture_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def build_architecture(nodes_path: Path, edges_path: Path, manifest_path: Path, config_path: Path) -> dict:
    validation = validate_topology(nodes_path, edges_path, manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = load_architecture_config(config_path)
    role_by_group = config["computational_roles"]
    required_groups = set(manifest["selection"]["cell_type_groups"])
    missing_roles = sorted(required_groups - set(role_by_group))
    if missing_roles:
        raise ValueError(f"No computational role defined for groups: {missing_roles}")
    node_rows = _read_csv(nodes_path)
    edge_rows = _read_csv(edges_path)
    active_ids = {int(row["source"]) for row in edge_rows} | {int(row["target"]) for row in edge_rows}
    nodes = [
        ArchitectureNode(int(row["root_id"]), row["cell_type"], row["group"], role_by_group[row["group"]], int(row["root_id"]) in active_ids)
        for row in node_rows
    ]
    edges = [ArchitectureEdge(int(row["source"]), int(row["target"]), int(row["syn_count"])) for row in edge_rows]
    role_counts: dict[str, int] = {}
    for node in nodes:
        role_counts[node.computational_role] = role_counts.get(node.computational_role, 0) + 1
    return {
        "schema_version": config["schema_version"],
        "architecture": {
            "name": config["name"],
            "description": config["description"],
            "topology_sha256": validation["sha256"],
            "node_count": len(nodes),
            "active_node_count": len(active_ids),
            "isolated_node_count": len(nodes) - len(active_ids),
            "edge_count": len(edges),
            "role_counts": dict(sorted(role_counts.items())),
        },
        "computational_roles": role_by_group,
        "structural_policy": config["structural_policy"],
        "nodes": [asdict(node) for node in nodes],
        "edges": [asdict(edge) for edge in edges],
    }

def write_architecture(architecture: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(architecture, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Task 6 computational architecture from a validated topology.")
    parser.add_argument("--nodes", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/computational_architecture_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/flywire_v783_circuit/computational_architecture.json"))
    args = parser.parse_args()
    architecture = build_architecture(args.nodes, args.edges, args.manifest, args.config)
    write_architecture(architecture, args.output)
    print(json.dumps(architecture["architecture"], indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
