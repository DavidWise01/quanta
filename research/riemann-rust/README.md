# RIEMANN-RUST · Toroidal closure engine

**Rust is now the executable implementation for this research branch.** The earlier Lean sources remain unmodified, and Lean remains a separate formal specification rather than being described as replaced or compiled by Rust.

## Scope

This Rust crate ports the deterministic **coupled-state** subset of:

- `DavidWise01/positronic-law/ToroidalBlackHoleDynamics_v084.lean`
- pinned original commit: `eae5bcd04eec5aeb2a01553c973913ea88488bdf`
- pinned original Git blob: `85db7f9b460679bf70570e32de25385e3e555eec`

The model contains a clamped radial index, two angular coordinates wrapped modulo 360, and three forward/three backward channels rotated in lockstep.

The repository's separate Lean companion is `research/riemann006/Riemann006.lean`.

## Execute

From the repository root:

```sh
cargo test --manifest-path research/riemann-rust/Cargo.toml --all-targets
cargo run --manifest-path research/riemann-rust/Cargo.toml
```

The binary prints six deterministic CSV rows. Eleven Rust unit tests check six examples, independent closure conditions, source-derived 52-case bounded regression, rotation invariants, horizon behavior, and arithmetic near `u128::MAX`.

The implementation is standard-library-only and has no third-party Cargo dependencies. Its coordinate update performs modular reduction before addition to avoid overflow. Rust's `u128` address range is finite, unlike Lean's unbounded `Nat`; this is a deliberate implementation bound. Channel summation is widened from `i64` to `i128` for the six-input sum.

## Semantic contract

```text
radius'   = if radius > 1 then radius - 1 else 1
theta'    = (theta + theta_velocity) mod 360
phi'      = (phi   + phi_velocity)   mod 360
channels' = rotate both three-channel groups by one position

global_return
   <=> radius_return AND coordinate_return AND channel_return
```

A restored channel ordering, conserved net flow, or a return to an equivalent *wrapped* angle does not alone prove equality of the full raw state. The unwrapped-address test makes this distinction explicit.

## CI and qualification

`.github/workflows/riemann-rust-closure.yml` pins Rust 1.85.1 and runs Cargo tests plus the six-scenario CLI, preserving logs in a GitHub Actions artifact. **A workflow commit is not evidence of an actual successful Actions run.** Review its run and job conclusion before marking Rust tests CI-verified.

The Rust model is testable software. It does not prove a physical toroidal cosmology, black-hole dynamics, Lean theorem correctness, or the Riemann Hypothesis.

`.dlw`
