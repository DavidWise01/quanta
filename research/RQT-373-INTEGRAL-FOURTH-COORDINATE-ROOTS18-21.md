# RQT-373 — A stronger exact ancestor exclusion for roots 18–21

**2026-11-14. Original roots 18–21 remain OPEN.** The executable adds a real arithmetic necessary condition, not another sampled cube iteration.

## The mathematical bottleneck corrected

RQT-369–372 used only the fact that the discriminant in the original rank-four lattice must be a nonnegative square. But **a square discriminant is not sufficient for an integer fourth coordinate**. This matters because the coefficient of the fourth-coordinate square is nonunit modulo 81.

Use the original frozen stoicheion RQT-242 Gram F4 and Wall H4, with the exact unimodular RQT-363 chart U. Set G=U F4 U.T, let t=(a,b,c,d), and require t.T G t=-2.

```text
A = G33 = -5868287405277328266
B = G03*a + G13*b + G23*c
C = G00*a² + G11*b² + G22*c² + 2 G01 ab + 2 G02 ac + 2 G12 bc + 2

A*d² + 2 B*d + C = 0
Delta = B² - A C.
```

The old GMA generation-two test required only `Delta mod81` to be a square residue. The new necessary gate requires the direct integer-coordinate congruence:

```
EXISTS d in {0,...,80}:
    A*d*d + 2*B*d + C == 0 (mod 81).
```

This is a strict improvement whenever A is not invertible modulo81. Here A mod81=48, divisible by3. To implement it efficiently, precompute the exact 6,561 possible (B mod81,C mod81) witness pairs arising from the 81 possible residues of d. A parent failing the pair-membership gate has **no** integer d, regardless of whether its discriminant happens to be a square modulo81.

## Complete cubed-nine generation-two census

Two 9×9×9 generations assign the lowest two balanced base-nine digits of all three free coordinates. The 531441 unique triples `a,b,c∈[-40,40]` thus represent exactly all generation-two ancestors. Every descendant differs in each free coordinate by a multiple of81, so B and C and the full quadratic modulo81 are unchanged. Any rejected parent excludes **all** its subsequent descendants, with no false-negative pruning.

| Result | Parent families |
|---|---:|
| Full two-generation census | 531441 |
| Previously excluded by square discriminant | 124659 |
| **Newly excluded by no integer d modulo81** | **4374** |
| Total certified impossible families | **129033** |
| Unexcluded after both tests | **402408** |

Representative exact counterexample:

```text
(a,b,c)=(-40,-39,-40)
B mod81 = 21
C mod81 = 21
Delta mod81 = 0  (a quadratic residue)
A mod81 = 48
But for every d=0,...,80:
  48*d²+42*d+21 != 0 (mod81).
```

So the earlier test would incorrectly let the entire family survive; the new exact coordinate gate safely excludes it. Other examples are emitted by the program.

## The 27 cubic cores all updated

The executable assigns every one of 531441 ancestors to its authentic first-generation 3×3×3 macrocore (27 cores, each with 27 microcells; 729 microcells per generation). Each core receives 19683 ancestor states and now tracks three separate counts: old discriminant exclusions, new d-coordinate exclusions, and survivors. A deterministic 2000-case independent descendant-congruence test also verifies that changing a,b,c by multiples of81 cannot alter the gate, and cross-checks lookup-table membership by direct enumeration of all 81 possible d residues.

## Genuine four-root block gate

The program optionally accepts `--four-roots-json four.json` containing four integer four-vectors in their proposed order r18, r19, r20, r21. It calculates:
- the exact original-F4 norms of **each** proposed vector (must all equal -2);
- the **six internal** lower Wall pairings `r_j.T H4 r_i` (j>i, must all vanish);
- the accepted first-root parity for r18: 0111,1001, or 1110.

**It does NOT claim a valid extension of the frozen 17-reflection product** because the upstream prefix-factorization witness was not supplied. The old RQT-362 all-17 Wall orthogonality was explicitly corrected by RQT-363, and must not be resurrected.

## Reproduce

```bash
python research/rqt373-exact-fourth-coordinate-gate.py
python research/rqt373-exact-fourth-coordinate-gate.py --four-roots-json four.json
```

Local independent execution generated:
- `/mnt/data/rqt373_integral_fourth_coordinate.py`
- `/mnt/data/rqt373_results.json`

The self-contained GitHub version prints exact per-core totals and examples, and asserts all three global census counts.

## Next natural target — RQT-374

Use the stronger fourth-coordinate congruence at deeper cubic-generation levels only on selected certified ancestor families. Unlike the pure 3-adic discriminant unit-square check, integer-coordinate divisibility can keep pruning a family. More importantly, continue a global exact integral norm-representation solver for the original F4; **root18–21 require actual four integer vectors and the authentic frozen-prefix verification**.

**No original root18, root19, root20, or root21 has been found.**
