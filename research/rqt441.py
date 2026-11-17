import json,math,hashlib,sys
from pathlib import Path
s=json.load(open(sys.argv[1]));Q=[[int(v) for v in r] for r in s['restricted_Gram']]; B=[[int(v) for v in r] for r in s['reduced_kernel_basis']];F=[[int(v) for v in r] for r in s['original_F4']]
sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest(); assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
A=[[v//2 for v in r] for r in Q];a,b,c=A[0];g,e=A[1][1:];f=A[2][2];al=c*c-f*a;K=c*e-f*b;ga=e*e-f*g;de=-f;assert al<0 and de>0
chains={}; gates=[]
for p,end in [(2,12),(3,5),(5,5)]:
 prev=None; rows=[]
 for k in range(1,end+1):
  m=p**k; sq={i*i%m for i in range(m)}
  if prev is not None:assert {r%(m//p) for r in sq}==prev
  prev=sq;rows.append({'power':k,'modulus':m,'square_classes':len(sq)})
 gates.append((m,sq));chains[str(p)]=rows
mods=(256,63,65,11,17,19,23,31,25);sq={m:{i*i%m for i in range(m)} for m in mods}
for p,n in [(13,11),(23,7)]:assert f%p==(c+5*e)%p==0 and (-a-10*b-25*g)%p==n and n not in {i*i%p for i in range(p)}
rows=[]
for name,yl,yh,dl,dh in [('regression',1,512,1,511),('new_denominator',1,512,513,767)]:
 cnt=dict.fromkeys(['pairs','feasible_x','prime_rejected','base','after4096','after243','after3125','exact_squares','witnesses'],0); hits=[]
 for y in range(yl,yh+1):
  for d in range(dl,dh+1,2):
   cnt['pairs']+=1;R=(K*K-al*ga)*y*y-al*de*d*d
   if R<0:continue
   h=math.isqrt(R);lo=-((h-K*y)//(-al));hi=(K*y+h)//(-al)
   for x in range(lo,hi+1):
    cnt['feasible_x']+=1
    if (x%13 and (y-5*x)%13==0) or (x%23 and (y-5*x)%23==0):cnt['prime_rejected']+=1;continue
    E=al*x*x+2*K*x*y+ga*y*y+de*d*d;assert E>=0
    if any(E%m not in sq[m] for m in mods):continue
    cnt['base']+=1
    for (m,S),key in zip(gates,['after4096','after243','after3125']):
     if E%m not in S:break
     cnt[key]+=1
    else:
     t=math.isqrt(E)
     if t*t!=E:continue
     cnt['exact_squares']+=1;L=c*x+e*y
     for ss in {t,-t}:
      if (ss-L)%f:continue
      z=(ss-L)//f;w=(x,y,z); assert sum(A[i][j]*w[i]*w[j] for i in range(3) for j in range(3))==-d*d
      r=[sum(B[i][j]*w[j] for j in range(3)) for i in range(4)];assert sum(F[i][j]*r[i]*r[j] for i in range(4) for j in range(4))==-2*d*d
      if math.gcd(x,y,z,d)==1:cnt['witnesses']+=1;hits.append(list(map(str,(*w,d))))
 rows.append({'tile':name,'y':[yl,yh],'odd_d':[dl,dh],'counts':cnt,'hits':hits});print(name,cnt,flush=True)
assert rows[0]['counts']['base']==1251
out={'RQT':441,'sha256':sha,'chains':chains,'tiles':rows,'root19':'OPEN' if not any(r['hits'] for r in rows) else 'REVIEW','prefix18':'UNVERIFIED'}
Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
