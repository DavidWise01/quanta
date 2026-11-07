# Chapter 10 — The Code
## When a Language Learns to Read Itself

*QUANTA: The Wordle of Space*  
*David Lee Wise*  
*Reader-first manuscript draft 0.1 — 6 November 2026*

> A mark becomes a letter when we agree how to read it. A language begins when the letters know how to belong together.

### 1. The note on the door

Imagine finding a note on your front door.

It contains only three marks:

```text
[ . ]
```

You smile. You remember the cup that held water, the pebble inside the box, and the first lessons of QUANTA.

But what does the note *say*?

Perhaps it means “something is here.”

Perhaps it means “keep this safe.”

Perhaps it means nothing more than the drawing of a dot between two brackets.

The shapes alone cannot decide.

Whoever wrote the note must share a reading rule with whoever receives it.

And if the note is going to be read by a machine, the rule must become precise enough for a machine to follow.

That is our next discovery:

**The code is not hidden behind the marks. The code is the agreement that gives the marks an orderly reading.**

### 2. An alphabet is not yet a sentence

Here are some of our marks:

```text
0    .    |    [ ]    ( )    { }
```

We have met them one by one. They have given us a beginning, a point, a boundary, a container, a returning path, and a scope of possibility.

But if we put them in an arbitrary order, we do not automatically have a meaningful QUANTA sentence.

```text
[ ( . ) ]
```

This is readable as nested forms.

Now look at:

```text
[ ( . ]
```

Something is unfinished. The opening parenthesis has no matching closing partner.

That does not make the marks evil or useless. It simply means we do not have a complete, well-paired structure under the reading rules we are introducing.

For the first time, QUANTA will say not only **what a mark suggests**, but **whether a group of marks can be read together**.

### 3. The rule of pairs

Think of opening a small wooden nesting doll.

Inside sits another doll.

The outer one closes around the inner one, and the inner one closes around its own space.

Our brackets behave similarly.

```text
[ . ]        paired

( . )        paired

[ ( . ) ]    paired and nested
```

Each opening mark must find its own matching close.

We can picture the structure as two hands holding something carefully:

```text
[   ( . )   ]
^           ^
outer pair
```

The important thing is not the number of marks. It is that they fit together without crossing their partners.

These two patterns do *not* fit the introductory grammar:

```text
[ ( . ]

[ ( ] )
```

The first is missing a close. The second closes the outer pair before closing the inner one.

We will call such arrangements **unbalanced**.

The word is gentle but exact: a reader cannot finish the nesting with the expected rules.

### 4. What belongs inside

Return to the box:

```text
[ . ]
```

There is a marked interior.

Now let us place a returning path inside it:

```text
[ ( . ) ]
```

This is a visual sentence with two levels.

The box holds a loop-like form. The loop-like form holds a dot marker in our notation.

It is not yet a physical engine. It does not prove a torus contains a particle. It simply gives our reader a consistent *structure of containment*.

We can read it from the outside inward:

**box → return → mark**

Or from the inside outward:

**mark → return → box**

Both readings point to the same nested shape. They tell different stories about the direction in which we are *describing* it, not two different physical events.

### 5. The smallest reading machine

Imagine asking a child to check whether a string of brackets is well formed.

They might use a stack of little cards.

Every time they see an opening bracket, they place a card on the stack.

Every time they see a closing bracket, they look at the most recent card.

If it matches, they remove that card.

If it does not match, they stop and show you the problem.

At the end, the stack should be empty.

It sounds like a game because it is one.

It is also the basis of a simple parser.

A parser is a reader that follows explicit rules rather than guessing what the author intended.

For our first QUANTA reader, the rules are deliberately small:

- A dot `.` is a mark.
- Square brackets `[ ]` and parentheses `( )` form matching pairs.
- Paired forms may contain dots or other paired forms.
- An unmatched or improperly crossed pair fails this *introductory* check.
- Vertical bars `|` are reserved for a later transport grammar, and are not validated by this nesting game.

This is a teaching subset—not a declaration that all future QUANTA syntax must fit these five rules.

### 6. The mirror at the center

There is something beautiful about:

```text
[()]
```

The openers arrive in one order:

```text
[ (
```

Then the closers return in the reverse order:

```text
) ]
```

