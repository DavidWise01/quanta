# RQT-432 — The Pell Orbit Gate

Date: 2026-11-16. The candidate successor root19 lattice is the RQT-401 source Gram, conditional on frozen root18 predecessor compatibility.

## Conditional theorem

From RQT-431: for fixed integral x,y, the homogeneous target gives s²-Dd²=E0(x,y), D=-f>0 nonsquare, f=A22, s=fz+L(x,y), with z integral iff s≡L (mod D).

**Assume a first valid integer seed (s,d) exists**. Let u+v√D be a nontrivial positive Pell unit, u²-Dv²=1. Some positive power U+V√D is congruent (1,0) modulo 2D, because multiplication by a norm-one unit is invertible in the finite ring modulo 2D, so it has finite order. For that power set s'=Us+DVd and d'=Vs+Ud. Then s'²-Dd'²=E0, s'≡s≡L modulo D, d'≡d modulo2; hence z'=(s'-L)/f is integral and q(x,y,z')=-(d')². Each descendant must still pass primitive normalization and original F4 verification. This theorem **does not construct an original first seed or a unit for the actual 1352-bit D**.

## Executed exact controls

Synthetic A0=diag(1,1,-2), x=1, y=0: f=-2, D=2, E0=2, valid seed (s,d)=(-2,1), z=1. The norm-one unit (3,2) squared is (17,12), congruent (1,0) modulo4. Four verified generations:

| k | s | d | z |
|---|---:|---:|---:|
| 0 | -2 | 1 | 1 |
| 1 | -10 | -7 | 5 |
| 2 | -338 | -239 | 169 |
| 3 | -11482 | -8119 | 5741 |

Each satisfies q(1,0,z)=-d² and remains primitive. Deliberately invalid initial (-1,1) was rejected. This synthetic form is NOT the original RQT-401/F4 lattice.

## ASCII visual

```
       RQT-432 : PELL ORBIT GATE
      +------------------------------+
      |  s² - D d² = E0(x,y)        |
      |             |                |
      |      VERIFIED SEED ?        |
      |        NO      YES          |
      |        X        |           |
      |          Pell unit U,V       |
      |          (1,0) mod 2D        |
      |                 |            |
      |          s' = Us+DVd        |
      |          d' = Vs+Ud         |
      |                 |            |
      |         z' = (s'-L)/f        |
      |                 |            |
      |      exact norm + gcd       |
      |                 |            |
      |           ROOT19 OPEN       |
      +------------------------------+
```

Results: Conditional orbit theorem VERIFIED; original rational witness NOT CONSTRUCTED; integral root19 OPEN; root20 OPEN; root21 conditional. The generated JPG is conceptual and not independent source evidence.

Next: RQT-433 first-seed search or a fixed-pair modular obstruction. Avoid treating orbit closure as an original root.
