#!/usr/bin/env python3
"""RQT-396 exact local congruence sieve for frozen root19 lattice.

Usage: python research/rqt396-modular-gate.py /path/to/rqt388-full.json
The input MUST contain the full restricted_Gram matrix from the RQT-388
--out run, not the small published summary.
"""
import argparse, itertools, json, math
from pathlib import Path

MODULI=(5,7,8,9)
EXPECTED={5:20,7:42,8:192,9:162}

def local_classes(Q,m):
    q=[[int(Q[i][j])%m for j in range(3)] for i in range(3)]
    survivors=[]
    for x,y,z in itertools.product(range(m),repeat=3):
        v=(x,y,z)
        if (2+sum(q[i][j]*v[i]*v[j] for i in range(3) for j in range(3)))%m==0:
            survivors.append((x,y,z))
    return survivors

def audit(src):
    Q=src.get("restricted_F4_Gram",src.get("restricted_Gram"))
    if Q is None:
        raise ValueError("Need full RQT-388 reduced 3x3 Gram, not summary")
    assert len(Q)==3 and all(len(row)==3 for row in Q)
    assert all(int(Q[i][j])==int(Q[j][i]) for i in range(3) for j in range(3))
    counts={}
    sample={}
    for m in MODULI:
        survivors=local_classes(Q,m)
        counts[str(m)]=len(survivors)
        sample[str(m)]=list(survivors[0]) if survivors else None
        assert len(survivors)==EXPECTED[m], (m,len(survivors),EXPECTED[m])
    M=math.prod(MODULI)
    assert math.gcd(5,7)==math.gcd(7,8)==math.gcd(8,9)==math.gcd(5,9)==1
    total=math.prod(counts.values())
    assert total==26127360
    return {
      "RQT":396,
      "status":"PASS inherited local class counts; NO GLOBAL ROOT19 DECISION",
      "basis":"RQT-388 reduced saturated rank-three kernel",
      "moduli":list(MODULI),
      "survivor_triples_by_modulus":counts,
      "one_surviving_residue_triple_each":sample,
      "combined_modulus":M,
      "combined_surviving_residue_triples":total,
      "logic":"CRT combines 4 coprime modular solutions coordinatewise; residue classes do not prove integer norm -2",
      "global_cone":"177065/100000 < x/y < 178600/100000; y!=0",
      "caveat":"The open cone can be met by sufficiently large lifts of ANY fixed (x,y) residue pair modulo M; no archimedean exclusion follows from these congruences",
      "root19":"OPEN","root20":"OPEN","root21":"conditional",
      "scope":"Finite moduli (5,7,8,9) only; positive modular feasibility is not integral existence"
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("kernel_json")
    p.add_argument("--out")
    args=p.parse_args()
    result=audit(json.loads(Path(args.kernel_json).read_text()))
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
