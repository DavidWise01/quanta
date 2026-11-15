#!/usr/bin/env python3
import copy
import unittest
from ada073_governance import governance_packet,evaluate,fixture,OWNED,SOURCE_ROOT

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.report=fixture()
        self.p=self.report["governance_packets"]
        self.args={"registry_hash":self.report["trusted_registry_hash"],
                   "capture_sha":self.report["test_capture_binding"],
                   "key_id":"key-v2"}
    def test_three_packets_same_fixture_ancestry(self):
        self.assertEqual(len(self.p),3)
        self.assertFalse(self.report["true_external_authority_collected"])
    def test_owned_source_not_external(self):
        self.assertEqual(evaluate([self.p[0]],**self.args)["eligible_governance_roots"],0)
    def test_public_mirror_not_independent(self):
        self.assertEqual(evaluate([self.p[1]],**self.args)["eligible_governance_roots"],0)
    def test_unverified_new_key_not_independent(self):
        self.assertEqual(evaluate([self.p[2]],**self.args,
                    trusted_external_roots=("synthetic:separately-labeled-key",))["eligible_governance_roots"],0)
    def test_verified_root_could_pass_structural_gate(self):
        p=governance_packet(key_id="key-v2",registry_hash=self.args["registry_hash"],
                 capture_sha=self.args["capture_sha"],root="test:external-root",
                 verified_identity=True)
        r=evaluate([p],**self.args,trusted_external_roots=("test:external-root",))
        self.assertEqual(r["eligible_governance_roots"],1)
        self.assertEqual(r["promotion"],"abstain")
    def test_repeated_external_root_not_multiplied(self):
        p=governance_packet(key_id="key-v2",registry_hash=self.args["registry_hash"],
                 capture_sha=self.args["capture_sha"],root="test:external-root",
                 verified_identity=True)
        r=evaluate([p,p,p],**self.args,trusted_external_roots=("test:external-root",))
        self.assertEqual(r["eligible_governance_roots"],1)
    def test_publication_cannot_govern_own_validation(self):
        p=governance_packet(key_id="key-v2",registry_hash=self.args["registry_hash"],
                 capture_sha=self.args["capture_sha"],root=SOURCE_ROOT,verified_identity=True)
        self.assertEqual(evaluate([p],**self.args,trusted_external_roots=(SOURCE_ROOT,))["eligible_governance_roots"],0)
    def test_tampered_packet_rejected(self):
        p=copy.deepcopy(self.p[0])
        p["capture_sha256"]="00"
        with self.assertRaises(ValueError):evaluate([p],**self.args)
    def test_wrong_capture_rejected_even_when_hash_valid(self):
        p=governance_packet(key_id="key-v2",registry_hash=self.args["registry_hash"],capture_sha="different")
        with self.assertRaises(ValueError):evaluate([p],**self.args)
    def test_wrong_registry_rejected(self):
        p=governance_packet(key_id="key-v2",registry_hash="different",capture_sha=self.args["capture_sha"])
        with self.assertRaises(ValueError):evaluate([p],**self.args)
    def test_wrong_key_rejected(self):
        p=governance_packet(key_id="old-key",registry_hash=self.args["registry_hash"],capture_sha=self.args["capture_sha"])
        with self.assertRaises(ValueError):evaluate([p],**self.args)
    def test_empty_bindings_rejected(self):
        with self.assertRaises(ValueError):governance_packet(key_id="",registry_hash="abc",capture_sha="abc")
    def test_no_promotion_from_governance_alone(self):
        self.assertEqual(self.report["gate"]["independent_empirical_witnesses"],0)
        self.assertEqual(self.report["promotion"],"abstain")
    def test_deterministic(self):
        self.assertEqual(fixture(),fixture())

if __name__=="__main__":
    unittest.main()
