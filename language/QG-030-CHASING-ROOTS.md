# QG-030 — Chasing Roots

Carrier: `||||`. The next natural boundary after QG-029 contextual `IS → WAS → WHICH MEANS` is to ask what must be established for an interpretation to follow.

## Invariant

```text
WHICH MEANS (target interpretation)
     ↓ REQUIRES
prior historical claims
     ↓ REQUIRES
earliest source roots / unknown or disputed leaves
```

The engine stores an explicit *directed acyclic dependency graph* of statements. Each prerequisite names an earlier or contemporary context-year claim. Every node has a status: `sourced`, `annotated`, `hypothesis`, `unknown`, or `disputed`; sourced nodes require at least one HTTPS evidence URL. Each causal edge means "the author declares this is required"; a link does **not** establish logical entailment or historical truth.

A backward root chase traverses all reachable prerequisites in deterministic input order and returns roots, evidence gaps, and facts not connected to the target. An uncited leaf is a gap even if the statement is plausible. An `unknown` or `disputed` internal statement is also a gap.

QG-029's source context (historical year, IANA time-zone annotation, group/place, evidence, user-assigned social weights) remains intact. The three 60-ring role stations remain attached to the IS, WAS and WHICH MEANS witnesses. A time zone is not a social weight, historical proof, or a calendar conversion.

**Example:** "Ada Lovelace's notes explored the Analytical Engine's wider possibilities" may depend on the text of her 1843 notes, the proposed machine and her earlier mathematical education. Annotate each link, cite the corresponding historical sources, and mark missing support explicitly.

## Constraints

- Maximum 60 fact nodes and 180 prerequisite links.
- Years represented are CE 1–9999; the prerequisite year may not exceed the containing claim's year.
- No cycles, missing referenced nodes, duplicate IDs or repeated dependency IDs.
- Exact canonical reconstruction checks every node, social context and phase witness. Structural verification is not cryptographic authenticity.
- `interpretationProven:false` is intentional; the program does not prove factual or causal claims.

## Artifacts
- [Executable root tracer](./chasing-roots.mjs)
- [Seven regression tests](../tests/chasing-roots.test.mjs)
- [Interactive lab](../roots.html)
