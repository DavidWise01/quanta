#!/usr/bin/env python3
"""RQT-388: exact LLL on saturated successor rank-three Wall kernel.
Requires research/rqt386-exact-null-and-root-candidate.py and
research/rqt377-exact-wall-kernel-ladder.py, both in this repository.
Usage: python research/rqt388-exact-second-key.py --bound 30
"""
import argparse,itertools,importlib.util,json,subprocess,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as s

def load_module(path):
    spec=importlib.util.spec_from_file_location("rqt_ladder",str(path))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def nearest(q):
    return (2*q.numerator+q.denominator)//(2*q.denominator)

def gram_schmidt(rows):
    orth=[];norm=[];mus=[]
    for x in rows:
        w=[Fraction(a) for a in x];mu=[]
        for j,y in enumerate(orth):
            c=sum(Fraction(a)*b for a,b in zip(x,y))/norm[j]
            w=[a-c*b for a,b in zip(w,y)];mu.append(c)
        orth.append(w);norm.append(sum(a*a for a in w));mus.append(mu)
    return mus,norm

def exact_lll(rows):
    b=[v[:] for v in rows];n=len(b)
    u=[[int(i==j) for j in range(n)] for i in range(n)]
    k=1;loops=0
    while k<n:
        mu,ns=gram_schmidt(b)
        for j in range(k-1,-1,-1):
            c=nearest(mu[k][j])
            if c:
                b[k]=[a-c*z for a,z in zip(b[k],b[j])]
                u[k]=[a-c*z for a,z in zip(u[k],u[j])]
                mu,ns=gram_schmidt(b)
        if ns[k]>=(Fraction(3,4)-mu[k][k-1]**2)*ns[k-1]:
            k+=1
        else:
            b[k],b[k-1]=b[k-1],b[k]
            u[k],u[k-1]=u[k-1],u[k]
            k=max(k-1,1)
        loops+=1
        if loops>10000:raise RuntimeError("exact LLL failed iteration ceiling")
    mu,ns=gram_schmidt(b)
    assert abs(s.Matrix(u).det())==1
    assert all(abs(mu[i][j])<=Fraction(1,2) for i in range(n) for j in range(i))
    assert all(ns[k]>=(Fraction(3,4)-mu[k][k-1]**2)*ns[k-1] for k in range(1,n))
    return s.Matrix(b),s.Matrix(u),loops

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--bound',type=int,default=30)
    p.add_argument('--out',default=None)
    args=p.parse_args();assert 1<=args.bound<=100
    here=Path(__file__).resolve().parent
    prior=subprocess.run([sys.executable,str(here/'rqt386-exact-null-and-root-candidate.py')],
                          check=True,capture_output=True,text=True)
    certificate=json.loads(prior.stdout)
    r=[int(x) for x in certificate['root_candidate_r']]
    m=load_module(here/'rqt377-exact-wall-kernel-ladder.py')
    F,H=m.F,m.H
    B,Q0,_=m.kernel_ladder([r])
    assert B.shape==(4,3) and (s.Matrix(r).T*H.T*B)==s.zeros(1,3)
    assert (s.Matrix(r).T*F*s.Matrix(r))[0]==-2
    L,U,loops=exact_lll(B.T.tolist())
    assert L==U*B.T and abs(U.det())==1
    R=L.T;Q=R.T*F*R
    assert Q==U*Q0*U.T and Q.det()==Q0.det()
    assert s.Matrix(r).T*H.T*R==s.zeros(1,3)
    d1=int(Q[0,0]);d2=int(Q[:2,:2].det());d3=int(Q.det())
    assert d1*d2*d3!=0
    pivots=(Fraction(d1),Fraction(d2,d1),Fraction(d3,d2))
    primes=(8,9,5,7,11,13,17,19,23,29,31)
    forms={m:[[int(Q[i,j])%m for j in range(3)] for i in range(3)] for m in primes}
    nclass={}
    for mod in (8,9,5,7):
        nclass[str(mod)]=sum(
            (sum(forms[mod][i][j]*z[i]*z[j] for i in range(3) for j in range(3))+2)%mod==0
            for z in itertools.product(range(mod),repeat=3))
    count=Counter();candidates=[]
    for z in itertools.product(range(-args.bound,args.bound+1),repeat=3):
        if z==(0,0,0):continue
        count['tested']+=1
        if any((sum(forms[mod][i][j]*z[i]*z[j] for i in range(3) for j in range(3))+2)%mod
               for mod in primes):
            count['modular_rejection']+=1;continue
        count['modular_survivor']+=1
        if sum(int(Q[i,j])*z[i]*z[j] for i in range(3) for j in range(3))==-2:
            v=R*s.Matrix(z)
            assert (v.T*F*v)[0]==-2 and (v.T*H*s.Matrix(r))[0]==0
            candidates.append([str(int(x)) for x in v])
    result={'rqt':388,'status':'PASS exact saturated successor kernel',
       'rank':3,'LLL_iterations':loops,'basis_transform_det':int(U.det()),
       'old_coordinate_max_bits':max(abs(int(x)).bit_length() for x in B),
       'new_coordinate_max_bits':max(abs(int(x)).bit_length() for x in R),
       'restricted_form_signature':[sum(x>0 for x in pivots),sum(x<0 for x in pivots)],
       'restricted_determinant_bits':abs(d3).bit_length(),
       'modular_classes':nclass,'bounded_coefficients':args.bound,
       'counts':dict(count),'root19_candidates':candidates,
       'root19_status':'OPEN' if not candidates else 'NORM/WALL WITNESS REQUIRES FULL CHECK',
       'basis_unimodular_matrix':[[str(x) for x in row] for row in U.tolist()],
       'reduced_kernel_basis':[[str(x) for x in row] for row in R.tolist()],
       'restricted_Gram':[[str(x) for x in row] for row in Q.tolist()],
       'scope':'Finite coefficient box only; not a proof of root19 nonexistence'}
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in
          ('basis_unimodular_matrix','reduced_kernel_basis','restricted_Gram')},indent=2))
if __name__=='__main__':main()
