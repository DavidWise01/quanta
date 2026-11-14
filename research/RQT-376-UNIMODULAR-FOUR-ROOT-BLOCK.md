# RQT-376 — Four-root Wall flags must be unimodular

**Date:** 2026-11-14. **Exact theorem verified on the authentic frozen F4/H4. Roots 18–21 remain OPEN.** This turn also produces the requested JPG visualization at local artifact `/mnt/data/RQT-376-cubic-GMA-visual.jpg`.

## The useful exact upgrade

The preceding cubic GMA audits tested necessary modular conditions for `r.T F4 r=-2`, but did not produce original integer vectors. This turn isolates an **exact global algebraic requirement** on the proposed four-root completion.

Let the candidate roots be the columns of an integer 4×4 matrix `R=[r18 r19 r20 r21]`. The original frozen Wall matrix H4 is integral, `det(H4)=1`, and `H4+H4.T=-F4`.

Assume
1. Every `r_j.T F4 r_j=-2`.
2. The **six internal Wall pairings** `r_j.T H4 r_i=0` for every `18<=i<j<=21`.

For each column, because `H4+H4.T=-F4`:
```text
2*(r_j.T H4 r_j) = -(r_j.T F4 r_j) = 2,
so r_j.T H4 r_j = 1.
```

Therefore `W=R.T H4 R` is *upper triangular*, with diagonal exactly `(1,1,1,1)`, so `det(W)=1`. But `det(W)=det(R)^2*det(H4)=det(R)^2`. Thus

```
                    det(R) = +1 or -1.
```

This is a **global necessary consequence** of the exact norm and Wall equations, no local congruence, sample search, or bounding radius involved.

## Early rejection for each partial block

Every first k columns of a unimodular integer matrix (k=1,2,3,4) generate a primitive direct-summand sublattice. Accordingly the gcd of **all k×k minors** of the 4×k matrix must equal 1. This supplies an exact early filter:

```text
root18:             gcd of its 4 entries = 1
roots18-19:         gcd of 6 two-by-two minors = 1
roots18-20:         gcd of 4 three-by-three minors = 1
roots18-21:         |det([r18 r19 r20 r21])| = 1
```

This condition alone is not sufficient for norm/Wall/factorization validity. The six Wall pairings remain mandatory. The original frozen 17-reflection predecessor factorization/order must still be independently verified when authentic root candidates are found.

## Reproducible executable and synthetic controls

`research/rqt376-four-root-unimodular-flag.py` embeds authentic RQT-242 F4/H4 and asserts the original Gram determinant, H4 unimodularity, and `H4+H4.T=-F4`. It accepts `--candidate-json` with an ordered list of 1–4 original four-coordinate integer root candidates. It checks F4 norms, internal H4 lower pairings, successive maximal-minor gcds, and for full four-block the exact determinant theorem.

A separately identified **synthetic** positive control `H=I4, F=-2 I4, R=I4` passes all four norm equations, six pairings and determinant 1; a synthetic vector `(2,0,0,0)` fails both the norm and primitive-prefix tests. These prove that the verifier's logic is executable; they are **not** original F4 roots.

Local independent executed source:
`/mnt/data/rqt376_unimodular_block.py`, exact results:
`/mnt/data/rqt376_result.json`.

## The cubic geometry remains intact

The 27 spatial cores and their `9×9×9` microcells remain the indexing lattice for nine nested generations around central `||||`. They are not substituted for F4/H4, and a conceptual picture does not claim that visually highlighted cells are exact individual coordinate witnesses.

**JPG this turn:** `/mnt/data/RQT-376-cubic-GMA-visual.jpg`. The generated infographic is an illustrative visualization; RQT-369–375 audit counts are drawn from different cohorts, not additive totals. The central singlet is the box `||||`.

## Next natural target — RQT-377

Use the primitive-minor gcd test as an early filter in a constructive search for four integer vectors. A candidate first root must have exact norm -2 and accepted parity. A candidate second root must also be H-orthogonal to root18 and form a primitive rank-two sublattice; the third similarly forms a primitive rank-three sublattice; the fourth closes a unimodular rank-four Wall flag. Then verify original 17-root prefix product and rank/order without assuming unsupported orthogonality to every predecessor.

**Status: No authentic original root 18, 19, 20 or 21 has been recovered.**
