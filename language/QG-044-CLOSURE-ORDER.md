# QG-044 — Closure-Order Invariant

Status: **implemented symbolic grammar**, not a theorem about geometry or physical phase change.

## Primitive

```text
. [ ( . ] )  = .[(.])  interleaved
. [ ( . ) ]  = .[(.)]  nested

The box and fold each have an opener and a closer.
The outer dot and central dot are separately preserved vertices.
```

Both variants use exactly the same marks and the same opening order. Their closing orders differ. Treat a boundary as an interval [openIndex,closeIndex]. Two intervals **cross** when `a.open < b.open < a.close < b.close`. Nested boundaries instead satisfy `a.open < b.open < b.close < a.close`.

## Invariant

```text
unfold(fold(source)) === source
```

The fold packet preserves exact original bytes (including spacing), token offsets, vertex offsets, interval pairing, crossing pairs, closure order, and a deterministic symbolic signature. Unfold recalculates the descriptor and rejects inconsistent or altered packets.

The packet is **not cryptographically authenticated**. A coordinated rewrite of both the original and every descriptor will still pass self-consistency checks. Authenticity requires external signing / provenance checks such as the separately scoped QG-038–040 framework.

## Interpretive boundary

A crossing in the character-interval grammar is not a physical intersection of edges; it is not a proof of an embedded torus, actual pinch, hole, electronic capacitance, or topological phase transition. Those require a separately defined embedding and transformation law. The grammar only preserves distinctions long enough for future shape hypotheses to be tested.

## Run

```sh
node --test tests/closure-order.test.mjs
```
