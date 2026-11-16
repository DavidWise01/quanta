#!/usr/bin/env python3
"""ADA-074: read-only external policy bootstrap, explicitly NOT external PKI.

RFC 5280 and RFC 9162 are normative references. They provide validation
policy, but no trust anchor for this synthetic collector. Self-declared
independence, source URLs, and a local key never bootstrap external identity.
"""
import json
from ada055_candidates import hash_payload
from ada073_governance import fixture as prior_fixture

VERSION="ADA074-policy-bootstrap-v1"
POLICY_REFERENCES=(
    ("RFC5280", "https://www.rfc-editor.org/rfc/rfc5280.html",
     "Certification path validation takes an independently selected trust anchor as input."),
    ("RFC9162", "https://www.rfc-editor.org/rfc/rfc9162.html",
     "Certificate transparency and log inclusion do not substitute for normal certificate validation."),
)
SOURCE_ROOT="quanta-owned:ada-governance-experiment"


def policy_document():
    """Pinned declarative rules, not downloaded RFC bytes or trusted CA roots."""
    body={
        "version":VERSION,
        "references":[{"id":ident,"url":url,"interpretation":interpretation}
                      for ident,url,interpretation in POLICY_REFERENCES],
        "rule_order":("registered_root", "identity_binding", "role_authorized",
                      "signature_verified", "revocation_fresh", "provenance_distinct"),
        "publication_trust_not_granted_by_reference":True,
        "empirical_promotions_from_policy_alone":False,
    }
    body["digest"]=hash_payload(body)
    return body


def decide(assertion, registry):
    """Fail closed: labels and hashes cannot enroll themselves as external keys.

    registry is an *externally provisioned* read-only mapping from key_id to
    trusted metadata. No caller-supplied assertion may alter registry.
    """
    policy=policy_document()
    if not isinstance(registry,dict):
        raise ValueError("registry must be pre-provisioned")
    if not isinstance(assertion,dict):
        raise ValueError("assertion must be a mapping")
    key_id=assertion.get("key_id")
    known=registry.get(key_id) if isinstance(key_id,str) else None
    checks={
        "registered_root":known is not None,
        "identity_binding":bool(known is not None and
             assertion.get("identity")==known.get("identity") and
             known.get("identity")),
        "role_authorized":bool(known is not None and
             known.get("role")=="capture-collector"),
        "signature_verified":assertion.get("signature_verified") is True,
        "revocation_fresh":assertion.get("revocation_fresh") is True,
        "provenance_distinct":bool(known is not None and
             known.get("ancestry") not in (SOURCE_ROOT,"OEIS:A003095") and
             known.get("externally_established") is True and
             assertion.get("source_ancestry") != known.get("ancestry")),
    }
    structural=all(checks.values())
    return {"policy_digest":policy["digest"],"checks":checks,
            "structurally_eligible":structural,
            "external_identity_authenticated":False,
            "empirical_witnesses":0,"promotion":"abstain",
            "reason":("candidate passed policy structure but no real external "
                      "identity verification has occurred" if structural else
                      "missing or disqualified trust prerequisites")}


def fixture():
    previous=prior_fixture()
    assertion={"key_id":"fixture-key-v2",
               "identity":"quanta-fixture-collector",
               "source_ancestry":"OEIS:A003095",
               "signature_verified":True,"revocation_fresh":True,
               "claims_external_independence":True}
    # Do not bootstrap registry from the signed claim or a source URL.
    missing=decide(assertion,{})
    owned=decide(assertion,{"fixture-key-v2":{
        "identity":"quanta-fixture-collector",
        "role":"capture-collector",
        "ancestry":SOURCE_ROOT,
        "externally_established":False}})
    copied=decide(assertion,{"fixture-key-v2":{
        "identity":"quanta-fixture-collector","role":"capture-collector",
        "ancestry":"OEIS:A003095","externally_established":True}})
    structural=decide(assertion,{"fixture-key-v2":{
        "identity":"quanta-fixture-collector","role":"capture-collector",
        "ancestry":"synthetic:separate-governor","externally_established":True}})
    return {"version":VERSION,"policy":policy_document(),
            "upstream_registry_hash":previous["trusted_registry_hash"],
            "scenarios":{"missing_trust_anchor":missing,
                         "owned_self_bootstrap":owned,
                         "source_as_governor":copied,
                         "declared_separate_root":structural},
            "actual_external_certificates_processed":0,
            "actual_externally_provisioned_roots":0,
            "empirical_witnesses":0,"promotion":"abstain"}


if __name__=="__main__":
    f=fixture()
    print(json.dumps({
        "policy_sources":[x[0] for x in POLICY_REFERENCES],
        "case_results":{k:{"eligible":v["structurally_eligible"],
                           "promotion":v["promotion"]}
                        for k,v in f["scenarios"].items()},
        "authenticated_external_roots":0,
        "empirical_witnesses":0,
        "promotion":"abstain",
    },indent=2))
