#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from ada069_lineage import (fixture, inspect_capture, compare_captures,
                            verify_registry, create_registry)
from ada068_raw_capture import synthetic_fixture, persist_create_only, SOURCE, make_record

class ADA069Tests(unittest.TestCase):
    def setUp(self):
        self.report=fixture()
    def test_one_publication_two_capture_events(self):
        c=self.report["comparison"]
        self.assertEqual(c["publication_roots"],1)
        self.assertEqual(c["capture_events"],2)
    def test_byte_delta_retained(self):
        d=self.report["comparison"]["delta"]
        self.assertEqual(d["comparison"],"content_changed")
        self.assertEqual(len(d["changed_offsets"]),1)
    def test_same_root_distinct_capture_identity(self):
        c=self.report["comparison"]
        self.assertEqual(c["left"]["source_root"],c["right"]["source_root"])
        self.assertNotEqual(c["left"]["capture_id"],c["right"]["capture_id"])
    def test_synthetic_cannot_claim_authentication(self):
        c=self.report["comparison"]
        self.assertFalse(c["left"]["external_signature_verified"])
        self.assertFalse(c["right"]["external_signature_verified"])
        self.assertEqual(c["authenticated_collector_attestations"],0)
    def test_no_false_witnesses_or_promotion(self):
        c=self.report["comparison"]
        self.assertEqual(c["independent_empirical_witness_roots"],0)
        self.assertEqual(c["decision"],"abstain")
    def test_valid_registry(self):
        self.assertTrue(verify_registry(self.report["events"]))
        self.assertEqual(len(self.report["events"]),4)
    def test_tampered_registry_rejected(self):
        rows=json.loads(json.dumps(self.report["events"]))
        rows[2]["payload"]["comparison"]="identical"
        with self.assertRaises(ValueError):verify_registry(rows)
    def test_deleted_event_rejected(self):
        rows=self.report["events"][:1]+self.report["events"][2:]
        with self.assertRaises(ValueError):verify_registry(rows)
    def test_create_only_registry(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"events.jsonl"
            create_registry(p,self.report["events"])
            with self.assertRaises(FileExistsError):
                create_registry(p,self.report["events"])
            self.assertTrue(verify_registry([json.loads(s) for s in p.read_text().splitlines()]))
    def test_capture_integrity_detects_tamper(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/"snapshot"
            raw,meta=synthetic_fixture()
            persist_create_only(raw,meta,path)
            self.assertEqual(inspect_capture(path)["byte_length"],len(raw))
            (path/"response.bin").write_bytes(raw+b"x")
            with self.assertRaises(ValueError):inspect_capture(path)
    def test_equal_bytes_with_separate_capture_events(self):
        with tempfile.TemporaryDirectory() as root:
            raw,meta=synthetic_fixture()
            for name in ("a","b"):
                persist_create_only(raw,meta,Path(root)/name)
            result=compare_captures(Path(root)/"a",Path(root)/"b")
            self.assertEqual(result["delta"]["comparison"],"identical")
            self.assertEqual(result["publication_roots"],1)
    def test_deterministic(self):
        self.assertEqual(fixture(),fixture())

if __name__=="__main__":
    unittest.main()
