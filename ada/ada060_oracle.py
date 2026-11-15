#!/usr/bin/env python3
"""ADA-060 independently *modularized* synthetic challenge definition.

Different code surface, NOT independent evidence ancestry or a blinded source.
These constraints are not used by the frozen ADA-059 selector.
"""
from fractions import Fraction as F

RULE_VERSION = "ada060-challenge-v1"
MAX_SINGLE = F(3, 4)
MAX_TOTAL = F(5, 4)
SOURCE_ROOT = "synthetic:quanta:ada-family"  # same owned root as selector


def challenge(state, evidence=None):
    v = tuple(F(x) for x in state)
    if len(v) != 3:
        raise ValueError("three amplitudes required")
    checks = {
        "single_coordinate_cap": max(v) <= MAX_SINGLE,
        "aggregate_budget": sum(v) <= MAX_TOTAL,
    }
    # A history claim requires a distinct, supplied measurement record.
    # No evidence means unknown, not False or True.
    history = None
    if evidence is not None:
        if evidence.get("source_root") != SOURCE_ROOT:
            raise ValueError("unexpected evidence provenance")
        value = evidence.get("observed_replay")
        if type(value) is not bool:
            raise ValueError("observed_replay must be an explicit Boolean")
        history = value
    return {"rules": RULE_VERSION, "checks": checks,
            "history_witness": history,
            "known_pass": all(checks.values()),
            "promotion": "reject" if not all(checks.values()) or history is False
                         else "abstain" if history is None else "eligible"}
