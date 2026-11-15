# ADA-046 · Persistent Kernel Charter

**State:** a committed, deterministic, replayable mathematical kernel. This is not a self-running autonomous agent and not a verified quantum chemistry simulation.

## Source of truth

- `kernel.py` implements deterministic symbolic transformations with the Python standard library.
- `kernel/events.jsonl` is a hash-linked, append-only local journal, beginning with a synthetic genesis event.
- Each event stores `seq`, `prev`, `kind`, `ancestry`, `state` and SHA-256 digest of canonical JSON.
- Only a single writer is supported. The local append operation uses fsync, but cannot guarantee a transaction across crashes; an incomplete tail fails verification.
- Git commits provide durable, versioned snapshots **when changes are committed and pushed**. Local appends are not automatically mirrored.
- `ada-kernel.html` is a **read-only** GitHub Pages compatible HTML projection, not a second independent witness.

## Canonical structure

```
{ Juliet +1
  [ Josephson -1
    ( Mandelbrot 0 : {s} )
  ]
}
{[({s})]}
```

One manifold, three mini-states, 2/5 internal π phase steps and 3/5 external φ scale steps. Signed 11-position `-5..+5` ouroborus and two-turn spinor counter; first common positive address return is `lcm(11,5,2)=110`.

`phase_fifths` stores the phase as an exact integer multiple of π/5. `phi_fifths` stores the reciprocal amplitude exponent as an exact integer multiple of 1/5: `a=φ^(phi_fifths/5)/3`, `b=φ^(-phi_fifths/5)/3`, `c=1/3`. Thus `27abc=1` symbolically, regardless of the exponent.

A `tick` increments either the phase register on beats 1–2 or the scale exponent on beats 3–5. A `recover` event explicitly applies the inverse of accumulated phase and scale. This restores the **modeled phase and scale**, but does not delete steps, restore arbitrary physical degrees of freedom, or independently validate an experiment.

## Use

From repository root:

```bash
python3 ada/kernel.py verify
python3 -m unittest discover -s ada -p 'test_kernel.py'
python3 ada/kernel.py tick --count 110 --ancestry synthetic:fixture
python3 ada/kernel.py status
python3 ada/kernel.py recover --ancestry synthetic:fixture
python3 ada/kernel.py verify
```

Do **not** run the 110-step demonstration on the committed baseline unless intentionally advancing the real journal. Instead copy the ledger to a scratch path and pass `--ledger scratch/events.jsonl`.

## Witness rules

One ancestry label is **not** three independent witnesses. Mirrored GitHub and Pages surfaces share one source root. Hash-chain integrity detects modification only when a previously trusted head hash or Git commit is pinned; anyone able to rewrite the ledger and all hashes could forge a new chain. Protect the original commit reference, require independent witnesses before promoting evidence, and preserve all original events. Never publish gated source material on Pages.

## Next ADA-047

Run an explicit 110-step demonstration on a scratch ledger, append an inverse correction event, verify geometrical phase/scale restoration and ensure the full lineage is still recoverable. Record separate source roots before making any corroboration claim.
