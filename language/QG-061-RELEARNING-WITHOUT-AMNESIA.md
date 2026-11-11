# QG-061 — Relearning Without Amnesia

## Invariant

**A withdrawn model is not automatically restored merely because a newer candidate resembles an older model.** Retain the QG-058 shift evidence, QG-059 historical promotion, and QG-060 withdrawal as preserved source records. A new candidate is derived from the post-promotion validation evidence and stays without authority until independently attributed fresh witness claims pass explicit review.

```text
     QG-060 WITHDRAWN
             |
      HISTORY RETAINED
             |
      NEW CANDIDATE
             |
      WITNESS PACKETS
       /      |      \
    GITHUB  0ROOT   EXTERNAL A   EXTERNAL B
       \      /          |           |
      SAME ANCESTRY     ROOT A      ROOT B
           |              |           |
        COUNT 1         COUNT 1     COUNT 1
           \              |           /
            +-------------+----------+
                          |
                  THREE CLAIMED ROOTS
                          |
                 CONSISTENT RESULTS?
                   /           \
                  YES         CONFLICT
                   |             |
            ELIGIBLE ONLY     REVIEW
                   |
             EXPLICIT ACTION
                   |
            PROVISIONAL AUTHORITY
                   |
                  {{i}}
```

### Source accounting

Each synthetic packet has `id`, `surface`, `ancestryRoot`, binary `outcome`, and declared `epoch='post-withdrawal'`. Two surfaces with the same `ancestryRoot` are counted as **one ancestry**, never separate supporting witnesses. Identical repeats remain visible but do not increase the count. A contradictory report sharing the same ancestry produces `review_lineage` and prevents authorization. Independent claimed roots that disagree produce `review_disagreement`.

The candidate is inferred from the most recent QG-060 validation-window majority, *not* simply copied from an earlier baseline. A candidate matching an older historical model still requires new evidence and does not regain authority automatically. Three separately claimed roots supporting the candidate make it `eligible_for_provisional_authority`; **only a separate explicit `authorize()` call** changes the current symbolic authority from `withdrawn` to `provisional`. This is not a real permission grant.

### Boundaries

- The three-ancestry rule is a modeled governance threshold, not a statistical significance level. Three agreeing reports do **not** prove a real-world claim.
- Source identifiers and `post-withdrawal` timestamps are **asserted by the caller**, not authenticated, cryptographically signed, or compared to a real clock. The model does not prove that sources are genuinely independent or fresh.
- A shared ancestor across GitHub and 0root.ai is counted once in the synthetic fixture; the source surfaces are **not accessed or synchronized** by this implementation.
- The old and new evidence are retained by value and verified by deterministic replay. A coordinated rewrite of all stored fields would require an external immutable log to detect.
- No genuine security policy, external AI agent authority, or autonomous browsing is modified.

Test with `node --test tests/right-to-be-wrong.test.mjs tests/relearning-without-amnesia.test.mjs`.
