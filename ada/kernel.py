#!/usr/bin/env python3
"""ADA-046 deterministic, append-only, hash-linked manifold kernel.
Standard library only. This is a mathematical fixture, not physical quantum dynamics.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from fractions import Fraction

GENESIS = "ADA-046-GENESIS"
ROLES = ["Josephson:-1", "Mandelbrot:0", "Juliet:+1"]
MANIFOLD = "{[({s})]}"

def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()

def fresh():
    return {"step": 0, "phase_fifths": 0, "phi_fifths": 0,
            "box": "constant:1311", "singlet": "{s}", "manifold": MANIFOLD,
            "roles": list(ROLES), "closure": "27abc=1", "witness_count": 0}

def event(prev, seq, kind, provenance="synthetic:ada-owned", **kwargs):
    data = {"seq": seq, "prev": prev, "kind": kind,
            "ancestry": provenance, **kwargs}
    data["hash"] = digest(data)
    return data

def advance(state, record):
    kind = record["kind"]
    out = dict(state)
    if kind == "genesis":
        if record["seq"] != 0:
            raise ValueError("genesis must be first")
    elif kind == "tick":
        expected_beat = state["step"] % 5
        expected_domain = "internal" if expected_beat < 2 else "external"
        if record.get("beat") != expected_beat + 1 or record.get("domain") != expected_domain:
            raise ValueError("wrong five-beat schedule")
        out["step"] += 1
        if expected_domain == "internal":
            out["phase_fifths"] += 1
        else:
            out["phi_fifths"] += 1
    elif kind == "recover":
        if record.get("phase_delta_fifths") != -state["phase_fifths"]:
            raise ValueError("recovery phase must invert prior value")
        if record.get("phi_delta_fifths") != -state["phi_fifths"]:
            raise ValueError("recovery scale must invert prior value")
        out["phase_fifths"] += record["phase_delta_fifths"]
        out["phi_fifths"] += record["phi_delta_fifths"]
    else:
        raise ValueError("unknown operation")
    out["witness_count"] += 1
    if record.get("state") != out:
        raise ValueError("state snapshot does not match replay")
    return out

def replay(path):
    state = fresh()
    previous = GENESIS
    count = 0
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.endswith("\n"):
                raise ValueError("incomplete or nonterminated JSONL record")
            rec = json.loads(line)
            if rec.get("seq") != count or rec.get("prev") != previous:
                raise ValueError("sequence/parent hash mismatch")
            signed = dict(rec)
            claimed = signed.pop("hash", None)
            if claimed != digest(signed):
                raise ValueError("content hash mismatch")
            if not isinstance(rec.get("ancestry"), str) or not rec["ancestry"]:
                raise ValueError("source ancestry missing")
            if count == 0 and rec["kind"] != "genesis":
                raise ValueError("missing genesis")
            if count > 0 and rec["kind"] == "genesis":
                raise ValueError("duplicate genesis")
            state = advance(state, rec)
            previous = claimed
            count += 1
    if count == 0:
        raise ValueError("empty ledger")
    return state, previous, count

def genesis(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = fresh()
    data = event(GENESIS, 0, "genesis", state={**state, "witness_count": 1})
    # x prevents replacing a pre-existing evidence ledger
    with path.open("x", encoding="utf-8") as f:
        f.write(canonical(data) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return data

def append(path, kind, ancestry):
    state, head, count = replay(path)
    if kind == "tick":
        beat = state["step"] % 5
        attrs = {"beat": beat + 1, "domain": "internal" if beat < 2 else "external"}
    elif kind == "recover":
        attrs = {"phase_delta_fifths": -state["phase_fifths"],
                 "phi_delta_fifths": -state["phi_fifths"]}
    else:
        raise ValueError("invalid command")
    next_state = {**state, "witness_count": state["witness_count"] + 1}
    if kind == "tick":
        next_state["step"] += 1
        next_state["phase_fifths"] += int(attrs["domain"] == "internal")
        next_state["phi_fifths"] += int(attrs["domain"] == "external")
    else:
        next_state["phase_fifths"] = 0
        next_state["phi_fifths"] = 0
    rec = event(head, count, kind, provenance=ancestry, state=next_state, **attrs)
    # single-writer assumption; always verify before appending
    with Path(path).open("a", encoding="utf-8") as f:
        f.write(canonical(rec) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return replay(path)[0]

def classification(s):
    n = s["step"]
    return {
        "address_return": n > 0 and n % 11 == n % 5 == n % 2 == 0,
        "algebraic_return": True,  # exact reciprocal phi-exponent representation
        "geometric_return": s["phase_fifths"] % 10 == 0 and s["phi_fifths"] == 0,
        "ancestry_replay_valid": True,
        "phase_pi": str(Fraction(s["phase_fifths"], 5)),
        "phi_exponent": str(Fraction(s["phi_fifths"], 5)),
    }

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["init", "tick", "recover", "verify", "status"])
    ap.add_argument("--ledger", default="ada/kernel/events.jsonl")
    ap.add_argument("--ancestry", default="synthetic:ada-owned")
    ap.add_argument("--count", type=int, default=1)
    args = ap.parse_args()
    if args.command == "init":
        genesis(args.ledger)
    elif args.command in ("tick", "recover"):
        if not (1 <= args.count <= 100000):
            ap.error("--count must be 1..100000")
        if args.command == "recover" and args.count != 1:
            ap.error("recover only accepts one correction event")
        for _ in range(args.count):
            append(args.ledger, args.command, args.ancestry)
    state, head, count = replay(args.ledger)
    print(json.dumps({"records": count, "head": head, "state": state,
                      "returns": classification(state)}, indent=2))

if __name__ == "__main__":
    main()
