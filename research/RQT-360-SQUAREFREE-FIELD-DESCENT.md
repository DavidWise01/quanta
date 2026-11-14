# RQT-360 — Squarefree norm fields for two authentic ternary conics

**Exact arithmetic verified, 2026-11-14.** This is a field-reduction certificate, not a global rational point or original root18.

## Ancestry
Original frozen `F4` from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`; RQT-355's unimodular reductions for rational slopes `194/195` and `201/202`; RQT-357 reversible norm equation; RQT-358 integer conductor and membership caveat. RQT-351 local-global existence and RQT-353A primitive divisibility-one theorem remain upstream results. No alternate Gram used.

## Exact new factorization

For reduced Gram `A=V.T*T.T*F4*T*V`, let `p=-A00`, `q=-A02`, `r=-A22`, `D=p*r-q*q`, `gamma=p*A21-q*A01`, and `N=det A`. The exact quadratic norm relation is `M²+D L²=p N h²`, with `L=p*x+q*y-A01*h` and `M=D*y-gamma*h`.

**194/195**:
```text
D = 2020692228609206586199528939517571540
  = 2² * 3 * 5 * 103 * 3389 * 96480629249265737246217724177
  = 2² * 505173057152301646549882234879392885
c = 2
delta = 505173057152301646549882234879392885
fundamental field discriminant = -2020692228609206586199528939517571540
```

**201/202**:
```text
D = 3272928109767528305742489923852754456
  = 2³ * 3⁵ * 409 * 4116393630162305313751408539161
  = 18² * 10101629968418297239945956555101094
c = 18
delta = 10101629968418297239945956555101094
fundamental field discriminant = -40406519873673188959783826220404376
```

The large factors in both factorizations passed primality verification in SymPy; delta is squarefree. These are different quadratic fields `Q(sqrt(-delta))`. Their ramified rational primes are exactly the prime divisors of their fundamental discriminants: first `2,3,5,103,3389,96480629249265737246217724177`; second `2,3,409,4116393630162305313751408539161`.

## A genuine norm equation, with all integer gates retained
Introduce `B=c*L`. Then the identity becomes

```text
Norm_{Q(sqrt(-delta))/Q}(M+B*sqrt(-delta)) = M²+delta*B² = p*N*h².
```

**This is not an independent, automatically equivalent integer equation.** Its solutions must pass the original membership constraints:
```text
B mod c = 0,
L=B/c,
(M+gamma*h) mod D = 0,
y=(M+gamma*h)/D,
(L+A01*h-q*y) mod p = 0,
x=(L+A01*h-q*y)/p.
```
Then and only then does `(x,h,y)` produce a guaranteed integral ternary vector, `u=T*V*(x,h,y)`, with `u.T*F4*u=0`.

The exact executed verifier asserts original determinant, unimodular basis, full integer factorization, primality, squarefree decomposition, fundamental field discriminant, and norm plus inverse identities on multiple signed triples. These are exact calculations, not approximate roots.

## Status and next RQT-361
The explicit integer null vector is **OPEN**; so are original roots 18–21. A constructive solver could now use quadratic-field ideal arithmetic, norm representation or a certified ternary conic solver in each field, but it must filter all reconstructed candidates by the full lattice membership constraints and original F4 norm. Progress requires an exact integer witness; multiplying local residues or loosening integrality gates is not progress.

Local executed artifacts: `/mnt/data/rqt360_quadratic_field_descent.py`, `/mnt/data/rqt360_quadratic_fields.json`.
The bracket/cubit time-angle syntax is provenance indexing rather than an arithmetical proof.
