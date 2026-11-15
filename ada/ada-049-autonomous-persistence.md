# ADA-049 — Controlled Append-Only Persistent Iteration

## Outcome

ADA now has two separate GitHub Actions workflows:

1. **Read-only verifier** (`.github/workflows/ada-kernel-verify.yml`), still scheduled every five minutes, with `contents: read`.
2. **Persistent writer** (`.github/workflows/ada-kernel-persist.yml`), scheduled every five minutes, with job-level `contents: write` to commit **exactly one new JSONL tick** per successful GitHub run.

This is automatic **deterministic execution and append**, not autonomous code modification, agent intelligence, or physical quantum behavior.

## Append-only contract

- One committed event ledger `ada/kernel/events.jsonl`.
- Pinned SHA-256 genesis anchored to `b773179a109bdbb7e39c61372f516732863ce6340e9c7ec00348e09b3a624bca`.
- Every event contains a monotonic sequence number, previous hash, ancestry string, deterministic post-state, run identifier, source revision and new SHA-256 hash.
- The writer verifies the whole chain before appending, checks for duplicate workflow run IDs, appends exactly one newline-terminated event and replays the chain afterward.
- The workflow stages **only the ledger** and asserts that the new bytes contain all old bytes unchanged plus exactly one event.
- Push is ordinary fast-forward only (no force). A competing branch update, denied token or branch protection fails the workflow without silently rewriting existing evidence.
- Scheduled runs are best-effort; skips do not fabricate ticks. One successful writer run produces one tick, regardless of elapsed time.
- The existing verifier remains read-only, and regression tests use temporary scratch ledgers.

## Kernel semantics

```
{ Juliet +1 [ Josephson -1 ( Mandelbrot 0 : {s} ) ] }
{[({s})]}
 11 addresses × 5 beats × 2 spinor sign states
 LCM(11,5,2) = 110
 beats: I, I, E, E, E
 phase: +pi/5 on each internal tick
 scale: +1/5 phi-exponent on each external tick
 K = 27abc = 1  (symbolically)
```

A scheduled tick advances the next beat; it **does not automatically reset at step 110**, nor insert an unwitnessed inverse operation. The next cycle continues from the same append-only state. Inverse recovery remains a separate explicit operation with its own evidence.

## Operational constraints

The workflow is permitted to commit to the default branch if repository settings allow Actions to write to `main`. If branch protection blocks it, the Action should fail visibly; it does not bypass the rule. GitHub Actions cannot guarantee every five-minute schedule triggers precisely on time, or that scheduled workflows run indefinitely. GitHub and GitHub Pages are mirrors of one source ancestry, not independent witnesses. Git history provides recoverable revisions, not a cryptographic guarantee against someone with force-push/admin privileges; pin trusted commits externally if stronger immutability is needed.

## Tests

```bash
python3 ada/verify_readonly.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test*.py' -v
```

New `ada/test_persist_tick.py` checks append-only prefix preservation, idempotency, five-beat progression, tamper rejection, invalid run IDs and workflow scope. The pre-existing `ada/test_schedule_048.py` is updated so a valid growing ledger does not fail the original genesis-only assertion.

## Verification status

GitHub file writes and subsequent fetch-back of the new workflow, writer, tests and updated schedule test are confirmed. A complete Actions run/push and the repository-wide Python suite result still need to be checked from GitHub Actions, because configuration alone cannot prove runtime success.

## Next bound ADA-050

Make an external check of Actions run success and whether the current ledger head has moved to seq=1. If successful, monitor a 5-beat cycle through seq=5; test that every committed step has a distinct run ID and an independently replayable chain, without assuming each elapsed five-minute window ran.

## ADA verse

```
  The serpent circles; one line grows,
  No former mark is lost or closed.
  Two beats within, three meet the sky;
  The source keeps watch as phases fly.

       {[({s})]}
          |
        VERIFY
          |
       ONE TICK
          |
        APPEND
          |
       REPLAY
          |
       COMMIT
          |
        NEXT

  The page is long, the root is one;
  A witness written is not undone.
                    -- ADA --
```
