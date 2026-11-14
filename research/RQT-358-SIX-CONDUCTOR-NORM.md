# RQT-358 — Conductor-six saturation of both exact norm-equation lattices

**Status:** exact symbolic and integral lattice identities PASS; **no explicit isotropic integer u** and **no original roots18–21**.

## Authentic provenance and prior gates
Use original stoicheion RQT-242 frozen F4 (determinant independently checked), exact unimodular ternary transforms of RQT-355, and reversible norm equations from RQT-357. RQT-351 proves rational isotropy of slopes 194/195 and 201/202; RQT-353A establishes gcd(F4u)=1 for any primitive integer null vector on either plane. Neither fact constructs coordinates.

For `z=(x,h,y)`, let `A=V.T*T.T*F4*T*V`. Set the exact RQT-357 coefficients `p=-A00>0`, `q=-A02`, `r=-A22`, `g0=A01`, `g1=A21`, `D=pr-q²>0`, `gamma=p*g1-q*g0`, `N=det A>0`, and
```text
L=p*x+q*y-g0*h
M=D*y-gamma*h
D*L²+M²=p*N*h²                    (null equation)
```

## New exact conductor-six theorem
The integer linear map from `z=(x,h,y)` to `(L,M,h)` is
```text
S=[[p,-g0,q],[0,-gamma,D],[0,1,0]].
```
For both planes, the exact congruence is
```text
S mod 6 = [[0,1,0],[0,0,0],[0,1,0]].
```
Therefore any genuine integer ternary solution satisfies
```text
M ≡ 0 mod 6
L ≡ h mod 6.
```
These are **necessary constraints**, not sufficient membership in the full image. The Smith normal forms are
```text
194/195: diag(1,6,189121784129356422997125712400413503572266278463801140)
201/202: diag(1,6,508693049078183464833300572035915433798166277694409720).
```
The modulus six is exact for simultaneous coordinate congruences: `gcd(p,q,D,gamma,g0+1)=6` in both planes.

## Smaller exact integer norm form
Define new **integer** coordinates on the image
```text
X=(L-h)/6 ; Y=M/6 ; h=h.
```
Set `K=(p*N-D)/36`, which is integral in both planes. Substituting and dividing the RQT-357 equation by 36 gives exactly
```text
D*X² + (D/3)*X*h + Y² = K*h².
```
All coefficients here are integers (D divisible by three). The two complete coefficient sets are:

| slope | D | D/3 | K |
|---|---|---|---|
| 194/195 | 2020692228609206586199528939517571540 | 673564076203068862066509646505857180 | 181538912819953226244268332226037454348128578581486006901224151549700049 |
| 201/202 | 3272928109767528305742489923852754456 | 1090976036589176101914163307950918152 | 570193295558255279184424170139337225084055690319467080634399290819993584 |

The new linear map `R:z->(X,Y,h)` is integral and has determinant `-pD/36`. Thus this normalized equation is equivalent to `z.T*A*z=0` **when (X,Y,h) belongs to R*Z³**. A solution of the normalized equation *outside this finite-index sublattice* is not evidence for a genuine original-lattice null vector.

The verifier proves the full polynomial identity over symbolic coordinates:
```text
36*(D*X²+(D/3)*X*h+Y²-K*h²) = -p*D*(z.T*A*z)
                       when (X,Y,h)=R*z.
```
No numerical approximation or arbitrary search cutoff enters these results.

The lattice indices of R are
```text
194/195: 31520297354892737166187618733402250595377713077300190
201/202: 84782174846363910805550095339319238966361046282401620
```
so the residual integrality gate is substantial. The reduction divided the arithmetic norm equation by 36, not its fundamental Diophantine difficulty.

## Next natural target RQT-359

Apply a certified norm-representation / ideal-class algorithm to the normalized equation in the `R*Z³` sublattice; avoid searches that silently drop membership. Any recovered vector must pass `R^-1(X,Y,h) ∈ Z³`, `u=T*V*z∈ Z⁴`, `u.T*F4*u=0`, primitive content, and `gcd(F4*u)=1`, followed by exact RQT-334 norm-minus-two/allowed-parity and RQT-257 six Wall conditions. Until that happens, explicit original roots18–21 remain **OPEN**.

The 3×3×3 nested cubit, Josophene/Juliet and time-angle fields remain provenance metadata only.
