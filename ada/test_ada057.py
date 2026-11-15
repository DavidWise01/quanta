#!/usr/bin/env python3
"""ADA-057 ancestry, repair and persistence regressions."""
import json
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path
from ada057_generations import build, verify, export_create_only
from ada055_candidates import PARENT, closure


class GenerationalMemoryTests(unittest.TestCase):
    def setUp(self):
        self.events = build()
    def test_exact_eight_records(self):
        self.assertEqual(len(self.events), 8)
        self.assertTrue(verify(self.events))
    def test_g0_failure_remains(self):
        self.assertEqual(self.events[1]["state"], ["1", "1/3", "1/3"])
        self.assertEqual(self.events[1]["K"], "3")
    def test_g0_repairs_preserved(self):
        self.assertEqual(self.events[2]["state"], ["1", "1/3", "1/9"])
        self.assertEqual(self.events[3]["state"], ["1", "1/9", "1/3"])
        self.assertEqual(self.events[2]["K"], self.events[3]["K"])
    def test_promotion_is_only_selected_repair(self):
        self.assertEqual(self.events[4]["parent_roots"], [self.events[3]["hash"]])
        self.assertEqual(self.events[4]["state"], self.events[3]["state"])
    def test_second_generation_fail_and_repair(self):
        self.assertEqual(self.events[5]["state"], ["3", "1/9", "1/3"])
        self.assertEqual(self.events[5]["K"], "3")
        self.assertEqual(self.events[7]["state"], ["3", "1/27", "1/3"])
        self.assertEqual(self.events[7]["K"], "1")
    def test_second_repair_ancestry(self):
        self.assertEqual(self.events[7]["parent_roots"], [self.events[5]["hash"]])
        self.assertEqual(self.events[6]["parent_roots"], [self.events[5]["hash"]])
    def test_single_owned_source_root(self):
        self.assertEqual(len({r["source_ancestry"] for r in self.events}),1)
        self.assertEqual(len({r["hash"] for r in self.events}),8)
    def test_tamper_rejected(self):
        cloned = json.loads(json.dumps(self.events))
        cloned[5]["state"][0] = "99"
        with self.assertRaises(ValueError):
            verify(cloned)
    def test_missing_history_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.events[:4]+self.events[5:])
    def test_deterministic(self):
        self.assertEqual(build(), build())
    def test_exclusive_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"generations.jsonl"
            export_create_only(path,self.events)
            saved = path.read_bytes()
            with self.assertRaises(FileExistsError):
                export_create_only(path,self.events)
            self.assertEqual(path.read_bytes(),saved)
            self.assertEqual([json.loads(s) for s in path.read_text().splitlines()],self.events)
    def test_original_parent_unchanged(self):
        self.assertEqual(PARENT,(F(1,3),)*3)
        self.assertEqual(closure(PARENT),1)


if __name__ == "__main__":
    unittest.main()
