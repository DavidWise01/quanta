# RQT-580 — Recursive Narrow-Cone Exact Search

**Executed exact finite ray-neighborhood scan** using original reduced rank-four Gram from RQT-575 and RQT-578 discriminant-survivor directions. The surviving rays are deduplicated to:
(35,-10,14), (45,-13,18), (80,-23,32), (95,-27,38), (115,-33,46).

For each ray r, t=1..20000 and every epsilon in {-1,0,1}^3, set (v,w,z)=t*r+epsilon. Solve the rank-four quadratic q(u,v,w,z)=-2 by discriminant Delta=b²−a(c+2), a=F00, b=F01v+F02w+F03z, c=(v,w,z)^T F[1:4,1:4](v,w,z). Exact integer arithmetic with isqrt, no floats.

**Complete run:** 5 rays × 20000 values × 27 offsets = **2700000 triples**. Exactly **2695792 nonnegative discriminants**; **0 perfect-square discriminants**; **0 integral norm−2 vectors**. Independent rerun replicated these counts. Finite selected ray neighborhoods only, not a nonrepresentation proof.

RQT-579's recursive sexagesimal encoding is a lossless index for t and nested addresses; it does not itself change the lattice or generate new Gram vectors. We do **not** claim the ray family exhausts all Diophantine possibilities. Original 22D Gram/Wall replay not reached, because no exact candidate was produced. Root 19 OPEN.

**Next RQT-581:** algebraic square-class/Diophantine parameter analysis along each ray, or stronger complete arithmetic obstructions; avoid simply increasing bounds.

Conversation artifacts include executable Python, JSON counts, research markdown, new orange/navy risograph-style JPEG and standalone embedded-JPEG HTML. This committed GitHub viewer is text only; GitHub Pages and JPEG binary repo publication remain unverified.
