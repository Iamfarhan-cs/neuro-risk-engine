# Neuro-Risk Engine

Neuro-Risk Engine is a computational-neuroscience research experiment investigating whether a Drosophila-connectome-inspired, event-driven/spiking neural architecture can provide useful computational properties for financial risk decision-making.

## Research question

> Can a Drosophila-connectome-inspired, event-driven/spiking neural architecture learn financial risk decision-making and provide useful advantages over conventional models?

This project is a research/sandbox experiment. It does not assume that biological inspiration will outperform conventional machine-learning methods.

## Motivation

The experiment investigates whether biological connectivity and event-driven/spiking computation can provide useful properties for a sequential financial-risk task, including predictive behavior, latency, computational cost, robustness, and generalization.

## Biological inspiration

The Drosophila connectome provides a source of biological wiring/topology.

**Important:** the connectome is used as a wiring/topology source, not as a pretrained financial model.

Conceptually:

Drosophila connectome
→ biological connectivity/topology
→ computational architecture
→ spiking/event-driven neural model
→ financial risk experiment

## Financial environment

The initial financial environment will use synthetic transaction/behavioral data. Initial decisions are:

- PASS
- REVIEW
- STEP-UP

No real customer financial data or real financial authorization decisions are used.

## Planned model comparison

1. Rule-based baseline
2. XGBoost
3. Conventional neural network / MLP
4. Generic SNN
5. Connectome-inspired / Fly-SNN
6. Random-topology SNN

The critical controlled comparison is Fly-inspired topology versus randomized topology while controlling relevant model capacity and experimental conditions.

## Planned metrics

- Precision
- Recall
- False-positive rate
- False-negative rate
- Latency
- Computational cost
- Robustness
- Generalization to unseen patterns
- Event/synaptic activity

## Scientific principles

The project distinguishes:

- **Hypothesis:** a testable expectation.
- **Prior expectation:** reasoning informed by existing knowledge before measurement.
- **Measured result:** an outcome obtained from the defined experiment.

The Fly-SNN must not be presented as superior before experiments are performed. XGBoost, MLP, generic SNN, Fly-SNN, or random topology may win, or the Fly-SNN may trade predictive accuracy for efficiency or robustness.

## Reproducibility

Experiments will use explicit configurations, documented preprocessing, controlled comparisons, deterministic seeds where appropriate, and recorded evaluation results.

## Safety and sandbox scope

This is a research/sandbox project.

- It does not make real financial decisions.
- It does not use real customer financial data.
- It will not automatically authorize, reject, freeze, or block real financial accounts.

## Current status

**Task 1 — Foundation:** complete.

Later tasks will introduce synthetic financial data, conventional baselines, SNNs, connectome topology, controlled topology experiments, and evaluation. Those experiments are not implemented in Task 1.
