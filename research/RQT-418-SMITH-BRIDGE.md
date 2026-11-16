# RQT-418 — Four-Dimensional Smith Bridge

2026-11-16. Exact RQT-401 candidate-successor form; position-18 predecessor compatibility remains unverified.

## Four-variable form and new exact integer structure

The rational solution problem is q(w)=-d², q(w)=wᵀAw, A=Q/2, hence the homogeneous four-dimensional integral form H=diag(A,1) with (w,d)ᵀH(w,d)=0.

Executed the exact Smith normal form of H over Z. The invariant-factor magnitudes are:

  (1, 1, 9, |det(A)|/9).

The determinant has 3512 bits. All invariant factors divide the next. The Smith result is an equivalence of *integer linear presentations*, obtained by independent unimodular row and column operations. **It is not a congruence diagonalization H↦UᵀHU and cannot itself produce an isotropic vector.** No explicit rational or integer root has been constructed.

## Exact residue check for denominator prime 3

For each d modulo 9, enumerated every w∈(Z/9Z)^3 satisfying q(w)+d²=0 mod9. Counts:
- d=0,3,6: 243 total, 216 primitive mod3;
- d=1,2,4,5,7,8: 162 total and primitive mod3.

Thus a rational denominator divisible by 3 is **not excluded** by this local level. In particular, do not use the elementary divisor 9 to claim that d must be coprime to 3.

## Canonical ASCII story

```text
       RQT-418 : FOUR-DIMENSIONAL SMITH BRIDGE
     +-----------------------------------------+
     |        ORIGINAL F4 / RANK-THREE Q      |
     +-------------------+---------------------+
                         |
                      A=Q/2
                         |
                  H=diag(A,1)
                         |
               SMITH INVARIANTS
                  1 | 1 | 9 | N
                         |
              MOD 9 PRIMITIVE CHECK
                    /          \
                  3|d          3∤d
                   |            |
                216            162
            primitive         per d
               per d            |
                    \          /
                    RATIONAL?
                    NOT YET
                       |
                  ROOT19 OPEN
```

The calculation is performed on the exact full RQT-401 Gram and saved as research/RQT-418-results.json. RQT-414 rational existence remains valid but nonconstructive here. Root19 OPEN; root20 OPEN; root21 conditional. JPG and an embedded-JPG HTML are separately downloadable conversation artifacts. GitHub chapter preserves the ASCII diagram.

Next practical goal: an actual congruence-preserving constructive isotropic-vector algorithm (or exact integral-congruence reduction), followed by direct norm and Wall checks.