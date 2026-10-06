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

The Fly-SNN must not be presented as superior before experiments are performed.

## Reproducibility

Experiments use explicit configurations, documented preprocessing, controlled comparisons, deterministic seeds where appropriate, and recorded evaluation results.

### Local setup

Use Python 3.13 or newer:

```text
python -m venv .venv
python -m pip install -e .
python -m pytest -q
```

For the Task 7 LIF CLI:

```text
python -m neuro_risk_engine.neuron_dynamics --input 0.2 0.2 0.2 1.5 0.0
```

GitHub Actions validates installation, tests, and source compilation on pushes and pull requests targeting `development`.

## Safety and sandbox scope

This is a research/sandbox project.

- It does not make real financial decisions.
- It does not use real customer financial data.
- It will not automatically authorize, reject, freeze, or block real financial accounts.

## Current status

**Tasks 1–7:** complete and audited.

The project is now ready to proceed to the next research task, while remaining strictly experimental and synthetic.
