# Task 8 — Event / Spike Representation

Task 8 converts boolean spike states from the Task 7 LIF dynamics into an explicit deterministic event representation.

## Core representation

A SpikeEvent contains a discrete timestep and the emitting neuron ID. A SpikeTrain stores the strictly increasing spike timesteps for one neuron. Population events are ordered by timestep and then neuron ID.

A binary time-by-neuron raster is provided as an alternate representation of the same events.

## Event measurement

spike_count counts emitted events. firing_rate reports event density per simulation step. It is not a biological firing-rate measurement and Task 8 makes no physical-time calibration claim.

## Validation

Negative IDs or timesteps, duplicate or unordered spike times, duplicate neuron IDs, unknown raster neurons, out-of-range events, and non-positive durations are rejected. Invalid data are not silently repaired.

## Scope boundary

No financial features, transaction data, financial-to-spike encoding, connectome weights, synaptic delays, neurotransmitter/sign modeling, plasticity, learning, training, benchmarking, topology changes, or financial performance criteria are introduced.

The biological topology remains frozen. Task 8 only defines how Task 7 exposes discrete events.

## CLI

python -m neuro_risk_engine.spike_representation --input 1:0.2,0.2,1.5,0.0 2:0.2,0.2,1.5,0.0
