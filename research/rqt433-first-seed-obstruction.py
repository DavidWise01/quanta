#!/usr/bin/env python3
"""RQT-433: exact fixed-pair obstruction from mod 13 and 23.
Run with RQT-401 full JSON: python research/rqt433-first-seed-obstruction.py RQT401.json
"""
import argparse,hashlib,itertools,json
from pathlib import Path
SHA="5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809"
def audit(data):
 Q=[[int(t) for t in row] for row in data["restricted_Gram"]]
 B=[[int(t) for t in row] for row in data["reduced_kernel_basis"]]
 F=[[int(t) for t in row] for row in data["original_F4"]]
 assert len(Q)==3 and all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 assert all(sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4))==Q[i][j] for i in range(3) for j in range(3))
 sha=hashlib.sha256(json.dumps([[str(t) for t in row] for row in Q],separators=(",",":")).encode()).hexdigest()
 assert sha==SHA
 A=[[t//2 for t in row] for row in Q]
 a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
 primes={}
 for p,target in ((13,11),(23,7)):
  assert f%p==(c+5*e)%p==0
  assert (-a-10*b-25*g)%p==target
  squares={v*v%p for v in range(p)}
  assert target not in squares
  bad=[]
  for x,y in itertools.product(range(p),repeat=2):
   L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y
   if L%p==0 and -M%p not in squares:
    bad.append((x,y))
    assert all((M+2*L*z+f*z*z+d*d)%p!=0
       for z,d in itertools.product(range(p),repeat=2))
  assert set(bad)=={(x,5*x%p) for x in range(1,p)}
  primes[str(p)]={"forbidden_pairs":len(bad),"nonresidue":target,
       "condition":f"x != 0 mod {p} and y == 5*x mod {p}"}
 mod=13*23
 bad13={(x,y) for x in range(mod) for y in range(mod) if x%13 and (y-5*x)%13==0}
 bad23={(x,y) for x in range(mod) for y in range(mod) if x%23 and (y-5*x)%23==0}
 assert len(bad13|bad23)==9802
 examples=[]
 for p,x,y in ((13,41,23),(23,140,79)):
  assert 177065*y<100000*x<178600*y
  assert x%p and (y-5*x)%p==0
  examples.append({"p":p,"x":x,"y":y,"inside_cone":True,"forbidden_all_z_d":True})
 return {"RQT":433,"status":"PASS unbounded fixed-pair exclusion",
   "Gram_SHA256":sha,"F4_backmap":True,"prime_results":primes,
   "excluded_pairs_mod299":9802,"total_pairs_mod299":89401,
   "cone_examples":examples,"rational_witness":"OPEN","root19":"OPEN",
   "root18_prefix":"UNVERIFIED","root20":"OPEN","root21":"conditional"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("full_rqt401_json");p.add_argument("--out")
 x=p.parse_args();r=audit(json.loads(Path(x.full_rqt401_json).read_text()))
 if x.out:Path(x.out).write_text(json.dumps(r,indent=2)+"\n")
 print(json.dumps(r,indent=2))
