# ADA-073 — Governance Independence Gate

This iteration sits **above** ADA-072's signed-registry/time fixture. It links a governance assertion to the current registry-event hash, capture binding, collector key ID and publication source ancestry. Records are deterministic, content-hashed and never rewrite the earlier journal.

The three trial claims are (1) Quanta-owned governance, (2) a copied public mirror, and (3) a differently labeled but **unauthenticated** authority. The result is zero independently authenticated governance roots. A structurally eligible external-root fixture is tested separately, but its self-declared independent label does not constitute real verification.

The checks deliberately separate:
- Cryptographic key validity (ADA-070).
- Current enrollment and revocation (ADA-071).
- Signature and timestamp *assertions* (ADA-072).
- **Governance independence** (ADA-073).
- Independently observed empirical reality (still unavailable).

A verifier cannot bootstrap external trust merely by allowing a user-controlled assertion `identity_independently_authenticated=true`; a real trust anchor must be established outside this code and fixture. Even an authenticated external governor would not itself prove a published numerical result or physical observation. Actual promotion stays **ABSTAIN**.

Run:
```bash
python3 ada/ada073_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada073.py' -v
cat ada/ada-073-governance.txt
```

Fourteen regression tests cover copied sources, key-label laundering, repeated roots, mismatched capture bindings, tampered packets, synthetic structural passes, and continued abstention.

## Next natural invariant — ADA-074

Use a separately acquired and authenticated external authority document to bootstrap a read-only trust policy. Record who governed the key, on what basis, and when, instead of trusting a Boolean field in a self-authored packet.

## A.D.A

Three masks may take the evening stage,
Yet share the pen that wrote the page.
