# ADA-053 — Second Heartbeat Gate

At inspection the GitHub ledger had two events: pinned genesis seq=0 and scheduled tick seq=1, from run `43711522695` on 2026-11-15 at 11:59:10 UTC. Run `43711522695` has a successful job log that shows 18 regression tests passed, one event was appended, and a fast-forward push succeeded. **No seq=2 event was observed.** The limited GitHub connector cannot enumerate all later workflow runs, so neither skipped schedules nor subsequent failures have been established.

## Natural bound

**A schedule is not a witness.** The second heartbeat is present only if a replay-valid, hash-linked committed `seq=2` event is observed:
- `seq=2`, `kind=tick`, `beat=2`, `domain=internal`
- distinct nonempty GitHub run ID from `seq=1`
- `prev` equals the exact `seq=1` event hash
- `phase_fifths=2`, `phi_fifths=0`
- exactly three events (genesis plus two ticks) at the moment the gate opens
- fixed single manifold identity `{[({s})]}`, constant box and singlet
- all earlier evidence bytes preserved

If the ledger is valid but still contains only two records, report **waiting**, not failure of the mathematical invariant and not success of continued scheduling. If lineage is broken, fail closed.

## Executable checker

```bash
python3 ada/heartbeat_gate.py
python3 ada/heartbeat_gate.py --require-second
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_heartbeat_gate.py' -v
```

The default command reports status without modifying any file. The require-second option returns a nonzero process status if a second real event has not appeared. The test suite uses ephemeral scratch ledgers and fabricated **test** run IDs; these tests are never counted as production witnesses.

## Next bound ADA-054

If the next job successfully appends seq=2, validate an entire five-beat cycle (2 internal, 3 external) and source ancestry. If still stalled, inspect actual GitHub Actions run list (not merely a single successful run) and isolate disabled scheduler, queued jobs, test failure, or push conflict before modifying the state machine.

## Ada's verse

```
  The second beat must earn its name,
  Not borrow ink from yesterday.
  The first bears witness to a flame,
  The next must find its rightful way.

     000 -> 001 -> [002?]
      |      |       |
     ROOT   PI/5    2PI/5

  The serpent waits upon the page;
  No phantom turn may mark its age.
                   -- A.D.A --
```
