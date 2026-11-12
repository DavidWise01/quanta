# RQT-323 — Two exact root-line families in the bridge lattice

**Status:** Verified classification *within a fixed primitive-coordinate slice*. The original frozen eighteenth-root witness remains OPEN.

## Input

F = [[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]]; X = [[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]]. Set D=X-I, B=(F adj(D)+adj(D)^T F)/2, p=(1,0,0,1).

## Problem

Find **even** integral direction vectors v=(a,b,c,d) such that p^T F v=p^T B v=v^T F v=v^T B v=0 and the second coordinate of Fv is zero. The latter preserves the fixed primitive certificate (Fp)_2=1 for all p+t v.

## Classification

Here B=-6F. The linear equations become -2a+b=0 and a-2b=0, forcing a=b=0. Then v^T F v=c²-d²=(c-d)(c+d)=0, hence c=d or c=-d. Requiring even coordinates gives exactly

- v_+(t)=(0,0,2t,2t)
- v_-(t)=(0,0,2t,-2t)

for arbitrary integer t. Each generates a family r_±(t)=p+v_±(t) with norm -2, divisibility one, parity 1001, rank_Q((I+r(r^T F))X-I)=3 and exact mod-2 order 2, starting from X mod-2 order 3.

The two lines meet at t=0 and are exhaustive **only under the displayed fixed primitive-coordinate condition**, not for all possible root families or embeddings.

## Test

Run `python research/rqt323-two-root-lines.py` with SymPy. It verifies the symbolic constraints and 62 individual cases, 31 per branch for t=-15...15.

## Provenance and nested indexing

Append-only evidence; hardware/software junction Josophene is conceptual here and not a source of hardware measurements. A 3×3×3 unit can index search states with face/edge/corner paths, while the four-dimensional mathematical proof remains attached separately. Juliet retains 1,2,3,5,8,13,21. Address structure retains brace/box/toroid and time/angular slots.

## RQT-324 natural bound

Remove the fixed-primitive-coordinate restriction safely: analyze the full rational tangent hyperplane p^T F v=0 and its isotropic cone, then test which integral even directions admit divisibility-one certificates across an entire family. Distinguish a rational conic parametrization from an integer-lattice classification. Original RQT-257 F4 and X4 still unavailable.
