#!/usr/bin/env python3
"""RQT-387: exact first-stage successor audit for RQT-386 integer root.
Run with --certificate RQT-386-Exact-Root-Candidate.json, or
--reconstruct research/rqt386-exact-null-and-root-candidate.py.
"""
import argparse,hashlib,json,math,subprocess,sys
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
I=s.eye(4)
assert H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
def m2(M):return M.applyfunc(lambda v:int(v)%2)
def rank2(M):
 rows=[[int(M[i,j])%2 for j in range(M.cols)] for i in range(M.rows)]
 k=0
 for j in range(M.cols):
  ix=next((i for i in range(k,len(rows)) if rows[i][j]),None)
  if ix is None:continue
  rows[k],rows[ix]=rows[ix],rows[k]
  for i in range(len(rows)):
   if i!=k and rows[i][j]:rows[i]=[a^b for a,b in zip(rows[i],rows[k])]
  k+=1
 return k
def check(c):
 u=s.Matrix([int(x) for x in c['original_null_u']])
 v=s.Matrix([int(x) for x in c['bezout_partner_v']])
 r=s.Matrix([int(x) for x in c.get('candidate_root_vector_r',c.get('root_candidate_r'))])
 assert math.gcd(*map(int,u))==1 and math.gcd(*map(int,F*u))==1
 assert (u.T*F*u)[0]==0 and (u.T*F*v)[0]==1
 q=int((v.T*F*v)[0])//2
 assert 2*q==(v.T*F*v)[0] and (1+q)*u-v==r
 assert (r.T*F*r)[0]==-2 and (r.T*H*r)[0]==1
 assert ''.join(str(int(x)%2) for x in r)=='0111'
 S=I+r*(r.T*F);D=I+H.inv()*F;E=S*D
 assert S*S==I and S.T*F*S==F and S.det()==-1
 assert D.det()==1 and D.T*F*D==F and E.T*F*E==F
 d,e=m2(D),m2(E)
 assert (D-I).rank()==4 and (E-I).rank()==3
 assert rank2(d-I)==2 and rank2(e-I)==1
 assert m2(d*d)!=I and m2(d*d*d)==I
 assert m2(e*e)==I and e!=I
 assert e==s.Matrix([[0,0,0,1],[0,1,0,0],[0,0,1,0],[1,0,0,0]])
 return {'RQT':387,'status':'PASS original first-stage reflection successor conditions',
 'candidate_SHA256':hashlib.sha256(','.join(str(x) for x in r).encode()).hexdigest(),
 'exact_root_norm':-2,'parity':'0111',
 'initial_rational_moving_rank':4,'after_candidate_rational_moving_rank':3,
 'initial_GF2_order':3,'after_candidate_GF2_order':2,
 'initial_GF2_moving_rank':2,'after_candidate_GF2_moving_rank':1,
 'after_candidate_GF2_matrix':[[int(v) for v in row] for row in e.tolist()],
 'eighteenth_stage':'FIRST-STAGE ACCEPTED; full 21-word not certified',
 'missing':['compatible root19','compatible root20','forced cofactor root21','full residual factorization']}
def main():
 p=argparse.ArgumentParser();p.add_argument('--certificate');p.add_argument('--reconstruct');a=p.parse_args()
 if a.certificate:
  with open(a.certificate) as f:c=json.load(f)
 elif a.reconstruct:
  out=subprocess.run([sys.executable,a.reconstruct],capture_output=True,text=True,check=True)
  c=json.loads(out.stdout)
 else:p.error('Provide --certificate <JSON> or --reconstruct <RQT-386 source>')
 print(json.dumps(check(c),indent=2))
if __name__=='__main__':main()
