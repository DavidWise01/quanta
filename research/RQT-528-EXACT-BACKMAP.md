# RQT-528 — Exact Affine Back-Map

Frozen conditional Gram SHA256: `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. Exact RQT-520 input SHA256: `e02cd985b505c431fe4c66911d7dd0bf06dcb3299a3c7d77aade5e7a0afa10e2`.

For the quadratic `Q=a x²+2bxy+g y²+2cxz+2eyz+f z²+1`, set `A=fg−e²`, `B=ce−fb`, `C=c²−fa`, `J=B²+AC`. Exact checks: `9|A`, `9|B`, `9f|J`, `gcd(A,B)=9`. Put `α=A/9, β=B/9, H=J/(9f)`; `gcd(α,β)=1`.

**Exact affine coordinates**: `v=αy−βx`, `k=cx+ey+fz`.

**Full defect identity** (all integers x,y,z):
`9v²+αk²=f(Hx²−α+αQ)`.

For `Q=0`, necessary reduced norm equation:
`9v²+αk²=f(Hx²−α)`.

**Exact if-and-only-if original integer back-map** for any integer representation v,k at fixed x:
`α|(v+βx)`, `y=(v+βx)/α`;
`f|(k−cx−ey)`, `z=(k−cx−ey)/f`.
The affine lattice of valid (v,k) has index `|αf|` inside Z². Representations without both divisibility conditions are not integer roots.

**Executed**: all 73 RQT-523 surviving fixed-x corridors tested; five deterministic (y,z) examples each, 365 exact integer identity and inverse assertions passed. Exhaustive modular norm-pair counts (3,9,27,81) = (146,438,1314,3942), and every pair already satisfies `3|u` with u=3v. Thus 0 additional 3-adic exclusions.

**0 new exclusions**: original 720-corridor sample remains 647 conditionally excluded, 73 open. **Root19 OPEN; predecessor18 UNVERIFIED.** No global norm representation or full class group computed. The seven-level base-60 seeded-cross remains a navigation frame, not exhaustively traversed.

**Next RQT-529:** global norm representation in the correct affine coset, or independent root-18 predecessor certificate.

Reproducible local Python, JSON, research Markdown, new JPEG and JPEG-embedded HTML are attached in the conversation; committed GitHub HTML is the research-text edition.
