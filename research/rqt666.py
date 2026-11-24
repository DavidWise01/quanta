#!/usr/bin/env python3
"""RQT-666: exact conditional Pell recurrence and 128-CF-convergent gate.
Run: python research/rqt666.py RQT-619-results.json [RQT-666-results.json]
"""
import json,math,sys,hashlib
from pathlib import Path
SOURCE_SHA='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def candidates(a):
 root=math.isqrt(a);assert root*root!=a
 m=0;d=1;b=root;p0,p1=0,1;q0,q1=1,0
 for i in range(128):
  p=b*p1+p0;q=b*q1+q0
  yield i,p,q,p*p-a*q*q
  p0,p1=p1,p;q0,q1=q1,q
  m=d*b-m;d=(a-m*m)//d;assert d>0;b=(root+m)//d
def main():
 src=Path(sys.argv[1]);raw=src.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 data=json.loads(raw);assert data['rqt']==619 and len(data['families'])==27
 rows=[];total={'convergents':0,'norm_plus_one':0,'norm_minus_one':0,'target_matches':0,'integer_seeds':0}
 for rec in data['families']:
  r0,r1,r2,r3,r4,r5=map(int,rec['R_coefficients_as_strings'])
  a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5;N=h*h-a*c
  assert r0 and a>0
  counts={'convergents':0,'norm_plus_one':0,'norm_minus_one':0,'target_matches':0,'integer_seeds':0}
  matches=[]
  for i,p,q,k in candidates(a):
   counts['convergents']+=1;assert k==p*p-a*q*q
   if k==1:
    counts['norm_plus_one']+=1
    z,y=2,3;zn=p*z+a*q*y;yn=q*z+p*y
    assert zn*zn-a*yn*yn==z*z-a*y*y
   if k==-1:counts['norm_minus_one']+=1
   if k==N:
    counts['target_matches']+=1
    recovered=[]
    for z in (p,-p):
     if (z-h)%a:continue
     t=(z-h)//a
     for y in (q,-q):
      numerator=-r1*t-r3+y
      if numerator%(2*r0):continue
      u=numerator//(2*r0)
      assert r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5==0
      counts['integer_seeds']+=1;recovered.append({'u':str(u),'t':str(t)})
    matches.append({'index':i,'p':str(p),'q':str(q),'recovered':recovered})
  for key in total:total[key]+=counts[key]
  rows.append({'canonical_id':rec['canonical_id'],'member_ids':rec['member_ids'],
   'a':str(a),'h':str(h),'N':str(N),'counts':counts,'target_matches':matches})
 assert total=={'convergents':3456,'norm_plus_one':0,'norm_minus_one':0,'target_matches':0,'integer_seeds':0}
 out={'rqt':666,'source_sha256':SOURCE_SHA,'total':total,'orbits':rows,
 'recurrence':{'precondition':'U²−aV²=1 and z²−ay²=N','z_prime':'U*z+a*V*y',
 'y_prime':'V*z+U*y','norm':'z_prime²−a*y_prime²=N',
 'additional_gate':'z≡h mod a, then original integer u and G(u,t)=0'},
 'new_all_scale_exclusions':0,'selected_excluded':82,'selected_unresolved':53,
 'root19':'OPEN','original_22d_wall':'NOT REPLAYED','scope':'Finite 128-term continued fraction prefix per orbit'}
 dst=Path(sys.argv[2] if len(sys.argv)>2 else 'RQT-666-results.json')
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-666:',total)
if __name__=='__main__':main()
