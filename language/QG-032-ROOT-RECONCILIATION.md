# QG-032 — Root Reconciliation

**Carrier:** `||||`. QG-030 traces backward to roots. QG-031 propagates root updates forward. QG-032 keeps **two opposing observations of one root** in an append-only reconciliation history.

## Rule

`|||| → ROOT → {supporting observation | challenging observation} → OPEN → REVIEW → ||||`

Each observation includes a unique ID, leaf-root address, position (`supports` or `challenges`), statement, observed year, supplied HTTPS evidence links and an explicit question that would settle the disagreement. An encounter requires two different observations concerning the *same existing leaf root* with opposite positions.

Every encounter records its exact original QG-030 source context and the reachable downstream claims via reverse dependency edges. The conflict remains `open` until an explicit human decision—`support`, `challenge`, or `insufficient`—is appended, accompanied by a rationale and at least one source link. A reviewed conflict keeps **both original observations** and every earlier event.

## Invariants
1. No observation or decision silently changes a QG-030 source statement or dependent claim status.
2. Two different rooted observations are preserved in order; contradiction is not silently discarded.
3. Event history is strictly append-only and replayed against a validated source graph.
4. The same root can have many separate conflicts; each receives a local conflict address.
5. Review is a documented assessment and never automatic historical truth.
6. Missing citations, unsupported IDs, invalid times and repeated decisions fail closed.
7. Recomputed impact includes all dependent statements, with no duplicate node IDs.

## Scope and limitations
QG-032.1 supports a maximum of 32 conflicts and 64 events in a session. It accepts a QG-030 root packet or the latest validated QG-031 propagation snapshot. Observation year is bounded by the historical root and the source context year. An IANA timezone is preserved through the QG-029 nested source; it is not itself a social-rank score. Supplied HTTPS URLs are **not independently checked** for agreement with statements. Replay is structural verification, not cryptographic identity or historical proof. Export JSON for persistence.

## Artifacts
- [Kernel](./root-reconciliation.mjs)
- [Seven regression tests](../tests/root-reconciliation.test.mjs)
- [Interactive Root Reconciliation lab](../reconcile.html)