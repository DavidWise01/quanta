# RQT-585 — Five Pell Coefficients

**Verified exact arithmetic, based on archived RQT-575/583/584 inputs:** 68 remaining ray-offset discriminant families have exactly **five distinct A coefficients**, each shared within a cone ray.

For Δ(t)=At²+Bt+C and D=B²−4AC, extract an exact square factor s² of A and let a=A/s², Z=2sY. Then the Pell necessary equation is **X²−aZ²=D**, with X=2At+B. Recovering an original integer candidate also requires **X≡B (mod 2A)**, **Z divisible by 2s**, and the eliminated Gram-coordinate integrality check.

| Ray | Open families | s |
|---|---:|---:|
| (35,−10,14) | 9 | 4 |
| (45,−13,18) | 22 | 5 |
| (80,−23,32) | 17 | 1 |
| (95,−27,38) | 12 | 7 |
| (115,−33,46) | 8 | 1 |

**New negative-scale exact search:** all t from −20000 through −1 for each of the 68 families: **1,360,000** scales tested, **1,357,537** nonnegative discriminants, **zero perfect square discriminants** and **zero norm−2 integer vectors**. Polynomial identities and reduced Pell equivalences tested exactly at multiple signed scales. Finite nonfinding only, not a global obstruction.

**Selected-family ledger unchanged:** 67/135 previously excluded at all scales, 68 unresolved. Original 22D Wall replay NOT RUN, Root 19 OPEN. The triple nested {{i}} breathing architecture is preserved as notation; no physical equivalence or root-generating action established.

**Next RQT-586:** choose one of the 68 generalized Pell equations, compute exact primitive congruence/orbit constraints, and recover a candidate only after both Pell and fourth-coordinate integrality hold.

Local conversation artifacts: full exact rqt585.py, JSON results, high-resolution brutalist neon JPEG, and standalone HTML embedding the JPEG. GitHub text viewer only; Pages and JPEG repo publishing unverified.
