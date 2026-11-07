# Chapter 25 — The Boundary Again
## Where a True Rule Stops Being True

*QUANTA: The Wordle of Space*  
*David Lee Wise*  
*Reader-first manuscript draft 0.1 — 7 November 2026*

> A boundary is not the enemy of a discovery. It tells us where the discovery belongs.

### 1. The line around the garden

The child walks behind the house, past the stream and the two paths, carrying the familiar notebook.

A small garden lies beside the wall.

Someone has placed stones around its edge.

The stones do not tell the plants how to grow. They tell the traveler where the garden begins and where a footstep might crush a seedling.

The child remembers the boundary from Chapter 4.

```text
|
```

At first, the bar separated one side from another.

Later, it helped form a path.

Now the child discovers a quieter use.

**A boundary can tell us where a statement remains dependable.**

### 2. The promise from yesterday

The notebook opens to the invariant from Chapter 24:

```text
.|.           2 dots, 1 bar
.|.|.         3 dots, 2 bars
.|.|.|.       4 dots, 3 bars
.|.|.|.|.     5 dots, 4 bars
```

Each string begins with a dot, alternates bars and dots, and ends with a dot.

For these strings:

```text
dots - bars = 1
```

If we append `|.`, the alternating structure survives.

One more dot.

One more bar.

The difference remains one.

But the child asks a new question:

**How far can that promise travel before it no longer applies?**

### 3. The first step outside

Start with our familiar wall-trace:

```text
.|.|.|.|.
```

Append the allowed pair:

```text
.|.|.|.|.|.
```

Still valid.

Now append only a dot:

```text
.|.|.|.|..
```

The new string has two neighboring dots at the end.

We did not find a mysterious exception to the original rule.

We used a different operation.

The promise never covered it.

```text
ALLOW    append |.
OTHER    append .
```

The distinction is important enough to deserve a line of its own:

**A rule has not failed when we ask it to govern something it never claimed to govern.**

The broader claim—that every appended symbol preserves alternation—*does* fail.

Our counterexample belongs to that broader claim.

### 4. The number that fools us

The child notices another trap.

Consider:

```text
..|
```

Two dots. One bar.

The count difference is one.

But the sequence starts with two dots beside each other and ends with a bar.

The number is right.

The structure is wrong.

Now consider:

```text
.|.|.       valid
..||.       not valid
```

Both contain three dots and two bars.

Yet only the first belongs to the chapter's alternating language.

This is a beautiful warning.

A property can be preserved without containing the whole identity of a structure.

The count difference is **necessary** for our grammar, but not **sufficient** to recognize it among arbitrary strings.

A trustworthy reader must inspect both the count and the order.

### 5. The little gate

Imagine placing a gate at the edge of the garden.

```text
IN DOMAIN  |  OUTSIDE DOMAIN
```

On one side: the inputs for which a rule has been established.

On the other: inputs the rule has not yet covered.

The gate is not a wall against curiosity.

It is a sign:

*Cross with another test.*

Suppose our string has already become invalid:

```text
.|..
```

If we now append the familiar `|.`, what happens?

```text
.|..|.
```

It remains invalid.

The earlier doubled dot did not magically disappear.

Our invariant says:

*If the starting string is valid, the declared extension preserves validity.*

It does not say:

*The extension repairs every invalid input.*

That difference—between preservation and repair—is a boundary worth remembering.

### 6. The wall answers differently

The child returns to the room with the lamp.

A square card hangs before the wall.

When the card turns under a fixed arrangement, its shadow width can change.

Yesterday, we asked what remained invariant in a well-defined model.

Today, we ask where that model's assumptions stop holding.

What if the lamp moves?

What if the card bends?

What if a second light casts another shadow?

The observations may differ from what the simple model predicts.

That does not instantly disprove the mathematics of the original idealization.

It shows that a different situation requires a different account.

We should record the departure.

Then test the changed conditions.

The one-box story is now mature enough to let its own assumptions be visible.

### 7. The tesseract stays honest

Our recurring motif is still here:

