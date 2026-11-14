# RQT-354 — Two exact 3-adic null branches in original 199/200 plane

**2026-11-14 — Exact local arithmetic PASS; explicit integral isotropic coordinates and original roots 18–21 OPEN.**

## Research objective
RQT-351 established existence of rational isotropic points on three original ternary slices of the frozen RQT-242 F4. RQT-353A certified pairing divisibility one automatically for planes 194/195 and 201/202, but found a rank-two mod3 pairing map on the 199/200 plane. That leaves a possible factor 3 in `gcd(F4u)`.

Rather than mistake the existence of a mod3 null residue for an actual integral root, RQT-354 investigates this ambiguity through full **3-adic branch lifting** on the authentic 199/200 ternary Gram.

## Definitions
For integer ternary coordinates v=(a,b,c), map to original 4D coordinates `u=T v=(-199a,b,200a,c)`. Set `G=T^T F4 T`, `Q(v)=v^T Gv` and `M=F4 T`. The property `M v=0 mod3` means that the **corresponding original-lattice pairing divisibility is divisible by 3**. The opposite is the local divisibility-one branch with respect to p=3, not proof that global gcd=1 unless all other determinant primes are also handled (RQT-353A handles those other primes).

At every exponent k from 1 through 30, enumerate all 27 ternary digits d in {0,1,2}^3, and retain `v+3^k d` when `Q(v+3^k d)=0 mod 3^(k+1)`. Preserve the base mod3 residue; verify every norm condition exactly.

## Two witnessed local branches
1. The primitive seed `v=(1,0,0) mod3` is in the mod3 pairing kernel: `F4 T v=0 mod3`. It has **27 possible lifts modulo9**, of which exactly **six** have an additional lift modulo27. The naive representative (1,0,0) itself dies at the next level; the program explicitly checks this pitfall. Selecting at each stage a branch having a further descendant produces an explicit compatible residue `v_3 mod 3^31` with `Q(v_3)=0 mod 3^31` and `F4 T v_3=0 mod3`.
2. The primitive seed `v=(0,1,1) mod3` has `F4Tv !=0 mod3` and a smooth mod3 null condition. Ordinary Hensel lifting gives an explicit compatible residue `v_1 mod3^31` with `Q(v_1)=0 mod3^31` but `F4Tv_1 !=0 mod3`.

These are **two local arithmetic witnesses** with different pairing-divisibility behavior. They do not prove either is a rational, globally integral, or exact isotropic vector. A finite chain of residues does not automatically certify an infinite singular p-adic lift; the smooth d1 branch does have the usual Hensel guarantee, while the d3 branch is evidenced only to the reported precision.

## Mathematical conclusion
The 3-primary ambiguity for the 199/200 plane cannot be dismissed by the shallow norm-congruence screen through modulo27: both pairing branches have representatives at arbitrarily many **tested finite levels**, here through `3^31`. This does not change the stronger **global divisibility-one theorem already established for planes 194/195 and 201/202**.

A generic SymPy ternary solver was attempted again on the two previously certified rationally isotropic planes and did not return a solution in the bounded execution window. That timeout is not mathematical evidence of nonexistence.

## Reproduction
Run `python research/rqt354-3adic-dual-lifts.py` with SymPy. It is self-contained: original frozen F4, original ternary map, exact norm, 27-digit branching, assertions for the six surviving mod9-to-mod27 paths, and both explicit final mod3^31 residues with full branch choice counts.

## Next RQT-355
Direct effort to constructing **an exact rational/null vector** on 194/195 or 201/202 using an arithmetic ternary isotropy algorithm (e.g. a certified conic/ideal descent). Repeating modular precision on 199/200 cannot by itself produce a genuine original root18. Once a primitive exact integer u is obtained, use the RQT-353A d1 theorem and RQT-334 exact Bézout construction, then audit the RQT-257 Wall flag for roots19–21.

**Evidence ancestry:** frozen stoicheion F4 is one source; two 3-adic branches are derived calculations, not independent original source ancestries. 3×3×3 nested cubit, Josophene/Juliet and time-angle coordinates remain metadata.
