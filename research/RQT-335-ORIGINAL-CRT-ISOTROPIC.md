# RQT-335 — Authentic simultaneous 2-adic / 3-adic root construction

**Status:** Constructive **local** modular certificate PASS. Actual integral isotropic vector, integer eighteenth root and roots19–21 remain **OPEN**. This is not the synthetic bridge lattice.

## Immutable upstream source
Original F4 and unimodular H4: `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py` (RQT-242). RQT-334 classified the binary isotropic-to-root parity gate. The executable `research/rqt335-original-crt-isotropic.py` embeds the authentic F4/H4, verifies determinant and residual preservation and supplies reproducible long coordinates.

## Exact local construction
Set `Q(x)=x^T F4 x/2`. Choose two seed vectors:
- 2-adic: u2=(0,0,0,1), Q(u2)=0 mod2, (F4u2)_0 odd.
- 3-adic: u3=(0,1,0,1), Q(u3)=0 mod3, (F4u3)_0 not divisible by3.

At each exponent k for p=2 or p=3, if `Q(u)=0 mod p^k` and `(F4u)_0` is a p-adic unit, choose a digit `d in {0,...,p-1}` and update `u <- u+d p^k e0` so `Q(u)=0 mod p^(k+1)`. The digit is uniquely determined by the exact linearized congruence:

```text
d = -(Q(u)/p^k) * ((F4 u)_0)^-1 mod p.
```

Lift independently to `2^256` and `3^128`, then combine all four components by the Chinese remainder theorem to obtain one integer representative u modulo `M=2^256 * 3^128`. This representative satisfies `Q(u)=0 mod M` and `(F4u)_0` is a unit at both 2 and 3. The CRT representative is **not** an exact isotropic integer vector.

Choose vbar=(0,1,1,0) (binary parity 0110), which pairs oddly with u. Adjust only v_0 by an even multiple to make `u^T F4 v=1 mod M`, preserving vbar parity. Set

```text
w = v - Q(v) u
r = u - w.
```

Exact integer calculations establish `Q(w)=0 mod M`, `u^T F4 w=1 mod M`, and `r^T F4 r=-2 mod M`. The root parity is **0111**, one of the authentic RQT-256 order-reducing classes. The successor reflection has mod2 order 2 and binary moving rank 1.

**Critical limitation:** The exact `Q(u)` is nonzero and the exact `r^T F4 r` is **not** -2. This is only one high-precision local arithmetic approximation, not an actual integer root18. The original RQT-249 already had a high-precision four-column modular completion, so this checkpoint isolates a constructive *isotropic/Bézout* route; it does not surpass that in global existence.

## Next bound RQT-336
A rational isotropic construction or certified rational reconstruction is needed to replace the local representative u with a genuine integer vector satisfying `Q(u)=0` exactly. Then compute gcd(Fu), construct exact r18 with RQT-334, and test RQT-257's six lower Wall equations for roots19–21. The 2-adic and 3-adic evidence alone cannot ensure exact global integrality.

## Witness lineage
- Original frozen F4/H4: stoicheion RQT-242, one source.
- Modular condition at 2: derived arithmetic witness.
- Modular condition at 3: derived arithmetic witness.
- CRT: derived from same F4/H4, not a third independent original source.
- Josophene/Juliet nested 3x3x3 tensor and time/angular address: evidence and iteration metadata only; no physical quantum hardware test.
