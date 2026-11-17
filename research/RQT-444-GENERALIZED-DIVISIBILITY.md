# RQT-444 — Generalized Divisibility Kernel

For any prime p and nonzero f, put h=v_p(f), E=L²-fC. Integral local roots correspond exactly to s²=E and s=L mod p^h. If E=0 require p^h|L. Otherwise v_p(E) must be even, say 2k, and U=E/p^(2k) must be a square unit. If k>=h require p^h|L. Otherwise require v_p(L)=k and let l=L/p^k, r=h-k. For odd p require l²=U mod p^r; for p=2 require l²=U mod 2^(r+1) in addition to U=1 mod8. The latter follows because squaring maps 1+2^r Z_2 onto 1+2^(r+1) Z_2 for r>=2; r=1 is automatic for odd units with U=1 mod8. Odd prime unit lifting follows from Hensel.

Executed 1936 synthetic controls at p=2,3,5,7 and h=0..3, and a new full-Gram tile y=705..736, odd d=1..767: 12288 pairs, 135168 feasible x, 14976 prime rejections, 393 baseline survivors, 269 coupled survivors, zero exact squares. The derivative source verifier reports this additional coupled stage under its inherited finite counter. Combined rectangle y=1..736 and odd d=1..767. No global nonexistence claim. Root19 OPEN; position18 UNVERIFIED.

Art correction: k<h is not automatic rejection; k>=h is not automatic acceptance. Original F4 norm is -2d².