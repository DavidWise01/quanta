# QG-037 — Independent Closure Witness

**Invariant:** `|||| → final fold → independent unfolding → separate manifest → compare → preserve ||||`.

QG-036 produces a full nested [84211] tree. QG-037 traverses the **final folded tree directly**, without invoking QG-036 recovery or accepting `packet.source` as the expected answer.

The verifier independently unfolds the final tree and reconstructs the 8 ordered leaves (four identity leaves plus four complete 1311 chamber leaves). It checks exact equality to a **separately supplied manifest**, verifies every six-face chamber, compares intermediate stages reconstructed from the final tree, and rejects alteration of any recorded chamber or actor ordering.

**Important boundary:** The judge ruling and original event ledger are not encoded in the eight witness leaves themselves. QG-037 compares the source-wrapper ruling and events with the external manifest, rather than pretending it can derive them from an incomplete folded tree.

The external manifest must be saved independently and trusted. Creating a fresh manifest from a simultaneously tampered packet would defeat this comparison. The protocol does not establish document provenance, cryptographic signature, truth, actual Byzantine fault tolerance or quantum computation. The manifest is structurally checked with QG-035 event replay; that does not make the author genuine.

## Verification conditions

1. QG-035 manifest is valid, complete and ruled.
2. Final `1 → 1` carries the same nested tree.
3. Independent tree walk gives exactly eight original leaves in canonical actor order.
4. Every chamber has all six distinct interior faces and matches its manifest.
5. All 8/4/2/1 intermediate stages match independent reconstruction.
6. Ruling and event ledger match the independently supplied manifest.
7. No original report is modified and `interpretationProven:false` remains.

## Artifacts

- [Verifier kernel](./independent-closure.mjs)
- [Nine tests](../tests/independent-closure.test.mjs)
- [Interactive verification lab](../independent-closure.html)
