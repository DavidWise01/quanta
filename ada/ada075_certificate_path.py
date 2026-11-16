#!/usr/bin/env python3
"""ADA-075: three-certificate Ed25519 X.509 path verifier.

REAL certificate signatures and subject/issuer links are verified against
explicitly pinned synthetic root bytes. Revocation status is supplied as a
separate local fixture; there is NO OCSP/CRL fetch, PKIX policy-tree handling,
external PKI enrollment, or authenticated wall clock. Fail closed.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

VERSION="ADA075-x509-path-v1"
NOW=datetime(2026,11,15,18,0,0,tzinfo=timezone.utc)
HOST="capture.example.test"
SEEDS=(bytes([0x55])*32,bytes([0x66])*32,bytes([0x77])*32)

def key(n):
    return Ed25519PrivateKey.from_private_bytes(SEEDS[n])

def subject(name):
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,name)])

def make_cert(issuer_name, subject_name, public, signing_key, serial,
              *, ca=False, hostname=None, server=False, before=None, after=None):
    start=before or NOW-timedelta(days=1)
    end=after or NOW+timedelta(days=1)
    builder=(x509.CertificateBuilder().subject_name(subject(subject_name))
        .issuer_name(subject(issuer_name)).public_key(public).serial_number(serial)
        .not_valid_before(start).not_valid_after(end)
        .add_extension(x509.BasicConstraints(ca=ca,path_length=(1 if ca else None)),critical=True))
    if ca:
        builder=builder.add_extension(x509.KeyUsage(
            digital_signature=False,content_commitment=False,
            key_encipherment=False,data_encipherment=False,key_agreement=False,
            key_cert_sign=True,crl_sign=True,encipher_only=False,decipher_only=False),critical=True)
    if hostname:
        builder=builder.add_extension(x509.SubjectAlternativeName([x509.DNSName(hostname)]),critical=False)
    if server:
        builder=builder.add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),critical=False)
    return builder.sign(signing_key,algorithm=None)

def fixture():
    root_key,inter_key,leaf_key=[key(i) for i in range(3)]
    root=make_cert("fixture-root","fixture-root",root_key.public_key(),root_key,1001,ca=True)
    inter=make_cert("fixture-root","fixture-intermediate",inter_key.public_key(),root_key,1002,ca=True)
    leaf=make_cert("fixture-intermediate","fixture-collector",leaf_key.public_key(),
                   inter_key,1003,hostname=HOST,server=True)
    pinned=hashlib.sha256(root.public_bytes(serialization.Encoding.DER)).hexdigest()
    statuses={str(c.serial_number):{"status":"good",
        "this_update":(NOW-timedelta(hours=1)).isoformat(),
        "next_update":(NOW+timedelta(hours=1)).isoformat()} for c in (leaf,inter)}
    return (leaf,inter,root),pinned,statuses

def _bounds(c):
    # Compatible with older and newer cryptography releases.
    return (c.not_valid_before.replace(tzinfo=timezone.utc),
            c.not_valid_after.replace(tzinfo=timezone.utc))

def verify_path(chain,pinned_root_sha256,statuses,*,hostname=HOST,now=NOW):
    """Restricted RFC5280-inspired fixture validator, NOT general PKIX."""
    if len(chain)!=3:
        raise ValueError("requires leaf, intermediate and root")
    leaf,inter,root=chain
    der=root.public_bytes(serialization.Encoding.DER)
    if hashlib.sha256(der).hexdigest()!=pinned_root_sha256:
        raise ValueError("untrusted root")
    if root.issuer!=root.subject or leaf.issuer!=inter.subject or inter.issuer!=root.subject:
        raise ValueError("broken issuer chain")
    for cert,issuer in ((leaf,inter),(inter,root),(root,root)):
        issuer.public_key().verify(cert.signature,cert.tbs_certificate_bytes)
        lower,upper=_bounds(cert)
        if not lower<=now<=upper:
            raise ValueError("certificate time invalid")
    for ca in (inter,root):
        if not ca.extensions.get_extension_for_class(x509.BasicConstraints).value.ca:
            raise ValueError("issuer is not a CA")
        if not ca.extensions.get_extension_for_class(x509.KeyUsage).value.key_cert_sign:
            raise ValueError("issuer cannot sign certificates")
    if leaf.extensions.get_extension_for_class(x509.BasicConstraints).value.ca:
        raise ValueError("leaf cannot be CA")
    eku=leaf.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
    if ExtendedKeyUsageOID.SERVER_AUTH not in eku:
        raise ValueError("incorrect leaf purpose")
    sans=leaf.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
    if hostname not in sans.get_values_for_type(x509.DNSName):
        raise ValueError("hostname not in exact DNS SAN list")
    for cert in (leaf,inter):
        s=statuses.get(str(cert.serial_number))
        if not s or s.get("status")!="good":
            raise ValueError("revoked or missing revocation evidence")
        try:
            start=datetime.fromisoformat(s["this_update"])
            end=datetime.fromisoformat(s["next_update"])
        except (ValueError,KeyError,TypeError):
            raise ValueError("malformed revocation timing")
        if start.tzinfo is None or end.tzinfo is None or not start<=now<=end:
            raise ValueError("expired or untrusted revocation claim")
    return {"chain_signatures_valid":True,"root_pinned":True,
            "dns_san_matched":True,"local_status_fresh":True,
            "revocation_source_authenticated":False,
            "external_trust_anchor_authenticated":False,
            "independent_empirical_witnesses":0,
            "promotion":"abstain"}

def run():
    chain,pin,status=fixture()
    result=verify_path(chain,pin,status)
    return {"version":VERSION,"certificates":len(chain),"test_root_sha256":pin,
            "status_origin":"synthetic-local-revocation-fixture",
            "result":result,"real_external_capture":False}

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
