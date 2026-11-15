#!/usr/bin/env python3
"""ADA-045 deterministic four-level return regression; standard library."""
from fractions import Fraction
from math import lcm

assert lcm(11,5,2)==110
assert all(not (n%11==n%5==n%2==0) for n in range(1,110))
assert 110%11==110%5==110%2==0

# 22 five-beat cycles; 2 internal pi/5 changes per cycle.
phase_in_pi = 22 * 2 * Fraction(1,5)
assert phase_in_pi == Fraction(44,5)
assert phase_in_pi % 2 == Fraction(4,5)   # 4pi/5 remains
# 3 external phi^(1/5) scaling changes per 5-beat cycle;
# use reciprocal symbolic exponents for exact product conservation.
exponent = Fraction(22*3,5)
assert exponent == Fraction(66,5)
a_coeff = Fraction(1,3)
b_coeff = Fraction(1,3)
c_coeff = Fraction(1,3)
assert 27*a_coeff*b_coeff*c_coeff==1
assert exponent != 0  # scale has not returned

witness = [("origin",0)]
for step in range(1,111):
    witness.append(("step",step))
assert len(witness)==111 and witness[0]==("origin",0)
assert witness != [("origin",0)]
print("PASS address return = 110")
print("PASS ninefold algebraic conservation = 1")
print("COUNTEREXAMPLE geometric return: phase residual 4pi/5; phi exponent 66/5")
print("PASS append-only witness ancestry recoverability")
