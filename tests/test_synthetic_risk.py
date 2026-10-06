from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from neuro_risk_engine.synthetic_risk import DECISIONS, FEATURE_NAMES, generate_transactions, write_csv, write_metadata


def test_generation_is_deterministic() -> None:
    assert generate_transactions(20, seed=42) == generate_transactions(20, seed=42)


def test_different_seed_changes_environment() -> None:
    assert generate_transactions(20, seed=42) != generate_transactions(20, seed=43)


def test_three_decision_classes_are_frozen() -> None:
    rows = generate_transactions(2_000, seed=42)
    assert set(row.decision for row in rows) == set(DECISIONS)


def test_feature_schema_excludes_latent_risk_score() -> None:
    rows = generate_transactions(3, seed=42)
    fields = set(rows[0].__dataclass_fields__)
    assert set(FEATURE_NAMES).issubset(fields)
    assert "risk_score" not in fields
    assert "decision" not in FEATURE_NAMES


def test_values_stay_within_declared_ranges() -> None:
    for row in generate_transactions(500, seed=42):
        assert 1.0 <= row.amount <= 10_000.0
        assert 7 <= row.account_age_days <= 3_000
        assert 0 <= row.transaction_velocity_24h <= 20
        assert 0.0 <= row.merchant_risk <= 1.0
        assert 0.0 <= row.geo_distance_km <= 2_000.0
        assert 0.0 <= row.device_novelty <= 1.0
        assert 0 <= row.failed_attempts_24h <= 6
        assert -1.0 <= row.hour_sin <= 1.0
        assert -1.0 <= row.hour_cos <= 1.0
        assert row.decision in DECISIONS


def test_invalid_sample_count() -> None:
    with pytest.raises(ValueError):
        generate_transactions(0)


def test_csv_and_metadata_outputs(tmp_path: Path) -> None:
    rows = generate_transactions(10, seed=7)
    csv_path = tmp_path / "transactions.csv"
    metadata_path = tmp_path / "metadata.json"
    write_csv(rows, csv_path)
    write_metadata(metadata_path, len(rows), 7)
    with csv_path.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert len(csv_rows) == 10
    assert metadata["task"] == 9
    assert metadata["seed"] == 7
    assert metadata["latent_risk_excluded_from_features"] is True
