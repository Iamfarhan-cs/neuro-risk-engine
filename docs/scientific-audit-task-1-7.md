# Scientific Audit — Neuro-Risk Engine Tasks 1–7

## Overall result

PASS AFTER SCIENTIFIC REMEDIATION

## S-01 — DNa02/DNa03 lateralization error

The previous Task 6 configuration assigned DNa02 to a left-steering role and DNa03 to a right-steering role. This is not supported by the cited navigation literature. DNa02 and DNa03 are cell types with right/left copies; PFL3R/PFL3L are the populations explicitly defined by axonal projection hemisphere.
Fix: DNa02 is now steering_output_population and DNa03 is steering_intermediate_population. Later hemispheric copies must come from explicit neuron-level metadata/connectivity.

## S-02 — Five-synapse threshold qualification

The 5-synapse threshold is defensible as an operational graph-construction rule, and whole-brain FlyWire network analysis has used it. It is not a universal biological cutoff.
Fix: keep threshold 5 as the frozen primary topology, but preregister sensitivity analyses at thresholds 1, 5, 10, and 31. The threshold cannot be selected after observing financial performance.

## S-03 — Financial mapping preregistration

The biological circuit is experimentally grounded in goal-directed navigation, not financial risk. A later analogy between navigation variables and financial variables could become post-hoc if it is chosen after model results are visible.
Fix: before financial experiments, freeze the financial state variables, computational abstraction, neural population mapping, encoding, temporal resolution, normalization, data split, and common representation used by all baselines.

## S-04 — Homogeneous LIF is a simplification

Task 7 uses one LIF parameterization. This is acceptable as a controlled computational baseline, but it is not evidence that all biological neuron classes have identical dynamics.
Fix: explicitly retain this interpretation in the architecture specification. Any future heterogeneous dynamics must be treated as a separate experimental factor.

## Scientific controls now frozen

1. Biological topology is selected independently of financial performance.
2. Primary topology threshold is 5 synapses.
3. Threshold robustness values are 1, 5, 10, and 31.
4. DNa02/DNa03 lateralization is never inferred from cell-type names.
5. PFL3L/PFL3R lateralization follows explicit projection definitions.
6. Financial input mapping is frozen before model comparison.
7. The same task representation is available to biological and control models.
8. LIF defaults are computational parameters, not biological measurements.
9. No scientific conclusion is drawn before controlled evaluation.
10. Real payment authorization, real customer data, and real-world financial decisions remain outside scope.

## Not yet validated

- connectome topology improves financial prediction;
- SNNs have lower latency or computational cost;
- biological topology improves robustness;
- the navigation circuit is an appropriate financial inductive bias;
- any observed gain is caused specifically by biological topology rather than sparsity, parameter count, dynamics, or training differences.

## Conclusion

Tasks 1–7 now form a defensible scientific foundation for the next experimental stage. The next task may proceed only while preserving these controls.