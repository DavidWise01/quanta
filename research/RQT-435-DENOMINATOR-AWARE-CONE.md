# RQT-435 — The Denominator-Aware Cone Gate

Date: 2026-11-16. Canonical RQT-401 full candidate-successor Gram. Source SHA256: 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809.

## Global denominator-aware theorem

Let A=Q/2, f=A22<0, L=A02*x+A12*y, M=A00*x²+2*A01*x*y+A11*y². For q(w)=-d² define E_d=L²-f(M+d²). For y nonzero, E_d/y² is a concave quadratic in x/y plus (-f)*d²/y². RQT-394 verified that this quadratic plus (-f) is strictly negative outside the rational interval (177065/100000,178600/100000), including at both exact endpoints. When 0<|d|<=|y|, the additional term is no larger than (-f). Therefore every genuine rational witness in this branch must obey the same strict slope corridor.

**The theorem does not apply its fixed cone to the complementary |d|>|y| branch.** Those candidates require a denominator-dependent analysis.

## Executed exact finite search

Checked y=1..3000, x strictly inside the exact cone, odd 1<=d<=min(25,y). Zero upper bound was placed on z. Applied exact nonresidue obstructions (13,23), modular square filters (256,63,65,11,17,19,23,31), nonnegative discriminant, integer square root, integral z and original F4 backmap checks.

| Gate | Cases |
|---|---:|
| Cone pairs (x,y) | 69,094 |
| (x,y,d) combinations | 898,201 |
| Excluded by primes 13/23 | 98,474 |
| Prime survivors | 799,727 |
| Modular square survivors | 3,239 |
| Nonnegative E_d | 3,238 |
| Exact square E_d | **0** |
| Rational or integer root witnesses | **0** |

The result is bounded; negative y is covered by simultaneous sign reversal of (x,y,z). The complement |d|>|y| and denominators above 25 remain unsearched. Rational existence from RQT-414 remains abstractly established, with no explicit coordinate witness.

## ASCII

```text
        RQT-435 : DENOMINATOR-AWARE CONE
                q(w)=-d²
                    |
          +---------+---------+
          |                   |
       |d|<=|y|            |d|>|y|
          |                   |
       narrow cone         no fixed cone
          |                   |
      prime 13,23          open region
          |                   |
      898201 cases        future solver
          |
      3239 mod squares
          |
      3238 nonnegative
          |
      ZERO exact squares
          X
       ROOT19 OPEN
```

Generated JPG is conceptual rather than mathematical evidence. GitHub and HTML mirror one original source ancestry. Frozen root18 compatibility UNVERIFIED, root19 OPEN, root20 OPEN, root21 conditional.

Next RQT-436: construct the expanding denominator-dominated cone and use it to search |d|>|y| without false exclusions.
