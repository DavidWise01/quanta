# QUANTA · Changelog

## 2026-11-08 — QG-020 · Corpus Box
- Created `language/corpus-box.mjs` with `||||` structured documents, chapters, sections, paragraph witnesses, deterministic source addresses, typed references and inverse validation.
- Published `corpus.html`, an interactive address tree and 4→3→2→1 view, plus QG-020 spec and seven GitHub Actions regression tests.
- The corpus packet preserves canonical text and references; the Chrome Dot is a projection rather than independent lossless compression.

## 2026-11-08 — QG-019 · Paragraph Box
- Added `language/paragraph-box.mjs`, an ordered paragraph container with exact LF line-break witnesses, sentence fragment links, offsets and context.
- Built `paragraphs.html` to explore four visual folds and recover complete paragraph source through canonical QG-018 sentence and QG-017 word references.
- Added a formal spec and seven CI tests; the initial test run exposed the 128-character nested word limit, which was addressed by 128-character fragment cap.

## 2026-11-08 — QG-018 · Sentence Box
- Instantiated `language/sentence-box.mjs`, preserving exact capitalization, spaces, punctuation, word offsets and word-to-word relationship indices.
- The a/b/c/d phase register continues across words, resets on `.`, `?`, `!`, and rotates somatic drawing verbs at sentence level.
- Added `sentences.html`, an interactive four-level fold/unfold lab, plus specification and six regression tests. The initial GitHub Actions suite passed.

## 2026-11-07 — QG-017 · Word Box composition
- Introduced `language/word-box.mjs` with a single `||||` carrier for ordered words, spaces, per-letter quarter-turn phases, contextual semantic witness, and translated somatic drawing actions.
- Added `words.html` to fold a whole phrase through levels 4→3→2→1 and reconstruct the exact text; the canonical source dictionary remains available at all levels.
- Added `language/QG-017-WORD-BOX.md`, automated tests and an Actions workflow.

## 2026-11-07 — QG-016 · Alphabet Box phase–semantic–somatic transport
- Implemented `language/alphabet-box.mjs`: complete A–Z vector stroke corpus, `||||` carrier, `||LETTER||` tokens, preserved semantic glyph identity, and ordered somatic drawing verbs.
- Added quads `a/b/c/d` at 0°/90°/180°/270°, each displaying `4 → 3 → 2 → 1` while preserving full canonical source strokes.
- Created `alphabet.html`, QG-016 specification, and six automated invariant tests; the initial GitHub Actions suite passed.
- The alphabet engine is geometric transport rather than encryption, and optional meanings are provided by context rather than inferred from isolated letters.

## 2026-11-07 — QG-015 source cryptographic audit
- Published `research/QG-015-CRYPTOGRAPHIC-AUDIT.md` and `tests/cryptographic-audit.test.mjs`; 8 adversarial regression cases completed successfully.
- Audit documents known issues: replay, sender-label impersonation, weak-passphrase/offline guessing risk, inadequate inbound size bounds, and lack of independent witness authentication.
- Marked the public sender/receiver console as an **educational-only prototype, NOT approved for sensitive use**. No cryptographic algorithms or existing envelope format changed during the audit.

## 2026-11-07 — QG-015 · Authenticated Chrome Dot Transport
- Instantiated `language/authenticated-chrome.mjs` joining the 128→1+127 recoverable fold, downward-spiral address transport, and authenticated AES-GCM envelope.
- Added the browser sender/receiver console `authenticated.html`, QG-015 specification, automated tests and GitHub Actions workflow.
- Confirmed round-trip and tamper rejection in GitHub Actions across all supported dimension levels; preserved warnings that this is not an independently security-audited system.

## 2026-11-07 — QG-014 · Recoverable Chrome Dot
- Instantiated `language/recoverable-fold.mjs`, an immutable exact reversible 128-bit folding primitive with XOR-right witnesses.
- Two four-width chunks are preserved, and the final 1→1 fold is a fixed point; portable frames carry one terminal bit plus 127 witness bits.
- Added `fold.html` for witness export/import and complete source recovery, plus deterministic regression tests and GitHub Actions.
- Clarified that one visible dot without its witness is information-losing and that the witness must be authenticated externally for security.

## 2026-11-07 — QG-013 width-ladder clarification
- Author clarified the legacy signature as the nine-stage descending **bit-width** ladder `128/64/32/16 · 8/4/2/1 · 1` in four-number chunks, with the final 1→1 a stable fixed point.
- Kept raw serialization unchanged; added explicit normalized constants, a validator, tests, the on-page width display, and revised research-language definitions.
- Distinguished this bit-width ladder from eight-source globules and from AES-256-GCM encryption.

