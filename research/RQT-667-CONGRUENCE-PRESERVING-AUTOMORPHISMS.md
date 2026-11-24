# RQT-667 — Congruence-Preserving Pell Automorphisms

## Mathematical result

For the archived integral quadratic

\[G(u,t)=r_0u^2+r_1ut+r_2t^2+r_3u+r_4t+r_5=0,\]

put \(a=r_1^2-4r_0r_2>0\), \(h=r_1r_3-2r_0r_4\), \(c=r_3^2-4r_0r_5\), \(D=|2r_0|\), and \(M=aD\). Any integer solution corresponds to \(z=at+h\), \(y=\pm(2r_0u+r_1t+r_3)\), and \(z^2-ay^2=N=h^2-ac\).

**Sufficient subgroup theorem:** If \(U^2-aV^2=1\), \(U\equiv1\pmod M\), and \(V\equiv0\pmod M\), the recurrence
\[z'=Uz+aVy, \qquad y'=Vz+Uy\]
retains the generalized Pell norm and recovers a legitimate integral pair \((u',t')\) from any existing original integer solution. Indeed,
\[t'=Ut+Vy+\frac{(U-1)h}{a},\]
so \(t'-t\equiv0\pmod D\); similarly \(y'-y\equiv0\pmod D\). Thus \(y'\equiv\pm(r_1t'+r_3)\pmod D\). The reconstructed \(u'\) is integral and satisfies the original quadratic exactly.

This is **sufficient, not minimal or necessary**. If any norm-one Pell unit exists, some positive power meets these congruences because its integral determinant-one recurrence matrix has finite order modulo \(M\). This observation does not construct a unit or a starting integer seed.

## Exact verification

- Source: RQT-619 original 27-equation certificate, SHA256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- All 27 canonical charts validated: original discriminant identity; \(D,M\) integers and the subgroup sufficient algebraic conditions.
- Synthetic integer test \(u^2-2t^2=1\): \(a=8,D=2,M=16\). The 16th power of unit \((3,1)\) meets the congruence gate and maps original \((u,t)=(1,0)\) to a nontrivial solution, directly verified in the original equation.
- No nontrivial norm-one unit or original integer seed is asserted for any of the 27 unresolved real charts.
- Exact Python verifier: `research/rqt667.py`.
- Exact JSON certificate SHA256: `92bc91bf892d666530d37a63579aa0d4829d472502d7e546a5a45f77f38dc512`.

## Status

82/135 selected families excluded at all scales (60.74%); 53 unresolved in 27 canonical sign-orbits. **Root 19 remains OPEN**. Original 22D Wall NOT REPLAYED. No new exclusion. Sources have shared ancestry, not independent corroboration.

## RQT-668 natural bound

Determine whether a **smaller exact congruence subgroup** is sufficient for each chart and compute the finite modular action without assuming a verified Pell unit. If a genuine unit and seed are later identified, apply the subgroup gate and verify the original integer equation before claiming a root.

`{{i}} · .dlw`