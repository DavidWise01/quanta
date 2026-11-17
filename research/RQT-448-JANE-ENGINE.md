# RQT-448 — J.A.N.E. Engine

Canonical architecture: `{{ 9xJx9 || 9xAx9 || 9xNx9 || 9xEx9 || }}`. Implementation assigns J=just-in-time candidate routing, A=incremental arithmetic, N=norm verification, E=evidence retention. Each stage has 81 logical lanes indexed by (y mod 9,x mod 9), not independent parallel workers. A candidate belongs to exactly one lane; x advances by 9. For E(x)=alpha*x²+2*K*y*x+gamma*y²+delta*d² the first difference advances by 162*alpha. The implementation checks incremental state against direct arithmetic; no speedup is claimed. E is also the discriminant symbol, distinct from the evidence operator.

Frozen Gram fingerprint 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809; original F4 backmap checked. Synthetic positive control found all 112 solutions for y=1..12. New disjoint d=1 tile y=10001..10100: 15414 feasible x, 30828 norm substitutions, zero fallback cases, zero hits. Root19 OPEN. Root18 prefix UNVERIFIED. All four lane matrices emitted by executable verifier. JPG is conceptual, with alternative labels for A/N/E; source implementation is authoritative.

Next: checkpoint each lane independently, then merge coverage without double counting.
