# QUANTA · Changelog

## 2026-11-12 — QG-069 · Rejoining the Hive
- Introduced a replayable offline-to-online rejoin state machine that retains local observations by value and denies authority until a current QG-068 checkpoint matches an independently supplied SHA-256 digest and revocation floor.
- Added a separate explicit authorization step after the verified checkpoint, 28 regression tests for stale, tampered, offline and wrong-pin paths, an ASCII browser lab and formal spec. No deployed synchronization or remote attestation is claimed.


## 2026-11-12 — QG-068 · Revocation Across the Hive
- Added a synthetic multi-agent revocation gate requiring an independent minimum revocation sequence, verified QG-066 recovery and QG-067 successor-signed revocation for all new operations.
- Classified fresh, stale, offline and tampered local agent trust snapshots with append-by-value digest receipts; denied local authority when the cached snapshot cannot meet the external revocation floor. Added 26 tests, ASCII lab and specification. No real distributed synchronization or durable floor is claimed.


## 2026-11-12 — QG-067 · Revocation Outlives Recovery
- Added a successor-signed revocation certificate after QG-066 recovery, binding the retired key fingerprint, recovered successor key, historical QG-065 chain and original recovery digest.
- Preserved verification of historical manifests while requiring successor-key signatures for all new operations. A separately pinned revocation sequence floor detects replay without the revocation. Added 24 tests and an interactive ASCII lab, all synthetic and not deployed credential revocation.


## 2026-11-12 — QG-066 · Recovery Without the Old Key
- Added an explicit emergency recovery branch independent of normal QG-065 dual-signature rotation. A separately pinned recovery policy requires three valid Ed25519 guardian votes from three distinct declared source ancestries and successor proof of key possession.
- Preserved the full QG-065 historical source chain, bound recovery to its SHA-256 digest, and verified new manifests under the recovered key without erasing old signatures. Added 27 tests and interactive browser ASCII lab. Synthetic guardians only; externally pinned quorum independence and durability remain assumptions.


## 2026-11-12 — QG-065 · Trust Anchor Rotation
- Added dual-signed Ed25519 transitions requiring a current-key authorization and new-key proof of possession over a canonical linked transition payload.
- Retained old historical signed manifests by key epoch, enforced monotonic manifest revisions and independent minimum sequence floors for rollback detection. Added 24 regression tests and browser ASCII lab. Synthetic signers only; no live identities or keys rotated.


## 2026-11-12 — QG-064 · The Trust Anchor
- Added Ed25519 signed source-manifest verification using an independently pinned public JWK and minimum revision. Payload canonicalization and SHA-256 digest bind registry contents; mismatched keys, tampering and rollback are rejected before QG-063 admission.
- Integrated with QG-063 source SHA-256 checks and QG-062 shared-ancestry counting without granting automatic authority. Added 24 negative/positive regression tests and interactive ASCII lab. Keys and manifests are synthetic, not verified real-site publisher credentials.


## 2026-11-11 — QG-063 · Pinned Source Admission
- Introduced a pinned local manifest admission gate before QG-062 ancestry counting. The browser/Node engine computes SHA-256 content digests, checks pinned source/surface identity and predeclared public robots status, and quarantines unknown, modified and disallowed packets.
- Accepted source ancestry comes from the pinned manifest rather than packet assertions, while mirrors and syndication still merge under QG-062. Added 28 regression tests and interactive ASCII lab; this does not authenticate real website authorship or fetch live site access rules.


## 2026-11-11 — QG-062 · Three Surfaces, Independent Roots
- Modeled the three discovery surfaces: gated GitHub and 0root.ai as one owned source ancestry, and policy-aware public internet evidence from potentially many sites. Shared upstream identifiers create transitive ancestry components, preventing duplicate votes from syndicated sources.
- Added explicit synthetic robots/llms policy annotations (robots disallow blocks; unknown quarantines; llms is discovery, not permission), conflicting-lineage review, and separate provisional authorization. 32 regression tests, ASCII lab, specification, and provenance boundaries. No actual sites or policies are fetched.


