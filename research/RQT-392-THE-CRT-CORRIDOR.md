# RQT-392 — The CRT Corridor: 98% of modular coefficient classes excluded

**2026-11-15 | Authentic frozen F4/H4 audit PASS | Original root19 remains OPEN.**

## Where the search stands

RQT-386 produced a true integer norm−2 original F4 reflection, RQT-387 certified its first-stage rank/order properties, RQT-388 constructed the exact saturated rank-three Wall successor kernel and reduced its basis, RQT-389/390 globally excluded its three coordinate planes, and RQT-391 checked the 400-million-pair exact cylinder with the third coordinate algebraically unrestricted. None of the latter operations recovered root19.

This turn advances the **constructive congruence sieve** for the rank-three successor equation, not a radius search:

```text
r19 = B*(x,y,z)
Q = B.T F4 B
(x,y,z).T Q (x,y,z) = -2.
```

Here B is the original RQT-388 saturated **integer** Wall-kernel basis, with `r19.T H4 r18=0` automatically. The exact root must satisfy every modular reduction of the norm equation.

## New exact mod-3 rule

The full original restricted Gram, reduced modulo 3, is

```text
Q mod3 =
[1 0 1]
[0 0 0]
[1 0 1].
```

Consequently `(x,y,z).T Q (x,y,z) ≡ (x+z)^2 (mod3)`. As the target `-2 ≡ 1 mod3`:

```text
(x+z)^2 ≡ 1 (mod3)  <=>  x+z not divisible by 3.
```

Exactly **18 of 27** coefficient residue triples mod3 survive. This excludes one-third of all coordinate triples in their residue system without any coordinate bound.

## Exact mod16 parity and mod5 combination

From RQT-390, the fixed reduced Gram satisfies

```text
Q mod16 =
[ 2  8  2 ]
[ 8  4  6 ]
[ 2  6 14 ].
```

The exact equation `v.T Q v = -2 mod16` holds for **768 of 4096** triples mod16, with precisely three coefficient parity patterns:

```text
001: 256 admissible triples
011: 256 admissible triples
110: 256 admissible triples.
```

Because Q has even diagonal and is symmetric integral, adding 8 to any coefficient does not change `v.T Q v mod16`. Therefore the same condition can be checked on coefficient triples mod8, with exactly **96 of 512** such triples admissible; this is **not** the weaker norm-mod8 condition that admits 192 of 512 triples. Mod5 independently admits **20 of 125** residue triples.

The moduli 16, 3 and 5 are pairwise coprime. By CRT their coefficient triples combine bijectively to triples modulo `16*3*5=240`:

| Local norm condition | Admissible | Total | Fraction |
|---|---:|---:|---:|
| Mod16 | 768 | 4096 | 3/16 |
| Mod3 | 18 | 27 | 2/3 |
| Mod5 | 20 | 125 | 4/25 |
| **Combined CRT mod240** | **276480** | **13824000** | **1/50 = 2%** |

Exactly **49 of 50** modulo-240 coefficient classes are excluded by these necessary conditions. This is a universal, periodic residue-class exclusion, not an estimate from sampling; it DOES NOT claim only 2% of global exact roots exist, nor that any of the surviving classes actually contains an integer root.

## Explicit local-only CRT seed

Select the integer coefficient triple

```text
(x,y,z) = (1,49,34).
```

The exact original-F4 restricted norm obeys

```text
v.T Q v ≡ -2 ≡ 238 (mod240).
```

The program maps `B*v` back to the original four-coordinate lattice and checks `(B*v).T F4 (B*v)=v.T Q v` **exactly**. Crucially, the exact norm is **not** −2. The triple is a genuine **local CRT witness but not root19**. This retains the invariant that repeated local modular observations are not proof of a global norm representation.

## Reproducible source and data

```bash
python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
python research/rqt392-crt-corridor.py /tmp/rqt388.json
```

The committed RQT-392 program independently embeds authentic frozen F4/H4 and checks `Q=B.T F4 B`, the original Gram modulo 3 and 16, the full residue enumerations, the CRT fraction and the sample vector. Executed local source: `/mnt/data/rqt392_crt_corridor.py`. Executed exact JSON: `/mnt/data/RQT-392-crt-corridor-results.json`.

## 3D visual-story artifact

The new high-definition JPG **RQT-392-The-CRT-Corridor-3D.jpg** shows the 9×9×9 GMA cube with the 27 spatial cores and central `||||` singlet, three distinct modular filter beams eliminating most candidate classes, the small local key `(1,49,34)`, and the still-locked root19 portal. This is conceptual visual narrative, not a scatterplot of the full 13.8-million-class residue space. The JPG is delivered in the conversation; the `rqt392.html` GitHub story uses a self-contained 3D-style visualization. The JPG binary has **not** been uploaded to GitHub.

## Next RQT-393

The next meaningful target is to **lift a CRT-admissible residue class into a true exact integer norm−2 solution** using a constructive indefinite ternary quadratic/norm representation algorithm, not merely to multiply more modular filters or expand the cylinder. The exact congruence gate is now ready to prefilter candidate vectors. If root19 is recovered, reconstruct it as `B*z` and verify its original F4 norm and Wall pairing with root18, then descend to rank2 for root20; root21 is supplied by the conditional cofactor theorem.

**Root18: first-stage PASS. Root19 OPEN. Root20 OPEN. Root21 conditional. Full 21-reflection product OPEN.**
