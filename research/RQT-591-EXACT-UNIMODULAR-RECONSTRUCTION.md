# RQT-591 — Exact HNF/LLL Unimodular Basis Reconstruction

## Executed, not assumed
Recovered the user-archive sources:
- RQT-541 `historical_index64_basis.json` (21×21)
- RQT-545 `saturated_rank4_basis_21x4.json` (21×4)
- RQT-545 `rank4_gram.json` (4×4; hash confirmed in RQT-590)
- RQT-545 `rank4_wall.json` (4×4; hash confirmed in RQT-590)
- Original archived RQT-544 exact-rational `qlll` function and RQT-575 driver

Constructed the exact 22×21 coordinate map K and embedding A=K·B·N (22×4); computed HNF(A), applied exact-rational qlll(HNF(A)^T), and solved A·U=R^T.

## Verified exact assertions
- 152 LLL steps (matches RQT-575 archive)
- U has integral entries and abs(det(U))=1
- A·U=R^T
- Fr=U^T·F·U; Hr=U^T·H·U
- Hr+Hr^T=-Fr
- det(Fr)=det(F), det(Hr)=det(H)
- Fr[0,0]=-9603309702921447656 (RQT-589 independently recovered scalar)
- With b=Fr[0,1:4] and S=Fr[1:4,1:4], `b^T b - Fr[0,0]·S = M` matches **every entry** of the RQT-589 independently reconstructed discriminant matrix.

The first row of Fr is `[-9603309702921447656, -5518412993766573646, 4661604576371729393, -8977768565951810684]`.

## Provenance and limitations
The reconstructed Fr serialized using JSON indent=2 + newline hashes to `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228`. The archived expected `rqt575/reduced_gram.json` SHA-256 is `aa8607e3582dd979ee35a07782bb56eafc6c247a7edf6584531bb7cc9844473d`. Common formatting variants did not close this mismatch. **The 4×4 form is a verified rederived Gram, not a byte-identical archival recovery.**

The 22×4 embedding A was reconstructed from the archived historical bases, but the original 22D Gram/Wall replay has not been performed. No new root was found, and no exhaustive integer root existence theorem follows.

**Ledger:** 81/135 selected ray-offset families excluded, 54 unresolved. Root19 OPEN.

## Next natural bound — RQT-592
Use reconstructed exact Fr to replay the RQT-583 equations directly from the Gram at signed t values. Classify coordinate recovery through the parity and divisibility condition `u=(-b(v)±√Δ(v))/a` for any true square discriminant, and recover the complete 22D source Gram/Wall before attempting the full Wall verification.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
