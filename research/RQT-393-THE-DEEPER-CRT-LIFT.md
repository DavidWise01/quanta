# RQT-393 — The Global Key: Deeper CRT Lift

**2026-11-15 · Exact original F4 prime-power arithmetic PASS · Root 19 remains OPEN.**

## Purpose

RQT-386 found an explicit integer norm−2 reflection in the original frozen F4, RQT-387 verified its first-stage moving-rank and mod2 operator-order reduction, RQT-388 constructed the saturated root19 Wall kernel and reduced its basis, RQT-389–390 excluded all three reduced-coordinate hyperplanes, RQT-391 certified a finite exact radius-10000 two-coordinate cylinder exclusion, and RQT-392 proved that only 1/50 of coefficient classes modulo240 satisfy the original rank-three norm congruence.

This turn strengthens the *local* sieve through exact prime-power lifts, using the **same** rank-three kernel B and **same frozen** F4. It does **not** claim to have found root19.

## Authentic equation

Let `r19=B z`, `z=(x,y,z3)∈Z³`, and `Q=B.T F4 B`. The required exact conditions remain:

```
z.T Q z = -2
r19.T H4 r18 = 0.
```

The saturated kernel guarantees the Wall pairing for every Bz. Only vectors with **exact original norm −2** may be accepted. The congruence `z.T Q z = -2 mod m` is necessary but not sufficient.

## Deepened prime-power tests

The self-contained `research/rqt393-deeper-crt-lift.py` reconstructs original F4/H4 and Q from the JSON output of `research/rqt388-exact-second-key.py`, verifies `Q=B.T F4 B`, and exhaustively enumerates triples in each listed residue ring:

| Modulus | Exact admissible triples | Total | Density |
|---|---:|---:|---:|
| 16 | 768 | 4096 | 3/16 |
| **64** | **12288** | **262144** | **3/64** |
| 3 | 18 | 27 | 2/3 |
| **27** | **1458** | **19683** | **2/27** |
| 5 | 20 | 125 | 4/25 |
| **25** | **500** | **15625** | **4/125** |

Modulo64, all surviving triples lie in **exactly three** coefficient-parity classes `001,011,110`, each with 4096 representatives. The 64,27,25 moduli are pairwise coprime, so the Chinese remainder theorem makes the combined count an **exact multiplication**:

```
M = 64 * 27 * 25 = 43200
all coefficient classes = 43200³ = 80621568000000
surviving = 12288 * 1458 * 500 = 8957952000
surviving fraction = 1/9000.
```

Hence **8999/9000** of residue classes modulo43200 fail at least one of the necessary tests. This is a density **of classes modulo a deeper modulus**, not a claim that 1/9000 of all global integer solutions are present or that the surviving 8.96 billion classes contain any global norm−2 root.

## Explicit CRT lift of the previous local key

RQT-392 demonstrated local-only key `(1,49,34)`, satisfying `z.T Q z +2 = 0 mod240` but not the integer equation. RQT-393 constructs its genuine congruence-class lift

```text
(1,49,34) mod240
       ↓ add 240*3 to coordinate x
(721,49,34) mod43200
```

Checks:

```
(721,49,34) ≡ (1,49,34) mod240
(721,49,34).T Q (721,49,34) + 2 ≡ 0 mod43200.
```

The original-lattice vector `B*(721,49,34)` was checked directly to satisfy `(Bz).T F4 (Bz)=z.T Q z` as an exact integer identity. **Its actual integer norm is not −2**; it is explicitly **NOT** root19.

An exhaustive single-coordinate-lift audit tested all `k=0,...,179` for each of the three families `(1,49,34)+240*k*e_i`. Exactly four lifts occur when shifting x, with k=3,48,93,138; no such lift occurs when shifting y alone or z alone. These are complete finite calculations of that defined family, not claims about all lifts or all root19 candidates.

## Reproduction and exact evidence

```bash
python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
python research/rqt393-deeper-crt-lift.py /tmp/rqt388.json --out /tmp/rqt393.json
```

The proof is deterministic and uses integer-only congruences. Local executed equivalent:
- `/mnt/data/rqt393_deeper_crt.py`
- `/mnt/data/RQT-393-results.json`.

The complete counts and lift data are preserved in the GitHub `research/RQT-393-results.json` and are verified by assertions in the committed executable.

## Visual story

This turn's cinematic **3D** JPG is `RQT-393-The-Deeper-CRT-Lift-3D.jpg`. It shows a volumetric 9×9×9 GMA around central `||||`, 27 spatial cores, three prime-power filter planes, a golden lifted key labelled `(721,49,34)` and root19's still-locked portal. The user also receives a standalone HTML containing **the actual JPG encoded into the HTML**, suitable for offline viewing. A separate `rqt393.html` 3D interactive-style source page is committed to GitHub. The JPG binary itself is a conversation attachment and has **not** been committed to GitHub.

The visual is a narrated depiction of arithmetic, not an exact volumetric scatterplot of the `43,200³` residue classes.

## Next natural target — RQT-394

Stop treating arbitrarily high p-adic precision as global existence proof. Use the stronger CRT admissibility as a prefilter in a **constructive integral ternary norm-representation algorithm**, such as an exact indefinite ternary solver, quaternion-splitting, or binary norm descent. A genuine next-root witness requires **full integer** norm −2 and the original one-sided Wall pairing. Then root20 can be sought in its rank-two kernel and root21 forced by the signed cofactor theorem.

**Root18: first-stage PASS. Root19: OPEN. Root20: OPEN. Root21 conditional. Complete 21-reflection word OPEN.**
