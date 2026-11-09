# QG-045 — Center-Pinch Conservation

**Status:** implemented small Euclidean geometry model and deterministic replay; no physical toroid or continuous-topology theorem claimed.

## WHAT / WHY

```text
 n boundary vertices + 1 center vertex
              |
       n ring edges
       n radial edges
              |
       pinch coordinates
              |
   check every triangular face
   check nonincident edge crossings
              |
       keep graph fixed
              |
     replay full history
```

The model is the **wheel graph**, drawn in the plane with an interior center joined to every outer vertex. The Fibonacci walk `1/1/2/3/5/8/13` is used as a sequence of seven *allowed observation/pinch strength checkpoints*, not as a claim that one polygon is simultaneously a torus and a box. Test outer counts `n=3,4,5,8,13`.

For an initial `n`-ring:

- vertices `V=n+1` (including center)
- edges `E=2n` (ring plus spokes)
- faces `F=n+1` (n bounded triangular faces plus the exterior)
- Euler characteristic `V-E+F=2`.

Pinch events move the center by a bounded `dx,dy`, scale radial vectors by `1-strength*(.55+.45*cos(lobes*theta))`, and preserve the original ring order and edge incidence. Candidate geometry is rejected if triangle faces degenerate or reverse, or if a pair of nonincident edges crosses. Every pinch checks 19 intermediate samples and the endpoint; sampling is a computational safeguard, **not** a proof against every possible continuous crossing between samples.

An append-only *value-based* ledger records all actions and prior/next geometry. Replaying it checks exact deterministic snapshots and invariants. The ledger can be copied and altered wholesale; authenticity must come from an external trusted signature/append-only store, not this self-consistency test.

**Boundary:** Same graph topology under a deformation does not establish a torus, a new physical phase, a capacitance law, or an electromagnetic mechanism. A pinched silhouette is still the same wheel graph until a mathematically defined surgery changes its connections.

## Run

```sh
node --test tests/center-pinch.test.mjs
```
