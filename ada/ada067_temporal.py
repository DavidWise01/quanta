#!/usr/bin/env python3
"""ADA-067 temporal source-integrity comparison without invented live captures.

Read-only base ADA-066. A new observation is append-only if explicitly exported.
Source publication ancestry is stable across captures, even when hashes differ.
"""
import argparse
import hashlib
import json
from pathlib import Path
from ada066_capture import CAPTURE, MANIFEST, verify as verify_066
from ada055_candidates import hash_payload

VERSION="ADA067-temporal-integrity-v1"
SOURCE="https://oeis.org/A003095/b003095.txt"
ANCESTRY="OEIS:A003095"
ACCESS="unavailable:403"
TIME="2026-11-15T18:06:00+00:00"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compare(original, candidate, *, label):
    """Byte-level comparison. Neither input is altered."""
    left, right = bytes(original), bytes(candidate)
    differences = [i for i in range(min(len(left),len(right))) if left[i]!=right[i]]
    # Record missing/added suffix indices; never truncate a failure report.
    differences += list(range(min(len(left),len(right)),max(len(left),len(right))))
    kind = "identical" if not differences else (
        "length_changed" if len(left)!=len(right) else "content_changed"
    )
    return {
        "label":label, "old_sha256":digest(left),"new_sha256":digest(right),
        "old_length":len(left), "new_length":len(right),
        "changed_offsets":differences, "comparison":kind,
        "same_publication_ancestry":True,
        "independent_new_witnesses":0,
    }


def record_event(events, kind, detail, *, observed_at=TIME):
    payload={
        "seq":len(events), "version":VERSION,"kind":kind,
        "source_url":SOURCE,"source_ancestry":ANCESTRY,
        "time_utc":observed_at,
        "previous_hash":events[-1]["hash"] if events else None,
        "detail":detail,
    }
    payload["hash"]=hash_payload(payload)
    events.append(payload)
    return payload


def verify_events(events):
    prior=None
    for n,event in enumerate(events):
        if event["seq"]!=n or event["previous_hash"]!=prior:
            raise ValueError("broken temporal event chain")
        if event["source_url"]!=SOURCE or event["source_ancestry"]!=ANCESTRY:
            raise ValueError("source ancestry changed")
        claimed=event["hash"]
        unsigned=dict(event)
        unsigned.pop("hash")
        if hash_payload(unsigned)!=claimed:
            raise ValueError("temporal event hash mismatch")
        prior=claimed
    return True


def build_fixture():
    previous=verify_066()
    baseline=CAPTURE.read_bytes()
    if digest(baseline)!=previous["capture_sha256"]:
        raise ValueError("ADA-066 baseline modified")
    events=[]
    record_event(events,"baseline-verified",{
        "sha256":digest(baseline),"length":len(baseline),
        "capture_kind":"normalized transcription, NOT upstream HTTP bytes"
    })
    record_event(events,"live-retrieval-unavailable",{
        "result":ACCESS,"captured_response_bytes":False,
        "new_snapshot_comparison":"not attempted; no fetched bytes"
    })
    identical=compare(baseline,baseline,label="synthetic-identical")
    altered=baseline.replace(b"5 677",b"5 678")
    changed=compare(baseline,altered,label="synthetic-content-mutation")
    truncated=compare(baseline,baseline[:-1],label="synthetic-truncation")
    for result in (identical,changed,truncated):
        record_event(events,"synthetic-diagnostic",result)
    verify_events(events)
    return {
        "version":VERSION,"source_url":SOURCE,
        "source_ancestry":ANCESTRY,
        "live_source_status":ACCESS,
        "actual_new_source_snapshot":False,
        "synthetic_diagnostics":[identical,changed,truncated],
        "events":events,
        "distinct_source_publications":1,
        "independent_empirical_witnesses":0,
        "promotion":"abstain",
        "last_event_hash":events[-1]["hash"],
    }


def export_create_only(path,events):
    output=Path(path)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("x",encoding="utf-8",newline="\n") as file:
        for event in events:
            file.write(json.dumps(event,sort_keys=True,separators=(",",":"))+"\n")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--export",type=Path)
    parser.add_argument("--verify",type=Path)
    args=parser.parse_args()
    if args.verify:
        rows=[json.loads(line) for line in args.verify.read_text().splitlines()]
        verify_events(rows)
        print("PASS: hash-linked temporal archive")
        return
    report=build_fixture()
    if args.export:
        export_create_only(args.export,report["events"])
    print(json.dumps({
        "baseline_sha256":report["events"][0]["detail"]["sha256"],
        "live_source_status":report["live_source_status"],
        "comparisons":[(r["label"],r["comparison"],len(r["changed_offsets"]))
                       for r in report["synthetic_diagnostics"]],
        "events":len(report["events"]),
        "independent_witnesses":0,
        "promotion":"abstain",
    },indent=2))


if __name__=="__main__":
    main()
