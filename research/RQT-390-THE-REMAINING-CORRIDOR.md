# RQT-390 — The Remaining Corridor: all three coordinate planes excluded

**2026-11-15 · Exact original F4 congruence PASS · Root19 remains OPEN.**

## Three-dimensional visual story

This turn's story image **RQT-390-The-Remaining-Corridor-3D.jpg** is rendered as a **true 3D perspective**: a 9×9×9 volumetric GMA cube around `||||`, with three coordinate sheets crossing at the center and vanishing from the available root19 search. The neon chrome Root18 portal remains open at the first stage; root19 is locked, and roots20–21 remain pending. The JPG is delivered separately in the conversation, and a self-contained 3D-style HTML/SVG story is committed to the repository. The JPG itself is not yet a GitHub binary asset. The geometry is explanatory, not the original integer coordinate values.

## Original exact successor lattice

RQT-386 recovered an original F4 integer norm−2 root candidate, RQT-387 verified its correct initial rank/order reduction, RQT-388 produced the exact **saturated integer rank-three Wall kernel**, and RQT-389 globally excluded the planes `x=0` and `y=0` in that fixed reduced basis.

Let `B∈Z^(4×3)` be that RQT-388 reduced saturated basis. Its Gram is the authentic

```text
Q = B.T F4 B.
r19 = B*(x,y,z)
r19.T F4 r19 = -2
r19.T H4 r18 = 0.
```

Since the lattice is even, `q(x,y,z)=(x,y,z).T Q (x,y,z)/2` is integer-valued, and root19 requires `q=-1`. In that exact reduced basis, independently verified against the frozen original F4, the full `Q mod16` is:

```text
[ 2  8  2 ]
[ 8  4  6 ]
[ 2  6 14 ]
```

## The final hyperplane, z=0, is globally impossible

On `z=0` the exact half-form reduces modulo 8 to

```text
q(x,y,0) ≡ x² + 2y² (mod 8).
```

The quadratic residues modulo8 are `{0,1,4}`. Exhaustive enumeration of all **64 residue pairs** `(x,y) mod8` gives the attainable half-norm values

```text
{0,1,2,3,4,6}
```

and, crucially, **never 7**. But the target `q=-1` requires `q ≡ 7 mod8`. Hence no integers x,y, of **any** size, can satisfy the root19 norm equation on `z=0`.

The executable independently maps each of the 64 residue pairs through the reduced integral basis B back into the original four coordinates, evaluates `r.T F4 r mod16`, and confirms that none equals `-2 mod16`. This is **an exact, unbounded obstruction**, unlike RQT-388's bounded coefficient search.

## Combined RQT-389 + RQT-390 global conclusion

- RQT-389: `x=0` is excluded globally by binary Gauss minimum.
- RQT-389: `y=0` is excluded globally by binary Gauss minimum.
- RQT-390: `z=0` is excluded globally by the simpler exact modulo8 half-form residue test.

Therefore every genuine successor root19 in the **fixed RQT-388 reduced lattice basis** must satisfy

```text
x != 0 and y != 0 and z != 0.
```

This is a **global necessary condition**, not proof that no root19 exists in the full ternary lattice. These conditions depend on the fixed unimodular choice of reduced basis, although the exclusion of the corresponding sublattices is exact.

## Additional new parity gate

Auditing all `8³=512` coefficient triples modulo8, exactly **96** satisfy the full norm equation modulo16. They occupy only three coefficient parity classes:

```text
001 : 32 triples
011 : 32 triples
110 : 32 triples
```

Thus, in this reduced basis, a candidate root19 must lie in one of these three parity classes, and every coefficient must be **nonzero as an integer**. These necessary constraints can be passed to the RQT-391 constructive ternary solver.

## Reproducible arithmetic and provenance

Run:

```bash
python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
python research/rqt390-remaining-corridor.py /tmp/rqt388.json
```

The RQT-390 executable embeds frozen F4/H4 and verifies the RQT-388 reduced basis and Gram from exact machine-readable numbers. The local executed equivalent `/mnt/data/rqt390_remaining_corridor.py` produced the exact JSON certificate `/mnt/data/RQT-390-exact-certificate.json`.

Git files:
- `research/rqt390-remaining-corridor.py`
- `research/RQT-390-corridor-certificate.json`
- `research/RQT-390-THE-REMAINING-CORRIDOR.md`
- `rqt390.html` (interactive 3D-feel CSS/SVG illustrated chapter; independent of the binary JPG).

## Next: RQT-391 — The Interior Search

The true remaining rank-three search lies in integer triples with **all x,y,z nonzero**, one of the three mod2 patterns `001,011,110`, and exact indefinite norm `z.T Q z=-2`. A useful constructive next step is to search for integral points through a ternary indefinite norm algorithm or two-variable Pell-type slices **with z nonzero**; a local congruence is never an acceptable substitute for an exact original (F4) vector. Upon a valid root19, descend to rank2 for root20 and force root21 by the earlier cofactor theorem.

**Root18: first-stage accepted. Root19 OPEN. Root20 OPEN. Root21 conditional. Complete 21-reflection factorization OPEN.**
