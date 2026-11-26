# ADA-316N .dlw — independent model benchmark, not native Rust.
import itertools,json,time,statistics
S=(0,)*8; V=(0,1)*4; M=(None,)*8; H=(0,0,0,0,1,1,1,1); I=(3,)*8
patterns=[(S,), (V,), (M,), (H,), (I,), (V,S), (V,V,S), (S,S,V), (M,V,S,H), (V,)*15, (S,)*15, (V,S,M,H,I)*3]
names=['stable','volatile','missing','neutral','invalid','balanced','contract bias','expand bias','mixed','volatile 15','stable 15','mixed 15']
def adjust(p,h):
 w,k=p
 if len(h)!=8 or any(x not in (0,1,2) for x in h):return p
 c=sum(a!=b for a,b in zip(h,h[1:]))
 return (min(w+1,8),max(k-1,0)) if c==0 else (max(w-1,3),min(k+1,12)) if c>=4 else p
def full(p,seq,n):
 for e in range(n):p=adjust(p,seq[e%len(seq)])
 return p,n
def fast(p,seq,n):
 q,r=divmod(n,len(seq)); work=0
 for _ in range(q):
  old=p
  for h in seq:p=adjust(p,h);work+=1
  if old==p:break
 for h in seq[:r]:p=adjust(p,h);work+=1
 return p,work
states=list(itertools.product(range(3,9),range(13)))
results=[]
for name,seq in zip(names,patterns):
 a=[];b=[];counts=[]
 for repeat in range(3):
  t=time.perf_counter_ns();ref=[full(p,seq,1000) for p in states];a.append(time.perf_counter_ns()-t)
  t=time.perf_counter_ns();opt=[fast(p,seq,1000) for p in states];b.append(time.perf_counter_ns()-t)
  assert [p for p,w in ref]==[p for p,w in opt]
  counts=[w for p,w in opt]
 results.append(dict(name=name,period=len(seq),max_work=max(counts),min_work=min(counts),sum_work=sum(counts),full_ms=statistics.median(a)/1e6,fast_ms=statistics.median(b)/1e6))
print(json.dumps(dict(scope='Python model only',horizon=1000,states=78,repetitions=3,comparisons=12*78*3,results=results),indent=2))
