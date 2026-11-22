#!/usr/bin/env python3
"""RQT-591 exact replay of archived HNF/LLL construction.
Run: python rqt591.py ROOT where ROOT has rqt544.py, historical_index64_basis.json,
saturated_rank4_basis_21x4.json, rank4_gram.json, rank4_wall.json.
"""
import ast,json,hashlib,sys
from pathlib import Path
from fractions import Fraction
import sympy as S
from sympy.matrices.normalforms import hermite_normal_form
p=Path(sys.argv[1]);load=lambda n:S.Matrix(json.loads((p/n).read_text()))
ast544=ast.parse((p/'rqt544.py').read_text())
fn=next(n for n in ast544.body if isinstance(n,ast.FunctionDef) and n.name=='qlll')
env={'Fraction':Fraction,'S':S}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<qlll>','exec'),env)
B=load('historical_index64_basis.json');N=load('saturated_rank4_basis_21x4.json')
F=load('rank4_gram.json');H=load('rank4_wall.json')
assert F.shape==H.shape==(4,4) and B.shape==(21,21) and N.shape==(21,4)
I=S.eye(22)
K=S.Matrix.hstack(*[I[:,j]-I[:,0] if j<20 else I[:,j] for j in range(1,22)])
A=K*B*N
R,T,steps=env['qlll'](hermite_normal_form(A).T)
U=A.solve(R.T)
assert steps==152 and abs(U.det())==1 and all(x.q==1 for x in U)
assert A*U==R.T
Fr=U.T*F*U;Hr=U.T*H*U
assert Hr+Hr.T==-Fr and Fr.det()==F.det() and Hr.det()==H.det()
M=Fr[0,1:4].T*Fr[0,1:4]-Fr[0,0]*Fr[1:4,1:4]
assert Fr[0,0]==-9603309702921447656
assert M==S.Matrix([[-33923887662911442206164954953584674140,-4219194573559178010400265744479501422,81850829273715620803639379963437553624],[-4219194573559178010400265744479501422,-21708964175564668486249102082477843199,-5011140550130980758998505863715699836],[81850829273715620803639379963437553624,-5011140550130980758998505863715699836,-208380363797895400994011084419064194688]])
out={'rqt':591,'steps':steps,'detU':str(U.det()),'reduced_gram':[[str(v) for v in row] for row in Fr.tolist()],'U':[[str(v) for v in row] for row in U.tolist()],'wall_symmetrization':True,'schur':True,'root19':'OPEN'}
Path('RQT-591-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS 152 LLL steps, exact unimodular Gram/Wall and RQT-589 Schur; Root19 OPEN')
