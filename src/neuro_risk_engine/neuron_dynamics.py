from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class LIFParameters:
    tau_membrane: float = 20.0
    threshold: float = 1.0
    reset: float = 0.0
    resting_potential: float = 0.0
    dt: float = 1.0
    refractory_steps: int = 2

    def __post_init__(self) -> None:
        if self.tau_membrane <= 0:
            raise ValueError('tau_membrane must be > 0')
        if self.dt <= 0:
            raise ValueError('dt must be > 0')
        if self.threshold <= self.reset:
            raise ValueError('threshold must be greater than reset')
        if self.refractory_steps < 0:
            raise ValueError('refractory_steps must be >= 0')

@dataclass(frozen=True)
class LIFState:
    membrane_potential: float = 0.0
    refractory_remaining: int = 0
    spike: bool = False

def step_lif(state: LIFState, input_current: float, parameters: LIFParameters) -> LIFState:
    if state.refractory_remaining > 0:
        return LIFState(
            membrane_potential=parameters.reset,
            refractory_remaining=state.refractory_remaining - 1,
            spike=False,
        )

    decay = -(state.membrane_potential - parameters.resting_potential)
    next_potential = state.membrane_potential + (
        parameters.dt / parameters.tau_membrane
    ) * (decay + input_current)

    if next_potential >= parameters.threshold:
        return LIFState(
            membrane_potential=parameters.reset,
            refractory_remaining=parameters.refractory_steps,
            spike=True,
        )

    return LIFState(
        membrane_potential=next_potential,
        refractory_remaining=0,
        spike=False,
    )

def simulate_lif(input_currents: Iterable[float], parameters: LIFParameters, initial_potential: float | None = None) -> list[LIFState]:
    state = LIFState(
        membrane_potential=parameters.resting_potential if initial_potential is None else initial_potential
    )
    states: list[LIFState] = []
    for current in input_currents:
        state = step_lif(state, float(current), parameters)
        states.append(state)
    return states

def parameters_from_config(path: Path) -> LIFParameters:
    config = json.loads(path.read_text(encoding='utf-8'))
    return LIFParameters(**config['parameters'])

def main() -> None:
    parser = argparse.ArgumentParser(description='Simulate the frozen Task 7 discrete-time LIF neuron.')
    parser.add_argument('--config', type=Path, default=Path('configs/neuron_dynamics_v1.json'))
    parser.add_argument('--input', nargs='+', type=float, required=True)
    args = parser.parse_args()
    parameters = parameters_from_config(args.config)
    states = simulate_lif(args.input, parameters)
    print(json.dumps([{'membrane_potential': s.membrane_potential, 'refractory_remaining': s.refractory_remaining, 'spike': s.spike} for s in states], indent=2))

if __name__ == '__main__':
    main()
