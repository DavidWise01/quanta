#!/usr/bin/env python3
"""ADA-071: append-only collector key lifecycle with fail-closed trust gate.

Synthetic trust roots only. Registry state controls CURRENT authorization.
Valid Ed25519 signatures do not establish external source truth or witnesses.
Requires 'cryptography'; leaves ADA-070 and scheduled ADA ledger untouched.
"""
import copy
import json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from ada055_candidates import hash_payload
from ada070_attestation import (canonical, public_b64, collector_claim,
                                sign_claim, verify_attestation)
from ada069_lineage import fixture as lineage_fixture

VERSION="ADA071-key-registry-v1"
COLLECTOR="fixture-collector-not-external"
OLD_KEY=Ed25519PrivateKey.from_private_bytes(bytes.fromhex("11"*32))
NEW_KEY=Ed25519PrivateKey.from_private_bytes(bytes.fromhex("22"*32))


def event(events, action, key_id, public_key, *, epoch):
    """Add a deterministic integrity-linked lifecycle event."""
    if action not in ("enroll", "revoke"):
        raise ValueError("unknown lifecycle operation")
    record={
        "seq":len(events),"version":VERSION,"epoch":epoch,
        "action":action,"collector_id":COLLECTOR,
        "key_id":key_id,"public_key_ed25519_b64":public_key,
        "prev_hash":events[-1]["hash"] if events else None,
        "trust_origin":"synthetic-local-pinning",
    }
    record["hash"]=hash_payload(record)
    events.append(record)
    return record


def registry_state(events):
    """Validate full lineage and calculate currently authorized identity."""
    seen=set()
    active=None
    previous=None
    previous_epoch=-1
    for i,r in enumerate(events):
        unsigned=dict(r)
        claimed=unsigned.pop("hash",None)
        if r["seq"]!=i or r["prev_hash"]!=previous:
            raise ValueError("broken lifecycle chain")
        if r["version"]!=VERSION or r["collector_id"]!=COLLECTOR:
            raise ValueError("unexpected registry identity")
        if hash_payload(unsigned)!=claimed:
            raise ValueError("tampered registry")
        if type(r["epoch"]) is not int or r["epoch"]<=previous_epoch:
            raise ValueError("non-monotone epoch")
        if r["action"]=="enroll":
            if active is not None or r["key_id"] in seen:
                raise ValueError("active key or reused key identifier")
            active=(r["key_id"],r["public_key_ed25519_b64"])
            seen.add(r["key_id"])
        elif r["action"]=="revoke":
            if active is None or active!=(r["key_id"],r["public_key_ed25519_b64"]):
                raise ValueError("revocation does not match active key")
            active=None
        else:
            raise ValueError("unknown registry action")
        previous=claimed
        previous_epoch=r["epoch"]
    return {"active_key_id":active[0] if active else None,
            "active_public_key":active[1] if active else None,
            "events":len(events),"last_hash":previous,
            "trust_origin":"synthetic-local-pinning"}


def verify_at_epoch(packet, events, *, evaluation_epoch, required_key_id):
    """Do not trust historical authorization after a key is revoked."""
    if type(evaluation_epoch) is not int or not events or evaluation_epoch<events[-1]["epoch"]:
        raise ValueError("stale or invalid evaluation epoch")
    state=registry_state(events)
    if state["active_key_id"]!=required_key_id:
        return {"signature_valid":False,"authorized_now":False,
                "reason":"key revoked, replaced or unknown",
                "external_identity_authenticated":False,"promotion":"abstain"}
    result=verify_attestation(packet,{COLLECTOR:state["active_public_key"]})
    return {"signature_valid":result["valid"],"authorized_now":result["valid"],
            "reason":result["reason"],
            "external_identity_authenticated":False,"promotion":"abstain"}


def fixture():
    capture=lineage_fixture()["comparison"]["left"]
    claim=collector_claim(capture)
    original=sign_claim(claim,OLD_KEY,COLLECTOR)
    replacement=sign_claim(claim,NEW_KEY,COLLECTOR)
    entries=[]
    old_pub=public_b64(OLD_KEY)
    new_pub=public_b64(NEW_KEY)
    event(entries,"enroll","key-v1",old_pub,epoch=1)
    before=verify_at_epoch(original,entries,evaluation_epoch=1,required_key_id="key-v1")
    event(entries,"revoke","key-v1",old_pub,epoch=2)
    revoked=verify_at_epoch(original,entries,evaluation_epoch=2,required_key_id="key-v1")
    event(entries,"enroll","key-v2",new_pub,epoch=3)
    prior_key=verify_at_epoch(original,entries,evaluation_epoch=3,required_key_id="key-v1")
    rotated=verify_at_epoch(replacement,entries,evaluation_epoch=3,required_key_id="key-v2")
    state=registry_state(entries)
    return {"version":VERSION,"lifecycle":entries,"state":state,
            "before_rotation":before,"revoked_key":revoked,
            "prior_key_after_rotation":prior_key,"new_key":rotated,
            "source_ancestry":"OEIS:A003095",
            "distinct_external_collectors":0,
            "independent_empirical_witnesses":0,
            "promotion":"abstain"}


if __name__=="__main__":
    f=fixture()
    print(json.dumps({
        "lifecycle_events":len(f["lifecycle"]),
        "old_key_initially_valid":f["before_rotation"]["authorized_now"],
        "revoked_key_authorized":f["revoked_key"]["authorized_now"],
        "rotated_key_authorized":f["new_key"]["authorized_now"],
        "independent_empirical_witnesses":0,
        "promotion":"abstain","last_hash":f["state"]["last_hash"]
    },indent=2))
