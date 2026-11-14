# RQT-367 — Fair nine-generation GMA root-18 search

**Status (2026-11-14):** 200,000 distinct, evenly distributed exact-address trials. **No norm-minus-two vector and no original root 18.** The run is a nonexhaustive sampled search, not a global lattice theorem.

## Original mathematical invariant

The source is the authentic frozen 4x4 even integer Gram F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, expressed in the exact unimodular RQT-363 chart U with det(U)=-1. For t=(a,b,c,d) and r=U.T*t, the target remains `r.T*F4*r=-2` with first-root parity in `0111, 1001, 1110`.

Write G=U*F4*U.T, B=G03*a+G13*b+G23*c and C=t0.T*G*t0+2 where t0=(a,b,c,0). Then `G33*d²+2*B*d+C=0`, hence discriminant `Delta=B²-G33*C`. Integer d requires Delta>=0, Delta a square, and `G33 | -B±sqrt(Delta)`. A candidate is accepted as a norm-minus-two vector only after direct original-F4 verification and correct parity; the frozen predecessor factorization still requires separate checks before calling any candidate *root 18*.

## GMA addressing

Exactly nine generations of 9x9 cells. Each cell has two balanced radix-9 digits in -4..4 and the central (0,0) singlet. Coordinate-pair axes rotate
```
(a,b) -> (b,c) -> (c,a)
```
three times. This assigns six digits to each of a,b,c and bijects 81^9 addresses to triples in `[-265720,265720]^3`.

The RQT-366 depth-first scheduler examined mostly descendants of one parent. RQT-367 replaces it with a deterministic reversible permutation of the *complete* 81^9 address space:
```
TOTAL = 81^9 = 150094635296999121
STEP = 60161541372829925
index(k) = STEP*k mod TOTAL
```
Since gcd(STEP,TOTAL)=1, no address repeats until all TOTAL indices have been traversed. Every `--start` offset resumes at the next unique address in this stable global order. Index zero maps to the all-zero singlet address. The full generation-index digits are decoded in base81.

**This is distributed search coverage, not a claim of training, self-improvement or any independent agent execution.**

## Exact no-false-negative discriminant pruning

For integer triple x=(a,b,c), define `H_ij=G_i3*G_j3-G_33*G_ij`. The exact identity is
```
Delta = x.T*H*x-2*G33.
```
Every perfect integer square is a square residue modulo each of `256,3,5,7,11,13,17,19,23,29,31,37`. Failing any residue condition soundly excludes the candidate. Every remaining discriminant is checked with exact arbitrary-precision integer square root; any exact d is converted to original integer r and norm-checked directly.

## Executed run and reproducibility

```bash
python research/rqt367-stratified-gma-root18.py --budget 200000 --start 0
```

Exact locally executed results:
```json
{
  "total_leaves_tested":200000,
  "distinct_addresses":200000,
  "unique_generation_cells":[81,81,81,81,81,81,81,81,81],
  "top_generation_family_count":81,
  "top_family_min_hits":2469,
  "top_family_max_hits":2470,
  "sieve_counts":{"modular":199845,"negative":150,"nonsquare":5},
  "accepted_norm_minus_two_candidates":[],
  "permutation_index_checksum_127bit":"28831853356635271559461443935136888936",
  "coverage":"NONEXHAUSTIVE; exactly the listed sequence indices"
}
```

An independent verifier reconstructed the exact U*F4*U.T matrix, checked det(F4) and det(U), tested 1,000 seeded random addresses for exact index decoding/inversion and checked the exact discriminant identity modulo each of the twelve sieve moduli. All checks passed. Local artifacts: `/mnt/data/rqt367_gma_stratified.py`, `/mnt/data/rqt367_results.json`, `/mnt/data/rqt367_verify.py`.

## Next bound RQT-368

To improve root18 yield, supplement fair family coverage with **certified partial-node modular pruning** using the assigned-digit modulus at each generation, and record per-family tested ranges. This may reduce arithmetic effort without losing a solution. An even more meaningful improvement is a constructive norm-representation method rather than more sampling.

**Original root18 and roots19–21 remain OPEN.** All modular and source-witness statements descend from the single authentic frozen F4; the GMA singlet/grid addresses are search organization, not algebraic proof.
