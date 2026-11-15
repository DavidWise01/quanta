# RQT-389 — The Three-Dimensional Forge: Two Global Hyperplanes Closed

**2026-11-15 · Original rank-three root-19 Wall kernel · Exact integer proof PASS · Root 19 OPEN.**

## The genuine next-root equation

RQT-386 produced an original integer F4 norm−2 root and RQT-387 verified its first-stage rational and GF(2) order/rank reductions. The successor root19 must satisfy both:
```
r19.T F4 r19 = -2
r19.T H4 r18 = 0.
```
RQT-377 constructed the **saturated** integral rank-three Wall kernel, and RQT-388 transformed its basis by an exact unimodular matrix with determinant −1. In its fixed reduced basis B, `r19=B*(x,y,z)`, and `Q=B.T F4 B` is the exact even integral indefinite ternary Gram with signature (1 positive, 2 negative). Set `T=Q/2`: the equation to solve is `(x,y,z).T T (x,y,z)=-1`.

The preserved cubic GMA remains nine generations of 9×9×9, grouped in 27 spatial cores around the singlet `||||`. The cubic addressing is not substituted for the exact quadratic form.

## New exact global theorem — two coordinate planes cannot contain root19

Take the coordinate planes **x=0** and **y=0** in the RQT-388 fixed reduced integer basis. Each restriction of `T` is a binary symmetric negative definite integral Gram. Equivalently, `P=-T_restricted` is positive definite.

RQT-389 independently runs **exact binary Gauss reduction** on each P, tracking integral `U∈GL(2,Z)`. It certifies all three fundamental conditions:
```text
abs(det(U)) = 1
T_reduced = U.T P U
0 < T_reduced[0,0] <= T_reduced[1,1]
2*abs(T_reduced[0,1]) <= T_reduced[0,0]
```
The Gauss reduction theorem then makes the first basis vector a shortest nonzero vector. Its exact squared-length `m=T_reduced[0,0]` is a **global minimum over every nonzero integer pair** on that coordinate plane.

| Reduced ternary plane | Exact shortest half-norm magnitude | Certified bit length |
|---|---|---:|
| `x=0` (coordinates 1,2) | exact positive integer in replayable JSON | **1090 bits** |
| `y=0` (coordinates 0,2) | exact positive integer in replayable JSON | **1088 bits** |

Both shortest magnitudes exceed 1 enormously. Every nonzero vector on either plane therefore has half-norm at most `-m<-1` and cannot solve `z.T T z=-1`. The zero vector also fails. Thus:

```text
For ANY genuine integer successor root19:
    x != 0 AND y != 0.
```

This is an **unbounded exact certificate**, not a sampled search radius or a claim that the full indefinite ternary lattice lacks solutions. It is specific to the fixed RQT-388 reduced integer basis; the numerical coordinate-zero condition is basis dependent.

## Local shadows: 2-adic and 3-adic witnesses are NOT global roots

Restrict further to the fixed line `(x,0,1)`. Its norm equation is an ordinary integer quadratic

```text
f(x)=T00*x*x + Q02*x + T22 + 1 = 0.
```

Its exact discriminant is **negative** (2441-bit magnitude), and `T00<0`, so the equation has **no real solution at all**.

Nevertheless, exact modular lifting produces:
```text
f(1127524804) == 0  (mod 2^32)
f(3157891116) == 0  (mod 3^20)
```
with **four** roots modulo 2^32 and **two** modulo 3^20. An exact CRT combination satisfies the equation modulo `2^32 * 3^20`, but the resulting **integer f(x) is not zero**, as the negative discriminant proves is inevitable.

This is a precise counterexample to promoting local p-adic/CRT agreement to global integral norm representation. Its two local witness families do not count as independent *original-source* ancestries because both come from the same F4 data.

## Reproduction and evidence

Primary executable `research/rqt389-global-two-plane-exclusion.py` consumes the exact machine-readable rank-three kernel from RQT-388. It accepts either archived local JSON key `restricted_F4_Gram` or the committed RQT-388 standalone engine's `restricted_Gram` field.

```bash
python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
python research/rqt389-global-two-plane-exclusion.py /tmp/rqt388.json --out /tmp/rqt389.json
```

The exact result file contains both full (1000+-bit) minimum half-norm integers, the binary unimodular change-of-basis matrices, the proof assertions, the local 2/3-adic witnesses and the CRT modulus. Local executed artifacts:
- `/mnt/data/rqt389_exact_slices.py`
- `/mnt/data/RQT-389-exact-certificate.json`
- `/mnt/data/rqt389_local_global.py`
- `/mnt/data/RQT-389-local-global-results.json`
- `/mnt/data/RQT-389-The-Three-Dimensional-Forge.jpg`.

The JPG is a narrative illustration of the two excluded planes disappearing from the cubic model. It is **not** a plot of individual exact root vectors; its binary remains a conversation artifact. A self-contained HTML/SVG story page is separately committed into the repository.

## Next natural target RQT-390

Now impose `x*y != 0` **as a mathematically certified invariant** in a constructive indefinite ternary representation algorithm, and investigate the remaining nonexcluded `z=0` slice as a binary Pell-type norm representation. A genuine r19 must be explicitly reconstructed through the saturated kernel and verified with the original F4/H4 norm and Wall pairing; its finite/p-adic shadows are not enough.

**Root18: first-stage accepted. Root19: OPEN. Root20: OPEN. Root21: conditional cofactor. Full 21-word: OPEN.**
