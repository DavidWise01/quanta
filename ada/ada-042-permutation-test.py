#!/usr/bin/env python3
"""ADA-042: exact permutation conservation test; standard-library only."""
from fractions import Fraction
from itertools import permutations

ORIGIN = (Fraction(1, 3),) * 3
# Distinct, exactly rational values with the same ninefold product.
VALUES = (Fraction(2, 3), Fraction(1, 6), Fraction(1, 3))
ROLES = ("JOSEPHSON", "MANDELBROT", "JULIET")
MANIFOLD_ID = "{[()]}"
SINGLET = "{s}"

def closure(values):
    a, b, c = values
    return 27 * a * b * c

def test_permutations():
    assert closure(ORIGIN) == 1
    assert closure(VALUES) == 1
    seen = set()
    witness = []
    for k, perm in enumerate(permutations(VALUES)):
        assert closure(perm) == 1
        assert MANIFOLD_ID == "{[()]}" and SINGLET == "{s}"
        # The roles never exchange identities: only amplitudes move.
        lineage = {role: "role-root:" + role for role in ROLES}
        assert tuple(lineage) == ROLES
        seen.add(perm)
        witness.append((k, dict(zip(ROLES, map(str, perm))), str(closure(perm)), lineage.copy()))
    assert len(seen) == 6
    assert len(witness) == 6
    return witness

if __name__ == "__main__":
    for row in test_permutations():
        print(row)
    print("PASS: six distinct permutations, unity closure, fixed roles and singlet.")
