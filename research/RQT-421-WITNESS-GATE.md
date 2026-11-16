# RQT-421 — The Three-Path Witness Gate

Date: 2026-11-16.

## Actual executed audit

The full frozen RQT-401 JSON includes the original symmetric integral F4 matrix, the 4×3 reduced kernel basis B, and the restricted 3×3 Gram Q. Exact integer multiplication verifies:

**Bᵀ F4 B = Q**, with Q even and A=Q/2.

For every integer w∈Z³, the original mapped vector r=Bw therefore has norm rᵀF4r=2wᵀAw. For the homogenized H=diag(A,1), the exact norm of (w,d) is wᵀAw+d². A unimodular matrix U from RQT-419 has det U=1 and H'=UᵀHU; setting t=U⁻¹(w,d), the exact H' norm of t equals the H norm of (w,d).

Five test vectors were substituted through all representations; all identities passed, none was isotropic. The RQT-401 Gram fingerprint was checked against the prior published SHA256.

## Evidence boundary

These are three arithmetically equivalent checks of ONE original Gram source, **not three independent witnesses or ancestries**. A candidate is accepted as an explicit rational witness only after an actual primitive integer vector (w,d), d odd/nonzero, passes exact homogeneous norm zero. Root19 integral witness further demands d=±1, appropriate original Wall constraints, and frozen-prefix compatibility.

RQT-414 proves rational existence abstractly, but **no explicit vector was constructed here**. Root19 OPEN; root20 OPEN; root21 conditional. Candidate root18 ordering relative to the 17 frozen predecessors remains unverified.

## ASCII

```
        RQT-421 :: THREE-PATH WITNESS GATE
                 (w,d) ∈ Z^4
                      |
          +-----------+-----------+
          |           |           |
       ORIGINAL      REDUCED    CONGRUENT
          F4           Q/2         H'
          |            |           |
          +------------+-----------+
                       |
                   norm = 0?
                       |
                  gcd(w,d)=1?
                       |
                    d ODD?
                       |
                RATIONAL WITNESS
                   NOT FOUND
                       |
                   d = 1 ?
                       |
                 ROOT19 : OPEN
```

The high-definition JPG and an HTML with its JPEG embedded are available as separate conversation artifacts. The repository page remains ASCII-only.
