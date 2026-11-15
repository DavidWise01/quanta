#!/usr/bin/env python3
"""Append exactly one ADA kernel tick per distinct GitHub Actions run.

One writer, one new JSONL line, pinned genesis, replay validation and no
mutation of any earlier bytes. Git commit/push is handled by the workflow.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from kernel import GENESIS, ROLES, MANIFOLD, replay, event, canonical
from verify_readonly import TRUSTED_GENESIS_HASH

DEFAULT_LEDGER = Path(__file__).resolve().parent / "kernel" / "events.jsonl"


def verify_ledger(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        first = fh.readline()
    if not first.endswith("\n"):
        raise ValueError("truncated genesis")
    genesis = json.loads(first)
    if (genesis.get("hash") != TRUSTED_GENESIS_HASH
            or genesis.get("prev") != GENESIS
            or genesis.get("kind") != "genesis"
            or genesis.get("seq") != 0):
        raise ValueError("trusted genesis mismatch")
    state, head, count = replay(path)
    if (state["manifold"] != MANIFOLD or state["roles"] != ROLES
            or state["box"] != "constant:1311"
            or state["singlet"] != "{s}"
            or state["closure"] != "27abc=1"
            or state["witness_count"] != count):
        raise ValueError("persistent kernel identity mismatch")
    return state, head, count


def append_scheduled_tick(path, run_id, source_revision="unknown"):
    path = Path(path)
    if not run_id or not run_id.isdecimal() or int(run_id) <= 0:
        raise ValueError("run_id must be a positive GitHub Actions integer")
    if not source_revision or len(source_revision) > 128:
        raise ValueError("invalid source revision")
    before = path.read_bytes()
    state, head, count = verify_ledger(path)
    for raw in before.splitlines():
        rec = json.loads(raw)
        if rec.get("workflow_run_id") == run_id:
            # Idempotency: do not re-apply a job that has already committed.
            return {"appended": False, "step": state["step"], "head": head, "records": count}
    beat = state["step"] % 5
    domain = "internal" if beat < 2 else "external"
    next_state = {**state, "step": state["step"] + 1, "witness_count": count + 1}
    next_state["phase_fifths"] += int(domain == "internal")
    next_state["phi_fifths"] += int(domain == "external")
    rec = event(
        head, count, "tick", provenance="synthetic:ada-scheduled",
        beat=beat + 1, domain=domain, state=next_state,
        workflow_run_id=run_id,
        source_revision=source_revision,
        created_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    line = (canonical(rec) + "\n").encode("utf-8")
    # Append, never replace; fail closed if the file changed after validation.
    if path.read_bytes() != before:
        raise RuntimeError("ledger changed between verify and append")
    with path.open("ab") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())
    after = path.read_bytes()
    if after != before + line:
        raise RuntimeError("prior evidence bytes were modified")
    observed, new_head, new_count = verify_ledger(path)
    if observed != next_state or new_count != count + 1 or new_head != rec["hash"]:
        raise RuntimeError("replay mismatch after append")
    return {"appended": True, "step": observed["step"],
            "head": new_head, "records": new_count, "beat": beat + 1, "domain": domain}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--source-revision", default="unknown")
    args = ap.parse_args()
    print(json.dumps(append_scheduled_tick(args.ledger, args.run_id, args.source_revision),
                     sort_keys=True))


if __name__ == "__main__":
    main()
