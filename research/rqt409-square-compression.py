#!/usr/bin/env python3
"""RQT-409: exact square compression, full RQT-401 Gram required."""
import argparse,json,math
from pathlib import Path
def audit(src):
 q=[[int(x) for x in row] for row in src['restricted_Gram']]
 assert len(q)==3 and all(len(row)==3 for row in q)
 assert all(q[i][j]==q[j][i] for i in range(3) for j in range(3))
 assert all(v%2==0 for row in q for v in row)
 h=[[v//2 for v in row] for row in q]
 a,b,c=h[0];d,e=h[1][1:];f=h[2][2]
 assert f%2==1
 # A-norm is -1: f z²+2(cx+ey)z+(ax²+2bxy+dy²+1)=0
 U=c*c-f*a;V=2*(c*e-f*b);W=e*e-f*d;T=-f
 assert math.gcd(U,math.gcd(V,math.gcd(W,T)))==1
 assert [z%16 for z in (U,V,W,T)]==[10,14,3,9]
 rows=[]
 for k in range(2,9):
  m=1<<k;squares={n*n%m for n in range(m)}
  valid=sum((U*x*x+V*x*y+W*y*y+T)%m in squares
            for x in range(m) for y in range(m))
  rows.append({'modulus':m,'admissible_xy_pairs':valid})
 assert [r['admissible_xy_pairs'] for r in rows]==[12,40,96,320,1024,3840,14336]
 parity={f'{x}{y}':(U*x*x+V*x*y+W*y*y+T)%4 for x in (0,1) for y in (0,1)}
 assert parity=={'00':1,'01':0,'10':3,'11':0}
 return {'RQT':409,'status':'PASS exact quadratic-discriminant compression',
  'identity':'D=4E', 'E_mod16_coefficients':[10,14,3,9],
  'E_parity_mod4':parity,'levels':rows,
  'proof':'f=(Q/2)[2,2] odd, so z exists mod 2^k iff E is a square mod 2^k',
  'root19':'OPEN','root18_predecessor':'UNVERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('full_kernel_json');p.add_argument('--out')
 a=p.parse_args();r=audit(json.loads(Path(a.full_kernel_json).read_text()))
 if a.out:Path(a.out).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
