#!/usr/bin/env python3
"""RQT-577 reproducible exact 2-adic lift. Requires local RQT-575 reduced_gram.json."""
import json,sys
F=[[int(z) for z in row] for row in json.load(open(sys.argv[1]))]
q=lambda x:sum(x[i]*F[i][j]*x[j] for i in range(4) for j in range(4))
fx0=lambda x:sum(F[0][j]*x[j] for j in range(4))
x=[1,0,1,0]
assert (q(x)+2)%16==0 and fx0(x)%2
for k in range(4,33):
 assert (q(x)+2)%(1<<k)==0 and fx0(x)%2
 if k==32:break
 bit=((q(x)+2)//(1<<k))%2
 x[0]+=bit*(1<<(k-1))
assert x==[359343129,0,1,0]
assert q(x)+2==-1240051220113294867730903967631147008
assert q(x)!=-2
print('PASS 29 exact congruences mod 2^4 ... 2^32; global integral root and root19 OPEN')
