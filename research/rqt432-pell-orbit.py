#!/usr/bin/env python3
"""RQT-432: exact Pell-unit orbit theorem; needs a first valid seed.
Usage: python research/rqt432-pell-orbit.py [--full-gram-json FILE]
       [--candidate '[x,y,s,d]' --unit '[u,v]' --period N]
"""
import argparse,json,math
from pathlib import Path
def mul(a,b,D):return (a[0]*b[0]+D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def power(a,n,D):
 out=(1,0)
 while n:
  if n&1:out=mul(out,a,D)
  a=mul(a,a,D);n//=2
 return out
def orbit(A,x,y,s,d,unit,period,steps=3):
 a,b,c=A[0];g,e=A[1][1:];f=A[2][2];D=-f
 assert D>0 and math.isqrt(D)**2!=D
 L=c*x+e*y;M=a*x*x+2*b*x*y+g*y*y;E0=L*L-f*M
 u,v=unit
 assert u>1 and v>0 and u*u-D*v*v==1
 assert d!=0 and s*s-D*d*d==E0 and (s-L)%D==0
 step=power(unit,period,D)
 assert step[0]%(2*D)==1 and step[1]%(2*D)==0
 rows=[];cur=(s,d)
 for k in range(steps+1):
  sk,dk=cur
  assert sk*sk-D*dk*dk==E0 and (sk-L)%D==0
  z=(sk-L)//f
  q=a*x*x+2*b*x*y+2*c*x*z+g*y*y+2*e*y*z+f*z*z
  assert q==-dk*dk and dk%2==d%2
  rows.append({'generation':k,'s':str(sk),'d':str(dk),'z':str(z),'primitive':math.gcd(x,y,z,dk)==1})
  cur=mul(cur,step,D)
 return {'D':str(D),'unit':list(unit),'unit_power':list(step),'period':period,'orbit':rows}
def run(data=None,candidate=None,unit=None,period=None):
 A0=[[1,0,0],[0,1,0],[0,0,-2]]
 test=orbit(A0,1,0,-2,1,(3,2),2)
 assert [(v['s'],v['d'],v['z']) for v in test['orbit']]==[
  ('-2','1','1'),('-10','-7','5'),('-338','-239','169'),('-11482','-8119','5741')]
 try:orbit(A0,1,0,-1,1,(3,2),2);raise RuntimeError('invalid seed accepted')
 except AssertionError:pass
 out={'RQT':432,'status':'PASS synthetic Pell-unit orbit and invalid-seed rejection',
 'original_first_seed':'NOT CONSTRUCTED','root19':'OPEN',
 'theorem':'A Pell unit power equal to (1,0) modulo 2D preserves s congruent L modulo D and odd d, so exact integral z and Pell norm persist for a verified seed.',
 'synthetic_control':test,'scope':'Conditional; no original-lattice seed or unit computed'}
 if data is not None:
  Q=[[int(t) for t in row] for row in data['restricted_Gram']]
  assert len(Q)==3 and all(len(row)==3 for row in Q)
  assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
  assert all(t%2==0 for row in Q for t in row)
  A=[[t//2 for t in row] for row in Q];D=-A[2][2]
  assert D.bit_length()==1352 and math.isqrt(D)**2!=D
  out['actual_D_bits']=1352
  if candidate is not None:
   if unit is None or period is None:raise ValueError('unit and verified period required')
   out['candidate_orbit']=orbit(A,*candidate,unit,period)
   out['note']='Each descendant still requires primitive and original F4 checks'
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--full-gram-json');p.add_argument('--candidate')
 p.add_argument('--unit');p.add_argument('--period',type=int);p.add_argument('--out')
 a=p.parse_args()
 result=run(json.loads(Path(a.full_gram_json).read_text()) if a.full_gram_json else None,
 json.loads(a.candidate) if a.candidate else None,json.loads(a.unit) if a.unit else None,a.period)
 if a.out:Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
