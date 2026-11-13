#!/usr/bin/env python3
"""RQT-333: authentic F4 reduced-height exhaustive search, y0=1011..1020.
Exact conditional Schur bounds. Norm targets -2 and 0. SymPy required.
"""
import json
from math import floor,ceil,isqrt
from fractions import Fraction as Q
import sympy as s
J=s.Matrix([[9208923577999086,-2890579252927294,-1029318396906446,276003667781247],[-2890579252927294,-136287821825501156,-29512715198402862,11299357575842588],[-1029318396906446,-29512715198402862,-1127313935375881122,-146309554088173376],[276003667781247,11299357575842588,-146309554088173376,-5868287405277328266]])
T=s.Matrix([[31,4,-31,-18],[-100,-13,100,58],[-9,-1,9,5],[336,43,-335,-195]])
F=T.inv()*J*T.T.inv()
assert T.det()==-1 and F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
P=-J[1:4,1:4]; V=P.inv()*J[1:4,0]; beta=J[0,0]+(V.T*P*V)[0]; K=P.inv()[:2,:2].inv()
assert all(P[:i,:i].det()>0 for i in range(1,4)) and beta>0
f=lambda z:Q(int(z.p),int(z.q))
c1,c2=f(V[0]),f(V[1]);a,b,c=f(K[0,0]),f(K[0,1]),f(K[1,1]);alpha=a-b*b/c
assert alpha>0 and c>0
def enclosure(center,r2):
    assert r2>=0
    radius=isqrt(r2.numerator//r2.denominator)+2
    lo=floor(center)-radius-1; hi=ceil(center)+radius+1
    assert lo<=center<=hi and (center-lo)**2>=r2 and (hi-center)**2>=r2
    return lo,hi
j=[[int(z) for z in row] for row in J.tolist()]
total={-2:0,0:0};pos={-2:0,0:0};sq={-2:0,0:0};found={-2:[],0:[]};rows=[]
for t in range(1011,1021):
    rec={'y0':t}
    for target in (-2,0):
        R=f(beta)*t*t-target
        lo1,hi1=enclosure(c1*t,R/alpha)
        count=nonnegative=squares=0
        for y1 in range(lo1,hi1+1):
            delta=Q(y1)-c1*t
            remaining=R-alpha*delta*delta
            if remaining<0:continue
            lo2,hi2=enclosure(c2*t-b/c*delta,remaining/c)
            for y2 in range(lo2,hi2+1):
                count+=1
                A=j[3][3]
                B=2*(j[0][3]*t+j[1][3]*y1+j[2][3]*y2)
                C=j[0][0]*t*t+2*j[0][1]*t*y1+2*j[0][2]*t*y2+j[1][1]*y1*y1+2*j[1][2]*y1*y2+j[2][2]*y2*y2-target
                disc=B*B-4*A*C
                if disc<0:continue
                nonnegative+=1
                rt=isqrt(disc)
                if rt*rt!=disc:continue
                squares+=1
                for n in {-B+rt,-B-rt}:
                    if n%(2*A):continue
                    y3=n//(2*A)
                    y=s.Matrix([t,y1,y2,y3])
                    assert (y.T*J*y)[0]==target
                    found[target].append(list(map(int,y)))
        total[target]+=count;pos[target]+=nonnegative;sq[target]+=squares
        rec[str(target)]={'pairs':count,'nonnegative_discriminants':nonnegative,'square_discriminants':squares}
    rows.append(rec)
assert total=={-2:806968,0:806968} and sq=={-2:0,0:0} and not found[-2] and not found[0]
print(json.dumps({'scope':'original stoicheion RQT-242/RQT-254 lattice',
 'positive_y0':[1011,1020],'negative_y0':'covered by central symmetry',
 'pairs_checked':total,'nonnegative_discriminants':pos,
 'square_discriminants':sq,'roots':found,'slices':rows,
 'prior_searches':'RQT-254 up to 1000 (not replayed), RQT-332 1001..1010',
 'combined_height_necessary':'|y0|>=1021 conditional on prior certificates',
 'roots_18_through_21':'OPEN'},indent=2))
