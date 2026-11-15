# RQT-383 — The p-adic Staircase: Local Lifts Before the Global Key

**2026-11-14 | Exact arithmetic experiment completed | Authentic root18–21 coordinates remain OPEN.**

## The story and the precise goal

The user-selected cubic GMA remains `{{9×9×9}}^9` around central singlet `||||`: 729 microcells per generation, 27 spatial macrocores, nine generations. The RQT-383 JPG chapter, **RQT-383-The-P-adic-Staircase.jpg**, illustrates two original ternary planes, p-adic lifts, an exact lattice-reduction search, and the unopened roots 18–21. It is **conceptual art**, not a plot of discovered exact roots; the JPG is supplied as a separate conversation artifact, not uploaded to GitHub.

RQT-381 gave a Bézout/parity bridge that constructs a norm-(-2) integer vector once a genuine primitive integer isotropic `u` with `gcd(F4*u)=1` is available. RQT-382's two-plane cylinders found no u with two reduced coordinates at magnitude <=10,000. This chapter attempts a **different constructive method** rather than simply extending that radius.

## Original exact lattice and planes

The source is the original frozen stoicheion RQT-242 integer F4/H4, checked by the published executable against det F4, det H4 = 1, and H4+H4.T=-F4. For plane `m/n∈{194/195,201/202}`, the integer embedding and chart are:

```text
T(m,n)=[[-m,0,0],[0,1,0],[n,0,0],[0,0,1]]
V194 = [[1,3,1],[-25,-74,-24],[113,340,113]]
V201 = [[1,2,1],[-26,-51,-25],[117,235,117]]
A = V.T T.T F4 T V
u = T V z,  z=(h,x,y) integer
```

Both (V) are unimodular, and the exact ternary matrices `A` agree with the independently verified RQT-382 forms.

## The p-adic lift

Choose p from **5,7,11,13,17** and a local projective representative `z=(h,1,y)` with `z.T A z = 0 mod p` and `2(Az)_0 != 0 mod p` (a smooth derivative). Lift h from mod p to mod `p^k`, keeping x=1 and y fixed:

```text
M=p^j
Q(z)=z.T A z
e=(Q(z)/M) mod p
g=2(Az)_0 mod p
h_new=h + M*(-e*g^{-1} mod p)
```

The program asserts `Q(h_new,1,y)=0 mod p^(j+1)` at **every step**, so the local witnesses are exact, not numeric approximations. It tests k=5,8,11,14.

## Integer lattice-reduction attempt

For a lifted local line `(h,1,y) mod M`, construct the integer lattice spanned by the following **rows**:

```
(M,0,0)
(h,1,y)
(0,0,M)
```

It has determinant ±M². Its LLL-reduced basis and all nonzero combinations of coefficients in `{-2,-1,0,1,2}^3` are **actual integer vectors**. For every one, evaluate the full exact ternary norm `z.T A z`. Any equality to zero is lifted via `u=T V z` and rechecked against the **original F4**. A merely small, local, or nearly-null vector is **never reported as an exact witness**.

## Actual executed results

The locally executed self-contained SymPy source `/mnt/data/rqt383_padic_lll.py` produced `/mnt/data/rqt383_padic_lll_results.json`:

| Exact check | Count |
|---|---:|
| Selected smooth p-adic branches | **264** |
| Individually asserted Hensel lift steps | **2,244** |
| LLL-derived integer vectors checked with exact norm | **33,528** |
| Nonzero integer null vectors recovered | **0** |

Per-plane/prime seed counts:

| Plane | p=5 | p=7 | p=11 | p=13 | p=17 |
|---|---:|---:|---:|---:|---:|
| 194/195 local smooth seeds available | 4 | 6 | 10 | 14 | 18 |
| 194/195 seeds used | 4 | 6 | 8 | 8 | 8 |
| 201/202 local smooth seeds available | 4 | 4 | 8 | 12 | 16 |
| 201/202 seeds used | 4 | 4 | 8 | 8 | 8 |

**Important mathematical scope:** A selected local p-adic branch need not contain a small global rational point. Searching its LLL basis with bounded combination coefficients is **not** exhaustive over global integer null vectors or over all local branches. Thus the zero discoveries neither refute the earlier rational isotropy result nor prove the global norm-(-2) equation lacks integer solutions.

## GitHub deliverables and exact status

- `research/rqt383-padic-lll-null-recovery.py`: self-contained authentic Gram matrices, exact p-adic Hensel lift, exact LLL and norm checks; prints replayable results.
- `research/RQT-383-PADIC-STAIRCASE.md`: this append-only result ledger.
- Conversation JPG `RQT-383-The-P-adic-Staircase.jpg`: a chapter illustration, **not** an original integer root witness and **not yet committed as binary image**.

**Roots18–21 remain OPEN.** The internal three-root Wall flag would force root21 by RQT-379, but none of roots18–20 has been constructed in the original lattice.

## Next natural target RQT-384

Move from one fixed local projective `y/x` ratio to a **certified constructive conic-solving algorithm** (e.g. explicit ternary quadratic zero via number-field norm equations or quaternion-splitting), retaining the full original F4 exact witness test. Preserve the 27 cubic cores and a new JPG story chapter. Do not infer an exact global null vector from p-adic lifting alone.
