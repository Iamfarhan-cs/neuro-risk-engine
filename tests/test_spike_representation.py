from neuro_risk_engine.neuron_dynamics import LIFState
from neuro_risk_engine.spike_representation import SpikeEvent, SpikeTrain, events_to_raster, firing_rate, population_spike_events, states_to_spike_events, states_to_spike_train

def states(*spikes: bool) -> list[LIFState]:
    return [LIFState(membrane_potential=0.0, spike=spike) for spike in spikes]

def test_state_to_events():
    assert states_to_spike_events(states(False, True, False, True), 7) == (SpikeEvent(1, 7), SpikeEvent(3, 7))

def test_spike_train():
    assert states_to_spike_train(states(True, False, True), 2) == SpikeTrain(2, (0, 2))

def test_population_order():
    assert population_spike_events([(9, states(False, True)), (3, states(True, True))]) == (SpikeEvent(0, 3), SpikeEvent(1, 3), SpikeEvent(1, 9))

def test_raster():
    assert events_to_raster((SpikeEvent(0, 3), SpikeEvent(1, 9), SpikeEvent(2, 3)), (3, 9), 3) == ((1, 0), (0, 1), (1, 0))

def test_empty_raster():
    assert events_to_raster((), (1, 2), 2) == ((0, 0), (0, 0))

def test_event_density():
    assert firing_rate((SpikeEvent(0, 1), SpikeEvent(3, 1)), 4) == 0.5

def test_invalid_event_rejected():
    try:
        SpikeEvent(-1, 1)
        assert False
    except ValueError:
        pass
