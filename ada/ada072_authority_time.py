#!/usr/bin/env python3
"""ADA-072 signed registry authority and signed time claims.

Security boundary DEMONSTRATION ONLY. Authority and time-service keys are fixed,
publicly disclosed synthetic fixture keys; no independent real trust anchor.
An authenticated timestamp token is NOT proof of wall-clock correctness.
"""
import base64
import json
from datetime import datetime
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from ada055_candidates import hash_payload
from ada070_attestation import canonical, public_b64, collector_claim, sign_claim, verify_attestation
from ada069_lineage import fixture as lineage_fixture

VERSION="ADA072-authority-time-v1"
COLLECTOR="fixture-collector-not-external"
AUTHORITY_KEY=Ed25519PrivateKey.from_private_bytes(bytes([0x33])*32)
TIME_KEY=Ed25519PrivateKey.from_private_bytes(bytes([0x44])*32)
OLD_KEY=Ed25519PrivateKey.from_private_bytes(bytes([0x11])*32)
NEW_KEY=Ed25519PrivateKey.from_private_bytes(bytes([0x22])*32)
PINNED_AUTHORITY=public_b64(AUTHORITY_KEY)
PINNED_TIME_SERVICE=public_b64(TIME_KEY)
TIMES=("2026-11-15T20:00:00+00:00","2026-11-15T20:01:00+00:00",
       "2026-11-15T20:02:00+00:00")

def sign(private, value):
    return base64.b64encode(private.sign(canonical(value))).decode("ascii")

def verify_sig(public_b64, value, signature):
    try:
        key=Ed25519PublicKey.from_public_bytes(base64.b64decode(public_b64,validate=True))
        key.verify(base64.b64decode(signature,validate=True),canonical(value))
        return True
    except (ValueError,InvalidSignature,TypeError):
        return False

def new_event(events,action,key_id,public_key,*,recorded_at):
    """A signed update and a separate signed time assertion bound to its hash."""
    if action not in ("enroll","revoke"):
        raise ValueError("unsupported update")
    claim={"schema":VERSION,"seq":len(events),"prev_hash":events[-1]["hash"] if events else None,
           "collector":COLLECTOR,"action":action,"key_id":key_id,"key_public":public_key}
    signed={"claim":claim,"authority_signature":sign(AUTHORITY_KEY,claim)}
    event_digest=hash_payload(signed)
    time_claim={"schema":VERSION,"event_hash":event_digest,"observed_time":recorded_at,
                "service":"synthetic-time-service"}
    event={"claim":claim,"authority_signature":signed["authority_signature"],
           "hash":event_digest,"time_claim":time_claim,
           "time_signature":sign(TIME_KEY,time_claim)}
    events.append(event)
    return event

def replay(events,*,authority=PINNED_AUTHORITY,time_service=PINNED_TIME_SERVICE):
    active=None
    seen=set()
    last_hash=None
    last_time=None
    for seq,event in enumerate(events):
        claim=event["claim"]
        if claim["schema"]!=VERSION or claim["collector"]!=COLLECTOR:
            raise ValueError("wrong registry domain")
        if claim["seq"]!=seq or claim["prev_hash"]!=last_hash:
            raise ValueError("broken authority chain")
        if not verify_sig(authority,claim,event["authority_signature"]):
            raise ValueError("untrusted registry authority signature")
        signed={"claim":claim,"authority_signature":event["authority_signature"]}
        if event["hash"]!=hash_payload(signed):
            raise ValueError("registry content hash mismatch")
        token=event["time_claim"]
        if token.get("schema")!=VERSION or token.get("event_hash")!=event["hash"]:
            raise ValueError("unbound time token")
        if token.get("service")!="synthetic-time-service":
            raise ValueError("unexpected time issuer")
        if not verify_sig(time_service,token,event["time_signature"]):
            raise ValueError("untrusted time signature")
        stamp=datetime.fromisoformat(token["observed_time"])
        if stamp.tzinfo is None or (last_time is not None and stamp<=last_time):
            raise ValueError("timezone missing or nonmonotone trusted time claim")
        last_time=stamp
        identifier=claim["key_id"]
        public=claim["key_public"]
        if claim["action"]=="enroll":
            if active is not None or identifier in seen:
                raise ValueError("active key exists or key id reused")
            active=(identifier,public)
            seen.add(identifier)
        elif claim["action"]=="revoke":
            if active!=(identifier,public):
                raise ValueError("revocation does not match active key")
            active=None
        else:
            raise ValueError("unknown action")
        last_hash=event["hash"]
    return {"active_key_id":active[0] if active else None,
            "active_public_key":active[1] if active else None,
            "event_count":len(events),"last_event_hash":last_hash,
            "signed_time_claims":len(events)}

def authorize(packet,registry,*,required_key_id):
    state=replay(registry)
    if state["active_key_id"]!=required_key_id:
        return {"collector_signature":False,"current_authorization":False,
                "external_authority_authenticated":False,"promotion":"abstain"}
    result=verify_attestation(packet,{COLLECTOR:state["active_public_key"]})
    return {"collector_signature":result["valid"],
            "current_authorization":result["valid"],
            "external_authority_authenticated":False,"promotion":"abstain"}

def fixture():
    capture=lineage_fixture()["comparison"]["left"]
    claim=collector_claim(capture)
    old_packet=sign_claim(claim,OLD_KEY,COLLECTOR)
    new_packet=sign_claim(claim,NEW_KEY,COLLECTOR)
    oldpub=public_b64(OLD_KEY)
    newpub=public_b64(NEW_KEY)
    history=[]
    new_event(history,"enroll","key-v1",oldpub,recorded_at=TIMES[0])
    before=authorize(old_packet,history,required_key_id="key-v1")
    new_event(history,"revoke","key-v1",oldpub,recorded_at=TIMES[1])
    after=authorize(old_packet,history,required_key_id="key-v1")
    new_event(history,"enroll","key-v2",newpub,recorded_at=TIMES[2])
    stale=authorize(old_packet,history,required_key_id="key-v1")
    current=authorize(new_packet,history,required_key_id="key-v2")
    result={"version":VERSION,"authority_root":"synthetic:fixture-authority",
            "time_root":"synthetic:fixture-time","history":history,
            "before":before,"revoked":after,"stale":stale,"current":current,
            "state":replay(history),"external_authorities":0,
            "external_time_attestations":0,"empirical_witnesses":0,
            "promotion":"abstain"}
    return result

if __name__=="__main__":
    x=fixture()
    print(json.dumps({"signed_registry_events":x["state"]["event_count"],
     "signed_time_claims":x["state"]["signed_time_claims"],
     "old_authorized_before":x["before"]["current_authorization"],
     "old_authorized_after":x["revoked"]["current_authorization"],
     "new_authorized":x["current"]["current_authorization"],
     "real_trust_anchors":0,"promotion":"abstain"},indent=2))
