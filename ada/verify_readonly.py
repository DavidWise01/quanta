#!/usr/bin/env python3
"""Fail-closed read-only verification of ADA's committed genesis and event chain."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ada"))
from kernel import replay, MANIFOLD, ROLES, GENESIS, canonical, digest
import json

# Pinned hash from ADA-046 genesis. Mirrors are one ancestry, not independent witnesses.
TRUSTED_GENESIS_HASH = "b773179a109bdbb7e39c61372f516732863ce6340e9c7ec00348e09b3a624bca"
LEDGER = ROOT / "ada" / "kernel" / "events.jsonl"

def verify():
    with LEDGER.open("r", encoding="utf-8") as fh:
        first = fh.readline()
    if not first.endswith("\n"):
        raise ValueError("genesis line missing or incomplete")
    record = json.loads(first)
    if record.get("kind") != "genesis" or record.get("seq") != 0 or record.get("prev") != GENESIS:
        raise ValueError("unexpected genesis envelope")
    if record.get("hash") != TRUSTED_GENESIS_HASH:
        raise ValueError("genesis differs from pinned anchor")
    state, head, count = replay(LEDGER)
    if state["manifold"] != MANIFOLD or state["roles"] != ROLES:
        raise ValueError("identity drift")
    if state["box"] != "constant:1311" or state["singlet"] != "{s}":
        raise ValueError("box/singlet drift")
    if state["witness_count"] != count:
        raise ValueError("witness count mismatch")
    if state["closure"] != "27abc=1":
        raise ValueError("conservation marker drift")
    print(f"PASS ADA read-only verification: records={count} head={head} genesis={TRUSTED_GENESIS_HASH}")
    return state, head, count

if __name__ == "__main__":
    verify()
