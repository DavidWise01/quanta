# RQT-329 — Original root 18–21 matrix preflight

**Current evidence:** The original frozen F4,X4 have **not** been recovered. Original roots 18, 19, 20, 21 are **OPEN**. A constructed bridge example must never be substituted for them.

## Exact input gate

The executable `research/rqt329-frozen-preflight.py` requires either `--demo` or `--input original.json`. Original JSON must have full integral 4x4 `F4`, `X4` and a `source` provenance entry. File SHA-256 is printed with the results. The script rejects nonsymmetric or singular Gram matrices and transformations not preserving the form.

The preflight computes exact Gram determinant, inertia (rational symmetric congruence reduction), rational moving rank, exact binary order up to 32 (otherwise unknown), and for Lorentzian signature (1,3) compares two positive-norm vectors to detect whether X reverses the two positive-cone components.

## Necessary obstruction theorem

For a real symmetric form with exactly one positive direction and all others negative, positive-norm vectors form two connected cones. Any reflection in a norm-negative vector fixes a positive-norm vector and hence preserves each cone component. An isometry X reversing components **cannot** equal any product of norm-negative reflections. This rules out four norm -2 reflections, indeed any number, without enumerating integer candidates. If X preserves the components, this obstruction is absent **but integrality, norm, parity, divisibility, rank and mod-2 conditions remain open**. Other signatures require different tests; the script returns `not_applicable` rather than inventing a result.

## Regression

`python research/rqt329-frozen-preflight.py --demo` checks the constructed bridge F,X and reports det F=-3, signature (1,3), moving rank 4, binary order 3, reversing orientation with an exact positive-vector witness. This is **not** an original frozen result.

Nested {brace[box(toroid)]} spatial tensor and 1+6+12+8 neighborhoods, Josophene software hook, Juliet gates and time/angular address are evidence routing metadata, not mathematical proof of a frozen root.

## Next natural bound — RQT-330

Recover F4,X4 from a verifiable immutable source or derive a no-go result for any available precise invariants. Only after an original-input preflight passes should we run the source-bound root-18 search and continue the reflected transformations toward roots 19–21.
