# RQT-334 — Constructive isotropic-to-eighteenth-root parity gate

**Status: exact frozen-lattice binary classification and conditional Bézout theorem PASS. Actual isotropic vector and root18 OPEN.**

## Source
The integral symmetric even Gram F4 and unimodular Wall H4 are embedded exactly from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. Original residual is `D4=I+H4^-1F4`. This is not the RQT-307 synthetic bridge.

## Constructive target
Find an actual `u in Z^4` satisfying `u^T F4 u=0` and `gcd(F4u)=1`. This is the explicit primitive isotropic vector required by the RQT-247 existential proof and the RQT-253 infinite-orbit construction.

Once such u exists, the pairing map `z -> u^T F4 z` is surjective onto the integers, so for any binary class `vbar` with `u^T F4 vbar ≡ 1 (mod 2)`, take `v=vbar+2z` such that `u^T F4 v=1`. Since F4 is even, `q(v)=v^T F4 v/2` is integral. Set

```
w = v - q(v)u
r = u - w.
```

Then `u²=0`, `w²=0`, `u·w=1`, so `r²=-2` exactly. Also `u·r=-1` forces `gcd(F4 r)=1`, without an extra search. The resulting parity is `r ≡ vbar+(1+q(vbar))u (mod2)`.

## Complete binary enumeration from authentic F4

An actual norm-zero u with gcd(F4u)=1 has `q(u)≡0 (mod2)` and `F4u !=0 (mod2)`. There are exactly **six** such binary u classes:

| u mod2 | eligible root18 parities achievable |
|---|---|
| 0001 | 0111,1001 |
| 0010 | 0111,1110 |
| 0101 | 0111,1001 |
| 0110 | 0111,1110 |
| 1000 | 1001,1110 |
| 1100 | 1001,1110 |

For each u class, exactly four binary v classes satisfy odd pairing and yield an accepted first-root parity. Thus **24 compatible (u mod2,v mod2) pairs** in total. Every possible primitive norm-zero u class supports **two** of the three desired first-root parity classes. The script enumerates them exhaustively from the original F4 and proves the hyperbolic-plane Bézout norm identities symbolically.

This establishes that if an actual primitive norm-zero u of pairing divisibility one is found, its parity creates **no further obstruction** to constructing a genuine integral norm−2 root18 in one of the required binary classes. The resulting root automatically drops the rational moving rank 4→3, and the RQT-256 result implies binary order 3→2.

## Critical limitations

- No explicit integral u or r18 in frozen coordinates has been constructed here. The RQT-247 theorem established existential availability, but the large-height search is still needed.
- The parity screen only handles the first-root gate. It does **not** certify one of the forty modulo-four full-completion-compatible first-root residues, six exact Wall equations, roots19–21, or full 21-reflection product.
- This is a **conditional constructive theorem** plus exhaustive finite binary enumeration, not an instantiated root witness.
- It avoids repeating small-height exclusion searches and supplies targeted parity data for rational-isotropic solvers.

## RQT-335 — next natural bound

Find a concrete rational isotropic point on the original F4 quadric, clear denominators to a primitive integer u, check `gcd(F4u)`, and if div1 apply this certified gate to produce and verify **actual r18**. Pin exact source coordinates and SHA in the evidence ledger.

Nested {brace[box(toroid)]} geometry with 3×3×3 positions, Josophene and Juliet are source/iteration metadata only; independent proofs remain exact arithmetic.
