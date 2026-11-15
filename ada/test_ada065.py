#!/usr/bin/env python3
import unittest
from ada065_published_replay import verify, PUBLISHED_CASES, SOURCE_ROOTS
from ada063_external_replay import evolve

class ADA065Tests(unittest.TestCase):
    def setUp(self): self.report=verify()
    def test_four_published_cases_match(self):
        self.assertEqual(self.report["passing"],4)
        self.assertEqual(self.report["total"],4)
    def test_extended_oeis_orbit(self):
        self.assertEqual(PUBLISHED_CASES[0][3][-2:],(458330,210066388901))
    def test_two_distinct_publication_roots(self):
        self.assertEqual(len(SOURCE_ROOTS),2)
    def test_duplicate_plus_one_not_third_witness(self):
        self.assertEqual(self.report["distinct_external_publication_roots"],2)
        self.assertEqual(self.report["independent_empirical_witness_roots"],0)
    def test_no_external_bytes_claim(self):
        self.assertFalse(self.report["reference_capture_bytes_archived"])
    def test_cannot_promote_physics(self):
        self.assertEqual(self.report["promotion"],"abstain")
    def test_reference_values_are_separate_from_computation(self):
        for row in self.report["cases"]:
            self.assertEqual(row["reference_values"],row["computed_values"])
            self.assertTrue(row["matched"])
    def test_counterexample_is_detectable(self):
        published=PUBLISHED_CASES[0][3]
        wrong=tuple(published[:-1])+(published[-1]+1,)
        trace=evolve((1,0),len(wrong))
        self.assertNotEqual(tuple(x[0] for x in trace),wrong)
    def test_reproducible(self):
        self.assertEqual(verify(),verify())
    def test_authority_and_provenance(self):
        for row in self.report["cases"]:
            self.assertIn(row["source_url"],SOURCE_ROOTS.values())
            self.assertEqual(row["reference_transcription"],"manual")
    def test_orbit_parameters_are_real(self):
        self.assertTrue(all(c[2][1]==0 for c in PUBLISHED_CASES))
    def test_exact_integers(self):
        self.assertTrue(all(all(x.denominator==1 and y.denominator==1 for x,y in evolve(c[2],len(c[3]))) for c in PUBLISHED_CASES))
if __name__=="__main__":
    unittest.main()
