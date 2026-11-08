# QG-029 — Societal Somatic Context (IS → WAS → WHICH MEANS)

Carrier `||||`. QG-029 adds **contextual social semantics** to the QG-028 SEE/DO/LEARN 60-ring binding.

```text
subject at contextual place and year
  IS          contemporary role/description as of contextual year
  WAS         preceding role/event, timestamped at a year not after IS
  WHICH MEANS explicitly attributed interpretation or consequence
```

Three statement anchors reuse the semantic 60-ring phase positions of their chosen uppercase glyph: `IS→a`, `WAS→b`, `WHICH MEANS→c` at entry phase 0, with the QG-028 DO somatic drawing verbs attached to WAS. These are **symbolic phase slots**, not signals of objective social rank, and drawing verbs are not physical behavior.

The **context witness** includes:
- Historical `year` (integer CE 1–9999) and prior `wasYear`.
- `timezone` (IANA zone ID, e.g. `Europe/London`).
- `place` and `group` (the actual societal frame used to assess a role).
- `evidence` (HTTPS URLs with source labels), and epistemic status (`sourced`, `annotated`, `hypothesis`, `fictional`).
- Human-assigned, **ordinal** weights on `authority`, `reach` and `legacy` from 0–5, a 0–1 confidence annotation and explanatory `basis`.

**Do not infer importance from gender, title, identity or timezone.** A time zone translates clocks; a historical year/era, polity, social group and documentary sources explain the relevant societal context. If two records concern different groups or places, the engine refuses numerical weight comparison. Even in matching scopes, their difference is a comparison of *caller-provided ratings*, not an established social science measurement.

Example: Ada Lovelace as a British mathematical writer in 1843; earlier study and collaboration with Charles Babbage; her 1843 notes discussed the Analytical Engine's general-purpose potential. Evidence: [Science Museum Group](https://collection.sciencemuseumgroup.org.uk/people/cp38764/ada-lovelace), [Oxford History of Science Museum](https://www.hsm.ox.ac.uk/imagining-ai), and [original 1843 notes](https://www.yorku.ca/pclassic/Lovelace/lovelace.htm).

A statement such as *"a king was exempt from all laws"* is **not a generic historical rule**. The law, place, historical period and sovereign privileges must be independently evidenced. A deliberately fictional king example carries `status:fictional`, not factual authority.

The historical year and timezone in this iteration are **source annotations**; the kernel validates them but does not compute historic local civil times, medieval timezone transitions, calendar reforms, or legislation. Those would require dedicated, independently sourced models.

## Transport and validation
- `bindSocialContext(claim)` produces the canonical packet with role stations, QG-028 glyph/verb witnesses, context and evidence.
- `recoverSocialContext(packet)` rebuilds and checks all witnesses and returns the exact contextual claim.
- `compareSocialContext(a,b)` checks the same subject and group/place before computing **ordinal annotation differences**, never inherent rank.
- `verifySocialContext` returns pass/failure without throwing.

## Artifacts
- [Executable kernel](./societal-somatic.mjs)
- [Seven tests](../tests/societal-somatic.test.mjs)
- [Interactive lab](../society.html)
