#!/usr/bin/env python3
"""RQT-440: exact lossless residue-mask sieve; full RQT-401 JSON required.
Usage: python research/rqt440-residue-engine.py FULL.json
"""
import json,math,hashlib,itertools,sys
S=json.load(open(sys.argv[1]));Q=[[int(v) for v in r] for r in S['restricted_Gram']]
F=[[int(v) for v in r] for r in S['original_F4']]
B=[[int(v) for v in r] for r in S['reduced_kernel_basis']]
assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
sha=hashlib.sha256(json.dumps([[str(t) for t in r] for r in Q],separators=(',',':')).encode()).hexdigest()
assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2]
alpha=c*c-f*a;K=c*e-f*b;gamma=e*e-f*g;delta=-f
assert alpha<0 and delta>0
mods=(16,9,25,256,63,65,11,17,19,23,31)
sq={m:{i*i%m for i in range(m)} for m in mods}
def E(x,y,d):return alpha*x*x+2*K*x*y+gamma*y*y+delta*d*d
mask={}
for m in (16,9,25):
 mask[m]=[[sum(1<<x for x in range(m) if E(x,y,d)%m in sq[m]) for d in range(m)] for y in range(m)]
def allow(m,x,y,d):return bool(mask[m][y%m][d%m]&(1<<(x%m)))
for m in mask:
 assert all(allow(m,x,y,d)==(E(x,y,d)%m in sq[m]) for x,y,d in ((0,0,0),(3,5,7),(-19,238,17),(99,101,103)))
out=[]
for name,yl,yh,dl,dh in [('old',1,256,1,255),('A',1,256,257,511),('B',257,512,1,511)]:
 n=dict.fromkeys(('pairs','empty','integer_x','prime_rejected','after16','after9','after25','baseline','extended','squares'),0)
 for y in range(yl,yh+1):
  for d in range(dl,dh+1,2):
   n['pairs']+=1
   R=(K*K-alpha*gamma)*y*y-alpha*delta*d*d
   if R<0:n['empty']+=1;continue
   h=math.isqrt(R);lo=-((h-K*y)//(-alpha));hi=(K*y+h)//(-alpha)
   if lo>hi:n['empty']+=1;continue
   for x in range(lo,hi+1):
    n['integer_x']+=1
    if (x%13!=0 and (y-5*x)%13==0) or (x%23!=0 and (y-5*x)%23==0):
     n['prime_rejected']+=1;continue
    if not allow(16,x,y,d):continue
    n['after16']+=1
    if not allow(9,x,y,d):continue
    n['after9']+=1
    ee=E(x,y,d);assert ee>=0
    base=all(ee%m in sq[m] for m in (256,63,65,11,17,19,23,31))
    if base:n['baseline']+=1
    if not allow(25,x,y,d):continue
    n['after25']+=1
    if not base:continue
    n['extended']+=1
    if math.isqrt(ee)**2==ee:n['squares']+=1
 out.append({'tile':name,'counts':n})
 print(name,n,flush=True)
assert [r['counts']['integer_x'] for r in out]==[64512,64512,386560]
assert [r['counts']['baseline'] for r in out]==[223,213,1335]
assert [r['counts']['extended'] for r in out]==[154,143,954]
assert all(r['counts']['squares']==0 for r in out)
result={'RQT':440,'status':'PASS','source_sha256':sha,
 'mask_moduli':[16,9,25],'mask_bits_popcount':{str(m):sum(z.bit_count() for row in mask[m] for z in row) for m in mask},
 'tiles':out,'total_integer_x':515584,'old_survivors':1771,'new_survivors':1251,'additional_rejected':520,
 'witness':'OPEN','root19':'OPEN','root18_prefix':'UNVERIFIED'}
print(json.dumps(result,indent=2))
if len(sys.argv)>2:open(sys.argv[2],'w').write(json.dumps(result,indent=2)+'\n')
