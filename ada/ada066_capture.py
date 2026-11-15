#!/usr/bin/env python3
"""ADA-066 immutable normalized excerpt capture verification.

This records a reproducible copied excerpt, not original upstream HTTP bytes.
Never rewrite the committed capture; verify SHA-256, expected content and orbit.
"""
from pathlib import Path
import hashlib
import json
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
CAPTURE=ROOT/"ada-066-oeis-excerpt.txt"
MANIFEST=ROOT/"ada-066-capture.json"
EXPECTED_SHA="7ccd51e94cae1ec6d1fc0df3fce2d4adfb8737b618f9ea243c404c950f232169"

def verify(capture=CAPTURE,manifest=MANIFEST):
    m=json.loads(Path(manifest).read_text(encoding="utf-8"))
    raw=Path(capture).read_bytes()
    actual=hashlib.sha256(raw).hexdigest()
    if actual!=EXPECTED_SHA or m["transcript_sha256"]!=EXPECTED_SHA:
        raise ValueError("immutable excerpt SHA-256 mismatch")
    if len(raw)!=m["transcript_size_bytes"]:
        raise ValueError("capture size mismatch")
    if m["authenticated_original_response"] is not False:
        raise ValueError("raw upstream response is not authenticated")
    if m["independent_empirical_witness_roots"]!=0 or m["promotion"]!="abstain":
        raise ValueError("unsupported evidence promotion")
    lines=raw.decode("utf-8").splitlines()
    parsed=[]
    for index,line in enumerate(lines):
        n,v=line.split(" ")
        if int(n)!=index:
            raise ValueError("noncontiguous reference index")
        parsed.append(int(v))
    if len(parsed)!=8:
        raise ValueError("unexpected reference length")
    z=0
    for n,reference in enumerate(parsed):
        if z!=reference:
            raise ValueError("frozen orbit engine differs from archived reference")
        z=z*z+1
    return {"reference_terms":len(parsed),"matches":len(parsed),
            "capture_sha256":actual,"archive_kind":m["archive_kind"],
            "physical_witnesses":0,"promotion":"abstain"}

if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
