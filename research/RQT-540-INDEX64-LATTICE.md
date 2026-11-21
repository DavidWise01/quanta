# RQT-540 — Index-64 Lattice Recovered

**Executed exact original-source reconstruction** of an index-64 Wall-integral lattice from Stoicheion's public 22×22 Gram and operator. In the primitive rank-21 h-perpendicular basis K, compute `GK=K.T G K`, `XK=K Y`, `W=GK*(Y-I)^(-1)`, and `Z=4W`. Use GF(2) row reduction of `Z.T mod2` to construct the integer kernel `Z.T x=0 mod2`.

**Verified binary pivots:** (0,1,9,10,15,19), rank 6. **Independently constructed 21×21 integral lattice basis B** satisfying `abs(det B)=64`, `(Z.T*B)%2=0`; `HB=B.T W B` is integral with `det HB=1`; `QB=B.T GK B` has `det QB=-16384`; `HB+HB.T=-QB`. Exact runtime 0.205 s.

Both published ambient vectors RQT-224's initial root16 and RQT-241's Branch2 root17 have integral B coordinates. Their being in the same Wall-integral lattice does **not** make them an ordered compatible root chain.

**Critical limitation:** The reconstructed B is a valid index-64 parity-kernel basis, **not demonstrated coordinate-identical to the historic RQT-198 B**. The original RQT-216 reduced 21×6 basis Z6 and its coordinate conventions remain missing. Therefore the authentic Branch-2 6D→22D transported root16 and its correct pair with r17 are PENDING. Never apply the published RQT-216 6D coefficient vector to an alternate basis without the intervening change-of-basis map. No new root19 candidate or exclusion.

**Original-source SHA256 (raw UTF-8):** G d7722b6c0c5f2d45db3ff29583929b0ba38933cb6281b754083bf2c0d2438422; X e21c218c85abbfcc82ab1221f8c463259b0c9154f678150b67963e1a46134ede.

**Status:** reconstructed 21D lattice PASS; root18 first-stage PASS from prior audits; full original 17-root chain PENDING; root19 OPEN, full21 OPEN; selected conditional ledger unchanged 647 excluded / 73 unresolved of 720. Seven-level base-60 architecture retained as navigation, not enumerated this turn.

**RQT-541:** independently rederive saturated rank-six lattice from the fifteen ordered original roots, then relate it to RQT-216's 6D basis and transport both branch16 vectors without conflating coordinates. Local runnable Python, full 21×21 B JSON, exact results, JPEG and embedded-JPEG HTML are available as conversation artifacts. This GitHub edition is text-only, Pages unverified.

Sources: https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-198-wall-integral-lattice.md and https://github.com/DavidWise01/stoicheion/tree/main/research/rqt/source
