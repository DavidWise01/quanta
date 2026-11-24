#!/usr/bin/env python3
"""RQT-665 — exact Pell residuals, normalized nearest squares and off-window CF probes.
Usage: python rqt665.py RQT-619-results.json [output.json] [bound=100000].
Python standard library only. Rank normalized gaps by integer cross products.
"""
import sys,json,hashlib,math
from functools import cmp_to_key
from pathlib import Path
SHA='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def denominators(a):
 root=math.isqrt(a)
 if root*root==a:return []
 m=0;d=1;v=root;q0,q1=1,0;out=[]
 for _ in range(12):
  q=v*q1+q0;out.append(q);q0,q1=q1,q
  m=d*v-m;d=(a-m*m)//d;v=(root+m)//d
 return out
def compare(v,w):
 diff=v['gap']*w['spacing']-w['gap']*v['spacing']
 return (-1 if diff<0 else 1 if diff>0 else 0)
def main():
 raw=Path(sys.argv[1]).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
 base=json.loads(raw);assert base['rqt']==619 and len(base['families'])==27
 B=int(sys.argv[3]) if len(sys.argv)>3 else 100000
 rows=[];nonnegative=tests=outside=out_squares=0;seeds=0;squares=0
 for record in base['families']:
  r0,r1,r2,r3,r4,r5=map(int,record['R_coefficients_as_strings'])
  a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5;N=h*h-a*c
  assert a>0 and r0!=0
  def observe(t):
   F=(a*t+2*h)*t+c;z=a*t+h
   assert z*z-a*F==N
   if F<0:return None
   s=math.isqrt(F);g0=F-s*s;g1=(s+1)*(s+1)-F
   y=s if g0<=g1 else s+1;gap=min(g0,g1)
   assert z*z-a*y*y-N==a*(F-y*y)
   return {'t':t,'gap':gap,'spacing':2*s+1,'y':y,'square':gap==0}
  best=[];nn=ns=0
  for t in range(-B,B+1):
   tests+=1;x=observe(t)
   if x is None:continue
   nn+=1;nonnegative+=1
   if x['square']:
    ns+=1;squares+=1
    for sign in (-1,1):
     k=-(r1*t+r3)+sign*x['y']
     if k%(2*r0)==0:
      u=k//(2*r0)
      assert r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5==0
      seeds+=1
   best.append(x)
   best.sort(key=cmp_to_key(compare))
   if len(best)>5:best.pop()
  extra=set(sign*q+step for q in denominators(a) for sign in (-1,1) for step in (-1,0,1) if abs(sign*q+step)>B)
  outside+=len(extra);exsq=0
  for t in sorted(extra):
   x=observe(t)
   if x is not None and x['square']:
    exsq+=1;out_squares+=1
    for sign in (-1,1):
     k=-(r1*t+r3)+sign*x['y']
     if k%(2*r0)==0:
      u=k//(2*r0)
      assert r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5==0
      seeds+=1
  rows.append({'canonical_id':record['canonical_id'],'nonnegative':nn,'exact_squares':ns,
   'best_normalized':[{'t':x['t'],'gap':str(x['gap']),'spacing':str(x['spacing'])} for x in best],
   'additional_off_window_probes':len(extra),'extra_exact_squares':exsq})
 assert tests==27*(2*B+1)
 if B==100000:assert (tests,nonnegative,squares,seeds,outside,out_squares)==(5400027,5398223,0,0,276,0)
 out={'rqt':665,'source_sha256':SHA,'bounded_t':B,'bounded_checks':tests,'nonnegative_F':nonnegative,
 'bounded_squares':squares,'additional_nonexhaustive_probes':outside,'extra_squares':out_squares,
 'integer_seeds':seeds,'orbits':rows,'new_full_family_exclusions':0,'selected_excluded':82,
 'selected_unresolved':53,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
 dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-665-results.json')
 dst.write_text(json.dumps(out,indent=2)+'\n')
 print('PASS RQT-665',tests,'exact checks;',outside,'off-window probes;',seeds,'seeds')
if __name__=='__main__':main()
