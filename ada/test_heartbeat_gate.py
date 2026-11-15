#!/usr/bin/env python3
"""ADA-053 heartbeat gate tests use scratch ledgers only."""
import tempfile
import unittest
from pathlib import Path
from kernel import genesis
from persist_tick import append_scheduled_tick
from heartbeat_gate import status

class HeartbeatGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)/"events.jsonl"
        genesis(self.path)
    def tearDown(self):
        self.temp.cleanup()
    def test_genesis_is_valid_but_not_a_second_heartbeat(self):
        result = status(self.path)
        self.assertTrue(result["chain_valid"])
        self.assertFalse(result["second_heartbeat_observed"])
        self.assertEqual(result["event_count"],1)
    def test_one_tick_is_not_enough(self):
        append_scheduled_tick(self.path, "11001")
        result = status(self.path)
        self.assertFalse(result["second_heartbeat_observed"])
        self.assertEqual(result["last_seq"],1)
    def test_two_distinct_ticks_open_gate(self):
        append_scheduled_tick(self.path,"11001")
        prefix=self.path.read_bytes()
        append_scheduled_tick(self.path,"11002")
        result = status(self.path)
        self.assertTrue(result["second_heartbeat_observed"])
        self.assertEqual(result["last_seq"],2)
        self.assertEqual(result["step"],2)
        self.assertEqual(result["second_run_id"],"11002")
        self.assertTrue(self.path.read_bytes().startswith(prefix))
    def test_duplicate_run_does_not_open_gate(self):
        append_scheduled_tick(self.path,"11001")
        before=self.path.read_bytes()
        append_scheduled_tick(self.path,"11001")
        self.assertEqual(self.path.read_bytes(),before)
        self.assertFalse(status(self.path)["second_heartbeat_observed"])
    def test_tampered_second_witness_fails_closed(self):
        append_scheduled_tick(self.path,"11001")
        append_scheduled_tick(self.path,"11002")
        self.path.write_bytes(self.path.read_bytes().replace(b"11002",b"22002"))
        with self.assertRaises(ValueError):
            status(self.path)
if __name__=="__main__":
    unittest.main()
