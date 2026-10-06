from __future__ import annotations
import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence
from .neuron_dynamics import LIFParameters, LIFState, parameters_from_config, simulate_lif

@dataclass(frozen=True, order=True)
class SpikeEvent:
    timestep: int
    neuron_id: int
    def __post_init__(self) -> None:
        if self.timestep < 0:
            raise ValueError("timestep must be >= 0")
        if self.neuron_id < 0:
            raise ValueError("neuron_id must be >= 0")

@dataclass(frozen=True)
class SpikeTrain:
    neuron_id: int
    spike_timesteps: tuple[int, ...]
    def __post_init__(self) -> None:
        if self.neuron_id < 0:
            raise ValueError("neuron_id must be >= 0")
        if any(t < 0 for t in self.spike_timesteps):
            raise ValueError("spike timesteps must be >= 0")
        if tuple(sorted(set(self.spike_timesteps))) != self.spike_timesteps:
            raise ValueError("spike timesteps must be strictly increasing")

def states_to_spike_events(states: Sequence[LIFState], neuron_id: int) -> tuple[SpikeEvent, ...]:
    if neuron_id < 0:
        raise ValueError("neuron_id must be >= 0")
    return tuple(SpikeEvent(timestep=i, neuron_id=neuron_id) for i, state in enumerate(states) if state.spike)

def states_to_spike_train(states: Sequence[LIFState], neuron_id: int) -> SpikeTrain:
    events = states_to_spike_events(states, neuron_id)
    return SpikeTrain(neuron_id, tuple(event.timestep for event in events))

def population_spike_events(state_traces: Iterable[tuple[int, Sequence[LIFState]]]) -> tuple[SpikeEvent, ...]:
    events: list[SpikeEvent] = []
    for neuron_id, states in state_traces:
        events.extend(states_to_spike_events(states, neuron_id))
    return tuple(sorted(events, key=lambda event: (event.timestep, event.neuron_id)))

def events_to_raster(events: Iterable[SpikeEvent], neuron_ids: Sequence[int], n_timesteps: int) -> tuple[tuple[int, ...], ...]:
    if n_timesteps < 0:
        raise ValueError("n_timesteps must be >= 0")
    ids = tuple(neuron_ids)
    if len(ids) != len(set(ids)) or any(neuron_id < 0 for neuron_id in ids):
        raise ValueError("neuron_ids must be unique and non-negative")
    columns = {neuron_id: i for i, neuron_id in enumerate(ids)}
    raster = [[0 for _ in ids] for _ in range(n_timesteps)]
    for event in events:
        if event.neuron_id not in columns:
            raise ValueError(f"event neuron_id {event.neuron_id} is not in neuron_ids")
        if event.timestep >= n_timesteps:
            raise ValueError(f"event timestep {event.timestep} is outside raster length {n_timesteps}")
        raster[event.timestep][columns[event.neuron_id]] = 1
    return tuple(tuple(row) for row in raster)

def spike_count(events: Iterable[SpikeEvent]) -> int:
    return sum(1 for _ in events)

def firing_rate(events: Iterable[SpikeEvent], duration_steps: int) -> float:
    if duration_steps <= 0:
        raise ValueError("duration_steps must be > 0")
    return spike_count(events) / duration_steps

def _parse_neuron_input(spec: str) -> tuple[int, list[float]]:
    try:
        neuron_id_text, values_text = spec.split(":", 1)
        neuron_id = int(neuron_id_text)
        values = [float(value) for value in values_text.split(",") if value]
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("input must use NEURON_ID:CURRENT,CURRENT,...") from exc
    if neuron_id < 0 or not values:
        raise argparse.ArgumentTypeError("neuron_id must be >= 0 and at least one current is required")
    return neuron_id, values

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert discrete LIF states into event/spike representations.")
    parser.add_argument("--config", type=Path, default=Path("configs/neuron_dynamics_v1.json"))
    parser.add_argument("--input", nargs="+", required=True, type=_parse_neuron_input, metavar="NEURON_ID:C1,C2,...")
    args = parser.parse_args()
    parameters: LIFParameters = parameters_from_config(args.config)
    traces = [(neuron_id, simulate_lif(currents, parameters)) for neuron_id, currents in args.input]
    events = population_spike_events(traces)
    neurons = []
    for neuron_id, states in sorted(traces, key=lambda item: item[0]):
        train = states_to_spike_train(states, neuron_id)
        neurons.append({"neuron_id": train.neuron_id, "spike_timesteps": list(train.spike_timesteps)})
    print(json.dumps({"event_count": len(events), "events": [asdict(event) for event in events], "neurons": neurons}, indent=2))

if __name__ == "__main__":
    main()
