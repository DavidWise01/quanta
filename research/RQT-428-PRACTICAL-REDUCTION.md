# RQT-428 — Practical Reduction Gate

Date 2026-11-16. Original: full frozen candidate-successor RQT-401 Gram; positional root18 compatibility still unverified.

Let A=Q/2, T=[[-9,-25,0],[-5,-14,0],[0,0,1]], det T=+1, C=TᵀAT. RQT-428 uses V=[[1,0,0],[0,1,-8],[0,0,1]], det V=+1, D=VᵀCV=(TV)ᵀA(TV). This is a genuine integral congruence and preserves all rational and integral representations.

## Executed exact audit

Enumerated every single elementary shear I+k e_ij for i≠j and k in {-4,-3,-2,-1,1,2,3,4}: 48 tests. None reduces the sum of bit lengths of the 6 upper-triangular coefficients of C. This is only a finite local test, not optimality under GL₃(Z).

The separate k=-8 shear strictly decreases the coefficient absolute-value sum S and hence Cassels' numerical height bound, while leaving the bit-length score unchanged. Exact 3D scores: original A 7053; C 7015; D 7015. The four-dimensional scores add one for the d² coefficient: 7054,7016,7016. All three Cassels bounds remain 611 digits. This is *not yet* a practical construction algorithm.

## ASCII
```text
       RQT-428 : PRACTICAL REDUCTION
     +--------------------------------+
     | A = Q/2                        |
     |    |                           |
     | C = T^T A T     det T = +1      |
     |    |                           |
     | D = V^T C V     det V = +1      |
     |    |                           |
     | 48 SMALL SHEARS               |
     | 0 BIT-SCORE IMPROVEMENTS      |
     | k = -8 REDUCES S              |
     |    |                           |
     | HEIGHT BOUND : 611 DIGITS     |
     | ROOT 19 : OPEN                |
     +--------------------------------+
```

No explicit rational witness and no integer root19 found. Root18 ordering unverified; root20 open, root21 conditional. The new JPG illustrates the research concept only, not proof or a root witness. The single underlying Gram means multiple arithmetic checks do not constitute independent source ancestries.

Next RQT-429: certified rational isotropic-vector construction rather than surrogate coefficient-size optimization.