## 2026-11-07 — QG-013 · Downward Spiral Transport
- Preserved the proposed literal signature `12|8/64/3|2/16/8|/4/2/1/1` as an unassigned versioned field label, without inventing semantics for its numeric segments.
- Created `language/downward-spiral.mjs`: Gray-address ordered eight-source globules across dimensions 3–11, clockwise outer-to-inner grid traversal, and reversible payload-byte transport.
- Applied local standard AES-256-GCM authenticated encryption with fresh nonce/salt, PBKDF2-HMAC-SHA-256 and authenticated header fields; the spiral is not itself encryption.
- Published `spiral.html`, a browser-local send/decrypt console and 16×16 spiral visualization at 11D; added tests and an Actions workflow.
- Linked the new console from the homepage and 11D lab and extended the lexicon and claims ledger.

## 2026-11-07 — QG-012 · Quantum Chrome Dot
- Defined `\\.|./` as a proposed fold primitive: 8 → 4 → 2 → 1 → 1, with unchanged terminal-node identity at the fifth state.
- Added a provenance-preserving fold control to the 11D experiment without altering the underlying hypercube adjacency or vertex counts.
- Added the QG-012 specification, lexicon notation, arithmetic invariant, and appropriate physical-claim caveat.

## 2026-11-07 — QG-011 · Eleven-dimensional globule
- Added `language/QG-011-11D-GLOBULE.md` with exact graph substrate definitions and an explicit distinction between the eleven-dot level signature and the 11D hypercube.
- Added `11d.html`, an interactive n=1–11 canvas projection, exact vertex/edge/face counts, graph validation, and projection rotation.
- Updated the home-page navigation, reader links, visual lexicon, and research claims ledger.
- The term globule is a proposed QUANTA container metaphor and is not an experimentally validated M-theory object.

## 2026-11-07 — Complete GitHub Pages book and cover
- Published `book.html` as a full manuscript reader, sourcing every original chapter (1–32.5) from the canonical repository Markdown files.
- Added the geometric QUANTA cover as `assets/quanta-geometric-cover.svg` and featured the book and cover on the existing home page.
- Included all puzzles and technical notes, a 33-item table of contents, responsive navigation, search, reading progress and the complete Word manuscript link.

## 2026-11-07 — Chapter 32.5 · The Half-Step · Manuscript complete
- Added the final half-chapter: The Half-Step, Q32 The Open Gap Remains Legible, and Puzzle 032.5.
- Added an interactive half-open-door journal with an unassigned dot and an explicitly open question.
- Completed the planned 32 full chapters plus an intentionally shorter 32.5 coda, with the site, lexicon, claims ledger, and roadmap updated.
- The final dot is a literary symbol, not evidence for an extra physical dimension.

## 2026-11-07 — Chapter 32 · The One Box
- Added Chapter 32: The One Box, Q31 One Box, Distinctions Intact, and Puzzle 032.
- Added a session-only one-box composition lab preserving separate types and origins of marks, evidence, copies, analogies, and unknowns.
- Completed the 32 full chapters; the intentionally shorter Chapter 32.5 coda remains.
- Extended lexicon and research ledger without promoting metaphors to physical evidence.

## 2026-11-07 — Chapter 31 · The Shadow Revisited
- Added Chapter 31: The Shadow Revisited, Q30 A Revisited Observation Keeps Its Layers, and Puzzle 031.
- Added a codebook-selection experiment preserving the original five-dot trace while appending interpretations in a temporary journal.
- Entered the final 31–32.5 arc of the book, with the original wall-shadow revisited through layered evidence.
- Extended the lexicon and claims ledger to distinguish syntax, semantics, mathematical proofs, empirical findings, and metaphors.

## 2026-11-07 — Chapter 30 · The Homecoming
- Added Chapter 30: The Homecoming, Q29 Home Preserves the Outside, and Puzzle 030.
- Added an interactive local home-index lab preserving separate origin and ownership for observations and received copies.
- Completed the neighbor/exchange/weave/homecoming act and prepared the final 31–32.5 arc.
- Updated lexicon and claims ledger.

## 2026-11-07 — Chapter 29 · The Weave
- Added Chapter 29: The Weave, Q28 A Weave Must Preserve Its Sources, and Puzzle 029.
- Added an interactive provenance tracer distinguishing two originating observations from three copied reports.
- Updated lexicon and claims ledger on source lineages, typed relationships, and feedback loops.

## 2026-11-07 — Chapter 28 · The Exchange
- Added Chapter 28: The Exchange, Q27 Exchange Preserves Meaning and Provenance Boundaries, and Puzzle 028.
- Added a simulated four-step exchange lab differentiating sending, receipt, interpretation, and agreement, with an in-session journal.
- Extended lexicon and claims ledger on codebooks, integrity, attribution, and authority boundaries.

