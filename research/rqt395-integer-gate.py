#!/usr/bin/env python3
"""RQT-395 exact integer gate for RQT-388 reduced kernel.

Input JSON needs restricted_F4_Gram (or restricted_Gram), not merely the
summary certificate. A bounded scan is NOT a global nonexistence proof.
"""
import argparse, json, math
from pathlib import Path

def audit(source, max_y=1000):
    Q=source.get("restricted_F4_Gram",source.get("restricted_Gram"))
    if Q is None: raise ValueError("Full reduced 3x3 Gram matrix required")
    a,b,c,d,e,f=(int(Q[i][j]) for i,j in
                   ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2)))
    assert f!=0
    A,K,C=c*c-f*a,c*e-f*b,e*e-f*d
    result=dict(RQT=395,status="FINITE TEST ONLY; root19 OPEN",
                checked_xy=0,real=0,squares=0,integral_z=0,roots=[])
    for y in range(1,max_y+1): # up to simultaneous sign reversal
        for x in range((177065*y)//100000+1,(178600*y-1)//100000+1):
            result["checked_xy"]+=1
            D=A*x*x+2*K*x*y+C*y*y-2*f
            if D<0:continue
            result["real"]+=1
            t=math.isqrt(D)
            if t*t!=D:continue
            result["squares"]+=1
            L=c*x+e*y
            for sign in (-1,1):
                n=-L+sign*t
                if n%f:continue
                z=n//f
                assert a*x*x+2*b*x*y+2*c*x*z+d*y*y+2*e*y*z+f*z*z==-2
                result["integral_z"]+=1
                result["roots"].append([x,y,z])
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("kernel_json")
    p.add_argument("--max-y",type=int,default=1000)
    args=p.parse_args()
    print(json.dumps(audit(json.loads(Path(args.kernel_json).read_text()),args.max_y),indent=2))
