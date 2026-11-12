# RQT-325 — Primitive rays of the full bridge tangent cone

**Status:** Exact integral-ray normalization and bounded parameter enumeration verified for the **constructed bridge lattice only**. The actual frozen eighteenth root is **OPEN**.

## 1. Algebraic cone

For p=(1,0,0,1) and the RQT-307 bridge Gram F, any root-line direction v=(a,b,c,d) must obey b=2a and

```
c²-(d-a)²=6a².
```

A rational projective parametrization is

```
w(m,n) = (2mn, 4mn, 6m²+n², 6m²-n²+2mn)
```

for rational homogeneous parameters [m:n]. The two a=0 rays appear at m=0 and n=0. For coprime integers (m,n), not both zero, the displayed w is integral but not necessarily primitive.

## 2. Exact ray normal form

Define g=gcd(|w_1|,...,|w_4|) and u=w/g. Choose orientation such that the first nonzero component of u is positive. Then u is a primitive integer vector on the isotropic cone. The complete set of **even** integral vectors on that rational line is

```
v_k = 2k u,  k in Z.
```

An affine root family is r_k=p+2k u. The rational projective parameter identification (m,n)~(-m,-n) means a pair and its negative represent the same direction, even before normalizing by g. Distinct primitive u identify distinct *lines through this chosen p*, but do **not** classify orbits under the full integral isometry group.

## 3. Finite replay

Enumerate all coprime integer (m,n) in [-8,8]² excluding (0,0):
- 176 parameter pairs.
- 88 distinct unoriented primitive rays (every ray appears twice from (m,n) and (-m,-n)).
- 86 rays have a nonzero first component a, so are outside the old a=0 two-line slice.
- Raw content g distribution across 176 parameter pairs: g=1:90; g=2:48; g=3:24; g=6:14.
- Every ray is checked at seven values of k=-3,-2,-1,0,1,2,3: 616 root checks. For each, norm -2, divisibility one, parity 1001, rational rank 4→3 and binary order 3→2 pass.

This is a **finite parameter-window result** with symbolic proof of the underlying cone/normalization, not a claim that the set of all rays is finite.

## 4. Primitive and parity preservation

v=2u is even, so every p+kv keeps parity 1001. Along all these directions (F r)_1+(F r)_4=-2 and (F r)_2 is odd; hence gcd(F r)=1. B=-6F in this bridge, so the six quadratic conditions hold. Exact order in F2 only depends on root parity.

## 5. Nested tensor index and provenance

The nested {brace[box(toroid)]} unit remains 3×3×3 with face/edge/corner motion and spatial index fields rur/rc/rll, cu/c/cl, fur/fcr/flr. Josophene is the quantum-hardware to Quanta-software hook; no hardware evidence was used. Juliet contains the 1,2,3,5,8,13,21 progression. Time includes year:month:day || hour:minute:second || degree.arcminute.arcsecond. Each primitive u is an ancestry-preserving family identifier, not an independent witness of the frozen root.

## 6. Reproduce

Run `python research/rqt325-primitive-cone-rays.py` (SymPy required).

## RQT-326 — next natural bound

Classify whether two distinct primitive rays become equivalent under actual **integral isometries** of F that stabilize the base root p (or act on the entire root family). Require an explicit isometry U with U^T F U=F and appropriate U p=p before merging families. Do not collapse distinct rays based solely on matching invariants.

Frozen RQT-257 matrices F4 and X4 are not available; do not transplant the bridge classification into the original root-18 claim.
