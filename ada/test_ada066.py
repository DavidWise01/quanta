import unittest
import tempfile
from pathlib import Path
from ada066_capture import verify,CAPTURE,MANIFEST

class CaptureTests(unittest.TestCase):
    def test_valid_normalized_excerpt(self):
        self.assertEqual(verify()["matches"],8)
    def test_not_raw_http_response(self):
        self.assertIn("NOT raw HTTP response",verify()["archive_kind"])
    def test_evidence_remains_unpromoted(self):
        self.assertEqual(verify()["physical_witnesses"],0)
        self.assertEqual(verify()["promotion"],"abstain")
    def test_tampered_value_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"capture.txt"
            p.write_bytes(CAPTURE.read_bytes().replace(b"5 677",b"5 678"))
            with self.assertRaises(ValueError):verify(p,MANIFEST)
    def test_truncated_capture_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"capture.txt"
            p.write_bytes(CAPTURE.read_bytes()[:-1])
            with self.assertRaises(ValueError):verify(p,MANIFEST)
    def test_source_capture_unchanged(self):
        old=CAPTURE.read_bytes()
        verify()
        self.assertEqual(old,CAPTURE.read_bytes())
if __name__=="__main__":
    unittest.main()
