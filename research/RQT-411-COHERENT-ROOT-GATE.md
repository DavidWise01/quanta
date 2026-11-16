# RQT-411 — The Coherent Root Gate

## Exact theorem from the original candidate-successor Gram
Let A=Q/2, f=A22, L=A02*x+A12*y, M=A00*x²+2A01*xy+A11*y²+1 and E=L²-fM. Since 299=13*23 divides f, E≡L² modulo 299 for **every integer pair (x,y)**. So square-residue tests modulo divisors of f cannot eliminate a single (x,y) pair.

A genuine integer z requires E=s²≥0 for some ordinary integer s, and the *same sign* must satisfy f | (s-L) or f | (s+L). Partial factorization is not a replacement for exact divisibility by |f|.

## Executed exact CRT classification
Enumerated all 299²=89401 (x,y) residues from the full RQT-401 matrix. There are 78936 classes with four roots s modulo 299, 10166 with two, and 299 with one. For the actual (16,9), L mod299=148 and roots are 125,148,151,174. Exactly 148 and 151 are coherent; 125 and 174 are mixed-sign. The integer E(16,9) is positive but nonsquare, so this is *not* a root19 witness.

Only factors 13 and 23 of the 1352-bit coefficient f have been used; do not state f is fully factored. The frozen position-18 predecessor compatibility is still unverified.

Root19 OPEN · Root20 OPEN · Root21 conditional.

## ASCII diagram
```text
       RQT-411 : COHERENT ROOT GATE
              E(x,y)=s²
                  |
              s mod 299
               /      \
         coherent    mixed
         148,151    125,174
            |           X
          mod |f|
            |
        z integral?
            |
         ROOT19 OPEN
```

The JPG and embedded-JPG standalone HTML are conversation artifacts; the repository chapter contains the ASCII visual.
