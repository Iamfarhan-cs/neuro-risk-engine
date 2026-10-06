# Task 7 — Neuron Dynamics

## Objective

Task 7 introduces the first explicit neuron dynamics model on the frozen Task 6 computational architecture.

The selected model is a discrete-time Leaky Integrate-and-Fire (LIF) neuron.

This task defines computation, not biological parameter fitting. The initial parameters are explicit computational defaults and must not be described as measured properties of the selected Drosophila neurons.

## Model

For a non-refractory timestep:

```text
V[t+1] = V[t] + (dt / tau) * (-(V[t] - V_rest) + I[t])
```

A spike is emitted when:

```text
V[t+1] >= threshold
```

After a spike:
- membrane potential is reset to `reset`;
- `refractory_steps` timesteps are entered;
- spikes are suppressed during the refractory period.

The implementation uses forward Euler integration.

## Frozen initial parameters

| Parameter | Value |
|---|---:|
| tau_membrane | 20.0 |
| threshold | 1.0 |
| reset | 0.0 |
| resting_potential | 0.0 |
| dt | 1.0 |
| refractory_steps | 2 |

These are computational parameters. They are not claimed to be experimentally measured Drosophila neuron parameters.

## Input boundary

The model accepts an abstract scalar input current.

No financial feature, transaction field, spike encoder, connectome-derived weight, synaptic delay, plasticity rule, or learning rule is introduced in Task 7.

## Reproducibility

Parameters are frozen in:

```text
configs/neuron_dynamics_v1.json
```

The implementation is deterministic for a fixed input sequence and parameter configuration.

## CLI

From the repository root:

```text
python -m neuro_risk_engine.neuron_dynamics --input 0.2 0.2 0.2 1.5 0.0
```

## Tests

The test suite covers:
- membrane leakage toward rest;
- positive input accumulation;
- threshold spike and reset;
- refractory behavior;
- deterministic simulation;
- invalid parameter rejection.

## Scope boundary

Task 7 does not introduce:
- financial data;
- synthetic transactions;
- feature encoding;
- model training;
- topology modification;
- connectome weights;
- synaptic delays;
- plasticity;
- benchmarking.

The next computational layer is event/spike representation and later input encoding.
