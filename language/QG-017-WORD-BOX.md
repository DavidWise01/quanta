# QG-017 — Word Box: Phase–Semantic–Somatic Composition

**Carrier:** \`||||\`

**Words:** ordered sequences of \`||A||\` through \`||Z||\` tokens with explicit spaces.

**Natural boundary:** A single letter is a reversible unit in QG-016; a **word or phrase** needs ordering, word boundaries, shared phase scheduling and spatial offsets in addition to its individual geometry and pen strokes. The carrier now owns the composition, not just a series of disconnected glyphs.

## Deterministic grammar (v1)

- Accept 0–128 characters: uppercase A–Z words separated by **one** space; no leading/trailing whitespace.
- Each letter is a QG-016 canonical \`||LETTER||\` reference, with its original stroke/vertex geometry recoverable from the built-in dictionary.
- Each letter increments a phase counter \`a→b→c→d→a\`, or \`0°,90°,180°,270°,0°\`.
- Each space is a real transport token (width 2) and resets the phase to \`a\`.
- A glyph advances horizontal composition by six coordinate units (stroke grid width four + two spacing).
- Glyphs retain \`levelSchedule=[4,3,2,1]\`, preserving their full canonical geometry as a referenced witness even when level 1 displays a single dot.

## Three synchronized layers

1. **Geometry:** reconstruct rotated stroke paths for every character at its ordered word offset.
2. **Semantic:** reconstruct exact characters and word boundaries; an optional context string travels with the packet, but word meanings are *not automatically inferred*.
3. **Somatic:** replay \`PEN_UP\`, \`MOVE\`, \`DRAW\`, \`TURN\` in the same glyph/word index sequence. The pen verbs are transformed by each letter's selected quarter-turn phase.

## Fold and recovery

\`\`\`text
||||  QUANTA GLOBULE  ||||
 Q(a,0°) U(b,90°) A(c,180°) N(d,270°) T(a,0°) A(b,90°)
 [SPACE resets phase]
 G(a,0°) L(b,90°) O(c,180°) B(d,270°) U(a,0°) L(b,90°) E(c,180°)
   ↓ level 4 geometry
   ↓ level 3 vertices
   ↓ level 2 endpoints
   ↓ level 1 chrome dot per letter
   ↑ canonical source glyph reference + phase + order + spaces
   = QUANTA GLOBULE
\`\`\`

The dot alone does not determine a letter, word, or meaning: source references, phases, and spacing are retained in the full word packet. These are **presentation levels**, not physical dimensional transitions. A JSON packet is not encryption and has no independent cryptographic authenticity.

## Tests

- Round-trip A–Z, sample phrases and empty input with exact spacing preservation.
- Ensure a/b/c/d cycling, 90° changes and reset after each word.
- Ensure 4/3/2/1 fold views never delete the recoverable source identity.
- Ensure Q retains its tail stroke, with its MOVE/DRAW/TURN verbs.
- Reject invalid spaces/characters and tampered ordering, phase, or coordinates.
- Build semantic context and somatic transcripts for the entire word sequence.

## Files

- [Executable composition kernel](./word-box.mjs)
- [Automated tests](../tests/word-box.test.mjs)
- [Live word composer](../words.html)
