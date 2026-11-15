# RQT-382 — The Isotropic Forge: 800 million exact two-coordinate plane tests

**2026-11-14 | RQT-382 | Roots 18–21 remain OPEN.**

## Goal and story

The exact norm-minus-two construction in RQT-381 requires a primitive original integer isotropic vector `u` with `u.T F4 u=0` and pairing divisibility `gcd(F4*u)=1`. Two prior rationally isotropic planes, 194/195 and 201/202, are candidates for constructing such a vector. The new JPG chapter `RQT-382-Isotropic-Forge.jpg` depicts those two planes feeding an unopened root18 forge through a Bézout bridge. This is conceptual artwork, not a representation of verified integer coordinates. The JPG is available in this conversation, but **has not been uploaded into GitHub**; this executable and research report are committed to `DavidWise01/quanta`.

The new research is a fully exact direct search for integral null vectors on BOTH ternary planes. Rather than put a small bound on all three coordinates, **only two coordinates (x,y) are bounded; h is solved algebraically and unrestricted**.

## Original frozen source and unimodular charts

Frozen F4/H4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, exact identities `H4+H4.T=-F4`, `det(H4)=1`, and

```text
det(F4)=-8281492574115056973770683990411769007319047636247715225543944839911172.
```

For slope m/n define the integral 4×3 plane embedding
```text
T(m,n)=[[-m,0,0],[0,1,0],[n,0,0],[0,0,1]].
```
The two unimodular 3×3 coordinate changes are

```text
V194 = [[1,3,1],[-25,-74,-24],[113,340,113]]
V201 = [[1,2,1],[-26,-51,-25],[117,235,117]]
det(V194)=det(V201)=-1.
```

Define the exact ternary forms `A=V.T*T.T*F4*T*V`. Their coefficients are embedded in `research/rqt382-isotropic-cylinder.cpp`, and the independently executed SymPy verifier reconstructs and checks every coefficient against the original four-dimensional F4. Thus the search includes every integer vector on either plane with the specified two reduced coordinates; no rational scaling or unverified substitute Gram is used.

## Exact discriminant with h UNBOUNDED

Let `z=(h,x,y)`. The original-plane integer null condition is

```text
0 = z.T A z = A00*h² + 2*(A01*x+A02*y)*h
                         + A11*x²+2*A12*x*y+A22*y².
B=A01*x+A02*y
C=A11*x²+2*A12*x*y+A22*y²
D=B²-A00*C.
```

For ANY integer h to solve the equation, D must be a nonnegative perfect integer square and at least one numerator `-B±sqrt(D)` must be divisible by `A00`; then `h=(-B±sqrt(D))/A00` is checked by directly evaluating `A00*h²+2B*h+C=0`.

The square test is first performed with an exact integer modular-residue sieve using 12 moduli:
```text
256,3,5,7,11,13,17,19,23,29,31,37.
```
For each modulus m precompute exact quadratic residues and the three reduced coefficients
```text
K00=A01²-A00*A11
K01=A01*A02-A00*A12
K11=A02²-A00*A22
D=K00*x²+2*K01*x*y+K11*y².
```

The sieve only rejects nonsquare residues; all surviving discriminants are evaluated and square-tested using **arbitrary-precision Boost cpp_int**. Thus there are no floating-point square tests or false-negative sieve exclusions. The trivial pair (x,y)=(0,0) is excluded: because A00≠0, it yields only h=0.

## Executed, complete exact search cylinder

Compile `g++ -O3 -std=c++17 research/rqt382-isotropic-cylinder.cpp -o rqt382` and run `./rqt382 10000`. This enumerates all 20001² coordinate pairs for each original plane:

| Plane | Total pairs including zero | Nonzero pairs | Pass modular sieve | Nonnegative exact D | Perfect-square exact D |
|---|---:|---:|---:|---:|---:|
| 194/195 | 400040001 | 400040000 | 570968 | 254230 | **0** |
| 201/202 | 400040001 | 400040000 | 2301092 | 1064540 | **0** |
| Combined | 800080002 | 800080000 | 2872060 | 1318770 | **0** |

**Certified exact finite statement:** For each of these two reduced integral ternary planes, a nonzero integer isotropic `u=T*V*(h,x,y)` must satisfy `max(|x|,|y|)>=10001`. The third coordinate h is not bounded. This is a necessary lower bound in the **specific recorded unimodular ternary charts**, not an absolute coordinate-size lower bound across all bases.

The earlier reported RQT-356 bound involved a different coordinate being small, so do not conflate the two independently bounded searches. The prior RQT-351 rational-isotropy claim remains logically compatible: rational isotropic vectors may have extremely large primitive integer coordinates.

## Independent verification

The independently executed `research/rqt382-verify-original-plane-charts.py` rebuilds F4/H4/T/V/A from integers and verifies the original determinant and Wall relation, unimodularity of both V, exact transformed Gram matrices, and **5000 seeded random triples per plane**, including exact original four-dimensional norm and exact discriminant polynomial identities modulo each of the 12 filters. All 10000 cases passed.

An attempted generic SymPy ternary solver on 194/195 using the reduced A was capped at 22 seconds and did not return a point; a timeout **does not** prove impossibility. The exact exhaustive cylinder result above is independently valid and substantially stronger than a mere timeout within its stated coordinate bounds.

## The proof standard and next natural target — RQT-383

No explicit primitive null vector was produced. No authentic original `r18` or roots19–21 were produced. The RQT-381 conditional Bézout formula, RQT-377 exact Wall-kernel ladder, and RQT-379 forced last-root theorem remain pending a genuine integer `u` or `r18` coordinate witness. Even after a norm-minus-two vector is obtained, verifying its identity as the eighteenth reflection requires the actual original frozen 17-reflection factorization/order check. Keep all 27 cubic GMA spatial cores and narrative JPGs, but prefer a **true constructive ternary isotropic solver**, such as a certified rational conic parametrization, over only increasing finite coordinate bounds.

**Roots 18,19,20,21 = OPEN. The null-vector forge is still waiting for its first exact coordinate witness.**
