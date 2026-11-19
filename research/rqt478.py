import json,hashlib,itertools,sys
from pathlib import Path
import sympy as s

def run(path):
 S=json.load(open(path)); Q=s.Matrix(S['restricted_Gram']); B=s.Matrix(S['reduced_kernel_basis']); F=s.Matrix(S['original_F4'])
 sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q.tolist()],separators=(',',':')).encode()).hexdigest()
 assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809' and B.T*F*B==Q and all(x%2==0 for x in Q)
 H=s.diag(Q/2,1); P=s.Matrix([[1,0,0,0],[0,s.Rational(1,3),0,0],[s.Rational(1,3),0,-s.Rational(1,3),0],[0,0,0,1]])
 K=P*H*P.T; assert all(x.q==1 for x in K) and abs(P.det())==s.Rational(1,9) and K.det()*81==H.det() and K.det()%3
 A=[[int(x) for x in r] for r in K.tolist()]; N=[[int(x) for x in r] for r in (3*P).tolist()]; hits=[]; tests=admissible=0;best=None
 for w in itertools.product(range(-9,10),repeat=3):
  v=(*w,1); n=sum(v[i]*A[i][j]*v[j] for i in range(4) for j in range(4)); X=[sum(v[i]*N[i][j] for i in range(4)) for j in range(4)];tests+=1
  if all(t%3==0 for t in X):
   admissible+=1
   if any(w) and (best is None or abs(n)<best):best=abs(n)
  if n==0:
   assert (s.Matrix(X).T*H*s.Matrix(X))[0]==0;hits.append(X)
 return dict(RQT=478,sha256=sha,det_before_bits=abs(int(H.det())).bit_length(),det_after_bits=abs(int(K.det())).bit_length(),det_ratio=81,old_mod3=H.applyfunc(lambda x:int(x)%3).tolist(),new_mod3=K.applyfunc(lambda x:int(x)%3).tolist(),P=[[str(x) for x in r] for r in P.tolist()],K=[[str(x) for x in r] for r in K.tolist()],tests=tests,integral_original=admissible,best_bits=best.bit_length(),hits=hits,root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
 out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2,default=int)+'\n');print({k:v for k,v in out.items() if k!='K'})
