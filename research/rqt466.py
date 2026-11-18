import json, hashlib, math, sys
from pathlib import Path
from sympy import primerange, sqrt_mod, isprime

def vp(n,p):
    assert n
    k=0
    while n%p==0:n//=p;k+=1
    return k,n

def symbol(n,h,p):
    k,u=vp(n,p); l,v=vp(h,p)
    if p==2:return (-1)**((((u-1)//2)*((v-1)//2)+k*((v*v-1)//8)+l*((u*u-1)//8))%2)
    return (-1)**(((p-1)//2*k*l+l*(pow(u%p,(p-1)//2,p)!=1)+k*(pow(v%p,(p-1)//2,p)!=1))%2)

def run(path,prior):
    S=json.load(open(path));Q=[[int(x) for x in r] for r in S['restricted_Gram']];B=[[int(x) for x in r] for r in S['reduced_kernel_basis']];F=[[int(x) for x in r] for r in S['original_F4']]
    sha=hashlib.sha256(json.dumps([[str(x) for x in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
    assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
    a,b,c=[x//2 for x in Q[0]];g,e=[x//2 for x in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;delta=a*(g*f-e*e)-b*(b*f-c*e)+c*(b*e-c*g);assert D%9==delta%9==b%3==e%3==0
    H=D//9; old=json.load(open(prior));assert old['sha256']==sha
    zs=[z for z in range(1,6562) if str(z) not in old['blocked'] and z%8 in old['mod8_allowed']];assert len(zs)==2087
    for z,(p,k) in old['blocked'].items():
        assert isprime(p) and a%p and pow(D%p,(p-1)//2,p)==p-1 and vp(D-delta*int(z)**2,p)[0]==k and k%2
    rows=[];controls=0
    for p in (2,19,9781,290533):
        assert isprime(p) and vp(H,p)[0]==1
        bad=[z for z in zs if symbol(a*(H-delta//9*z*z),H,p)==-1]
        rows.append(dict(p=p,tests=len(zs),excluded=bad))
        for x in range(-9,10):
            for y in range(-9,10):
                n=x*x-H*y*y
                if n:assert symbol(n,H,p)==1;controls+=1
    projection=[]
    for m in (128,81):
        aa,bb,cc,gg,ee,ff=[v%m for v in (a,2*b,2*c,g,2*e,f)]
        allowed=[z for z in range(m) if any((aa*x*x+bb*x*y+cc*x*z+gg*y*y+ee*y*z+ff*z*z+1)%m==0 for x in range(m) for y in range(m))]
        projection.append(dict(m=m,allowed=len(allowed),excluded=[z for z in zs if z%m not in allowed]))
    survivors=set(zs)-{z for r in rows+projection for z in r['excluded']}; blocked={}; primes=0
    for p in primerange(1000001,5000001):
        primes+=1
        if not a%p or not delta%p or pow(D%p,(p-1)//2,p)!=p-1:continue
        r=D*pow(delta,-1,p)%p
        if pow(r,(p-1)//2,p)!=1:continue
        for z in sqrt_mod(r,p,all_roots=True):
            if z in survivors:
                k,_=vp(D-delta*z*z,p)
                if k%2:blocked[z]=[p,k];survivors.remove(z)
    return dict(RQT=466,sha256=sha,prior_verified=len(old['blocked']),initial=len(zs),ramified=rows,norm_controls=controls,projection=projection,new_primes=primes,new_blocked=blocked,remaining=len(survivors),first_survivors=sorted(survivors)[:30],root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
    out=run(sys.argv[1],sys.argv[2]);Path(sys.argv[3]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='new_blocked'});print('new blocked',len(out['new_blocked']))
