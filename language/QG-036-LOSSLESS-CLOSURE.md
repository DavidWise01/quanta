# QG-036 — Lossless Closure of One [84211] Quantum Box

**Invariant:** `|||| → [8] → [4] → [2] → [1] → [1] → recover → preserve ||||`

The enclosing symbolic [84211] box must not discard the original four sealed [1311] actor chambers when advancing through its fold stages.

## Transport

1. Verify QG-035 event replay, six unique faces in each of four actors, and one appended judge ruling.
2. Produce eight ordered leaves: `[A.identity, A.completeChamber, B.identity, B.completeChamber, C.identity, C.completeChamber, D.identity, D.completeChamber]`. Each complete chamber contains all face records, statement and source label.
3. Pair leaves into four nodes, then two, then one. Pair nodes carry **both complete child nodes**.
4. Final `1 → 1` is an exact identity carry, not another lossy reduction.
5. The original QG-035 ledger and all events are retained separately. Unfold the final single node to exactly the eight original leaves and verify the QG-035 source by event replay.

This is an **expandable nested representation**, not data compression; the fully expanded tree retains duplicate records at several stages. No data is encoded in a lone scalar 1.

## No-erase law

`A,B,C` may report. `D` may append a bounded verdict. Neither D nor the fold may replace any sealed source report. If a chamber is open, the judge verdict is absent, an event changes, a fold child changes, or the final 1→1 stage differs, closure is rejected.

## Limits

This symbolic arrangement is not a physical quantum computer, a proof of Byzantine consensus or cryptographically authenticated history. Deterministic replay checks structural consistency, not original authorship or historical truth.

- [Executable lossless closure kernel](./lossless-closure.mjs)
- [Eight tests](../tests/lossless-closure.test.mjs)
- [Interactive fold viewer](../lossless-closure.html)
