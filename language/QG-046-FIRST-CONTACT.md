# QG-046 — First Contact / First Broken Edge

**Scope:** specified Euclidean radial pinch family, not all possible deformations.

```text
OUTER n + CENTER
       |
RADIAL SCALING: s
       |
0 <= s < 1 : no center contact
       |
s = 1 : first vertex reaches center
       |
STOP / PRESERVE DEGENERATE EVIDENCE
```

For n in {3,4,5,8,13}, each outer vertex i has polar angle θ_i = 2πi/n. Each radius changes by r_i(s) = 1 - s(0.55 + 0.45 cos(lobes θ_i)). For integer lobes 1..8, the coefficient lies in [0.1,1], with coefficient at i=0 exactly 1. Thus every radius is strictly positive for 0 <= s < 1, and the index-zero radius vanishes at s=1.

With positive radii and radial ordering, the embedded ring is star-shaped and all fan triangles have positive signed areas A_i = r_i r_(i+1) sin(2π/n)/2. Therefore this particular deformation retains the nondegenerate wheel graph until s=1. At s=1 the zero-radius vertex coincides with the center and incident faces collapse. This is a **singular embedding**, not an automatic change of topological type. Defining a post-contact surgery would be a different experiment.

Fibonacci observation strengths are step/13 for steps 1,1,2,3,5,8,13. The repeated 1 is a distinct observation; step 13 reaches the boundary. The 14 tests check preboundary, boundary, postboundary, repeatable replay, and tampering. Internal ledgers are self-consistent but not externally authenticated.

```sh
node --test tests/center-pinch.test.mjs tests/first-broken-edge.test.mjs
```
