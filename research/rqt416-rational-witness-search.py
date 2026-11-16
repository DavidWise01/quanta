#!/usr/bin/env python3
"""RQT-416 exact bounded rational witness sieve. Requires full RQT-401 JSON."""
import argparse,json,math
from pathlib import Path
def audit(source,B=100,maxden=31):
 Q=[[int(t) for t in row] for row in source['restricted_Gram']]
 assert len(Q)==3 and all(len(row)==3 for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
 assert all(t%2==0 for row in Q for t in row)
 A=[[t//2 for t in row] for row in Q]
 assert [[t%4 for t in row] for row in A]==[[1,0,1],[0,2,3],[1,3,3]]
 a,b,c=A[0];d,e=A[1][1:];f=A[2][2]
 mods=[64,63,65,11,13,17,19,23]
 residues={m:{n*n%m for n in range(m)} for m in mods}
 stats={'tested':0,'D_nonnegative':0,'passed_modular_squares':0,
        'exact_square':0,'integral_z':0}
 witnesses=[]
 for x in range(-B,B+1):
  for y in range(-B,B+1):
   if x==y==0 or (x%2==1 and y%2==0):continue
   L=c*x+e*y;C=a*x*x+2*b*x*y+d*y*y
   for den in range(1,maxden+1,2):
    stats['tested']+=1
    E=L*L-f*(C+den*den)
    if E<0:continue
    stats['D_nonnegative']+=1
    if any(E%m not in residues[m] for m in mods):continue
    stats['passed_modular_squares']+=1
    s=math.isqrt(E)
    if s*s!=E:continue
    stats['exact_square']+=1
    for sign in (-1,1):
     n=-L+sign*s
     if n%f:continue
     z=n//f;v=(x,y,z)
     assert sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))==-den*den
     if math.gcd(math.gcd(math.gcd(abs(x),abs(y)),abs(z)),den)!=1:continue
     stats['integral_z']+=1;witnesses.append({'w':list(map(str,v)),'d':den})
 rejected=[]
 for x,y,z,den in [(16,9,1,3),(23,13,6,5),(31,17,9,7)]:
  v=(x,y,z)
  norm=sum(A[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
  assert norm!=-den*den
  rejected.append({'w':[x,y,z],'den':den,'is_witness':False})
 return {'RQT':416,'status':'BOUNDED SEARCH: no witness',
  'bounds':{'abs_x':B,'abs_y':B,'odd_d_max':maxden},
  'search_counts':stats,'root_witnesses':witnesses,
  'invalid_initial_artwork_examples':rejected,
  'rational_existence':'Proven previously (RQT-414), explicit coordinates not constructed',
  'root19':'OPEN','root18_position':'UNVERIFIED',
  'scope':'No global nonexistence claim'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_rqt401_json')
 p.add_argument('--bound',type=int,default=100);p.add_argument('--max-den',type=int,default=31)
 p.add_argument('--out');args=p.parse_args()
 r=audit(json.loads(Path(args.full_rqt401_json).read_text()),args.bound,args.max_den)
 if args.out:Path(args.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
