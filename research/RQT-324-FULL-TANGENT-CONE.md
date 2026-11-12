# RQT-324 — Full even isotropic tangent cone

**Status:** symbolic proof and finite regression on constructed bridge lattice. **Original frozen eighteenth root remains OPEN.**

For bridge Gram F = [[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]], X = [[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]], and base p=(1,0,0,1), define D=X-I and B=sym(F adj(D)). Direct calculation: det D=12, B=-6F.

For an integral affine direction v=(a,b,c,d), p^T F v=0 gives **b=2a**, while v^T F v=0 becomes

```text
c²-(d-a)²=6a².
```

This is a rational quadratic cone rather than just two lines. In the fixed primitive-coordinate slice from RQT-323 one additionally imposes (Fv)_2=0, forcing a=0 and c=±d; that slice restriction is now removed.

## Rational projective parametrization

Set a=2mn, c=6m²+n², d=6m²-n²+2mn and b=2a. This parametrizes rational rays up to overall nonzero rational scale (including the limiting ray m=0). To force even integral directions choose

```
v(m,n)=2*(2mn,4mn,6m²+n²,6m²-n²+2mn)
```

for integer m,n. This gives infinitely many integral directions but is **not** a claim that every even integral vector is expressed with integer m,n without scaling; classification is via the cone equation.

## Stronger divisibility invariant

For any even integral direction v satisfying the tangent/null constraints, let r_k=p+k v. The vector F r_k always satisfies

```text
(F r_k)_1 + (F r_k)_4 = -2
(F r_k)_2 = 1 - 3 k a   (odd for every integer k since a even).
```

Thus gcd(F r_k) divides 2 and is odd, forcing gcd=1 for all k. Parity is constantly 1001. Six quadratic line conditions hold (since B=-6F), so norm -2 and rational moving rank 4→3 persist. Mod2 successor reflection is constant and has order 2; X mod2 order 3.

## Verified finite experiment

Enumerated a,c,d even in [-14,14], with b=2a and the exact cone condition: **45 directions** including zero. Each tested for k=-2,-1,0,1,2: **225/225 exact replay cases passed**. Crucially a nonzero-a direction exists: v=(-4,-8,-14,-14), outside the former restricted slice. First search over [-6,6] had missed all nonzero-a directions; finite bounds do matter.

Run `python research/rqt324-full-tangent-cone.py` with SymPy.

## Provenance

Hardware/software Josophene hook, Juliet generation gates, spatial 3×3×3 cubit, and nested brace/box/toroid/time record carry *addresses and evidence* and are not substitutes for lattice proofs. Neither the bridge F nor bridge X is the original frozen RQT-256 pair.

## RQT-325 — next natural bound

Classify even integral directions via primitive rational projective slopes and exact scaling factors; identify which produce genuinely distinct root lines modulo sign and lattice isometries. In the actual RQT-257 lattice the analogous classification requires frozen F4 and X4.
