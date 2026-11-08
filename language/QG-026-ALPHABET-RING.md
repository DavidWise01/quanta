# QG-026 — Alphabet on the Sixty Ring

**Carrier:** `||||`.

QG-025 established 60 exact stations with 4 quads of 15 stations. QG-026 connects this to the **entire A–Z vector alphabet, semantic glyph identities, and somatic drawing verbs** implemented in QG-016.

## The exact vertex map
The canonical uppercase glyph font uses coordinates `(x,y)` in the inclusive integer square `0..4 × 0..4`. Assign each vertex a unique home address:

```text
home(x,y) = 2 * (5*y + x)
home addresses = 0,2,4,6,...,48   (25 distinct stations)
ring(x,y,q) = (home(x,y) + 15*q) mod 60
q ∈ {0,1,2,3} = a,b,c,d
phase degrees = 90*q
```

All 25 canonical source vertices have unique home stations, and the map can be inverted exactly. A quarter-turn moves a vertex's active station forward by 15. Four turns restore the same station. **This shifts the glyph's transport phase around the ring; it does not claim that the 5×5 glyph itself undergoes a rigid 2D rotation.**

## Three simultaneous channels
- **Geometry**: every stroke and vertex is explicitly carried, including the distinct diagonal tail of `Q`.
- **Semantics**: immutable uppercase letter identity and an optional caller-provided meaning. No autonomous interpretation of a letter's meaning.
- **Somatics**: original QG-016 stroke verbs `PEN_UP`, `MOVE`, `DRAW`, and `TURN`, retaining chronological stroke indices and ring-addressed `from`, `to`, and `at` positions where applicable.

A word/phrase is a succession of tokens `||A||` ... `||Z||`, each letter advancing `a→b→c→d→a`, with spaces preserved exactly and resetting to `a`. Maximum supported length is 128 uppercase characters or spaces. This QG-026 text protocol is a deterministic bridge to the QUANTA alphabet/word carriers, not a full natural-language serializer.

## Example
```text
|||| ||Q|| [a] : source vertex (4,4) -> home 48 -> station 48
     ||Q|| [b] : source vertex (4,4) -> home 48 -> station 03
     ||Q|| [c] : source vertex (4,4) -> home 48 -> station 18
     ||Q|| [d] : source vertex (4,4) -> home 48 -> station 33
four 90° turns return station 48
||||
```

**Capacity note**: 60 station addresses don't, by themselves, compress an arbitrary alphabet, message, or somatic action sequence. The packet retains canonical letter identity and full geometric/somatic witnesses. The ring is an addressable phase display; stations can be reused for different verbs and letters.

## Test boundaries
1. All 25 source vertices have distinct, exactly invertible station addresses.
2. Four +15 steps return every vertex to its source station.
3. Every uppercase A–Z glyph reconstructs at all four quads.
4. `Q` tail and ordered somatic verb locations survive each quarter turn.
5. Text order, exact spaces, and word-level phase cycling reconstruct.
6. Changed phase, vertex and somatic witness values are detected.
7. Unsupported characters and invalid 5×5 coordinates are refused.

## Artifacts
- [Executable alphabet-ring kernel](./alphabet-ring.mjs)
- [Seven regression tests](../tests/alphabet-ring.test.mjs)
- [Interactive ring language lab](../ring-language.html)