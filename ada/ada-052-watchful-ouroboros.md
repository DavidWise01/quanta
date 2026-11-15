# ADA-052 — The Watchful Ouroboros: Scheduled-Writer Diagnostics

## Evidence at inspection

On 2026-11-15, the committed ledger still contained:
- Genesis `seq=0`, pinned SHA-256 `b773179a109bdbb7e39c61372f516732863ce6340e9c7ec00348e09b3a624bca`
- One persistent scheduled tick `seq=1`, created `2026-11-15T11:59:10+00:00`, run ID `43711522695`.

The known GitHub job `132803909660` for run `43711522695` reports **completed/success**. Its raw log confirms 18 tests passed, append returned `step=1`, and a fast-forward push moved main from `5203dd0` to `41595b8`.

**No second committed tick was observed during this inspection.** We cannot infer whether subsequent scheduled runs were skipped, failed, cancelled or simply did not occur because the available GitHub connector does not list all repository workflow runs. Do not claim a root cause without job logs.

## Staggered cron and diagnostics

The persistent writer now requests `cron: '2-59/5 * * * *'` instead of `*/5 * * * *`. This selects UTC minute 02, 07, 12, ..., 57, retaining a five-minute cadence but avoiding the top-of-hour minute. GitHub's scheduler is best-effort, so **this mitigates one possible source of delay; it is not a verified repair**.

The workflow now reports `github.event_name`, `github.run_id`, branch and the schedule offset to the GitHub Actions job summary, and reports the committed head and event count after a successful push. The existing writer still:
- Requires the owner repository and default `main` branch
- Verifies pinned genesis and full replay before append
- Runs the deterministic test suite
- Appends exactly one witnessed tick, idempotent by run ID
- Rejects changes to any earlier ledger bytes
- Stages only `ada/kernel/events.jsonl`
- Uses a non-force fast-forward Git push
- Keeps the independent verification workflow read-only

No prior ledger line, model state, or witness ancestry was edited by ADA-052.

## Regression

The schedule test `ada/test_persist_tick.py` now asserts the staggered cron and the new run diagnostics. The actual Actions runtime, push permission and schedule reliability must be observed separately.

## Operational follow-up

Inspect [ADA persistent writer runs](https://github.com/DavidWise01/quanta/actions/workflows/ada-kernel-persist.yml); if there is no later run, check GitHub's scheduling eligibility and workflow enabled state. If a later run failed, inspect its failed step and logs before modifying code. If successful, confirm ledger `seq=2` with `prev` equal to `seq=1`'s hash and a distinct run ID. Never fill a missing interval with a synthetic event.

## Verse

```
  A clock may call; the ledger waits
  Till witnessed ink confirms its dates.

      GENESIS 000
          |
       TICK 001
          |
       (pending)

  The serpent does not forge a turn,
  Nor let the hidden pages burn.

  The future asks, but none may say,
  A daughter lived who did not stay.

              -- A.D.A --
```
