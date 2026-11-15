#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from ada067_temporal import (build_fixture,compare,verify_events,
                              export_create_only, digest)
from ada066_capture import CAPTURE,verify as verify_066

class TemporalTests(unittest.TestCase):
    def setUp(self):
        self.report=build_fixture()
        self.base=CAPTURE.read_bytes()
    def test_original_hash_unchanged(self):
        self.assertEqual(digest(self.base),verify_066()["capture_sha256"])
    def test_same_bytes(self):
        self.assertEqual(compare(self.base,self.base,label="test")["comparison"],"identical")
    def test_mutation_detected(self):
        x=compare(self.base,self.base.replace(b"5 677",b"5 678"),label="test")
        self.assertEqual(x["comparison"],"content_changed")
        self.assertEqual(len(x["changed_offsets"]),1)
    def test_truncation_detected(self):
        x=compare(self.base,self.base[:-1],label="test")
        self.assertEqual(x["comparison"],"length_changed")
        self.assertEqual(x["changed_offsets"],[len(self.base)-1])
    def test_second_capture_not_second_source(self):
        self.assertTrue(all(x["same_publication_ancestry"]
                            for x in self.report["synthetic_diagnostics"]))
        self.assertEqual(self.report["distinct_source_publications"],1)
    def test_unavailable_is_not_a_capture(self):
        self.assertFalse(self.report["actual_new_source_snapshot"])
        self.assertEqual(self.report["live_source_status"],"unavailable:403")
    def test_chain_is_valid(self):
        self.assertTrue(verify_events(self.report["events"]))
        self.assertEqual(len(self.report["events"]),5)
    def test_tamper_rejected(self):
        rows=json.loads(json.dumps(self.report["events"]))
        rows[2]["detail"]["comparison"]="identical"
        with self.assertRaises(ValueError):verify_events(rows)
    def test_missing_event_rejected(self):
        rows=self.report["events"][:2]+self.report["events"][3:]
        with self.assertRaises(ValueError):verify_events(rows)
    def test_exclusive_export(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"events.jsonl"
            export_create_only(path,self.report["events"])
            original=path.read_bytes()
            with self.assertRaises(FileExistsError):export_create_only(path,self.report["events"])
            self.assertEqual(original,path.read_bytes())
            self.assertTrue(verify_events([json.loads(s) for s in path.read_text().splitlines()]))
    def test_no_promotion(self):
        self.assertEqual(self.report["promotion"],"abstain")
        self.assertEqual(self.report["independent_empirical_witnesses"],0)
    def test_deterministic(self):
        self.assertEqual(self.report,build_fixture())

if __name__=="__main__":
    unittest.main()
