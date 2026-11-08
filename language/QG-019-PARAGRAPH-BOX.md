# QG-019 — Paragraph Box: Lines, Context and Sentence Relations

**Carrier:** \`||||\`.

The paragraph is the next compositional boundary after letters (QG-016), words (QG-017) and sentences (QG-018).

## Language

- Exact permitted input: ASCII A–Z and a–z, spaces, \`.,!?;:'"()-\`, and LF (\`\\n\`) line breaks; maximum 4096 characters.
- Keep all original character offsets, original case, punctuation, repeated spaces and blank lines.
- Each line is segmented at sentence-ending punctuation groups (\`.\`, \`?\`, \`!\`). Segment lengths beyond 512 characters are divided into consecutive 512-character chunks to meet the QG-018 input bound.
- Each sentence fragment gets a canonical QG-018 Sentence Box.
- Every fragment records its globally ordered sequence index, line index, source offset and links to previous / next fragments.
- Line break is itself a separate transport token.
- A paragraph can include optional **user-provided contextual meaning**. No intrinsic or emergent semantic understanding is implied.
- The phase resets inside each QG-018 sentence and does not otherwise cross independently serialized sentence fragments. This preserves QG-018's per-sentence phase semantics.
- The whole packet is structurally verified by recomputing expected word/sentence/paragraph records from the explicit original source.

## Transport and fold

\`\`\`text
||||   One dot. Another.
       The box returns.    ||||
         ├─ line 0
         │  ├─ sentence fragment 0 → fragment 1
         └─ line 1
            └─ sentence fragment 2

4: original QG-016 strokes
3: source vertices
2: endpoints
1: Chrome Dot view (one dot per glyph)

↑ inverse via the retained canonical source, sentence records and link witnesses
= exact original paragraph
\`\`\`

A dot is a *presentation* only. It does not independently encode the paragraph. The actual transport packet retains the explicit source text and links to its underlying geometry.

## Invariants

1. Every original byte (for the permitted ASCII grammar) recovers exactly.
2. Line breaks and blank lines are not normalized away.
3. Segment indices, source offsets and relationships are regenerated to detect mutation.
4. Every nested sentence reconstructs through QG-018 and its inner QG-017 word boxes.
5. Levels \`4/3/2/1\` share the exact glyph count and canonical source references.
6. The context is explicit reader/user-supplied metadata, not automated interpretation.

## Implementation

- [Paragraph kernel](./paragraph-box.mjs)
- [Seven regression tests](../tests/paragraph-box.test.mjs)
- [Interactive Paragraph Box](../paragraphs.html)
