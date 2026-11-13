#!/usr/bin/env python3
"""RQT-339 — exhaustive authentic F4 joint-wedge search, x2=5001..5010.
Checks norms 0 and -2 with exact rational Schur bounds and integer discriminants.
Previously certified RQT-338 wedge and RQT-333 root y0-height are prerequisites.
No exact root18 claim.
"""
import json
from math import isqrt
from fractions import Fraction as Q
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
U=s.Matrix([[0,0,1,0],[-24,-22,-17,-17],[1,0,0,0],[0,-13,0,-10]])
assert U.det()==1 and F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
J=U.inv().T*F*U.inv();P=-J[2:,2:];V=P.inv()*J[2:,:2];K=J[:2,:2]+J[:2,2:]*P.inv()*J[2:,:2]
assert P[0,0]>0 and P.det()>0 and K.det()<0
rat=lambda a:Q(int(a.p),int(a.q))
a,b,c=[rat(P[i,j]) for i,j in ((0,0),(0,1),(1,1))]
alpha=a-b*b/c
v00,v01,v10,v11=[rat(V[i,j]) for i,j in ((0,0),(0,1),(1,0),(1,1))]
k00,k01,k11=[rat(K[i,j]) for i,j in ((0,0),(0,1),(1,1))]
assert alpha>0 and c>0
J0=[[int(z) for z in row] for row in J.tolist()]
def box(center,r2):
    assert r2>=0
    radius=isqrt(r2.numerator//r2.denominator)+2
    low=center.numerator//center.denominator-radius-1
    high=-(-center.numerator//center.denominator)+radius+1
    assert (center-low)**2>=r2 and (high-center)**2>=r2
    return low,high
results=[]
for t in range(5001,5011):
    row={'x2':t}
    for target in (0,-2):
        pairs=nonneg=squares=0;roots=[];ys=0
        y_min=-(63*t//250+2)
        y_max=-(2*t//125-2)
        for y in range(y_min,y_max+1):
            if not (125*(-y)>2*t and 250*(-y)<63*t):continue
            if target==-2 and -y<1021:continue
            R=k00*t*t+2*k01*t*y+k11*y*y-target
            if R<0:continue
            ys+=1
            center0=v00*t+v01*y
            center1=v10*t+v11*y
            lo,hi=box(center0,R/alpha)
            for z0 in range(lo,hi+1):
                d0=Q(z0)-center0
                remain=R-alpha*d0*d0
                if remain<0:continue
                low,high=box(center1-b/c*d0,remain/c)
                for z1 in range(low,high+1):
                    pairs+=1
                    w=[t,y,z0]
                    A=J0[3][3]
                    B=2*sum(w[i]*J0[i][3] for i in range(3))
                    C=sum(w[i]*J0[i][j]*w[j] for i in range(3) for j in range(3))-target
                    disc=B*B-4*A*C
                    if disc<0:continue
                    nonneg+=1
                    d=isqrt(disc)
                    if d*d!=disc:continue
                    squares+=1
                    for num in {-B+d,-B-d}:
                        if num%(2*A):continue
                        z2=num//(2*A)
                        z=s.Matrix([t,y,z0,z2])
                        assert (z.T*J*z)[0]==target
                        x=U.inv()*z
                        assert (x.T*F*x)[0]==target
                        roots.append({'z':list(map(int,z)),'x':list(map(int,x))})
        row[str(target)]={'joint_y0_values':ys,'coordinate_pairs':pairs,
            'nonnegative_discriminants':nonneg,'square_discriminants':squares,'roots':roots}
    results.append(row)
assert sum(x['0']['coordinate_pairs'] for x in results)==1669992
assert sum(x['-2']['coordinate_pairs'] for x in results)==238128
assert not any(x[str(q)]['roots'] or x[str(q)]['square_discriminants'] for x in results for q in (0,-2))
print(json.dumps({'status':'PASS exhaustive finite wedge','source':'authentic stoicheion F4',
 'x2_positive':[5001,5010],'negative_by_symmetry':True,'results':results,
 'total_norm0_pairs':1669992,'total_normminus2_pairs':238128,
 'roots18_to21':'OPEN','combined_x2_height':'abs(x2)>=5011 (assuming earlier certificates)'},indent=2))
