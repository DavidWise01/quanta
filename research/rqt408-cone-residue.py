#!/usr/bin/env python3
"""RQT-408: cone x projected residue compatibility, exact integer arithmetic.
The sole mathematical input is the established RQT-394 cone and
RQT-407 projected mask. Does NOT represent an integral norm -2 root.
"""
import argparse,itertools,json
from pathlib import Path

DEN=100000
LOW=177065
HIGH=178600
M=256
Y_BASE=16896 # divisible by 256, ensures real interval width > 256

def cone_lift(rx,ry,offset=0):
    assert 0<=rx<M and 0<=ry<M and offset>=0
    y=Y_BASE+ry+M*offset
    lo=(LOW*y)//DEN+1
    x=lo+(rx-lo)%M
    assert x%M==rx and y%M==ry
    assert LOW*y<DEN*x<HIGH*y
    return x,y

def audit(mask=None):
    count=0
    example=[]
    for ry in range(M):
        for rx in range(M):
            x,y=cone_lift(rx,ry)
            if len(example)<4:example.append(dict(rx=rx,ry=ry,x=x,y=y))
            # A whole infinite family exists: y += 256*k and recompute x
            assert cone_lift(rx,ry,offset=1)[1]==y+M
            count+=1
    assert count==M*M
    result={'RQT':408,'status':'PASS exact all-65536 residue-class cone lifts',
            'cone':'177065/100000 < x/y < 178600/100000',
            'modulus':M,'all_residue_pairs_lifted':count,
            'uniform_y_interval':[Y_BASE,Y_BASE+M-1],
            'family':'for any k>=0 take y=16896+ry+256*k, x=L+((rx-L) mod 256), L=floor(177065*y/100000)+1',
            'proof':'real-interval width is 1535*y/100000 > 256 for y>=16896; any residue class x mod256 occurs between strict bounds',
            'examples':example,'actual_root19':'OPEN',
            'scope':'Cone compatibility with every local xy residue, not exact discriminant-square existence'}
    if mask is not None:
        assert mask['modulus']==256 and mask['xy_pairs']==14336
        result['RQT407_admissible_xy_pairs']=14336
        result['conclusion']='All 14336 previously allowed pairs have arbitrarily large cone lifts. No further excluded residue class comes from cone alone.'
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--rqt407',help='Optional RQT-407 level record for modulus 256')
    p.add_argument('--out')
    a=p.parse_args()
    mask=json.loads(Path(a.rqt407).read_text()) if a.rqt407 else None
    result=audit(mask)
    if a.out:Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
