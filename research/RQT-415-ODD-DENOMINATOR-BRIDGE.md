# RQT-415 — The Odd Denominator Bridge

Date: 2026-11-15. Fixed RQT-401 reduced candidate-successor Gram.
The previous RQT-414 result established rational existence, but gave no explicit coordinates.

## Global arithmetic theorem

Let q(v)=vᵀAv with A=Q/2. Write a rational solution v=w/d in
lowest terms, so d>0, w∈Z³, gcd(w0,w1,w2,d)=1 and q(w)=-d².
The actual matrix A modulo 4 is
 [1 0 1]
 [0 2 3]
 [1 3 3].

Since A is symmetric, q(w) modulo4 depends only on coordinate parities.
The primitive nonzero parities have residues:
 001→3, 010→2, 011→3, 100→1, 101→2, 110→3, 111→2.
Consequently q(w) divisible by 4 implies all three coordinates of
w are even. If d were even, q(w)=-d² would be divisible by 4,
forcing gcd(w0,w1,w2,d)≥2: contradiction. Thus every reduced rational
solution has an ODD denominator.

Since d odd, -d²≡3 modulo4, forcing numerator parity to be one of
001, 011, 110. Exact local enumeration finds 24 numerator triples
mod4 and 96 triples mod8 compatible with -d² for odd d.

This theorem is independent of coordinate height and narrows any
future rational witness search. It does NOT prove d=1, and no rational
coordinates or integral root19 have been constructed.

## ASCII illustration

```
        RQT-415 :: ODD DENOMINATOR BRIDGE
           +-------------------------+
           |     q(w) = -d^2        |
           +------------+------------+
                        |
                 d even / odd
                   /       \
              EVEN         ODD
                |           |
           q(w)=0 mod4    allowed
                |           |
            w all even    001 011 110
                |           |
           NOT LOWEST    denominator 1?
                X           |
                          ROOT19
                           OPEN
```

Source ancestry: one canonical GitHub corpus; a generated JPG is supplied
as a conversation artifact and embedded in a standalone downloadable HTML.
Root18 ordering unverified; root19 OPEN; root20 OPEN; root21 conditional.
