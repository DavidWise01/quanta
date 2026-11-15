"""ADA-058: synthetic transfer challenge tests; no persistent ledger writes."""
import unittest
from fractions import Fraction as F
from ada058_transfer import (evaluate_challenge, evaluate_generations,
                             MAX_AMPLITUDE, MAX_IMBALANCE)
from ada057_generations import build
from ada055_candidates import closure


class TransferTests(unittest.TestCase):
    def setUp(self):
        self.result = evaluate_generations()
        self.named = {x["name"]: x for x in self.result["observations"]}

    def test_rules_explicit(self):
        self.assertEqual(MAX_AMPLITUDE, F(1))
        self.assertEqual(MAX_IMBALANCE, F(9))
        self.assertEqual(len(self.named), 4)

    def test_origin_passes(self):
        self.assertEqual(self.named["origin"]["passed"], 5)

    def test_first_generation_passes(self):
        x = self.named["gen0_selected"]
        self.assertTrue(x["all_pass"])
        self.assertEqual(x["imbalance"], "9")

    def test_second_generation_fails_external_constraints(self):
        x = self.named["gen1_selected"]
        self.assertEqual(x["K"], "1")
        self.assertEqual(x["passed"], 3)
        self.assertFalse(x["checks"]["resource_cap"])
        self.assertFalse(x["checks"]["balance"])
        self.assertEqual(x["imbalance"], "81")

    def test_alternate_second_generation_also_fails(self):
        x = self.named["gen1_alternative"]
        self.assertEqual(x["K"], "1")
        self.assertEqual(x["imbalance"], "27")
        self.assertEqual(x["passed"], 3)

    def test_permutation_invariance_alone_is_not_transfer(self):
        self.assertTrue(self.named["gen1_selected"]["checks"]["permutation_stability"])
        self.assertFalse(self.named["gen1_selected"]["all_pass"])

    def test_zero_or_negative_state_rejected(self):
        for state in ((F(0),F(1),F(1)),(F(-1),F(-1),F(1))):
            x = evaluate_challenge(state)
            self.assertFalse(x["checks"]["positive"])
            self.assertFalse(x["all_pass"])

    def test_ancestry_unchanged(self):
        events = build()
        for obs in self.result["observations"]:
            self.assertEqual(obs["source_event_hash"], events[obs["source_event_seq"]]["hash"])

    def test_deterministic(self):
        self.assertEqual(evaluate_generations(), evaluate_generations())

    def test_no_automatic_promotion_from_closure_only(self):
        self.assertEqual(closure(tuple(F(x) for x in self.named["gen1_selected"]["state"])), 1)
        self.assertFalse(self.named["gen1_selected"]["all_pass"])


if __name__ == "__main__":
    unittest.main()
