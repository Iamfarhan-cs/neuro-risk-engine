# Task 9: Synthetic Financial Risk Environment

## Objective

Define and implement the first controlled financial environment for Neuro-Risk Engine.

The environment is synthetic by design. It provides the same frozen information to later baseline and SNN experiments without using real customer or payment data.

## Frozen decision space

Each synthetic transaction receives one of three experiment targets:

1. PASS
2. REVIEW
3. STEP-UP

These are research labels, not production authorization decisions.

## Frozen feature schema

| Feature | Type | Meaning |
|---|---|---|
| amount | continuous | Synthetic transaction amount |
| account_age_days | integer | Synthetic account age |
| transaction_velocity_24h | integer | Recent transaction count |
| merchant_risk | continuous | Synthetic merchant risk factor in [0, 1] |
| geo_distance_km | continuous | Synthetic distance from prior context |
| device_novelty | continuous | Synthetic device novelty in [0, 1] |
| failed_attempts_24h | integer | Recent failed-attempt count |
| hour_sin | continuous | Cyclic time-of-day representation |
| hour_cos | continuous | Cyclic time-of-day representation |

The latent risk score used to construct the target is not emitted as a model feature.

## Label construction

The generator computes a latent synthetic risk score from the declared variables and bounded random noise.

Decision thresholds are:

PASS: score < 0.33

REVIEW: score >= 0.33 and < 0.66

STEP-UP: score >= 0.66

The latent score is a data-generation mechanism only. Exposing it to a model would create target leakage.

## Reproducibility

Generation uses Python's seeded random.Random generator.

The default seed is 42.

The same sample count and seed must produce the same observations. Changing the seed produces a different synthetic environment.

## Scientific controls

The financial environment is frozen before model benchmarking.

Later models must receive:

- the same generated observations;
- the same feature information;
- the same target labels;
- the same train, validation, and test partition.

Model-specific stochastic seeds must be recorded separately.

The connectome topology must not be selected or modified using financial performance.

## Scope boundary

Task 9 does not implement financial-to-spike encoding, model training, baseline models, SNN training, topology modification, benchmarking, or production financial decisions.

## Safety boundary

All generated observations are synthetic. The module contains no customer identifiers, payment credentials, production integrations, authorization calls, account actions, or real financial records.
