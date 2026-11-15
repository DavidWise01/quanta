#!/usr/bin/env python3
"""ADA-070: Ed25519 collector attestation over immutable capture provenance.

A valid signature proves possession of a trusted collector signing key, not
publication authorship, source independence, or an observed physical result.
Requires the third-party Python 'cryptography' package.
"""
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from ada055_candidates import hash_payload
from ada069_lineage import fixture as lineage_fixture

VERSION="ADA070-ed25519-v1"
TEST_SEED=b"\x11"*32
TEST_COLLECTOR="fixture-collector-not-external"
SOURCE_ROOT="OEIS:A003095"


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")


def public_b64(private_key):
    return base64.b64encode(private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )).decode("ascii")


def collector_claim(capture):
    needed=("capture_id","body_sha256","byte_length","source_root",
            "capture_time","provenance")
    if any(k not in capture for k in needed):
        raise ValueError("incomplete capture claim")
    if capture["source_root"]!=SOURCE_ROOT:
        raise ValueError("unexpected publication root")
    return {"version":VERSION, "capture_id":capture["capture_id"],
            "body_sha256":capture["body_sha256"],
            "byte_length":capture["byte_length"],
            "source_root":capture["source_root"],
            "capture_time":capture["capture_time"],
            "capture_provenance":capture["provenance"]}


def sign_claim(claim,private_key,collector_id):
    if claim.get("version")!=VERSION or not collector_id:
        raise ValueError("invalid signing context")
    signature=private_key.sign(canonical(claim))
    return {"collector_id":collector_id,"claim":claim,
            "signature_ed25519_b64":base64.b64encode(signature).decode("ascii")}


def verify_attestation(packet, trusted_keys):
    collector=packet.get("collector_id")
    if collector not in trusted_keys:
        return {"valid":False,"reason":"untrusted collector key",
                "publication_verified":False,"promotion":"abstain"}
    try:
        claim=packet["claim"]
        if claim["version"]!=VERSION or claim["source_root"]!=SOURCE_ROOT:
            raise ValueError("unrecognized claim")
        encoded=base64.b64decode(packet["signature_ed25519_b64"],validate=True)
        keybytes=base64.b64decode(trusted_keys[collector],validate=True)
        Ed25519PublicKey.from_public_bytes(keybytes).verify(encoded,canonical(claim))
    except (KeyError,ValueError,TypeError,InvalidSignature):
        return {"valid":False,"reason":"signature or claim failed",
                "publication_verified":False,"promotion":"abstain"}
    return {"valid":True,"reason":"collector signature valid",
            "publication_verified":False,"promotion":"abstain"}


def fixture():
    lineage=lineage_fixture()
    left=lineage["comparison"]["left"]
    right=lineage["comparison"]["right"]
    private=Ed25519PrivateKey.from_private_bytes(TEST_SEED)
    trusted={TEST_COLLECTOR:public_b64(private)}
    a=sign_claim(collector_claim(left),private,TEST_COLLECTOR)
    b=sign_claim(collector_claim(right),private,TEST_COLLECTOR)
    results=[verify_attestation(x,trusted) for x in (a,b)]
    report={
        "version":VERSION,"publication_root":SOURCE_ROOT,
        "collector_id":TEST_COLLECTOR,"key_role":"synthetic test key; not deployed",
        "trusted_public_key_b64":trusted[TEST_COLLECTOR],
        "capture_claims":[a,b],"verifications":results,
        "valid_signatures":sum(x["valid"] for x in results),
        "unique_collector_keys":1,"publication_roots":1,
        "externally_authenticated_collectors":0,
        "independent_empirical_witnesses":0,"promotion":"abstain",
    }
    report["digest"]=hash_payload(report)
    return report


if __name__=="__main__":
    x=fixture()
    print(json.dumps({"valid_signatures":x["valid_signatures"],
        "unique_collector_keys":x["unique_collector_keys"],
        "publication_roots":x["publication_roots"],
        "externally_authenticated_collectors":x["externally_authenticated_collectors"],
        "empirical_witnesses":x["independent_empirical_witnesses"],
        "promotion":x["promotion"],"digest":x["digest"]},indent=2))
