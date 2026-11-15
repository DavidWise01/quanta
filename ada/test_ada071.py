#!/usr/bin/env python3
import copy
import unittest
from ada071_registry import (fixture,event,registry_state,verify_at_epoch,
                             OLD_KEY,NEW_KEY,COLLECTOR)
from ada070_attestation import public_b64,collector_claim,sign_claim
from ada069_lineage import fixture as lineage_fixture

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.f=fixture()
        self.old_pub=public_b64(OLD_KEY)
        self.new_pub=public_b64(NEW_KEY)
    def test_three_events(self):
        self.assertEqual(len(self.f["lifecycle"]),3)
    def test_initial_authorization(self):
        self.assertTrue(self.f["before_rotation"]["authorized_now"])
    def test_revoked_rejected(self):
        self.assertFalse(self.f["revoked_key"]["authorized_now"])
    def test_prior_key_not_resurrected(self):
        self.assertFalse(self.f["prior_key_after_rotation"]["authorized_now"])
    def test_new_key_authorized_only_locally(self):
        self.assertTrue(self.f["new_key"]["authorized_now"])
        self.assertFalse(self.f["new_key"]["external_identity_authenticated"])
    def test_replay_on_reused_key_id_forbidden(self):
        events=copy.deepcopy(self.f["lifecycle"])
        event(events,"revoke","key-v2",self.new_pub,epoch=4)
        event(events,"enroll","key-v1",self.old_pub,epoch=5)
        with self.assertRaises(ValueError): registry_state(events)
    def test_active_key_cannot_be_overwritten(self):
        rows=[]
        event(rows,"enroll","key-v1",self.old_pub,epoch=1)
        event(rows,"enroll","key-v2",self.new_pub,epoch=2)
        with self.assertRaises(ValueError):registry_state(rows)
    def test_revocation_must_match(self):
        rows=[]
        event(rows,"enroll","key-v1",self.old_pub,epoch=1)
        event(rows,"revoke","key-v2",self.new_pub,epoch=2)
        with self.assertRaises(ValueError):registry_state(rows)
    def test_tamper_detected(self):
        rows=copy.deepcopy(self.f["lifecycle"])
        rows[1]["action"]="enroll"
        with self.assertRaises(ValueError):registry_state(rows)
    def test_missing_event_detected(self):
        rows=[self.f["lifecycle"][0],self.f["lifecycle"][2]]
        with self.assertRaises(ValueError):registry_state(rows)
    def test_stale_evaluation_rejected(self):
        packet=sign_claim(collector_claim(lineage_fixture()["comparison"]["left"]),
                          NEW_KEY,COLLECTOR)
        with self.assertRaises(ValueError):
            verify_at_epoch(packet,self.f["lifecycle"],evaluation_epoch=1,required_key_id="key-v2")
    def test_no_external_witness_promotion(self):
        self.assertEqual(self.f["independent_empirical_witnesses"],0)
        self.assertEqual(self.f["promotion"],"abstain")
    def test_same_publication_root(self):
        self.assertEqual(self.f["source_ancestry"],"OEIS:A003095")
    def test_determinism(self):
        self.assertEqual(fixture(),fixture())

if __name__=="__main__":
    unittest.main()
