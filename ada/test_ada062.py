import unittest
from ada062_packets import (packet,validate,assess,fixture,ROOTS,OWNED_ROOT,
                            exact_replay,CLAIM)

class ADA062Tests(unittest.TestCase):
    def setUp(self):
        self.target="synthetic-candidate-062"
        self.state=("1","1/9","1/3")
    def test_exact_replay(self):
        self.assertEqual(exact_replay(self.state),"1")
    def test_three_simulated_do_not_promote(self):
        a=[packet(root,root,self.target,self.state) for root in ROOTS]
        self.assertEqual(assess(a,self.target,authorized_roots=ROOTS)["decision"],"abstain")
    def test_mirror_does_not_promote(self):
        a=[packet(OWNED_ROOT,"mirror-"+str(i),self.target,self.state,
                  derived_from=("quanta",),origin="measured") for i in range(3)]
        self.assertEqual(assess(a,self.target,authorized_roots=(OWNED_ROOT,))["root_count"],0)
    def test_declared_measured_not_real_independence(self):
        a=[packet(root,root,self.target,self.state,origin="measured") for root in ROOTS]
        r=assess(a,self.target,authorized_roots=ROOTS)
        self.assertEqual(r["declared_gate"],"eligible")
        self.assertEqual(r["decision"],"abstain")
    def test_tamper_detected(self):
        p=packet(ROOTS[0],"x",self.target,self.state)
        p["reported_output"]="3"
        with self.assertRaises(ValueError):validate(p)
    def test_replay_mismatch_retained(self):
        p=packet(ROOTS[0],"x",self.target,self.state,declared_result="3")
        self.assertFalse(validate(p)["replay_match"])
    def test_subject_mismatch(self):
        p=packet(ROOTS[0],"x",self.target,self.state)
        with self.assertRaises(ValueError):assess([p],"other",authorized_roots=ROOTS)
    def test_missing_source_rejected(self):
        with self.assertRaises(ValueError):packet("", "x",self.target,self.state)
    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            packet(ROOTS[0],"x",self.target,self.state,captured="2026-11-15T16:57:00")
    def test_multiple_inputs_required(self):
        with self.assertRaises(ValueError): exact_replay(("1","2"))
    def test_fixture_retains_false_report(self):
        f=fixture()
        self.assertEqual(len(f["packets"]),5)
        self.assertFalse(f["incorrect_result_replay"]["replay_match"])
        self.assertEqual(f["promotion"],"abstain")
    def test_deterministic(self):
        self.assertEqual(fixture(),fixture())
if __name__=="__main__":unittest.main()
