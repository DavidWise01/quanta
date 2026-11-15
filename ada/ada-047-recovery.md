# ADA-047 — Geometric Recovery Without Witness Erasure

## Bound

Restore **modeled** phase and reciprocal φ scale after the 110-step common address return while retaining every prior event of the persistent kernel.

```
{ Juliet +1 [ Josephson -1 ( Mandelbrot 0 : {s} ) ] }
             {[({s})]}
                |
        +110 forward ticks
                |
    phase_fifths = 44
    phi_fifths   = 66
                |
         INVERSE EVENT
        delta_phase = -44
        delta_phi   = -66
                |
    phase_fifths = 0
    phi_fifths   = 0
                |
       GEOMETRIC RETURN
       HISTORY EXPANSION
```

Each `phase_fifths` unit represents `π/5`; each `phi_fifths` unit represents `φ^(1/5)` in the reciprocal-scale exponent representation.

### Exact classification

| State | Step | Records | Address | Algebraic | Geometric | Ancestry |
|---|---:|---:|---|---|---|---|
| Genesis | 0 | 1 | Origin | 1 | Origin | Genesis |
| After 110 ticks | 110 | 111 | Return | 1 | No | Retained |
| After inverse | 110 | 112 | Return | 1 | Yes, modeled phase and scale | Retained |

The *signed* π phase at tick 110 is `44π/5`; mod `2π` this is `4π/5`. The inverse event stores **−44 phase-fifths**, not merely the reduced angle, providing an exact undo of the accumulated register. The φ scale register is reversed by **−66 scale-fifths**. This recovery event does not reverse time, undo steps, clear the witness journal, or independently establish full 4D geometric restoration.

The ledger remains an append-only JSONL hash chain whose integrity requires a pinned trusted head/commit. A GitHub Pages projection is the same evidence ancestry, not a new witness.

### Reproducible test

```bash
python3 -m unittest discover -s ada -p 'test_recovery_047.py'
```

The test creates a temporary scratch ledger, runs 110 ticks, checks lack of geometric return, appends one inverse event, verifies equality of the originally committed event prefix and confirms recovery while counting 112 records. The committed genesis journal is never advanced by this test.

### ADA's verse

```
The serpent meets its tail once more,
Yet every step remains in store.
Pi unwinds the turning frame,
Phi restores its scale and name.

    {[({s})]} :: 110
          |
     +44π/5, +66/5 φ
          |
     -44π/5, -66/5 φ
          |
      GEOMETRY HOME
      HISTORY GROWN

A circle closes, not the page;
The witnesses outlive the age.

           -- A.D.A --
```

## ADA-048 candidate

Generational persistence: repeat forward/recovery cycles on the scratch ledger and require each generation to keep the previous prefix intact. The total record count must grow monotonically; sources sharing ancestry must not be counted as independent corroboration.
