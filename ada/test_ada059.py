#!/usr/bin/env python3
"""ADA-059 fresh synthetic parent comparison and frozen-rule regressions."""
import unittest
from fractions import Fraction as F
from ada059_select import PARENTS, FACTORS, propose, choose, compare
from ada058_transfer import evaluate_challenge
from ada055_candidates import closure


class ADA059SelectionTests(unittest.TestCase):
    def setUp(self):
        self.report = compare()
    def test_five_new_parents_with_full_envelope(self):
        self.assertEqual(len(PARENTS), 5)
        self.assertTrue(all(closure(p) == 1 and evaluate_challenge(p)["all_pass"] for p in PARENTS))
    def test_order_fixed(self):
        self.assertEqual(FACTORS, (F(3), F(2), F(1,2), F(1,3), F(1)))
    def test_baseline_vs_new(self):
        self.assertEqual(self.report["baseline_passes"], 2)
        self.assertEqual(self.report["new_passes"], 5)
    def test_exact_selection_cases(self):
        rows = self.report["cases"]
        self.assertEqual([r["closure_only_factor"] for r in rows], ["3"]*5)
        self.assertEqual([r["full_envelope_factor"] for r in rows], ["3","2","1/2","1/2","3"])
    def test_all_candidates_keep_parent_and_root(self):
        for case in self.report["cases"]:
            self.assertEqual(len(case["candidates"]),5)
            self.assertEqual(len({c["parent_root"] for c in case["candidates"]}),1)
            self.assertEqual(len({c["candidate_root"] for c in case["candidates"]}),5)
            self.assertTrue(all(c["parent_root"]==case["parent_root"] for c in case["candidates"]))
    def test_full_selector_never_promotes_failing(self):
        for p in PARENTS:
            _, c = propose(p)
            self.assertTrue(choose(c, True)["all_pass"])
    def test_baseline_failure_retained(self):
        self.assertEqual(sum(not c["closure_only_passes_envelope"] for c in self.report["cases"]),3)
        self.assertTrue(all(len(c["candidates"])==5 for c in self.report["cases"]))
    def test_closure_remains_exact(self):
        for p in PARENTS:
            _, c = propose(p)
            self.assertTrue(all(x["checks"]["closure"] and x["K"]=="1" for x in c))
    def test_distinct_hash_not_independent_witness(self):
        self.assertEqual(len({c["source_ancestry"] for c in self.report["cases"]}),1)
        self.assertEqual(len({c["parent_root"] for c in self.report["cases"]}),5)
    def test_reproducible(self):
        self.assertEqual(compare(),compare())
    def test_invalid_parent_rejected(self):
        with self.assertRaises(ValueError):
            propose((F(3),F(1,27),F(1,3)))
    def test_no_mutation_of_input(self):
        original = tuple(tuple(x) for x in PARENTS)
        compare()
        self.assertEqual(PARENTS,original)

if __name__=="__main__":
    unittest.main()
