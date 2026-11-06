# Chapter 1 — Zero
## The Origin That Is Not Empty

*QUANTA: The Wordle of Space*  
*David Lee Wise*  
*Manuscript draft 0.1 — 6 November 2026*

> A language needs somewhere to begin. It does not follow that the beginning must be empty.

### 1. Before the first mark

Imagine a sheet with no marks on it.

You may call the sheet blank. You may also say that no position has yet been selected, no distance has been measured, and no boundary has been drawn. These are not quite the same statement. The sheet still offers the *possibility* of positions, measurements, and boundaries. What is absent is a choice.

QUANTA begins with that distinction.

The first symbol is:

```text
0
```

In ordinary arithmetic, zero is a number: the additive identity. Add zero to a number and the number does not change. Zero apples means an empty count of apples. But an origin on a coordinate axis is something different. The point labeled 0 is not a claim that there is nothing at that point. It is the place from which positions are measured.

QUANTA uses **structured zero** as a proposed language concept: a designated reference state at which descriptions can begin and to which they can be compared. Its exact internal representation must be specified by the grammar. Until we have defined that representation, we do not assume zero contains physical matter, energy, hidden dimensions, or a particular number of positions.

This small act of restraint is important. A symbol should earn its meaning through a definition, and a physical claim should earn its credibility through evidence.

### 2. Three meanings of zero

We will keep three meanings separate throughout this book.

**Arithmetic zero** is the number `0`, satisfying `a + 0 = a`.

**Coordinate zero** is an origin: a reference chosen to label locations. Move the origin and the physical distance between two objects remains the same.

**QUANTA zero** is the proposed initial state in a symbolic construction. It may carry a declared schema, internal roles, or allowable transformations, but those are *features of the language*, not facts established about the vacuum of space.

We write the distinction schematically:

```text
0_num     arithmetic identity
0_origin  coordinate reference
0_Q       QUANTA initial symbolic state
```

These are names for different concepts. They are not three new physical particles.

### 3. The first distinction

Set down a point:

```text
.
```

The point is our first mark. A mathematical point has a position but no volume. The printed dot above, of course, has ink and width; it is a *drawing of* a point, not the point itself.

Place this mark relative to the chosen origin:

```text
0 ---- .
```

Now a relationship can be described. But we have not yet declared its distance. The four dashes are a typographic convenience, not four units of length.

Let the selected point have coordinate `x` on a one-dimensional axis with origin `0`. Its distance from the origin is `|x|`, assuming an ordinary Euclidean metric. If we select two coordinates `a` and `b`, the distance is `|b-a|`.

The first lesson is simple: **position requires a reference; distance requires both positions and a rule for measurement.**

### 4. From a mark to a rule

A vocabulary tells us what symbols are called. A grammar tells us what we may do with them.

Suppose we declare an operation `mark` that changes an unmarked descriptive state into one with a selected point:

```text
mark(0_Q) -> (0_Q, p)
```

Here `p` is a point identifier. The arrow means “produces a new description”; it does not yet describe physical particle creation.

Next, define a comparison:

```text
compare(p, q) -> relationship(p, q)
```

The relationship might be coincidence, separation, order, adjacency, or distance, depending on the structure we supply.

Notice what is missing: no observer is required to make the mathematical definition true. An observer may *record* the result, but a statement about two coordinates is not created by looking at them.

This is a first QUANTA discipline: do not confuse **description**, **measurement**, and **physical causation**.

### 5. The gap

Two marks invite a new question:

```text
.               .
```

What lies between them?

In an ordinary geometric model, there may be continuously many points between two distinct positions. On a discrete lattice, there may be a finite number of allowed positions. In a graph, two nodes may be adjacent even if we have assigned no spatial distance at all.

So the *gap* must be defined relative to the model.

We provisionally write:

```text
gap(p, q | M)
```

Read this as “the gap between points `p` and `q` under model `M`.” The vertical bar means “given” here; it is **not yet** the QUANTA boundary operator.

A gap may be a measured distance, a count of intervening lattice steps, a missing edge, or a topological separation. Naming the model prevents one attractive picture from being mistaken for a universal law.

### 6. The first boundary

Now draw a boundary:

```text
| . |
```