The outside has to wait for the inside.

A little doorway opens. Another opens within it. The inner doorway closes first. Then the outer doorway closes.

This is not a new law of matter. It is the familiar mathematical idea of **proper nesting**.

But it gives the QUANTA page an immediate sense of rhythm.

Open.

Enter.

Return.

Close.

We can begin to imagine a language in which entering and leaving are distinct acts, and every closing boundary knows which opening it belongs to.

### 7. A different kind of line

Now recall our transport motif:

```text
.|.|.|.|.
```

It does not have nested brackets.

Instead it alternates marks and separators.

Five dots.

Four boundaries.

This arrangement tells us that QUANTA may need *more than one grammatical pattern*.

A nested structure answers: **what belongs inside what?**

A path answers: **what lies beside what, and what might cross between?**

Neither should be forced into the other's grammar merely because both use the same small alphabet.

We can sketch the difference:

```text
[()]         nesting

.|.|.|.|.    sequence
```

There is room for both in one language.

The next chapters will have to define how a nested vessel sends a signal along a sequential path, what survives transfer, and how a receiver knows it got the same message.

### 8. The reader who says “unknown”

Suppose our little parser encounters:

```text
[}{]
```

The symbol `}{` has appeared in the larger QUANTA corpus as a possible unbinding or transformation motif.

But we have not introduced its exact grammar here.

A careless reader might invent a meaning.

A trustworthy reader says:

**Not part of the grammar I have been given.**

That is not failure. It is correct restraint.

Likewise:

```text
{{i}}
```

We have used this as a recognizable identity or observer-center motif. Its full operator semantics are not established by our simple bracket checker.

A language reader can be correct by recognizing its limits.

We do not need to pretend to know everything in order to begin reading something.

### 9. Wordle of Space — Puzzle 010

Which of these is well-paired under the first QUANTA nesting rules?

```text
A:  [ ( . ) ]

B:  [ ( . ]

C:  [ ( ] )
```

**Answer: A.**

B forgets to close the parentheses.

C closes the box while the parentheses are still open.

A completes its innermost pair before closing its outermost pair.

Now try a harder one:

```text
[ ( [ . ] ) ]
```

Follow it with your finger.

Open a box.

Open a loop.

Open another box.

Meet the dot.

Close the inner box.

Close the loop.

Close the outer box.

The story returns without losing its place.

### 10. The tenth QUANTA rule

We have traveled from the first zero to a message that can be recognized.

Now we give the message a readable structure.

> **Q9 — Form Before Interpretation.** Before assigning a meaning to a QUANTA expression, a reader must determine which grammar applies and whether the expression is well formed within that grammar. Unsupported forms remain unassigned rather than being silently repaired.

A reader may then ask what the expression means.

That second question belongs to interpretation, and ultimately to the codebook we began exploring in Chapter 9.

We now have three little treasures:

```text
.           a mark

[()]        a nested form

.|.|.|.|.   a sequential form
```

And a promise:

**Read the marks as they are before claiming what they say.**

Across the valley, the grandmother sends her two flashes.

The boy knows the meaning because they share a code.

One day, he writes down the rule so a third person can read it too.

The note is no longer a secret between two windows.

It is the beginning of a language someone else can learn.

*End of Chapter 10 — Next: Chapter 11, The Grammar.*

---

### Optional technical note

The introductory bracket checker implements a simple properly nested delimiter language. It verifies syntax, not physical correctness or message meaning. It deliberately excludes the full semantics of `|`, `{ }`, `}{`, and `{{i}}`. The general QUANTA grammar remains under development. An implementation should distinguish invalid syntax from constructs reserved for a richer dialect.

### Chapter 10 technical ledger

| ID | Statement | Status |
|---|---|---|
| M-020 | Properly nested brackets can be checked with a stack | Established computer science |
| M-021 | Syntax checking does not by itself establish semantic meaning | Established language-design distinction |
| Q-020 | Dots and paired square/round delimiters form a first teaching subset | Proposed QUANTA grammar subset |
| Q-021 | The transport motif belongs to a separate sequence-reading context | Proposed design direction |
| Q9 | Form Before Interpretation | Proposed language design rule |
| P-010 | Successful parsing of QUANTA syntax validates a physical theory | Not established |
