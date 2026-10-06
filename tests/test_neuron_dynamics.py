from pathlib import Path

import pytest

from neuro_risk_engine.neuron_dynamics import (
    LIFParameters,
    LIFState,
    simulate_lif,
    step_lif,
)


def test_membrane_leaks_toward_resting_potential() -> None:
    parameters = LIFParameters()
    state = LIFState(membrane_potential=0.8)

    result = step_lif(state, 0.0, parameters)

    assert 0.0 < result.membrane_potential < 0.8
    assert result.spike is False


def test_positive_input_accumulates_membrane_potential() -> None:
    parameters = LIFParameters()
    state = LIFState(membrane_potential=0.0)

    result = step_lif(state, 0.5, parameters)

    assert result.membrane_potential == pytest.approx(0.025)
    assert result.spike is False


def test_threshold_emits_spike_and_resets() -> None:
    parameters = LIFParameters(
        tau_membrane=10.0,
        threshold=1.0,
        reset=0.0,
        dt=1.0,
        refractory_steps=2,
    )
    state = LIFState(membrane_potential=0.9)

    result = step_lif(state, 2.0, parameters)

    assert result.spike is True
    assert result.membrane_potential == parameters.reset
    assert result.refractory_remaining == 2


def test_refractory_period_blocks_spike() -> None:
    parameters = LIFParameters(refractory_steps=2)
    state = LIFState(
        membrane_potential=0.0,
        refractory_remaining=2,
        spike=True,
    )

    first = step_lif(state, 100.0, parameters)
    second = step_lif(first, 100.0, parameters)
    third = step_lif(second, 0.0, parameters)

    assert first.refractory_remaining == 1
    assert second.refractory_remaining == 0
    assert first.spike is False
    assert second.spike is False
    assert third.spike is False


def test_simulation_is_deterministic() -> None:
    parameters = LIFParameters()
    inputs = [0.5] * 10

    first = simulate_lif(inputs, parameters)
    second = simulate_lif(inputs, parameters)

    assert first == second


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"tau_membrane": 0.0}, "tau_membrane"),
        ({"dt": 0.0}, "dt"),
        ({"threshold": 0.0, "reset": 0.0}, "threshold"),
        ({"refractory_steps": -1}, "refractory_steps"),
    ],
)
def test_invalid_parameters_fail_fast(
    kwargs: dict, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        LIFParameters(**kwargs)
