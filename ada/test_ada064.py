import unittest
from pathlib import Path
from ada064_observatory import observe
from ada063_external_replay import FIXTURES

class ObservatoryTests(unittest.TestCase):
    def setUp(self): self.report=observe()
    def test_exact_replays(self):
        self.assertEqual(self.report["passes"],5)
        self.assertEqual(self.report["total"],5)
    def test_fixture_names(self):
        self.assertEqual([r["name"] for r in self.report["observations"]],[f[0] for f in FIXTURES])
    def test_no_physical_claim(self):
        self.assertFalse(self.report["physical_coupling_tested"])
        self.assertEqual(self.report["independent_empirical_witnesses"],0)
        self.assertEqual(self.report["promotion"],"abstain")
    def test_ancestry_not_independent(self):
        self.assertTrue(all(x["source_root"]=="quanta-owned:derived-observer" for x in self.report["observations"]))
    def test_deterministic(self): self.assertEqual(observe(),observe())
    def test_ascii_art(self):
        p=Path(__file__).resolve().parent/"ada-064-evidence-observatory.txt"
        text=p.read_text()
        for token in ("{s}","OUROBOROS","ABSTAIN","EXTERNAL DEFINITION"):
            self.assertIn(token,text)
    def test_frozen_fixture(self): self.assertEqual(len(FIXTURES),5)
if __name__=="__main__": unittest.main()
