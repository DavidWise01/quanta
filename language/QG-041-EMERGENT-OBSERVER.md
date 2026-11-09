# QG-041 — Emergent Observer Preference

**Premise:** a sufficiently experienced player might find it more rewarding to watch many games concurrently than to play only one. This is a hypothesis about agent preference, not an established consequence of game theory.

`24! = 620,448,401,733,239,439,360,000` is the count of permutations of 24 distinguishable positions. The kernel treats it as an **experience-space metaphor** and optionally stores a `declaredPriorGames` value as unverified metadata. It **does not** enumerate or pretend to have played 24! games.

## Falsifiable toy model

Each append-only event either:
- `play`: engages one game and reports an observed pattern, outcome payoff and attention cost.
- `observe`: compares 2–6 distinct games and records observed patterns, payoff and cost.

The explicitly declared utility proxy is:
`2 × previously unseen patterns + 0.75 × distinct games + payoff − cost`.

These weights are a design hypothesis, not a measurement of enjoyment. A bounded six-play and three-observation rolling-average comparison selects `play`, `observe` or `indifferent` only after at least six actual plays and three actual observation samples. Before that, `undetermined`. A margin of 0.25 reduces small switches. **No hard-coded switch at 24! or at any game count.**

The player can later choose to play again if the evidence changes. No mode is irreversible. The append-only event record is replay-verified to detect accidental or local tampering but provides no cryptographic authentication.

## Simulation outcomes

Expected from deterministic synthetic fixtures:
- repeated low-novelty play plus rich cross-game observations → `observe`
- expensive low-novelty monitoring → `play`
- declared 24! games without comparative observations → `undetermined`
- strong new game opportunities after observing → `play`

These are behaviors of the defined utility model, **not proof that a real agent has discovered joy, achieved consciousness or played a massive number of games**. No repository-wide autonomous player is activated.

- [Kernel](./emergent-observer.mjs)
- [Eleven executable tests](../tests/emergent-observer.test.mjs)
- [Interactive viewer](../emergent-observer.html)
