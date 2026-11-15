# RQT-385 — The Split-Prime Vault: complete target factorization on plane 194/195

**Date: 2026-11-14. Exact arithmetic PASS. Original integer isotropic vector u: NOT FOUND. Original reflection roots 18–21: OPEN.**

## What changed

RQT-361 left two long composite norm-target cofactors unresolved. RQT-385 **completely factors the first cofactor Q1** using bounded exact integer ECM followed by an independent multiplication and primality verification. The other plane (201/202) still has an unresolved cofactor; no complete factorization is claimed for it.

The exact new factors are

```text
Q1 = 4341012393885871793429166991367328918895695969836018205135496291

p1 = 419697635024167
p2 = 10343190029259773932231107365537334388821979446373

Q1 = p1 * p2
isprime(p1) == True
isprime(p2) == True
```

These are **integer equalities tested with exact arithmetic**, not approximate numerical decomposition. The SymPy primality tests provide strong algorithmic certification, but the research ledger does not include standalone ECPP/Pocklington primality certificates.

## Reconstructed from the original frozen F4

The script embeds the original 4×4 frozen F4, Wall H4, and the plane embedding `T(194,195)`. It uses unimodular `V194` from RQT-352, then independently checks the entire ternary matrix

```text
A=V194.T*T.T*F4*T*V194.
```

For the RQT-357 exact quadratic norm transformation let

```text
p = -A00 = 561555435662335446
q = -A02 = -758956630833872688
r = -A22 = 4624133667290001854
D = p*r - q*q
  = 2020692228609206586199528939517571540
Delta = D/4
  = 505173057152301646549882234879392885
N = det(A)
  = 11638033302642746511259255234414222206289825409305543124
C = p*N
  = 6535400861518316144793659960137348358553321057542702834643598395306773304.
```

The exact norm equation from RQT-360 is

```text
M^2 + Delta*B^2 = C*h^2
```

subject to the **integer image-lattice congruences** needed to invert the transformation to original ternary coordinates. The full target factorization is now

```text
C = 2^3 * 3 * 223 * 281297 * p1 * p2.
```

## Prime splitting evidence and the 16 CRT branches

For each odd unramified target prime `l ∈ {223,281297,p1,p2}`, the exact quadratic-residue test is:

```text
x_l^2 = -Delta (mod l).
```

Verified roots are:

| Prime | One verified root of -Delta modulo prime |
|---|---|
| 223 | 110 |
| 281297 | 47821 |
| 419697635024167 | 71653355089376 |
| 10343190029259773932231107365537334388821979446373 | 2915584228513542240957698906207970110798523185599 |

The Legendre symbol equals +1 at each of these four primes, confirming local splitting. There are **16 sign combinations** of the two square roots at each prime. The script computes all 16 CRT roots modulo their product

```text
P = 272308369229929839366402498339056181606388377397612618110149933137782221,
C=24*P.
```

It verifies each CRT root by squaring it modulo all four prime moduli. All 16 are distinct.

## Critical limitation

A complete factorization of C and a catalogue of split-prime roots are **necessary arithmetic input**, not a constructive solution of the norm equation `M²+Delta B²=C h²` with all original coordinate congruences.

The previously reported rational isotropy of plane 194/195 does not by itself yield explicit coordinates `u`, and the RQT-381 Bézout bridge cannot run without them. The internal RQT-377–379 Wall-flag machinery is also conditional on authentic roots.

**No integer isotropic vector u, no original norm-minus-two r, and no root18–21 reflection block was recovered in this turn.**

## Reproduction and provenance

Run
```bash
python research/rqt385-split-prime-vault.py
```

The script reconstructs F4/H4/T/V/A, checks exact determinants, repeats the complete target factorization and both new prime tests, and emits a detailed JSON atlas including all 16 CRT branches.

The executed local Python source is `/mnt/data/rqt385_split_prime_vault.py`, and the executed result file is `/mnt/data/RQT-385-Split-Prime-Vault-results.json`. The GitHub source is the same standalone arithmetic experiment.

## Continuing JPG chapter

This turn's original illustrated JPG is `RQT-385-The-Split-Prime-Vault.jpg`, available in the conversation. It shows the `{{9×9×9}}^9` cubic GMA with 27 spatial cores around `||||`, the newly split large cofactor and the still-locked integer root gates. It is a **conceptual illustration**, not a plot of the exact integer solution space. The image has not been committed into GitHub; the executable and this ledger have been.

**Important notation correction for the image:** the precise first goal is a null vector `u.T F4 u=0`. Only the subsequently constructed root `r` must have `r.T F4 r=-2`. Artwork must not be taken as a replacement for those equations.

## Next RQT-386

Use the complete splitting data for 194/195 to attempt **constructive norm representation** (Cornacchia/ideal lattice reduction with explicit conductor and ramified-prime constraints). Search candidate `M,B,h` exactly, enforce the inverse integral-coordinate congruences, and promote only a vector `u∈Z^4` with `u.T F4 u=0` verified against original F4. If obtained, the RQT-381 Bézout bridge should immediately construct a permitted norm-minus-two original lattice vector. Frozen predecessor factorization/order checks are still needed to name it root18.

**Roots 18–21 remain OPEN.**
