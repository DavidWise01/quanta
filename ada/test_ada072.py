#!/usr/bin/env python3
"""ADA-072 signed authority, signed time and anti-replay regression."""
import copy
import unittest
from ada072_authority_time import (fixture,replay,authorize,new_event,sign,
    AUTHORITY_KEY,TIME_KEY,PINNED_TIME_SERVICE,PINNED_AUTHORITY,
    OLD_KEY,NEW_KEY,TIMES,COLLECTOR)
from ada070_attestation import public_b64,sign_claim,collector_claim
from ada069_lineage import fixture as lineage_fixture

class AuthorityTests(unittest.TestCase):
    def setUp(self):
        self.f=fixture()
        self.history=self.f["history"]
    def test_three_signed_events(self):
        self.assertEqual(replay(self.history)["event_count"],3)
        self.assertEqual(replay(self.history)["signed_time_claims"],3)
    def test_initially_authorized(self):
        self.assertTrue(self.f["before"]["current_authorization"])
    def test_revoked_unauthorized(self):
        self.assertFalse(self.f["revoked"]["current_authorization"])
    def test_rotated_prior_denied(self):
        self.assertFalse(self.f["stale"]["current_authorization"])
    def test_current_key_valid(self):
        self.assertTrue(self.f["current"]["current_authorization"])
        self.assertFalse(self.f["current"]["external_authority_authenticated"])
    def test_registry_claim_tamper(self):
        h=copy.deepcopy(self.history)
        h[1]["claim"]["action"]="enroll"
        with self.assertRaises(ValueError):replay(h)
    def test_time_claim_tamper(self):
        h=copy.deepcopy(self.history)
        h[2]["time_claim"]["observed_time"]="2027-01-01T00:00:00+00:00"
        with self.assertRaises(ValueError):replay(h)
    def test_wrong_authority_key(self):
        with self.assertRaises(ValueError):
            replay(self.history,authority=public_b64(OLD_KEY))
    def test_wrong_time_key(self):
        with self.assertRaises(ValueError):
            replay(self.history,time_service=public_b64(NEW_KEY))
    def test_missing_event(self):
        with self.assertRaises(ValueError):
            replay(self.history[:1]+self.history[2:])
    def test_nonmonotone_time(self):
        h=copy.deepcopy(self.history)
        h[1]["time_claim"]["observed_time"]=TIMES[0]
        h[1]["time_signature"]=sign(TIME_KEY,h[1]["time_claim"])
        with self.assertRaises(ValueError):replay(h)
    def test_reused_key_identifier(self):
        h=copy.deepcopy(self.history)
        new_event(h,"revoke","key-v2",public_b64(NEW_KEY),
                  recorded_at="2026-11-15T20:03:00+00:00")
        new_event(h,"enroll","key-v1",public_b64(OLD_KEY),
                  recorded_at="2026-11-15T20:04:00+00:00")
        with self.assertRaises(ValueError):replay(h)
    def test_replay_is_deterministic(self):
        self.assertEqual(fixture(),fixture())
    def test_external_trust_not_fabricated(self):
        self.assertEqual(self.f["external_authorities"],0)
        self.assertEqual(self.f["external_time_attestations"],0)
        self.assertEqual(self.f["empirical_witnesses"],0)
        self.assertEqual(self.f["promotion"],"abstain")
    def test_timestamp_is_attested_claim_not_proven_clock(self):
        self.assertEqual(self.f["time_root"],"synthetic:fixture-time")
if __name__=="__main__":
    unittest.main()