## 2026-11-07 — Chapter 27 · The Neighbor
- Added Chapter 27: The Neighbor, Q26 Neighboring Records Preserve Identity, and Puzzle 027.
- Added a two-notebook provenance lab showing attributed copies without independent verification or source edits.
- Began the connections arc, preserving identifiers and authority boundaries between neighbors.
- Updated visual lexicon and research claims ledger.

## 2026-11-07 — Chapter 26 · The Repetition
- Added Chapter 26: The Repetition, Q25 Repetition Preserves Every Trial, and Puzzle 026.
- Added an interactive, explicitly fictional repeat-measurement lab with per-trial fixed tolerance and append-only in-session records.
- Concluded the planned experiment-and-invariant arc; Chapter 27 begins the connection arc.
- Updated lexicon and claims ledger on method, variation, and repeatability scope.

## 2026-11-07 — Chapter 25 · The Boundary Again
- Added Chapter 25: The Boundary Again, Q24 A Claim Must Carry Its Boundary, and Puzzle 025.
- Added a browser-based boundary tester for valid versus invalid domains and allowed versus excluded transformations.
- Updated lexicon and claims ledger on scoped implications and necessary versus sufficient conditions.

## 2026-11-07 — Chapter 24 · The Invariant
- Added Chapter 24: The Invariant, Q23 Invariance Requires a Declared Transformation, and Puzzle 024.
- Added an interactive alternating-sequence invariant test with a contrasting out-of-domain edit and an in-session event trace.
- Updated visual lexicon and claims ledger to distinguish formal-language preservation from physical claims.

## 2026-11-07 — Chapter 23 · The Failure
- Added Chapter 23: The Failure, Q22 Preserve the Smallest Honest Failure, and Puzzle 023.
- Added a bounded counterexample minimizer for the introductory alternating-sequence grammar, retaining the original failing example and reduction trace.
- Updated lexicon and claims ledger to distinguish a mathematical counterexample from a diagnosed physical cause.

## 2026-11-07 — Chapter 22 · The Experiment
- Added Chapter 22: The Experiment, Q21 Experiment With Declared Controls, and Puzzle 022.
- Added an idealized card-shadow projection simulation with a session-only trial/deviation log, explicitly labeled model rather than physical measurement.
- Updated the lexicon and claims ledger, distinguishing a card shadow from an actual tesseract projection model.

## 2026-11-07 — Chapter 21 · The Question
- Added Chapter 21: The Question, Q20 A Question Must Expose Its Test, and Puzzle 021.
- Added a question-building lab recording variables, observations and comparison baselines without claiming a test was performed.
- Started the planned experiment-and-invariant act of the 32.5-chapter book.
- Updated visual lexicon and research claims ledger.

## 2026-11-07 — Chapter 20 · The Lesson
- Added Chapter 20: The Lesson, Q19 Learning Requires a Tested Revision, and Puzzle 020.
- Added a teaching experiment contrasting sunlight-only selection with inspection; recorded outcomes remain limited to observations.
- Reached the 20-of-32.5 milestone; Chapter 21 begins the test-and-invariant act.
- Updated lexicon and claims ledger, distinguishing proposed policies from verified learning.

## 2026-11-07 — Chapter 19 · The Feedback and 32.5-Chapter Plan
- Added Chapter 19: The Feedback, Q18 Feedback Must Reference Reality and Puzzle 019.
- Established the 32.5-chapter roadmap, including the final half-chapter and a return to one box.
- Added a simulated prediction-versus-outcome comparison with a temporary append-only feedback journal.
- Extended lexicon and claims ledger without claiming feedback automatically yields improvement.

## 2026-11-07 — Chapter 18 · The Action
- Added Chapter 18: The Action, Q17 Action Requires an Outcome Trace and Puzzle 018.
- Added a simulated action-trace journal that separates selection, attempt, and hypothetical outcome.
- Updated the lexicon and claims ledger to distinguish command receipt from verified action result.

## 2026-11-07 — Chapter 17 · The Choice
- Added Chapter 17: The Choice, Q16 Choice Without Retroactive Certainty and Puzzle 017.
- Added a temporary choice journal distinguishing selection, attempted action, and reported outcome.
- Extended lexicon and claims ledger with provisional alternative-brace notation and decision provenance.

## 2026-11-07 — Chapter 16 · The Difference
- Added Chapter 16: The Difference, with Q15 Difference With Scope and Puzzle 016.
- Added a reversible dot-count difference experiment with a temporary append-only report ledger.
- Updated the lexicon and claims ledger to keep representational change distinct from cause.

