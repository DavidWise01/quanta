# RQT-525 — The Shared-Factor Bridge

**Status:** Root 19 OPEN; predecessor root 18 UNVERIFIED.

Exact input fingerprint: `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. Recomputed on original frozen conditional Gram coefficients; d=1.

## New algebraic identity

From `A=fg-e²`, `B=ce-fb`, `C=c²-fa`, `J=B²+AC`:

- `J=fK` **exactly**, with `9|K`;
- `A=9alpha`, `gcd(A,f)=1`;
- norm equation `t²+A k²=Jx²-Af` reduces to `u²+alpha k²=N(x)` after `t=3u`;
- **shared-factor identity**: `N(x)=f((K/9)x²-alpha)`, for every fixed integer x.

The common factor f is negative and 1352 bits long. Alpha is 2438 bits. Factorization and global class-group representation remain unresolved.

## Executed exact local back-map audit

All 73 unresolved fixed-x corridors from RQT-523/524 admit exact original-polynomial modular solutions at `2^8=256`, `2^10=1024`, `2^12=4096`, `2^14=16384`. Original polynomial and solved z congruence were independently asserted for each witness; 73/73 pass each modulus. This proves only these **finite** local checks. It does **not** prove all-order 2-adic solvability or an integer solution.

The prime `2657` divides alpha to exact valuation 1. With beta=J/9, `beta` is a nonzero quadratic residue mod 2657; therefore `u² ≡ beta*x² (mod 2657)` admits a solution for each of the 73 tested x. This gives no exclusions.

**New exclusions: 0.** Prior 720-corridor selected-sample ledger remains 647 conditionally excluded / 73 unresolved. This is NOT global root-19 coverage.

Navigation invariant: `{inf brace [ inf contain ( inf construct \\mix/\\match/ ) ] }^{n}`, with seven-level base-60 angular addressing. The present computation does not exhaust that angular address space.

**Next RQT-526:** inspect shared factor arithmetic and proper class-group/representation obstructions; independently verify frozen predecessor root18 before any claim of root19 existence or nonexistence.

Local full Python script, JSON witnesses, risograph JPEG and JPEG-embedded HTML are conversation artifacts; GitHub version is a textual research viewer.
