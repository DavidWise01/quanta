# RQT-400 — The Two-Adic Gate

Date: 2026-11-15. Canonical visuals: ASCII only.
Target: norm -2 in the original F4 form, restricted to the frozen
RQT-388 saturated rank-three successor kernel.

## Exact lift rule, with critical base-case distinction

Let N(v)=v^T Q v+2 for symmetric integral Q.

For k>=1, any v modulo 2^k and t in {0,1}^3 has

 N(v+2^k t)-N(v)
 = 2^(k+1)(Qv).t + 2^(2k) t^T Q t.

Both terms are divisible by 2^(k+1), because 2k >= k+1 for k>=1.

Therefore if v solves N(v)=0 modulo 2^k, all 8 lifts to
modulo 2^(k+1) either survive (when N(v)=0 modulo 2^(k+1))
or all fail (when not). The base level modulo 2 must be enumerated
directly: a lift from modulus 1 does NOT satisfy this rule.

The criterion must not be confused with singular branch survival
at all future generations. An all-eight family can die later.

## Independently enumerated illustrative counts

Direct enumeration of all 3-coordinate residues, not the target
frozen Q, produced these survivor counts for moduli 2,4,8,16,32:

 Q=diag(1,1,1):       4, 24, 96, 384, 1536
 Q=diag(1,-1,-1):      4,  8, 32, 128,  512
 Q=zero:               8,  0,  0,   0,    0

The zero form illustrates a complete local obstruction: all
mod-2 residues survive, and none lifts to mod 4.

## Proof boundary

If NO norm-minus-two solution exists modulo 2^k for any k,
there cannot be an integral root19. But nonzero survivors at
every checked finite level are not an integer witness.

The published script requires the full RQT-388 --out JSON
with restricted_Gram; the summarized result does not carry Q.
No target-matrix computation is claimed for this checkpoint.

Root18 first-stage previously accepted.
Root19 OPEN; root20 OPEN; root21 conditional.
Next: reconstruct or publish the frozen full Gram and execute the
target-specific two-adic check before any further claim.
