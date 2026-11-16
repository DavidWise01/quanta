# RQT-433 — The First-Seed Obstruction Gate

Date: 2026-11-16. **Actual canonical RQT-401 Gram**, source SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. Exact backmap `B^T F4 B=Q` checked. The RQT-386 candidate has not been verified against the frozen 17-reflection prefix.

For `A=Q/2`, let `q(x,y,z)=a*x²+2*b*xy+2*c*xz+g*y²+2*e*yz+f*z²`, `L=c*x+e*y`, and `M=a*x²+2*b*xy+g*y²`. A primitive rational witness must satisfy `q(x,y,z)+d²=0` over integers with nonzero odd `d`.

Modulo any odd prime p dividing f, the equation becomes `d² ≡ -M-2Lz (mod p)`. **Both p=13 and p=23 divide f and satisfy c+5e=0 (mod p)**. On `y=5x mod p`, L vanishes and the z-term disappears.

* p=13: `d² ≡ 11x² (mod 13)`; 11 is a quadratic nonresidue. No solution for x nonzero mod13.
* p=23: `d² ≡ 7x² (mod 23)`; 7 is a quadratic nonresidue. No solution for x nonzero mod23.

These are **unbounded necessary restrictions**: exactly 12 of 169 xy residue pairs modulo13 and 22 of 529 modulo23 are excluded. Inclusion–exclusion modulo299 excludes **9,802 of 89,401** xy classes, without limiting z or d. The checker independently enumerates all residue z,d possibilities for each forbidden xy and certifies the exact CRT count.

Two excluded pairs nevertheless lie inside the exact RQT-394 real cone `177065/100000 < x/y < 178600/100000`: **(41,23)** (13 obstruction) and **(140,79)** (23 obstruction). Real-cone eligibility therefore does not imply a first rational Pell seed.

## ASCII diagram
```text
     RQT-433 : FIRST-SEED OBSTRUCTION
    +---------------------------------+
    | q(x,y,z)+d²=0                 |
    |             |                   |
    |       y = 5*x (mod p)          |
    |          /        \\             |
    |        p=13       p=23         |
    |      d²=11x²    d²=7x²        |
    |      NONSQUARE  NONSQUARE     |
    |          \\        /             |
    |      NO FIXED SEED             |
    | 9802/89401 xy classes gone     |
    |             |                   |
    |         ROOT19 OPEN            |
    +---------------------------------+
```

The neon JPG is conceptual art, not proof. Multiple GitHub/HTML records derive from one canonical matrix and do not constitute independent source ancestry. Explicit rational witness **OPEN**, integer root 19 **OPEN**, root 20 **OPEN**, root 21 conditional.

Next RQT-434: use these global pair exclusions together with the exact real cone and square-compression test in a certified first-seed construction search.