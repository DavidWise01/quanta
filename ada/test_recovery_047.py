#!/usr/bin/env python3
"""ADA-047: scratch-ledger recovery regression. No writes to committed baseline."""
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction
from kernel import genesis, append, replay, classification, MANIFOLD, ROLES

class RecoveryTest(unittest.TestCase):
    def test_complete_recovery_after_110_ticks(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"events.jsonl"
            genesis(p)
            origin, h0, n0 = replay(p)
            self.assertEqual(n0,1)
            self.assertEqual(origin["manifold"],MANIFOLD)
            self.assertEqual(origin["roles"],ROLES)
            for i in range(110):
                append(p,"tick","synthetic:ada-047-test")
            before, h110, n110 = replay(p)
            self.assertEqual(n110,111)
            self.assertEqual(before["step"],110)
            self.assertEqual(before["phase_fifths"],44)
            self.assertEqual(before["phi_fifths"],66)
            self.assertTrue(classification(before)["address_return"])
            self.assertTrue(classification(before)["algebraic_return"])
            self.assertFalse(classification(before)["geometric_return"])
            self.assertEqual(Fraction(before["phase_fifths"],5) % 2,Fraction(4,5))
            self.assertNotEqual(h110,h0)
            lines_before=p.read_text(encoding="utf-8").splitlines(keepends=True)
            append(p,"recover","synthetic:ada-047-test")
            after, h111, n111=replay(p)
            self.assertEqual(n111,112)
            self.assertEqual(after["step"],110)
            self.assertEqual(after["phase_fifths"],0)
            self.assertEqual(after["phi_fifths"],0)
            self.assertEqual(after["box"],origin["box"])
            self.assertEqual(after["singlet"],origin["singlet"])
            self.assertEqual(after["roles"],origin["roles"])
            self.assertEqual(after["manifold"],origin["manifold"])
            self.assertTrue(classification(after)["address_return"])
            self.assertTrue(classification(after)["algebraic_return"])
            self.assertTrue(classification(after)["geometric_return"])
            self.assertEqual(after["witness_count"],112)
            self.assertNotEqual(h111,h110)
            lines_after=p.read_text(encoding="utf-8").splitlines(keepends=True)
            self.assertEqual(lines_after[:111],lines_before)
            self.assertEqual(len(lines_after),112)
            self.assertEqual(p.read_text().count("\n"),112)
            # The append-only ledger retains both the original and recovery witnesses.
            self.assertEqual(origin["witness_count"],1)
if __name__=="__main__":
    unittest.main()
