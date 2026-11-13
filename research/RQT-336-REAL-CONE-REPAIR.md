# RQT-336 — Real-cone obstruction to the old local lift, and repaired seeds

**Original frozen lattice:** `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py` (authentic F4/H4). **Exact geometric obstruction proven.** An exact primitive isotropic vector and roots 18–21 remain OPEN.

## What was wrong with the RQT-335 local route?

RQT-335 lifted the local seeds `(0,0,0,1)` and `(0,1,0,1)` solely by changing coordinate zero. Its modular isotropic candidate therefore had `x2=0` identically throughout. That 3D slice is **negative definite over R** for the true frozen Gram, so no nonzero rational or integral isotropic vector exists in it. Increasing modular precision on that one slice cannot yield an exact rational root.

Exact restriction F4 to indices (0,1,3) has leading principal minors

```text
-4523390658618420908
 25308187194284000900348648581750862832
-221558456266631028133980179381936436454111437649775071276
```

Signs are -, +, -, satisfying Sylvester's negative-definiteness criterion. Hence `u.T F4 u=0`, `u != 0` necessarily implies `u[2] != 0` (zero-based coordinate numbering). This is an *exact global real-geometric filter* for the isotropic construction, not a no-go for norm-minus-two roots.

## Corrected local construction

Choose seeds with nonzero coordinate 2:

- 2-adic seed `u2=(0,0,1,0)`; `Q(u2)=0 mod2`; derivative at coordinate 0 a 2-adic unit.
- 3-adic seed `u3=(0,1,1,1)`; `Q(u3)=0 mod3`; derivative at coordinate 0 a 3-adic unit.

Hensel-lift each by changing coordinate 0 only to powers `2^256` and `3^128`. Coordinate 2 remains **1** exactly. CRT combines the residues modulo `M=2^256*3^128`; the resulting representative has `u[2]=1`, `Q(u)=0 mod M`, parity 0010 and the chosen local unit pairing. For a binary-compatible Bézout partner, construct `w=v-Q(v)u`, `r=u-w`; the candidate has parity **0111** and norm minus two modulo M. Its binary successor has order two and moving rank one.

**Critical:** `Q(u)` is not zero as an integer and `r.T F4 r` is not minus two as an integer. The repaired sequence only eliminates the previous real-impossibility obstruction; it does not construct an exact root18. A 2-adic/3-adic approximation may be far from an actual rational point.

## Reproduction

`python research/rqt336-real-cone-repair.py` with SymPy; exact integer checks, no floating-point decisions.

## Next natural target RQT-337

Construct an actual **rational** isotropic vector with nonzero coordinate 2 on the original quadric, then primitive-integralize it, check pairing divisibility one and perform the RQT-334 exact Bézout construction. Prefer an explicit indefinite quadratic-form solver or rational parametrization with certified matrix identities. Stop counting modular digits as exact global roots.

## Provenance

Original F4/H4 is one source ancestry. CRT modulo two primes creates two computational witnesses, not two independent original sources. Nested 3×3×3 brace/box/toroid, {{i}}/{{j}}/{{n}}, Juliet and time-angle indexing label search evidence; no hardware quantum result is claimed.
