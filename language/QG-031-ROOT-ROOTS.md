# QG-031 — Root Roots: Forward Propagation

**Carrier:** `||||`.

QG-030 “Chasing Roots” walks **backward** from an interpretation through dependencies. QG-031 “Root Roots” walks **forward** whenever the evidence at one or more prerequisite *leaf roots* changes.

## Natural invariant

```text
WHICH MEANS ─→ REQUIRES ─→ ROOT A ─→ evidence
             └→ REQUIRES ─→ ROOT B ─→ evidence

new evidence arrives at ROOT A
     │
     └→ reverse dependency edges
           └→ every dependent statement
                └→ WHICH MEANS marked for review
```

Root Roots maintains an **append-only ledger** of complete canonical QG-030 snapshots. Each update is a new revision `p0001`, `p0002`, ... with parent link, updated root IDs, and canonical impacted-node addresses. Previous revisions remain exactly recoverable.

- Only *leaf nodes* (those with zero `requires` links) can have their **status** and **evidence links** updated.
- An update with no actual change is rejected.
- Simultaneous independent root updates share dependents without duplicating them.
- Propagation never rewrites parent claim text, social context, ordinal ratings, or dependent statuses.
- An impact is **“needs review”**, *not* a logical proof, a claim of truth, or automated fact-checking*.
- An HTTPS link records supplied evidence metadata; the kernel cannot verify that the linked source supports the claim.

## Functions

- `instantiateRootPropagation(source)`: preserve original root DAG.
- `propagateRoots(ledger, updates, comment)`: append evidence changes and trace affected nodes.
- `inspectRootImpact(ledger, revisionId)`: return affected addresses and review status.
- `recoverRootRevision(ledger, revisionId)`: recover exact historical source snapshot.
- `verifyRootPropagation(ledger)`: check every snapshot and parent/update transition.

QG-031 uses QG-030's bounded graph of up to 60 nodes and 180 links. Propagation history has a maximum of 32 snapshots. JSON export is required for persistence beyond the current browser session. Source fingerprints detect uncoordinated accidental tampering, not adversarial rewrites.

## Artifacts

- [Executable propagation kernel](./root-propagation.mjs)
- [Seven regression tests](../tests/root-propagation.test.mjs)
- [Interactive Root Roots viewer](../root-roots.html)
