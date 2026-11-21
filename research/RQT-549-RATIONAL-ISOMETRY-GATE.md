# RQT-549 — Rational Isometry Gate

**Exact computation** with frozen historical RQT-516 and alternative RQT-545 4×4 Wall/Gram matrices. The rational intertwiner equation `D_new U = U D_historical` has a **four-dimensional rational nullspace**. Every intertwiner is `U=t0 B0+t1 B1+t2 B2+t3 B3`, and the simultaneous Wall-isometry equation `Uᵀ H_new U = H_historical` yields 16 exact quadratic equations in four rational coefficients. Full coefficients and four basis matrices are available in the local results.json.

A bounded coefficient test checked all **624 nonzero 4-tuples in [-2,2]^4**; no exact rational simultaneous Wall isometry appeared. This is NOT a global rational nonexistence proof.

**New prime-five path:** independently lifted the RQT-548 witness from modulus 25 through modulus **125** and **625**. At both stages the correction linear system has rank 14 with two free parameters over F5, and the following matrix is an exact Wall-isometry witness modulo 625:

`[[479,51,198,27],[61,445,86,455],[543,21,335,260],[618,4,472,4]]`.

Its determinant is invertible modulo 5. It was checked against the original full integer Wall matrices, and simultaneous Gram congruence follows from F=−H−Hᵀ. **One lift path verified; not an exhaustive count of prime-five descendants.**

**Status:** Rational operator conjugacy VERIFIED; four-dimensional rational Wall-isometry equations DERIVED but unsolved; local p5 congruence through 625 VERIFIED; global integral GL4 equivalence OPEN; root18 transfer not established; root19 OPEN; full21 OPEN. Original 720 selected conditional corridors remain 647 excluded / 73 unresolved. Seven-level base-60 navigation retained but not traversed.

**Next RQT-550:** solve rational 4-variable simultaneous isometry equations with number-field norm methods or identify a rigorous obstruction, then test integral equivalence only after a rational isometry is certified.

The Python engine, full JSON coefficient system, new Bauhaus-style WAKAKU JPEG and self-contained JPEG-embedded HTML were created as conversation artifacts; the GitHub HTML is text based and GitHub Pages serving remains unverified.
