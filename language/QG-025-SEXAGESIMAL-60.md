# QG-025 — Sexagesimal 60 Ring

**Carrier:** `||||`. **Natural boundary:** one radix-60 positional transport frame, with 60 exact stations (`0..59`) and four QUANTA quads of 15 stations each.

## History vs QUANTA design
Babylonian arithmetic used place values of powers of 60. Digits from 1 through 59 were built using repeated unit and ten signs; surviving manuscripts have complex conventions regarding empty places and the absence or later development of a placeholder. QG-025 uses **modern explicit zero digits**, as do many modern sexagesimal transcriptions. This is not a reconstruction of historical Babylonian cuneiform typography.

The Indian/Vedic mathematical tradition is distinct from Babylonian sexagesimal numeration; documented later Indian mathematical notation includes decimal place value. The 1965 book titled 'Vedic Mathematics' is a modern reconstruction rather than a proven direct transcription of Vedic sutras. Neither historical tradition is claimed as the source of the QUANTA quads.

## 60 as a useful natural boundary
- `60 = 3 × 4 × 5 = 2² × 3 × 5`.
- Divisors of 60 are `1,2,3,4,5,6,10,12,15,20,30,60`, allowing exact equal subdivision into all those sizes.
- Four quads × 15 stations = 60. A **90° phase shift corresponds exactly to +15 modulo 60**.
- Quad `a` = 0–14; `b` = 15–29; `c` = 30–44; `d` = 45–59.
- Station `n` has angle `6n` degrees and quad/local address `(floor(n/15), n mod 15)`.
- Rotating four 90° quarter turns returns to exactly the original station.

## Integer transport
Unsigned decimal integer `N` is encoded as canonical sexagesimal digits by repeated division by 60, with digits in `0..59`. Reversing the digit polynomial reconstructs N exactly: `N = sum(d_i × 60^i)` for least-significant-position indexing.

Examples: `59 → [59]`, `60 → [1,0]`, `3600 → [1,0,0]`, `3835 → [1,3,55]`.

The packet carries the explicit decimal source, sexagesimal digits, station locations and all four 90° phase views as verifiable witnesses. BigInt preserves arbitrary integer precision within the implemented 256-digit decoder bound. Neither this representation nor rotating station positions encrypts or compresses data.

## Test targets
1. Exactly 60 unique stations in four equally sized quads.
2. Full four-quarter-turn cycle returns to origin for every station.
3. All 12 integer divisors of 60 validated.
4. Exact radix conversion at digit and place-value boundaries.
5. BigInt roundtrip beyond floating-point precision.
6. Modified phase/number/source rejected via deterministic reconstruction.
7. Malformed digits and values refused.

## Sources
- [MacTutor History of Mathematics — Babylonian numerals](https://mathshistory.st-andrews.ac.uk/HistTopics/Babylonian_numerals/)
- [MacTutor — Babylonian mathematics](https://mathshistory.st-andrews.ac.uk/HistTopics/Babylonian_mathematics/)
- [Kim Plofker, Mathematics in India](https://sanskrit.uohyd.ac.in/Algorithms_in_Ancient_India/Material/Kim_Plofkar_Maths_in_India.pdf)
- [S. G. Dani, Vedic Mathematics in Perspective](https://www.math.tifr.res.in/~dani/vmissc.pdf)

## Artifacts
- [Executable kernel](./sexagesimal-ring.mjs)
- [Regression tests](../tests/sexagesimal-ring.test.mjs)
- [Interactive 60 Ring](../sixty.html)