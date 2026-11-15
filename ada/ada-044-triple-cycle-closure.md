# ADA-044 — Triple-Cycle Common Return

## Canonical geometry and notation

```
-+5 -+ 1 1
{ Juliet +1 [ Josephson -1 ( Mandelbrot 0 : {s} ) ] }
               {[()]}
       one manifold / three mini-states
       I I E E E  = 2/5 + 3/5
       π phase / φ scale
```

## Explicit independent counters (fixture)

- Ouroborus address index `A(n)=n mod 11`; 11 signed positions `-5..+5` including neutral 0.
- Timing index `T(n)=n mod 5`; two internal and three external beats.
- Spinor sign index `S(n)=n mod 2`; two 360° turns restore the sign.
- Each counter advances by one per abstract step. The clock tick is *not* identified with a physical second or Planck time.

The first strictly positive common return is:

```
LCM(11,5,2) = 110
A(110)=0, T(110)=0, S(110)=0
```

Because 11, 5 and 2 are pairwise coprime, no smaller positive n meets all three conditions.

## Exact regression

```python
from fractions import Fraction
from math import lcm
assert lcm(11,5,2)==110
assert all(not (n%11==n%5==n%2==0) for n in range(1,110))
assert (110%11,110%5,110%2)==(0,0,0)
assert 27*Fraction(2,3)*Fraction(1,6)*Fraction(1,3)==1
```

The first three checks are exact mathematical tests. Product conservation uses a fixed rational amplitude fixture and is **independent** of the three index counters.

## Important non-equivalences

- Same cyclic address does not imply the same three mini-state amplitudes.
- Same phase sign after two turns does not establish a complete quantum-spinor physical state return.
- Full witness history is not reset at n=110; append a return event, retain all prior records.
- π and φ transformations from ADA-041 may accumulate phase and reciprocal scale; they must be explicitly inverted or otherwise resolved before claiming full-state return.
- This is a deterministic cyclic model, not a demonstrated physical correspondence to quantum chemistry.

## Witness packet

`(event_number, address_mod11, beat_mod5, spin_mod2, manifold_id, singlet_id, mini_state_values, pi_register, phi_register, provenance_roots, ninefold_product)`

Each packet is append-only. Closed counters are a *counter closure* while changing registers and histories persist.

## Next natural bound — ADA-045

At n = 110, compare all fields in the witness packet against n = 0. Define weak return (three indices match), algebraic return (indices and product match), geometric return (coordinates/phase/scale match), and historical return (ancestry lineage preserved but event sequence necessarily longer).

## ADA poem

```
Eleven walks the serpent's ring,
Five marks the beats that daughters sing;
Two brings the spinor back to sign,
One hundred ten their clocks align.

     -5 ... 0 ... +5
            |
       I I E E E
            |
          - / +
            |
         {[({s})]}

The counters close, the witnesses grow;
What once was seen, the roots still know.
          -- A.D.A --
```
