# RQT-416 — Rational Witness Search (negative finite result)

Date 2026-11-16. The source is the original RQT-401 full candidate-successor reduced Gram A=Q/2.

## Aim

Construct rational v=w/d, with primitive (w,d), odd positive d and q(w)=-d². This is the constructive next step after the RQT-414 Hasse–Minkowski existence theorem, but it has NOT yet succeeded.

## Exact bounded enumeration

For x,y in [-100,100], excluding (0,0) and the impossible parity x odd, y even, and d in {1,3,...,31}, calculate

  E=(A02*x+A12*y)² - A22*(A00*x²+2A01*x*y+A11*y²+d²).

A necessary condition for an integer z completing q(x,y,z)=-d² is E≥0 and E a perfect integer square; then test full A22 divisibility and direct norm equality.

Execution against the full saved matrix produced:
- 484,800 (x,y,d) triples tested
- 608 nonnegative discriminants
- 6 passing square-residue sieves (mod 64,63,65,11,13,17,19,23)
- 0 exact integer-square discriminants
- 0 explicit rational witnesses

This excludes only the specified bounded coordinate and denominator region. The RQT-414 existence theorem still implies some rational solution somewhere.

## Visual correction and witness lineage

The FIRST generated RQT-416 concept image displayed three invented vectors as if verified:
 W1=(16,9,1), d=3
 W2=(23,13,6), d=5
 W3=(31,17,9), d=7.

Exact direct substitution into the saved A rejects all three. They are NOT rational or integer root witnesses. A SECOND corrected JPG explicitly marks all three as rejected, and is the canonical image of this chapter.

Source ancestry: one frozen RQT-401 matrix. The image cannot serve as independent evidence. The executable checks and full-matrix certificate are authoritative.

## ASCII

```text
          RQT-416 : RATIONAL WITNESS SEARCH
      +--------------------------------------+
      |  q(w) = -d^2  /  odd d = 1 ... 31    |
      |  |x| <=100, |y| <=100                |
      |                                      |
      |  484,800  NUMERATOR/DENOMINATOR      |
      |      |                               |
      |     608    NONNEGATIVE E            |
      |      |                               |
      |       6    MODULAR SQUARE SURVIVORS |
      |      |                               |
      |       0    EXACT SQUARE E           |
      |      X                               |
      |  ARTWORK W1,W2,W3 = REJECTED        |
      +----------------+---------------------+
                       |
             EXPLICIT RATIONAL?
                 NOT FOUND
                       |
               ROOT19 OPEN
```

Rational existence PROVEN abstractly, coordinates NOT CONSTRUCTED.
Integer root 19 OPEN. Original root18 position remains unverified.
Root20 OPEN; Root21 conditional.
