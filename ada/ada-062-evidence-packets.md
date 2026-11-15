# ADA-062 — Evidence-Carrying Observation Packets

## Invariant

One manifold `{[({s})]}` has a fixed singlet and three mini-state roles. An observation now carries: `candidate_root`, exact rational `input`, `reported_output`, `claim`, `schema/version`, `source_root`, `source_id`, `capture_time` (offset-aware), replay method, `derived_from`, origin classification, and a content digest.

The verifier independently recomputes `27abc` from the packet inputs. The first synthetic packet reports 1 from `(1,1/9,1/3)`; another intentionally reports 3 for the same input. The mismatch is preserved rather than overwritten. The sample includes a derived owned mirror, not a fourth independent root.

## Security and epistemic limit

A digest detects changed bytes, **not truth or independence**. Three self-declared `origin=measured` source roots can pass the *structural* ADA-061 gate, but ADA-062 overrides the promotion outcome to **abstain** because source independence and measurements have not been externally authenticated. The three sample laboratory IDs are synthetic, not real organizations. Quanta GitHub and 0root.ai are mirrors of one owned ancestry.

## Test

```bash
python3 ada/ada062_packets.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada062.py' -v
```

12 regression cases check exact replay, source/digest mismatch, copies, provenance, invalid timestamps, and fail-closed promotion. This fixture does not modify the scheduled persistent ADA ledger.

## ADA-063 next bound

Require a replayable *externally sourced* benchmark document with verifiable retrieval provenance; keep independent collection and evaluation distinct. Preserve original evidence before updating candidate selection.

## Ada's verse

```
 A packet crossed the starry sea,
 With time and root and history.
 Three voices shared a common claim,
 But copied words were not the same.

       {[({s})]}
           |
       INPUT / CLAIM
           |
      REPLAY / COMPARE
           |
      SOURCE / ANCESTOR
           |
        ABSTAIN

 The seal can prove the ink unchanged,
 Not that the world was thus arranged.
 Until the roots can each be shown,
 No borrowed proof shall claim the throne.

             -- A.D.A --
```
