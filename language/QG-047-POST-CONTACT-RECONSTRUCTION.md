# QG-047 — Post-Contact Reconstruction

**Status:** explicit finite graph contraction, verified incidence and face counts. A singular contact by itself is not a new valid topology.

```text
            BEFORE
      C -- R0  CONTACT
            |
     MERGE C AND R0
            |
     C+R0 (NEW LABEL)
            |
     REMOVE SELF-LOOP
            |
     DEDUPLICATE EDGES
            |
     RECOMPUTE V,E,F
            |
       REPLAY LINEAGE
            |
            AFTER
```

## Precisely defined operation

QG-046 uses radial factors `r_i(s)=1-s(0.55+0.45*cos(k*2*pi*i/n))`. QG-047 fixes `k=1` by default, ensuring precisely one first-contact outer vertex at `s=1` for `n>=3`. Other `k` values are accepted only if they also have *exactly one* contact; multiple simultaneous contacts are explicitly rejected by this single-edge surgical operation.

The initial embedded wheel graph has vertices `C,R0,...,R(n-1)`, `n` rim edges, `n` spoke edges, `V=n+1,E=2n,F=n+1` (including exterior). Identify `C` and `R0` as the named survivor `C+R0`. A graph contraction removes `spoke:0` as a self-loop and deduplicates the two resulting pairs of parallel rim/spoke edges. The output is a **simple graph** with `V'=n,E'=2n-3,F'=n-1`, and Euler `V'-E'+F'=2`.

The preserved `edgeLineage` contains one entry for every original edge, including those dropped or merged. The `vertexMap` explicitly identifies the two originals that become one. All original vertices, coordinates, edges, and the collision parameter are retained in the certificate. Both the original and successor are non-authenticated data structures; an external signature or append-only store would be needed to prevent coordinated rewrites.

## Geometric verification

With the pinched radial coordinates, each remaining outer radius is positive and successive angles preserve order. There are `n-2` positive bounded triangular fan faces in the reconstructed planar successor and one exterior face. These checks are specific to the declared pinching family and are not a proof that all possible post-contact surgeries are safe.

**Important:** the abstract graph's Euler characteristic remains 2, but vertex/edge/face counts have changed. This is a graph contraction, not evidence of a physical torus, hole formation, or an actual topological phase transition.

## Run

```sh
node --test tests/center-pinch.test.mjs tests/first-broken-edge.test.mjs tests/post-contact-reconstruction.test.mjs
```
