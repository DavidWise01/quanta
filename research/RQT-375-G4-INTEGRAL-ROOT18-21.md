# RQT-375 — Generation-four integer-coordinate obstruction, roots18–21

**Date 2026-11-14. Status: exact local scan PASS; no original roots18–21 constructed.** This continues the genuine `{{9×9×9}}^9` GMA architecture around singlet `||||`, retaining 27 cubic spatial cores, 729 microcells per generation, and exact frozen RQT-242 F4.

## Stronger exact fourth-coordinate gate at modulus 6561

For the original even integral Gram F4 and the unimodular RQT-363 chart U, set `G=U F4 U.T`. For `t=(a,b,c,d)`, the exact norm minus-two equation is:

```text
A d² + 2B d + C = 0,
A = G33 = -5868287405277328266,
B = G03*a + G13*b + G23*c,
C = 2 + sum_{i,j<3} Gij*t_i*t_j,
Delta = B² - A*C.
```

A square discriminant modulo 9^4=6561 remains only necessary. The stronger integer-coordinate condition requires **an actual residue d modulo 6561** satisfying this quadratic.

For each selected generation-three parent, compute every integer solution `d0 modulo729`. Any residue `d modulo6561` reduces to `d0` and is therefore of the form `d=d0+729j`, j∈0..8. The exact lifting identity is

```text
f(d0+729j) = f(d0) + 729*j*(2*A*d0+2*B)
              + (729*j)^2*A
              (mod 6561),
```
where the last term vanishes modulo6561. Consequently a fourth-coordinate lift exists iff for some d0 and j:

```text
j*(2*A*d0+2*B) == -(f(d0)/729) (mod 9).
```

This is a complete and finite test; it avoids treating a modular-square discriminant as an integer-coordinate witness.

## Executed local results

Using 81 g2 parent records (three in each of the 27 macrocores) from the recorded original RQT-371 chain, select the first actual g3 descendant with a fourth-coordinate solution modulo729. For each selected g3 parent, **exhaust all 729 generation-four child microcells**. Each descendant has the same a,b,c modulo6561 as its g4 ancestor, so exclusion applies to the *entire deeper subtree*.

| Result for the 59,049 selected g4 children | Count |
|---|---:|
| Non-square Delta modulo6561 | 486 |
| Delta square, but no integer fourth coordinate modulo6561 | **81** |
| Survives both necessary gates | **58,482** |
| Total | **59,049** |

A concrete extra obstruction (from the `FCC` core):
```text
g3 = (-361, -360, -349)
g4 = (-3277, -3276, 1838)
B mod6561 = 1764
C mod6561 = 6507
Delta mod6561 = 0  (a square)
BUT no d mod6561 solves A*d²+2*B*d+C=0.
```

**Independent direct verification:** all 81 newly excluded g4 children were replayed by exhaustively testing `d=0,...,6560` against the exact congruence. No d solution was found in any one of those 81 checks. This is a stronger check than simply trusting the Hensel-lift code. The full local result is archived as `/mnt/data/rqt375_g4_results.json` and the executed self-contained local engine is `/mnt/data/rqt375_g4_integral.py`. Its 27 SHA-256-linked core packets have chain tip:

```text
adf9bf52e1b5992049e85efa16b7b2a7024d546ef39d5aa01bffbf0332419f62
```

The separately committed GitHub executable reconstructs the cubic parent-selection ordering directly from frozen F4, without requiring the local RQT-371 JSONL file. Its parent-picking algorithm is reimplemented and may result in different per-core packets/hashes if the earlier square-only parent-preference rules choose different parents; do not conflate its hash with the local executed hash. Both variants enforce the same exact mathematical gate. The local numerical results above specifically refer to the locally executed scan over recorded RQT-371 parent vectors.

## No overstatement of results

These 59,049 children are **not** the entire fourth-generation space. The result is an exact exclusion only for the selected 81 parent lineages; no exact global norm-minus-two vector has been produced, and root18–21 remain OPEN. The original frozen 17-root prefix and six internal Wall pairing equations remain acceptance requirements for the proposed four-root completion; never assume all-17 H-orthogonality without proof.

The next meaningful RQT-376 task is a **constructive integral representation algorithm** producing explicit r18 and then a four-root block, not simply adding additional generations of cubic routing. Keep `F4/H4` fixed and prove every candidate's original norm and genuine reflection-prefix compatibility.
