# RQT-357 — Reversible arithmetic norm equation for two original conics

**2026-11-14 — Exact symbolic identity PASS.** This is a constructive equation reduction, **not** an explicit rational/null-vector solution. Original integral roots 18–21 remain **OPEN**.

## Exact source

The original frozen rank-four Gram is F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, checked by its full determinant. The two ternary planes `194/195` and `201/202` were proved rationally isotropic in RQT-351 and pairing-divisibility-one for primitive integer null vectors in RQT-353A. The exact unimodular ternary transformations V were established in RQT-355.

Write `z=(x,h,y)`, `u=T*V*z`, `A=V.T*T.T*F4*T*V` with `T(a,b,c)=(-ma,b,na,c)`. Define
```
p = -A[0,0] > 0
q = -A[0,2]
r = -A[2,2] > 0
g0 = A[0,1]
g1 = A[2,1]
D = p*r-q*q > 0
gamma = p*g1-q*g0
N = det(A) > 0.
```

## Exact, reversible identity

Set `L=p*x+q*y-g0*h` and `M=D*y-gamma*h`. Symbolic expansion over the integers **proves identically**:

```
D*L² + M² - p*N*h² = -p*D*(z.T*A*z).
```

Thus `z.T*A*z=0` implies `D*L²+M²=p*N*h²`. Conversely, if integers `L,M,h` satisfy this norm equation **and the two required congruences**:

```
M + gamma*h ≡ 0 (mod D)
y = (M + gamma*h)/D
L + g0*h - q*y ≡ 0 (mod p)
x = (L + g0*h - q*y)/p
```

then `x,h,y` are integers and satisfy `z.T*A*z=0` exactly. The reconstruction identities were checked on multiple signed integer triples, and the polynomial identity was proved for arbitrary symbols. **Never drop the two congruence gates**: a generic norm-equation solution need not map into the integer ternary lattice.

## Numerical coefficients (all integers)

| constant | slope 194/195 | slope 201/202 |
|---|---:|---:|
| p | 561555435662335446 | 932546695834969470 |
| q | -758956630833872688 | -793284734389436322 |
| r | 4624133667290001854 | 4184486200006240562 |
| D | 2020692228609206586199528939517571540 | 3272928109767528305742489923852754456 |
| g0 | 907442644571173949 | 1534419477527031407 |
| gamma | 2139658254648790665123572010888675738 | 3735953012725885367431690182925799424 |
| N=det(A) | 11638033302642746511259255234414222206289825409305543124 | 22011722020759586930044622407479396684126082368458590484 |

Additional exact consistency: `gcd(D,gamma)` is 6 for slope 194/195 and 24 for slope 201/202, while `gcd(D,p*N)` is respectively 12 and 72.

## Proof status

- PROVED: each original ternary conic is mathematically equivalent over **integer coordinates** to its displayed binary norm equation **with the two congruence gates**.
- PROVED upstream: rational isotropic points exist on both planes (RQT-351), and any primitive integer isotropic point there has gcd(F4u)=1 (RQT-353A).
- NOT FOUND: actual integer solutions to the norm equations satisfying both congruence gates; no explicit u; no explicit norm-minus-two root18; no four-root Wall completion.

This is a better arithmetic solver interface than blindly raising reduced-coordinate height. An exact solver can now attack norm representation `M²+D*L²=p*N*h²` using norm equations in Q(sqrt(-D)), binary quadratic forms / ideals, or certified conic algorithms, then filter via the two integral reconstruction congruences.

## Reproduce

`python research/rqt357-reversible-norm-equation.py` (SymPy). Local executed: `/mnt/data/rqt357_norm_equation.py`; JSON `/mnt/data/rqt357_norm_equation.json`.

## Next natural bound — RQT-358

Implement a genuine arithmetic norm-equation solver with integrality-gate enforcement. An explicit nonzero triple `(L,M,h)` is admissible only if the norm is **exactly zero** under the identity, both congruences hold, and primitive reconstructed `u=T V z` verifies `u.T F4 u=0` and `gcd(F4u)=1`. Then apply RQT-334 and check RQT-257 Wall successor equations. The 3x3x3 cubit, Josophene/Juliet, time-angle and braces are provenance metadata only.
