# ADA-314N .dlw — independent model, not Rust execution.
import math,json

def dominant(g):
    values=[math.floor((1+math.cos(((g+120*i)%360)*math.pi/180))/3*1_000_000+0.5) for i in range(3)]
    return max(range(3),key=lambda i:values[i])

def history(e): return [dominant(g) for g in range(e*24-8,e*24)]
def adjust(p,h):
    w,k=p
    c=sum(a!=b for a,b in zip(h,h[1:]))
    return (min(w+1,8),max(k-1,0)) if c==0 else (max(w-1,3),min(k+1,12)) if c>=4 else p
H=[history(e) for e in range(1,16)]
assert all(history(e)==H[(e-1)%15] for e in range(1,1001))
def optimized(e,p):
    for _ in range(e//15):
        before=p
        for h in H:p=adjust(p,h)
        if p==before:break
    for h in H[:e%15]:p=adjust(p,h)
    return p
checks=0
for w in range(3,9):
    for k in range(13):
        p=(w,k)
        for e in range(1001):
            assert p==optimized(e,(w,k)),(w,k,e)
            checks+=1
            if e<1000:p=adjust(p,history(e+1))
print(json.dumps(dict(scope='independent Python model; not native Rust',states=78,epoch_boundaries=1001,comparisons=checks,period_checks=1000,changes=[sum(a!=b for a,b in zip(h,h[1:])) for h in H],default_final=optimized(1000,(8,0)))))
