from __future__ import annotations

import argparse
import csv
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

DECISIONS = ("PASS", "REVIEW", "STEP-UP")

@dataclass(frozen=True)
class RiskTransaction:
    transaction_id: int
    amount: float
    account_age_days: int
    transaction_velocity_24h: int
    merchant_risk: float
    geo_distance_km: float
    device_novelty: float
    failed_attempts_24h: int
    hour_sin: float
    hour_cos: float
    decision: str

FEATURE_NAMES = (
    "amount", "account_age_days", "transaction_velocity_24h", "merchant_risk",
    "geo_distance_km", "device_novelty", "failed_attempts_24h", "hour_sin", "hour_cos",
)

def _bounded(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))

def _decision(risk_score: float) -> str:
    if risk_score < 0.33:
        return "PASS"
    if risk_score < 0.66:
        return "REVIEW"
    return "STEP-UP"

def generate_transactions(n: int, seed: int = 42) -> list[RiskTransaction]:
    """Generate reproducible synthetic transaction-risk observations."""
    if n < 1:
        raise ValueError("n must be >= 1")
    rng = random.Random(seed)
    rows: list[RiskTransaction] = []
    for transaction_id in range(n):
        amount = _bounded(rng.lognormvariate(math.log(80.0), 0.95), 1.0, 10_000.0)
        account_age_days = rng.randint(7, 3_000)
        velocity = rng.randint(0, 20)
        merchant_risk = rng.random()
        geo_distance_km = _bounded(rng.expovariate(1 / 80.0), 0.0, 2_000.0)
        device_novelty = rng.random()
        failed_attempts = rng.randint(0, 6)
        hour = rng.randrange(24)
        radians = 2 * math.pi * hour / 24
        hour_sin, hour_cos = math.sin(radians), math.cos(radians)

        amount_component = min(math.log1p(amount) / math.log1p(10_000.0), 1.0)
        age_component = 1.0 - min(account_age_days / 3_000.0, 1.0)
        velocity_component = min(velocity / 20.0, 1.0)
        geo_component = min(geo_distance_km / 500.0, 1.0)
        failed_component = min(failed_attempts / 6.0, 1.0)

        risk_score = (
            0.24 * amount_component + 0.12 * age_component
            + 0.16 * velocity_component + 0.18 * merchant_risk
            + 0.10 * geo_component + 0.12 * device_novelty
            + 0.08 * failed_component
        )
        risk_score = _bounded(risk_score + rng.gauss(0.0, 0.045), 0.0, 1.0)

        rows.append(RiskTransaction(
            transaction_id=transaction_id,
            amount=round(amount, 4),
            account_age_days=account_age_days,
            transaction_velocity_24h=velocity,
            merchant_risk=round(merchant_risk, 6),
            geo_distance_km=round(geo_distance_km, 4),
            device_novelty=round(device_novelty, 6),
            failed_attempts_24h=failed_attempts,
            hour_sin=round(hour_sin, 6),
            hour_cos=round(hour_cos, 6),
            decision=_decision(risk_score),
        ))
    return rows

def write_csv(rows: list[RiskTransaction], path: Path) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)

def write_metadata(path: Path, n: int, seed: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0", "task": 9, "dataset_type": "synthetic",
        "n_samples": n, "seed": seed, "features": list(FEATURE_NAMES),
        "target": "decision", "classes": list(DECISIONS),
        "label_generation": "latent_risk_score_thresholds",
        "latent_risk_excluded_from_features": True, "real_customer_data": False,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Task 9 synthetic financial risk environment.")
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("experiments/data/task9_transactions.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("experiments/data/task9_metadata.json"))
    args = parser.parse_args()
    rows = generate_transactions(args.n, args.seed)
    write_csv(rows, args.output)
    write_metadata(args.metadata, args.n, args.seed)
    print(json.dumps({"samples": len(rows), "seed": args.seed, "output": str(args.output), "metadata": str(args.metadata)}))

if __name__ == "__main__":
    main()
