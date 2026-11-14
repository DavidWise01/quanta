# RQT-347 — Discriminant-prime obstruction in authentic rational slope planes

**Status:** Exact verified local obstruction for three specified rational planes of the original RQT-242 Gram F4. **No exact integral root 18; roots 18–21 OPEN.**

For n>0 and d in {-1,+1}, set m=n+d and parameterize the ternary rational plane x=(-ma,b,na,c). Its integral Gram is G=T^T F4 T with T rows (-m,0,0), (0,1,0), (n,0,0), (0,0,1).

An integer primitive ternary isotropic vector would reduce to a primitive isotropic solution modulo every prime power. At an odd prime p, suppose:
1. p divides det(G) but p² does not;
2. the upper-left 2x2 principal minor h is nonzero mod p;
3. -h is nonsquare mod p.

Then the reduced ternary form has rank 2 and anisotropic nondegenerate component. Every primitive mod-p null vector belongs to its one-dimensional radical. To construct its radical generator v=(v0,v1,1), invert the upper-left 2x2 block modulo p. If Q(v)=v^T Gv is divisible by p but not by p², no vector v+pz can be isotropic mod p²: Q(v+pz)=Q(v)+2p z^T Gv+p² Q(z) ≡ Q(v) mod p², since Gv=0 mod p. Every primitive mod-p root is a scalar multiple of v, so **no primitive mod-p² isotropic vector exists**, and no rational isotropic vector exists in that plane.

## Executed certificates

| slope | p | -minor Legendre | radical v mod p | Q(v)/p mod p |
|---|---:|---:|---|---:|
| 187/188 | 887773937 | -1 | (12636392,214959457,1) | 459468411 |
| 839/838 | 159171641 | -1 | (99086324,80055564,1) | 1677429 |
| 840/839 | 2316121 | -1 | (765088,692695,1) | 1268829 |

All the listed p are prime and each divides its ternary determinant to exponent exactly 1. Every rational plane listed is therefore locally obstructed and contains no nonzero rational null vector.

This result follows RQT-346's separate obstruction at slope 838/837 using p=83. The earlier survival of 187/188 and 839/838 modulo p=3 did not imply global rational solvability. RQT-347 identifies new obstructing primes and closes those cases.

## Reproduction and limitations

Run `python research/rqt347-discriminant-prime-obstruction.py` with SymPy. It reconstructs each plane directly from the frozen F4, proves primality, determinant valuation, nonsquare two-minor, and the nonliftable radical norm. The local independently executed copy is `/mnt/data/rqt347_discriminant_prime_obstruction.py`. No floating-point logic or bounded search is needed for these three nonexistence results.

This is not a proof that the full four-dimensional F4 has no rational isotropic vector and does not certify a missing integral reflection root. Future RQT-348 should build a **general bad-prime local-obstruction sieve** for rational slopes and attempt a genuine global four-variable rational isotropic witness. When obtained, normalize primitive, test gcd(F4u)=1, construct root18 via RQT-334, and verify downstream RQT-257 Wall conditions.

**Source ancestry:** One authentic stoicheion RQT-242 F4/H4 source; all three modular calculations are derived independent arithmetical tests, not independent original source witnesses. The nested 3x3x3 tensor, Josophene/Juliet and time-angle metadata remain indexing only.
