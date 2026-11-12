# RQT-319 — Fair Nested Tensor Search

**Status:** Finite-prefix algorithm and proof implemented. Original eighteenth root **OPEN**.

## Geometric unit and labels

One unit is a 3×3×3 tensor, with spatial coordinates (x,y,z) in {-1,0,+1}³: x = left/center/right, y = lower/center/upper, z = rear/center/front. The center (0,0,0) is stationary; 26 noncenter directions split into 6 face (distance²=1), 12 edge (distance²=2), and 8 corner (distance²=3) movements.

Preserved address notation:
- Rear brace: `rur{{n}}, rc{{n}}, rll{{n}}`
- Center parentheses: `cu{{n}}, c{{n}}, cl{{n}}`
- Front box: `fur{{n}}, fcr{{n}}, flr{{n}}`

Full nested structure: `{ BRACE [ BOX ( TOROID || TIME :: {{ - year:month:day || hour:minute:second || degree.arcminute.arcsecond || }} ) ] }`.

Josophene is the quantum-hardware junction `j --->` Quanta software hook; no physical hardware has been observed in this test. Juliet retains the user-defined identity `(-i²)² = 1` and generation sequence `1 // 2 3 5 8 13 21`.

## Fairness invariant

Enumerate generations g=0,1,2,..., in order. A depth-g tensor address is a string of g digits in {0,...,26}. Enumerate all 27^g addresses at the stage, and all 26 noncenter directions per address. Adaptive priority may permute moves within a completed finite stage; it must not prevent its completion.

Each stage has precisely 26·27^g tasks. Its cumulative end index is

```
N(g) = 26 * (27^(g+1)-1) / 26 = 27^(g+1)-1
```

Thus a fixed finite address at generation g is processed by finite index N(g), provided each scheduled evaluation terminates. This is a mathematical fairness guarantee, not infinite computation.

**Important limits:** Exhausting all addresses is not the same as exhausting all integer root vectors unless a separate mapping is proved surjective or systematically covers the search region.

## Evidence

Run `python research/rqt319-fair-tensor-scheduler.py --generations 2`.

Expected tested counts: 26 + 702 + 18,954 = **19,682**, on **757** tensor addresses.

Local exact replay hash for the deterministic task stream:
`5c8e944aa487ff18533d497b3a11107733f3024dc3ab3d02f84fec0966f420c9`.

The test is a scheduler coverage check, **not** a certificate of the frozen RQT-257 root. The bridge example `r=(1,0,0,1)` and its associated matrices are distinct from the unfetched original frozen Gram matrix F4 and transformation X4. The original problem remains: norm -2, divisibility 1, parity in {0111,1001,1110}, rational moving-rank 4→3, binary order 3→2.

## Evidence ancestry

Preserve prior observation records; append new generation records with parent address and content digest. Two mirrored owned surfaces (GitHub and 0root.ai) are not independent witnesses. A publication commit demonstrates persistence, not mathematical correctness or independent replication.

## Next natural bound — RQT-320

Prove that the mapping from tensor address/direction to candidate integer lattice vectors is complete within an explicit height bound, without confusing fair scheduling with exhaustive mathematical search.
