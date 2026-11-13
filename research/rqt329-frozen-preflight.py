#!/usr/bin/env python3
"""RQT-329 original-lattice preflight. No frozen matrices are invented.
Usage: python research/rqt329-frozen-preflight.py --demo
       python research/rqt329-frozen-preflight.py --input original.json
JSON keys: F4 (4x4 integral), X4 (4x4 integral), source (provenance).
"""
import argparse, json, hashlib
from pathlib import Path
from itertools import product
import sympy as s
F_DEMO=[[-3,1,0,1],[1,-2,0,0],[0,0,1,0],[1,0,0,-1]]
X_DEMO=[[0,-1,0,0],[1,-1,0,0],[0,0,-1,0],[1,-1,0,-1]]

def inertia(A):
    A=s.Matrix(A); plus=minus=zero=0
    while A.rows:
        n=A.rows
        pivot=next((i for i in range(n) if A[i,i]),None)
        if pivot is None:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n) if A[i,j]),None)
            if pair is None: zero+=n;break
            i,j=pair
            P=s.eye(n);P[j,i]=1
            A=P.T*A*P
            pivot=i
        ix=[pivot]+[i for i in range(n) if i!=pivot]
        A=A.extract(ix,ix)
        a=A[0,0]
        if a>0:plus+=1
        else:minus+=1
        A=A[1:,1:]-A[1:,0]*A[0,1:]/a
    return [plus,minus,zero]

def order2(X):
    Y=s.eye(4)
    for n in range(1,33):
        Y=(Y*X).applyfunc(lambda t:int(t)%2)
        if Y==s.eye(4):return n
    return None

def positive_reference(F):
    for h in range(1,4):
        for coords in product(range(-h,h+1),repeat=4):
            if max(map(abs,coords))!=h:continue
            v=s.Matrix(coords)
            if (v.T*F*v)[0]>0:return v
    return None

def evaluate(d,bridge=False):
    F=s.Matrix(d['F4']);X=s.Matrix(d['X4']);I=s.eye(4)
    if F.shape!=(4,4) or X.shape!=(4,4):raise ValueError('4x4 matrices required')
    if any(t.q!=1 for t in list(F)+list(X)):raise ValueError('integer matrices required')
    if F!=F.T or F.det()==0 or X.T*F*X!=F:raise ValueError('invalid Gram/isometry input')
    sig=inertia(F)
    out={'status':'bridge-demo-only' if bridge else 'original-input-preflight',
      'frozen_roots_18_to_21':'OPEN','source':d.get('source'),
      'gram_determinant':str(F.det()),'signature':sig,
      'moving_rank':int((X-I).rank()),'binary_order':order2(X),
      'orientation':'not_applicable'}
    if sig[0]==1:
        e=positive_reference(F)
        if e is not None:
            val=(e.T*F*X*e)[0]
            if val==0:raise AssertionError('Lorentzian positive pair not zero')
            out['orientation']='reversing' if val<0 else 'preserving'
            out['orientation_witness']={'e':list(map(int,e)),'pairing':str(val)}
            out['negative_reflections']='impossible (any count)' if val<0 else 'not ruled out'
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--demo',action='store_true')
    g.add_argument('--input',type=Path)
    a=ap.parse_args()
    if a.demo:d={'F4':F_DEMO,'X4':X_DEMO,'source':'constructed bridge; NOT frozen RQT-256'}
    else:
        raw=a.input.read_bytes();d=json.loads(raw)
        if not d.get('source'):raise ValueError('original input needs provenance in source')
    result=evaluate(d,a.demo)
    if not a.demo:result['source_sha256']=hashlib.sha256(raw).hexdigest()
    print(json.dumps(result,indent=2))
