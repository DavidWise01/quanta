#!/usr/bin/env python3
"""RQT-664 exact near-square census + contextual sqrt(a) continued fractions.
python rqt664.py RQT-619-results.json [results.json] [bound=100000].
Python standard library; no floating-point and no all-scale claims.
"""
import sys,json,math,hashlib,heapq
from pathlib import Path
EXPECTED='97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021'
def convergents(a,limit=12):
 if a<=0:return []
 root=math.isqrt(a)
 if root*root==a:return [{'p':str(root),'q':'1','residual':'0','exact':True}]
 m=0;d=1;x=root;pm2,pm1=0,1;qm2,qm1=1,0;rows=[]
 for j in range(limit):
  p=x*pm1+pm2;q=x*qm1+qm2
  rows.append({'index':j,'p':str(p),'q':str(q),'pell_residual':str(p*p-a*q*q)})
  pm2,pm1=pm1,p;qm2,qm1=qm1,q
  m=d*x-m;d=(a-m*m)//d
  assert d>0 and (a-m*m)%d==0
  x=(root+m)//d
 return rows
def main():
 src=Path(sys.argv[1]);raw=src.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
 d=json.loads(raw);assert d['rqt']==619 and len(d['families'])==27
 dst=Path(sys.argv[2]) if len(sys.argv)>2 else Path('RQT-664-results.json')
 bound=int(sys.argv[3]) if len(sys.argv)>3 else 100000
 assert 1<=bound<=1000000
 summary=[];total_positive=total_squares=0;solutions=[]
 for item in d['families']:
  rid=item['canonical_id'];r0,r1,r2,r3,r4,r5=map(int,item['R_coefficients_as_strings'])
  a=r1*r1-4*r0*r2;h=r1*r3-2*r0*r4;c=r3*r3-4*r0*r5
  best=[];positive=squares=integral=0
  for t in range(-bound,bound+1):
   F=(a*t+2*h)*t+c
   if F<0:continue
   positive+=1
   low=math.isqrt(F)
   lowgap=F-low*low;upgap=(low+1)*(low+1)-F
   y=low if lowgap<=upgap else low+1
   gap=min(lowgap,upgap)
   ranking=(gap,abs(t),t)
   entry={'t':t,'nearest_y':str(y),'absolute_square_gap':str(gap),
    'relative_gap_numerator':str(gap),'relative_gap_denominator':str(2*low+1),
    'F':str(F),'is_exact_square':gap==0,
    'coordinate_divisible':((-r1*t-r3+y)%(2*r0)==0 or (-r1*t-r3-y)%(2*r0)==0)}
   if len(best)<5:heapq.heappush(best,(-gap,-abs(t),-t,entry))
   elif ranking<(-best[0][0],-best[0][1],-best[0][2]):
    heapq.heapreplace(best,(-gap,-abs(t),-t,entry))
   if gap==0:
    squares+=1
    for sign in (-1,1):
     z=-r1*t-r3+sign*low
     if z%(2*r0):continue
     u=z//(2*r0)
     assert r0*u*u+r1*u*t+r2*t*t+r3*u+r4*t+r5==0
     integral+=1;solutions.append({'orbit':rid,'u':str(u),'t':t,'sign':sign})
  top=[v[-1] for v in sorted(best,key=lambda z:(-z[0],-z[1],-z[2]))]
  assert len(top)==5
  summary.append({'canonical_id':rid,'member_ids':item['member_ids'],
   'search_parameters':2*bound+1,'F_nonnegative':positive,'exact_square_count':squares,
   'recovered_integer_coordinate_count':integral,'leading_coefficient_a':str(a),
   'sqrt_a_continued_fraction_convergents':convergents(a),
   'five_smallest_absolute_square_gaps':top})
  total_positive+=positive;total_squares+=squares
 res={'rqt':664,'source_rqt619_sha256':EXPECTED,'bound_t_inclusive':bound,
  'total_parameters':27*(2*bound+1),'nonnegative_F':total_positive,
  'exact_square_discriminants':total_squares,'integer_seeds':len(solutions),
  'closest_approach_definition':'min(|F(t)-floor(sqrt(F))^2|, |(floor(sqrt(F))+1)^2-F(t)|)',
  'cf_scope':'CF convergents of sqrt(a) are diagnostic, not generalized Pell roots or exhaustive integer t search',
  'records':summary,'solutions':solutions,'selected_excluded':82,'selected_unresolved':53,
  'new_all_scale_exclusions':0,'root19':'OPEN','original_22d_wall':'NOT REPLAYED'}
 if bound==100000:
  assert res['total_parameters']==5400027 and res['nonnegative_F']==5398223
  assert res['exact_square_discriminants']==0 and not solutions
 dst.write_text(json.dumps(res,indent=2)+'\n')
 print('PASS',res['total_parameters'],'tested;',res['nonnegative_F'],'nonnegative;',total_squares,'squares')
 print('sha256',hashlib.sha256(dst.read_bytes()).hexdigest())
 for r in summary:print(r['canonical_id'],r['five_smallest_absolute_square_gaps'][0]['absolute_square_gap'])
if __name__=='__main__':main()
