import csv
import hashlib
import json
from pathlib import Path

import pytest

from neuro_risk_engine.architecture import build_architecture
from neuro_risk_engine.validate_topology import ValidationError

def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def fixture(tmp_path: Path):
    nodes, edges, manifest, config = (tmp_path / 'nodes.csv', tmp_path / 'edges.csv', tmp_path / 'manifest.json', tmp_path / 'config.json')
    groups = ['EPG', 'Delta7', 'FC2', 'PFL2', 'PFL3L', 'PFL3R', 'DNa02', 'DNa03']
    node_rows = [{'root_id': str(i), 'cell_type': g, 'group': g, 'inclusion_reason': 'test', 'source_version': 'v783'} for i, g in enumerate(groups, 1)]
    edge_rows = [
        {'source': '1', 'target': '2', 'syn_count': '5'},
        {'source': '2', 'target': '4', 'syn_count': '7'},
        {'source': '3', 'target': '5', 'syn_count': '8'},
        {'source': '5', 'target': '7', 'syn_count': '6'},
    ]
    write_csv(nodes, ['root_id', 'cell_type', 'group', 'inclusion_reason', 'source_version'], node_rows)
    write_csv(edges, ['source', 'target', 'syn_count'], edge_rows)
    digest = hashlib.sha256()
    for path in (nodes, edges):
        digest.update(path.name.encode('utf-8'))
        digest.update(path.read_bytes())
    manifest.write_text(json.dumps({'selection': {'synapse_threshold': 5, 'cell_type_groups': {g: [g] for g in groups}}, 'graph': {'selected_nodes': 8, 'active_nodes': 6, 'isolated_nodes': 2, 'directed_edges': 4}, 'outputs': {'nodes': 'nodes.csv', 'edges': 'edges.csv'}, 'sha256': digest.hexdigest()}), encoding='utf-8')
    config.write_text(json.dumps({
        'schema_version': 2, 'name': 'test_architecture', 'description': 'test',
        'computational_roles': {
            'EPG': 'head_direction_representation', 'Delta7': 'head_direction_integration',
            'FC2': 'goal_signal_representation', 'PFL2': 'steering_gain_modulation',
            'PFL3L': 'steering_integration_left', 'PFL3R': 'steering_integration_right',
            'DNa02': 'steering_output_population', 'DNa03': 'steering_intermediate_population'
        },
        'structural_policy': {'weight_assignment': 'deferred'},
    }), encoding='utf-8')
    return nodes, edges, manifest, config

def test_build_architecture_preserves_topology_and_correct_roles(tmp_path: Path):
    nodes, edges, manifest, config = fixture(tmp_path)
    result = build_architecture(nodes, edges, manifest, config)
    assert result['architecture']['node_count'] == 8
    assert result['architecture']['edge_count'] == 4
    assert result['architecture']['active_node_count'] == 6
    assert result['architecture']['isolated_node_count'] == 2
    assert result['nodes'][0]['computational_role'] == 'head_direction_representation'
    roles = {node['group']: node['computational_role'] for node in result['nodes']}
    assert roles['DNa02'] == 'steering_output_population'
    assert roles['DNa03'] == 'steering_intermediate_population'
    assert result['edges'][0]['syn_count'] == 5

def test_invalid_topology_is_rejected_before_architecture_build(tmp_path: Path):
    nodes, edges, manifest, config = fixture(tmp_path)
    rows = list(csv.DictReader(edges.open(encoding='utf-8')))
    rows[0]['syn_count'] = '4'
    write_csv(edges, ['source', 'target', 'syn_count'], rows)
    with pytest.raises(ValidationError):
        build_architecture(nodes, edges, manifest, config)
