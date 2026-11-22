# RQT-594 — Odd-Prime-Power Coordinate Recovery

## Exact local execution

Used the RQT-591 reconstructed reduced 4×4 Gram and archived RQT-583/584/586 JSON certificates. The Gram and Pell inputs matched their recorded SHA-256 fingerprints.

The prior selected-ray ledger contains **82/135 all-scale excluded** families (including RQT-592 family 13), leaving **53** to test.

The reduced norm equation in integer coordinates u,t is q(u,t) + 2 = 0. For an odd prime p not dividing the leading Gram entry a, solvability modulo p^k is equivalent to the discriminant Δ(t) having a square root modulo p^k, with u = (−b(t) ± sqrt(Δ(t)))·a⁻¹ (mod p^k).

Here a = −9603309702921447656, coprime to 3 and 5. For every one of the 53 families, all t residues were scanned for every power 3^1 through 3^9 (19683) and 5^1 through 5^6 (15625), using complete square-residue tables. The first admissible t was paired with a recovered u, and q(u,t)+2 ≡ 0 (mod p^k) was asserted directly using the reconstructed Gram.

**Verified outcomes:** 53/53 survived all tested odd prime-power moduli. Number of admissible t residues per family at the top levels: **6561–19683 at 19683**, and **3647–15625 at 15625**. **Zero newly excluded families.**

**Scope and limits:** Finite moduli are not a proof of existence of global integer coordinates; this is neither a new root nor a complete all-primes local-global classification. The 135 corridors do not exhaust the full 4D lattice. Original 22D Wall replay NOT RUN. Root19 OPEN. The reduced Gram is an exact rederivation; byte identity with the missing RQT-575 archived matrix remains unconfirmed.

## Next natural bound — RQT-595

Switch from increasing prime-power bounds to **global Pell orbit constraints**. For a selected surviving Pell family, use exact generalized Pell equations, index/parity recovery and modular sieving on orbits. Preserve candidate integer u and t only if their recovered 4D norm equals −2. Do not claim a global no-solution theorem from a finite orbit cutoff.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
