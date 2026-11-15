#!/usr/bin/env python3
"""RQT-386 verified first exact original F4 norm-minus-two root candidate.
EXPLICIT witness, NOT yet certified as the eighteenth frozen reflection.
SymPy required. Run: python research/rqt386-exact-null-and-root-candidate.py
"""
import itertools,json,math
import sympy as s
from sympy.ntheory.modular import crt
from sympy.ntheory import sqrt_mod
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
H=s.Matrix([[2261695329309210454,-1051245631696015003,1175645097188971547,1627042015946053765],[-1188134889995383173,3351801182310041338,491285385866907237,-2161158408172372287],[1246578957491359670,693903984986601793,2635043040004191520,-2244501232348113591],[1482429990082813264,-2257268153558244069,-2405192609807710046,6186706227706453238]])
assert H.det()==1 and H+H.T==-F
T=s.Matrix([[-194,0,0],[0,1,0],[195,0,0],[0,0,1]])
V=s.Matrix([[1,3,1],[-25,-74,-24],[113,340,113]])
A=V.T*T.T*F*T*V
p=-int(A[0,0]);q=-int(A[0,2]);g0=int(A[0,1]);g1=int(A[2,1])
D=p*(-int(A[2,2]))-q*q;gamma=p*g1-q*g0;Delta=D//4;C=p*int(A.det())
primes=[223,281297,419697635024167,10343190029259773932231107365537334388821979446373]
P=math.prod(primes)
assert C==24*P and D==4*Delta
rootmods=[int(sqrt_mod(-Delta,t)) for t in primes]
R,mod=crt(primes,rootmods);assert mod==P
def dot(x,y):return x[0]*y[0]+Delta*x[1]*y[1]
def near(n,d):return (2*n+d)//(2*d) if n>=0 else -near(-n,d)
def gauss(a,b):
 while True:
  if dot(b,b)<dot(a,a):a,b=b,a
  c=near(dot(a,b),dot(a,a))
  if c==0:
   assert 2*abs(dot(a,b))<=dot(a,a)<=dot(b,b)
   return a,b
  b=(b[0]-c*a[0],b[1]-c*a[1])
a,b=gauss((P,0),(int(R),1))
alpha=474649450978634736175766122678998
beta=222309235551026216137681687722434
h=74247063525679595379713821277894166492373
assert (dot(a,a)//P)*alpha**2+2*(dot(a,b)//P)*alpha*beta+(dot(b,b)//P)*beta**2==24*h*h
M=a[0]*alpha+b[0]*beta
B=a[1]*alpha+b[1]*beta
assert M*M+Delta*B*B==C*h*h
L=s.Rational(B,2)
y=s.Rational(M+gamma*h,D)
x=(L+g0*h-q*y)/p
# Correct ternary order is (x,h,y), NOT (h,x,y).
zrat=[x,s.Rational(h),y]
mul=s.ilcm(*(v.q for v in zrat))
z=[int(t*mul) for t in zrat];gg=math.gcd(*z);z=[t//gg for t in z]
u=T*V*s.Matrix(z)
assert (u.T*F*u)[0]==0 and math.gcd(*map(int,u))==1
fu=F*u
assert math.gcd(*map(int,fu))==1
# Exact integer Bezout coefficients for u.T F v =1.
coeff=[];d=0
for component in fu:
 i,j,k=map(int,s.gcdex(d,int(component)))
 coeff=[i*t for t in coeff]+[j];d=k
assert d==1
bez=s.Matrix(coeff)
def half(v):
 n=int((v.T*F*v)[0]);assert n%2==0;return n//2
def parity(v):return ''.join(str(int(x)%2) for x in v)
options=[]
for digits in itertools.product(range(4),repeat=4):
 v0=s.Matrix(digits)
 if int((u.T*F*v0)[0])%4!=1:continue
 if parity((1+half(v0))*u-v0)=='0111':
  options.append(v0);break
assert options
v0=options[0];n=int((u.T*F*v0)[0]);v=v0+4*((1-n)//4)*bez
assert (u.T*F*v)[0]==1
root=(1+half(v))*u-v
assert (root.T*F*root)[0]==-2
assert (root.T*H*root)[0]==1 and parity(root)=='0111'
assert math.gcd(*map(int,root))==1
print(json.dumps({
 'rqt':386,'status':'EXACT ORIGINAL F4 NULL AND NORM -2 ROOT CANDIDATE VERIFIED',
 'plane':'194/195','original_null_u':[str(int(t)) for t in u],
 'original_null_norm':0,'pairing_divisibility':1,
 'bezout_partner_v':[str(int(t)) for t in v],
 'pairing_u_F_v':1,'root_candidate_r':[str(int(t)) for t in root],
 'root_F_norm':-2,'root_H_self':1,'root_parity':'0111',
 'frozen_17_predecessor_compatibility':'NOT VERIFIED',
 'reflection_18':'CANDIDATE, NOT CERTIFIED POSITION 18',
 'roots_19_20_21':'OPEN'},indent=2))
