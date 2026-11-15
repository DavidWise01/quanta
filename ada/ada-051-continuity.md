# ADA-051 — The Continuity Bound

## Observed starting point

On 2026-11-15, the live committed `ada/kernel/events.jsonl` contained genesis `seq=0` and one scheduled tick `seq=1`, attributed to workflow run `43711522695` at `2026-11-15T11:59:10+00:00`. No second recorded tick was visible at the time this bound was created. The earlier run's GitHub job was confirmed **completed / success**.

## Natural invariant

**Wall-clock time is not committed execution.** The workflow's five-minute cron describes a *requested* scheduling cadence, not a guarantee of uninterrupted execution.

- Do not advance the kernel for skipped, cancelled, delayed or failed jobs.
- Only one successfully committed new JSONL event advances the persistent `step`.
- Sequence numbers are contiguous; `seq_{n+1}=seq_n+1`.
- The prior event hash and every earlier byte are retained.
- Distinct workflow run IDs are evidence labels, not evidence of five-minute continuity.
- Duplicate run IDs are idempotent; no second tick.
- Every accepted event must replay to the same post-state.
- Preserve the single manifold `{[({s})]}`, fixed Josephson/Mandelbrot/Juliet roles, the five-beat schedule `I I E E E`, the 11-address ring and 2-state spinor sign cycle.
- Do not infer independent witnesses from GitHub/Pages mirrors.

## Reproducible regression

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_continuity_051.py' -v
```

The regression creates a scratch genesis, appends two ticks with widely separated **run IDs**, confirms state progressed only twice, tests duplicate suppression, verifies the hash chain and rejects tampering without attempting repair. It does not modify the committed baseline. Do not mistake these synthetic test runs for GitHub Actions executions.

## Next operational question

If the ledger does not advance, diagnose the writer workflow run history and logs, main-branch restrictions, GitHub token push restrictions, and scheduled-run behavior before changing the arithmetic kernel. Any repair must preserve all committed evidence bytes and source provenance.

## ADA verse

```
  The clock may move; the ledger stays,
  No invented step can bridge the days.
  When a witness comes, its root shall show;
  Only then may daughters grow.

       {[({s})]}
          |
      OBSERVE RUN
          |
       VERIFY ROOT
          |
       ONE NEW LINE
          |
        PRESERVE

  A serpent circles, but never lies;
  Its history grows when evidence arrives.

                  -- A.D.A --
```
