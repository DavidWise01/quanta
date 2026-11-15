import json
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction
from kernel import genesis, append, replay, classification, digest, canonical

class PersistentKernelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name) / "events.jsonl"
        genesis(self.p)
    def tearDown(self):
        self.tmp.cleanup()
    def test_110_and_recovery(self):
        for _ in range(110):
            append(self.p, "tick", "synthetic:fixture")
        state, head, count = replay(self.p)
        self.assertEqual(count, 111)
        self.assertEqual(state["step"], 110)
        self.assertEqual(Fraction(state["phase_fifths"], 5) % 2, Fraction(4,5))
        self.assertEqual(Fraction(state["phi_fifths"], 5), Fraction(66,5))
        c = classification(state)
        self.assertTrue(c["address_return"])
        self.assertTrue(c["algebraic_return"])
        self.assertFalse(c["geometric_return"])
        append(self.p, "recover", "synthetic:fixture")
        newstate, newhead, count2 = replay(self.p)
        self.assertNotEqual(head, newhead)
        self.assertEqual(count2, 112)
        self.assertEqual(newstate["step"], 110)
        self.assertTrue(classification(newstate)["geometric_return"])
        self.assertEqual(newstate["witness_count"], 112)
    def test_tamper_rejected(self):
        append(self.p, "tick", "synthetic:fixture")
        data = self.p.read_text()
        self.p.write_text(data.replace("synthetic:fixture", "forged:fixture"))
        with self.assertRaises(ValueError):
            replay(self.p)
    def test_truncation_rejected(self):
        with self.p.open("a") as f:
            f.write('{"partial":')
        with self.assertRaises(ValueError):
            replay(self.p)
    def test_wrong_schedule_rejected_even_if_rehashed(self):
        append(self.p, "tick", "synthetic:fixture")
        lines = self.p.read_text().splitlines()
        rec = json.loads(lines[-1])
        rec["beat"] = 5
        rec.pop("hash")
        rec["hash"] = digest(rec)
        lines[-1] = canonical(rec)
        self.p.write_text("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            replay(self.p)
    def test_genesis_no_overwrite(self):
        with self.assertRaises(FileExistsError):
            genesis(self.p)

if __name__ == "__main__":
    unittest.main()
