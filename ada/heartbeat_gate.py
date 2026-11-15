#!/usr/bin/env python3
"""ADA-053 persistent heartbeat gate.

Read-only checker: validates pinned genesis and all committed events.
By default reports readiness; --require-second fails until real seq=2 exists.
Never synthesizes events, edits the ledger, or treats a schedule as evidence.
"""
import argparse
import json
from pathlib import Path

from persist_tick import verify_ledger
from kernel import digest, canonical

LEDGER = Path(__file__).resolve().parent / "kernel" / "events.jsonl"


def status(path=LEDGER):
    path = Path(path)
    state, head, count = verify_ledger(path)
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    for index, event in enumerate(events):
        if event["seq"] != index:
            raise ValueError("noncontiguous sequence")
        if index:
            parent = events[index - 1]
            if event["prev"] != parent["hash"]:
                raise ValueError("broken parent linkage")
        payload = dict(event)
        claimed = payload.pop("hash")
        if digest(payload) != claimed:
            raise ValueError("hash mismatch")
    ids = [e["workflow_run_id"] for e in events if e.get("workflow_run_id")]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate workflow run IDs")
    observed_second = len(events) >= 3
    if observed_second:
        second = events[2]
        if second["kind"] != "tick" or second.get("beat") != 2 or second.get("domain") != "internal":
            raise ValueError("unexpected second committed transition")
        if second["state"]["phase_fifths"] != 2 or second["state"]["phi_fifths"] != 0:
            raise ValueError("unexpected second phase")
        if second.get("workflow_run_id") == events[1].get("workflow_run_id"):
            raise ValueError("second tick reused workflow run ID")
    return {
        "genesis_pinned": True,
        "chain_valid": True,
        "event_count": count,
        "last_seq": count - 1,
        "head": head,
        "second_heartbeat_observed": observed_second,
        "second_run_id": events[2].get("workflow_run_id") if observed_second else None,
        "step": state["step"],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ledger", type=Path, default=LEDGER)
    p.add_argument("--require-second", action="store_true")
    args = p.parse_args()
    report = status(args.ledger)
    print(json.dumps(report, indent=2))
    if args.require_second and not report["second_heartbeat_observed"]:
        raise SystemExit("SECOND HEARTBEAT NOT YET OBSERVED (no fabricated tick)")


if __name__ == "__main__":
    main()
