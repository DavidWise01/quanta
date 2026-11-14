# RQT-378 — The Cofactor Key: Exact two-sign formula for root 21

**2026-11-14 | Frozen original F4/H4 verified | Original roots 18–21 still OPEN.**

## The story

The GMA remains `{{9×9×9}}^9`, nine nested cubic generations with 729 microcells per generation, 27 spatial cores and the `||||` singlet. RQT-377 established a saturated Wall-kernel descent: once an authentic root 18 exists, root19 is a rank3 search, root20 a rank2 search and root21 a rank1 search. RQT-378 now makes that *last step explicit*, requiring no integer lattice enumeration for root21.

## Exact signed-cofactor theorem

Let `R3=[r18 r19 r20]` be a 4×3 integer matrix of **three genuine, independent** norm-minus-two roots with their three internal lower Wall conditions zero. Use the authentic frozen Wall matrix H4:
```text
r_j.T * H4 * r_i = 0  for 18<=i<j<=20
r_i.T * F4 * r_i = -2.
C = R3.T * H4.T     (3×4).
```

Every integer fourth root r21 must solve `C*r21=0`. For j=0,1,2,3, define the signed cofactor

```text
v_j = (-1)^j det(C with column j deleted).
```

Then `C*v=0` exactly. As H4 is unimodular, the signed cofactor vector of C is primitive if and only if the primitive rank-three prefix R3 has gcd of its 3×3 minors 1. The RQT-376 theorem proves that any completed four-root Wall flag must be unimodular; therefore the three-root prefix must be primitive.

Consequently **if the first three roots really extend to a four-root flag**, the only possible fourth vectors are `r21=+v` and `r21=-v`. Test both exact norms and the final integer determinant:
```text
r21.T*F4*r21 == -2
abs(det([r18 r19 r20 r21])) == 1.
```
This cofactor formula is exact integer arithmetic, not a rational nullspace heuristic. If either test fails, that three-root prefix cannot complete to an authentic four-root flag. If they pass, the four-root block's norm and internal Wall flag conditions are satisfied; authentic frozen predecessor-factorization/order verification is still required before declaring roots18–21 complete.

## Executed tests and limitations

The executable `research/rqt378-root21-signed-cofactor-closure.py` embeds frozen stoicheion RQT-242 F4 and H4 and verifies H4+H4.T=-F4, det(H4)=1 and det(F4) exactly.

- **Synthetic positive control (NOT an original F4 root):** H=I4, F=-2I4 and first three standard basis vectors yield signed-cofactor `v=(0,0,0,-1)`, so the two candidates are ±e4. Both have norm -2 and produce determinant ±1.
- **Synthetic negative control:** a first candidate `(2,0,0,0)` has norm -8, correctly rejected.
- **Original F4/H4 kernel identity control:** arbitrary first three standard basis columns, explicitly not asserted to be authentic roots, produce a primitive signed-cofactor vector annihilated by their exact original Wall constraint matrix.

All executable checks passed. No real integral original r18, r19, r20 was supplied, so root21 is **conditional**, not instantiated. The 17-reflection frozen predecessor product is unverified.

Run:
```bash
python research/rqt378-root21-signed-cofactor-closure.py
python research/rqt378-root21-signed-cofactor-closure.py --three-roots-json proposed_18_to_20.json
```

Local independently run source: `/mnt/data/rqt378_cofactor_closure.py`. Local execution JSON: `/mnt/data/rqt378_results.json`.

## Story JPG: The Cofactor Key

A new chapter JPG `RQT-378-The-Cofactor-Key.jpg` is delivered in the conversation. The artwork depicts orange, teal and blue root gates generating three Wall planes, their intersection as a purple integral line, and the two exact ± cofactor endpoints. It is **conceptual mathematical storytelling** and not a plotted authentic root witness. The JPG is a separate conversation artifact, not yet uploaded to GitHub; this markdown and executable **are** committed to GitHub.

## Next target RQT-379

Prioritize actual root18 construction from original F4, then use saturated integer kernels to seek roots19 and 20. The last root21 can now be **computed directly from signed 3×3 minors** once the first three authentic roots are found. Preserve all 27 GMA cores for addressed search, original evidence provenance, and a distinct JPG chapter each turn.

**Original roots18–21 remain OPEN.**
