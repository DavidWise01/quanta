#!/usr/bin/env python3
"""ADA-073: governance independence before external trust.

A correctly signed governance statement is not independently governed merely
because a different synthetic key signs it. Fail closed on shared ancestry,
unauthenticated trust roots, missing input bindings and copied evidence.
"""
import json
from ada055_candidates import hash_payload
from ada072_authority_time import fixture as signed_fixture
from ada070_attestation import canonical

VERSION="ADA073-governance-independence-v1"
OWNED="synthetic:quanta-owned-corpus"
GOVERNANCE_ID="fixture-governance"
SOURCE_ROOT="OEIS:A003095"


def governance_packet(*, key_id, registry_hash, capture_sha, source_root=SOURCE_ROOT,
                      root=OWNED, copied_from=None, verified_identity=False):
    """Evidence statement about governance, not a proof of its independence."""
    if not key_id or not registry_hash or not capture_sha:
        raise ValueError("incomplete governance binding")
    body={"version":VERSION,"governor":GOVERNANCE_ID,
          "governance_root":root,"copied_from":copied_from,
          "key_id":key_id,"registry_hash":registry_hash,
          "capture_sha256":capture_sha,"publication_source_root":source_root,
          "identity_independently_authenticated":bool(verified_identity)}
    body["hash"]=hash_payload(body)
    return body


def evaluate(packets, *, registry_hash, capture_sha, key_id,
             owned_ancestry=OWNED, trusted_external_roots=()):
    """No promotions with unverified identities or publication-root overlap."""
    examined=[]
    eligible=set()
    for p in packets:
        body=dict(p)
        digest=body.pop("hash",None)
        if digest!=hash_payload(body):
            raise ValueError("tampered governance packet")
        if p["version"]!=VERSION:
            raise ValueError("incorrect governance version")
        if (p["registry_hash"]!=registry_hash or
            p["capture_sha256"]!=capture_sha or p["key_id"]!=key_id or
            p["publication_source_root"]!=SOURCE_ROOT):
            raise ValueError("governance statement bound to different evidence")
        external=(p["governance_root"] in trusted_external_roots
                  and p["governance_root"]!=owned_ancestry
                  and p["governance_root"]!=SOURCE_ROOT
                  and p["copied_from"] is None
                  and p["identity_independently_authenticated"])
        if external:
            eligible.add(p["governance_root"])
        examined.append({"root":p["governance_root"],"external_root_eligible":external,
                         "copied":p["copied_from"] is not None,
                         "identity_verified":p["identity_independently_authenticated"]})
    return {"evaluated":len(examined),"eligible_governance_roots":len(eligible),
            "evidence":examined,"publication_roots":1,
            "independent_empirical_witnesses":0,"promotion":"abstain",
            "reason":"collector governance does not verify external empirical observations"}


def fixture():
    upstream=signed_fixture()
    last=upstream["state"]["last_event_hash"]
    claim=upstream["history"][-1]["claim"]
    capture_hash=hash_payload({"experiment":"ADA073","upstream":last})
    key_id=claim["key_id"]
    packets=[
        governance_packet(key_id=key_id,registry_hash=last,capture_sha=capture_hash),
        governance_packet(key_id=key_id,registry_hash=last,capture_sha=capture_hash,
                          root="synthetic:public-mirror",copied_from=OWNED),
        governance_packet(key_id=key_id,registry_hash=last,capture_sha=capture_hash,
                          root="synthetic:separately-labeled-key",
                          verified_identity=False),
    ]
    result=evaluate(packets,registry_hash=last,capture_sha=capture_hash,
                    key_id=key_id)
    return {"version":VERSION,"upstream_authority_events":len(upstream["history"]),
            "trusted_registry_hash":last,"test_capture_binding":capture_hash,
            "governance_packets":packets,"gate":result,
            "true_external_authority_collected":False,
            "source_ancestry":"quanta-owned:synthetic-fixture",
            "promotion":"abstain"}


if __name__=="__main__":
    report=fixture()
    print(json.dumps({"governance_packets":len(report["governance_packets"]),
      "eligible_independent_governors":report["gate"]["eligible_governance_roots"],
      "external_authority_collected":report["true_external_authority_collected"],
      "empirical_witnesses":report["gate"]["independent_empirical_witnesses"],
      "promotion":report["promotion"]},indent=2))
