# RQT-611 — 7-Adic Geometry & Integral Seed Compatibility

## Executive summary
RQT-610 proved exact all-exponent 7-adic branch counts for the two singular selected families, **2** and **24**. RQT-611 derives a new, globally necessary **parameter-congruence gate** and constructs eight independently checkable regular 7-adic jets for each family through precision **7^11**.

An integer norm−2 solution in family **2** necessarily satisfies
```
t (mod 49) ∈ {13,20,27,34}.
```
In family **24** the corresponding condition is
```
t (mod 49) ∈ {15,22,29,36}.
```
This excludes *parameter congruence classes*, not either family at all scales. Four of the seven classes compatible with the unique root mod 7 survive the next relevant stage.

## Exact proof
Write `Q(u,t) = q_F(u,ray*t+offset)+2`. For each family the sole mod-7 root `(u0,t0)` is respectively `(1,6)` and `(6,1)`. RQT-610 certified the **exact integer identity** `Q(u0+7x,t0+7y)=49 P(x,y)`. The eight zeros of each reduced polynomial P modulo 7 are all regular (nonzero coordinate gradient). Their y-coordinates are:
- Family 2: `{1,2,3,4}`.
- Family 24: `{2,3,4,5}`.

Because any exact integral zero Q=0 must satisfy P=0 modulo 7, `t=t0+7y` must lie in the corresponding four classes modulo 49. Conversely, these four classes are only **local necessary conditions**: they do not establish the existence of a global integer seed.

For every one of the eight regular reduced roots, a deterministic derivative-controlled Hensel lift was constructed through `P(x,y)=0 (mod 7^10)`. The exact original norm identity then yields `Q(u,t)=0 (mod 7^11)` for the mapped `u=u0+7x,t=t0+7y`. All 16 reconstructed jets were individually verified by exact integer arithmetic. The complete JSON certificate contains each stage of the jet and its final u,t residue. This is a *7-adic compatibility witness*, not an integer norm−2 solution.

## Source provenance
- RQT-610 local certificate SHA256: `d1f4b2b7b6252aece3dde0c24c6d298f530dfd455c7fcd8a9fdf1ad9022d61a3`.
- Exact RQT-611 replay uses the original reduced-polynomial coefficients and roots in that certificate.
- All arithmetic is integer-only; no numerical approximations or arbitrary root guesses.

## Status
- Local branches carried to 7^11: **8/8 per family**, **16/16 total**.
- Newly certified global necessary t restrictions: **two** (one per family).
- New *whole-family* all-scale exclusions: **0**.
- Selected-family ledger unchanged: **82/135 excluded (60.74%), 53 unresolved**.
- Original 22-dimensional Wall replay not performed; Root 19 **OPEN**.

## Next natural bound — RQT-612
Combine the new 49-residue restrictions with existing exact prime-power conditions and check whether an admissible **integer Pell seed** is found. Distinguish congruence-compatible integer parameters from square discriminants and exact norm−2 vectors; preserve the original Wall verification gate.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
