#!/usr/bin/env python3
"""RQT-560: exact compositeness witness for RQT-559 norm numerator.
Usage: python rqt560-composite-witness.py RQT-559-results.json
"""
import sys,json,math
from pathlib import Path
d=json.loads(Path(sys.argv[1]).read_text())
N=int(d['numerator']); T=int(d['T']);beta=int(d['beta'])
assert N.bit_length()==942 and N%2 and math.gcd(N,beta)==math.gcd(N,T)==1
v=N-1;s=0
while v%2==0: v//=2;s+=1
R=[pow(2,v*2**i,N) for i in range(s)]
assert s==2 and R[0]!=1 and all(x!=N-1 for x in R)
print('PASS: exact base-2 strong Miller-Rabin compositeness certificate; s=',s)
print('Individual prime factors and relative norm obstruction: UNRESOLVED.')
