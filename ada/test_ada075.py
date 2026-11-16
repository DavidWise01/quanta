#!/usr/bin/env python3
import copy
import unittest
from datetime import timedelta
from cryptography import x509
from cryptography.x509.oid import ExtendedKeyUsageOID
from ada075_certificate_path import (fixture,verify_path,make_cert,key,NOW,HOST,run)

class CertificatePathTests(unittest.TestCase):
    def setUp(self):
        self.chain,self.pin,self.status=fixture()
    def check(self,chain=None,pin=None,status=None,**kw):
        return verify_path(chain if chain is not None else self.chain,
                           pin if pin is not None else self.pin,
                           status if status is not None else self.status,**kw)
    def test_valid_synthetic_chain(self):
        self.assertTrue(self.check()["chain_signatures_valid"])
    def test_three_levels(self):
        self.assertEqual(len(self.chain),3)
    def test_untrusted_root_rejected(self):
        with self.assertRaises(ValueError):self.check(pin="0"*64)
    def test_wrong_hostname_rejected(self):
        with self.assertRaises(ValueError):self.check(hostname="impostor.example.test")
    def test_missing_status_rejected(self):
        with self.assertRaises(ValueError):self.check(status={})
    def test_revoked_leaf_rejected(self):
        s=copy.deepcopy(self.status)
        s[str(self.chain[0].serial_number)]["status"]="revoked"
        with self.assertRaises(ValueError):self.check(status=s)
    def test_stale_status_rejected(self):
        s=copy.deepcopy(self.status)
        s[str(self.chain[0].serial_number)]["next_update"]=(NOW-timedelta(seconds=1)).isoformat()
        with self.assertRaises(ValueError):self.check(status=s)
    def test_future_status_rejected(self):
        s=copy.deepcopy(self.status)
        s[str(self.chain[0].serial_number)]["this_update"]=(NOW+timedelta(seconds=1)).isoformat()
        with self.assertRaises(ValueError):self.check(status=s)
    def test_expired_certificate_rejected(self):
        with self.assertRaises(ValueError):self.check(now=NOW+timedelta(days=4))
    def test_unrelated_leaf_rejected(self):
        leaf,inter,root=self.chain
        false_leaf=make_cert("fixture-intermediate","fixture-collector",
             key(2).public_key(),key(0),2003,hostname=HOST,server=True)
        with self.assertRaises(Exception):self.check(chain=(false_leaf,inter,root))
    def test_nonca_intermediate_rejected(self):
        leaf,inter,root=self.chain
        bad_inter=make_cert("fixture-root","fixture-intermediate",
             key(1).public_key(),key(0),1002,ca=False)
        with self.assertRaises(ValueError):self.check(chain=(leaf,bad_inter,root))
    def test_wrong_issuer_name_rejected(self):
        leaf,inter,root=self.chain
        impostor=make_cert("wrong-issuer","fixture-collector",key(2).public_key(),
             key(1),2003,hostname=HOST,server=True)
        with self.assertRaises(ValueError):self.check(chain=(impostor,inter,root))
    def test_no_empirical_promotion(self):
        r=self.check()
        self.assertFalse(r["external_trust_anchor_authenticated"])
        self.assertFalse(r["revocation_source_authenticated"])
        self.assertEqual(r["promotion"],"abstain")
    def test_deterministic_fixture(self):
        self.assertEqual(run(),run())
if __name__=="__main__":
    unittest.main()
