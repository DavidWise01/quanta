#!/usr/bin/env python3
"""Independent original F4 reflection witness audit. Input RQT-386 JSON certificate."""
import argparse,json,math
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
T=s.Matrix([[-194,0,0],[0,1,0],[195,0,0],[0,0,1]])
V=s.Matrix([[1,3,1],[-25,-74,-24],[113,340,113]])
assert H+H.T==-F and H.det()==1
def validate(j):
 u=s.Matrix([int(t) for t in j['original_null_u']])
 v=s.Matrix([int(t) for t in j['bezout_partner_v']])
 r=s.Matrix([int(t) for t in j.get('candidate_root_vector_r',j.get('root_candidate_r'))])
 z=s.Matrix([int(t) for t in j.get('ternary_coordinates_x_h_y',[])])
 if len(z)==3:assert T*V*z==u
 assert math.gcd(*map(int,u))==1 and math.gcd(*map(int,F*u))==1
 assert (u.T*F*u)[0]==0 and (u.T*F*v)[0]==1
 q=int((v.T*F*v)[0])//2
 assert 2*q==(v.T*F*v)[0]
 assert r==(1+q)*u-v and (r.T*F*r)[0]==-2
 assert (r.T*H*r)[0]==1
 assert ''.join(str(int(t)%2) for t in r)=='0111'
 R=s.eye(4)+r*(r.T*F)
 assert R*R==s.eye(4) and R.T*F*R==F and R.det()==-1
 return {'status':'PASS independent exact integer verification',
         'u_F_u':0,'gcd_Fu':1,'u_F_v':1,'r_F_r':-2,
         'reflection_det':-1,'reflection_involution':True,
         'frozen_17_prefix_order':'NOT CHECKED'}
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('certificate',help='JSON output of rqt386-exact-null-and-root-candidate.py')
 args=ap.parse_args()
 with open(args.certificate) as f: j=json.load(f)
 print(json.dumps(validate(j),indent=2))
