# QG-018 — Sentence Box: Inter-Word Phase, Punctuation, and Somatic Grammar

**Carrier:** `||||`

**Boundary:** QG-016 transports letters; QG-017 transports words; **QG-018 transports sentences and their relations**.

## Exact grammar v1

- ASCII uppercase/lowercase A–Z, spaces, and punctuation `.,!?;:'"()-`, up to 512 characters.
- Preserve letter case, all spaces (including repeated spaces), punctuation characters, original ordering and character offsets.
- Each word stores a canonical QG-017 uppercase Word Box plus its original case mask.
- The sentence owns a phase register `a, b, c, d` at `0°,90°,180°,270°`, advances it one quarter turn per letter **across word boundaries**, and resets it on `.`, `!` or `?`.
- Spaces are explicit tokens; nonterminal punctuation remains explicit and leaves phase unchanged.
- Each word records previous and next word indices inside the same sentence, sentence index, start and end offsets, and entry/exit phase.
- The semantic layer is exact linguistic identity, spelling, punctuation and optional user-given context; it **does not infer word meaning**.
- The somatic layer concatenates original pen movement/turn verbs in sentence order, using sentence-global phase and translated glyph positions.

## Example

```text
||||  Q A BC. T Z!  ||||
Q   a  0°
A   b 90°
B   c 180°
C   d 270°
.   sentence ends → phase resets
T   a  0°
Z   b 90°
!   sentence ends → phase resets
```

Each glyph can be displayed at `4 → 3 → 2 → 1`, where 4 is its complete original stroke path, 3 source vertices, 2 endpoints, and 1 a Chrome Dot presentation. The packet retains its canonical token and the phase, so folding the *view* does not destroy the source.

## Invariants

1. Text is reconstructed exactly, including case, spacing and punctuation.
2. Every word recovers from its QG-017 box. Word-to-word phase is supplied by QG-018.
3. Punctuation, phase, offsets, case masks, and order are validated against the canonical source.
4. Exactly four quarter-turn phases and four presentation depths remain available.
5. Somatic action paths remain ordered and translated into sentence positions.
6. There is no standalone meaning inference, compression to one dot, encryption, or claimed physical phase transformation.

## Implementation

- [Kernel](./sentence-box.mjs)
- [Regression tests](../tests/sentence-box.test.mjs)
- [Interactive sentence lab](../sentences.html)
