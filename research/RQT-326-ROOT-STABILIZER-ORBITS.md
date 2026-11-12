# RQT-326 — Exact bridge-lattice stabilizer subgroup

**Scope:** Explicit, verified subgroup of integral isometries fixing the chosen bridge root. **Not** a classification of all lattice isometries or of the unrecovered frozen root 18.

## Setup

Bridge Gram and original transformation are the RQT-307 construction:

```text
F=[[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]]
X=[[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]]
p=(1,0,0,1)
```

## Explicit isometries

```text
C = [1 0  0 0]      T = [1 0 0  0]
    [0 1  0 0]          [0 1 0  0]
    [0 0 -1 0]          [0 0 1  0]
    [0 0  0 1]          [2 0 0 -1]
```

Direct matrix tests give C^T F C = F, T^T F T = F, Cp=Tp=p, det(C)=det(T)=-1, C²=T²=I, CT=TC. Thus G={I,C,T,CT} is a Klein four subgroup of the root stabilizer. In tangent coordinates v=(a,2a,c,d), C flips c, while T sends d to 2a-d; equivalently the two independent signs of c and (d-a) can change. Every member acts integrally on the entire bridge lattice, not only the tangent cone.

A sample primitive ray (2,4,7,7) has a certified four-element subgroup orbit:

```text
(2,4, 7, 7)
(2,4,-7, 7)
(2,4, 7,-3)
(2,4,-7,-3)
```

Each associated affine root line is r_k=p+2k v with parity 1001.

## Critical distinction: geometry versus fixed X

An F-isometry U conjugates root reflections, U S_r U^-1 = S_{Ur}, but it need not commute with the *fixed* X. Therefore root-reflection rank/order success does not automatically transport to a general fixed-X problem. The script independently verifies all five conditions for every generated bridge ray. Here B=-6F makes the rational rank-drop equation automatic for norm -2 and parity 1001 controls the mod-2 order, so the entire subgroup orbit stays certified.

## Finite parameter window and exact closure

Starting with the 88 unoriented primitive rays obtained from coprime (m,n) in [-8,8]²:
- 62 additional rays appear when taking the closure under G.
- The resulting **150** primitive rays split into exactly **38 subgroup orbits** (37 of size four, 1 of size two).
- All 150 rays are checked for k=-2,-1,0,1,2, i.e. **750** exact root-reflection verifications.
- The original 88-ray parameter window was not closed under even this small symmetry subgroup, so directly dividing 88 by four would be incorrect.

No claim that these 38 are the global isometry classes of all rational tangent rays. Larger isometry groups may relate distinct G orbits.

## Provenance and nested tensor

The {brace[box(toroid)]} 3×3×3 tensor (1 center, 6 faces, 12 edges, 8 corners) indexes search/evidence. Josophene is the hardware/software hook; these observations are software-only. Juliet carries its 1,2,3,5,8,13,21 gates. Preserve nine spatial addresses and year:month:day || hour:minute:second || degree.arcminute.arcsecond without inventing values.

## Reproduction

`python research/rqt326-root-stabilizer-orbits.py` (requires SymPy).

## RQT-327 next bound

Search for and certify extra root-stabilizing integral isometries of F using a bounded height search. Distinguish a subgroup-orbit merge (explicit U) from an undecided match. To make progress on the actual eighteenth-root problem, recover frozen F4 and X4 first.
