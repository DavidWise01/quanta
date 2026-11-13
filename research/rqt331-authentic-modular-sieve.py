#!/usr/bin/env python3
"""RQT-331: complete norm -2 residue lifts in the authentic RQT-242 lattice.
Sources: DavidWise01/stoicheion research/rqt/rqt242_mod4_audit.py
and RQT-254-unimodular-second-height.md. No integral root claimed.
"""
import json
from itertools import product
from collections import Counter
import sympy as s
T=s.Matrix([[31,4,-31,-18],[-100,-13,100,58],[-9,-1,9,5],[336,43,-335,-195]])
J=s.Matrix([[9208923577999086,-2890579252927294,-1029318396906446,276003667781247],[-2890579252927294,-136287821825501156,-29512715198402862,11299357575842588],[-1029318396906446,-29512715198402862,-1127313935375881122,-146309554088173376],[276003667781247,11299357575842588,-146309554088173376,-5868287405277328266]])
F=T.inv()*J*T.T.inv()
assert T.det()==-1 and T*F*T.T==J
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
assert F[0,0]==-4523390658618420908 and F[0,1]==2239380521691398176
assert T.T.inv()[0,:]==s.Matrix([[-24,-22,-17,-17]])
allowed={(0,1,1,1):'0111',(1,0,0,1):'1001',(1,1,1,0):'1110'}
TM=[[int(T[j,i]) for j in range(4)] for i in range(4)]
JM=[[int(J[i,j]) for j in range(4)] for i in range(4)]
def parity(y):
    return tuple(sum(TM[i][j]*y[j] for j in range(4))%2 for i in range(4))
def normres(y,mod):
    return sum(y[i]*JM[i][j]*y[j] for i in range(4) for j in range(4))%mod
res=[y for y in product(range(2),repeat=4) if parity(y) in allowed and normres(y,4)==2]
assert len(res)==3
stages=[]
m=2
while True:
    counts=Counter(allowed[parity(y)] for y in res)
    expected=3*m**3//8
    assert len(res)==expected and all(counts[p]==expected//3 for p in ('0111','1001','1110'))
    stages.append({'coordinate_modulus':m,'norm_modulus':2*m,
                   'eligible_residues':len(res),'per_parity':expected//3})
    if m==64:break
    new=[]
    for y in res:
        for bits in product((0,1),repeat=4):
            z=tuple(y[i]+m*bits[i] for i in range(4))
            if normres(z,4*m)==(4*m-2):new.append(z)
    res=new;m*=2
print(json.dumps({'status':'PASS exact authentic modular sieve',
 'frozen_source':'DavidWise01/stoicheion RQT-242 + RQT-254',
 'root18_status':'OPEN; no exact integral root claimed',
 'root19_20_21_status':'OPEN',
 'stages':stages,'last_stage_residue_examples':sorted(res)[:3],
 'prior_RQT254_height_exclusion':'|y0|<=1000 excluded for norm -2; source result, not rerun',
 'source_original_y0':'-24*x0-22*x1-17*x2-17*x3'},indent=2))
