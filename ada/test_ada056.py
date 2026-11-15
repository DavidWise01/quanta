#!/usr/bin/env python3
import unittest
from fractions import Fraction as F
from ada055_candidates import PARENT, closure, evaluate, hash_payload
from ada056_repair import repair_juliet


class RepairTest(unittest.TestCase):
    def setUp(self):
        self.report = repair_juliet()

    def test_failed_candidate_retained(self):
        failure = self.report["failure"]
        self.assertEqual(failure["state"], ["1", "1/3", "1/3"])
        self.assertEqual(failure["closure"], "3")
        self.assertEqual(failure["status"], "rejected")

    def test_both_one_coordinate_repairs_close(self):
        opts = self.report["repair_options"]
        self.assertEqual(len(opts), 2)
        self.assertEqual([x["axis"] for x in opts], ["b", "c"])
        self.assertTrue(all(x["closure"] == "1" for x in opts))
        self.assertTrue(all(x["changed_components"] == 1 for x in opts))
        self.assertEqual([x["state"] for x in opts],
                         [["1", "1/9", "1/3"], ["1", "1/3", "1/9"]])

    def test_tie_breaker(self):
        self.assertEqual(self.report["chosen_repair"]["axis"], "b")
        self.assertEqual(self.report["chosen_repair"]["factor"], "1/3")

    def test_chain_preserves_failed_ancestor(self):
        fail = self.report["failure"]
        for candidate in self.report["repair_options"]:
            self.assertEqual(candidate["failure_root"], fail["candidate_root"])
            self.assertEqual(candidate["parent_root"], fail["parent_root"])
            self.assertNotEqual(candidate["root"], fail["candidate_root"])
        self.assertEqual(len({x["root"] for x in self.report["repair_options"]}), 2)

    def test_original_parent_and_original_three_outcomes_unchanged(self):
        self.assertEqual(PARENT, (F(1, 3),) * 3)
        self.assertEqual(evaluate()["selected"], "Josephson")
        self.assertEqual(closure(PARENT), 1)

    def test_minimality_when_preserving_growth_axis(self):
        failed = tuple(F(x) for x in self.report["failure"]["state"])
        self.assertEqual(closure(failed), 3)
        self.assertFalse(closure(failed) == 1)
        for option in self.report["repair_options"]:
            state = tuple(F(x) for x in option["state"])
            self.assertEqual(state[0], failed[0])
            self.assertEqual(sum(x != y for x, y in zip(state, failed)), 1)
            self.assertEqual(closure(state), 1)

    def test_determinism(self):
        self.assertEqual(repair_juliet(), repair_juliet())


if __name__ == "__main__":
    unittest.main()
