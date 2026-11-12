# RQT-322 — Affine root-line certificate

**Status:** Exact theorem and executable example, **bridge lattice only**. The frozen original eighteenth-root matrices F4 and X4 remain unrecovered.

Given integral symmetric nonsingular F and integral isometry X with D=X-I nonsingular, define B=(F adj(D) + adj(D)^T F)/2. An integral root p and nonzero even direction v generate r_k=p+kv for all integers k. S_r=I+r(r^T F), Y_r=S_r X.

## Six quadratic conditions

If p^T F p=-2, p^T B p=det D, p^T F v=v^T F v=p^T B v=v^T B v=0, then q_F(r_k)=-2 and q_B(r_k)=det D for all k. Consequently rank_Q(Y_r-I)=3: determinant lemma gives rank ≤3, and rank-one perturbation of invertible D gives rank ≥3.

If v is even and p's parity is an admissible class for which Y_p mod2 has order 2 while X mod2 has order 3, then the same order conditions hold for every k (all r_k share parity). To ensure divisibility one for all k, it suffices to find a fixed coordinate j with (F p)_j=±1 and (F v)_j=0. Nonzero v makes the family unbounded.

## Exact bridge inputs

F=[[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]]; X=[[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]]. Set p=(1,0,0,1), v=(0,0,2,2). Direct exact evaluations: det D=12; B=-6F; q_F(p)=-2; q_B(p)=12; all four cross/direction quantities vanish. Fp=(-2,1,0,0); Fv=(2,0,2,-2); hence fixed primitive coordinate j=2 (1-based). The reflection successor has rank 3 and mod-2 order 2; X mod2 has order 3. The family has parity 1001 and passes all five bridge tests for every integer k.

## Boundary

This does not prove that the original frozen RQT-257 lattice admits an eighteenth root or an affine family. A failure to find v does not imply a finite root set: this is a sufficient family certificate, not a complete classification of infinite solutions.

The spatial indexing of the 3×3×3 nested cubit, Josophene j hardware/software hook, Juliet gate progression and the brace/box/toroid/time address are metadata and routing; do not substitute for exact matrix checks.

## Reproduction

Run `python research/rqt322-affine-line-certificate.py` with SymPy. Proof checks are symbolic; additionally tests k=-15,...,15.

## Next bound RQT-323

Given actual frozen matrices and a candidate base root p, solve the simultaneous isotropic-direction conditions for even integer v and test fixed-primitive coordinates. Keep failure witnesses and ancestry.
