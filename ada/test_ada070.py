#!/usr/bin/env python3
import copy
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from ada070_attestation import (fixture,TEST_SEED,TEST_COLLECTOR,
    collector_claim,sign_claim,verify_attestation,public_b64)
from ada069_lineage import fixture as lineage_fixture

class ADA070Tests(unittest.TestCase):
    def setUp(self):
        self.report=fixture()
        self.key=Ed25519PrivateKey.from_private_bytes(TEST_SEED)
        self.trusted={TEST_COLLECTOR:public_b64(self.key)}
        self.packet=self.report["capture_claims"][0]
    def test_two_signatures_verify(self):
        self.assertEqual(self.report["valid_signatures"],2)
        self.assertTrue(all(v["valid"] for v in self.report["verifications"]))
    def test_single_signing_identity(self):
        self.assertEqual(self.report["unique_collector_keys"],1)
    def test_untrusted_key_rejected(self):
        self.assertFalse(verify_attestation(self.packet,{})["valid"])
    def test_signature_tampered_rejected(self):
        p=copy.deepcopy(self.packet)
        p["signature_ed25519_b64"]="AAAA"
        self.assertFalse(verify_attestation(p,self.trusted)["valid"])
    def test_capture_digest_tampered_rejected(self):
        p=copy.deepcopy(self.packet)
        p["claim"]["body_sha256"]="0"*64
        self.assertFalse(verify_attestation(p,self.trusted)["valid"])
    def test_source_root_tampered_rejected(self):
        p=copy.deepcopy(self.packet)
        p["claim"]["source_root"]="different"
        self.assertFalse(verify_attestation(p,self.trusted)["valid"])
    def test_capture_time_tampered_rejected(self):
        p=copy.deepcopy(self.packet)
        p["claim"]["capture_time"]="2030-01-01T00:00:00+00:00"
        self.assertFalse(verify_attestation(p,self.trusted)["valid"])
    def test_other_key_rejected(self):
        other=Ed25519PrivateKey.from_private_bytes(b"\x22"*32)
        self.assertFalse(verify_attestation(self.packet,{TEST_COLLECTOR:public_b64(other)})["valid"])
    def test_valid_signature_not_promotion(self):
        self.assertTrue(verify_attestation(self.packet,self.trusted)["valid"])
        self.assertEqual(verify_attestation(self.packet,self.trusted)["promotion"],"abstain")
    def test_not_independent_external_witness(self):
        self.assertEqual(self.report["externally_authenticated_collectors"],0)
        self.assertEqual(self.report["independent_empirical_witnesses"],0)
        self.assertEqual(self.report["publication_roots"],1)
    def test_claim_binding(self):
        c=collector_claim(lineage_fixture()["comparison"]["left"])
        self.assertEqual(c["body_sha256"],self.packet["claim"]["body_sha256"])
    def test_deterministic(self):
        self.assertEqual(fixture(),fixture())
if __name__=="__main__":
    unittest.main()
