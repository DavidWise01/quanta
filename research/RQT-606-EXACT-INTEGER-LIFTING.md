# RQT-606 — Exact Integer Lifts of Combined CRT Witnesses

## Exact execution
Recovered and verified the RQT-605 combined-coordinate witnesses, the RQT-604 family certificate ancestry, and the rederived RQT-591 4×4 Gram.

- RQT-605 source SHA-256: `c3f6d0c97c960e6d5721e08d63e4b55e9752ecb139c5dc014f3fac9ea4dc724d`
- Gram SHA-256: `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228`
- RQT-604 ledger tip: `e2bd1c5818a294ecd578af40791c81b3b96c432ee9276f0f404b7e4b054994a2`
- Combined modulus: `M=121298984430624000`

For each of 53 unresolved selected families, the exact integer representative of the original RQT-605 coordinate class was lifted as
`u=u_0+kM, t=t_0+ℓM`, with `-20≤k,ℓ≤20`. Every one of the `53·41²=89,093` integer pairs was evaluated directly in the rederived Gram:

`q_F(u,ray·t+offset)+2`.

Every evaluated norm residual was divisible by M, as expected; **zero pairs had exact residual zero**. The smallest absolute residual among all pairs was
`6040581229604935205810905019372225945310919968000`.

## One-step lifting of the stored coordinate class
For each family and each `p∈{2,3,5,7,11}`, exhaustively checked the `p²` coordinate refinements `(u_0+iM,t_0+jM)`, where `i,j∈[0,p-1]`, seeking `q_F+2≡0 (mod pM)`.

- For p=2: **26/53 stored residue classes do not lift** to modulus 2M; 27/53 do.
- For p=7: **2/53 stored classes do not lift** to modulus 7M; 51/53 do.
- For p=3,5,11: **53/53 stored classes lift**.

The two p=7 failures are selected-family indices **2 and 24**. The 26 p=2 failures are indices `0,1,2,7,28,29,30,33,34,35,37,44,49,55,56,57,61,62,64,65,67,81,89,92,109,110`.

These are genuine extra obstructions for the **particular residue classes fixed by RQT-605**, not evidence that their **entire families** are impossible. Other solutions modulo M may lift even when a stored witness does not.

## Scope
- Exact integer searches: **89,093 pairs**, all nonzero norm residual.
- New all-scale selected-family exclusions: **0**.
- Global selected-family ledger: **82/135 excluded (60.74%), 53 unresolved**; selected corridors do not cover the entire four-dimensional lattice.
- Original 22D Wall replay: **NOT PERFORMED**.
- Root 19: **OPEN**.

## RQT-607 natural bound
For each family with a nonliftable stored CRT class, sample or enumerate *alternate* valid classes modulo M in a bounded, auditable way; test existence of extensions modulo 2M and 7M. This distinguishes a badly chosen representative from a true local family obstruction. Do not count a nonliftable single representative as an all-scale exclusion.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
