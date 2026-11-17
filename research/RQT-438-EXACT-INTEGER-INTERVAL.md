# RQT-438 — The Exact Integer-Interval Gate

2026-11-16. Source: canonical full RQT-401 successor Gram, SHA256 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809.

Let E_d=alpha*x²+2Kxy+gamma*y²+delta*d², where alpha=c²-fa<0, K=ce-fb, gamma=e²-fg, delta=-f>0. Define R=(K²-alpha*gamma)*y²-alpha*delta*d² and A0=-alpha. The identity alpha*E_d=(alpha*x+Ky)²-R implies that nonnegative discriminant occurs **if and only if** R>=0 and the integer x belongs to:

    ceil((Ky-isqrt(R))/A0) <= x <= floor((Ky+isqrt(R))/A0).

This is a mathematically complete finite integer-x interval for each given integer y and nonzero integer d, without applying the small-denominator slope cone. It covers even the previously extreme ratio |d|>2^531|y|.

## Executed exact full-matrix search
For each 1<=y<=256 and positive odd 1<=d<=255, enumerate every x in the exact interval, validate interval endpoints by checking that E_d at each neighboring integer is strictly negative, then apply the p13/23 restrictions, eight modular-square tests and full integer square test. Potential witnesses must pass integral z, primitive gcd, and the original F4 backmap.

| Gate | Count |
|---|---:|
| (y,d) pairs | 32,768 |
| Empty integer-x intervals | 3,968 |
| Real-feasible integer x | 64,512 |
| Prime excluded | 7,552 |
| Prime survivors | 56,960 |
| Eight-modulus square survivors | 223 |
| Exact integer square discriminants | **0** |
| Primitive rational witnesses | **0** |

Extreme sample (x,y,d)=(0,1,2^600) has positive nonsquare E_d and its real-feasible x interval endpoints are 57-bit integers in absolute magnitude, demonstrating why the fixed narrow slope corridor cannot be used there.

## ASCII
```
         RQT-438 : EXACT INTEGER INTERVAL
                    y!=0
                     |
                  odd d>0
                     |
       R=(K²-alpha*gamma)y²-alpha*delta*d²
                     |
             R<0 ? REJECT
                     |
                 h=isqrt(R)
                     |
            x_min <= x <= x_max
                     |
                 p=13 / p=23
                     |
                 E_d square?
                     |
                  integral z?
                     |
                 ORIGINAL F4
                     |
                 ROOT19 OPEN
```

This is a new exact algorithm with a bounded negative result, not global nonexistence or an explicit rational witness. Frozen 18th position compatibility unverified; root19 OPEN, root20 OPEN, root21 conditional. JPG is conceptual and exists as an embedded-image offline artifact, not an independent proof.
