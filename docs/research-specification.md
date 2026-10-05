# Neuro-Risk Engine — Research Specification

## 1. Research question

**Can a Drosophila-connectome-inspired, event-driven/spiking neural architecture learn financial risk decision-making and provide useful advantages over conventional models?**

This is a research question, not a claim that the proposed architecture will outperform existing methods.

## 2. Research motivation

The experiment investigates whether biological connectivity and event-driven/spiking computation can provide useful computational properties for a financial risk decision task. The evaluation will consider predictive performance as well as latency, computational cost, robustness, and generalization.

## 3. Biological inspiration

The Drosophila connectome is used as a source of biological wiring/topology.

**The connectome is used as a wiring/topology source, not as a pretrained financial model.**

The intended transformation is:

Drosophila connectome
↓
biological connectivity/topology
↓
computational architecture
↓
spiking/event-driven neural model
↓
financial risk experiment

The later experiment must distinguish biological topology from the neural dynamics implemented on that topology.

## 4. Financial task

The initial environment will be synthetic. It will represent financial transaction/behavioral patterns rather than real customer activity.

Initial risk decisions:

- PASS
- REVIEW
- STEP-UP

The environment is deliberately isolated from real payment authorization or account-management systems.

## 5. Planned model comparisons

The planned comparison set is:

1. Rule-based baseline
2. XGBoost
3. MLP
4. Generic SNN
5. Fly-SNN
6. Random-SNN

The purpose of the baselines is to establish whether any observed behavior is actually useful relative to conventional approaches.

## 6. Critical controlled experiment

The central topology experiment compares:

**Fly-inspired topology vs randomized topology**

Relevant model capacity and experimental conditions should be controlled so that topology—not simply model size or training budget—is the principal experimental difference.

A result in favor of Fly topology is not assumed. Similar random-topology performance is itself an informative result.

## 7. Planned metrics

Predictive metrics:

- Precision
- Recall
- False-positive rate
- False-negative rate

Systems/efficiency metrics:

- Latency
- Computational cost
- Event/synaptic activity

Scientific behavior:

- Robustness
- Generalization to unseen patterns

Metrics must be defined precisely before the corresponding experiments are compared.

## 8. Scientific hypothesis

A hypothesis is a testable expectation, not an established result.

The project will distinguish:

- **Hypothesis:** what the experiment predicts may happen.
- **Prior expectation:** what existing reasoning suggests before measurement.
- **Measured result:** what the implemented experiment actually observes.

The project must not claim that Fly-SNN is better before measurement.

Possible valid outcomes include:

- XGBoost wins.
- MLP wins.
- Generic SNN wins.
- Fly-SNN wins.
- Fly-SNN loses accuracy but provides efficiency or robustness advantages.
- Random topology performs similarly to Fly topology.

## 9. Reproducibility principles

Future experiments should:

- Keep experiment definitions explicit.
- Record configuration and relevant seeds.
- Separate training, validation, and evaluation data appropriately.
- Preserve comparable conditions across model families.
- Record metrics and experimental outcomes.
- Keep synthetic data generation reproducible where practical.
- Avoid uncontrolled changes between comparison runs.

## 10. Research limitations

The initial environment is synthetic and therefore cannot establish performance on real-world financial fraud or risk populations.

A connectome-inspired topology is not equivalent to reproducing biological cognition. The experiment tests computational consequences of a topology and neural model, not whether the software reproduces a fruit fly brain.

Benchmark conclusions will depend on the chosen synthetic task, data-generating process, model capacity, training procedure, hardware, and evaluation protocol.

## 11. Safety and scope

This is a research/sandbox project.

It does not make real financial decisions.

It does not use real customer financial data.

It will not automatically authorize, reject, freeze, or block real financial accounts.

The financial environment and all initial experiments must remain synthetic and isolated from production payment systems.
