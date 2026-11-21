# RQT-527 — Global Factor Audit

**Exact outcome:** 73 conditional fixed-x norm targets have `gcd(Hx_i²−α)=1`, hence their norm targets `N_i=f(Hx_i²−α)` satisfy `gcd(N_i)=abs(f)`. There is no additional common integer factor across these **73 selected** targets.

Frozen Gram SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809` verified against RQT-520 frozen inputs. `A=9α`, `J=9fH`, `gcd(α,H)=gcd(α,f)=1`.

Exact prime trial divisions below 2 million: `abs(f)=13*23*C_f` with both exponents 1 and 1,344-bit unknown cofactor; `α=2657*C_α` with exponent 1 and 2,426-bit unknown cofactor. Both f primes split: Legendre(-α/13)=Legendre(-α/23)=+1. At p=2657 ramified in α, Legendre(fH/2657)=+1, so no new obstruction. Pollard p−1 at B=250000 using four bases (2,3,5,7) did not discover an additional factor of C_f; **not** a primality proof. No complete class-group computation was done.

**New exclusions 0. Ledger remains 647/720 conditional fixed-x exclusions, 73 unresolved. Root19 OPEN; root18 predecessor UNVERIFIED.** Local arithmetic neither constructs an integral root nor proves global nonexistence.

Canonical geometry: `{inf brace [ inf contain ( inf construct \\mix/\\match/ ) ] }^{n}`, with seven-level sexagesimal addressing as a navigation layer, not exhaustively traversed.

Next RQT-528: exact back-map + class-group/representation feasibility with rigorous certificates, and predecessor18 validation.

Full reproducible script, JSON and Art Nouveau JPEG are supplied as conversation artifacts. This GitHub page is a text edition; Pages deployment and JPEG upload not confirmed.
