# Task 6 — Topology-to-Computational Architecture

## Scientifically corrected role mapping

| Biological group | Computational role |
|---|---|
| EPG | head-direction representation |
| Delta7 | head-direction integration |
| FC2 | goal-signal representation |
| PFL2 | steering gain modulation |
| PFL3L | left steering integration |
| PFL3R | right steering integration |
| DNa02 | steering output population |
| DNa03 | steering intermediate population |

## Lateralization correction

DNa02 and DNa03 are cell types/populations, not intrinsically left and right computational roles. The 2024 steering model explicitly represents right and left copies as DNa02R/DNa02L and DNa03R/DNa03L, while PFL3R/PFL3L are defined by axonal projection hemisphere. Therefore the architecture must not encode DNa02 as left or DNa03 as right.
If later experiments require hemispheric DNa02/DNa03 units, those copies must be represented explicitly from neuron-level metadata and connectivity rather than inferred from the cell-type label.

## Biological grounding

The selected circuit is a navigation circuit in which EPG activity represents heading, FC2 activity represents a navigational goal, PFL3 compares goal and heading representations, PFL2 modulates steering gain, DNa02 is a downstream steering-output readout, and DNa03 participates in an indirect PFL2/PFL3-to-DNa02 pathway.
These functions justify the computational architecture only. They do not imply that the biological circuit naturally implements financial-risk concepts.

## Structural rules

1. Every validated biological node is retained in the architecture manifest.
2. Active message-passing nodes are nodes participating in retained edges.
3. Isolated biological nodes remain represented but inactive for message passing.
4. Edge direction is preserved exactly.
5. Raw syn_count is retained as structural metadata.
6. No trainable computational weight is assigned yet.
7. Task 7 supplies a common LIF dynamics model; this is an explicit computational simplification, not a claim that all selected biological neurons have identical dynamics.
8. No synaptic delay, plasticity, or learning rule is assigned yet.
9. No financial feature is mapped to a biological population yet.
10. The topology cannot be modified because of anticipated financial-model performance.

## Connectome threshold caveat

The extraction pipeline currently uses a 5-synapse edge threshold. This is an operational graph-construction rule, not a universal biological definition of a real connection.
Lin et al. used a five-synapse threshold in whole-brain network analysis and explicitly examined robustness to threshold variation. Other FlyWire analyses show stronger reproducibility for higher-weight edges. Therefore the financial experiment must not treat the 5-synapse graph as uniquely correct.
The primary frozen topology remains threshold 5. The preregistered robustness analysis must evaluate thresholds 1, 5, 10, and 31. Threshold sensitivity is a robustness analysis, not a mechanism for choosing whichever topology performs best after seeing financial results.

## Financial mapping guardrail

Before synthetic financial features are mapped into the architecture, the mapping must be documented and frozen before model comparison.
It must specify:
1. financial state variables;
2. computational abstraction for each variable;
3. neural populations receiving each variable;
4. rate/current/spike encoding;
5. temporal resolution;
6. normalization;
7. train/validation/test separation;
8. whether the same representation is used by all model baselines.
This prevents the experiment from selecting an input representation after observing which topology performs best.

## Scientific handoff

biological evidence → frozen topology → computational architecture → Task 7 dynamics → future event/spike representation → preregistered synthetic financial task → controlled comparison

No financial conclusion can be drawn yet.
