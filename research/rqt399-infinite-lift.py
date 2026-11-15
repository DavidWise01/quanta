#!/usr/bin/env python3
"""RQT-399: exact regular p-adic lifts; input FULL RQT-388 --out JSON."""
import argparse,itertools,json,math
from pathlib import Path

def prime(p):
 return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))

def norm(Q,v):
 return 2+sum(Q[i][j]*v[i]*v[j] for i in range(3) for j in range(3))

def classify(Q,p):
 regular=[];alive=[];dead=[]
 for v in itertools.product(range(p),repeat=3):
  n=norm(Q,v)
  if n%p:continue
  g=[2*sum(Q[i][j]*v[j] for j in range(3))%p for i in range(3)]
  if any(g):regular.append(v)
  elif n%(p*p)==0:alive.append(v)
  else:dead.append(v)
 return {'mod_p':len(regular)+len(alive)+len(dead),'regular':len(regular),
         'singular_alive':len(alive),'singular_dead':len(dead),
         'mod_p2':len(regular)*p*p+len(alive)*p**3,
         'regular_witness':regular[0] if regular else None}

def construct(Q,p,v,depth):
 v=list(v);assert norm(Q,v)%p==0
 g=[2*sum(Q[i][j]*v[j] for j in range(3))%p for i in range(3)]
 j=next(i for i,t in enumerate(g) if t)
 out=[{'power':1,'vector':v[:]}];mod=p
 for k in range(1,depth):
  defect=(norm(Q,v)//mod)%p
  t=(-defect*pow(g[j],-1,p))%p
  v[j]+=mod*t;mod*=p
  assert norm(Q,v)%mod==0
  out.append({'power':k+1,'vector':v[:]})
 return out

def audit(Q,primes=(2,3,5,7),depth=6):
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 rows=[]
 for p in primes:
  assert prime(p)
  c=classify(Q,p);c['p']=p
  c['regular_infinite_lift_certified']=bool(c['regular'])
  c['constructive_chain']=construct(Q,p,c['regular_witness'],depth) if c['regular'] else []
  rows.append(c)
 return {'RQT':399,'status':'LOCAL P-ADIC TEST','results':rows,
         'global_integer_root':'UNDECIDED',
         'scope':'Regular p-adic solutions are necessary local data, not global integer witnesses'}

if __name__=='__main__':
 pa=argparse.ArgumentParser()
 pa.add_argument('full_kernel_json');pa.add_argument('--depth',type=int,default=6);pa.add_argument('--out')
 args=pa.parse_args()
 src=json.loads(Path(args.full_kernel_json).read_text())
 raw=src.get('restricted_F4_Gram',src.get('restricted_Gram'))
 if raw is None:raise ValueError('Need full RQT-388 reduced Gram JSON, not summary')
 result=audit([[int(n) for n in row] for row in raw],depth=args.depth)
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
