# RIEMANN-010 · Rust/WASM Toroidal Universe Laboratory

The executable state engine is Rust. The browser's neon toroidal mesh is a Canvas2D projection over Rust-computed state. Lean remains an independent formal reference; neither Rust nor WebAssembly changes the original Lean sources.

## Locations

- Rust model: `research/riemann-rust/src/lib.rs`
- WASM adapter: `research/riemann-wasm/src/lib.rs`
- Browser viewer: `docs/riemann-rust/index.html`
- Compiled artifact: `docs/riemann-rust/toroid.wasm` (published by CI)
- CI build and publication: `.github/workflows/riemann010-rust-wasm-pages.yml`
- Actual-binary smoke test: `research/riemann-wasm/smoke.mjs`

## Build and verify

```bash
rustup toolchain install 1.85.1 --component rustfmt --target wasm32-unknown-unknown
cargo +1.85.1 test --manifest-path research/riemann-rust/Cargo.toml --all-targets
cargo +1.85.1 test --manifest-path research/riemann-wasm/Cargo.toml
cargo +1.85.1 build --manifest-path research/riemann-wasm/Cargo.toml --target wasm32-unknown-unknown --release
cp research/riemann-wasm/target/wasm32-unknown-unknown/release/quanta_toroidal_wasm.wasm docs/riemann-rust/toroid.wasm
node research/riemann-wasm/smoke.mjs docs/riemann-rust/toroid.wasm
```

The workflow executes and records both Rust test suites, verifies the WASM magic header, runs Node's real WASM runtime against all six counterexamples, and publishes only the compiled WASM asset to the existing root Pages tree. The main QUANTA homepage is preserved; a navigation link to this lab is appended.

**Browser loading is fail-closed:** if `toroid.wasm` cannot be fetched or the exported ABI is not v10, controls remain disabled and the interface displays HOLD. The visualization does not silently fall back to a JavaScript simulation.

## Contract

The discrete CoupledState includes radius (horizon clamp), two coordinates modulo 360, and forward/backward three-channel permutations. Complete equality means all fields return exactly, not merely modulo equivalence or channel-only cycle closure. Rust `u128` models a bounded subset of Lean's `Nat`; this does not prove an entire physical universe or any RH theorem.

Current evaluation statuses are recorded separately in the numbered evidence manifest. Do not treat a committed workflow as evidence of its completion.

`.dlw`
