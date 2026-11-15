#!/usr/bin/env python3
"""ADA-061 — witness-ancestry gate.

Demonstrates three-source agreement logic with explicitly synthetic fixtures.
No real external witnesses are asserted. No operational ledger writes.
"""
import json
from ada060_unseen import run as prior_run
from ada055_candidates import hash_payload

MIN_ROOTS = 3
FIXTURE_ROOTS = ("simulated-lab-A", "simulated-lab-B", "simulated-lab-C")


def make_packet(candidate_root, source_root, observed, *, origin="simulation", copied_from=None):
    """Immutable-style deterministic evidence packet; observation may be True/False."""
    if type(observed) is not bool:
        raise ValueError("observed must be Boolean")
    packet = {
        "candidate_root": candidate_root, "source_root": source_root,
        "observed_replay": observed, "origin": origin,
        "copied_from": copied_from,
    }
    packet["digest"] = hash_payload(packet)
    return packet


def check_packets(packets, candidate_root, numeric_pass, *, authorized_roots=()):
    """Fail closed on unknown roots, mismatched subjects and copied witnesses.

    'promotable' is a trust-gate decision, never proof of physical truth.
    """
    if not numeric_pass:
        return {"decision": "reject", "reason": "known numeric challenge failed",
                "independent_roots": 0}
    accepted = []
    counted_roots = set()
    for packet in packets:
        body = dict(packet)
        claimed = body.pop("digest", None)
        if claimed != hash_payload(body):
            raise ValueError("evidence packet digest mismatch")
        if packet["candidate_root"] != candidate_root:
            raise ValueError("packet describes different candidate")
        if packet["origin"] != "measured":
            continue
        root = packet["source_root"]
        if root not in authorized_roots:
            continue
        if packet["copied_from"] is not None:
            continue
        if root in counted_roots:
            continue
        counted_roots.add(root)
        accepted.append(packet["observed_replay"])
    roots = len(counted_roots)
    if roots < MIN_ROOTS:
        return {"decision": "abstain", "reason": "fewer than three eligible independent roots",
                "independent_roots": roots}
    if not all(v == accepted[0] for v in accepted):
        return {"decision": "abstain", "reason": "independent witnesses disagree",
                "independent_roots": roots}
    if not accepted[0]:
        return {"decision": "reject", "reason": "independent replay failure",
                "independent_roots": roots}
    return {"decision": "eligible", "reason": "three independently sourced agreeing replay packets",
            "independent_roots": roots}


def run_fixture():
    old = prior_run()
    # Select a numerically passing prior candidate, but do not assert it was measured.
    passing = next(x for x in old["cases"] if x["selected_result"]["known_pass"])
    target = passing["selected_root"]
    fake = [make_packet(target, root, True) for root in FIXTURE_ROOTS]
    copied = [make_packet(target, FIXTURE_ROOTS[0], True, copied_from="mirror")]
    disagreement = [make_packet(target, root, i != 2, origin="measured")
                    for i, root in enumerate(FIXTURE_ROOTS)]
    # Explicitly tagged simulation packets cannot qualify as measured witnesses.
    return {
        "target": target, "source_ancestry": old["source_ancestry"],
        "simulated_three_agree": check_packets(fake, target, True),
        "copied_report": check_packets(copied, target, True),
        "disagreement_fixture": check_packets(
            disagreement, target, True, authorized_roots=FIXTURE_ROOTS
        ),
        "real_evidence_collected": False,
        "promotion": "abstain",
        "fixtures": fake + copied + disagreement,
    }


if __name__ == "__main__":
    print(json.dumps(run_fixture(), indent=2))
