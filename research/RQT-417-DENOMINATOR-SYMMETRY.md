# RQT-417 — The Denominator Symmetry Gate

Date: 2026-11-16. Source: full frozen RQT-401 candidate-successor Gram.

## Exact theorem

For any integral quadratic form q and integers d,m satisfying gcd(d,m)=1, multiplication by d has an inverse modulo m. The coordinatewise map w↦d⁻¹w is a bijection between residue solutions to q(w)≡−d² (mod m) and q(u)≡−1 (mod m). This is valid for every positive integer modulus relatively prime to d, not only primes.

Thus **mere existence and counts** of modular solutions at moduli coprime to d cannot distinguish rational denominator d from denominator 1. This theorem does not imply globally integral solvability: the modulus may share factors with d and global height/integrality and original Wall constraints remain.

## Independent exact enumerations on actual A=Q/2

* m=4, d∈{1,3,5,7}: 24 solutions for each d.
* m=8, d∈{1,3,5,7}: 96 solutions for each d.
* m=9, d∈{1,2,4,5,7,8}: 162 solutions for each d.
* m=11, d∈{1,2,3,5,7}: 110 solutions for each d.

The verifier enumerates both sets and asserts their equality after mapping by d modulo m.

## ASCII narrative

```
             RQT-417 :: DENOMINATOR SYMMETRY
               +------------------------+
               |       q(w) = -d^2     |
               +-----------+------------+
                           |
                      gcd(d,m)=1
                           |
                    u = inv(d)*w
                           |
                      q(u) = -1
                           |
                SAME MODULAR COUNTS
                    /           \
                d = 1           d > 1
                    \           /
                      INTEGER?
                         |
                     ROOT19 OPEN
```

RQT-414 proves rational existence abstractly; no explicit rational coordinates were produced in RQT-417. RQT-416's invalid trial witnesses remain invalid. Integer root19 OPEN, root20 OPEN, root21 conditional. RQT-386 candidate's position 18 relative to frozen predecessor remains unverified.

The 3D JPG and embedded-JPG HTML are provided as separate conversation artifacts; this GitHub chapter has ASCII visuals.
