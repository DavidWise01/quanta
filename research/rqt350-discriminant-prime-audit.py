#!/usr/bin/env python3
"""RQT-350: four newly certified ternary rational-isotropy obstructions.
Original RQT-242 frozen Gram. Exact Python/SymPy replay; no integral root.
The six other planes are UNRESOLVED; factoring is not claimed complete.
"""
import json
import sympy as s
F=s.Matrix([
[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
CASES=[
 (196,197,32790353,[25985934,27145414,1],9242088),
 (200,201,307273,[100866,273575,1],145715),
 (841,840,2492311,[724605,637158,1],152989),
 (844,843,661417,[47179,44181,1],395865),
]
records=[]
for m,n,p,coords,witness in CASES:
 assert s.isprime(p)
 T=s.Matrix([[-m,0,0],[0,1,0],[n,0,0],[0,0,1]])
 G=T.T*F*T
 det=int(G.det())
 assert det%p==0 and det%(p*p)!=0
 a,b,c=[int(G[i,j]) for i,j in [(0,0),(0,1),(1,1)]]
 h=(a*c-b*b)%p
 assert h!=0 and pow((-h)%p,(p-1)//2,p)==p-1
 v=s.Matrix(coords)
 assert v[2]==1
 assert all(int(z)%p==0 for z in G*v)
 norm=int((v.T*G*v)[0])
 assert norm%p==0 and norm%(p*p)!=0
 assert (norm//p)%p==witness
 records.append({'slope':f'{m}/{n}','bad_prime':p,'det_valuation':1,
 'anisotropic_binary_quotient':True,'radical_mod_p':coords,
 'norm_div_p_mod_p':witness,'primitive_mod_p2_root':False})
assert len(records)==4
unresolved=['188/189','192/193','194/195','199/200','201/202','851/850']
print(json.dumps({'result':'PASS exact original-lattice local obstructions',
 'prior_RQT349_excluded':21,'newly_excluded':4,'total_excluded':25,
 'unresolved_count':len(unresolved),'unresolved':unresolved,
 'new_certificates':records,
 'caveat':'This does not give complete factorization or global rational roots.',
 'integral_roots18_to21':'OPEN'},indent=2))
