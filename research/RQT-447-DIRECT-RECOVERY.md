# RQT-447 — Direct Coordinate Recovery

For f nonzero, E=L²−fC>=0, the real roots of fz²+2Lz+C=0 are at distance sqrt(E)/|f| from −L/f. When E<f², every integral root belongs to {floor(−L/f),floor(−L/f)+1}. More generally put j=isqrt(floor(E/f²)); the four candidates relative to floor(−L/f) are −j,−j−1,j,j+1. Exact substitution is necessary and sufficient. The general algorithm passed 45,384 exhaustive controls with both signs of f.

Executed frozen Gram SHA 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809; verified B^T F4 B=Q. New exact interval scan d=1, y=3001..10000: 697951 feasible x values, all with E<f², 1395902 direct coordinate substitutions and zero witnesses. The integer-x interval still uses isqrt; the discriminant sqrt is bypassed. Sign symmetry handles negative y. Earlier RQT-434 covered the d=1 branch to y=3000; its exclusions rely on the earlier cone theorem. No global nonexistence claim. Root19 OPEN; frozen position18 UNVERIFIED.

Next: certify a uniform height bound for the zero-quotient property, and use linear residual updates to accelerate direct integer-root testing. JPEG is conceptual, not a proof.