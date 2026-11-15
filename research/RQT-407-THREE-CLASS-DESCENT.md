# RQT-407 — The Three-Class Integer Descent

Date: 2026-11-15. Canonical source: RQT-401 full reduced Gram.
The source itself is conditional on the RQT-386 candidate's
unverified compatibility with the frozen 17-predecessor sequence.

## Exact new computation

Q has all even coefficients. Let A=Q/2. Solving the original exact
equation Q(v)=-2 is equivalent over integers to A(v)=-1.

For powers of two from 2 through 256, all solutions modulo each power
were enumerated by exact coordinatewise lifting. The algorithm
projects surviving triples (x,y,z) to their possible (x,y) residues.

| modulus | surviving triples | projected xy pairs |
|---:|---:|---:|
| 2 | 4 | 4 |
| 4 | 24 | 12 |
| 8 | 96 | 40 |
| 16 | 384 | 96 |
| 32 | 1536 | 320 |
| 64 | 6144 | 1024 |
| 128 | 24576 | 3840 |
| 256 | 98304 | 14336 |

At modulus 256, 14336 of the 65536 possible xy residue pairs
can admit some z. The excluded fraction is 51200/65536=78.125%.

At modulus 4 and higher, survivors belong only to parity types
001,011,110 as certified in RQT-406, equally divided among
the three families at modulus 256.

## What this proves

For an actual integer root v, reducing (x,y) modulo 256 must land
inside this exact finite projection. Every excluded xy residue
pair is globally impossible at ANY coordinate magnitude.
However, passing the finite projection is not evidence of an
actual integer solution: the exact full norm, real cone, and
integer third-coordinate conditions remain mandatory.

This is a finite local *sieve*, not an infinite-descent argument.
Do not mistake the conceptual JPG art for an accurate quadratic
coefficient display: the authoritative coefficients are in Q.

## Next constructive move

Compute the periodic allowable xy mask, intersect with the global
RQT-394 rational slope corridor, and use a rigorous global
representation algorithm instead of simply scanning larger boxes.

Root19 OPEN, root20 OPEN, root21 conditional. ASCII always;
a new generated JPG is available separately in the conversation.