```text
[ .|.|.|.|. ]
```

It is the wall-trace inside one box.

And our story has imagined that trace as a shadow of a richer form—a tesseract glimpsed through a lower-dimensional view.

But a metaphor is not a projection map.

To turn it into a formal model, we would need to specify the four-dimensional coordinates, the projection rule, and the method that converts the result into a particular pattern of marks.

Without those, we can explore the picture as language.

We cannot claim that every five-dot trace corresponds to a physical tesseract.

We have found a boundary between **what the symbols prove** and **what they invite us to imagine**.

And that boundary makes both sides more useful.

### 8. Three labels for the notebook

The child draws three headings:

```text
PROVED       holds under the declared rules
DISPROVED    a valid counterexample was found
UNTESTED     the relevant test has not been done
```

Some claims may be undecided rather than easily falling into any of these boxes, but this first notebook makes one distinction particularly clear.

**Untested does not mean false.**

And **not yet disproved does not mean true**.

A proof is a reason.

A counterexample is a reason.

An empty page is neither.

This matters when an agent, a program, or a person is asked to make decisions from incomplete records.

If we can say “outside the tested domain,” we can preserve the uncertainty without hiding it.

### 9. Wordle of Space — Puzzle 025

The rule says:

*For a valid alternating dot-and-bar string, appending `|.` preserves validity.*

Which statement is correct?

A. Appending `|.` will repair every invalid string.

B. Appending `|.` to a valid string preserves its alternating grammar.

C. Every string with one more dot than bars is valid.

**Answer: B.**

The guarantee depends on the input belonging to the declared domain.

Now try a harder puzzle:

```text
input:  .|..
action: append |.
output: .|..|.
```

Why is this *not* a counterexample to our actual invariant?

Because the starting input was already invalid.

The input lies outside the domain in which the guarantee was proved.

**Try it:** Create one valid string, one invalid string with the correct counts, and one invalid string with incorrect counts. Apply the same extension to each. Record what the original rule actually promises.

### 10. The twenty-sixth QUANTA rule

The child walks once more to the garden wall.

The stones are still there.

Inside them, something grows.

Outside them, the world continues.

The boundary was never meant to end discovery.

It shows us where to begin the next careful question.

> **Q24 — A Claim Must Carry Its Boundary.** A QUANTA claim must preserve the domain, assumptions, and conditions under which its evidence or proof applies. Out-of-domain inputs are marked as untested or separately evaluated, not silently counted as confirmation or refutation of the scoped claim.

The child opens the notebook to its oldest pages.

Zero.

A dot.

A gap.

A boundary.

The same mark has returned, but its meaning has deepened.

```text
[ .|.|.|.|. ]
```

One box.

A visible trace.

A rule that preserves something.

And a boundary showing exactly how far the rule has earned our trust.

**A good boundary does not make the universe smaller. It makes our knowledge more precise.**

*End of Chapter 25 — Next: Chapter 26, The Repetition.*

---

### Optional technical note

For the introductory language `L = { "." + "|." repeated n times : n ≥ 1 }`, define `T(s) = s + "|."`. The statement `s ∈ L ⇒ T(s) ∈ L` is proved. Its converse is not required, and the implication does not promise that `T` repairs arbitrary strings. The necessary count relation `#dots − #bars = 1` is not sufficient for membership in `L`. Model assumptions and grammar domains must be recorded separately from speculative physical interpretations.

### Chapter 25 technical ledger

| ID | Statement | Status |
|---|---|---|
| M-050 | An implication with a restricted domain does not assert its conclusion for arbitrary inputs | Established logic |
| M-051 | A necessary condition need not be sufficient | Established mathematics |
| Q-050 | A QUANTA invariant record carries domain, assumptions, and allowed transformations | Proposed record architecture |
| Q-051 | Out-of-domain cases are recorded separately rather than misclassified | Proposed evaluation practice |
| Q24 | A Claim Must Carry Its Boundary | Proposed language design rule |
| P-025 | The alternating-string rule establishes an unrestricted law of physical projection | Not established |
