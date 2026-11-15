#!/usr/bin/env python3
"""ADA-068: fail-closed raw capture with immutable bytes and provenance metadata.

The fetch operation has not succeeded in the supplied ADA-068 example:
fixtures are simulated. Byte hashes certify retained bytes, not source truth.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

SOURCE="https://oeis.org/A003095/b003095.txt"
ANCESTRY="OEIS:A003095"
VERSION="ADA068-raw-capture-v1"
ALLOWED_URLS={SOURCE}
HEADER_NAMES=("content-type","etag","last-modified","content-length")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def _utc(when=None):
    return when or datetime.now(timezone.utc).isoformat()


def make_record(data, *, requested_url, final_url, status, headers, captured_at=None,
                method="https-GET", provenance="network", verified_transport=True):
    """Capture metadata from actual response supplied by caller."""
    if requested_url not in ALLOWED_URLS or final_url not in ALLOWED_URLS:
        raise ValueError("unapproved URL or redirect")
    if status!=200:
        raise ValueError("response not HTTP 200")
    if not isinstance(data,bytes):
        raise TypeError("capture requires exact bytes")
    if not data:
        raise ValueError("empty response")
    safe_headers={name:headers[name] for name in HEADER_NAMES if name in headers}
    return {
        "schema":VERSION, "requested_url":requested_url,"final_url":final_url,
        "source_ancestry":ANCESTRY, "http_status":status,
        "capture_time_utc":_utc(captured_at),"method":method,
        "response_headers":safe_headers,
        "response_body_sha256":sha(data),"response_body_length":len(data),
        "capture_provenance":provenance,
        "transport_claim":verified_transport,
        "independent_witness_roots":0,
        "promotion":"abstain",
    }


def persist_create_only(data, record, directory):
    """Two exclusive files; no silent overwrite of previous evidence.

    The destination must be a fresh empty directory; if either create fails,
    the caller must inspect partial files rather than treating it as success.
    """
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    if any(directory.iterdir()):
        raise FileExistsError("capture directory must be empty")
    capture=directory/"response.bin"
    manifest=directory/"manifest.json"
    with capture.open("xb") as fp:
        fp.write(data)
    with manifest.open("x",encoding="utf-8") as fp:
        json.dump(record,fp,sort_keys=True,indent=2)
        fp.write("\n")
    verify(directory)
    return directory


def verify(directory):
    directory=Path(directory)
    data=(directory/"response.bin").read_bytes()
    m=json.loads((directory/"manifest.json").read_text(encoding="utf-8"))
    if m["schema"]!=VERSION or m["source_ancestry"]!=ANCESTRY:
        raise ValueError("manifest schema or ancestry mismatch")
    if m["requested_url"]!=SOURCE or m["final_url"]!=SOURCE:
        raise ValueError("unexpected URL")
    if m["http_status"]!=200:
        raise ValueError("unexpected HTTP status")
    if sha(data)!=m["response_body_sha256"] or len(data)!=m["response_body_length"]:
        raise ValueError("raw capture mismatch")
    if m["promotion"]!="abstain" or m["independent_witness_roots"]!=0:
        raise ValueError("unsupported promotion or witness count")
    return {"sha256":sha(data),"bytes":len(data),"source_ancestry":ANCESTRY,
            "transport_claim":m["transport_claim"],"promotion":"abstain"}


def fetch(directory, *, timeout=12):
    request=Request(SOURCE,headers={"User-Agent":"ADA068-Quanta-Reference-Verification/1.0"})
    with urlopen(request,timeout=timeout) as response:
        final=response.geturl()
        if final!=SOURCE:
            raise ValueError("unapproved HTTP redirect")
        raw=response.read()
        headers={k.lower():v for k,v in response.headers.items()}
        record=make_record(raw,requested_url=SOURCE,final_url=final,
                           status=response.status,headers=headers,
                           provenance="live-https-response",verified_transport=True)
    persist_create_only(raw,record,directory)
    return verify(directory)


def synthetic_fixture():
    raw=b"0 0\n1 1\n2 2\n3 5\n"
    record=make_record(raw,requested_url=SOURCE,final_url=SOURCE,
                       status=200,headers={"content-type":"text/plain"},
                       captured_at="2026-11-15T18:06:00+00:00",
                       method="fixture",provenance="synthetic-not-network",
                       verified_transport=False)
    return raw,record


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--fetch",type=Path,help="create new raw snapshot directory")
    p.add_argument("--verify",type=Path,help="verify existing capture")
    p.add_argument("--fixture",type=Path,help="create synthetic diagnostic only")
    args=p.parse_args()
    if sum(x is not None for x in (args.fetch,args.verify,args.fixture))!=1:
        p.error("choose exactly one action")
    if args.fetch is not None:
        result=fetch(args.fetch)
    elif args.verify is not None:
        result=verify(args.verify)
    else:
        raw,record=synthetic_fixture()
        persist_create_only(raw,record,args.fixture)
        result=verify(args.fixture)
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
