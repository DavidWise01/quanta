#!/usr/bin/env python3
import unittest
from fractions import Fraction as F
from ada060_oracle import challenge, SOURCE_ROOT
from ada060_unseen import run
from ada059_select import compare, PARENTS

class ADA060Tests(unittest.TestCase):
    def setUp(self):
        self.report = run()

    def test_frozen_selector_unchanged(self):
        self.assertEqual(compare()["new_passes"],5)

    def test_diagnostic_counts(self):
        self.assertEqual(len(self.report["cases"]),5)
        self.assertEqual(self.report["known_challenge_passes"],3)
        self.assertEqual(self.report["rejections"],2)
        self.assertEqual(self.report["abstentions"],3)
        self.assertEqual(self.report["promotions"],0)

    def test_selected_factors_retained(self):
        self.assertEqual([x["selected_factor"] for x in self.report["cases"]],
                         ["3","2","1/2","1/2","3"])

    def test_no_unwitnessed_promotion(self):
        self.assertTrue(all(x["decision"] != "eligible" for x in self.report["cases"]))

    def test_unknown_is_distinct_from_failure(self):
        r=challenge((F(1,3),)*3)
        self.assertIsNone(r["history_witness"])
        self.assertEqual(r["promotion"],"abstain")
        self.assertEqual(challenge((F(1,3),)*3,
            {"source_root":SOURCE_ROOT, "observed_replay":False})["promotion"],"reject")
        self.assertEqual(challenge((F(1,3),)*3,
            {"source_root":SOURCE_ROOT, "observed_replay":True})["promotion"],"eligible")

    def test_invalid_oracle_evidence_rejected(self):
        with self.assertRaises(ValueError):
            challenge((F(1,3),)*3,{"source_root":"unrelated","observed_replay":True})
        with self.assertRaises(ValueError):
            challenge((F(1,3),)*3,{"source_root":SOURCE_ROOT,"observed_replay":"yes"})

    def test_five_candidate_records_per_parent(self):
        self.assertTrue(all(len(x["all_candidate_challenges"])==5 for x in self.report["cases"]))

    def test_source_is_not_independent(self):
        self.assertEqual(self.report["source_ancestry"],SOURCE_ROOT)
        self.assertEqual(len({x["parent_root"] for x in self.report["cases"]}),5)

    def test_no_input_mutation(self):
        original=tuple(tuple(p) for p in PARENTS)
        run()
        self.assertEqual(PARENTS,original)

    def test_deterministic(self):
        self.assertEqual(run(),run())

if __name__=="__main__":
    unittest.main()
