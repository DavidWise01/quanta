# QG-033 — Three-Witness Root Consensus

**Carrier:** `||||`. QG-032 kept two opposing observations of an existing prerequisite root. QG-033 records **three** individually named witnesses for the **same leaf root**, occupying three distinct 60-station phases.

## Witness placement

Given the original QG-029 subject glyph, bind the three roles to the same QG-028 60-ring stations `a`, `b`, and `c` (0°, 90°, 180°). The fourth quad remains reserved, not silently assigned. The symbolic witness slots are not social rankings.

Each witness has an ID, position (`supports`, `challenges`, or `undetermined`), statement, historical year, a labeled HTTPS source, and a declared independence rationale. Three distinct IDs **and** three distinct source hosts are required; that is a **weak structural diversity check**, not proof of independent authorship. Mirrors, coordinated publishers, and copied sources can remain correlated.

## Observable alignment vs truth

- All three support: `unanimous-support`.
- All three challenge: `unanimous-challenge`.
- All positions known but mixed: `split`.
- At least one undetermined: `incomplete`.

The system also reports the simple direction of majority for bookkeeping. **Neither majority nor unanimity validates historical truth.** The distinction between supporting evidence and a warranted conclusion still requires independent source reading.

An explicit review event can choose `support`, `challenge`, or `insufficient`, with a rationale and a labeled HTTPS citation. Review is separate from the original witnesses, and the QG-030 source root and any downstream claim wording remain unchanged.

## Invariants

1. Exactly three witness observations per trio.
2. All observations address one real QG-030/QG-031 leaf root.
3. Each witness has a unique identifier and a different cited HTTPS source host.
4. Context years are bounded by the historical root year and QG-029 contextual year.
5. Three source records and their ordered 60-station slots remain intact.
6. The append-only event history is replay-validated; review does not erase or rewrite witnesses.
7. A classified consensus always reports `interpretationProven:false`.

## Bounded implementation

Maximum 32 witness trios and 64 events in one session. IDs are local labels. Event replay and structurally checked URLs do not provide source authentication, content validation or cryptographic integrity. Exported JSON must be stored externally for persistence.

## Artifacts

- [Executable three-witness kernel](./three-witness-roots.mjs)
- [Seven regression tests](../tests/three-witness-roots.test.mjs)
- [Interactive lab](../three-witnesses.html)
