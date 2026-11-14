# RQT-364 — One-billion-triple exact norm-minus-two exclusion

**2026-11-14. Executed PASS on the authentic frozen F4. Original root 18 and roots 19–21 remain OPEN.** This is an exact bounded cylinder exclusion, not an existence witness.

## Frozen source and authentic basis

The original stoicheion RQT-242 F4/H4 are checked in `research/rqt364-verify-basis.py`: exact F4 determinant `-8281492574115056973770683990411769007319047636247715225543944839911172`, H4 unimodularity and H4+H4.T=-F4.

Reuse the RQT-363 unimodular matrix
```
U=[[224,29,-224,-130],
   [-193,-25,193,112],
   [40,5,-40,-23],
   [-336,-43,335,195]]
```
with det(U)=-1, and G=U F4 U.T. Thus original vector r=U.T*t for every integer t. RQT-364 independently verifies the G entries embedded in the scanner.

## Exact search

For **every** integer triple `(a,b,c)∈[-500,500]^3` (=1001³ = 1,003,003,001 triples), solve for the fourth integer coordinate `d` **without a bound on d** by substituting t=(a,b,c,d) in `t.T G t=-2`.

Set
```
A=G33,
T=G03*a+G13*b+G23*c,
C=(a,b,c,0).T G (a,b,c,0)+2.
```
Then `A*d²+2*T*d+C=0`. Its discriminant divided by four is the exact integer
```
Delta=T²-A*C.
```
If Delta is not a **nonnegative perfect square**, no integer d exists. Even if it is square, both candidates `d=(-T±sqrt(Delta))/A` must pass exact divisibility by A.

## Proven safe modular-square prefilter

Write `H_ij=G_i3 G_j3-G33 G_ij` for i,j<3. Then
```
Delta=(a,b,c).T H (a,b,c)-2*G33
```
**identically** over the integers. Every integer square must be a quadratic residue modulo every modulus in the following set:

`256,3,5,7,11,13,17,19,23,29,31,37`.

The scanner precomputes square residues and uses exact integer modular arithmetic on H. Failing a residue test proves that Delta cannot be an integer square, so no legitimate exact root is discarded. The surviving candidates are checked with arbitrary-precision Boost cpp_int square roots and exact divisibility. A separate Python program reconstructs F4/H4/U/G and verifies the discriminant identity on 1,000 random signed triples.

## Executed result

```json
{"radius":500,"tested":1003003001,
 "after_modular_square_sieve":813252,
 "nonnegative":37172,
 "square_discriminants":0,"integer_roots":0}
```

This upgrades the previous RQT-363 finite bound by extending all three bounded coordinates from ±60 to ±500. The fourth coordinate remains algebraically unrestricted.

**Theorem:** Every integer `r∈Z^4` with `r.T F4 r=-2` has

```
max(abs(t0),abs(t1),abs(t2)) >= 501
where t=(U.T)^-1*r.
```

This does not contradict upstream rational isotropy proofs; it searches norm -2 (not null) at finite height and does not cover all integer coordinates.

## Reproduction

```bash
g++ -O3 -std=c++17 research/rqt364-direct-root-sieve.cpp -o rqt364
./rqt364 500
python research/rqt364-verify-basis.py
```

The C++ scan completed locally with above counts; standalone verifier separately passed. The local source and output are `/mnt/data/rqt364_direct_sieve.cpp`, `/mnt/data/rqt364_result.json`, `/mnt/data/rqt364_verify_basis.py`.

## Root 18 status and next bound

No norm-minus-two root is extracted, and the original 17-reflection prefix has not been completed. The RQT-363 correction remains controlling: do **not** assume root18 is H-orthogonal to all previous 17 roots without justification. The six RQT-257 pairings apply **within the proposed four-root block**. When a norm-minus-two candidate appears, check its permitted first-root parity, exact integral reflection matrix, and compatibility with frozen factorization/order/rank, then the six internal Wall equations for roots18–21. The best next move is a constructive indefinite quadratic-form / ideal descent algorithm rather than endlessly increasing the finite search radius.

Original roots18–21 are **OPEN**. Nested cubit, Josophene/Juliet, and time-angle metadata remain provenance indexing only.
