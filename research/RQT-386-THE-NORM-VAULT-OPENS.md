# RQT-386 — The Norm Vault Opens: first explicit original F4 null vector and norm-minus-two reflection candidate

**2026-11-14 | BREAKTHROUGH | Exact original integer arithmetic PASS.**

The long-running **global norm-representation** obstruction is now solved constructively for plane **194/195**. This is **not yet a proof that the constructed reflection is number 18 of the original frozen 17-reflection factorization**; position and order must be checked independently. Roots19–21 remain open.

## Original integer null vector, now explicit

The following four signed integer coordinates are a **primitive exact null vector** of the unchanged original frozen RQT-242 F4:

```text
u0 = -855940091954473592321985452134670371913557752494031206262329291541629429577366216
u1 = -108556935070691544442477999242419589194498839774905557178241309621234287399243907
u2 =  860352154284135827333954449310622281047132792455340645469867071394936797771063980
u3 =  499120656477344840496337305046979169784145148428365286490946823795764785202610093
```

Independently certified, by computing exact products with the frozen original F4:

```text
u.T F4 u = 0
gcd(u0,u1,u2,u3) = 1
gcd(F4*u) = 1
```

These are real integers, not a rational-only solution, modular lift or synthetic test form.

## Exactly constructed norm-minus-two reflection candidate

A Bézout partner `v∈Z4` was computed with `u.T F4 v=1`, preserving root parity `0111`. Define `q(v)=v.T F4 v /2`, then

```text
r = (1+q(v))*u - v.
```

The exact original F4/H4 identities certify:

```text
r.T F4 r = -2
r.T H4 r = 1
r mod2 = 0111
gcd(r) = 1
```

The integral reflection `S=I4+r*(r.T F4)` is an involution, satisfies `S.T F4 S=F4`, and has determinant **−1**. It is thus a **genuine original-lattice reflection root candidate**. Its coordinates are long (approximately 488 decimal digits each); the self-contained GitHub Python executable prints every integer exactly, and the complete full-coordinate JSON file was delivered as a downloadable conversation artifact.

**Critical naming:** This is an explicit norm−2 vector with admissible first-root parity, **NOT CERTIFIED AS REFLECTION NUMBER 18**. The frozen 17-reflection product and successor rank/order criteria have not yet been checked. No root19/root20/root21 is asserted.

## How the vault was opened

RQT-385 completely factored the 194/195 norm target:

```text
C = 24 P
P = 223 * 281297 * 419697635024167
  * 10343190029259773932231107365537334388821979446373.
Delta = 505173057152301646549882234879392885.
```

For every one of 16 CRT sign branches, construct the full-rank integer lattice of pairs `(M,B)` satisfying

```text
M ≡ root * B (mod P),
M² + Delta B² = C h².
```

The lattice basis is `(P,0)` and `(root,1)`, with positive-definite inner product `<x,y>=x_M*y_M + Delta*x_B*y_B`.

**Exact two-dimensional Gauss reduction** returns bases `(e1,e2)` obeying

```text
||e1||² ≤ ||e2||²,
2*|<e1,e2>| ≤ ||e1||².
```

By the classical two-dimensional Gauss reduction theorem, e1 is a shortest nonzero lattice vector. For any nonzero integer null-vector solution satisfying the conic norm equation, it follows that

```text
C h² = M²+Delta B² >= min_branch ||e1||²
=> |h| >= 82,629,670.
```

This exact lower bound explains why the earlier small-coordinate searches did not recover a seed. It is an **unbounded consequence** of the 16 branch lattices (for the normalized reduced ternary coordinate h), not an absence proof.

Next, in the all-positive CRT branch, the reduced pair lattice norm divided by P has small exact 2D coefficients:

```text
664902061348876241 * alpha²
- 581109485265281976 * alpha*beta
+ 886739792056772469 * beta²
= 24 h².
```

SymPy's constructive ternary quadratic solver returned an **exact integer solution**:

```text
alpha = 474649450978634736175766122678998
beta  = 222309235551026216137681687722434
h     = 74247063525679595379713821277894166492373.
```

The verifier independently checks that equation and reconstructs integer `M,B` in the CRT lattice. It then inverts the earlier RQT-357/360 norm transformation **over the rationals**:

```text
L = B/2
y = (M+gamma*h)/D
x = (L+g0*h-q*y)/p
```

IMPORTANT: the ternary coordinate vector used with RQT-352 matrix A is **z=(x,h,y)**, not (h,x,y). Clear all rational denominators, divide by the coordinate gcd, and form the original integer four-vector `u=T194*V194*z`. The verifier evaluates `u.T F4 u=0` directly, without relying solely on the norm-equation identity.

Finally, RQT-381's Bézout-plus-parity bridge produces the above explicit norm-minus-two reflection candidate.

## Independent evidence and successor step

A separately written verifier, without using the reconstruction's functions, directly checks the full JSON coordinate witness, original F4 and H4 products, parity, primitive content and reflection involution. **It passed.**

The RQT-377 exact integer Wall-kernel ladder was also run using the new explicit candidate and gave a **saturated rank-three integer kernel** for a possible successor root19 (conditional on this candidate genuinely being reflection18). Its reconstructed restricted rank-three Gram is exactly symmetric and its Wall constraint checks to zero. The rank-three basis and Gram, which contain very large coefficients, are available in a separate conversation JSON artifact. **No root19 was recovered**.

## Artifacts, provenance and image

- GitHub: `research/rqt386-exact-null-and-root-candidate.py` (standalone reproducer, prints all exact coordinates)
- GitHub: `research/rqt386-verify-original-root-candidate.py` (independent verifier consuming emitted JSON)
- Conversation: `RQT-386-Exact-Root-Candidate.json` (full explicit exact-coordinate certificate, including all 16 CRT reduced branches)
- Conversation: `RQT-386-Root19-Conditional-Kernel.json` (saturated 3D Wall successor lattice)
- Conversation: `rqt386_norm_vault.py` (complete local executed 16-branch source)
- Conversation: `rqt386_verify_independent.py` (independent direct check)
- Visual chapter: `RQT-386-Gauss-Reduction-Vault.jpg` — the 27 cubic GMA cores, 16 CRT gates and opening vault are conceptual narration, not a plot of exact lattice coordinates. The JPG is supplied in this conversation, not binary-committed in GitHub.

The source ancestry is the same frozen stoicheion F4; independent implementations and checks are separate computational witnesses, **not independent original source ancestries**.

## RQT-387 — next true research target

**First:** recover the original frozen 17-reflection product/canonical order and test whether this actual norm-minus-two reflection qualifies as **root18**. If not, use the new explicit root as a genuine F4 norm witness and continue the factorization-compatible search; do not call it eighteenth by parity alone.

**Second:** use the saturated rank-three Wall kernel to seek a norm-minus-two root19; then its rank-two successor root20; root21 is forced by the RQT-379 cofactor theorem if the first three complete a valid Wall flag.

The original **existence of an integral norm−2 root is now demonstrated**, while the requested position-specific roots18–21 remain unresolved pending the frozen predecessor and further Wall equations. Keep the nested nine-generation `{{9×9×9}}^9` GMA with central `||||`, and tell the next chapter through a JPG.
