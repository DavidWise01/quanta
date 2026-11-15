#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from ada068_raw_capture import (SOURCE,ANCESTRY,make_record,persist_create_only,
                                verify,synthetic_fixture,sha)

class RawCaptureTests(unittest.TestCase):
    def test_synthetic_fixture_not_network(self):
        raw,record=synthetic_fixture()
        self.assertEqual(record["capture_provenance"],"synthetic-not-network")
        self.assertFalse(record["transport_claim"])
        self.assertEqual(record["response_body_sha256"],sha(raw))
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"capture"
            raw,r=synthetic_fixture()
            persist_create_only(raw,r,p)
            self.assertEqual(verify(p)["bytes"],len(raw))
    def test_exclusive_create(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"capture"
            raw,r=synthetic_fixture()
            persist_create_only(raw,r,p)
            with self.assertRaises(FileExistsError):
                persist_create_only(raw,r,p)
    def test_corrupt_bytes(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"capture"
            raw,r=synthetic_fixture()
            persist_create_only(raw,r,p)
            (p/"response.bin").write_bytes(raw+b"extra")
            with self.assertRaises(ValueError):verify(p)
    def test_corrupt_metadata(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"capture"
            raw,r=synthetic_fixture()
            persist_create_only(raw,r,p)
            m=json.loads((p/"manifest.json").read_text())
            m["independent_witness_roots"]=3
            (p/"manifest.json").write_text(json.dumps(m))
            with self.assertRaises(ValueError):verify(p)
    def test_redirect_rejected(self):
        with self.assertRaises(ValueError):
            make_record(b"abc",requested_url=SOURCE,final_url="https://example.com",
                        status=200,headers={})
    def test_http_error_rejected(self):
        with self.assertRaises(ValueError):
            make_record(b"blocked",requested_url=SOURCE,final_url=SOURCE,
                        status=403,headers={})
    def test_empty_capture_rejected(self):
        with self.assertRaises(ValueError):
            make_record(b"",requested_url=SOURCE,final_url=SOURCE,
                        status=200,headers={})
    def test_headers_whitelist(self):
        _,m=synthetic_fixture()
        self.assertEqual(m["response_headers"],{"content-type":"text/plain"})
    def test_lineage_and_abstention(self):
        _,m=synthetic_fixture()
        self.assertEqual(m["source_ancestry"],ANCESTRY)
        self.assertEqual(m["promotion"],"abstain")
    def test_fixture_is_deterministic(self):
        self.assertEqual(synthetic_fixture(),synthetic_fixture())

if __name__=="__main__":
    unittest.main()
