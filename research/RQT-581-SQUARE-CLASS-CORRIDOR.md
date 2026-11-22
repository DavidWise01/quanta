# RQT-581 — Square-Class Corridor Filter

**Exact integer calculation** on the archived RQT-575 reduced Gram matrix and the five RQT-580 narrow-cone rays. For each ray r and offset epsilon∈{−1,0,1}³, substitute (v,w,z)=t*r+epsilon into the eliminated-coordinate discriminant. Each of the 5×27=135 families is exactly Delta(t)=A*t²+B*t+C, verified against direct evaluation at integer scales −5,−2,−1,0,1,3,17.

**All-scale exclusion test:** for each family and m∈{8,16,32,64,128,256,3,9,27,5,25,7,11,13,17,19,23,29,31}, enumerate every t mod m. If no Delta(t) is a square mod m, then no integer t can produce a perfect-square discriminant. This is a rigorous family-level necessary-condition obstruction, regardless of scale.

**Result: 15 of 135 entire families excluded, 120 unresolved.** Minimal-modulus certificates: m=5: 3; m=7: 1; m=25: 8; m=29: 1; m=32: 2. The local JSON certificate contains all 135 exact A/B/C coefficients and every tested excluding modulus; reproducible exact Python enumerator attached as a conversation artifact.

**Scope:** these 15 exclusions hold only within the five selected rays and 27 offsets. Unresolved does not mean solvable. No norm−2 seed found; original 22D Gram/Wall test not run; no nineteenth root or 21-reflection word. The nested {{i}}/base-60 construction serves as indexing architecture, not as a proven root operator. Previous heuristic ~65% research-readiness is not a mathematically measured completion probability.

**Next RQT-582:** examine the remaining 120 families via CRT-compatible square classes, Pell-type Diophantine equations, or arithmetic obstruction certificates; seek a verified exact integer solution or global family-level obstruction.

Local artifacts: exact rqt581.py, results.json, RQT-581-RESEARCH.md, new volcanic neon JPEG and self-contained HTML with embedded JPEG. GitHub viewer is text-only; GitHub Pages and JPEG repository publication unverified.
