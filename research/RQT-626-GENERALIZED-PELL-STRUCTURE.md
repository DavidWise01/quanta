# RQT-626 — Five-Coefficient Generalized Pell Reduction

## Exact structural result

Independent integer-only replay of the **RQT-625** 27 canonical discriminants found that each discriminant coefficient triple (A,B,C) has **gcd exactly 4**. Writing

`Delta(t)=4(a*t^2 + 2*h*t + c)`

is always possible: a=A/4, h=B/8 and c=C/4 are integers, and **a is positive and nonsquare** in all 27 cases.

Put `z=a*t+h` and `N=h*h-a*c`. Then, identically for all integers t,

`z^2 - a*(a*t*t+2*h*t+c) = N`.

Thus Delta(t) is a nonnegative integer perfect square if and only if there are integers (z,y) with
- `z^2-a*y^2=N`;
- `z ≡ h (mod a)`;
- `t=(z-h)/a` integral.

In the converse, Delta(t)=(2y)^2. To recover an actual integer norm−2 vector one **must additionally check** the original quadratic root u is integral and satisfies Q(u,t)=0. The generalized Pell equation by itself does not establish that.

## The five coefficients

- **9** orbits (28,29,30,31,33,34,35,36,37): `a=89518360633605555683821304281344825`.
- **8** orbits (55,56,57,61,62,64,65,67): `a=865181362726903603566834179921037649`.
- **4** orbits (0,1,2,7): `a=158134758925461363207454619257200752`.
- **3** orbits (81,89,92): `a=149561530769640628300862186866588569`.
- **3** orbits (109,110,112): `a=1957113882671124377864756294075131977`.

All 27 pairs (a,N) are distinct, so five shared leading coefficients do **not** mean only five generalized Pell equations remain.

## Evidence and limits

- Source RQT-625 SHA256: `201bbc5dfde380016884c775ff1c390a69196303fce3a8199219de739c6ace69`.
- Complete local `RQT-626-results.json` SHA256: `1d901288a9a6007f79496615ef421bd0c6aa147aab1ecc33355e5ef71d4c1052`.
- Reproducer: `research/rqt626-pell-structure.py`.

**No new exclusion, no integer norm−2 seed and no original 22D Wall replay.** Selected family ledger stays **82/135 excluded at all scales (60.74%), 53 unresolved**, represented by 27 canonical orbits. Selected corridors do not exhaust the full lattice. **Root 19 OPEN.**

## Next natural bound — RQT-627

Group generalized Pell orbit calculations by the five leading coefficients while treating the 27 distinct targets N independently. Seek compact certified Pell seed or all-scale obstruction with the `z≡h mod a` and original integer-coordinate gates preserved. Do not confuse a shared number field or large finite search with an existence theorem.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
