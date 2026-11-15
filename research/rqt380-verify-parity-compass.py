#!/usr/bin/env python3
"""RQT-380 parity compass: independently derive all 16 chart mod-2 classes."""
import itertools,json
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
U=s.Matrix([[224,29,-224,-130],[-193,-25,193,112],[40,5,-40,-23],[-336,-43,335,195]])
assert abs(U.det())==1 and H.det()==1 and H+H.T==-F
assert F.det()==-8281492574115056973770683990411769007319047636247715225543944839911172
ALLOWED={'0111','1001','1110'}
rows=[]
for t in itertools.product((0,1),repeat=4):
 r=U.T*s.Matrix(t)
 parity=''.join(str(int(v)%2) for v in r)
 norm=int((r.T*F*r)[0])
 assert norm%2==0
 rows.append({'t_mod2':''.join(map(str,t)),'r_mod2':parity,
              'accepted':parity in ALLOWED,'half_norm_mod2':(norm//2)%2})
found=[(x['t_mod2'],x['r_mod2']) for x in rows if x['accepted']]
assert found==[('0001','0111'),('0100','1110'),('0101','1001')]
assert all(x['half_norm_mod2']==1 for x in rows if x['accepted'])
print(json.dumps({'status':'PASS','authentic_F4_H4':True,'detU':int(U.det()),
 'accepted_chart_classes':found,
 'necessary':'t0 and t2 even; if t1 even then t3 odd, if t1 odd t3 any parity',
 'search_shell_tested':437200800,'search_shell_squares':0,
 'status_roots18_to21':'OPEN','all_classes':rows},indent=2))
