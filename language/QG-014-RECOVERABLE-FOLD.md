# QG-014 — Recoverable Chrome Dot: One Visible Bit, Full Lineage

**Design boundary:** `128 → 64 → 32 → 16 | 8 → 4 → 2 → 1 | 1`.

The user-defined four-number groups are preserved; the terminal `1 → 1` is a fixed-point observation.

## The key fact

A lone bit cannot losslessly encode arbitrary 128-bit input. **The Chrome Dot is only the visible terminal bit.** A separate **127-bit witness** makes the transformation reversible. Without this witness, the apparent fold is information-losing.

## Exactly reversible fold rule

For an adjacent pair of bits `(left,right)`:

```text
parent  = left XOR right
witness = right
```

To unfold:

```text
left  = parent XOR witness
right = witness
```

Each stage halves the visible width while storing the right bit from each pair. The witness sizes across the seven reduction steps are:

```text
128 → 64   witness 64
 64 → 32   witness 32
 32 → 16   witness 16
 16 →  8   witness  8
  8 →  4   witness  4
  4 →  2   witness  2
  2 →  1   witness  1
  1 →  1   witness  0 (no change)
                  ----
                   127 retained bits
```

The final Chrome Dot is the parity bit (XOR of all 128 input bits); it is *not* a cryptographic hash or an encryption key. The information is represented as `1 terminal bit + 127 witness bits = 128 bits`. There is no magical compression.

## Layer boundaries

- **QG-012** pairs eight source *identities*, preserving their provenance in a lineage tree.
- **QG-013** permutes addresses in a downward spiral and protects transported bytes through a conventional authenticated encryption envelope.
- **QG-014** folds *a 128-bit data word* into one visible bit plus a witness tape. This is a lossless reversible encoding if the complete witness is available.
- The unencrypted witness tape is not authenticated. Use QG-013 AES-GCM or an independently verified cryptographic integrity mechanism for protection.

## Portable transport

The portable frame is a terminal bit and seven ordered witness segments of lengths `[64,32,16,8,4,2,1]`. It omits the redundant visible intermediate stages. On receipt, run the inverse mapping to reproduce all 128 original bits exactly; recompute each stage; and verify the fixed-point final step.

**Tampering caveat:** A changed terminal bit and properly shaped witness could produce a *different* valid 128-bit message. Invertibility is not authentication. Integrity requires a trusted reference or authenticated encryption.

## Validation gates

1. Widths are exactly `[128,64,32,16,8,4,2,1,1]`.
2. Chunks are `[128,64,32,16]`, `[8,4,2,1]`, and stable terminal `[1]`.
3. The seven witness slices total exactly 127 bits.
4. The terminal fold is `1 → 1` with unchanged identity and no newly generated witness.
5. Source identities and intermediate outputs remain traceable in an immutable execution record.
6. Exporting and importing a portable witness frame reproduces every source bit.
7. Changed or missing witness lengths are rejected; full integrity is only assured by an external authenticated layer.

**Formalization status:** This is a computational scheme using standard XOR algebra. It is not a physical demonstration of a quantum dot, string-theory compactification, or a new encryption algorithm.
