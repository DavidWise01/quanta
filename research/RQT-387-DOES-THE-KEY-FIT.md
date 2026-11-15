# RQT-387 — Does the Key Fit? Exact first-stage successor verification

**2026-11-15 | Original frozen successor gates PASS | Full 21-reflection word still OPEN.**

## Original source recovered; correct criterion established

This turn directly retrieved **original authoritative records** from `DavidWise01/stoicheion`, notably:
- [RQT-241 explicit seventeenth integral Wall root](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-241-explicit-seventeenth-root.md);
- [RQT-256 first-reflection order-reduction invariant](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-256-first-reflection-order-reduction.md);
- [RQT-257 automatic reflection-product theorem](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-257-automatic-reflection-product.md).

These establish that the original first 17 integral roots are a **frozen independent Wall prefix**, and its saturated rank-four residual has exact integral F4, H4 and `D4=I+H4^{-1} F4`. The candidate root18 must be an integral norm-minus-two root and satisfy the rank/order-reduction criterion. It is **not** correct to require `r18.T*H4*r_i=0` against all 17 in these **reduced 4D coordinates**; the original 17 constraints were already used to form the saturated residual rank-four kernel.

RQT-257 further proves that any **complete four-root internal Wall flag** of norm −2 roots, with all six lower H4 pairings zero, **automatically multiplies to D4**. Hence once compatible roots19 and20 and the forced cofactor root21 are constructed, the residual product needs no additional nonlinear search.

## Authentic RQT-386 candidate, now tested against the original successor test

Input is the explicit original F4 root candidate from `RQT-386-Exact-Root-Candidate.json`. Its exact integer coordinates (≈488 digits apiece) and construction are published reproducibly in [RQT-386 source](https://github.com/DavidWise01/quanta/blob/main/research/rqt386-exact-null-and-root-candidate.py).

The independent RQT-387 script **rechecks** the full integer null and Bézout certificate, original Gram and Wall identities and the exact candidate root:

```text
u.T F4 u = 0
gcd(u) = gcd(F4*u) = 1
u.T F4 v = 1
r = (1+v.T F4 v /2)*u - v
r.T F4 r = -2
r.T H4 r = 1
r mod2 = 0111
S_r = I+r*(r.T F4)
S_r²=I, S_r.T F4 S_r=F4, det(S_r)=-1
```

Now define the **genuine original reduced residual**

```text
D4 = I+H4.inv()*F4
E = S_r * D4.
```

Exact rational matrix arithmetic yields:

| Gate | Original D4 | After S_r D4 |
|---|---:|---:|
| Rank over Q of (operator − I) | **4** | **3** |
| Moving rank over F2 | **2** | **1** |
| Order over F2 | **3** | **2** |

In fact the new residual mod 2 is **exactly**

```text
[0 0 0 1]
[0 1 0 0]
[0 0 1 0]
[1 0 0 0]
```

That matrix exchanges the first and fourth coordinates, fixes the middle two, squares to the identity, and differs from identity by rank one mod2. The original D4 has order three mod2. These facts were independently checked using a handwritten GF(2) Gaussian-elimination rank routine rather than relying on SymPy's rational rank.

**RQT-387 conclusion: the RQT-386 norm-minus-two vector passes the exact original first-stage order/rank test for the eighteenth root candidate.** The input vector's SHA-256 over its comma-separated decimal coordinates is

```text
2247dc33eb514ac60e8fe3a39c157f9dbe4b8781b5ad42501c1e5860f89eb6a4
```

## Critical boundary: not yet a certified complete 21-word

This candidate qualifies for the prescribed first-stage reduction. **It has not been completed into a valid four-root internal Wall flag**, and thus has not yet certified the exact twenty-one-reflection product. In particular, no original integer root19 or root20 is exhibited and the forced root21 remains conditional on a valid triple.

Previous language about an additional all-17 one-sided Wall-orthogonality gate in the reduced rank-four coordinates was too restrictive; the recovered RQT-241/256/257 source determines the correct check. This correction is append-only and does not erase the earlier ledger.

## Reproduction

The published [RQT-387 executable](https://github.com/DavidWise01/quanta/blob/main/research/rqt387-first-lock-audit.py) can operate either on the provided exact JSON certificate or reconstruct it by running the prior RQT-386 source:

```bash
python research/rqt387-first-lock-audit.py --certificate RQT-386-Exact-Root-Candidate.json
# or
python research/rqt387-first-lock-audit.py --reconstruct research/rqt386-exact-null-and-root-candidate.py
```

The local execution passed and saved:
- `/mnt/data/rqt387_first_lock_audit.py`;
- `/mnt/data/RQT-387-first-lock-results.json`;
- `/mnt/data/RQT-387-Does-The-Key-Fit.jpg`.

The illustration shows the recovered candidate opening the **first** lock, with three still-open downstream gates. This is narrative mathematical art; numbers printed on the verification panel represent executed exact results. The JPG is available in the conversation. An HTML/SVG self-contained Git story page is also being published to the root of the `quanta` repository.

## Next RQT-388

Search the **rank-three saturated integer Wall kernel** for an exact norm-minus-two root19 with the correct one-sided pairing to this recovered root18. Use the certified kernel basis and exact restricted Gram from `RQT-386-Root19-Conditional-Kernel.json`. Once r19 is found, pass to rank two for r20; then RQT-379 constructs the fourth automatically from cofactors. Original 27 spatial cores and `{{9×9×9}}^9` story continue.

**Root18 first-stage gate PASSED. Roots19,20 remain OPEN. Root21 is conditionally forced. Full 21-word remains OPEN.**