The vertical strokes suggest enclosure along one axis. They do not, by themselves, produce a three-dimensional box.

We propose the provisional QUANTA vocabulary:

```text
0     designated initial state / origin
.     position marker
|     boundary marker
[ ]   box or retention notation
( )   loop or toroidal notation
{ }   generative or transformation scope
```

This is a *reading guide*, not yet the formal syntax specification. In later chapters each operator will receive a precise domain, legal constructions, and transformation rules.

For now, the lesson is that a boundary divides a description into regions or classes. It does not automatically imply an impermeable physical wall.

### 7. Why zero can be structured without being a substance

Consider a chessboard before the first move. No piece has moved, but the initial position already has structure: squares, pieces, permitted actions, and constraints. The state is not empty merely because no move has occurred.

Consider a computer program before its first instruction. It may have an entry state, variables, and rules. The entry state can be rich in structure, yet nothing has been executed.

QUANTA's structured zero is closer to these examples than to the claim that the physical universe arose from literal nothing.

We can represent the initial descriptive state as a tuple:

```text
0_Q := (alphabet, grammar, reference, state)
```

This is a **proposed pedagogical model** for Chapter 1, not a declaration that these four fields are the final canonical kernel. If the repository later fixes a more specific zero schema, we will replace the placeholder with its exact version and retain the older definition in the revision history.

The crucial distinction is between **potential operations specified by a language** and **actual events in nature**.

### 8. A miniature experiment

We can test whether our introductory definitions are coherent without testing cosmology.

Take two positions on a line: `a = 2` and `b = 7`.

Their separation is:

```text
d(a,b) = |7 - 2| = 5
```

Change the chosen coordinate origin by shifting both labels three units left:

```text
a' = -1
b' =  4

d(a',b') = |4 - (-1)| = 5
```

The coordinates change; the separation does not.

This is an **invariant**: a property preserved under a declared transformation. A language that aims to describe space should tell us what changes and what remains unchanged.

Our first demonstrable invariant is therefore:

```text
For any real a, b, t:

|(b+t) - (a+t)| = |b-a|
```

This identity is established elementary mathematics. It is not evidence that QUANTA has discovered new physics. It is an example of the standard QUANTA should require from every future claim: an explicit rule, a test, and a preserved quantity.

### 9. Wordle of Space — Puzzle 001

**Clue:** Two points are five units apart. The origin is moved. Has the distance changed?

**Answer:** Not if the move only relabels coordinates by a common translation and the metric stays the same.

**Try it:** Choose any two numbers, add the same third number to both, and calculate their difference.

**Challenge:** Would the answer remain true if you changed the *measurement rule* instead of moving the origin? Explain the difference.

**What this teaches:** A symbol is not its referent; an origin is not a substance; and a coordinate transformation is not necessarily a physical change.

### 10. The first QUANTA invariant

We can now state the first rule of the manuscript:

> **Q0 — Reference Preservation.** A transformation that merely changes the description's reference frame must not be presented as a change in an underlying geometric relationship unless the relation's definition also changes.

This is a design requirement for the proposed language. It will have to be refined when we introduce rotations, non-Euclidean geometry, time coordinates, and dynamical fields.

Zero is therefore not a conclusion. It is a promise to be precise about where we begin.

We have selected an origin. We have placed a mark. We have measured a gap. We have learned that some changes alter labels while preserving relationships.

Next, we will give the point an explicit identity.

*End of Chapter 1 — Next: Chapter 2, The Dot.*

---

### Chapter 1 technical ledger

| ID | Statement | Status |
|---|---|---|
| M-001 | `a + 0 = a` | Established mathematics |
| M-002 | `|(b+t)-(a+t)| = |b-a|` | Proven algebraic identity |
| Q-001 | `0_Q` denotes QUANTA's starting symbolic state | Proposed language definition |
| Q-002 | `0_Q := (alphabet, grammar, reference, state)` | Provisional chapter schema; requires canonical reconciliation |
| Q-003 | `Q0` reference preservation | Proposed grammar design rule |
| P-001 | QUANTA structures correspond directly to physical vacuum microstructure | Not established or claimed here |

**Editorial note:** An exact numbered-position zero kernel has not been verified from the repository's currently accessible README; no numerical size or physical dimension is assigned to it in this chapter.
