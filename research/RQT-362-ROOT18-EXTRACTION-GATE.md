# RQT-362 — Exact root-18 extraction gate (NO original root yet)

**Status:** Exact **conditional** root constructor and Wall-prefix verification implemented. **Original root18 is OPEN**, and roots19–21 remain OPEN. A genuine explicit null vector `u` on the authentic rank-four lattice and the full frozen preceding 17 root vectors have **not** been provided by this computation.

## Authentic input
The program embeds the original frozen symmetric F4 and Wall H4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. It checks exact determinant, `det(H4)=1` and `H4+H4.T=-F4`. It does not substitute synthetic Gram into the actual task.

## Required witness and construction

Given an **explicit primitive integer vector** `u in Z^4`, reject unless
```text
u.T F4 u = 0
gcd(u0,u1,u2,u3) = 1
gcd((F4*u)[0],...,(F4*u)[3]) = 1.
```
The checker constructs integer Bézout coefficients `z` for the primitive pairing row `p=F4*u`, with `p.T*z=1`. It enumerates all 16 possible binary residues for the partner `v0`; for each residue with odd `p.T*v0`, take
```text
v = v0 + 2*((1-p.T*v0)//2)*z
```
so `u.T F4 v = 1` exactly. Define the integer quadratic half-form `q(v)=v.T F4 v / 2` and
```text
r = (1+q(v))*u-v.
```
Then `r.T F4 r = -2` identically. Enforce one of the upstream accepted first-root binary classes `0111,1001,1110`. The original Wall identity automatically gives `r.T H4 r=1`.

**A norm-minus-two root with accepted parity is not automatically root18 after the original frozen 17 roots.** The optional JSON file of exactly 17 ordered original 4-vectors verifies `r.T H4 r_i=0` for each earlier root `i=1,...,17`. If any pairing is nonzero, the candidate fails the prefix extension gate; the checker reports it and never calls it a compatible root18. The exact orientation `r_j.T H r_i` matches the original RQT-257 flag for `j>i`.

## Actual execution
The program was self-tested locally on the **separately identified synthetic** hyperbolic test form `U⊕U`, where `U=[[0,1],[1,0]]`, `u=(1,0,0,0)`, and an accepted-parity norm-minus-two root was constructed and checked. This synthetic test verifies the *algorithm*, not existence in F4. Running the original F4 path with no supplied u truthfully prints `root18 OPEN`.

The previous direct call to SymPy's generic `diop_ternary_quadratic` on the exact reduced `194/195` form failed to complete within **40 seconds**, and **no coordinates** were obtained. The timeout is not a mathematical exclusion and does not contradict RQT-351 rational existence.

## Usage

```bash
python research/rqt362-root18-extractor.py
python research/rqt362-root18-extractor.py --u X0 X1 X2 X3
python research/rqt362-root18-extractor.py --u X0 X1 X2 X3 --prior-roots-json prior17.json
```

The program verifies exact integer norms, pairing and accepted parity; the prefix file is required for a claim that an extracted root is actually the eighteenth extension.

## Next actual research task

Find a genuine exact primitive integer F4-null vector in either proved-isotropic rational plane `194/195` or `201/202` via a certified constructive conic solver. RQT-353A proves any primitive null vector there has pairing divisibility one, so this extractor can proceed immediately upon receiving `u`. A fully validated original root18 still additionally requires the frozen 17-prefix Wall gate. **Never label a synthetic test or a conditional extractor as recovered root18.**
