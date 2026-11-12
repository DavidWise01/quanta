# QG-072 — Authority Must Have Scope

## Natural invariant

**Possessing a valid lease does not imply having permission to perform every action, or on every information surface.** QG-071 grants finite temporal authority. QG-072 introduces an explicit, issuer-signed action/surface capability matrix tied cryptographically to the particular active QG-071 lease, agent identity, checkpoint digest and revocation floor.

```text
              QG-071 LEASE VERIFIED
                        |
                ISSUER-SIGNED SCOPE
                        |
                REQUESTED ACTION?
                        |
             +----------+----------+
             |          |          |
           GITHUB    0ROOT.AI   PUBLIC INTERNET
           GATED      PUBLIC      EXTERNAL
             |          |          |
             +----------+----------+
                        |
               SOURCE CLASSIFICATION
                        |
                PERMISSION PRESENT?
               /                \
              YES               NO / EXPORT
               |                    |
              ALLOW                DENY
               |                    |
               +---------+----------+
                         |
                       {{i}}
```

## Signed grant

The capability grant has schema `QUANTA-QG-072-SCOPE`, binds the SHA-256 digest and sequence of the QG-071 signed lease, the agent identity, checkpoint digest, revocation floor and a finite explicit rule list. Ed25519 validation is performed using the **existing independently pinned QG-071 issuer key**, not a key supplied by the capability request. The grant is verified on every decision, including after lease expiry. A valid signature cannot revive an expired lease.

The action vocabulary is `observe`, `learn`, `publish`, `modify`. The three discovery surfaces remain `github`, `0root.ai`, `public-internet`. A request must carry its action, destination surface, original surface and information classification (`public` or `gated`). Matching action/surface pairs are admitted only while the lease is active and an issuer signature verifies. Unmatched pairs are denied; attempting to add or alter a signed grant invalidates the signature. Separate value-appended decision records retain both allowed and denied cases for deterministic replay.

For this finite model, external public internet is **discovery-only**: publishing and modifying external sites are never granted. Gated GitHub information is confined to GitHub, including when a request otherwise matches an allowed action on 0root.ai. This denies public mirroring of gated material by default. The two owned surfaces continue to share a source ancestry for witness counting, but they remain **different access-control boundaries**.

## Limitations

- The `classification` and `originSurface` fields are caller-declared. This model checks them; it **does not prove** them. A real system must attach and propagate authenticated information-flow labels through summaries, derived reports, and agent packets, rather than accepting untrusted self-classification.
- This prototype makes deterministic policy decisions only. It does not operate GitHub, 0root.ai, websites or credentials, grant platform permissions, enforce a live network perimeter, or independently verify robots/llms policy.
- Key custody, trusted logical time, durable spent-challenge state, signed revocation floors and real issuer authorization remain external requirements inherited from QG-062–071.
- A signed `publish @ 0root.ai` capability on its own is not permission to disclose gated source content; the provenance/export gate is independent and mandatory.

Run:
```sh
node --test tests/hive-authority-lease.test.mjs tests/hive-scoped-authority.test.mjs
```
