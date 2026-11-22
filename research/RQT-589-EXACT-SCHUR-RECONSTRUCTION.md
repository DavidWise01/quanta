# RQT-589 — Exact Schur/Discriminant Reconstruction

## Verified result
Recovered the original RQT-583 JSON from the user archive (SHA-256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`). Its 80 Pell equations yield 240 linear identities for seven unknowns: the six symmetric entries of `M` and the scalar `a`.

For a symmetric integer Gram `F = [[a,b^T],[b,H]]`, elimination gives
`Delta(v)=(b^T v)^2-a(v^T H v+2)=v^T M v-2a`, with `M=bb^T-aH`.

The 240×7 exact rational linear system has rank 7, consistent augmented rank 7, and **one exact solution**:
```text
a = -9603309702921447656
M =
[[-33923887662911442206164954953584674140,
   -4219194573559178010400265744479501422,
    81850829273715620803639379963437553624],
 [ -4219194573559178010400265744479501422,
  -21708964175564668486249102082477843199,
   -5011140550130980758998505863715699836],
 [ 81850829273715620803639379963437553624,
   -5011140550130980758998505863715699836,
 -208380363797895400994011084419064194688]]
```

All 80 archived equations passed exact checks: `A=r^TMr`, `B=2r^TMo`, `C=o^TMo-2a`, and `D=B²-4AC` (320 checks including D).

## Critical limitation: original Gram not uniquely identifiable
The eliminated-variable cross term vector `b` is not specified by the discriminant form. Even an integral Gram consistent with the recovered pair would admit integral shears of the eliminated coordinate changing `b` and `H` but preserving `M` and `a`. Accordingly, **do not assert that recovering M recovers the canonical F**. This run made no claim of recovering the original 22D embedding, no 22D Wall replay, no new exclusions, and no root 19.

Selected-family ledger remains **81 excluded / 54 unresolved of 135** (60% excluded). These selected families do not exhaust the entire rank-four lattice.

## Next natural bound — RQT-590
Recover the missing archival source with the canonical 4×4 Gram fingerprint `aa8607e3582dd979ee35a07782bb56eafc6c247a7edf6584531bb7cc9844473d`, or impose independent lattice data (for example, basis or parity) to select a valid `b` and `H` before any coordinate-recovery or Wall test.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
