# RQT-366 — Root18 GMA generational {{9x9}}^9 around a singlet

**2026-11-14 | Status: concrete search upgrade implemented, bounded depth-nine test completed, original root18 OPEN.**

## User-specified new search geometry
The 9x9 generation is centered on a single coordinate (the singlet) at (row,col)=(4,4), mapped to balanced ternary-like base-nine digits i,j∈{-4,...,4}. Every 9x9 grid has 81 addresses, including its own central singlet. Nine nested generations form **81^9=150094635296999121 unique addresses**, not a claim that this many agents or candidates have been instantiated.

## Exact original mathematics
Frozen authentic F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. The unimodular RQT-363 chart U satisfies det U=-1; original r=U.T*t and G=U*F4*U.T. A norm-minus-two candidate must satisfy t.T*G*t=-2.

Let t=(a,b,c,d), define
```
A=G[3,3]
B=G[0,3]*a+G[1,3]*b+G[2,3]*c
C=G[0,0]*a²+G[1,1]*b²+G[2,2]*c²
  +2G[0,1]*ab+2G[0,2]*ac+2G[1,2]*bc+2.
```
The exact norm equation is A*d²+2*B*d+C=0. Its divided discriminant is Delta=B²-A*C. Integer d requires Delta >=0, Delta a perfect square, and d=(-B±sqrt(Delta))/A an integer. The executable checks the original exact F4 norm and accepted root18 parities `0111, 1001, 1110`.

## Nine-generation bijective three-coordinate address
Each of nine generations contributes two independent balanced radix-9 digits, for a total of 18 digits and **six independent digits per search coordinate**. The coordinate pairs rotate deterministically:
```
g1: (a,b)     g2: (b,c)     g3: (c,a)
g4: (a,b)     g5: (b,c)     g6: (c,a)
g7: (a,b)     g8: (b,c)     g9: (c,a)
```
For each coordinate, the first time it is visited its digit has weight 9^0, next 9^1, etc., up to 9^5. Therefore every complete nine-generation address uniquely specifies a triple (a,b,c), and every triple in
```
a,b,c ∈ [-265720,265720]
```
has exactly one address. The all-zero address is the singlet at (0,0,0); the singlet is a valid state, not a deleted hole.

## Exact safe partial-node pruning
After some generations, counts c_i record how many low-order digits of each coordinate have been assigned. Future increments on coordinate i are multiples of 9^c_i. Thus if k=min(c_0,c_1,c_2), all future candidate triples remain identical mod9^k, and so does their quadratic discriminant Delta. If Delta mod9^k is not a quadratic residue, **no descendant can have a perfect-square discriminant** and the entire subtree can be safely pruned. This is an exact necessary condition, not a heuristic fitness function.

The traversal is depth-first and lazy. A node budget prevents unbounded work and the result explicitly marks when it was truncated. Every completed ninth-generation address receives an exact nonnegative perfect-square, integer fourth-coordinate, F4 norm and parity check. A candidate passing these gates still requires the actual frozen factorization/prefix tests before being named **root18**.

## Initial completed bounded test
Locally executed file `/mnt/data/rqt366_gma_9x9_root18.py` with `--depth 9 --budget 10000`:
```json
{"generation_reached":9,"nodes_examined":10000,
 "pruned_exact_modular":1,"completed_addresses":9869,
 "truncated":true,"exact_permitted_roots":[],"root18_status":"OPEN"}
```
The GitHub executable is the same algorithm with equivalent output labels. This run covers **only the first 9869 addresses in deterministic center-first depth-first order**, not all 81^9. No root found in that partial set; it is not a global nonexistence proof.

## Next RQT-367
Add branch scheduling by **search diversity** and exact modular witness packets, instead of exploring millions of neighbors within the first parent. Each branch packet should include its nine-generation GMA address, integer triple (a,b,c), exact Delta and any surviving fourth-coordinate(s), norm proof, first-root parity, and eventually authentic frozen-prefix rank/order and four-root Wall flag. Maintain append-only provenance and never call a partial search exhaustive.

The `{{9x9}}^9` singlet-centered tensor is a search-address geometry; it changes neither F4 nor the proof standard. Root18 and roots19–21 remain OPEN.
