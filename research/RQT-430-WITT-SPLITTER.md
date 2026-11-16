# RQT-430 — Exact Witt Splitter

Date 2026-11-16. The original RQT-401 Gram, reduced basis B, and original F4 are checked by SHA256 and B^T F4 B = Q. For H=diag(Q/2,1), the exact algorithm **requires** a supplied nonzero rational H-null vector p. It chooses v with beta=p^T H v nonzero and sets h=v-[q(v)/(2 beta)]p. Then q(h)=0 and p^T H h=beta. The orthogonal complement of p,h is 2D, yielding a rational congruence with block [[0,beta],[beta,0]] and a perpendicular binary form.

The executed synthetic positive control H0=diag(-1,1,1,1), p=(1,1,0,0) gives hyperbolic block [[0,-1],[-1,0]] and complement I2. Deliberately invalid p=(1,0,0,0) is rejected.

**Result:** a certified *conditional* Witt-splitting step. The first rational point in the actual RQT-401 form was not constructed; root19 remains OPEN. Candidate root18 position relative to the frozen 17-prefix remains UNVERIFIED.

**Art correction:** the new conceptual JPG incorrectly labels the original-F4 norm as zero. The correct backmap for a rational candidate (w,d) has (Bw)^T F4(Bw)=-2d². The exact checker and ASCII are authoritative.

```
            RQT-430 — EXACT WITT SPLITTER
            H = diag(Q/2,1)
                   |
            RATIONAL NULL p?
               /       \
              NO       YES
              X         |
                    NULL PAIR h
                        |
                  [0   beta]
                  [beta  0 ]
                        |
                    2D BINARY
                        |
             ORIGINAL F4: -2d²
                        |
                  ROOT 19 OPEN
```

Next: RQT-431 first-point construction using an exact isotropic-vector solver, then direct norm, gcd, parity, F4/H4 and prefix checks.