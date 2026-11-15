#!/usr/bin/env python3
"""RQT-389: unbounded coordinate-slice exclusions and p-adic contrast.
Input is the exact JSON emitted by RQT-388 or the archived RQT-388 result.
Usage:
  python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
  python research/rqt389-global-two-plane-exclusion.py /tmp/rqt388.json --out /tmp/rqt389.json
"""
import argparse,json
from pathlib import Path
import sympy as s

def nearest(n,d):
    assert d>0
    return (2*n+d)//(2*d) if n>=0 else -nearest(-n,d)

def reduced_binary(P):
    assert P.shape==(2,2) and P==P.T and P[0,0]>0 and P.det()>0
    dot=lambda x,y:int((x.T*P*y)[0])
    a=s.Matrix([1,0]);b=s.Matrix([0,1]);count=0
    while True:
        if dot(b,b)<dot(a,a):a,b=b,a
        coeff=nearest(dot(a,b),dot(a,a))
        if coeff==0:
            U=s.Matrix.hstack(a,b);T=U.T*P*U
            assert abs(U.det())==1
            assert 2*abs(int(T[0,1]))<=int(T[0,0])<=int(T[1,1])
            return {'transform':[[str(x) for x in row] for row in U.tolist()],
                 'minimum':int(T[0,0]),'minimum_bits':int(T[0,0]).bit_length(),
                 'gauss_iterations':count}
        b=b-coeff*a;count+=1
        if count>1000:raise RuntimeError('Gauss iteration limit')

def local_line(Q,power2=32,power3=20):
    T=Q/2
    a=int(T[0,0]);b=int(Q[0,2]);c=int(T[2,2])+1
    f=lambda x:a*x*x+b*x+c
    disc=b*b-4*a*c
    assert disc<0 and a<0 # No REAL root on the line (x,0,1).
    def lift(prime,exp):
        roots=[x for x in range(prime) if f(x)%prime==0]
        modulus=prime
        for k in range(2,exp+1):
            roots=[x+d*modulus for x in roots for d in range(prime)
                   if f(x+d*modulus)%(modulus*prime)==0]
            modulus*=prime
            assert roots
        return modulus,min(roots),len(roots)
    m2,x2,n2=lift(2,power2);m3,x3,n3=lift(3,power3)
    x=x2+m2*(((x3-x2)*pow(m2,-1,m3))%m3)
    assert f(x)%(m2*m3)==0 and f(x)!=0
    return {'line':'(x,0,1)','discriminant_sign':'negative',
      'discriminant_bits':abs(disc).bit_length(),'no_real_root':True,
      '2adic':{'modulus':str(m2),'exponent':power2,'witness':str(x2),'number_of_roots':n2},
      '3adic':{'modulus':str(m3),'exponent':power3,'witness':str(x3),'number_of_roots':n3},
      'simultaneous_CRT_x':str(x),
      'simultaneous_CRT_modulus':str(m2*m3),
      'exact_equation_value_is_zero':False}

def audit(data):
    raw=data.get('restricted_F4_Gram',data.get('restricted_Gram'))
    assert raw is not None
    Q=s.Matrix([[int(x) for x in row] for row in raw])
    assert Q==Q.T and all(int(Q[i,i])%2==0 for i in range(3))
    T=Q/2;certificates=[]
    for excluded_index,retained in ((0,[1,2]),(1,[0,2])):
        S=T.extract(retained,retained);P=-S
        assert P[0,0]>0 and P[1,1]>0 and P.det()>0
        result=reduced_binary(P)
        assert result['minimum']>1
        certificates.append({'forced_nonzero_coefficient_index':excluded_index,
          'slice_coordinate_indices':retained,
          'negative_definite':True,
          'minimum_abs_half_norm':str(result['minimum']),
          'minimum_abs_half_norm_bits':result['minimum_bits'],
          'gauss_transform':result['transform'],
          'gauss_iterations':result['gauss_iterations'],
          'global_conclusion':'No vector of norm -2 with this coefficient zero'})
    return {'RQT':389,'status':'PASS original rank-three kernel: two global slice exclusions',
      'original_kernel_rank':3,'root19_necessary':'first and second reduced coefficients both nonzero',
      'global_certificates':certificates,
      'local_not_global':local_line(Q),
      'root19':'OPEN','root20':'OPEN','root21':'conditional',
      'scope':'Exact unbounded exclusions for two coordinate planes, not the entire ternary lattice'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('kernel_json');p.add_argument('--out')
    args=p.parse_args();payload=json.loads(Path(args.kernel_json).read_text())
    result=audit(payload)
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
