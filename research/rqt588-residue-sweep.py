#!/usr/bin/env python3
"""RQT-588 exact residue test on archived RQT-583/584/586 JSON (no Gram or Wall claim).
Usage: python research/rqt588-residue-sweep.py RQT-583-results.json RQT-584-results.json RQT-586-results.json
"""
import hashlib, json, math, sys

def read(path):
    data=open(path,'rb').read()
    return json.loads(data),hashlib.sha256(data).hexdigest()

def moduli():
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97):
        q=p
        while q<=4096:
            yield q
            q*=p

e,he=read(sys.argv[1])
a,ha=read(sys.argv[2])
b,hb=read(sys.argv[3])
assert he==b['source_sha256']['rqt583/results.json']
assert ha==b['source_sha256']['rqt584/results.json']
blocked={int(x['family_index']) for x in a['certificates']}
blocked.update(int(x['family_index']) for x in b['certificates'])
eq={int(x['index']):x for x in e['equations']}
assert len(eq)==80 and len(blocked)==26
remaining=sorted(set(eq)-blocked)
assert len(remaining)==54
new_exclusions=[];square_hits=[]
for i in remaining:
    x=eq[i]
    A,B,C=(int(x[k]) for k in 'ABC')
    for m in moduli():
        squares={t*t % m for t in range(m)}
        if not any((A*t*t+B*t+C)%m in squares for t in range(m)):
            new_exclusions.append((i,m))
            break
    if i in {j for j,_ in new_exclusions}:
        continue
    for t in range(-2000,2001):
        d=A*t*t+B*t+C
        if d>=0 and math.isqrt(d)**2==d:
            square_hits.append((i,t))
assert not new_exclusions and not square_hits
print('RQT-588 PASS: 0 new exclusions; 0 square hits in [-2000,2000]; 54 unresolved. Root19 OPEN.')
