# RQT-374 — Exact modulo-729 integer-coordinate gate for roots 18–21

**2026-11-14. Root18, root19, root20, root21 remain OPEN.** RQT-374 extends RQT-373 from the exhaustive two-generation `mod81` audit to a **selected, fully enumerated generation-three descendant audit modulo 729**, preserving the user's volumetric `{{9×9×9}}^9` around `||||`.

## Genuine original lattice

Use the authentic frozen even integral F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, original Wall H4, and the exact unimodular RQT-363 basis U. A proposed integer root has `r=U.T*(a,b,c,d)`, `r.T F4 r=-2`, permitted first-root parity among `0111,1001,1110`, and ultimately requires authentic frozen predecessor factorization/order verification.

Let `G=U F4 U.T`, `A=G33`, `B=G03*a+G13*b+G23*c`, and `C=2+sum_{i,j<3} Gi,j * t_i*t_j`. The exact root norm requires:

```text
A*d² + 2*B*d + C = 0.
Delta = B² - A*C.
```

RQT-373 showed that a square Delta modulo 81 need not admit an integer fourth coordinate. Here the stronger test at *the next cubic generation* is
```text
exists integer d modulo 729:
  A*d² + 2*B*d + C = 0 (mod 729)
```
rather than only `Delta` a square mod729.

## Proven descendant pruning

Each generation of the cubic GMA assigns one balanced base-nine digit to each of a,b,c. After generation 3, any future descendants have coordinates congruent modulo `9³=729`, so their B, C, and Delta agree modulo729. If the direct fourth-coordinate congruence has no solution, **no descendant can produce an integer norm-minus-two root**, regardless of what occurs at later generations.

The executable reconstructs the 81 RQT-371 selected generation-two parent witnesses (three per each of 27 macrocores), then examines **all 729 third-generation child cells** of each parent:

| Status | Generation-three branches |
|---|---:|
| Exhaustively checked within 81 selected families | 59049 |
| Delta nonsquare modulo729 | 2916 |
| **Delta square, but no integer d modulo729** | **486** |
| Remaining necessary-condition survivors | **55647** |
| Total certified impossible branches | **3402** |

The 486 additional exclusions occur in exactly six spatial cores, **FCC, FCL, FDL, FUR, RCC, RCL**, with **81 new exclusions per core**. These are new beyond the pure square-discriminant gate at that level and apply to all descendants of those particular child nodes.

A concrete exact obstruction:
```text
(a,b,c) = (-364,-350,-356)
B mod729 = 81
C mod729 = 243
Delta mod729 = 0 (square)
But there is no d in 0..728 with
 A*d*d + 2*81*d + 243 = 0 (mod729).
```

The executable explicitly checks that incrementing every selected child coordinate by a multiple of729 preserves its B,C congruence, and asserts the global split and the 27 per-core packet counts.

## Scope and independence

The 81 initial parent families were selected by RQT-371 from a larger population, not exhaustively. Accordingly these exact 59049 child checks are complete **within those 81 families only**; they do not establish that all excluded branches in the global generation-three search have been counted.

This is an exact necessary local gate, not a constructed integral vector. The initial four roots remain OPEN, including root18. All computations share one authentic original stoicheion F4 provenance; independent arithmetic checks are not independent original-source ancestries.

## Reproduction

```bash
python research/rqt374-g3-integral-fourth-coordinate.py
```
The GitHub program is self-contained, regenerates its 81 parent witnesses using the RQT-371 exact selection algorithm, computes the direct modulo729 fourth-coordinate solution table and per-core proof packets, and asserts all totals.

An independent local computation using the frozen RQT-371 JSONL parent witnesses also obtained:
```json
{"survived":55647,"square_excluded":2916,"new_integral_excluded":486}
```

## Next natural target — RQT-375

The result demonstrates that integer-coordinate divisibility can prune some branches even when their discriminants are squares. Carry this direct coordinate gate to modulo `9^4=6561` for carefully selected survivors and, more importantly, run a **constructive indefinite norm-representation algorithm** alongside it to produce actual integer `r`, then search for four jointly valid roots with six internal Wall pairings and prefix-factorization verification. Do not declare roots18–21 on local witnesses alone.
