# RQT-566 — Fourth Discriminant Break

**Exact ECM divisor and new all-order local norm certificate.** Replayed RQT-565 JSON source SHA256 `cb0b5c188b20be75d2e28289958221f7832710cd351b91da00442b1589a4397b`.

The original 293-bit discriminant cofactor has prime divisor `p=22361230963`. Exact division leaves a **259-bit** cofactor, not certified prime. First configured ECM batch B1=6000/B2=60000, 12 curves, seed=56601 discovered divisor in 0.218 sec. SymPy's deterministic isprime check applies to this <2^64 number.

| Exact check | Value |
|---|---:|
| Prime | 22361230963 |
| v_p(Delta) | 1 |
| K mod p | 2379782987 |
| K²−4 mod p | 17464168712 |
| C mod p | 16478607289 |
| Legendre(delta/p) | −1 |
| Relative extension | unramified quadratic |
| Local relative norm | PASS |

This negative Legendre value does NOT obstruct the norm: the target C is a unit, so its inverse is a norm from the unramified quadratic local extension at all orders. The other planned ECM batches were not executed after the early hit.

**Not proved:** 259-bit cofactor primality, complete discriminant factorization, global relative norm, rational Wall isometry, integral GL4 equivalence, root19, or full21 reflection product. No new root19 exclusion. Historical conditional ledger remains 647 excluded/73 unresolved of 720 selected corridors.

A complete local Python script, results.json, research Markdown, conceptual underwater neon JPEG and self-contained illustrated HTML are attached in this conversation. GitHub HTML is text only. Some tiny labels in conceptual image are not numerical evidence. GitHub Pages and binary image publishing unverified.

**Next RQT-567:** factor 259-bit cofactor with exact divisibility and field-local gates.
