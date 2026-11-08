# QG-013 — Downward Spiral: QUANTA Transport and Encrypted Envelope

**Canonical proposed signature (preserved verbatim):** `12|8/64/3|2/16/8|/4/2/1/1`

**Status:** A newly defined software protocol built on a reversible address permutation and standard authenticated encryption. The author's clarified meaning is a descending **bit-width ladder in four-number chunks**: `128, 64, 32, 16 | 8, 4, 2, 1 | 1`. The raw compact spelling is retained as a legacy source signature. The four-number chunks are contiguous groups of four widths; the last solitary `1` is a terminal stability check, not an additional four-value group. The routing algorithm below is a separate implementation choice.

## Three things are separate

1. **Language:** `.` represents a vertex/endpoint, `|` represents an edge in the surface grammar, and `\\.|./` is a fold instruction. The original surface line by itself cannot encode all hypercube incidence.
2. **Transport:** A dimension-addressed, deterministic, invertible **permutation** of vertex identifiers. It is not encryption. The visual spiral is the traversal order.
3. **Encryption:** A separate standards-based **AES-256-GCM** authenticated encryption layer with a fresh 96-bit nonce, random 128-bit salt, and password-derived key via PBKDF2-HMAC-SHA-256 (250,000 iterations) in the browser's Web Crypto API. In production use, a reviewed key-management design and threat model are still required. No security guarantee is supplied by the spiral or Chrome Dot.

## Dimension-to-globule construction (3 through 11 dimensions)

For dimension `d`, `3 <= d <= 11`:

- The substrate has exactly `2^d` vertex addresses `0..(2^d-1)`.
- Produce a full Gray-code address traversal: `g(i) = i XOR (i >> 1)`, for `i = 0..2^d - 1`. Neighboring addresses change by one bit.
- Partition into `2^(d-3)` **globules of eight addresses each**. Globule `g` owns Gray indices `8g..8g+7`; there are no repeated or missing vertex addresses.
- Build a rectangular grid with `width = 2^ceil((d-3)/2)`, `height = 2^floor((d-3)/2)`. Visit each grid cell once via a **clockwise, outer-to-inner** rectangular spiral.
- Associate each spiral visit with its underlying row-major globule index. Transmit that globule's eight addresses in their Gray-code order.
- Each globule's **Chrome Dot** may fold `8 → 4 → 2 → 1 → 1`, retaining the eight distinct source addresses as a lineage tree. This is aggregation and never changes the original graph.

The route is invertible because it is a permutation of the underlying vertex IDs: decoding uses the inverse positions, not the terminal Chrome Dot alone.

For `d=11`, there are 2,048 addresses, 256 globules of eight, a 16×16 spiral grid, and a fixed-point representative for each globule. The abstract 11-cube continues to have **11,264 edges**. This does not imply an 11-dimensional physical object has been transported.

## Canonical bit-width ladder — clarified by the author

```text
128 | 64 | 32 | 16       chunk A — four widths
  8 |  4 |  2 |  1       chunk B — four widths
                       1 terminal fixed-point check
```

**Invariant:** `128 → 64 → 32 → 16 → 8 → 4 → 2 → 1 → 1`. Each nonterminal stage halves the previous width; the final stage leaves `1` unchanged. A four-number chunk is **four stage values**, not four bits (a nibble), and neither chunk is an independent AES key size. The native signature `12|8/64/3|2/16/8|/4/2/1/1` remains in the header for continuity; the normalized array is authoritative for this proposed language version.

This is a **width schedule**: it describes how many bits or positions a fold stage can be assigned in a future codec. The existing implementation's `gray8-outer-spiral-v1` route and AES-256-GCM envelope remain independent. Halving a displayed width is not automatically a reversible payload compressor; full information recovery requires the preserved source and an invertible permutation/encryption layer.

## Transport envelope

```json
{
  "version": "QG-013.1",
  "header": {
    "dimensions": 11,
    "signature": "12|8/64/3|2/16/8|/4/2/1/1",
    "algorithm": "AES-256-GCM",
    "kdf": "PBKDF2-HMAC-SHA-256",
    "iterations": 250000,
    "route": "gray8-outer-spiral-v1"
  },
  "salt": "<base64url; fresh 16 random bytes>",
  "nonce": "<base64url; fresh 12 random bytes>",
  "ciphertext": "<base64url; includes 16-byte GCM tag>"
}
```

The envelope header is bound as AES-GCM **additional authenticated data (AAD)**, so changing the signature, dimension, iteration count, or route invalidates decryption. The plaintext is UTF-8 and can contain textual JSON or Unicode text. Before AES-GCM encryption, each \`2^d\`-byte block is **actually permuted through the spiral route**, with zero padding for the final short block. A four-byte little-endian original byte length is included **inside the authenticated ciphertext**. On decryption the route is inverted, padding is checked, and the exact original UTF-8 sequence is restored. The output size reveals an approximate padded block count, and the route itself is public; it is never a substitute for cryptography.

## Validation gates

1. For every `d=3..11`, exactly `2^d` distinct addresses are visited.
2. Every adjacent pair in each Gray-code globule differs by exactly one bit.
3. Every address decodes to precisely its original position.
4. Each globule contains eight unique vertex addresses; its Chrome Dot retains all eight in its lineage.
5. At 11D, exactly **256 globules** occupy the full **16×16** grid without cell duplicates.
6. Crypto encrypt/decrypt round-trip preserves Unicode plaintext, including empty, short and multiple-block inputs; the encrypted cleartext frame contains its inverse-recoverable spiral permutation.
7. Wrong password, altered authenticated header, or modified ciphertext fails decryption.
8. Fresh salt and nonce are generated by a cryptographically secure random source; the same password and message should produce different serialized envelopes.
9. The normalized bit-width sequence is `128,64,32,16,8,4,2,1,1`; the two complete chunks each contain four entries, and the last `1` is an unchanged terminal state.

## Model boundary

*String theory* and *M-theory* discuss spacetime models requiring metrics, dynamics, fields and physical evidence. Here, 11 denotes the number of mathematical hypercube axes and a maximum supported address dimension in a software routing prototype. The term *globule* labels a grouping of eight source IDs and their fold lineage, not a verified fundamental particle, geometry of spacetime, or physical transport mechanism.
