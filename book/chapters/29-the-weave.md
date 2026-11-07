# Chapter 29 — The Weave
## When Many Paths Carry One Story

*QUANTA: The Wordle of Space*  
*David Lee Wise*  
*Reader-first manuscript draft 0.1 — 7 November 2026*

> A thousand echoes of one voice are not a thousand witnesses.

### 1. The third knock

The child and the neighbor are still sitting beside their two boxes.

Between them rests the folded note:

```text
.|.|.|.|.
```

Five dots. Four bars.

They have learned to share the marks without assuming they share every meaning.

Then someone knocks again.

A third traveler stands in the doorway carrying another box.

And beyond the traveler, down the hill, the child notices more lamps in more windows.

Each window might hold another notebook.

Each notebook might contain a different view of the world.

The little room that once held one box begins to feel like part of something larger.

### 2. Draw the neighbors

The child places three boxes on the table.

```text
         [ B ]
          / \
         /   \
      [ A ]--[ C ]
```

The drawing shows possible routes between A, B, and C.

It does not prove any message was sent.

But it does help the child ask useful questions:

Who observed what?

Who copied whom?

Which path carried each message?

And whose report is still missing?

A network begins with connections.

Trustworthy knowledge begins with the history of what moved along them.

### 3. Three reports, one source

The neighbor reads a measurement from notebook B.

A copies the measurement.

C hears A read the copy and writes it down.

Now all three notebooks say:

```text
6.1 cm
```

It may look like three confirmations.

But the child opens the records and draws their lineage:

```text
B: observation
   |
   v
A: copy of B
   |
   v
C: copy of A
```

One originating observation.

Three copies or appearances of that observation.

The extra notebooks may make the report easier to find. They do not automatically create more independent evidence that the measurement was correct.

**Counting copies as witnesses makes a weave look stronger than it is.**

### 4. The independent view

The traveler at C decides to measure the shadow separately.

They arrange the lamp and card using a documented method.

They write down their own reading, with its own conditions and uncertainties.

Now the provenance has another root:

```text
B: observation ----> A: copy ----> C: copy

C: new observation (separate event)
```

The new observation may agree with B.

Or disagree.

It is not automatically fully independent just because another person performed it. They may share the same method, instrument calibration, or hidden assumption.

But the record can at least distinguish a **new measurement event** from a **copied message**.

That is the beginning of careful corroboration.

### 5. A weave remembers its threads

The child draws lines of different kinds.

```text
A ----copy----> B
B ----report--> C
C ----query---> A
```

These are illustrative relationship labels, not executable QUANTA syntax.

A line can mean copied from, measured by, received by, or requested by.

Those are not interchangeable.

A good weave does not merely count edges.

It records the *type* and *direction* of each edge, with a source for the claim that the edge exists.

The child labels every strand before adding another.

The more complicated the drawing becomes, the more important those little labels are.

### 6. The center that isn't an owner

The child sets the original box in the middle.

```text
        [ B ]
          |
[ C ] -- [ A ] -- [ D ]
          |
        [ E ]
```

A can serve as a convenient hub.

It can collect reports and display where they came from.

But a hub is not necessarily the owner of what passes through it.

If B recorded a shadow, A's receipt does not turn B's observation into A's independent discovery.

If C disagrees, A may preserve both reports.

If D has no data, A should show that absence rather than invent a vote.

The center can help everyone find the records without pretending to be the source of every record.

### 7. The rumor that circles

Now imagine B sends a claim to C.

C sends it to D.

D sends it back to B.

```text
[ B ] --> [ C ]
  ^         |
  |         v
[ D ] <-----
```

B receives the claim again and thinks, *Someone else has confirmed it!*

But it is the original claim returning by another route.

The loop has created another appearance of evidence without creating a new observation.

The solution is not to forbid loops.

Loops can be useful for communication, retrying, and finding alternate paths.

The solution is to preserve a message identifier and the originating record so that the returned claim can be recognized.

A circle in the network need not become a circle in our reasoning.

### 8. Agreement without a vote

The child asks whether a majority of boxes should decide what happened.

Suppose four copies of one report say the shadow was short, while one independently measured result says it was long.

A simple vote gives the copied claim four votes and the measurement one.

Yet this arithmetic conceals the provenance.

We should first ask how many distinct observations the reports actually represent, what each measured, and whether their conditions were comparable.

Even three genuinely separate observers may share a mistaken assumption.

Agreement is evidence only to the extent that the sources and methods justify it.

QUANTA does not have to pretend that every disagreement has a tidy winner.

It can preserve a disagreement until a better test arrives.

### 9. Wordle of Space — Puzzle 029

The network has five reports:

```text
B1  original measurement: 6.1 cm
A1  copied from B1
C1  copied from A1
D1  copied from B1
E1  new measurement: 6.2 cm
```

How many distinct measurement events are identified by this record?

A. Five, because five notebooks contain numbers.

B. Two: B1 and E1. The other three entries are copies.

C. One, because all the numbers are similar.

**Answer: B.**

Two measurement events are reported. Their statistical independence still needs examination.

Now draw the arrows from each copy to its source. Observe how five entries reduce to two originating measurement records.

**Try it:** Invent a network of four boxes, with two original observations and two copies. Label every edge with its relationship. Then ask which reports would still exist if every copy were removed.

### 10. The thirtieth QUANTA rule

The child looks at the lamp in the window.

One room became two boxes.

Two boxes opened a gap for messages.

Now many boxes can connect.

But the weave must not make the history of its threads disappear.

> **Q28 — A Weave Must Preserve Its Sources.** A QUANTA network record must distinguish originating observations from copies, relays, interpretations, and independent tests. Every connection carries a declared relationship and provenance. Agreement, repetition, and message circulation must not be silently counted as additional independent witnesses.

The child draws the familiar trace inside one box:

```text
[ .|.|.|.|. ]
```

Then draws another box beside it.

Then another.

The wall now carries a pattern of boxes and lines.

None has to surrender its identity to become part of the picture.

And in the center of the weave, there is still a little space.

A gap.

A place for another question.

The child closes the notebook and looks toward home.

**A weave can connect the boxes. But what happens when the traveler returns to the first one?**

*End of Chapter 29 — Next: Chapter 30, The Homecoming.*

---

### Optional technical note

A provenance graph may represent events and records as nodes with typed, directed relations such as observed-by, copied-from, and derived-from. Counting distinct graph nodes alone does not establish independent empirical observations: copies, duplicated messages, correlated sensors, and shared calibration can introduce dependencies. Detecting cycles and assigning stable source identifiers help prevent repeated reports from being miscounted as independent corroboration. The chapter's network is an illustrative record model, not a deployed consensus system.

### Chapter 29 technical ledger

| ID | Statement | Status |
|---|---|---|
| M-058 | Copies of a record do not constitute additional independent observations | Established provenance and research principle |
| M-059 | Correlated observations and circular reporting can distort naive counts of corroboration | Established statistical and evidentiary reasoning |
| Q-058 | QUANTA network edges carry relationship types, directions, and source references | Proposed record architecture |
| Q-059 | Relays and copied reports must not be automatically counted as independent witness events | Proposed evaluation policy |
| Q28 | A Weave Must Preserve Its Sources | Proposed language design rule |
| P-029 | More agreeing messages guarantee more independent or correct evidence | Not established |
