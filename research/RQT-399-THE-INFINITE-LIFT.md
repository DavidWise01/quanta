# RQT-399 — The Infinite Lift

Date: 2026-11-15. Source ancestry: RQT-388/394/398. ASCII-only visuals.

## Theorem (regular Hensel branch)

Let Q be an integral symmetric 3x3 matrix and N(v)=v^TQv+2.
Suppose v mod p satisfies N(v)=0 mod p and at least one entry of
2Qv is nonzero modulo p. Given a lift v_k modulo p^k,
write w=v_k+p^k t, t in (Z/pZ)^3. Then

 N(w)/p^k = N(v_k)/p^k + (2Qv_k).t (mod p).

This linear equation in three variables has precisely p^2 solutions
because the gradient is nonzero. The gradient remains nonzero modulo p
at every generation. Induction produces an infinite compatible chain,
equivalently a solution over Z_p.

At p=2 all entries of 2Qv vanish mod 2, so none of the mod-2 seeds
qualifies for this regular theorem. The two-adic singular branches
require separate analysis.

## Independent algorithm cross-checks on illustrative forms

Executed locally on two illustrative matrices (not the target
RQT-388 matrix), with direct enumeration of all triples modulo p^2.
The predicted count agrees with brute force:

 Q=diag(1,1,1): p=2:24, p=3:54, p=5:500, p=7:2744.
 Q=diag(1,-1,-1): p=2:8, p=3:54, p=5:500, p=7:2744.

For p=3,5,7 an explicit regular branch was constructed through p^6
for both illustrative forms. This validates the routine but does not
certify root19.

## Logical boundary

An infinite p-adic lift for one prime does not automatically produce
a common integer lattice root satisfying the real slope corridor and
norm -2. Even having compatible local solutions at every prime does
not by itself provide a global integral point.

For the original root19 lattice, run the script with the complete
RQT-388 --out file (containing restricted_Gram), not the summary JSON.
No target-matrix results were executed in this turn.

Root19 OPEN; root20 OPEN; root21 conditional.
Next: RQT-400, the two-adic singular persistence gate.
