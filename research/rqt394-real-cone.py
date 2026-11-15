#!/usr/bin/env python3
"""RQT-394: global exact rational-slope corridor for frozen root19.
Usage: python research/rqt394-real-cone.py /tmp/rqt388.json
"""
import argparse,json,math
from pathlib import Path
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],
[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],
[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],
[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],
[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],
[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],
[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
def audit(j):
 B=s.Matrix([[int(x) for x in row] for row in j['reduced_kernel_basis']])
 Q=s.Matrix([[int(x) for x in row] for row in j.get('restricted_F4_Gram',j.get('restricted_Gram'))])
 assert B.shape==(4,3) and Q==Q.T and B.T*F*B==Q
 a,b,c,d,e,f=[int(Q[i,j]) for i,j in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))]
 # Disc in third variable z: f*z² + 2(cx+ey)z + (ax²+2bxy+dy²+2)=0
 A=c*c-f*a;K=c*e-f*b;C=e*e-f*d;constant=-2*f
 assert A<0 and K>0 and C<0 and constant>0 and A+constant<0
 lower,upper,den=177065,178600,100000
 assert lower*(-A)<K*den<upper*(-A)
 cert={}
 for name,num in (('lower',lower),('upper',upper)):
  poly=A*num*num+2*K*num*den+C*den*den
  assert poly<0 and poly+constant*den*den<0
  cert[name]={'fraction':f'{num}/{den}',
             'strict_negative_boundary_at_abs_y_ge_1':True,
             'certified_margin_bits':abs(poly+constant*den*den).bit_length()}
 # A<0 => D(x,y) is concave in x/y; vertex lies between endpoints.
 # For all integer y!=0, D<0 outside the open interval.
 x,y=16,9
 Delta=A*x*x+2*K*x*y+C*y*y+constant
 assert Delta>0 and math.isqrt(Delta)**2!=Delta
 return {'RQT':394,'status':'PASS exact global original F4 root19 real corridor',
  'necessity':'y != 0 and 177065/100000 < x/y < 178600/100000',
  'endpoint_certificates':cert,
  'x_equals_zero_or_y_equals_zero':'cannot yield required norm (prior RQT-389; y=0 also fails discriminant)',
  'real_but_not_integer_discriminant_example':{'x':16,'y':9,'Delta_positive':True,
     'Delta_perfect_square':False},
  'accepted_root19_found':False,'root18':'first-stage accepted',
  'root19':'OPEN','root20':'OPEN','root21':'conditional',
  'scope':'Unbounded necessary real cone, not sufficient integer construction'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('kernel_json');p.add_argument('--out')
 arg=p.parse_args();result=audit(json.loads(Path(arg.kernel_json).read_text()))
 if arg.out:Path(arg.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
