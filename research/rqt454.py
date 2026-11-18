import hashlib,json,math,sys
from pathlib import Path

def address(i):
    # Base 9^8 blocks, four digits on each flank, outermost first.
    shells=[]
    while True:
        i,r=divmod(i,9**8); digits=[]
        for _ in range(8): r,j=divmod(r,9);digits.append(j)
        digits=digits[::-1];shells.append((digits[:4],digits[4:]))
        if not i:return shells[::-1]

def decode(shells):
    i=0
    for left,right in shells:
        for digit in left+right:i=9*i+digit
    return i

def run(path,steps=100000):
    S=json.load(open(path));Q=[[int(v) for v in r] for r in S['restricted_Gram']];B=[[int(v) for v in r] for r in S['reduced_kernel_basis']];F=[[int(v) for v in r] for r in S['original_F4']]
    sha=hashlib.sha256(json.dumps([[str(v) for v in r] for r in Q],separators=(',',':')).encode()).hexdigest();assert sha=='5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809'
    assert all(Q[i][j]%2==0 and Q[i][j]==sum(B[k][i]*F[k][l]*B[l][j] for k in range(4) for l in range(4)) for i in range(3) for j in range(3))
    a,b,c=[v//2 for v in Q[0]];g,e=[v//2 for v in Q[1][1:]];f=Q[2][2]//2;D=b*b-a*g;T=D*(a*f-c*c)+(b*c-a*e)**2;target=4*T+D*a
    s=math.isqrt(D);assert s*s<D and abs(target)>2*s
    m=0;den=1;k=s;P0,P1=0,1;R0,R1=1,0;best=None;unit=None;stages=dict.fromkeys('JANE',0);digest=bytes(32)
    for i in range(steps):
        route=address(i);assert decode(route)==i;stages['J']+=1
        m2=den*k-m;den2,rem=divmod(D-m2*m2,den);assert not rem and 0<den2<=2*s;stages['A']+=1
        norm=(-1 if i%2==0 else 1)*den2
        if i<512:
            P=k*P1+P0;R=k*R1+R0;assert P*P-D*R*R==norm;P0,P1=P1,P;R0,R1=R1,R
        assert norm!=target;stages['N']+=1
        best=abs(norm) if best is None else min(best,abs(norm))
        digest=hashlib.sha256(digest+json.dumps([i,route,str(m2),str(den2)],separators=(',',':')).encode()).digest();stages['E']+=1
        m,den=m2,den2;k=(s+m)//den
        if norm==1:unit=i;break
    for i in (0,8,9,9**4,9**8-1,9**8,9**16+3):assert decode(address(i))==i
    return dict(RQT=454,sha256=sha,stages=stages,full_norm_controls=min(512,stages['N']),D_bits=D.bit_length(),target_bits=abs(target).bit_length(),convergent_norm_bound_bits=(2*s).bit_length(),target_outside_all_ordinary_convergents=True,unit_index=unit,min_norm_bits=best.bit_length(),chain_sha256=digest.hex(),next_state=dict(index=stages['E'],m=str(m),den=str(den),k=str(k)),last_address=address(stages['E']-1),root19='OPEN',prefix18='UNVERIFIED')
if __name__=='__main__':
    out=run(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='next_state'})
