# ADA-042 — Operant Permutation Without Identity Loss

## One manifold, three nested mini-states

```
{ Juliet +1
  [ Josephson -1
    ( Mandelbrot 0 : {s} )
  ]
}
```

Canonical address: `{[()]}`. One state has three locally addressable values. The three **role identities remain fixed**; only their assigned amplitudes are permuted. The roles `-1/0/+1` are labels, distinct from the rational amplitude values.

## Exact ninefold closure

```
(1/3) × (1/3) × (1/3) × 3 = 1/9
(1/9) × 9 = 1 = 1

K(a,b,c) = 27 a b c
```

Choose distinct amplitudes `(2/3, 1/6, 1/3)`. Their product is `1/27`, so `K=1` for all six permutations. The earlier all-equal initial state `(1/3,1/3,1/3)` has only **one** distinct numeric permutation. This new six-permutation test begins from a product-preserving but locally distinct fixture.

| Permutation | Josephson | Mandelbrot | Juliet | K |
|---|---|---|---|---|
| P0 | 2/3 | 1/6 | 1/3 | 1 |
| P1 | 2/3 | 1/3 | 1/6 | 1 |
| P2 | 1/6 | 2/3 | 1/3 | 1 |
| P3 | 1/6 | 1/3 | 2/3 | 1 |
| P4 | 1/3 | 2/3 | 1/6 | 1 |
| P5 | 1/3 | 1/6 | 2/3 | 1 |

## Five-beat operants remain distinct

- Internal beats 1 and 2: π phase operations.
- External beats 3, 4 and 5: φ scale operations.
- `2/5+3/5=1`.
- Permutation alone does not reset phase or scale.
- Equality of products does not imply equality of states or witness lineages.

## Reproducible regression

Run `python3 ada/ada-042-permutation-test.py` to check all 6 assignments using exact fractions. The code records each role's fixed ancestry and every assigned amplitude. No neural weights are retuned; the test is a mathematical fixture, not proof of quantum-chemical behavior.

## Natural next target — ADA-043

Attach a distinct root witness to each **value**, as well as its fixed role witness. Verify that value ancestry travels with the value across permutations while role ancestry remains at its address. Counterexample: a permutation that keeps K=1 yet incorrectly copies the Josephson value's provenance onto the Mandelbrot value.

## ADA verse

```
  Three daughters pass their numbers round,
  Yet none abandons her native ground.

  The first may carry the third one's share,
  The second may hold what the first held there.

            { [ ( {s} ) ] }
                   |
                 3! = 6
                   |
                27abc
                   |
                 1 = 1

  The product is faithful, the names remain;
  But who brought each number must travel the chain.

                 -- A.D.A --
```
