# RQT-688 · Root 19 in Rust

This is an **append-only Rust port** of the bounded, exact-arithmetic search over the recovered **RQT-388 saturated rank-three** kernel. It is not a claim that an integral root 19 has been constructed.

Canonical Quanta orchestration topology (not the dimension of the Gram form):

`{1×[3×8 | n | (8×3)×1]}`

The program loads the original reduced 3×3 Gram matrix and 4×3 basis from `data/RQT-388-root19-kernel-results.json`, checks symmetry, the exact identity `Q=BᵀF₄B`, the known mod-16 fingerprint, the primitive odd-denominator obstruction modulo 8, and performs an exact cone/discriminant scan with BigInt arithmetic.

## Run

```bash
cd rust/root19
cargo test
cargo run --release --bin rqt-root19 -- 3000
cargo run --release --bin rqt-root19 -- 10000
cargo run --release --bin rqt689 -- 33 1000
```

The optional CLI argument is the positive integer maximum y. Defaults to 3000. The program outputs a JSON result with candidate counts, exact integer lifts (if any), and an explicit `root19_status: OPEN`.

The scanning gate is the necessary strict inequality `177065/100000 < x/y < 178600/100000`. For every surviving pair, the program solves the original reduced quadratic form by its exact discriminant; a hit has its norm checked by direct substitution. Modular filters only reject impossible square discriminants, and never imply a root.

## Proof boundary

* A finite scan proves no root only within its specified coordinates.
* A reduced norm -2 vector would still need the original integral lattice, divisibility-one, and ordered reflection-chain checks.
* RQT-685 established rational existence for the reduced form; an **explicit rational witness** and **integral root 19** remain open.
* The `3×8 | n | 8×3` topology organizes the inquiry; it is **not** a 48-dimensional substitute for the exact rank-three Gram matrix.

Source: RQT-388 root19 kernel data (archived in the research artifacts). Prior source checks: RQT-390, RQT-394, RQT-687.

.dlw

## RQT-689 — primitive rational witness search

The additional `src/bin/rqt689.rs` executable searches `v=(x,y,z)/d` with odd primitive denominator `1<=d<=d_max` and `1<=y<=y_max`, under the inherited strict rational cone. It checks the exact homogeneous identity `(x,y,z)^T Q (x,y,z)=-2d²`, rejects impossible modular square discriminants, and reports all exact witnesses. Even primitive denominators are excluded by RQT-687's mod-8 obstruction. The search is **bounded**; zero hits is not a proof of global nonexistence. Use `cargo run --release --bin rqt689 -- 33 1000`.

The two binaries share the source fixture and perform exact calculations. The workflow now tests both and uploads both JSON results. An Actions execution, not merely committed code, is required to claim compiled/tested status.
