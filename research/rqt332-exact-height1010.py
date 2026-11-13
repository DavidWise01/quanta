#!/usr/bin/env python3
"""RQT-332: exhaustive true-lattice norm -2 search at 1001 <= |y0| <= 1010.
Reduced Gram is from stoicheion RQT-254. Exact rational outward bounding;
exact integer-square discriminant testing. No original root claimed.
"""
from math import isqrt, floor, ceil
from fractions import Fraction as Q
from itertools import product
import json
import sympy as s
J=s.Matrix([
[9208923577999086,-2890579252927294,-1029318396906446,276003667781247],
[-2890579252927294,-136287821825501156,-29512715198402862,11299357575842588],
[-1029318396906446,-29512715198402862,-1127313935375881122,-146309554088173376],
[276003667781247,11299357575842588,-146309554088173376,-5868287405277328266]])
T=s.Matrix([[31,4,-31,-18],[-100,-13,100,58],[-9,-1,9,5],[336,43,-335,-195]])
assert T.det()==-1
F=T.inv()*J*T.T.inv()
assert F[0,0]==-4523390658618420908 and F[0,1]==2239380521691398176
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
P=-J[1:4,1:4]
assert all(P[:i,:i].det()>0 for i in (1,2,3))
Pinv=P.inv();v=Pinv*J[1:4,0]; beta=J[0,0]+(v.T*P*v)[0]
assert beta>0
J=[[int(z) for z in row] for row in J.tolist()]
def rat(z):return Q(int(z.p),int(z.q))
rows=[];total=0
for t in range(1001,1011):
    R=rat(beta)*t*t+2
    box=[]
    for i in (0,1):
        center=rat(v[i])*t
        r2=R*rat(Pinv[i,i])
        radius=isqrt(r2.numerator//r2.denominator)+3
        lo=floor(center)-radius-2; hi=ceil(center)+radius+2
        # exact proof that both ends extend beyond the whole projected ellipsoid
        assert lo<=center<=hi
        assert (center-lo)**2>=r2 and (hi-center)**2>=r2
        box.append((lo,hi))
    num=0;squares=0;nonnegative=0;roots=[]
    for b in range(box[0][0],box[0][1]+1):
        for c in range(box[1][0],box[1][1]+1):
            num+=1
            A=J[3][3]
            B=2*(J[0][3]*t+J[1][3]*b+J[2][3]*c)
            C=J[0][0]*t*t+2*J[0][1]*t*b+2*J[0][2]*t*c+J[1][1]*b*b+2*J[1][2]*b*c+J[2][2]*c*c+2
            disc=B*B-4*A*C
            if disc<0:continue
            nonnegative+=1
            droot=isqrt(disc)
            if droot*droot!=disc:continue
            squares+=1
            for numerator in (-B+droot,-B-droot):
                if numerator%(2*A)==0:
                    d=numerator//(2*A)
                    y=(t,b,c,d)
                    assert sum(y[i]*J[i][j]*y[j] for i in range(4) for j in range(4))==-2
                    roots.append(y)
    total+=num
    rows.append({'y0':t,'y1_box':box[0],'y2_box':box[1],
                 'pairs':num,'nonnegative_discriminants':nonnegative,
                 'square_discriminants':squares,'roots':roots})
assert total==1042860 and all(r['square_discriminants']==0 for r in rows)
print(json.dumps({'status':'PASS: exhaustive finite interval',
'positive_y0':[1001,1010],'negative_y0':'symmetric by y -> -y',
'coordinate_pairs':total,'exact_roots':0,'slices':rows,
'prior_RQT254_bound':'|y0|<=1000 excluded earlier; not rerun here',
'combined_necessary_height':'|y0|>=1011 (conditional on earlier certificate)',
'root18':'OPEN','roots19_20_21':'OPEN'},indent=2))
