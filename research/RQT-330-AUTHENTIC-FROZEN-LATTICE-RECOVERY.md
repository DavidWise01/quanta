# RQT-330 — Original frozen lattice **recovered** from stoicheion

**2026-11-12 — source recovery PASS / original root 18–21 still OPEN.**

This is a correction to the RQT-258–329 bridge-only limitation: **authentic numerical matrices F4 and H4 are available in GitHub**.

## Immutable source identification

- Repo: `DavidWise01/stoicheion`
- Path: `research/rqt/rqt242_mod4_audit.py`
- Fetched source blob SHA: `11d4d1102ec450fd9bfba869ee9be261dc0490a4`
- Context: `RQT-242-rank-four-residual.md` and `RQT-256-first-reflection-order-reduction.md`.
- These data come from the earlier original RQT sequence, **not** the RQT-307 constructed bridge lattice.

`research/rqt330-authentic-frozen-preflight.py` embeds exact F4,H4 from this source and reconstructs `D4=I+H4.inv()*F4`. No invented numeric input.

## Exact recovered invariants

- F4 symmetric integral and nondegenerate; `det(F4)=-8281492574115056973770683990411769007319047636247715225543944839911172`.
- H4 unimodular `det(H4)=1`; `H4+H4.T=-F4`.
- D4 integral exact isometry: `D4.T F4 D4=F4`, `det D4=1`.
- Rational moving rank `rank_Q(D4-I)=4`.
- Mod-2 D4 has order three and equals `[[0,0,0,1],[1,1,1,0],[1,0,0,0],[0,0,1,0]]`.
- Exact inertia of F4 is `(1 positive, 3 negative)`.
- **Orientation preserved:** using an explicit rational positive vector from the positive pivot of the LDL congruence, `e.T*F4*D4*e>0`, so D4 maps the chosen positive-cone component to itself. The RQT-328 *bridge* orientation obstruction is **ABSENT** here, and was not applicable to the authentic target.

## Rank-drop identity

`E=D4-I=H4^-1 F4`, `det E=det F4`. Define the symmetrized adjugate form

```
B=(F4 adj(E)+adj(E)^T F4)/2.
```

Using `F4 E^-1=H4` and `H4+H4^T=-F4` shows

```
B=-(det F4)/2 * F4.
```

Hence every **actual** integral root r with `r.T F4 r=-2` automatically satisfies the rational moving-rank 4→3 equation. This is an exact theorem, not existence of r. For first-root parities 0111,1001,1110, the original RQT-256 report establishes mod-2 order 3→2.

## Bounded original root search

Enumerated r with `-3<=r_i<=3` and parity one of 0111,1001,1110:
- 0111: 192
- 1001: 144
- 1110: 192
- **528 distinct candidate vectors; zero norm -2 roots**.

No inference beyond that box: coefficients in F4 are enormous and later roots may have enormous coordinates.

## Real next step

RQT-331 should consume the authentic matrices from the pinned source and compute certified local/modular root residue tables plus an integral search strategy on the true F4. Once root 18 is found, propagate the reflected residual and find roots 19–21 with exact one-sided Wall conditions. RQT-257 ensures that a full upper-unitriangular Wall flag implies the exact four-reflection product identity.

## Provenance

The user-defined {brace[box(toroid)]} tensor is 3×3×3 (1 center, 6 faces, 12 edges, 8 corners); Josophene is the hardware/software bridge and Juliet the recursive 1/2/3/5/8/13/21 gates. The software verification is mathematical, not a hardware measurement. Preserve true source lineage and avoid counting multiple mirrors as independent witnesses.
