# QG-020 — Corpus Box

**Carrier:** `||||`.

The natural composition boundary after letters, words, sentences and paragraphs is a **corpus with documents, chapters, sections, source references and stable addresses**.

## Structured source

A corpus is a source object with `title`, `documents`, and `references`. Each document has a lower-case slug ID, title, and ordered chapters. Each chapter has its own ID, title, and ordered sections. Each section has an ID, title, and ordered paragraph texts. Paragraphs use QG-019 verbatim, so exact case, LF line breaks, spaces, punctuation and nested somatic stroke actions survive.

An address is an explicit tree path:

```text
doc/quanta
doc/quanta/ch/zero
doc/quanta/ch/zero/sec/opening
doc/quanta/ch/zero/sec/opening/p/0
```

Slug IDs are unique within their enclosing scope. Paragraph indices are stable *within an immutable snapshot*, and remain stable as long as earlier paragraphs are not inserted or deleted. For cross-version permanence, future revisions need explicit paragraph IDs and a versioned migration ledger; this version does not claim that reordering leaves numeric indices unchanged.

## Explicit reference verbs

References are typed links from one known address to another, e.g.:

```text
from: doc/quanta/ch/zero/sec/opening/p/0
to:   doc/quanta/ch/gap/sec/transport/p/0
relation: continues
```

Every endpoint must exist. Links are structured, ordered references, **not automatically inferred semantic equivalences**. Labels and contexts remain human-assigned.

## Fold views

For each paragraph, all four levels from QG-019 remain accessible:

- 4: full source stroke paths
- 3: vertices
- 2: endpoints
- 1: Chrome Dot view per letter

The complete corpus packet retains structured source, all nested paragraph witnesses and a direct address index. The visible dot alone never reconstructs the corpus.

## Validation gates

1. Exact round trip for documents, chapters, sections, paragraphs, including empty paragraphs.
2. Deterministic traversal order and unique scoped IDs.
3. Valid references resolve to known addresses; dangling references rejected.
4. Word/sentence/paragraph geometry and ordered somatic actions are inherited from QG-016–019.
5. Levels 4 and 1 preserve identical glyph counts.
6. Altered source witness, link order, address index or paragraph records fail deterministic reconstruction.
7. Limits: at most 8 documents, 16 chapters per document, 16 sections per chapter, 32 paragraphs per section; each paragraph obeys QG-019's 4096-character maximum.

**Status:** Computational transport language. Not a cryptographic protocol, universal alphabet, compression method, semantic understanding engine, or a physical 11-dimensional corpus.

## Artifacts

- [Corpus kernel](./corpus-box.mjs)
- [Tests](../tests/corpus-box.test.mjs)
- [Interactive corpus lab](../corpus.html)