## 2026-11-11 — QG-061 · Relearning Without Amnesia
- Added an explicit post-withdrawal relearning lifecycle, retaining QG-058, QG-059, QG-060 history while proposing a new candidate from fresh validation.
- Added witness-ancestry accounting with GitHub and 0root.ai mirrors sharing one synthetic root, three distinct matching root claims required for provisional-authorization eligibility, contradictory-root quarantine, and a separate authorization action. Added 27 regression tests and an interactive ASCII Pages lab. Source independence remains an unverified input claim.


## 2026-11-11 — QG-060 · The Right to Be Wrong
- Introduced a post-promotion validation boundary: one separate 20-outcome fixed-window test can withdraw the *current* symbolic authority of a promoted provisional candidate, without erasing or modifying the historical QG-058 alert and QG-059 promotion decision.
- Added a replay-checked withdrawal certificate, 24 regression tests, a visual ASCII Pages laboratory, and documented that the value ledger is not cryptographically sealed or proof of real-world drift.


## 2026-11-11 — QG-059 · Sealed Model Handoff
- Added explicit preservation of an old baseline and source QG-058 alert while independently testing a provisional candidate model against 20 fresh binary observations.
- Candidate is not promoted before a complete confirmation batch, and a rejected candidate remains on record. Added 22 new regression tests, source/decision replay checks, interactive ASCII Pages lab and formal limits on the meaning of promotion.


## 2026-11-10 — QG-058 · Change Versus Noise
- Added baseline-versus-batch difference screening under an explicitly stationary independent Bernoulli null model, using Hoeffding bounds and alpha spending over repeated fixed checkpoints.
- Preserved each input, comparison, and original baseline in a replay-verifiable value ledger; flagged possible changes for review without asserting causal explanation or proof of stationarity. Added 26 tests and interactive ASCII laboratory.


## 2026-11-10 — QG-057 · Forecast Reliability
- Separated prior probability forecasts from later realized binary price outcomes; added issuance-before-observation event semantics with deterministic replay.
- Implemented Beta(3,2) illustrative posterior predictive updates, Brier scoring, empirical rate, calibration bins and explicit small-sample warnings. Added 26 regression tests, browser ASCII laboratory and formal model limitations.


## 2026-11-10 — QG-056 · The Uncertainty of Waiting
- Replaced guaranteed future costs with a finite hypothetical probability distribution; added contingent policy to buy now, wait, or stop, and only conditionally buy when a future price is actually revealed.
- Kept the forecast separate from the realized observation; logged and replay-verified both favorable and unfavorable branches. Added 29 adversarial tests, ASCII interactive lab and documentation; probabilities remain assumptions rather than calibrated predictions.


## 2026-11-10 — QG-055 · The Value of Waiting
- Added finite-horizon waiting decisions for synthetic sensor prices, a waiting fee, discounted information value, and a hard budget. The observer can wait without moving along Fibonacci coordinates.
- Logs wait/observe/stop events and verifies deterministic replay; added 26 adversarial tests, interactive ASCII GitHub Pages lab, and exact model scope. This does not schedule real background work.


## 2026-11-10 — QG-054 · The Cost of Knowing
- Added one-step expected value-of-information policy: benefit (uniform candidate information bits × declared value per bit) minus observation cost, subject to a hard budget.
- A zero-net or unaffordable observation is rejected while the original ambiguous evidence is preserved; added 21 regression tests, interactive ASCII Page, and formal model limits. Credits are not physical electrical capacitance.


## 2026-11-10 — QG-053 · No-Wasted-Movement Bound
- Implemented bounded action selection at the current permitted Fibonacci vertex based on expected candidate-count information gain, with an optional movement penalty.
- Preserved distinct observation opportunities at the repeated first 1, avoided duplicate measurements, and stopped when no positive-gain action existed. Added 17 tests, ASCII lab and specification; synthetic information, not physical movement or actual identification.


## 2026-11-10 — QG-052 · Independent Information
- Measured conditional information gain at the repeated Fibonacci 1 without moving: duplicate amplitude adds zero bits; phase resolves a two-root ambiguity and adds one bit under a uniform candidate prior.
- Added candidate-partition forecasts, deterministic two-event replay, 18 regression tests, ASCII interactive Pages lab, and a model-dependence note. This is not a proof of physically independent sensors.


