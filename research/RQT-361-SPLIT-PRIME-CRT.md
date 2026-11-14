# RQT-361 — Exact split-prime CRT branches and norm-target factorization boundary

**2026-11-14. PASS:** reproducible arithmetic CRT certificates on the authentic RQT-242 frozen Gram `F4`. **No explicit norm-zero vector or original roots18–21.**

## Source and prior chain

RQT-351 establishes rational isotropy in slopes 194/195 and 201/202. RQT-353A establishes that any primitive integer isotropic point on these planes has `gcd(F4u)=1`. RQT-355 supplies unimodular reduced ternary transforms; RQT-357 gives the exact norm identity `M²+D L²=p*N*h²` with indispensable integral reconstruction gates; RQT-360 proves `D=c² delta` with squarefree delta.

This result retains the source ancestry of `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, and independently checks its exact determinant. No synthetic Gram or local congruence is promoted to a global root.

## New exact decomposition of the norm target

Set `C=p*N`, so the equation is `M²+delta*B²=C*h²` for `B=cL`. Two certified **partial** factorizations of C are:

```
194/195:
C = 2³ · 3 · 223 · 281297 · Q1
Q1 = 4341012393885871793429166991367328918895695969836018205135496291

201/202:
C = 2³ · 3² · 5 · 23 · 103 · 12967 · Q2
Q2 = 1856169084206954410930471425091180170460861602787423710191998241
```

The exact verifier proves both identities. All listed small factors are prime; **Q1 and Q2 are composite** (certified by SymPy `isprime`, without a supplied factor pair), each is coprime with its corresponding delta, and neither has a prime divisor below 25001. These are **NOT complete prime factorizations** of the norm targets. The composite Jacobi symbol `(-delta|Qi)` is +1 for each, but **a Jacobi symbol of +1 does not show that every prime factor splits.**

## Explicit known split-prime square roots

For a known odd prime `ell|C` with `(-delta|ell)=1`, compute `r_ell²=-delta mod ell`; any exact norm solution must satisfy one of the two branches `M=±r_ell*B mod ell`. The computed roots are:

| slope | known split prime ell | exact root r_ell |
|---|---:|---:|
| 194/195 | 223 | 110 |
| 194/195 | 281297 | 47821 |
| 201/202 | 5 | 1 |
| 201/202 | 23 | 10 |
| 201/202 | 103 | 44 |
| 201/202 | 12967 | 3827 |

The prime 3 is ramified in both fields; it is not labeled split. The prime 2 is treated separately.

The Chinese remainder theorem combines the **positive-sign branch**:

```text
194/195:
P = 223*281297 = 62729231
R = 60807973
R² ≡ -delta mod P
necessary branch M ≡ R*B mod P

201/202:
P = 5*23*103*12967 = 153594115
R = 145065656
R² ≡ -delta mod P
necessary branch M ≡ R*B mod P
```

An exact solution may choose a **different independent sign for each prime**: 4 branches for the first plane and 16 for the second. A single CRT root is not a sufficient membership or existence proof.

## Construction gate

Any putative `(M,B,h)` must pass **all**:

1. `M²+delta*B²=C*h²` **exactly**, not only modulo P.
2. `c|B`, and `L=B/c`.
3. `D|(M+gamma*h)`, with `y=(M+gamma*h)/D`.
4. `p|(L+g0*h-q*y)`, with `x=(L+g0*h-q*y)/p`.
5. `u=T*V*(x,h,y)` is primitive and satisfies `u^T F4 u=0` exactly.
6. Apply RQT-353A to test pairing divisibility one, then RQT-334 for root18 and RQT-257 exact Wall continuation.

The program `research/rqt361-split-prime-crt.py` is standalone, reproduces all factors and CRT roots from the authentic F4, and marks unresolved cofactors and integer roots explicitly.

## RQT-362 natural target

Finish factoring composite Q1/Q2 or implement a certified ideal-norm representation solver that can work without complete factorization; then recover an exact triple respecting the image lattice. The CRT branches reduce the search space but alone do not establish global solutions.

The 3×3×3 cubit, Josophene/Juliet, braces and time-angle addresses remain research-index metadata.
