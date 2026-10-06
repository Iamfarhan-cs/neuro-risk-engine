# Task 4 — FlyWire FAFB v783 Topology Extraction

Task 4 implements the frozen extraction specification from Task 3. It does not select a circuit from financial performance and does not implement the SNN.

## Frozen biological boundary

The extractor uses the pre-registered central-complex goal-directed steering pathway:

- EPG
- Delta7
- FC2 / FC2A / FC2B / FC2C
- PFL2
- PFL3L / PFL3R
- DNa02
- DNa03

The configuration uses exact cell-type aliases. If a class cannot be resolved in the selected FAFB v783 annotation export, extraction fails rather than guessing. The PFL3 left/right distinction is deliberately not inferred from soma hemisphere because the literature defines the populations by LAL projection.

## Input data

Expected static FAFB v783 exports:

- classification.csv.gz — root IDs and classification fields
- consolidated_cell_types.csv.gz — root IDs and primary cell types
- connections.csv.gz — directed pre_root_id, post_root_id, syn_count and neuropil

Uncompressed CSV files are also accepted. Raw FlyWire data are not committed to Git.

## Extraction rules

1. Match only pre-registered cell-type groups.
2. Keep FlyWire root IDs unchanged.
3. Keep only edges whose endpoints are selected neurons.
4. Aggregate synapse counts across neuropils for each neuron pair.
5. Apply the frozen >=5 synapse threshold.
6. Exclude self-loops from the active graph.
7. Retain isolated selected neurons in the node record.
8. Sort nodes and edges deterministically.
9. Compute SHA-256 over the exported node and edge files.

## Run

    python scripts/extract_flywire_v783.py \
      --classification /path/to/classification.csv.gz \
      --cell-types /path/to/consolidated_cell_types.csv.gz \
      --connections /path/to/connections.csv.gz \
      --output data/processed/flywire_v783_circuit

Outputs:

- nodes.csv
- edges.csv
- topology_manifest.json

## Scientific guardrails

- No random biological node selection.
- No financial feature inspection.
- No model training.
- No topology selection based on benchmark results.
- No raw FlyWire data committed to Git.
- No inference of missing cell-type mappings.
- No claim that this circuit predicts financial risk.

## Verification

Unit tests use miniature synthetic CSV fixtures only. They verify exact annotation matching, aggregation across neuropils, the five-synapse threshold, self-loop exclusion and manifest hashing.
