import unittest
from fractions import Fraction as F
from ada055_candidates import PARENT, MANIFOLD, SINGLET, ROLES, closure, evaluate, candidates

class ADA055Tests(unittest.TestCase):
    def setUp(self):
        self.result = evaluate()
    def test_origin_exact(self):
        self.assertEqual(closure(PARENT), 1)
        self.assertEqual(PARENT, (F(1,3),)*3)
    def test_three_children_one_parent(self):
        self.assertEqual(len(self.result["candidates"]),3)
        self.assertEqual(len({r["parent_root"] for r in self.result["candidates"]}),1)
        self.assertEqual(len({r["candidate_root"] for r in self.result["candidates"]}),3)
        self.assertTrue(all(r["source_ancestry"]=="synthetic:ada055:one-parent" for r in self.result["candidates"]))
    def test_closure_distinguishes_counterexample(self):
        by_name={r["candidate"]:r for r in self.result["candidates"]}
        self.assertEqual(by_name["Josephson"]["closure"],"1")
        self.assertEqual(by_name["Mandelbrot"]["closure"],"1")
        self.assertEqual(by_name["Juliet"]["closure"],"3")
        self.assertEqual(by_name["Juliet"]["status"],"rejected")
    def test_selection_rule(self):
        self.assertEqual(self.result["selected"], "Josephson")
        self.assertEqual(self.result["candidates"][0]["changed_components"],2)
        self.assertEqual(self.result["candidates"][1]["changed_components"],0)
    def test_parent_is_immutable(self):
        copy=tuple(PARENT)
        evaluate()
        self.assertEqual(PARENT,copy)
    def test_identity_preserved(self):
        self.assertTrue(all(r["manifold"]==MANIFOLD and r["singlet"]==SINGLET for r in self.result["candidates"]))
        self.assertEqual(tuple(r["role"] for r in self.result["candidates"]),ROLES)
    def test_reproducibility(self):
        self.assertEqual(evaluate(),evaluate())

if __name__=="__main__":
    unittest.main()
