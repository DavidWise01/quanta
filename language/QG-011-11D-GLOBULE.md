# QG-011 — QUANTA 11D Globule / Hypercube Substrate

**Status:** Proposed QUANTA notation over established hypercube mathematics. **Not** a validated physical string, M-theory compactification, or measured globule.

## Two layers, never conflated

### Surface signature — a dimension index

The teaching signature for level \(n\) is \(S_n = "." + "|."\) repeated \(n-1\) times.

- \(S_1 = .\)
- \(S_2 = .|.\)
- \(S_3 = .|.|.\)
- \(S_4 = .|.|.|.\)
- \(S_5 = .|.|.|.|.\)
- \(S_{11} = .|.|.|.|.|.|.|.|.|.|.\)

There are \(n\) dots and \(n-1\) bars. The signature is an **ordinal index / visualization convention**. It is a path with \(n\) vertices and \(n-1\) edges, **not** the 11D hypercube itself. In this layer \(\text{dots} - \text{bars} = 1\).

### Substrate — an actual n-dimensional hypercube

Define \(H_0\) as one vertex. Define \(H_1 = K_2\), two vertices joined by one edge. To obtain another independent axis:

\[
H_{n+1} = H_n \\square K_2
\]

Here \(\square\) is the Cartesian graph product. The new object consists of two disjoint copies of \(H_n\), plus one matching edge between corresponding vertices in the two copies.

**Address:** each vertex has an \(n\)-bit coordinate \(v\in\{0,1\}^n\).

**Edge:** vertices \(u\) and \(v\) are adjacent iff they differ in **exactly one** coordinate (Hamming distance 1).

**Face:** choose two coordinates to vary and fix the other \(n-2\); the resulting four vertices form a square.

For \(0\le k\le n\), the number of \(k\)-dimensional cubical faces is \(f_k(n)=\binom{n}{k}2^{n-k}\). Thus:

\[
V_n = 2^n,\qquad E_n = n2^{n-1},\qquad F_n = \binom{n}{2}2^{n-2}
\]

(The square-face formula is for \(n\ge2\).) At \(n=11\):

- **2,048 vertices**
- **11,264 edges**
- **28,160 square 2-faces**
- **22 boundary 10-dimensional facets**
- **11 incident edges at every vertex** (an 11-regular graph).

A 2D screen can show only a **projection** of these vertices and edges. Different original vertices may overlap on screen, and crossings on screen do not create new graph vertices.

## Dimension table

| n | Name | Surface signature dots | Actual vertices | Actual edges | Square faces |
|---:|---|---:|---:|---:|---:|
| 1 | segment | 1 | 2 | 1 | 0 |
| 2 | square | 2 | 4 | 4 | 1 |
| 3 | cube | 3 | 8 | 12 | 6 |
| 4 | tesseract | 4 | 16 | 32 | 24 |
| 5 | 5-cube / penteract | 5 | 32 | 80 | 80 |
| 6 | 6-cube | 6 | 64 | 192 | 240 |
| 7 | 7-cube | 7 | 128 | 448 | 672 |
| 8 | 8-cube | 8 | 256 | 1,024 | 1,792 |
| 9 | 9-cube | 9 | 512 | 2,304 | 4,608 |
| 10 | 10-cube | 10 | 1,024 | 5,120 | 11,520 |
| 11 | 11-cube | 11 | 2,048 | 11,264 | 28,160 |

## QUANTA globule design, provisional

The **globule** is a *hypothetical container around the abstract graph*, not another geometric property of the hypercube and not a particle. It can be represented as a conceptual envelope \(G(H_{11})\), with three explicit layers:

1. **Addresses**: all 11-bit vertices; no duplicates.
2. **Incidence**: all edges differing by one bit; no invented connections.
3. **Observer projection**: a declared map \(P:\{0,1\}^{11}\to\mathbb R^2\) for visualization. Its display is not lossless or evidence of physical dimensions.

If a string or brane analogy is added, it should be labeled a **separate physical hypothesis** with a defined metric, dynamics, compactification, and test.

## M-theory distinction

Most perturbative superstring theories use **10 spacetime dimensions** (typically 9 space + 1 time). M-theory is associated with **11 spacetime dimensions** (10 space + 1 time). The dimension in \(H_{11}\) above counts **11 graph-coordinate axes**; it is not automatically the same as 11 physical spacetime dimensions.

## Exact validation gates

1. Enumerate every address \(v\in[0,2^{11})\).
2. For each address and each bit position \(j\in[0,11)\), form neighbor \(v\oplus 2^j\).
3. Retain each undirected edge once using \(v< (v\oplus 2^j)\).
4. Assert 2,048 distinct vertices, 11,264 distinct edges, and degree 11 at every vertex.
5. For every two distinct axes, enumerate 512 choices of remaining coordinates; assert 28,160 unique square faces.
6. Rotate only the **projection**, without mutating addresses or incidence.
7. Keep the surface signature separate from these counts.

## References

- [Wolfram MathWorld — Hypercube Graph](https://mathworld.wolfram.com/HypercubeGraph.html)
- [Wolfram MathWorld — Hypercube](https://mathworld.wolfram.com/Hypercube.html)
- [Hammack — Hypercubes (cubical face formula)](https://richardhammack.github.io/reprints/Bridges2024.pdf)
- [Oxford — M-theory and gauge-gravity duality, eleven dimensions](https://academic.oup.com/book/60809/chapter/529007810)
