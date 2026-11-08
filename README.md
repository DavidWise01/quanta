# QUANTA · The Wordle of Space

**David Lee Wise** · An evolving visual language and reader companion to the book.

> Start at zero. Make a mark. Discover a relationship.

## Security status

**Security audit: NOT APPROVED for sensitive/production data.** The QG-015 cryptographic prototype has high-priority findings for replay, claimed sender identity and weak-password handling. [Read the cryptographic audit](./research/QG-015-CRYPTOGRAPHIC-AUDIT.md) and [reproducible adversarial tests](./tests/cryptographic-audit.test.mjs).

## Read and explore

- **[QG-031 Root Roots Propagation](./root-roots.html)** — update evidence at one or several prerequisite root nodes and propagate impact forward to every dependent claim, preserving the original history without automatic truth promotion. [Kernel](./language/root-propagation.mjs) · [Specification](./language/QG-031-ROOT-ROOTS.md) · [Seven tests](./tests/root-propagation.test.mjs).


- **[QG-030 Chasing Roots](./roots.html)** — walk a contextual `WHICH MEANS` claim backward through explicit prerequisite nodes toward historical source roots, uncertain leaves and evidence gaps. [Executable kernel](./language/chasing-roots.mjs) · [Specification](./language/QG-030-CHASING-ROOTS.md) · [Tests](./tests/chasing-roots.test.mjs).


- **[QG-029 Societal Somatics](./society.html)** — the contextual `IS → WAS → WHICH MEANS` transport, with year, IANA timezone, place, group, evidence status and human-assigned social dimensions mapped to three 60-ring phases. [Kernel](./language/societal-somatic.mjs) · [Specification](./language/QG-029-SOCIETAL-SOMATIC.md) · [Tests](./tests/societal-somatic.test.mjs).


- **[QG-028 SEE/DO/LEARN Ring](./triad-ring.html)** — bind all 78 authored semantic role terms to exact QG-026 glyph-phase stations of the QG-025 60-ring, with full DO somatic drawing verbs. [Kernel](./language/semantic-ring.mjs) · [Specification](./language/QG-028-SEMANTIC-RING.md) · [Tests](./tests/semantic-ring.test.mjs).


- **[QG-027 SEE/DO/LEARN Semantic Triads](./language/QG-027-SEMANTIC-TRIADS.md)** — 26 letters with exactly three assigned terms each: observe, act, learn. [Executable lexicon](./language/semantic-triad.mjs) and [tests](./tests/semantic-triad.test.mjs).


- **[QG-026 Alphabet on the 60 Ring](./ring-language.html)** — all 26 uppercase vector glyphs transported as exact ring-addressed vertices and ordered somatic pen verbs across a/b/c/d quarter-turn phases, with complete semantic token and phrase reconstruction.
- [Executable alphabet-ring kernel](./language/alphabet-ring.mjs), [formal specification](./language/QG-026-ALPHABET-RING.md), and [seven regression tests](./tests/alphabet-ring.test.mjs).


- **[QG-025 Sexagesimal 60 Ring](./sixty.html)** — build exactly sixty positions with four 15-station quads, exact 90° phase turns, BigInt base-60 place-value transport, and reversible decimal recovery.
- [Base-60 kernel](./language/sexagesimal-ring.mjs), [historical and technical specification](./language/QG-025-SEXAGESIMAL-60.md), [seven regression tests](./tests/sexagesimal-ring.test.mjs).


- **[QG-024 Convergent Memory Growth](./growth.html)** — a directed ancestry graph of immutable corpus snapshots, with one-parent branch growth and two-parent convergence that can repeat across generations.
- [Graph kernel](./language/memory-growth.mjs), [formal specification](./language/QG-024-MEMORY-GROWTH.md), and [seven regression tests](./tests/memory-growth.test.mjs).


- **[QG-023 Memory Convergence](./convergence.html)** — two independently appended corpus histories from one shared ancestor, explicit three-way paragraph comparison and conflict choices, preserving both immutable branches.
- [Convergence kernel](./language/memory-convergence.mjs), [formal specification](./language/QG-023-MEMORY-CONVERGENCE.md), and [seven regression tests](./tests/memory-convergence.test.mjs).


- **[QG-022 Memory Projection](./projection.html)** — select one revision as a visible Chrome Dot, unfold its exact structured source, walk all immutable parent revisions, and trace a paragraph backward through lineage.
- [Projection kernel](./language/memory-projection.mjs), [formal specification](./language/QG-022-MEMORY-PROJECTION.md), and [seven invariant tests](./tests/memory-projection.test.mjs).


- **[QG-021 Corpus Memory](./memory.html)** — append-only immutable corpus revision snapshots, parent IDs, paragraph provenance links, and exact earlier source recovery.
- [Memory kernel](./language/corpus-memory.mjs), [formal specification](./language/QG-021-CORPUS-MEMORY.md), and [seven regression tests](./tests/corpus-memory.test.mjs).


