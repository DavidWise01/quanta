# RQT-593 — Higher 2-Adic Coordinate Gates

## Executed result
RQT-592 established **82 excluded / 53 unresolved** of 135 *selected* ray-offset families; no claim is made about all rank-four integer vectors.

Using the reconstructed RQT-591 integer Gram and the 80 archived RQT-583 Pell equations, tested every one of the 53 surviving families by exact pairwise modular lifting of the norm equation in eliminated coordinate `u` and ray parameter `t`.

For each family, write `q(u,t)+2=a u² + b u t + c t²+d u+e t+f`. At modulus `2^k`, retain every valid residue pair `(u,t)`. For the next modulus, independently test each of its four lifts `(u+i·2^k,t+j·2^k)`, `i,j∈{0,1}`. This method preserves all modular solution branches and never treats a finite nonfinding as an all-scale proof.

**Results:** 53/53 families retain valid residue pairs at every tested power of two, through **8192**. Their counts at modulus 8192 range from **8192 to 49152**. **Zero new all-scale exclusions.**

A separate finite exact discriminant-square search for each of the 53 families, over **−12000≤t≤12000**, tested **1,272,053 family-parameter combinations** and found **zero perfect-square discriminants** and thus **zero recovered integer u** in this range. This is not an all-scale result.

Source fingerprints:
- Reconstructed RQT-591 Gram SHA256: `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228` (rederived, *not* byte-identical archived RQT-575 source).
- RQT-583 Pell archive SHA256: `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`.

**Status:** 82 of 135 selected families excluded (60.74%), 53 remain unresolved, Root19 OPEN; original 22D Wall replay not run.

## Next natural bound — RQT-594
Use higher odd-prime-power *joint coordinate* lifts (especially 3-adic and 5-adic), exploit divisibility of `−b(v)±√Δ(v)` by the leading Gram coefficient, and separately preserve any genuinely exact all-scale modular exclusions. Do not count finite no-hits as exclusions.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
