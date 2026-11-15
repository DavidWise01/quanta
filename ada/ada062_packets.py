#!/usr/bin/env python3
"""ADA-062 evidence-carrying observation packets (standard library).

All bundled cases are synthetic. A packet hash confirms byte consistency, NOT
independent origin, truthful measurement, or external verification.
No writes to the operational scheduled kernel.
"""
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import json
from ada055_candidates import hash_payload, closure
from ada061_witness import check_packets

EXPERIMENT="ADA-062-v1"
CLAIM="27abc=1"
FIXTURE_TIME="2026-11-15T16:57:00+00:00"
OWNED_ROOT="synthetic:quanta-owned"
ROOTS=("synthetic:lab-A","synthetic:lab-B","synthetic:lab-C")

def exact_replay(values):
    if not isinstance(values,(list,tuple)) or len(values)!=3:
        raise ValueError("three exact rational inputs required")
    a,b,c=(Fraction(x) for x in values)
    return str(closure((a,b,c)))

def packet(source_root, source_id, candidate_root, values, *,
           captured=FIXTURE_TIME, derived_from=(), declared_result=None,
           origin="simulation"):
    if not source_root or not source_id or not candidate_root:
        raise ValueError("source identity, ancestry, and candidate required")
    timestamp=datetime.fromisoformat(captured.replace("Z","+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("timezone is required")
    state=[str(Fraction(x)) for x in values]
    actual=exact_replay(state)
    observed=actual if declared_result is None else str(declared_result)
    body={
        "schema":EXPERIMENT, "source_root":source_root,
        "source_id":source_id, "candidate_root":candidate_root,
        "capture_time":timestamp.isoformat(), "claim":CLAIM,
        "input":state,"reported_output":observed,
        "replay_method":"fractions.Fraction; 27*a*b*c",
        "origin":origin, "derived_from":list(derived_from),
    }
    body["digest"]=hash_payload(body)
    return body

def validate(p):
    body=dict(p); claimed=body.pop("digest",None)
    if claimed != hash_payload(body):
        raise ValueError("packet digest mismatch")
    required=("source_root","source_id","candidate_root","capture_time","claim",
              "input","reported_output","replay_method","origin","derived_from")
    if any(not body.get(k) and body.get(k)!=[] for k in required):
        raise ValueError("missing evidence field")
    if body["schema"]!=EXPERIMENT or body["claim"]!=CLAIM:
        raise ValueError("unknown experiment or claim")
    if body["replay_method"]!="fractions.Fraction; 27*a*b*c":
        raise ValueError("unknown replay method")
    t=datetime.fromisoformat(body["capture_time"])
    if t.tzinfo is None:
        raise ValueError("timestamp without timezone")
    actual=exact_replay(body["input"])
    return {"replay_match":actual==body["reported_output"],
            "actual":actual, "claimed":body["reported_output"],
            "root":body["source_root"],"digest":claimed}

def assess(packets, target, authorized_roots=()):
    normalized=[]; seen_roots=set(); actual_results=[]
    for p in packets:
        observation=validate(p)
        if p["candidate_root"]!=target:
            raise ValueError("candidate mismatch")
        if p["source_root"] in seen_roots and p["origin"]=="measured" and not p["derived_from"]:
            # Do not allow repeated source-root measurements to masquerade as three roots.
            pass
        seen_roots.add(p["source_root"])
        actual_results.append(observation)
        if p["origin"]=="measured" and not p["derived_from"] and observation["replay_match"]:
            normalized.append({
                "candidate_root":target, "source_root":p["source_root"],
                "observed_replay":observation["actual"]=="1", "origin":"measured",
                "copied_from":None
            })
        else:
            normalized.append({
                "candidate_root":target, "source_root":p["source_root"],
                "observed_replay":False, "origin":"simulation",
                "copied_from":p["derived_from"][0] if p["derived_from"] else None
            })
        normalized[-1]["digest"]=hash_payload(normalized[-1])
    gate=check_packets(normalized,target,True,authorized_roots=authorized_roots)
    # Even three self-declared measured sources must not become real-world
    # authenticated evidence merely because their fields appear plausible.
    if gate["decision"]=="eligible":
        return {"decision":"abstain", "reason":"source independence not externally authenticated",
                "declared_gate":"eligible", "root_count":gate["independent_roots"],
                "observations":actual_results}
    return {"decision":gate["decision"],"reason":gate["reason"],
            "declared_gate":gate["decision"],"root_count":gate["independent_roots"],
            "observations":actual_results}

def fixture():
    target="synthetic-candidate-062"
    state=("1","1/9","1/3")
    samples=[packet(root,"experiment:"+root,target,state) for root in ROOTS]
    samples.append(packet(OWNED_ROOT,"quanta-owned-mirror",target,state,
                          derived_from=("github-owned",)))
    failing=packet(ROOTS[0],"wrong-output",target,state,declared_result="3")
    return {"claim":CLAIM,"target":target,"packets":samples+[failing],
            "simulated_result":assess(samples,target,authorized_roots=ROOTS),
            "incorrect_result_replay":validate(failing),
            "real_independent_witnesses":0,
            "promotion":"abstain"}

if __name__=="__main__":
    print(json.dumps(fixture(),indent=2))
