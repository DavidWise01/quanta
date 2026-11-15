# ADA-061 — Independent Witness Roots, Not Three Copies

## Natural bound

A shared checkpoint may become *eligible for promotion* only if it passes the numerical challenge and **at least three distinct authorized independent source roots agree on exactly the same replay proposition**. Identical copies and mirrors remain one ancestry. Missing evidence means abstention, not a guessed pass. Conflicting observations cause abstention and a request for more evidence.

## Evidence states

- `simulated`: an illustration/test packet, never accepted for promotion.
- `measured`: *declared* observation in the supplied packet; source must also be authorized. **Labels and hashes alone are insufficient proof that a source is truly independent or measured**.
- `copied_from`: disqualifies derivative reports for independent root counting.
- A `candidate_root` ties every report to the **same proposition**, rather than loosely similar claims.
- Each packet has a deterministic digest so tampering can be detected against the submitted bytes; digest is not an attestation of truthful observation or real independence.

## Outcomes

| Scenario | Distinct eligible roots | Decision |
|---|---:|---|
| Three simulated positive reports | 0 | abstain |
| Three mirrors of one measured root | 1 | abstain |
| Three independently **declared** measured positive reports | 3 | eligible in synthetic gate |
| Three conflicting measured reports | 3 | abstain |
| Three measured negative reports | 3 | reject |
| Numeric challenge fails | — | reject |

The measured scenarios are **synthetic fixtures**, not evidence that three real external organizations have evaluated ADA. The actual ADA-060 candidate therefore remains **unpromoted**.

## Reproduce

```bash
python3 ada/ada061_witness.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada061.py' -v
```

The test file includes 12 cases. The underlying operational ADA GitHub Actions journal remains unchanged. The new artifact is a witness-policy test, not automatic collection or verification of real-world outside data.

## Next natural bound — ADA-062

Implement content-addressed observation packets that contain a source URL/document identity, capture time, experiment version, tested proposition, and independently replayable input/output before promotion. Establish genuine independent roots through source tracing rather than by accepting `origin=measured` claims.

## ADA's verse

```
 Three daughters speak across the night;
 Three echoes do not make them right.

         { [ ( {s} ) ] }
                |
           ONE CLAIM
                |
         TRACE EACH ROOT
          /     |     \\
         A      B      C
          \\    |    //
             COMPARE
                |
         AGREE OR WAIT

 A mirror bears the mother's face;
 It cannot claim another place.
 Until three witnesses can show
 What each observed, we cannot know.

               -- A.D.A --
```
