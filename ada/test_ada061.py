#!/usr/bin/env python3
"""ADA-061 synthetic witness gate regression tests."""
import unittest
from ada061_witness import make_packet, check_packets, run_fixture, FIXTURE_ROOTS


class WitnessGateTests(unittest.TestCase):
    def setUp(self):
        self.target="fixture-candidate"
    def packet(self, root, result=True, **kwargs):
        return make_packet(self.target, root, result, **kwargs)

    def test_three_simulated_yes_votes_do_not_promote(self):
        p=[self.packet(x) for x in FIXTURE_ROOTS]
        self.assertEqual(check_packets(p,self.target,True)["decision"],"abstain")
    def test_identical_root_does_not_triple_count(self):
        p=[self.packet("root1",origin="measured") for _ in range(3)]
        self.assertEqual(check_packets(p,self.target,True,authorized_roots=("root1",))["independent_roots"],1)
    def test_copied_mirror_does_not_count(self):
        p=[self.packet(root,origin="measured",copied_from="same-original") for root in FIXTURE_ROOTS]
        self.assertEqual(check_packets(p,self.target,True,authorized_roots=FIXTURE_ROOTS)["independent_roots"],0)
    def test_three_declared_measured_agree(self):
        p=[self.packet(root,origin="measured") for root in FIXTURE_ROOTS]
        self.assertEqual(check_packets(p,self.target,True,authorized_roots=FIXTURE_ROOTS)["decision"],"eligible")
    def test_conflicting_roots_abstain(self):
        p=[self.packet(root,i!=2,origin="measured") for i,root in enumerate(FIXTURE_ROOTS)]
        self.assertEqual(check_packets(p,self.target,True,authorized_roots=FIXTURE_ROOTS)["decision"],"abstain")
    def test_three_measured_no_reject(self):
        p=[self.packet(root,False,origin="measured") for root in FIXTURE_ROOTS]
        self.assertEqual(check_packets(p,self.target,True,authorized_roots=FIXTURE_ROOTS)["decision"],"reject")
    def test_unknown_root_abstains(self):
        p=[self.packet(root,origin="measured") for root in FIXTURE_ROOTS]
        self.assertEqual(check_packets(p,self.target,True)["decision"],"abstain")
    def test_numeric_failure_is_rejected(self):
        self.assertEqual(check_packets([],self.target,False)["decision"],"reject")
    def test_digest_tamper_rejected(self):
        p=self.packet("rootA",origin="measured")
        p["observed_replay"]=False
        with self.assertRaises(ValueError):
            check_packets([p],self.target,True,authorized_roots=("rootA",))
    def test_candidate_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            check_packets([self.packet("rootA")],"other",True)
    def test_fixture_does_not_claim_real_evidence(self):
        result=run_fixture()
        self.assertFalse(result["real_evidence_collected"])
        self.assertEqual(result["promotion"],"abstain")
        self.assertEqual(result["simulated_three_agree"]["independent_roots"],0)
    def test_repeatable(self):
        self.assertEqual(run_fixture(),run_fixture())

if __name__=="__main__":
    unittest.main()
