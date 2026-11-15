#!/usr/bin/env python3
"""ADA-051: recorded-transition continuity, not wall-clock extrapolation."""
import json
import tempfile
import unittest
from pathlib import Path
from kernel import genesis, replay
from persist_tick import append_scheduled_tick, verify_ledger

class ContinuityBoundTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.path = Path(self.t.name) / "events.jsonl"
        genesis(self.path)
    def tearDown(self):
        self.t.cleanup()
    def records(self):
        return [json.loads(line) for line in self.path.read_text().splitlines()]
    def test_gap_in_wall_clock_does_not_fabricate_events(self):
        # Explicit run IDs can be far apart. They are identifiers, not a clock.
        first = append_scheduled_tick(self.path, "100000")
        prefix = self.path.read_bytes()
        self.assertEqual(first["step"], 1)
        second = append_scheduled_tick(self.path, "999999")
        self.assertEqual(second["step"], 2)
        self.assertEqual(second["records"], 3)
        self.assertTrue(self.path.read_bytes().startswith(prefix))
        _, head, count = verify_ledger(self.path)
        self.assertEqual(count, 3)
        self.assertEqual(second["head"], head)
        self.assertEqual([r.get("workflow_run_id") for r in self.records()[1:]], ["100000","999999"])
        self.assertEqual([r.get("beat") for r in self.records()[1:]], [1,2])
    def test_duplicate_retry_has_no_new_event(self):
        append_scheduled_tick(self.path, "701")
        before = self.path.read_bytes()
        result = append_scheduled_tick(self.path, "701")
        self.assertFalse(result["appended"])
        self.assertEqual(self.path.read_bytes(), before)
    def test_successive_hashes_are_linked_and_roles_fixed(self):
        for n in range(4):
            append_scheduled_tick(self.path, str(200+n))
        records = self.records()
        for previous, current in zip(records,records[1:]):
            self.assertEqual(current["prev"], previous["hash"])
            self.assertEqual(current["seq"], previous["seq"]+1)
            self.assertEqual(current["state"]["roles"],records[0]["state"]["roles"])
            self.assertEqual(current["state"]["manifold"],records[0]["state"]["manifold"])
        self.assertEqual(records[-1]["state"]["witness_count"], len(records))
        self.assertEqual(records[-1]["state"]["step"],4)
    def test_bad_ledger_rejected_instead_of_repaired(self):
        append_scheduled_tick(self.path,"801")
        bad = self.path.read_bytes().replace(b"synthetic:ada-scheduled",b"synthetic:ada-tampered")
        self.path.write_bytes(bad)
        with self.assertRaises(ValueError):
            append_scheduled_tick(self.path,"802")
        self.assertEqual(self.path.read_bytes(),bad)

if __name__ == "__main__":
    unittest.main()
