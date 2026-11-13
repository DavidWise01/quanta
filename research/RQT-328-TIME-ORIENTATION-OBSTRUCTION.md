# RQT-328 — Global time-orientation obstruction for the constructed bridge

**Verified scope:** constructed bridge F and X only. **Original frozen RQT-257 root 18–21 chain remains OPEN** because original F4 and X4 are unavailable.

## Exact matrices

```text
F = [-3  1  0  1]      X = [0 -1  0  0]
    [ 1 -2  0  0]          [1 -1  0  0]
    [ 0  0  1  0]          [0  0 -1  0]
    [ 1  0  0 -1]          [1 -1  0 -1]
```

The 3x3 restriction to indices (1,2,4) is negative definite: leading principal minors -3,+5,-3. The third basis vector e3=(0,0,1,0) has F norm +1 and is orthogonal to this negative 3-space. Thus signature(F)=(1 positive, 3 negative). The timelike cone q_F(x)>0 has two connected components, uniquely identified by the sign of x3.

## Root reflection fixes a future positive vector

For any *real* root r with r^T F r=-2, define S_r=I+r(r^T F) (correct minus-root reflection) and

```
w = e3 + (r3/2)r.
```

Then <r,w>_F = r3+(r3/2)*(-2)=0, so S_r w=w. Moreover w^T F w = 1 + r3²/2 > 0 and w3 = 1+r3²/2>0. Hence S_r fixes a future-component timelike vector and therefore preserves **both** positive-cone components (an isometry permutes the two connected components). Every product of negative-norm root reflections preserves the components.

But X e3 = -e3, so X interchanges the components. Therefore **no decomposition of this bridge X into any number of norm -2 reflections exists**, even over the real field. This is stronger than the specific RQT-327 three-step chain obstruction; no alternate negative-root-only path can succeed for the same X.

For the known bridge path, three norm -2 roots reach rank 1, and v=(0,1,2,0) has norm +2 and closes the chain via the positive-root formula S_v=I-v(v^T F). The positive-norm reflection flips the cone components, as required.

## Relation to spinor norm

Equivalently, in the real spinor-norm sign class, every negative-norm reflection contributes negative sign, every positive-norm reflection contributes positive sign. Spinor norm alone would preclude an *even* number of negative-norm reflections for a bridge X expressible as three negative plus one positive. The time-orientation argument is **stronger**: it forbids even or odd counts of exclusively negative reflections, because all such reflections preserve the future component. Keep this distinction; spinor norm and time orientation are different invariants.

## Do not transfer the claim to frozen F4, X4

The original root-18 target could have different real signature and orientation. Recover F4 and X4 from a verifiable frozen source, establish their signature, then evaluate whether X4 preserves the relevant cone. The original sequence also includes parity, divisibility, rank and binary order constraints that cannot be decided by the bridge proof.

## Reproduction and provenance

Run `python research/rqt328-time-orientation-obstruction.py` with SymPy. This checks the exact matrices, signature, positive vectors fixed by all three bridge reflections, and the +2 closing reflection.

Nested {brace[box(toroid)]} 3x3x3 geometry, nine named spatial addresses, Josophene j software hook, Juliet 1/2/3/5/8/13/21, and time/angle stamps remain evidence routing metadata, not independent roots. No hardware execution is claimed.

## RQT-329 next natural bound

Build a frozen-lattice preflight test that consumes **actual** F4,X4 and returns determinant, signature, orientation, real spinor-sign class where computed, binary order, and strict no-fabrication proof status. Distinguish hard mathematical obstruction from missing input.
