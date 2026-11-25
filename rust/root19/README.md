# RQT-688 · Root 19 in Rust

This is an **append-only Rust port** of the bounded, exact-arithmetic search over the recovered **RQT-388 saturated rank-three** kernel. It is not a claim that an integral root 19 has been constructed.

Canonical Quanta per-position grammar (not the dimension of the Gram form):

`{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))`

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
* The eight named recursive spatial positions around `CENTER{[(FOCUS)]}` organize the inquiry; they are **not** a substitute for the authentic reduced rank-three Gram matrix.

Source: RQT-388 root19 kernel data (archived in the research artifacts). Prior source checks: RQT-390, RQT-394, RQT-687.

.dlw

## RQT-689 — primitive rational witness search

The additional `src/bin/rqt689.rs` executable searches `v=(x,y,z)/d` with odd primitive denominator `1<=d<=d_max` and `1<=y<=y_max`, under the inherited strict rational cone. It checks the exact homogeneous identity `(x,y,z)^T Q (x,y,z)=-2d²`, rejects impossible modular square discriminants, and reports all exact witnesses. Even primitive denominators are excluded by RQT-687's mod-8 obstruction. The search is **bounded**; zero hits is not a proof of global nonexistence. Use `cargo run --release --bin rqt689 -- 33 1000`.

The two binaries share the source fixture and perform exact calculations. The workflow now tests both and uploads both JSON results. An Actions execution, not merely committed code, is required to claim compiled/tested status.

## RQT-690 — conditional rational point constructor

`src/bin/rqt690.rs` implements the exact identity on `H=diag(Q,2)`:

`T_p(w)=H(w)p - 2 B(p,w) w`, with `B(p,w)=pᵀ H w`.

If a verified null seed `p=(x,y,z,d)` with `d ≠ 0` exists, this generates more exact rational solutions, normalizes their integer coordinates and checks every homogeneous norm identity. Without a seed it exits nonzero, and it **never fabricates** an authentic rational witness. GitHub Actions tests the invalid-seed gate and runs Rust unit tests, including a synthetic-seed proof of the algebraic identity. The mathematical existence theorem does not supply explicit seed coordinates.

```bash
cargo test --bin rqt690
cargo run --release --bin rqt690 -- 0 0 0 1  # expected REJECT; not a root
```

To construct original-source rational points, supply four exact integers for a *separately certified* primitive null seed. A reduced rational point still does not establish the original 22D divisibility-one root or frozen reflection chain.

## RQT-691 — corrected recursive spatial topology (canonical)

The former `3×8 | n | (8×3)` layout was **incorrect** and is superseded. Every peripheral position contains the same **structural grammar**, not a numerical 3×8 array:

```text
{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))

upperleftrear{{|}}   centerupper{{|}}   upperrightfront{{|}}
centerleftrear{{|}} CENTER{[(FOCUS)]}  centerrightfront{{|}}
lowerleftrear{{|}}   centerlower{{|}}   lowerrightfront{{|}}

Each | branches into two child | symbols:
               |
             /   \\
          | top  | bottom
           / \\      / \\
          |   |    |   |  ...
```

The labels are **spatial names**; the 3×3 rendering above is a schematic ordering, not a claim all nine positions are coplanar. Each `|` emits a top-child and bottom-child `|`, each retaining its original spatial position and a distinct T/B ancestry address. The focus does not branch. For complete expansion the peripheral depth-`d` node count is `8×2^d` (one center is separate). No inference is made here about chemistry, the dimension of the original quadratic form, or root existence.

`cargo run --release --bin rqt691 -- 8` checks these structural invariants. The previous rank-three arithmetic routines remain independent from this visualization/grammar layer.
