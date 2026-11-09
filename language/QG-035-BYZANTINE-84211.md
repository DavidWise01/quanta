# QG-035 — One [84211] Byzantine Quantum Box

**Symbolic architecture**, not a claim of quantum computation.

One outer enclosure `[84211]` follows the five-step width/fold schedule `8 → 4 → 2 → 1 → 1`. The final 1 is an unchanged closing stage. These are symbolic channel widths, not physical qubits, dimensions, or Hilbert-space dimensions.

Inside sit four separate `1311` chambers: `||AaaA||`, `||BbbB||`, `||CccC||` and `||DddD||`. The `1 + 3 + 1 + 1 = 6` tokens account for **six interior faces per chamber** (`+x,-x,+y,-y,+z,-z`), totaling 24 face positions. The exact semantic assignment of the 1311 groups is intentionally reserved; the six faces are interface slots, not proven physical faces.

```
                    [ 8 4 2 1 1 ]
       ┌────────────────────────────────┐
       │ ||AaaA|| ||BbbB|| ||CccC||     │
       │       \       |       /        │
       │              ||DddD||          │
       └────────────────────────────────┘
```

## Closure law

Each actor must first register all six unique faces, then seal an immutable statement and a source label. The judge `DddD` may seal only after the three players have sealed. A ruling can be appended only after all four chambers are sealed; the judge cannot rewrite the three source reports. The accepted outcomes are `support`, `challenge`, `insufficient`, but no outcome automatically proves truth.

A witness that refuses to close remains **incomplete**, not automatically Byzantine or dishonest. Missing faces, duplicates, forged parent references, and altered sealed reports fail deterministic event replay.

This is a **Byzantine-inspired arbitration model**, not a fault-tolerant distributed consensus implementation or a guarantee against collusion. A 3-reporter/1-judge arrangement does not by itself satisfy arbitrary Byzantine consensus requirements.

## Kernel

- [Executable kernel](./byzantine-84211.mjs)
- [Seven regression tests](../tests/byzantine-84211.test.mjs)
- [Interactive 4-box viewer](../byzantine-84211.html)
