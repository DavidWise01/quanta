#!/usr/bin/env python3
"""RQT-634: exact sharp recovery-only exponents (not unit identity orders).
Python 3 standard library. Outputs deterministic JSON certificate.
"""
import json, math, hashlib, sys
from pathlib import Path
D=[89518360633605555683821304281344825,149561530769640628300862186866588569,158134758925461363207454619257200752]
S=[5,7,4]
ids=[[28,29,30,31,33,34,35,36,37],[81,89,92],[0,1,2,7]]
def powpair(v,n,mul,one):
    result=one
    for _ in range(n):result=mul(result,v)
    return result

rows=[]
for index,(orig,s,members) in enumerate(zip(D,S,ids),1):
    assert orig%(s*s)==0
    d=orig//(s*s)
    assert math.isqrt(d)**2!=d
    def mul(a,b):
        x,y=a;z,w=b
        return ((x*z+d*y*w)%s,(x*w+y*z)%s)
    one=(1%s,0)
    elements=[(x,y) for x in range(s) for y in range(s) if (x*x-d*y*y)%s==1%s]
    orders=[]
    for v in elements:
        current=one
        for order in range(1,2*s*s+1):
            current=mul(current,v)
            if current==one:break
        else:raise AssertionError('residue not unit')
        orders.append(order)
    identity_exponent=math.lcm(*orders)
    recovery_exponent=next(E for E in range(1,identity_exponent+1)
        if all((lambda v:powpair(v,E,mul,one)[1]==0)(v) for v in elements))
    assert identity_exponent in (6,4)
    assert recovery_exponent < identity_exponent
    assert all(powpair(v,recovery_exponent,mul,one)[1]==0 for v in elements)
    for e in range(1,recovery_exponent):
        assert any(powpair(v,e,mul,one)[1]!=0 for v in elements)
    witness=next(v for v in elements if all(powpair(v,e,mul,one)[1]!=0 for e in range(1,recovery_exponent)))
    rows.append(dict(group=index,original_D=str(orig),reduced_d=str(d),s=s,
        members=members,group_size=len(elements),
        identity_exponent=identity_exponent,recovery_only_exponent=recovery_exponent,
        sharp_witness=list(witness),
        residues=[dict(x=x,Y=y,order=order,at_recovery=list(powpair((x,y),recovery_exponent,mul,one)))
                 for (x,y),order in zip(elements,orders)]))
assert [v['identity_exponent'] for v in rows]==[6,6,4]
assert [v['recovery_only_exponent'] for v in rows]==[3,3,2]
assert [v['group_size'] for v in rows]==[6,6,8]
assert sum(len(v['members']) for v in rows)==16
out={'rqt':634,'title':'Sharp recovery-only Pell unit exponents','groups':rows,
     'theorem':'For D=s^2*d, reduced norm-one U^E has coefficient Y_E divisible by s at E=3,3,2 respectively; recovered (X,Y_E/s) solves X^2-D*y^2=1.',
     'correction':'RQT-631 exponents (6,6,4) are correct for return to (1,0) modulo s but not minimal for the weaker Y=0 recovery gate.',
     'actual_reduced_integer_units_found':0,'new_selected_family_exclusions':0,
     'selected_excluded':82,'selected_unresolved':53,'canonical_unresolved':27,
     'original_22d_wall':'NOT REPLAYED','root19':'OPEN'}
p=Path(sys.argv[1] if len(sys.argv)>1 else 'RQT-634-results.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print('PASS',[(r['s'],r['recovery_only_exponent'],r['identity_exponent']) for r in rows])
print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
