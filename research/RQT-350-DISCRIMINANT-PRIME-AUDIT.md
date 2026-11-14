# RQT-350 — Exact discriminant-prime audit and four new exclusions

**2026-11-14. Status: PASS for four newly certified rational-plane nonexistence results.** Authentic rank-four Gram F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, determinant independently checked. Original integral roots 18–21 remain OPEN.

## Progress from RQT-349

Of 31 adjacent-slope ternary planes, RQT-349 had rigorously excluded 21, leaving 10. RQT-350 adds **four exact odd-prime square obstruction certificates**, bringing the running tally to **25 excluded** and **6 unresolved**.

| slope m/n | bad prime p | radical mod p (a,b,c) | (v^T G v)/p mod p |
|---|---:|---|---:|
|196/197|32,790,353|(25,985,934; 27,145,414; 1)|9,242,088|
|200/201|307,273|(100,866; 273,575; 1)|145,715|
|841/840|2,492,311|(724,605; 637,158; 1)|152,989|
|844/843|661,417|(47,179; 44,181; 1)|395,865|

Every listed p is **prime**. Each divides det(G) to valuation exactly one; the leading 2x2 minor h is invertible mod p and -h is a quadratic nonresidue mod p, making the nondegenerate rank-two quotient anisotropic. The listed primitive radical v satisfies Gv=0 mod p, yet Q(v)/p is nonzero mod p. For any lift v+pz, the quadratic norm modulo p² remains Q(v), so no primitive p² null vector exists and therefore **no nonzero rational isotropic vector exists in that plane**. All of these facts are asserted and executed with arbitrary-precision arithmetic.

## Still unresolved

```text
188/189  192/193  194/195
199/200  201/202  851/850
```

**Unresolved is not a rational-root witness.** The determinant factoring investigation identified some small factors and some large unproved residual cofactors. RQT-350 does **not** claim a complete discriminant factorization or complete local-global audit of these six cases. Known small discriminant factors on these planes have not met the sufficient anisotropic-radical obstruction test; other primes, 2-adic conditions or a full ternary isotropy calculation remain possible.

## Reproduction and lineage

`python research/rqt350-discriminant-prime-audit.py` from `DavidWise01/quanta`; tested locally as `/mnt/data/rqt350_discriminant_audit.py` with JSON output `/mnt/data/rqt350_discriminant_audit.json`. This script is self-contained: it reconstructs all four ternary Gram matrices directly from the authentic F4 and checks the exact prime, valuation, Legendre, radical and norm assertions. No external JSON or unexplained numerical solver is required.

Earlier RQT-349 exclusions are referenced as their own existing certificates, not replayed by this shorter four-certificate script. The same original F4 provides the common evidence ancestry; distinct modular primes are derived arithmetic witnesses, not four separate primary sources.

## Next RQT-351

Choose one of the six unresolved planes for a **complete** rational-isotropy decision via certified local-global ternary quadratic-form algorithms (including 2-adic and large discriminant primes), or construct an exact full four-variable rational isotropic point. Once u is found, verify u^T F4 u=0, gcd(F4u)=1, RQT-334 Bezout root norm/parity and the RQT-257 exact Wall flag. No missing integral root has yet been produced.

The 3x3x3 cubit, Josophene/Juliet, brace-box-toroid and time-angle addresses remain research-index metadata.
