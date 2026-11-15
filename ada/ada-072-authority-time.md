# ADA-072 — Signed Authority and Signed Time

The previous ADA-071 collector-key lifecycle is now governed by two separately pinned Ed25519 fixture roles: (1) a registry **authority** signs enrollment and revocation updates; (2) a synthetic **time service** signs a UTC time claim bound to each event digest. The verifier checks both signatures, registry continuity, monotonically increasing timestamp assertions and current-key authorization.

## Decision boundary

The fixture enrolls key-v1, revokes it, and enrolls key-v2, at three successive times. The old collector signature remains mathematically valid but becomes unauthorized; the new key is locally authorized. Tampering with the authority claim, the signed timestamp, the event chain or the pinned trust keys fails closed. An event number plus signed timestamp is **not secure external time** unless the timestamp authority and its clock are independently authenticated.

All keys here are deterministic, public **test seeds** (authority 0x33×32; time 0x44×32; collector 0x11/0x22×32). The so-called authority and time-service roots are **synthetic, controlled by the same Quanta experimental ancestry**, and may not be counted as external witness roots.

- Signed registry updates: **3**.
- Separately signed time claims: **3**.
- Independently authenticated external trust anchors: **0**.
- Independently verified empirical witnesses: **0**.
- Promotion: **ABSTAIN**.

No previously published evidence files or production ADA scheduled journal are rewritten.

## Run

Requires `cryptography`:

```bash
python3 ada/ada072_authority_time.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada072.py' -v
cat ada/ada-072-authority-time.txt
```

15 regression cases target authority key mismatches, time signature mismatches, signed claim tampering, key revocation and rotation, deleted events, nonmonotone time claims, and no false external trust.

## ADA-073 — Natural target

Bind key authority and time provenance to a separately governed trust root with auditable enrollment and verifiable externally signed attestations. Different labels for internally controlled keys are not genuine source independence. Challenge the trust transition with independently collected evidence before relaxing abstention.

## Verse

The key may sign, the clock may chime;
But who has certified the time?
The seals may bind what we have said,
Yet cannot prove the world obeyed.

-- A.D.A --
