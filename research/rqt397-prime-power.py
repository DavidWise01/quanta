#!/usr/bin/env python3
"""RQT-397: exact prime-power local lifting for the fixed RQT-388 lattice.
Requires full --out JSON from rqt388-exact-second-key.py, NOT summary.
"""
import argparse,json,math
from pathlib import Path

def normplus2(Q,v,m):
 x,y,z=v
 a,b,c=Q[0];d,e=Q[1][1:];f=Q[2][2]
 return (a*x*x+2*b*x*y+2*c*x*z+d*y*y+2*e*y*z+f*z*z+2)%m

def audit(src,primes=(2,3,5,7),depth=2,cap=49):
 raw=src.get("restricted_F4_Gram",src.get("restricted_Gram"))
 if raw is None:raise ValueError("Full restricted_Gram matrix required")
 Q=[[int(v) for v in row] for row in raw]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 result={"RQT":397,"status":"LOCAL TEST ONLY","root19":"OPEN","primes":{}}
 for p in primes:
  if p<2 or any(p%d==0 for d in range(2,math.isqrt(p)+1)):
   raise ValueError(f"{p} is not prime")
  residues=[(0,0,0)];previous=1;levels=[]
  for k in range(1,depth+1):
   mod=previous*p
   if mod>cap:break
   lifted=[]
   for x,y,z in residues:
    for i in range(p):
     for j in range(p):
      for h in range(p):
       v=(x+previous*i,y+previous*j,z+previous*h)
       if normplus2(Q,v,mod)==0:lifted.append(v)
   nonprimitive=sum(all(t%p==0 for t in v) for v in lifted)
   if k>=2:assert nonprimitive==0
   levels.append({"modulus":mod,"surviving_residue_triples":len(lifted),
                  "nonprimitive_residue_triples":nonprimitive})
   residues=lifted;previous=mod
   if not residues:break
  result["primes"][str(p)]=levels
 result["local_obstruction_found"]=any(levels and levels[-1]["surviving_residue_triples"]==0
                                    for levels in result["primes"].values())
 result["scope"]="A zero at any full prime-power level is a global obstruction. Survivors imply no root existence."
 return result

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("full_kernel_json")
 p.add_argument("--depth",type=int,default=2)
 p.add_argument("--cap",type=int,default=49)
 p.add_argument("--out")
 args=p.parse_args()
 result=audit(json.loads(Path(args.full_kernel_json).read_text()),depth=args.depth,cap=args.cap)
 if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