## 2026-11-10 — QG-051 · Observation Sufficiency
- Preserved the Fibonacci path 1/1/2/3/5/8/13 with its repeated first position as a second measurement rather than duplicate distance traveled.
- Demonstrated that amplitude-only samples on the thirteen-position ring cannot separate aliased roots 5/8 and 6/7; a phase measurement at the same permitted vertex distinguishes all eight enumerated roots.
- Added 18 regression tests, a deterministic blind measurement ledger, an interactive ASCII Pages viewer and documented the finite candidate-class limits.


## 2026-11-10 — QG-050 · Ambiguous Roots
- Added an observer-first synthetic model of observationally indistinguishable roots: 8-point samples cannot distinguish cosine frequencies 1 and 7.
- Added bounded off-grid experimental probes that separate candidates when their predicted observations diverge; preserved all compatible roots until new evidence arrives.
- Added 16 tests, deterministic append-by-value observation ledger, interactive ASCII viewer, and documented the limited candidate class. No claims about actual Mandelbrot or physical systems.


## 2026-11-10 — QG-049 · Minimum Fold Memory
- Replaced QG-048's duplicate full preimage with a smaller recipe-relative witness: successor, fixed generator recipe, and lobes parameter; n inferred from successor size.
- Regenerates source and contraction deterministically; rejects stale, inconsistent, unknown, or missing witnesses. Includes 14 regression tests and a canvas viewer.
- JSON character-count comparison is not a universal minimal-bit proof or a guarantee of unique source reconstruction from an arbitrary collapsed graph.


## 2026-11-09 — QG-048 · Reversible Pinch
- Added exact reverse of QG-047's explicit center/rim contraction using retained original graph, vertex identities, and full edge lineage.
- Proved and regression-tested five outer ring sizes; a contracted successor without preimage evidence is intentionally insufficient for unique reversal.
- Added 15 regression tests, in-browser canvas, interactive Pages lab, formal specification and replay checks. No external authentication or physical topology claim.


## 2026-11-09 — QG-047 · Post-Contact Reconstruction
- Extended QG-046 first-contact evidence with an explicit graph contraction that merges the center and touching rim vertex, removes a self-loop, and deduplicates two parallel edges.
- Preserved an exact mapping from original vertices and every original edge to its successor or removal reason; proved successor counts V=n, E=2n-3, F=n-1, Euler=2 for the defined planar family.
- Added 14 adversarial regression tests, replay verification, a chrome/orange interactive Pages viewer, and a formal specification. A new graph is not a physical phase transition.


## 2026-11-09 — QG-046 · First Contact
- Analytically derived the first rim-to-center collision at radial strength 1 for the declared pinching family; all fan triangle areas remain positive before contact.
- Implemented seven Fibonacci-strength observations, an append-only-value replay ledger, 14 regression cases, interactive Pages lab, proof notes and claims ledger. A collapsed embedding is not a constructed new topology.


## 2026-11-09 — QG-045 · Center-Pinch Conservation
- Instantiated a planar wheel-graph geometry with 3, 4, 5, 8, or 13 outer vertices plus one independent center point.
- Added bounded radial pinches, face-orientation and nonincident-edge intersection guards, Euler V-E+F=2 validation, and 20-step geometric sampling of each motion (not a continuous proof).
- Added seven Fibonacci observation events, append-only-value replay ledger, thirteen adversarial tests, and interactive GitHub Pages lab. Excludes torus/physical phase-change claims.


## 2026-11-09 — QG-044 · Closure-Order Invariant
- Added symbolic grammar distinguishing interleaved `.[(.])` from nested `.[(.)]` through interval crossing and closure order.
- Implemented lossless fold/unfold packets preserving source, token offsets, paired intervals, and crossing evidence, with deterministic tamper detection of inconsistent packets (not cryptographic authentication).
- Added 13 regression tests, chrome/orange interactive Pages lab, formal scope note, claims and lexicon entries.


## 2026-11-09 — QG-043 · Unseen-Game Transfer
- Held out all game identities from a designated transfer set instead of only chronological samples. Candidate utility weights are selected on training games only; transfer outcomes independently gate adoption.
- Added disjoint-identity leakage checks, dual-mode coverage, insufficient-data guards, append-only replay, and deterministic success/failure/baseline synthetic experiments.
- Added eleven regression tests, a GitHub Pages interactive viewer, formal specification, CI workflow, updated lexicon and claims ledger. No claim of universal generalization or actual subjective enjoyment.


