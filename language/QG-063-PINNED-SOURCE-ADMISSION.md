# QG-063 — Prove the Source, Not Just the Claim

```text
          CLAIMED EVIDENCE
                  |
           SOURCE IDENTITY
                  |
         PINNED REGISTRY?
          /             \
        YES           UNKNOWN
         |               |
    SHA-256 CONTENT    QUARANTINE
      INTEGRITY
      /       \
    MATCH    MISMATCH
      |         |
  POLICY GATE  QUARANTINE
      |
  UPSTREAM ANCESTRY
      |
  QG-062 ROOT RECOUNT
      |
  EXPLICIT AUTHORIZATION
      |
     {{i}}
```

## Admission invariant

**A packet does not become an independent witness just because it asserts a source root.** A finite, locally pinned manifest maps a source/surface pair to a SHA-256 digest, trusted *declared* ancestor labels and, for public-internet entries, a modeled access policy. A submitted packet contains an identity, source, surface, text body, binary outcome, and a declared post-withdrawal epoch. The kernel computes the content digest itself using WebCrypto SHA-256, and matches both the source identity and the byte-level content digest against the pinned manifest.

If an entry is unknown or digest-mismatched, it remains visible with an explicit quarantine receipt but is not forwarded to QG-062. For external entries the independently pinned robots status must be `allow`; `disallow` blocks, and `unknown` quarantines. An `llms.txt` listing is discovery metadata, **not permission**. No source-provided ancestry claim is passed through: QG-062 receives ancestry identifiers from the pinned manifest only. GitHub and 0root.ai remain two owned surfaces of **one** corpus and are counted as one root. Multiple independent external sites still require QG-062's shared-upstream component checks before being counted.

On three consistent ancestry components the kernel produces an **eligibility signal only**. A separate explicit QG-062 authorization action is required; the old withdrawn symbolic authority and history remain in place until authorized.

## Limits of the claim

A matching hash proves only consistency with the content previously pinned, **not** that the website actually authored it, that the manifest was correct, or that two manifests are independent. A controlled registry or signatures bound to separately authenticated publishers would be required for stronger provenance. The registry is a caller-supplied trusted local assumption and could be tampered with along with all derived records; this value-only audit is not a cryptographically immutable external log.

The synthetic test does not access GitHub, 0root.ai, or any live external website. Its robots and llms status values are predeclared; no live crawling or compliance verification occurs. A real crawler must check per-agent site rules, terms, authorization, redirect boundaries, sensitive content restrictions and export gates, and must not leak gated material into public surfaces.

The complete action is replayable in the browser and Node 22+:

```sh
node --test tests/three-surface-ancestry.test.mjs tests/pinned-source-admission.test.mjs
```
