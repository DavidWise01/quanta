#!/usr/bin/env python3
import copy
import unittest
from ada074_bootstrap import (fixture,policy_document,decide,
                              POLICY_REFERENCES,SOURCE_ROOT)

class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.f=fixture()
        self.claim={"key_id":"key-A","identity":"observer-A",
                    "source_ancestry":"OEIS:A003095",
                    "signature_verified":True,"revocation_fresh":True}
        self.anchor={"key-A":{"identity":"observer-A",
                "role":"capture-collector","ancestry":"external:test-governor",
                "externally_established":True}}
    def test_references_are_external_policy_only(self):
        self.assertEqual(len(POLICY_REFERENCES),2)
        self.assertTrue(policy_document()["publication_trust_not_granted_by_reference"])
    def test_missing_anchor_fails(self):
        self.assertFalse(decide(self.claim,{})["structurally_eligible"])
    def test_owned_ancestry_fails(self):
        a=copy.deepcopy(self.anchor)
        a["key-A"]["ancestry"]=SOURCE_ROOT
        self.assertFalse(decide(self.claim,a)["structurally_eligible"])
    def test_source_governing_itself_fails(self):
        a=copy.deepcopy(self.anchor)
        a["key-A"]["ancestry"]="OEIS:A003095"
        self.assertFalse(decide(self.claim,a)["structurally_eligible"])
    def test_unestablished_anchor_fails(self):
        a=copy.deepcopy(self.anchor)
        a["key-A"]["externally_established"]=False
        self.assertFalse(decide(self.claim,a)["structurally_eligible"])
    def test_identity_mismatch_fails(self):
        c={**self.claim,"identity":"impostor"}
        self.assertFalse(decide(c,self.anchor)["structurally_eligible"])
    def test_role_mismatch_fails(self):
        a=copy.deepcopy(self.anchor)
        a["key-A"]["role"]="publisher"
        self.assertFalse(decide(self.claim,a)["structurally_eligible"])
    def test_missing_signature_fails(self):
        c={**self.claim,"signature_verified":False}
        self.assertFalse(decide(c,self.anchor)["structurally_eligible"])
    def test_stale_revocation_fails(self):
        c={**self.claim,"revocation_fresh":False}
        self.assertFalse(decide(c,self.anchor)["structurally_eligible"])
    def test_structural_pass_still_abstains(self):
        r=decide(self.claim,self.anchor)
        self.assertTrue(r["structurally_eligible"])
        self.assertFalse(r["external_identity_authenticated"])
        self.assertEqual(r["promotion"],"abstain")
    def test_assertion_cannot_mutate_registry(self):
        before=copy.deepcopy(self.anchor)
        decide(self.claim,self.anchor)
        self.assertEqual(self.anchor,before)
    def test_no_real_certificate_or_external_root(self):
        self.assertEqual(self.f["actual_external_certificates_processed"],0)
        self.assertEqual(self.f["actual_externally_provisioned_roots"],0)
        self.assertEqual(self.f["empirical_witnesses"],0)
    def test_fixture_deterministic(self):
        self.assertEqual(fixture(),fixture())
if __name__=="__main__":
    unittest.main()
