# RQT-584 — The Pell Discriminant Obstruction

**New exact result:** 12 of RQT-583's 80 unresolved Pell ray-offset families are excluded for *all integer scale parameters*. Selected family ledger: **67/135 excluded, 68/135 unresolved**. No integer norm−2 root and no Root 19 certificate.

Let Δ(t)=At²+Bt+C, D=B²−4AC. If an odd prime p satisfies p∤A, Legendre(A,p)=−1 and v_p(D)=1, then completing the square gives Δ(t)≡A(t−t0)² mod p, where t0=−B(2A)⁻¹ mod p. Off t0, the value is a quadratic nonresidue; at t0 it has valuation exactly one, so never an integer square. This is a rigorous all-scale exclusion.

**New certified family IDs and prime gates:**
- p=257: families 86 and 102
- p=281: families 60 and 74
- p=409: families 82 and 106
- p=1151: families 108 and 134
- p=1223: families 88 and 100
- p=1583: families 6 and 20

Exact integer verifier independently reconstructs the polynomial from original RQT-575 reduced Gram and RQT-583 ray/offset data at five signed scales, checks primes, quadratic nonresidues, discriminant valuation one and exceptional-root residues modulo p². Local JSON contains all 12 modulus certificates and source SHA256 fingerprints. This does not establish global nonrepresentation because 135 ray-offset families are only a restricted parameterization, and 68 of them remain unresolved.

**Not performed:** original 22D Wall ancestry and full reflection verification, since no exact norm−2 root was found. Root19 OPEN. The {{i}} nested primitive/recursive angular coordinates remain architecture, not a proven physical implementation.

**Next RQT-585:** solve or obstruct one of the 68 surviving generalized Pell equations with exact t integrality and eliminated-coordinate checks.

Local conversation artifacts: rqt584.py, results.json, RQT-584-RESEARCH.md, original Egyptian-art-deco laboratory JPEG and self-contained JPEG-embedded HTML. GitHub edition text-only; Pages and binary image repo publication unverified.
