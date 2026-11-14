# RQT-363 — Direct full-lattice root18 cylinder and prefix-gate correction

**Status: exact original-lattice bounded search PASS, NO root found.** Frozen genuine F4/H4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. Roots18–21 remain OPEN.

## Change of search strategy

Previous RQT-351 through RQT-361 targeted ternary isotropic conics and norm equations. This turn searches for an **actual norm-minus-two root directly in all four original lattice dimensions**, using an exact unimodular basis that was discovered using positive-definite majorant/LLL and **verified without approximation**:

```
U =
[[ 224,  29, -224, -130],
 [-193, -25,  193,  112],
 [  40,   5,  -40,  -23],
 [-336, -43,  335,  195]]
```

The verifier asserts `abs(det(U))=1`. For any integer `t=(a,b,c,d)`, the original integer vector is `r=U.T*t`, and its norm is `r.T*F4*r=t.T*G*t` with `G=U*F4*U.T`. Unimodularity guarantees no integer vectors are lost globally by the coordinate change.

## Exact complete three-coordinate cylinder

Fix `a,b,c∈[-60,60]` and solve **without any bound on d**:

```
A*d²+B*d+C = 0
A = G[3,3]
B = 2*(G[0,3]*a + G[1,3]*b + G[2,3]*c)
C = G[0,0]*a² + G[1,1]*b² + G[2,2]*c²
  + 2*(G[0,1]*a*b + G[0,2]*a*c + G[1,2]*b*c) + 2
```

The constant +2 encodes `r.T*F4*r=-2`. Compute exact integer discriminant `disc=B²-4*A*C`. If negative, no integer d; if nonnegative, require an **integer perfect square**, and then require exact divisibility of `(-B±sqrt(disc))/(2A)`. This is exhaustive within the specified cylinder, even when d is arbitrarily large.

Executed results:
```text
tested (a,b,c) integer triples: 1,771,561 = 121³
nonnegative discriminants:       81,167
perfect-square discriminants:    0
integer norm-minus-two vectors:  0
```

Therefore any genuine norm-minus-two root in the authentic F4 satisfies
```
max(|a|,|b|,|c|) >= 61
```
in this exact unimodular basis U, **regardless of d**. This is a finite coordinate bound and does NOT establish global nonexistence.

## Critical RQT-362 corrective note

RQT-362's conditional extractor included an optional `r18.T*H4*r_i=0` test against **all 17 older roots** and treated it as the mandatory prefix-extension gate. That was **not established by RQT-257** and is too restrictive to assume. The six original RQT-257 Wall constraints refer to pairwise relations **within the proposed four-root block** `r18,r19,r20,r21`: `r_j.T*H4*r_i=0` for 18<=i<j<=21. Matching the frozen 17-root prefix requires checking the actual specified product/factorization and successor rank/order, not asserting 17 undocumented orthogonalities.

Thus treat RQT-362's 17-prefix orthogonality feature as an optional exploratory diagnostic **ONLY**, not as a condition of being root18. This append-only note corrects the earlier claim. A norm-minus-two vector alone is also not yet a verified root18 extension of the frozen factorization.

## Reproduction and status

Run `python research/rqt363-full-lattice-root-cylinder.py` (SymPy). Exact arithmetic checks the frozen determinant, the Wall relation `H4+H4.T=-F4`, H4 unimodularity, U unimodularity, and every discriminant; no approximate norm is used. Locally executed files: `/mnt/data/rqt363_root18_cylinder.py` and `/mnt/data/rqt363_root18_cylinder_results.json`. Local majorant probe: `/mnt/data/rqt363_adaptive_majorant.py` (discovery only; a standalone proof does not rely on it).

## Next natural target RQT-364

Try an arithmetic indefinite-lattice norm-representation algorithm at larger effective scale, not an endless height increment. If an exact norm-minus-two r appears, test primitive content, accepted parity, exact integral reflection `R=I+r(r.T*F4)`, rank/order after composition with frozen matrix X4, and the **six internal Wall pairings** if attempting the four-root completion. Keep original roots18–21 OPEN until exact evidence exists.

Three witness directions (arithmetical norm, Wall compatibility, source ancestry) remain distinct; original stoicheion F4 is one provenance source. The 3×3×3 cubit and time-angle semantics remain indexing, not proof.
