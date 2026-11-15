#!/usr/bin/env python3
"""ADA-057: append-only *experimental* generational repair memory.

Exact rational arithmetic. Two witnessed generations from one ancestry.
Separate from the scheduled ADA state ledger; no autonomous model training.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from ada055_candidates import PARENT, MANIFOLD, SINGLET, closure, serial, hash_payload
from ada056_repair import repair_juliet

ANCESTRY = "synthetic:ada055:one-parent"


def record(events, kind, state, parents=(), **details):
    """Create a hash-linked evidence event with explicit DAG ancestry."""
    seq = len(events)
    payload = {
        "seq": seq,
        "kind": kind,
        "state": serial(state),
        "K": str(closure(state)),
        "parent_roots": list(parents),
        "previous_event_hash": events[-1]["hash"] if events else None,
        "manifold": MANIFOLD,
        "singlet": SINGLET,
        "source_ancestry": ANCESTRY,
        **details,
    }
    payload["hash"] = hash_payload(payload)
    events.append(payload)
    return payload


def build():
    first = repair_juliet()
    parent = tuple(PARENT)
    failure = tuple(F(v) for v in first["failure"]["state"])
    repaired_b = tuple(F(v) for v in first["chosen_repair"]["state"])
    repaired_c = tuple(F(v) for v in first["repair_options"][1]["state"])
    assert first["chosen_repair"]["axis"] == "b"
    assert closure(repaired_b) == closure(repaired_c) == 1
    events = []

    genesis = record(events, "origin", parent, generation=0, verdict="origin",
                     source_root=first["parent_root"])
    fail0 = record(events, "failed-Juliet", failure, [genesis["hash"]],
                   generation=0, verdict="rejected", operation="a*=3")
    alt0 = record(events, "repair-c", repaired_c, [fail0["hash"]],
                  generation=0, verdict="admissible-alternative", operation="c/=3")
    selected0 = record(events, "repair-b", repaired_b, [fail0["hash"]],
                       generation=0, verdict="selected", operation="b/=3")
    promoted = record(events, "promote", repaired_b, [selected0["hash"]],
                      generation=1, verdict="new-parent", operation="explicit promotion")

    a,b,c = repaired_b
    second_failure = (a*3,b,c)
    assert closure(second_failure) == 3
    fail1 = record(events, "failed-Juliet", second_failure, [promoted["hash"]],
                   generation=1, verdict="rejected", operation="a*=3")
    second_c = (second_failure[0],second_failure[1],second_failure[2]/3)
    second_b = (second_failure[0],second_failure[1]/3,second_failure[2])
    alt1 = record(events, "repair-c", second_c, [fail1["hash"]],
                  generation=1, verdict="admissible-alternative", operation="c/=3")
    selected1 = record(events, "repair-b", second_b, [fail1["hash"]],
                       generation=1, verdict="selected", operation="b/=3")

    assert second_b == (F(3), F(1,27), F(1,3))
    assert closure(second_b) == closure(second_c) == 1
    verify(events)
    return events


def verify(events):
    if not events or events[0]["kind"] != "origin":
        raise ValueError("missing origin")
    seen = set()
    roots = {}
    previous = None
    for i, event in enumerate(events):
        if event["seq"] != i or event["previous_event_hash"] != previous:
            raise ValueError("non-contiguous event chain")
        if event["manifold"] != MANIFOLD or event["singlet"] != SINGLET:
            raise ValueError("manifold or singlet changed")
        if event["source_ancestry"] != ANCESTRY:
            raise ValueError("source ancestry changed")
        parents = event["parent_roots"]
        if any(p not in seen for p in parents):
            raise ValueError("missing or forward-referenced ancestor")
        signed = dict(event)
        claimed = signed.pop("hash")
        if claimed != hash_payload(signed) or claimed in seen:
            raise ValueError("record digest mismatch or duplicate")
        if str(closure(tuple(F(v) for v in event["state"]))) != event["K"]:
            raise ValueError("closure statement mismatch")
        if event["verdict"] == "rejected" and event["K"] == "1":
            raise ValueError("invalid failure classification")
        if event["verdict"] in ("selected", "new-parent", "admissible-alternative") and event["K"] != "1":
            raise ValueError("nonconserving promotion")
        seen.add(claimed)
        roots[claimed] = event
        previous = claimed
    if len(events) != 8:
        raise ValueError("incomplete two-generation fixture")
    if events[4]["parent_roots"] != [events[3]["hash"]]:
        raise ValueError("promotion did not preserve selected repair")
    if events[5]["parent_roots"] != [events[4]["hash"]]:
        raise ValueError("second failure has wrong parent")
    return True


def export_create_only(path, events):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents silently rewriting any prior archive.
    with path.open("x", encoding="utf-8", newline="\n") as f:
        for entry in events:
            f.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--export", type=Path, default=None)
    p.add_argument("--verify", type=Path, default=None)
    args = p.parse_args()
    if args.verify:
        entries = [json.loads(line) for line in args.verify.read_text().splitlines()]
        verify(entries)
        print("PASS: archived lineage and eight-event chain")
        return
    events = build()
    if args.export:
        export_create_only(args.export, events)
    print(json.dumps({
        "records": len(events),
        "gen0_repair": events[3]["state"],
        "gen1_failure": events[5]["state"],
        "gen1_repair": events[7]["state"],
        "closure": events[7]["K"],
        "last_hash": events[-1]["hash"],
    }, indent=2))


if __name__ == "__main__":
    main()
