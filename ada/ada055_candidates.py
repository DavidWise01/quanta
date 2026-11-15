#!/usr/bin/env python3
"""ADA-055: three candidate transformations from one immutable parent.
Standard-library exact fractions; an exploratory mathematical fixture, not AI training.
No modification to the scheduled ADA kernel or its evidence ledger.
"""
from fractions import Fraction as F
import hashlib
import json

PARENT = (F(1, 3), F(1, 3), F(1, 3))
ROLES = ("Josephson:-1", "Mandelbrot:0", "Juliet:+1")
MANIFOLD = "{[({s})]}"
SINGLET = "{s}"

def serial(state):
    return [str(x) for x in state]

def closure(state):
    a, b, c = state
    return 27 * a * b * c

def hash_payload(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def candidates(parent=PARENT):
    a, b, c = parent
    # Equal parent ancestry, independent declared operations—not independent corroboration.
    return [
        ("Josephson", (a*2, b/2, c), "reciprocal coupling"),
        ("Mandelbrot", (a, b, c), "neutral iteration/control"),
        ("Juliet", (a*3, b, c), "unbalanced branching/counterexample"),
    ]

def evaluate(parent=PARENT):
    if closure(parent) != 1:
        raise ValueError("parent must satisfy closure")
    root = hash_payload({"manifold": MANIFOLD, "parent": serial(parent)})
    observed = []
    for i, (name, state, method) in enumerate(candidates(parent)):
        permitted = closure(state) == 1
        # Selection is a deterministic test result, NOT claimed learned quality.
        novelty = sum(x != y for x,y in zip(state, parent))
        record = {
            "candidate": name, "role": ROLES[i], "operation": method,
            "parent_root": root, "candidate_root": hash_payload({
                "parent_root":root, "candidate":name, "state":serial(state)
            }),
            "source_ancestry": "synthetic:ada055:one-parent",
            "manifold": MANIFOLD, "singlet": SINGLET,
            "state": serial(state), "closure": str(closure(state)),
            "passes_closure": permitted, "changed_components": novelty,
            "status": "admissible" if permitted else "rejected",
        }
        observed.append(record)
    # Prefer a passing changed state over an unchanged control, by predeclared scoring.
    eligible = [r for r in observed if r["passes_closure"]]
    winner = sorted(eligible, key=lambda r:(-r["changed_components"],r["candidate"]))[0]
    return {"parent":serial(parent),"parent_root":root,
            "candidates":observed,"selected":winner["candidate"],
            "selection_rule":"passing closure; most changed components; lexical tie-break"}

def main():
    print(json.dumps(evaluate(), indent=2))

if __name__ == "__main__":
    main()
