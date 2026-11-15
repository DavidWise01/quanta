#!/usr/bin/env python3
"""ADA-058: challenge transfer beyond closure in one source ancestry.

Exact-rational, predeclared synthetic constraints. Not a blinded benchmark,
physical experiment, or evidence of general autonomous intelligence.
"""
from fractions import Fraction as F
from itertools import permutations
import json

from ada055_candidates import closure, serial, hash_payload, MANIFOLD, SINGLET
from ada057_generations import build, verify, ANCESTRY

MAX_AMPLITUDE = F(1)
MAX_IMBALANCE = F(9)
CHALLENGES = ("closure", "positive", "resource_cap", "balance", "permutation_stability")


def evaluate_challenge(state):
    values = tuple(F(x) for x in state)
    if len(values) != 3:
        raise ValueError("exactly three mini-states required")
    positive = all(v > 0 for v in values)
    ratio = max(values) / min(values) if positive else None
    checks = {
        "closure": closure(values) == 1,
        "positive": positive,
        "resource_cap": all(0 < v <= MAX_AMPLITUDE for v in values),
        "balance": positive and ratio <= MAX_IMBALANCE,
        "permutation_stability": all(closure(p) == closure(values) for p in permutations(values)),
    }
    return {"state": serial(values), "K": str(closure(values)),
            "imbalance": str(ratio) if ratio is not None else None,
            "checks": checks, "passed": sum(checks.values()),
            "total": len(CHALLENGES), "all_pass": all(checks.values())}


def evaluate_generations():
    events = build()
    verify(events)
    names = ("origin", "gen0_selected", "gen1_selected", "gen1_alternative")
    indices = (0, 3, 7, 6)
    observations = []
    for name, index in zip(names, indices):
        event = events[index]
        result = evaluate_challenge(event["state"])
        observations.append({
            "name": name, "source_event_seq": event["seq"],
            "source_event_hash": event["hash"],
            "source_ancestry": ANCESTRY,
            "manifold": MANIFOLD, "singlet": SINGLET,
            **result,
        })
    return {
        "rule_version": "ADA058-synthetic-envelope-v1",
        "rules": {
            "K": "27abc=1", "minimum": "positive",
            "coordinate_max": str(MAX_AMPLITUDE),
            "max_to_min_ratio": str(MAX_IMBALANCE),
            "permutations": "all 6 assignments must preserve K",
        },
        "observations": observations,
        "status": "diagnostic transfer challenge, not blinded/general proof",
        "record_root": hash_payload({
            "challenge": "ADA058-synthetic-envelope-v1",
            "parents": [event["hash"] for event in events],
            "observations": observations,
        }),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate_generations(), indent=2))
