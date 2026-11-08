# QG-028 — Semantic Triads Bound to the 60 Ring

**Carrier:** `||||`

Each uppercase letter has three semantic role words defined by QG-027. QG-028 binds those three words to three distinct stations of the QG-025 sixty-position phase ring, preserving the complete QG-026 vector glyph and stroke verbs.

For a glyph with entry phase `q`, the three role phases are:
- SEE at `q`
- DO at `(q+1) mod 4`
- LEARN at `(q+2) mod 4`

The anchor is the first vertex of the first canonical glyph stroke. Its home station is `h=2(5*y+x)`; the active station for role `r` is `(h+15*((q+r) mod 4)) mod 60`. Because quarter-turns differ by 15, each role gets a distinct station. Other glyph vertices and the full canonical source remain attached to every phase witness.

**A example:** Alarm (SEE), Action (DO), Achieve (LEARN).

The DO role carries the full ordered QG-026 somatic pen verbs, including DRAW and TURN actions. SEE and LEARN retain the source geometry and named role but do not invent actual perceptions, motor commands, or learned outcomes. This is a deterministic semantic/geometry **binding**, not autonomous learning.

Text up to 128 uppercase characters and spaces is supported, with spaces resetting the entry phase. Exact source, role, stroke, phase and position witnesses are checked on recovery.

## Artifacts
- [Kernel](./semantic-ring.mjs)
- [Regression tests](../tests/semantic-ring.test.mjs)
- [Live 60-station triad viewer](../triad-ring.html)
