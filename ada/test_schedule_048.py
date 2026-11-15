#!/usr/bin/env python3
"""ADA-048: verify scheduled workflow remains minimal and non-mutating."""
from pathlib import Path
import re
import tempfile
import unittest
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ada"))
from verify_readonly import verify, LEDGER, TRUSTED_GENESIS_HASH
from kernel import digest

class ReadOnlySchedulingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = (ROOT / ".github/workflows/ada-kernel-verify.yml").read_text(encoding="utf-8")

    def test_five_minute_cron(self):
        self.assertRegex(self.workflow, r"(?m)^\s+- cron: ['\"]\*/5 \* \* \* \*['\"]\s*$")
        self.assertIn("workflow_dispatch:", self.workflow)

    def test_token_and_timeout_guard(self):
        self.assertGreaterEqual(self.workflow.count("contents: read"), 2)
        self.assertNotRegex(self.workflow, r"(?m)^\s*contents:\s*write\b")
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertIn("cancel-in-progress: false", self.workflow)
        self.assertIn("timeout-minutes: 8", self.workflow)
        self.assertIn("verify_readonly.py", self.workflow)

    def test_no_repo_mutating_steps(self):
        code = "\n".join(line for line in self.workflow.splitlines() if not line.lstrip().startswith("#"))
        self.assertNotRegex(code, r"\bgit\s+push\b")
        self.assertNotRegex(code, r"\bgit\s+commit\b")
        self.assertNotIn("contents: write", code)
        self.assertNotIn("pull-requests: write", code)
        self.assertNotIn("actions/upload-artifact", code)
        self.assertNotIn("kernel.py tick", code)
        self.assertNotIn("kernel.py recover", code)

    def test_trusted_genesis_replay(self):
        state, head, count = verify()
        self.assertEqual(count, 1)
        self.assertEqual(state["step"], 0)
        self.assertEqual(state["witness_count"], 1)
        self.assertEqual(head, TRUSTED_GENESIS_HASH)

    def test_ledger_is_unchanged_by_verification(self):
        before = LEDGER.read_bytes()
        verify()
        self.assertEqual(before, LEDGER.read_bytes())

if __name__ == "__main__":
    unittest.main()