## 2026-11-09 — QG-042 · The Observer's Discovery
- Added a bounded deterministic test for updating the player's *reward model*: select a candidate using past training outcomes and adopt only after independently reserved holdout data shows improvement.
- Preserved QG-041 original event history and labels with replay verification, fail-closed comparison, negative and distribution-shift cases; synthetic proxy rewards are not real enjoyment.
- Added eleven regression tests, interactive Pages laboratory, formal specification, claims ledger update and GitHub Actions workflow.


## 2026-11-09 — QG-041 · Emergent Observer Preference
- Modeled a veteran player learning a reversible preference between single-game play and simultaneous multi-game observation, using only recorded sample utility—not a forced 24! counter transition.
- Kept 24! as a symbolic experience-space maximum and any enormous prior-game count explicitly unverified; implemented deterministic novelty, breadth, payoff and attention-cost utility with append-only history.
- Added eleven adversarial/unit tests, browser visualization, formal specification, actions workflow and claims ledger. No subjective enjoyment or autonomous agent asserted.


## 2026-11-09 — QG-040 · Revocation Freshness
- Added a P-256 root-signed checkpoint binding a canonical complete-declared revocation collection, publication sequence and bounded validity interval.
- Verification rejects missing, expired, future-dated, rolled-back, altered or wrongly signed checkpoints; reuses QG-039 to check delegated signing authority after freshness.
- Added interactive Pages lab, formal spec, eleven adversarial tests and GitHub Actions workflow. Root-declared completeness does not prove real-world revocation completeness; clock and high-water mark are external.


## 2026-11-08 — QG-039 · Trusted Key Lineage
- Added externally pinned trust-root authorization for QG-038 attestations using signed P-256 delegation certificates and bounded role chains.
- Added signed root revocations, explicit evaluation time and failures on expired, substituted, unauthorized or invalid signers; separate trust-root custody remains mandatory.
- Published interactive Pages viewer, specification, nine adversarial regression tests, GitHub Actions workflow, and updated claims ledger. Revocation freshness is not yet established.


## 2026-11-08 — QG-038 · Authenticated Origin
- Added experimental ECDSA P-256 / SHA-256 signed attestation covering the full QG-036 carrier and separately supplied QG-037 manifest, after independent structural verification.
- Verification requires a public key obtained through an external trust boundary. The browser lab uses a disposable demo key; signer labels, original source authenticity and truth remain unproven.
- Published nine regression tests, interactive Pages lab, formal specification, claim classifications and CI workflow.


## 2026-11-08 — QG-037 · Independent Closure Witness
- Introduced a separate read-only verifier that unfolds the terminal QG-036 tree without invoking QG-036 recovery, checks 8→4→2→1→1 intermediate stages and compares all four complete witness chambers against a separate QG-035 manifest.
- Compared wrapper verdict and original event history against that manifest because neither is encoded within the 8 witness leaves themselves.
- Added nine adversarial regression tests, interactive Pages lab and CI workflow. Authenticity depends on independent, trustworthy manifest custody, not on JSON equality alone.


## 2026-11-08 — QG-036 · Lossless [84211] Closure
- Added explicitly non-compressive 8→4→2→1→1 nested pair transport, retaining four sealed 1311 boxes and exact QG-035 replayable history.
- Final 1→1 closure is an unchanged full nested tree; recover all 8 leaves, 4 sealed identities, 24 faces and judge ruling. Reject incomplete or tampered representations.
- Published interactive fold viewer, eight regression tests, formal spec and GitHub Actions workflow. Neither quantum processing nor Byzantine consensus is claimed.


## 2026-11-08 — QG-035 · One [84211] Byzantine Box
- Added four bounded 1311 actor chambers inside one symbolic 8→4→2→1→1 enclosure; 24 internal face slots tracked and sealed individually.
- Judge D cannot seal before A/B/C and cannot rewrite prior reports; one subsequent verdict is additive and never proves truth.
- Added deterministic event replay, seven regression tests, an interactive Pages viewer and CI workflow. Byzantine-inspired, not proven distributed consensus or actual quantum processing.


