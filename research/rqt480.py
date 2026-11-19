import json,hashlib,math,sys
from pathlib import Path
from sympy import Matrix,diag,Rational,primerange,isprime

def run(path):
 S=json.load(open(path));Q=Matrix(S['restricted_Gram']);B=Matrix(S['reduced_kernel_basis']);F=Matrix(S['original_F4']);sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q.tolist()],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809' and B.T*F*B==Q and all(x%2==0 for x in Q)
 H=diag(Q/2,1);P=Matrix([[1,0,0,0],[0,Rational(1,3),0,0],[Rational(1,3),0,-Rational(1,3),0],[0,0,0,1]]);K=P*H*P.T;assert all(x.q==1 for x in K) and K.det()*81==H.det()
 n=abs(int(K.det()));co=n;factors=[];count=0
 for p in primerange(2,5000001):
  count+=1;k=0
  while co%p==0:co//=p;k+=1
  if k:factors.append([p,k])
 assert math.prod(p**k for p,k in factors)*co==n
 t=math.isqrt(co);square=t*t==co
 cert=next((p,n%p) for p in primerange(3,1000) if pow(n%p,(p-1)//2,p)==p-1)
 return dict(RQT=480,sha256=sha,prime_limit=5000000,primes_screened=count,factors=factors,cofactor=str(co),cofactor_bits=co.bit_length(),cofactor_square=square,cofactor_probable_prime=bool(isprime(co)),det_bits=n.bit_length(),det_nonsquare_certificate=list(cert),witt_index_upper_bound=1,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='cofactor'})
