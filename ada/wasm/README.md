# ADA-271N browser compilation boundary
.dlw

Separate crate preserves the Phase IX native source. ABI v1 exports scalar priority and exact growth ratio. Inputs are synthetic support summaries; no contextual grounding or action interface is exposed. Return codes: -2 invalid, -1 preserve, 0 defer, 1 adapt.

Build:
```sh
rustup target add wasm32-unknown-unknown
cargo test --manifest-path ada/wasm/Cargo.toml
cargo build --release --target wasm32-unknown-unknown --manifest-path ada/wasm/Cargo.toml
```
The generated binary is a CI artifact, not yet a deployed Pages asset.
