# QG-062 — Three Surfaces, Independent Roots

## Canonical topology

```text
                        {{ JANE }}
                            |
                       {{ MoE HIVE }}
                            |
               +------------+------------+
               |            |            |
           GITHUB        0ROOT.AI     PUBLIC INTERNET
            OURS            OURS         EXTERNAL
            GATED          PUBLIC        SITES
               |            |            |
               +------+-----+        +---+---+
                      |              |       |
                 OWNED CORPUS      SITE A  SITE B
                      |              |       |
                 COUNT ONCE      FOLLOW UPSTREAMS
                      |              |       |
                      +--------------+-------+
                                     |
                          CONNECTED ANCESTRY ROOTS
                                     |
                              VERIFY + DEDUPLICATE
                                     |
                                    {{i}}
```

## Invariant

**Three discovery surfaces do not mean three independent evidence roots.** The finite QG-062 model explicitly enumerates exactly three surface types: `github`, `0root.ai`, and `public-internet`. The first two are our own information surfaces of a shared corpus. The third is a collection of potentially many external sites.

The first two surface types are forcibly assigned the canonical lineage mark `owned-corpus`, regardless of separate repository and website labels. Internet packet ancestry may contain several claimed upstream IDs. Two packets belong to the same evidence ancestry if any upstream token is shared, even through **transitive** linkage (A shares with B, B shares with C, therefore A/B/C form one connected component). Repeated packets from the same source also collapse by an automatic source token.

One connected ancestry component provides at most one evidence vote. Contradictory outcomes inside one component enter `review_shared_ancestry`. Disagreement between distinct components enters `review_disagreement`. Three consistent connected components supporting the inherited QG-061 candidate become `eligible_for_explicit_authorization`; **only** a separate explicit call makes the symbolic new authority provisional. QG-058/059/060 withdrawal history remains in the inherited record, with no deletion or direct system permissions changed.

## Public website access policies

External packets carry `policy: {robots:'allow'|'disallow'|'unknown', llms:'listed'|'unlisted'|'unknown'}`. A declared robots `disallow` blocks counting; `unknown` is quarantined. `allow` enables the synthetic packet to be considered subject to other applicable restrictions. `llms.txt` is informational discovery metadata only: being listed there does not override disallow, and absence of `llms.txt` does not automatically mean prohibited access.

The demonstration **does not fetch** the live robots.txt or llms.txt of any website, does not test legal or contractual rights, does not grant access to gated content, and does not move gated GitHub information to the public mirror. A production implementation would need live per-agent robots evaluation, authentication, terms checks, source metadata, and an export gate.

## Provenance boundaries

This graph consumes caller-supplied ancestry identifiers. It detects declared shared origins, not **undeclared hidden common ancestors**. It cannot guarantee real source independence, authenticity, freshness, or that a source was observed rather than fabricated. Consistency is checked through deterministic replay of packet fields, which is not a cryptographic append-only store.

The three-root requirement is governance within a synthetic model; it is not a statistical or scientific significance claim.

```sh
node --test tests/relearning-without-amnesia.test.mjs tests/three-surface-ancestry.test.mjs
```
