import unittest
from fractions import Fraction as F
from ada063_external_replay import evolve,evaluate,FIXTURES,SOURCE

class ADA063Tests(unittest.TestCase):
    def test_external_definition_identity(self):
        self.assertEqual(SOURCE["definition"],"z_(n+1)=z_n^2+c, z_0=0")
    def test_five_exact_orbits(self):
        self.assertEqual(evaluate()["exact_orbit_passes"],5)
        self.assertEqual(len(FIXTURES),5)
    def test_zero_is_fixed(self):
        self.assertEqual(evolve((0,0),6),((F(0),F(0)),)*6)
    def test_one_escapes_finite(self):
        self.assertEqual(evolve((1,0),4)[-1],(F(5),F(0)))
    def test_imaginary_periodic_trace(self):
        self.assertEqual(evolve((0,1),5)[4],(F(-1),F(1)))
    def test_minus_one_cycle(self):
        self.assertEqual(evolve((-1,0),6)[4],(F(0),F(0)))
    def test_minus_two_fixed_after_step_two(self):
        self.assertEqual(evolve((-2,0),5)[-1],(F(2),F(0)))
    def test_record_hashes_distinct(self):
        self.assertEqual(len({r["digest"] for r in evaluate()["results"]}),5)
    def test_no_false_external_witness(self):
        self.assertEqual(evaluate()["independent_empirical_witnesses"],0)
        self.assertEqual(evaluate()["promotion"],"abstain")
    def test_fixtures_are_owned(self):
        self.assertTrue(evaluate()["fixtures_authored_by_quanta"])
    def test_reproducible(self):
        self.assertEqual(evaluate(),evaluate())
    def test_fraction_parameter(self):
        trace=evolve((F(1,2),F(0)),3)
        self.assertEqual(trace[-1],(F(3,4),F(0)))

if __name__=="__main__":unittest.main()
