#!/usr/bin/env python3
"""RQT-567 exact compositeness check for RQT-566 remaining fixed-discriminant cofactor."""
n=555654409826629710119829271213958080091261217263858828861644919996120497288591
assert n.bit_length()==259
s=0;d=n-1
while d%2==0:s+=1;d//=2
assert s==1
for base in (2,3,5,7,11,13,17,19):
 z=pow(base,d,n)
 assert z not in (1,n-1),('unexpected probable-prime result',base)
print('PASS: rigorous composite witness at base 2; 259-bit residual factorization OPEN')