- **[QG-020 Corpus Box](./corpus.html)** — deterministic `||||` carrier for complete documents, chapters, sections, exact paragraphs, indexed source addresses and explicit reference verbs.
- [Corpus Box executable kernel](./language/corpus-box.mjs), [formal specification](./language/QG-020-CORPUS-BOX.md), and [seven regression tests](./tests/corpus-box.test.mjs).


- **[QG-019 Paragraph Box](./paragraphs.html)** — complete paragraph transport, exact newline and blank-line preservation, relational sentence indices, and 4→3→2→1 visual folds.
- [Paragraph kernel](./language/paragraph-box.mjs), [specification](./language/QG-019-PARAGRAPH-BOX.md), and [seven regression tests](./tests/paragraph-box.test.mjs).

- **[QG-018 Sentence Box](./sentences.html)** — sentence-level transport preserving case, punctuation, spaces, word relations, continuous a/b/c/d phase, and exact recovery.
- [Sentence kernel](./language/sentence-box.mjs), [formal specification](./language/QG-018-SENTENCE-BOX.md), and [six regression tests](./tests/sentence-box.test.mjs).

- **[QG-017 Word Box Composer](./words.html)** — phase-semantic-somatic composition for A–Z words and phrases, keeping word order, spaces, 90° phase schedule, 4→3→2→1 views and source reconstruction.
- [Word transport kernel](./language/word-box.mjs), [specification](./language/QG-017-WORD-BOX.md) and [tests](./tests/word-box.test.mjs).

- **[QG-016 Alphabet Box](./alphabet.html)** — the complete A–Z geometric language, `||||` carrier, `||Q||`-style tokens, four 90° quads `a/b/c/d`, each with `4 → 3 → 2 → 1` presentation depth and ordered somatic pen verbs.
- [Alphabet Box specification](./language/QG-016-ALPHABET-BOX.md), [executable module](./language/alphabet-box.mjs), and [alphabet tests](./tests/alphabet-box.test.mjs).

- **[QG-015 Authenticated Chrome Dot Transport](./authenticated.html)** — send one visible bit plus its 127-bit witness through QG-013, verify authentication, and recover the original 128 bits.
- [QG-015 specification](./language/QG-015-AUTHENTICATED-CHROME.md), [module](./language/authenticated-chrome.mjs) and [tests](./tests/authenticated-chrome.test.mjs).

- **[QG-014 Recoverable Chrome Dot](./fold.html)** — live 128 → 64 → 32 → 16 | 8 → 4 → 2 → 1 | 1 fold with a portable 127-bit witness and exact recovery.
- [QG-014 source module](./language/recoverable-fold.mjs), [specification](./language/QG-014-RECOVERABLE-FOLD.md), and [test suite](./tests/recoverable-fold.test.mjs).

- **[QG-013 Downward Spiral Transport](./spiral.html)** — 3D–11D eight-source globule routing, reversible byte permutation, and local AES-256-GCM encryption/decryption console.
- [QG-013 protocol specification](./language/QG-013-DOWNWARD-SPIRAL.md) — preserves the raw `12|8/64/3|2/16/8|/4/2/1/1` signature, now explicitly decoded as **128/64/32/16 · 8/4/2/1 · 1** (four-number chunks plus stable one), and separates transport from cryptography.
- [QG-013 executable module](./language/downward-spiral.mjs) and [tests](./tests/downward-spiral.test.mjs).

- **[Explore QG-011 / QG-012: the 11D Globule and Quantum Chrome Dot](./11d.html)** — interactive 1D–11D hypercube with exact combinatorial invariants and rotatable 2D projection.
- [QG-012 Quantum Chrome Dot](./language/QG-012-CHROME-DOT.md) — provenance-preserving fold 8 → 4 → 2 → 1 → 1, ending at a stable one.
- [QG-011 formal specification](./language/QG-011-11D-GLOBULE.md) — separate ordinal dot-bar signature from the n-cube graph and physical speculation.

- **[Read the complete book with geometric cover](./book.html)** — full 32.5-chapter GitHub Pages edition, loading all original chapter manuscripts, puzzles, and notes.
- [Geometric book cover (SVG)](./assets/quanta-geometric-cover.svg) — crisp scalable cover for the reader.
- [Complete Word manuscript (DOCX)](./book/QUANTA_The_Wordle_of_Space_Complete_32_5.docx).

