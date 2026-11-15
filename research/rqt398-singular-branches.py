#!/usr/bin/env python3
"""RQT-398: exact first singular Hensel lift of norm -2 in RQT-388 lattice.
Input: full rqt388-exact-second-key.py --out JSON with restricted_Gram.
Only counts p -> p**2; higher lifting is not inferred automatically.
"""
import argparse, itertools, json
from pathlib import Path

def classify(Q, p):
    if p < 2 or any(p % d == 0 for d in range(2, int(p**0.5)+1)):
        raise ValueError('p must be prime')
    assert len(Q)==3 and all(len(row)==3 for row in Q)
    assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
    base, regular, singular_alive, singular_dead = 0,0,0,0
    total=0
    samples={}
    for v in itertools.product(range(p), repeat=3):
        N=2+sum(Q[i][j]*v[i]*v[j] for i in range(3) for j in range(3))
        if N%p: continue
        base+=1
        gradient=tuple((2*sum(Q[i][j]*v[j] for j in range(3)))%p for i in range(3))
        c=(N//p)%p
        if any(gradient):
            regular+=1
            total+=p*p
            samples.setdefault('regular',list(v))
        elif c==0:
            singular_alive+=1
            total+=p**3
            samples.setdefault('singular_surviving',list(v))
        else:
            singular_dead+=1
            samples.setdefault('singular_dead',list(v))
    assert base==regular+singular_alive+singular_dead
    return {'prime':p,'mod_p_survivors':base,'regular_branches':regular,
            'singular_lifting_branches':singular_alive,
            'singular_dead_branches':singular_dead,
            'mod_p_squared_survivors':total,'sample_branches':samples,
            'no_local_solutions_mod_p_squared':total==0}

def audit(data, primes=(2,3,5,7)):
    q=data.get('restricted_F4_Gram',data.get('restricted_Gram'))
    if q is None: raise ValueError('Need full RQT-388 restricted_Gram; summary lacks matrix')
    Q=[[int(v) for v in row] for row in q]
    out={'RQT':398,'method':'exact first-order lift p to p^2',
         'derivation':'N(v+p*t)/p == N(v)/p + 2*(Qv).t (mod p), provided N(v)=0 (mod p)',
         'results':[classify(Q,p) for p in primes],
         'root19':'OPEN','scope':'A completely empty local level proves exclusion; survivors do not prove existence'}
    out['global_obstruction_found']=any(r['no_local_solutions_mod_p_squared'] for r in out['results'])
    if out['global_obstruction_found']: out['root19']='EXCLUDED (conditional on valid frozen Q input)'
    return out

if __name__=='__main__':
    pa=argparse.ArgumentParser()
    pa.add_argument('kernel_json')
    pa.add_argument('--primes',type=int,nargs='+',default=[2,3,5,7])
    pa.add_argument('--out')
    a=pa.parse_args()
    result=audit(json.loads(Path(a.kernel_json).read_text()),a.primes)
    if a.out: Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
