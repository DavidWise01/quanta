# RQT-351 — Hasse–Minkowski rational isotropy certified for three authentic planes

**Status: exact theorem hypotheses verified; three rational isotropic planes PROVED. Explicit integer coordinates and original roots 18–21 remain OPEN.**

## Source
Authentic frozen rank-four symmetric Gram F4: `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. The executable self-contained checker is `research/rqt351-local-global-rational-isotropy.py` in `DavidWise01/quanta`. Unlike previous finite congruence survivals, these statements invoke the Hasse–Minkowski local-global theorem for nondegenerate ternary quadratic forms over Q.

## Full-rank ternary planes

For each rational slope m/n, write x=(-ma,b,na,c), with integer 4x3 map T. The ternary Gram G=T^T F4 T is nondegenerate. The three newly proven rationally isotropic planes are:

```text
194/195    (x0/x2=-194/195)
199/200    (x0/x2=-199/200)
201/202    (x0/x2=-201/202)
```

**Exact complete factorization of |det(G)|** (all displayed large cofactors verified prime by SymPy):

```text
194/195: 2² · 281297 · 10343190029259773932231107365537334388821979446373

199/200: 2² · 3² · 7 · 75530352283322907062836197087153453231862314058622987

201/202: 2² · 12967 · 424379617890791758503212431701229981571028039802163
```

## Every completion gate

1. **Real place.** The eliminated (x1,x3) Gram block is negative definite, while the exact Schur maximum for fixed (x0,x2)=(-m,n) is positive for each case. Hence each G has both signs, and a nonzero real isotropic vector.

2. **Prime 2.** For each G, the primitive ternary seed v=(0,1,1) has Q(v)=v^T Gv divisible by 8 and (Gv)_i odd for some index i. Shifting v by successive 2^k multiples of that coordinate toggles the 2^(k+1) digit of Q for k>=2, extending the primitive solution to every 2-adic precision.

3. **Odd primes dividing det(G).** All exponent-one factors have nonzero leading binary determinant h mod p with -h a quadratic residue. Their rank-two quotient is split; a nonzero, smooth mod-p isotropic vector exists and lifts by Hensel. The special p=3² for slope 199/200 has a direct smooth seed (0,1,1) mod3.

4. **Other odd primes.** For p not dividing the determinant, G is nondegenerate ternary over F_p. Every nondegenerate ternary form over an odd finite field has a nontrivial isotropic vector, which is nonsingular and lifts to Q_p.

By **Hasse–Minkowski**, these local solutions at all completions certify the existence of nonzero **rational** isotropic vectors in all three planes.

## Exact status boundaries

- PROVED: rational null vectors **exist** in each of the three planes above, and their projective coordinates can in principle be scaled to primitive integer ternary vectors.
- NOT PROVED: an explicit coordinate vector, pairing divisibility one, allowed root18 parity, four-root Wall orthogonality, or the complete 21-reflection product.
- Prior RQT-350: 25 of the 31 planes are excluded by other certified local obstructions.
- Remaining **undecided** slopes: `188/189`, `192/193`, `851/850`. A large unresolved composite cofactor or absence of a local no-go certificate must not be mistaken for a rational witness.

## Next RQT-352

Construct explicit rational isotropic coordinates in one of the *proven* planes using an exact conic solver (e.g. quaternion norm splitting / LLL with a proof), then clear denominators, primitive-normalize, check u^T F4 u=0 and gcd(F4 u)=1, and use the existing RQT-334 Bézout/parity gate to attempt authentic root18. Keep all original roots18–21 OPEN until independently checked integral witnesses exist.

The 3×3×3 cubit, {{i}}/{{j}}/{{n}} and time-angle indexing are metadata only. All three derived certificates have the same original F4 source ancestry.