## 2026-11-07 — Chapter 15 · The Comparison
- Added Chapter 15: The Comparison, with Q14 Compare Without Conflation and Puzzle 015.
- Added a side-by-side representation comparison and in-session append-only comparison journal.
- Updated lexicon and claims ledger to distinguish representational similarity from identity, state, or cause.

## 2026-11-06 — Chapter 14 · The Record
- Added Chapter 14: The Record, with Q13 Memory Without Revision of History and Puzzle 014.
- Added a temporary append-only witness log with referenced corrections in the reader companion.
- Updated lexicon and claims ledger; distinguished durable memory policy from demo-only UI state.

## 2026-11-06 — Chapters 12–13 · Transformation and Witness
- Committed Chapter 12, previously drafted but absent from GitHub, preserving its core wall-shadow account and Q11.
- Committed Chapter 13, including Q12 Witness Without Possession and Puzzle 013.
- Added both visual reading sections, an append-only-in-session witness journal, and their interactive quizzes.
- Updated the lexicon and research ledger. Browser journal entries are temporary and not server-stored.

## 2026-11-06 — Chapter 11 · The Grammar
- Added Chapter 11: The Grammar, with Q10 Preserve the Relationship Type and Puzzle 011.
- Added a three-family teaching grammar recognizer to the GitHub Pages reader.
- Kept nested forms, sequential forms, and the reserved identity token distinct; full mixed grammar remains future work.

## 2026-11-06 — Chapter 10 · The Code
- Added full Chapter 10, introducing Q9 Form Before Interpretation and Puzzle 010.
- Added the first simple QUANTA nesting syntax checker in the GitHub Pages reader.
- Separated basic bracket syntax from reserved transport and identity forms.

## 2026-11-06 — Chapter 9 · The Signal
- Added the complete Chapter 9 manuscript, Puzzle 009, and Q8 Meaning Requires a Reading Rule.
- Added a two-codebook signal demonstration to the reader website.
- Updated lexicon and claims ledger to distinguish signal, message, and interpretation.

## 2026-11-06 — Chapter 8 · The Path
- Added Chapter 8: The Path, with relay-station imagery, Puzzle 008, and Q7 Trace Before Arrival.
- Added an accessible stepwise five-station relay with observable event history to the GitHub Pages reader.
- Extended the lexicon and ledger while leaving full physical or computational transport semantics open for specification.

## 2026-11-06 — Chapter 7 · The Vessel
- Added Chapter 7 as a standalone manuscript, including Q6 Passage With Provenance and Puzzle 007.
- Introduced the `.|.|.|.|.` transport motif as a five-mark, four-boundary string; formal semantics reserved for a later chapter.
- Added a four-stage visual vessel activity and quiz to the website, preserving the manuscript/reference split.

## 2026-11-06 — Chapter 6 · The Loop
- Added the complete Chapter 6 manuscript and Puzzle 006, introducing Q5 Return Without Erasure.
- Added the sixth visual reader chapter and a manually advanced loop demonstrating the preserved lap count.
- Updated lexicon and claims ledger, maintaining the distinction between a loop drawing and a moving system.

## 2026-11-06 — Chapter 5 · The Box
- Added the complete Chapter 5 manuscript and Puzzle 005, introducing Q4 Containment Preserves Distinction.
- Added Chapter 5 to the interactive reader and maintained the book, lexicon and claims ledger.

## 2026-11-06 — Chapters 3 and 4
- Saved Chapter 3: The Gap, including the central [()] analogy and Q2.
- Wrote Chapter 4: The Boundary, including Q3 and Puzzle 004.
- Extended the reader-facing site with both chapters and interactive puzzles.
- Updated the lexicon, claim ledger, and reading links.

## 2026-11-06 — Chapter 2 · The Dot
- Added the second reader-first manuscript with Q1 Identity Before Comparison and Puzzle 002.
- Extended the interactive reading website with Chapter 2 and its puzzle.
- Extended the visual language notes to distinguish identification from mere resemblance.

## 2026-11-06 — Reader companion foundation
- Established root-level GitHub Pages website.
- Introduced visual symbol tiles, a step-by-step symbolic playground, and Puzzle 001.
- Created lexicon, claims ledger, and reader-first editorial charter.
- Kept Chapter 1's technical source accessible while bringing a simpler reading edition to the website.
- Declared future publication pipeline: source manuscript → reviewed ebook and print formats.

## 2026-11-06 — Chapter 1 draft 0.1
- Added `book/chapters/01-zero.md`: origin, point, gap, first boundary, and Q0.
