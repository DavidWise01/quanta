#!/usr/bin/env python3
"""ADA-049 scheduled persistent tick regressions."""
import json
import tempfile
import unittest
from pathlib import Path

from kernel import genesis, replay
from persist_tick import append_scheduled_tick, verify_ledger


class PersistentTickTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "events.jsonl"
        genesis(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_appends_only_one_line_and_preserves_prefix(self):
        old = self.path.read_bytes()
        result = append_scheduled_tick(self.path, "1001", "fixture-source")
        self.assertTrue(result["appended"])
        self.assertEqual(result["step"], 1)
        self.assertEqual(result["records"], 2)
        self.assertTrue(self.path.read_bytes().startswith(old))
        self.assertEqual(self.path.read_bytes().count(b"\n"), 2)
        self.assertEqual(verify_ledger(self.path)[0]["phase_fifths"], 1)

    def test_rerun_is_idempotent(self):
        append_scheduled_tick(self.path, "2002")
        before = self.path.read_bytes()
        result = append_scheduled_tick(self.path, "2002")
        self.assertFalse(result["appended"])
        self.assertEqual(self.path.read_bytes(), before)

    def test_two_internal_three_external(self):
        for i in range(1, 6):
            append_scheduled_tick(self.path, str(3000 + i))
        state, _, count = replay(self.path)
        self.assertEqual(state["step"], 5)
        self.assertEqual(state["phase_fifths"], 2)
        self.assertEqual(state["phi_fifths"], 3)
        self.assertEqual(state["witness_count"], count)
        self.assertEqual(count, 6)
        events = [json.loads(x) for x in self.path.read_text().splitlines()]
        self.assertEqual([r["domain"] for r in events[1:]],
                         ["internal", "internal", "external", "external", "external"])

    def test_rejects_tampered_ledger_without_writing(self):
        broken = self.path.read_bytes().replace(b"synthetic:ada-owned", b"forged:ada-owned")
        self.path.write_bytes(broken)
        with self.assertRaises(ValueError):
            append_scheduled_tick(self.path, "4004")
        self.assertEqual(self.path.read_bytes(), broken)

    def test_rejects_bad_identifier_without_writing(self):
        before = self.path.read_bytes()
        for run_id in ["", "x", "-1", "0"]:
            with self.assertRaises(ValueError):
                append_scheduled_tick(self.path, run_id)
        self.assertEqual(self.path.read_bytes(), before)

    def test_readonly_workflow_still_readonly(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/ada-kernel-verify.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)

    def test_writer_workflow_scope_and_schedule(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/ada-kernel-persist.yml").read_text()
        self.assertIn("cron: '*/5 * * * *'", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("persist_tick.py", workflow)
        self.assertIn("git diff --cached --name-only", workflow)
        self.assertNotIn("git push --force", workflow)


if __name__ == "__main__":
    unittest.main()
