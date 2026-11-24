# RQT-646 — Higher-Precision 2-Adic Integer Recovery Gates

## Exact result

RQT-645's generalized Pell-square and original integral-coordinate gate were independently replayed for all **27 canonical unresolved sign-orbits** at moduli **16, 32, 64, 128 and 256**.

For the original reduced quadratic
```
Q(u,t)=2(r₀u²+r₁ut+r₂t²+r₃u+r₄t+r₅)=0,
a=r₁²−4r₀r₂,
h=r₁r₃−2r₀r₄,
c=r₃²−4r₀r₅,
F(t)=at²+2ht+c, L(t)=r₁t+r₃,
```
a candidate pair (t,y) modulo m must satisfy `y²≡F(t) (mod m)`. Requiring the original coordinate u to exist at this precision adds
```
y ≡ +L(t) or −L(t)  (mod gcd(m,|2r₀|)).
```
The code exhaustively enumerates each residue pair, preserves all t-lists and verifies projection compatibility between consecutive powers of two.

| Modulus m | Pell-compatible (t,y) pairs | Recovery-compatible (t,y) pairs | Pell-compatible t residues | Recovery-compatible t residues | Pell t residues rejected |
|---:|---:|---:|---:|---:|---:|
| 16 | 1,728 | 1,544 | 432 | 432 | 0 |
| 32 | 3,552 | 3,232 | 784 | 704 | 80 |
| 64 | 7,936 | 7,296 | 1,488 | 1,408 | 80 |
| 128 | 15,744 | 14,464 | 2,824 | 2,704 | 120 |
| 256 | 30,976 | 28,416 | 5,328 | **5,168** | **160** |

These t-counts are **sums over separate canonical-orbit residue spaces**, not single sets on which to compute a density across differing moduli.

Exactly **ten** orbits have additional coordinate recovery restrictions at m=32,64,128,256:
`28,31,34,37,55,61,64,67,109,112`.
They are the same ten seen in RQT-645. Mod-256 excludes 160 additional orbit–parameter residue classes beyond the Pell-square test alone. No full canonical orbit loses every recovery-compatible t residue.

## Source provenance, reproducibility and limits

- Original exact RQT-619 and RQT-626 JSON certificates were reopened locally and their derived identities checked for all 27 orbits.
- Exact Python 3 standard-library verifier: `research/rqt646-higher-precision.py`.
- Full local 27-orbit certificate with individual t-lists: `RQT-646-results.json`; SHA-256 `a60604e9c2fded56eb1b59aeb1dfb9383d555e75822ef3b8b81c8f5a3d3d0f01`.
- The reported congruences are **necessary finite-modulus restrictions**. They do not establish genuine integer-square discriminants, Pell target seeds, actual norm−2 roots, or full-family exclusions.

The original RQT-619 and RQT-626 certificates share underlying owned source ancestry; they are not independent evidence roots.

Selected-family ledger unchanged: **82/135 excluded all-scale (60.74%), 53 unresolved**, represented by 27 canonical sign-orbits. Selected corridors do not exhaust the full lattice. Original 22D Wall **NOT REPLAYED**. **Root 19 OPEN**.

## RQT-647 natural bound

Construct a **compatible 2-adic lifting tree** for the ten sharpened orbits: distinguish branches that lift indefinitely from those blocked at the next precision, preserving original-coordinate recovery at each lift. Then compare with the already known exact mod-256 coordinate projection rather than double-counting the same conditions.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
