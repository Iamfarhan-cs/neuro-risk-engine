Task 5 — Topology Validation and Quality Control

This task validates the frozen FlyWire FAFB v783 topology produced by Task 4 before SNN dynamics or synthetic financial data are introduced.

The validator checks required columns, unique node IDs, edge endpoint integrity, self-loop policy, the frozen five-synapse threshold, deterministic ordering, representation of every pre-registered cell-type group, manifest counts, active/isolated node counts, and the SHA-256 recorded for the exported node and edge files.

It fails closed: violations raise ValidationError rather than silently repairing the topology.

It does not download FlyWire data, change biological selection, infer cell types, prune nodes, introduce financial features, build or train an SNN, benchmark models, or select topology using financial results.

Run:

    python -m neuro_risk_engine.validate_topology --nodes data/processed/flywire_v783_circuit/nodes.csv --edges data/processed/flywire_v783_circuit/edges.csv --manifest data/processed/flywire_v783_circuit/topology_manifest.json

Tests use only synthetic fixtures. Task 6 may build on a topology that has passed this validation and must keep the biological topology frozen.
