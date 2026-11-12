# RQT-327 — Return to the 18th–21st reflection chain

**Status:** Exact three-step chain and fourth-step obstruction in the **constructed bridge lattice**. The original frozen RQT-256 matrices F4/X4 were not recovered from GitHub or the prior RQT-258/259 source scripts. The **original roots 18–21 remain OPEN**. No bridge root is presented as a frozen-lattice witness.

## Original target

For the original rank-four residual X4, find integral norm -2, divisibility-one roots (starting with permitted parity classes 0111,1001,1110) giving consecutive exact reflections down from rational moving rank four. Every step needs its own norm, gcd, parity/2-adic status, rank and successor Gram-isometry checks. Never infer a later step from an earlier parity class.

## Exact bridge example (det F=-3; not original frozen F4)

F = [[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]]; X17=[[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]]. X17 is a Gram isometry, moving rank 4, and mod-2 order 3.

With S_r=I+r(r^T F), the chain is:

- r18=(1,0,0,1): norm -2, gcd(F r18)=1, rank(X18-I)=3 and X18 mod2 order 2.
- r19=(0,-1,-1,-1): norm -2, gcd=1, X18 r19=-r19, rank(X19-I)=2.
- r20=(0,-1,-1,1): norm -2, gcd=1, X19 r20=-r20, rank(X20-I)=1.

All successors preserve F and square to I (in this particular bridge chain). Exact final matrix:

```text
X20 = [[ 1, 0, 0,0],
       [-1, 3,-2,0],
       [-2, 4,-3,0],
       [ 0, 0, 0,1]]
```

## Step 21 obstruction for **this chain**

The -1 eigenspace of X20 is the rational line spanned by v=(0,1,2,0), with v^T F v=+2. Every integral vector in that line is t v and has norm +2t², never -2. Since a rank-one involution X20 can be removed by one reflection only using that -1 eigendirection, there is no fourth norm -2 reflection on this chosen bridge path. A +2 reflection using S_plus=I-v(v^T F) satisfies S_plus X20=I. It is not an admissible norm -2 root.

**This does not establish a global impossibility:** a different choice of earlier roots might have a different successor, and the actual frozen lattice is not this bridge.

## Source recovery and provenance

Connected GitHub searches for the frozen determinant, RQT-256 and 'eighteenth' did not find the numerical original matrices. Earlier RQT-258/259 scripts expect external JSON containing F4 and X4 and do not embed them. The future frozen-root search must consume original values from a verifiable source and carry a source commit/hash before claiming certification.

Nested 3x3x3 {brace[box(toroid)]} geometry, nine spatial addresses, Josophene software junction and Juliet gates are maintained as **search/evidence metadata**, not substituted for exact reflection checks.

## Run

`python research/rqt327-bridge-chain-and-rank1-obstruction.py` with SymPy.

## Next natural bound — RQT-328

Derive the exact *rank-one sign obstruction* for all four-step chains, and test the reflection/spinor-norm invariant of the starting isometry. If no-four-negative-reflections can be certified for the bridge, explain why the norm +2 final reflection is forced; keep original frozen F4/X4 state OPEN pending source recovery.
