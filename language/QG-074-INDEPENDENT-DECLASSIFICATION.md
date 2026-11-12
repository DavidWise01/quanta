# QG-074 — Declassification Requires Independent Authority

## Invariant

An agent may propose a public release from gated-derived material, but **may not approve its own declassification**. The QG-073 gated node remains immutable and gated. The newly proposed public artifact is a **different object**, reviewed against exact bytes and full ancestry by three independently pinned reviewer keys and their separately declared ancestry roots.

```text
           QG-073 GATED DERIVATION
                     |
             PROPOSE NEW ARTIFACT
                     |
            PINNED EXACT BYTES
                     |
        +------------+-------------+
        |            |             |
      ROOT A       ROOT B        ROOT C
        |            |             |
        +------------+-------------+
                     |
           VERIFY ALL ED25519 VOTES
                     |
              QG-072 PUBLISH SCOPE
              /               \
          APPROVED            DENIED
             |                  |
        DISTINCT PUBLIC     KEEP PRIVATE
         RELEASE RECORD         |
             |                  |
             +---------+--------+
                       |
                     {{i}}
```

## Executable boundary

QG-074 consumes a QG-073 event ledger and an **independently pinned** registry digest and reviewer policy. The reviewed payload binds a source node ID and hash, exact graph hash, gated classification, upstream ancestry roots, origin surfaces, SHA-256 of the proposed exact public bytes, release destination `0root.ai`, release sequence and previous signed release hash.

At least three **distinct signed votes from reviewers assigned distinct pinned root ancestries** must verify against Ed25519 public keys in the independent reviewer registry. A duplicate reviewer, a forged signature, a shared upstream root, replaced release text, altered source ancestry, or wrong reviewer registry fails. The approval appends by value; it never modifies any original gated QG-073 node. Release approval itself is insufficient to publish: a separate, active QG-072 **issuer-signed `publish @ 0root.ai`** capability must also pass. That scoped authorization concerns the distinct reviewed public artifact; the original gated node is still restricted.

The independent `minReleaseSequence` detects replay of an earlier valid state only when advanced and durably stored outside the record. The synthetic implementation permits sequential approved releases, using a hash link to earlier release events.

## Important limitations

- **Three reviewer signatures cannot prove that a proposed release actually excludes confidential facts.** Reviewers in this demo are simulated signers, and ancestry independence is declared by pinned policy rather than independently proved in the real world. Human/legal/editorial review and authenticated information-flow enforcement are required before any live publication.
- The public release artifact is separate; there is no general mechanism here for the declassification of gated QG-073 graph nodes or automatic propagation of public status.
- The model does not access private GitHub repositories, alter 0root.ai, or publish anything. Keys and claimed approvals are synthetic.
- QG-062–073 trust boundaries still apply: GitHub/0root.ai share owned source ancestry but are distinct confidentiality surfaces, and external internet is not automatically a publication destination.

Test:
```sh
node --test tests/provenance-transformation.test.mjs tests/independent-declassification.test.mjs
```
