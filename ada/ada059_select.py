#!/usr/bin/env python3
"""ADA-059: frozen-rule selection comparison on synthetic fresh parents.

Every candidate comes from one parent/root per case. Exact rational arithmetic;
this is a deterministic fixture, not a blinded or independent empirical test.
"""
import json
from fractions import Fraction as F

from ada055_candidates import MANIFOLD, SINGLET, closure, serial, hash_payload
from ada058_transfer import evaluate_challenge

# Frozen ordering before evaluating new parents: it is the baseline tie-break.
FACTORS = (F(3), F(2), F(1, 2), F(1, 3), F(1))
PARENTS = (
    (F(1, 3), F(1, 3), F(1, 3)),
    (F(1, 2), F(2, 9), F(1, 3)),
    (F(2, 3), F(1, 6), F(1, 3)),
    (F(3, 4), F(1, 6), F(8, 27)),
    (F(1, 4), F(4, 9), F(1, 3)),
)
VERSION = "ADA059-envelope-predeclared-v1"
SOURCE_ANCESTRY = "synthetic:ada059:fixture"


def propose(parent):
    if closure(parent) != 1 or not evaluate_challenge(parent)["all_pass"]:
        raise ValueError("parent must be a full-envelope passing state")
    root = hash_payload({"version": VERSION, "manifold": MANIFOLD, "parent": serial(parent)})
    candidates = []
    a, b, c = parent
    for priority, q in enumerate(FACTORS):
        state = (a * q, b / q, c)
        checks = evaluate_challenge(state)
        row = {
            "factor": str(q), "priority": priority,
            "state": serial(state),
            "parent_root": root,
            "candidate_root": hash_payload({"parent_root": root, "factor": str(q), "state": serial(state)}),
            "source_ancestry": SOURCE_ANCESTRY,
            "manifold": MANIFOLD, "singlet": SINGLET,
            "changed_components": sum(x != y for x, y in zip(state, parent)),
            **checks,
        }
        candidates.append(row)
    return root, candidates


def choose(candidates, full_envelope):
    # Fixed rule: prefer any admissible changed state over an unchanged baseline,
    # then use declared FACTORS priority. There is no observed-performance retuning.
    valid = [r for r in candidates if (r["all_pass"] if full_envelope else r["checks"]["closure"])]
    if not valid:
        return None
    return sorted(valid, key=lambda r: (-r["changed_components"], r["priority"]))[0]


def compare():
    cases = []
    for i, parent in enumerate(PARENTS):
        root, candidates = propose(parent)
        old = choose(candidates, False)
        new = choose(candidates, True)
        assert old is not None and new is not None
        cases.append({
            "case": i, "parent": serial(parent), "parent_root": root,
            "source_ancestry": SOURCE_ANCESTRY,
            "candidates": candidates,  # rejected proposals are retained
            "closure_only_choice": old["candidate_root"],
            "closure_only_factor": old["factor"],
            "closure_only_passes_envelope": old["all_pass"],
            "full_envelope_choice": new["candidate_root"],
            "full_envelope_factor": new["factor"],
            "full_envelope_passes": new["all_pass"],
        })
    return {
        "version": VERSION, "manifold": MANIFOLD, "singlet": SINGLET,
        "factor_order": [str(x) for x in FACTORS],
        "cases": cases,
        "baseline_passes": sum(x["closure_only_passes_envelope"] for x in cases),
        "new_passes": sum(x["full_envelope_passes"] for x in cases),
        "shared_ancestry": SOURCE_ANCESTRY,
        "result_root": hash_payload({"version": VERSION, "cases": cases}),
        "caveat": "synthetic constructed cases; not independent held-out evidence",
    }


if __name__ == "__main__":
    summary = compare()
    print(json.dumps({
        "version": summary["version"],
        "cases": len(summary["cases"]),
        "baseline_passes": summary["baseline_passes"],
        "new_passes": summary["new_passes"],
        "per_case": [{
            "parent": x["parent"],
            "old_factor": x["closure_only_factor"],
            "new_factor": x["full_envelope_factor"],
            "old_passes": x["closure_only_passes_envelope"],
        } for x in summary["cases"]],
        "result_root": summary["result_root"],
        "caveat": summary["caveat"],
    }, indent=2))
