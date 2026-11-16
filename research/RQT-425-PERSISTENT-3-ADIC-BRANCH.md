# RQT-425 — The Persistent 3-Adic Branch

Date: 2026-11-16. Source: exact full RQT-401 candidate-successor Gram. The conditional root18 has not been matched to the frozen 17-reflection predecessor.

## Infinite constructive local result

Let A=Q/2 and q(w)=w^T A w. The actual A mod27 is [[8,3,14],[3,0,21],[14,21,2]]. Specialize w=(1,y,2), d=3k. All coefficients of the polynomial q(1,y,2) are divisible by 9 as integers. Hence P_k(y)=q(1,y,2)/9+k² is a polynomial over Z with P_k(y) ≡ 2+y+k² (mod 3) and derivative P'_k(y) ≡ 1 (mod 3).

For each k in Z_3, there is a unique root y modulo 3 and derivative is a unit. Hensel lifting gives a unique compatible y in Z_3, with the numerator primitive because x=1. Therefore every denominator d divisible by 3 occurs for this 3-adic solution family. This proves infinite *local* persistence, not rational or integral existence.

## Independent exact enumeration

| Modulus | Primitive triples, d=3 | Primitive triples, d=9 |
|---|---:|---:|
| 9 | 216 | 216 |
| 27 | 972 | 1944 |
| 81 | 8748 | 17496 |
| 243 | 78732 | 157464 |

The verifier enumerates all 27 lifts per surviving parent and separately constructs compatible y residues through 3^12 for k=1,3,9. Both checks were run against the saved full Gram.

## ASCII

```
         RQT-425 : PERSISTENT 3-ADIC BRANCH
       +------------------------------------+
       | q(w) = -d², w=(1,y,2), d=3k       |
       +------------------+-----------------+
                          |
            P_k(y)=2+y+k² (mod 3)
                          |
                P'_k(y)=1 (mod 3)
                          |
                  HENSEL LIFT
               /                 \
             d=3                 d=9
               |                   |
        9  : 216             9  : 216
       27  : 972            27  : 1944
       81  : 8748           81  : 17496
      243  : 78732         243  : 157464
               \                   /
                 EVERY 3^n
                      |
              INTEGER ROOT 19?
                    OPEN
```

Rational existence from RQT-414 remains abstract; no rational witness or ordinary integer root19 is claimed. The generated JPG is conceptual, and the GitHub/HTML mirrors share a single source ancestry.

Root19 OPEN; root20 OPEN; root21 conditional.

Next: instead of further 3-adic enumeration, target constructive global rational isotropy with exact coordinate output and cross-check to F4/H4.
