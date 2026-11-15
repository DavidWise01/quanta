#!/usr/bin/env python3
"""ADA-056: repair one rejected candidate without erasing counterexamples.

Exact rational fixture, deliberately bounded search. No changes to persistent
ADA kernel, its GitHub Actions writer, or the committed witness ledger.
"""
import json
from fractions import Fraction as F

from ada055_candidates import PARENT, MANIFOLD, SINGLET, closure, evaluate, hash_payload, serial

LABELS = ("a", "b", "c")
# Fixed before observing any repairs: preserve Juliet's chosen growth axis a,
# and alter exactly one of the remaining two coordinates.
ELIGIBLE_AXES = (1, 2)


def repair_juliet(parent=PARENT):
    baseline = evaluate(parent)
    rejected = next(r for r in baseline["candidates"] if r["candidate"] == "Juliet")
    failure = tuple(F(x) for x in rejected["state"])
    original_hash = rejected["candidate_root"]
    k0 = closure(failure)
    if k0 == 0:
        raise ValueError("cannot repair a zero-product candidate with nonzero scaling")
    proposed = []
    for axis in ELIGIBLE_AXES:
        repaired = list(failure)
        repaired[axis] /= k0
        repaired = tuple(repaired)
        changed = sum(x != y for x, y in zip(failure, repaired))
        # Every candidate independently carries the rejected input root.
        record = {
            "axis": LABELS[axis],
            "changed_components": changed,
            "operation": "divide one coordinate by failing K",
            "factor": str(F(1, 1) / k0),
            "state": serial(repaired),
            "closure": str(closure(repaired)),
            "passes_closure": closure(repaired) == 1,
            "failure_root": original_hash,
            "parent_root": rejected["parent_root"],
            "root": hash_payload({
                "parent_root": rejected["parent_root"],
                "failure_root": original_hash,
                "axis": LABELS[axis],
                "state": serial(repaired),
            }),
            "source_ancestry": rejected["source_ancestry"],
        }
        proposed.append(record)

    admissible = [x for x in proposed if x["passes_closure"]]
    if not admissible:
        raise ValueError("no admissible repair")
    # Predeclared minimal Hamming edit distance, then lexical axis.
    chosen = min(admissible, key=lambda x: (x["changed_components"], x["axis"]))
    return {
        "manifold": MANIFOLD,
        "singlet": SINGLET,
        "parent": serial(parent),
        "parent_root": rejected["parent_root"],
        "failure": rejected,  # immutable evidence carried verbatim
        "repair_options": proposed,
        "chosen_repair": chosen,
        "objective": "minimize changed coordinates; break ties by axis name",
        "status": "mathematically repaired, not physically validated",
    }


if __name__ == "__main__":
    print(json.dumps(repair_juliet(), indent=2))