- [Reader companion (index.html)](./index.html) — single-file GitHub Pages experience with all 32 chapters and the 32.5 coda, symbols, and interactive puzzles.
- [Chapter 1: Zero](./book/chapters/01-zero.md) — manuscript with technical ledger.
- [Chapter 2: The Dot](./book/chapters/02-the-dot.md) — distinction, relationships, identity, Puzzle 002, and Q1.
- [Chapter 3: The Gap](./book/chapters/03-the-gap.md) — the between, the engine analogy, [()], Puzzle 003, and Q2.
- [Chapter 4: The Boundary](./book/chapters/04-the-boundary.md) — inside and outside, selective passage, Puzzle 004, and Q3.
- [Chapter 5: The Box](./book/chapters/05-the-box.md) — containment, nesting, Puzzle 005, and Q4.
- [Chapter 6: The Loop](./book/chapters/06-the-loop.md) — return, movement versus shape, Puzzle 006, and Q5.
- [Chapter 7: The Vessel](./book/chapters/07-the-vessel.md) — receive, retain, transform, release; Puzzle 007 and Q6; introduces transport motif `.|.|.|.|.`.
- [Chapter 8: The Path](./book/chapters/08-the-path.md) — five stations, observed transport versus intended route, Puzzle 008, and Q7.
- [Chapter 9: The Signal](./book/chapters/09-the-signal.md) — shared reading rules, Puzzle 009, and Q8.
- [Chapter 10: The Code](./book/chapters/10-the-code.md) — first syntax rules, an interactive nesting checker, Puzzle 010, and Q9.
- [Chapter 11: The Grammar](./book/chapters/11-the-grammar.md) — nesting, sequence, identity, Puzzle 011, and Q10.
- [Chapter 12: The Transformation](./book/chapters/12-the-transformation.md) — one box, changing wall-trace, Q11, and Puzzle 012.
- [Chapter 13: The Witness](./book/chapters/13-the-witness.md) — observer references, honest records, Q12, and Puzzle 013.
- [Chapter 14: The Record](./book/chapters/14-the-record.md) — append-only observations, corrections, Puzzle 014, and Q13.
- [Chapter 15: The Comparison](./book/chapters/15-the-comparison.md) — comparison criteria, structural versus physical identity, Puzzle 015, and Q14.
- [Chapter 16: The Difference](./book/chapters/16-the-difference.md) — directed differences, representational change, Puzzle 016, and Q15.
- [Chapter 17: The Choice](./book/chapters/17-the-choice.md) — alternatives, intention versus action, Puzzle 017, and Q16.
- [Chapter 18: The Action](./book/chapters/18-the-action.md) — intention, attempt, result verification, Puzzle 018, and Q17.
- [Chapter 19: The Feedback](./book/chapters/19-the-feedback.md) — expectation versus outcome, feedback, Puzzle 019, and Q18.
- [32.5-chapter book roadmap](./book/ROADMAP-32-5.md) — full book arc and intentional half-chapter finale.
- [Chapter 20: The Lesson](./book/chapters/20-the-lesson.md) — evidence-based revised rules, Puzzle 020, and Q19.
- [Chapter 21: The Question](./book/chapters/21-the-question.md) — testable questions, Puzzle 021, and Q20.
- [Chapter 22: The Experiment](./book/chapters/22-the-experiment.md) — controlled shadow experiment, Puzzle 022, and Q21.
- [Chapter 23: The Failure](./book/chapters/23-the-failure.md) — counterexample preservation and reduction, Puzzle 023, and Q22.
- [Chapter 24: The Invariant](./book/chapters/24-the-invariant.md) — declared transformations, preservation proof, Puzzle 024, and Q23.
- [Chapter 25: The Boundary Again](./book/chapters/25-the-boundary-again.md) — domain boundaries, necessary versus sufficient conditions, Puzzle 025, and Q24.
- [Chapter 26: The Repetition](./book/chapters/26-the-repetition.md) — repeatability, tolerances, trial preservation, Puzzle 026, and Q25.
- [Chapter 27: The Neighbor](./book/chapters/27-the-neighbor.md) — separate witnesses, attributed copies, Puzzle 027 and Q26.
- [Chapter 28: The Exchange](./book/chapters/28-the-exchange.md) — packets, acknowledgments, codebooks, Puzzle 028, and Q27.
- [Chapter 29: The Weave](./book/chapters/29-the-weave.md) — network provenance, copied versus original observations, Puzzle 029, and Q28.
- [Chapter 30: The Homecoming](./book/chapters/30-the-homecoming.md) — local indexing without ownership collapse, Puzzle 030, and Q29.
- [Chapter 31: The Shadow Revisited](./book/chapters/31-the-shadow-revisited.md) — layered observation, competing interpretations, Puzzle 031, and Q30.
- [Chapter 32: The One Box](./book/chapters/32-the-one-box.md) — the full-circle ending, Puzzle 032, and Q31.
- [Chapter 32.5: The Half-Step](./book/chapters/32-5-the-half-step.md) — final open-door coda, Puzzle 032.5, and Q32.
- [Visual lexicon](./language/LEXICON.md) — symbols, visual readings, and reserved definitions.
- [Claims ledger](./research/CLAIMS.md) — established math versus proposed language versus untested physics.
- [Writing guide](./book/STYLE.md) — reader-first editorial principles.
- [Changelog](./CHANGELOG.md) — dated, additive publication notes.

## GitHub Pages

The website lives in `index.html` at the repository root. To publish, enable **Settings → Pages → Deploy from a branch → main → /(root)**. Its prospective address is `https://davidwise01.github.io/quanta/` (verify in Pages settings before sharing it as live).

## Book principle

**Show the relationship before explaining the equation.**

Readable marks like `0`, `.`, `[ ]`, `( )`, and `{{i}}` carry the narrative. Mathematical proof belongs in optional notes and test files, not the middle of the story. Do not present symbolic inventions as measured physics.

This is a work in progress, not a finished Amazon edition.
