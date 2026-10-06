# Task 6 — Topology-to-Computational Architecture

## Objective

Task 6 converts the validated FlyWire FAFB v783 topology into an explicit computational architecture specification.

The purpose is to define the structural role each biological neuron group will have in the future computational model without yet defining neuron dynamics, trainable weights, learning rules, temporal delays, financial feature encodings, or training procedures.

The biological topology remains frozen.

## Computational role mapping

| Biological group | Computational role |
|---|---|
| EPG | head-direction representation |
| Delta7 | head-direction integration |
| FC2 | goal-signal representation |
| PFL2 | steering integration |
| PFL3L | left steering integration |
| PFL3R | right steering integration |
| DNa02 | left steering output |
| DNa03 | right steering output |

These are architectural abstractions, not claims that the biological circuit implements financial concepts. Financial semantics are deliberately deferred.

## Structural rules

1. Every validated biological node is retained in the architecture manifest.
2. Active message-passing nodes are the nodes participating in retained edges.
3. Isolated biological nodes remain represented but are inactive for message passing.
4. Edge direction is preserved exactly.
5. Raw syn_count is retained as structural metadata.
6. No computational weight is assigned yet.
7. No neuron activation model is assigned yet.
8. No spike threshold, membrane equation, refractory period, delay, plasticity rule, or learning rule is assigned yet.
9. No financial feature is mapped to a biological population yet.
10. The topology cannot be modified because of anticipated financial-model performance.

## Why defer weights and dynamics?

A connectome provides structural connectivity. It does not uniquely specify a machine-learning implementation. Separating topology from dynamics, optimization, and financial representation makes later ablations possible.

## Output

The implementation produces computational_architecture.json, recording the architecture schema, exact Task 5 topology SHA-256, node/edge counts, active/isolated counts, role mapping, structural policy, every architecture node, and every structural edge with its original synapse count.

No raw FlyWire dataset is copied into the repository.

## Implementation

Run:

    python -m neuro_risk_engine.architecture \
      --nodes data/processed/flywire_v783_circuit/nodes.csv \
      --edges data/processed/flywire_v783_circuit/edges.csv \
      --manifest data/processed/flywire_v783_circuit/topology_manifest.json

The Task 5 validator runs first. If the topology fails validation, architecture construction stops rather than silently repairing or adapting the graph.

## What Task 6 does not do

Task 6 does not implement an SNN, define neuron dynamics, define spike encoding, define financial input features, define PASS/REVIEW/STEP-UP output semantics, train a model, generate synthetic transactions, benchmark models, randomize topology, or choose topology from financial results.

## Scientific handoff

The resulting bridge is:

    validated biological graph
            ↓
    computational architecture
            ↓
    [future task] neuron dynamics
            ↓
    [future task] event/spike representation
            ↓
    [future task] synthetic financial task

> Biology determines the structural topology; the financial experiment evaluates what computational properties that topology provides.
