# QG-073 — Provenance Must Survive Transformation

## Invariant

**Summarizing, translating, extracting or combining source material never removes confidentiality or ancestry restrictions.** A derived node inherits the complete union of source-root ancestry and original surfaces from its parents. If any parent is gated, the output is gated.

```text
                 PINNED SOURCES
            /         |          \
       GITHUB      0ROOT.AI     INTERNET
       [GATED]      [PUBLIC]     [PUBLIC]
            \         |          /
              SUMMARY / TRANSLATE / MIX
                         |
                INHERIT ALL ANCESTORS
                         |
                 ANY GATED PARENT?
                  /             \
                YES              NO
                 |                |
          GATED DERIVATION    PUBLIC DERIVATION
                 |                |
          DENY PUBLIC EXPORT  CHECK SIGNED SCOPE
                 |                |
                 +-------+--------+
                         |
                       {{i}}
```

## Synthetic trusted-source boundary

A caller supplies a *separately pinned* registry: each source has a stable ID, source surface, confidentiality (`public` or `gated`), named upstream ancestry roots, and a SHA-256 digest of its exact source text. The independent expected SHA-256 registry digest is passed separately to every operation. The kernel validates source text against its pinned digest; source events are not allowed to create their own trust labels.

A derived node references only earlier, already verified parent nodes. The kernel calculates `classification`, `ancestors`, and `origins` directly from those parents. A forged `classification:'public'` attached to the proposed output is not trusted. Subsequent derivations inherit the same restrictions transitively. Each transformation's text digest, parent list and computed labels are deterministically replayable from the append-by-value event log.

QG-073's `authorizeTransfer` uses the **derived** labels to build its own QG-072 authorization request. Material derived from any gated input is denied public export before reaching QG-072's signed action/surface scope. Public-only derived nodes must still have an active QG-071 lease and explicit QG-072 capability.

## Boundaries and claims

- **This is modeled provenance inheritance, not live information-flow security.** The original root classification and ancestry are trusted registry inputs. A wrong or maliciously pinned registry can yield wrong labels.
- The model neither analyzes whether transformation text covertly embeds private content nor prevents an agent from using data outside its recorded parent graph. Production requires provenance-carrying handles, authenticated data labels, taint-preserving transforms, and mandatory export-gate enforcement at the actual publish/network boundary.
- No declassification protocol exists. Derived gated content cannot become public merely by changing its text or requesting permission; any future declassification must be separately authorized and audited.
- GitHub and 0root.ai remain two surfaces sharing one **owned ancestry**, but their disclosure permissions differ. Public internet is an external discovery surface subject to separate site policies and evidence provenance.
- No real sites, private repos, credentials, or network operations are accessed.

Run:
```sh
node --test tests/hive-scoped-authority.test.mjs tests/provenance-transformation.test.mjs
```
