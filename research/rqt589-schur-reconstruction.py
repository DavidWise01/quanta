#!/usr/bin/env python3
"""RQT-589 exact discriminant matrix reconstruction. python rqt589.py RQT-583-results.json [out.json]"""
import sys,json,hashlib
import sympy as S
from pathlib import Path
p=Path(sys.argv[1]);raw=p.read_bytes();d=json.loads(raw)
expected="5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"
assert hashlib.sha256(raw).hexdigest()==expected
assert d["rqt"]==583 and len(d["equations"])==80
x=S.symbols("m11 m22 m33 m12 m13 m23 a")
def Q(v):
 u,w,z=v
 return x[0]*u*u+x[1]*w*w+x[2]*z*z+2*x[3]*u*w+2*x[4]*u*z+2*x[5]*w*z
eq=[]
for e in d["equations"]:
 r,o=e["ray"],e["offset"]
 A,B,C=[int(e[k]) for k in "ABC"]
 eq += [Q(r)-A,Q([r[j]+o[j] for j in range(3)])-Q(r)-Q(o)-B,Q(o)-2*x[6]-C]
mat,y=S.linear_eq_to_matrix(eq,x)
assert mat.rank()==mat.row_join(y).rank()==7
sol=list(S.linsolve((mat,y),x))[0]
assert all(v.is_Integer for v in sol)
M=S.Matrix([[sol[0],sol[3],sol[4]],[sol[3],sol[1],sol[5]],[sol[4],sol[5],sol[2]]]);a=sol[6]
for e in d["equations"]:
 r=S.Matrix(e["ray"]);o=S.Matrix(e["offset"])
 A=int((r.T*M*r)[0]);B=int(2*(r.T*M*o)[0]);C=int((o.T*M*o)[0]-2*a)
 assert [A,B,C]==[int(e[k]) for k in "ABC"]
 assert B*B-4*A*C==int(e["D"])
result=dict(rqt=589,source_sha256=expected,equations_checked=80,linear_constraints=len(eq),rank=7,a=str(a),M=[[str(M[i,j]) for j in range(3)] for i in range(3)],full_gram="NOT RECOVERED",original_22d_wall="NOT REPLAYED",excluded=81,unresolved=54,root19="OPEN")
Path(sys.argv[2] if len(sys.argv)>2 else "RQT-589-results.json").write_text(json.dumps(result,indent=2)+"\n")
print("PASS exact 80 families / 240 identities; full 4x4 canonical Gram NOT recovered; root19 OPEN")