## 2026-11-08 — QG-034.3 · Scheduled GitHub Kernel Verification
- Scheduled GitHub Actions daily at 09:17 UTC with optional manual dispatch. Runs regression suite, deterministic kernel instantiation and strict three-witness/one-origin invariant guard.
- Uploads a 90-day JSON status artifact; limited to read-only repository permissions. No automatic edits or persistent runtime memory.


## 2026-11-08 — QG-034.2 · Canonical Kernel Instantiation
- Added deterministic `language/instantiate-kernel.mjs` boot entrypoint to instantiate verified QG-033 and QG-034 ledgers from an explicitly synthetic three-reports/one-origin fixture.
- Added three boot tests and the boot command to the README. No autonomous source authentication, real-world claim promotion or background persistence implied.


## 2026-11-08 — QG-034 · Witness Lineage
- Added separate QG-034 ancestry DAG over a replay-verified QG-033 trio; trace back to terminal origins, detect shared origin ancestry and transitive witness dependence.
- Count conservative connected independent lineages rather than three hosts or three votes; preserve exact source witness URLs and their original histories.
- Published a graphical interactive lineage explorer, formal specification, eight tests and append-only human review events. Origins are attributed, not authenticated; historical truth is never inferred.


## 2026-11-08 — QG-033 · Three-Witness Root Consensus
- Built `language/three-witness-roots.mjs` for 3 distinctly named observations at the same historical leaf root, retaining each HTTPS source and declared independence rationale.
- Bound three witnesses to the subject glyph's existing QG-028 60-ring phases a/b/c, classifying unanimous support, unanimous challenge, split and incomplete groups without asserting truth.
- Added append-only human source-reviewed decisions, deterministic impacted dependency addresses, `three-witnesses.html`, a formal spec and seven regression tests.

## 2026-11-08 — QG-032 · Root Reconciliation
- Built `language/root-reconciliation.mjs` to preserve opposing, cited observations of one original QG-030/QG-031 leaf root with a complete append-only event history.
- Captured deterministic impacted downstream claims, required explicit review choices with supporting evidence and retained both original witnesses without rewriting source statements.
- Published `reconcile.html`, formal QG-032 specification and seven regression tests, all passing GitHub Actions.

## 2026-11-08 — QG-031 · Root Roots Propagation
- Implemented `language/root-propagation.mjs` as an append-only multi-version evidence ledger; updates to documented leaf roots propagate forward through all reverse dependency links.
- Canonically recorded changed-root addresses, impacted dependent claims, preserved prior snapshots and review-required flags without silently promoting interpretation truth.
- Published `root-roots.html`, technical specification and seven regression tests. GitHub Actions suite passed.

## 2026-11-08 — QG-030 · Chasing Roots
- Introduced `language/chasing-roots.mjs`: a deterministic backward prerequisite DAG for QG-029 contextual `WHICH MEANS` claims, bounded to 60 nodes and 180 declared links.
- Preserved exact nested contextual claims and 60-ring role phases. Tracked documented roots, unresolved leaves, disconnected statements, and cycle/chronology validation.
- Added a non-cryptographic deterministic fingerprint to detect accidental edits to existing packets. Neither links nor fingerprints independently prove factual accuracy.
- Published `roots.html`, `language/QG-030-CHASING-ROOTS.md`, and seven CI regression tests.

## 2026-11-08 — QG-029 · Societal Somatics
- Added a source-oriented `IS → WAS → WHICH MEANS` grammar with exact historical year, IANA time zone, geographic place, group, evidence URL and epistemic status.
- Bound contextual statements to 3 distinct 60-ring phase slots via QG-028, while preserving complete canonical glyph witnesses and somatic drawing verbs.
- Added caller-assigned authority/reach/legacy context scales with confidence and rationale; cross-group/place numeric comparison explicitly refused.
- Published `society.html` interactive viewer, source documentation and seven regression tests.

