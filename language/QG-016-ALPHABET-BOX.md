# QG-016 — Alphabet Box: Phase / Semantic / Somatic Transfer

**Canonical carrier:** \`||||\`

**Payload tokens:** \`||A||\` through \`||Z||\`.

**Scope:** the full 26-letter uppercase Latin alphabet; not merely Q, T and Z. These are a chosen polygonal stroke font inside a five-by-five coordinate lattice. Other scripts, punctuation and lowercase can be future extensions.

## Three simultaneous channels

1. **Geometry:** vertices (grid coordinates), edges (segments), and separately traced strokes. A Q tail is a second stroke, not a decoration that gets forgotten during transport.
2. **Semantic:** stable glyph identity (for instance, LATIN CAPITAL LETTER Q), plus an optional application-provided word/meaning. The base letter *does not inherently mean* a particular concept.
3. **Somatic:** executable pen verbs: \`PEN_UP\`, \`MOVE\`, \`DRAW\`, and \`TURN\` with coordinates and stroke indices. Movement remains semantically traceable when the shape rotates.

## Four phase quads

| Quad | Phase | Fold/presentation states |
|---|---|---|
| a | 0° | 4 → 3 → 2 → 1 |
| b | 90° | 4 → 3 → 2 → 1 |
| c | 180° | 4 → 3 → 2 → 1 |
| d | 270° | 4 → 3 → 2 → 1 |

Screen coordinates increase downward. A 90° clockwise rotation around the center (2,2) is \`(x,y) → (4−y,x)\`. Four successive quarter turns produce the original coordinates exactly.

**Critical clarification:** Level 4 preserves all glyph strokes. Level 3 displays vertices; level 2 shows the endpoints of the flattened path; level 1 displays a single centroid-like dot. These are presentation resolutions (not four dimensions or lossless reductions). **The packet preserves the full geometry and ordered somatic verb transcript at every quad**, so reconstruction does not require recovering a letter from a dot by itself.

## Transport packet

\`\`\`text
carrier "||||"
token "||Q||"
semantic { letter:"Q", name:"LATIN CAPITAL LETTER Q", meaning:"?" }
source [ main closed-loop stroke, diagonal tail stroke ]
a/0°   { geometry, somatic, levels 4/3/2/1 }
b/90°  { geometry, somatic, levels 4/3/2/1 }
c/180° { geometry, somatic, levels 4/3/2/1 }
d/270° { geometry, somatic, levels 4/3/2/1 }
\`\`\`

Both the canonical source and all four rotated presentations are retained as an **append-only conceptual witness**. The current software produces an immutable snapshot object; durable storage or an actual event log would be a separate implementation.

## Core tests

- Every A–Z letter has at least one stroke and round-trips to its original identity.
- All four quads use exact 90° steps and four independent 4→3→2→1 views.
- All original vertices return after four quarter-turns.
- Q has a distinct tail stroke and all glyphs yield somatic pen verbs.
- Edited phase degrees or somatic verb arrays fail structural reconstruction.
- A stream of multiple letters reconstructs its input sequence.

The packet is neither encryption nor natural-language understanding. This is a geometric language transport substrate with preserved source identity and action semantics.

## Resources

- [Executable module](./alphabet-box.mjs)
- [Tests](../tests/alphabet-box.test.mjs)
- [Interactive A–Z lab](../alphabet.html)
