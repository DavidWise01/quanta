# ADA-043 — Ouroborus Around Five

## Exact user notation
```
-+5 -+ 1 1
```

Keep literal syntax, rather than replacing it with an invented arithmetic identity.

## Proposed executable interpretation (fixture, not a declared equivalence)
- `-+5` selects symmetric signed addresses `-5,-4,-3,-2,-1,0,+1,+2,+3,+4,+5`, an **11-position** indexing convention including neutral zero.
- `-+ 1 1` names the two opposed unit directions `-1,+1` around the fixed singlet; their precise double-`1` semantic is retained as an unresolved design choice.
- Five-beat temporal cycle: `I,I,E,E,E`, internal `2/5`, external `3/5`.
- The ouroborus edge closes address `+5` back to `-5` without deleting the original visit record.
- The three mini-state roles remain nested in one manifold `{[()]}`: Josephson = -1; Mandelbrot = 0; Juliet = +1.
- Pi remains the phase operant, phi the scale operant.
- The ninefold product `K=27abc` remains the independent closure criterion, distinct from address-cycle closure.

## Exact regression invariants

```python
from fractions import Fraction
from itertools import permutations
addresses = list(range(-5,6))
assert len(addresses)==11
assert addresses[5]==0
assert [addresses[(i+1)%11] for i in range(11)][-1] == -5
beats=['I','I','E','E','E']
assert beats.count('I')==2 and beats.count('E')==3
a,b,c=Fraction(2,3),Fraction(1,6),Fraction(1,3)
assert all(27*x*y*z==1 for x,y,z in permutations((a,b,c)))
```

A closed index cycle is not the same as returning phase, full spinor, provenance, or entire physical system state. Treat the 11 address convention as a *candidate* that must be confirmed against the user-defined `-+5 -+ 1 1` syntax.

## Witness schema
Each movement records `(cycle,index,address_before,address_after,beat,pi_phase,phi_scale,manifold_id,singlet_id,role_roots,value_roots,K)`; all records append, none are rewritten. The cycle boundary is a new event, not an overwrite of position zero.

## Next natural bound — ADA-044
Test the difference between address closure (11 positions), timing closure (5 beats), and spinor return (2 turns). Under independent step counters, the first simultaneous return is `lcm(11,5,2)=110` elementary steps. This is a model assumption, not a claim that the notation itself explicitly defines those counters.

## ADA verse
```
The serpent circles fivefold time,
Two beats within, three outward rhyme.
The minus guards the root unseen,
The plus returns through what has been.

     -5 ... -1 0 +1 ... +5
       \                 /
        '--- OUROBORUS -'
                |
              {[()]}
                |
               {s}

Yet circles close while histories grow;
The witness keeps what cycles show.
```
