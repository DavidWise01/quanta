#!/usr/bin/env python3
"""ADA-069: cross-capture provenance, using only verified saved bytes.

A capture event is NOT a publication root and neither is an independent
measurement. No signature authentication is claimed. Original snapshots remain
unchanged; a new registry is created exclusively.
"""
import argparse
import json
import tempfile
from pathlib import Path
from ada055_candidates import hash_payload
from ada067_temporal import compare
from ada068_raw_capture import (SOURCE, ANCESTRY, make_record,
                                persist_create_only, verify, synthetic_fixture)

VERSION="ADA069-cross-capture-v1"


def inspect_capture(directory):
    directory=Path(directory)
    proof=verify(directory)
    record=json.loads((directory/"manifest.json").read_text(encoding="utf-8"))
    if record["source_ancestry"]!=ANCESTRY:
        raise ValueError("source ancestry mismatch")
    return {
        "capture_id":hash_payload({
            "schema":VERSION,
            "manifest":record,
            "body_sha256":proof["sha256"]
        }),
        "path":str(directory),
        "source_root":record["source_ancestry"],
        "body_sha256":proof["sha256"],
        "byte_length":proof["bytes"],
        "capture_time":record["capture_time_utc"],
        "provenance":record["capture_provenance"],
        "transport_claim":record["transport_claim"],
        "external_signature_verified":False,
    }


def compare_captures(first,second):
    left=inspect_capture(first)
    right=inspect_capture(second)
    delta=compare((Path(first)/"response.bin").read_bytes(),
                  (Path(second)/"response.bin").read_bytes(),
                  label="cross-capture")
    return {
        "left":left,"right":right,"delta":delta,
        "publication_roots":len({left["source_root"],right["source_root"]}),
        "capture_events":2,
        "independent_empirical_witness_roots":0,
        "authenticated_collector_attestations":0,
        "decision":"abstain",
    }


def record(entries, kind, payload):
    event={
        "seq":len(entries), "schema":VERSION,
        "kind":kind, "previous_hash":entries[-1]["hash"] if entries else None,
        "payload":payload,
    }
    event["hash"]=hash_payload(event)
    entries.append(event)
    return event


def verify_registry(entries):
    previous=None
    for index,event in enumerate(entries):
        if event["seq"]!=index or event["previous_hash"]!=previous:
            raise ValueError("broken registry chain")
        signed=dict(event)
        h=signed.pop("hash",None)
        if hash_payload(signed)!=h:
            raise ValueError("registry digest mismatch")
        if event["schema"]!=VERSION:
            raise ValueError("unexpected registry version")
        previous=h
    return True


def create_registry(path,entries):
    verify_registry(entries)
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("x",encoding="utf-8",newline="\n") as output:
        for row in entries:
            output.write(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n")
    return p


def fixture():
    """Both directories contain synthetic diagnostic bytes, not HTTP captures."""
    with tempfile.TemporaryDirectory() as root:
        base=Path(root)
        raw,first=synthetic_fixture()
        second_bytes=raw.replace(b"3 5",b"3 6")
        later=make_record(second_bytes,requested_url=SOURCE,final_url=SOURCE,
                          status=200,headers={"content-type":"text/plain"},
                          captured_at="2026-11-15T19:06:00+00:00",
                          method="fixture",provenance="synthetic-not-network",
                          verified_transport=False)
        persist_create_only(raw,first,base/"one")
        persist_create_only(second_bytes,later,base/"two")
        comparison=compare_captures(base/"one",base/"two")
        # No ephemeral temp paths in stable evidence, just fixed capture summaries.
        for key in ("left","right"):
            comparison[key].pop("path")
        events=[]
        record(events,"first-synthetic-capture",comparison["left"])
        record(events,"second-synthetic-capture",comparison["right"])
        record(events,"immutable-difference",comparison["delta"])
        record(events,"trust-gate",{
            "publication_roots":1,
            "independent_empirical_witness_roots":0,
            "externally_authenticated_attestations":0,
            "decision":"abstain"
        })
        verify_registry(events)
        return {"version":VERSION,"comparison":comparison,"events":events,
                "last_hash":events[-1]["hash"]}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--first",type=Path)
    p.add_argument("--second",type=Path)
    p.add_argument("--export",type=Path)
    p.add_argument("--verify-registry",type=Path)
    a=p.parse_args()
    if a.verify_registry:
        rows=[json.loads(s) for s in a.verify_registry.read_text().splitlines()]
        verify_registry(rows)
        print("PASS: create-only registry chain")
        return
    if a.first or a.second:
        if not a.first or not a.second:
            p.error("both --first and --second are required")
        report={"version":VERSION,"comparison":compare_captures(a.first,a.second)}
        events=[]
        record(events,"comparison",report["comparison"])
        report["events"]=events
    else:
        report=fixture()
    if a.export:
        create_registry(a.export,report["events"])
    print(json.dumps({
        "capture_events":report["comparison"]["capture_events"],
        "publication_roots":report["comparison"]["publication_roots"],
        "delta":report["comparison"]["delta"]["comparison"],
        "changed_bytes":len(report["comparison"]["delta"]["changed_offsets"]),
        "externally_authenticated_attestations":0,
        "promotion":"abstain",
    },indent=2))


if __name__=="__main__":
    main()