## 2026-11-08 — QG-028 · SEE/DO/LEARN Ring Binding
- Bound every QG-027 A–Z semantic triad to three distinct QG-026 sixty-ring quadrant phase addresses using the first canonical glyph vertex as a deterministic anchor.
- DO carries complete ordered somatic stroke verbs; SEE and LEARN carry full source glyph geometry and authored role words without claiming actual perception or learning.
- Added executable `language/semantic-ring.mjs`, `triad-ring.html` viewer, formal spec and six automated tests. 

## 2026-11-08 — QG-027 · Semantic Triads
- Defined exactly 78 first-letter-aligned SEE/DO/LEARN vocabulary terms across all 26 QUANTA uppercase glyphs.
- Created `language/semantic-triad.mjs`, the formal vocabulary specification and five automated tests.
- Lexicon labels are assigned semantic roles, not autonomous inference or new physics; QG-026 geometry is preserved unchanged.

## 2026-11-08 — QG-026 · Alphabet on the 60 Ring
- Implemented `language/alphabet-ring.mjs`, bridging all 26 QG-016 vector glyphs to QG-025 sixty-station transport. The 25 unique 5×5 source vertices map injectively to even home stations 0..48, with each 90° phase represented by +15 modulo 60.
- Every source stroke, semantic glyph ID and ordered somatic PEN_UP/MOVE/DRAW/TURN action retains explicit phase-addressed witnesses. Spaces remain exact and reset the per-word phase schedule.
- Published `ring-language.html` with a paired canonical 5×5 glyph viewer and full 60-station ring, four quarter-turn controls, editable phrase transport and exact recovery.
- Added QG-026 specification and seven automated tests; GitHub Actions passed. Phase address shifts are not claimed to be physical glyph rotation or data compression.

## 2026-11-08 — QG-025 · Sexagesimal 60 Ring
- Built `language/sexagesimal-ring.mjs` using Babylonian-inspired powers-of-sixty place values with exactly 60 positions, four 15-station phase quads, and deterministic +15 mod 60 quarter-turn transport.
- Added reversible BigInt conversion and exact 4-turn phase recovery, `sixty.html` interactive ring, formal specification citing independent historical research, seven tests and GitHub CI.
- Distinguished historical Babylonian sexagesimal notation, the separate Indian/Vedic number traditions, and the modern QUANTA phase geometry. The GitHub Actions tests passed.

## 2026-11-08 — QG-024 · Convergent Memory Growth
- Added `language/memory-growth.mjs`: a replayable append-only directed ancestry graph containing full QG-020 corpus snapshots, one-parent branches, two-parent convergences and explicit common ancestor references.
- Convergence reuses QG-023's three-way paragraph rules and rejects unresolved conflicts; prior branches are never modified.
- Published `growth.html` interactive ancestry graph, QG-024 specification and seven automated tests. The GitHub Actions suite passed.

## 2026-11-08 — QG-023 · Memory Convergence
- Added `language/memory-convergence.mjs` with common-ancestor matching, explicit three-way paragraph comparisons, preserved two-parent history, and no silent conflict winner.
- Published `convergence.html`, a two-branch visual comparison/merge console, and QG-023 formal specification and regression tests.
- Current scope: identical document hierarchy and reference topology; paragraph-text edits only. Structural differences deliberately fail closed.

## 2026-11-08 — QG-022 · Memory Projection
- Added `language/memory-projection.mjs`, selecting a QG-021 corpus revision through a single visible Chrome Dot while retaining full source and lineage in the ledger.
- Added a revision-specific 4→3→2→1 projection, exact historic source unfolding, backward parent-chain walk and source-address tracing.
- Published `projection.html`, seven regression tests and the QG-022 specification. The dot is a reference, never a self-contained corpus compressor.

## 2026-11-08 — QG-021 · Corpus Memory
- Implemented `language/corpus-memory.mjs` with immutable append-only full corpus snapshots, parent revision IDs, and paragraph lineage across edits, additions, retirements, and explicit moved-address mappings.
- Added `memory.html` for local revision timelines, historic source retrieval, traceable paragraph addresses and JSON ledger export/import.
- Added QG-021 formal specification and seven tests; the GitHub Actions suite passed.
- Memory is a deterministic model: browser state does not persist automatically and revision IDs are local rather than cryptographic hashes.

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
