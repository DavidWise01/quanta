#!/usr/bin/env python3
"""RQT-600: exact continued-fraction checkpoint replay plus fast Fibonacci bound.
Usage: python rqt600.py RQT-599-results.json RQT-597-results.json [out.json]
"""
import sys,json,math,hashlib
from pathlib import Path
p599,p597=map(Path,sys.argv[1:3]);s=json.loads(p599.read_text());r=json.loads(p597.read_text())
d=int(r["squarefree_D"])
assert d==int(s["squarefree_d"])==3580734425344222227352852171253793
assert math.isqrt(d)**2!=d
N=int(s["continued_fraction_steps"]);assert N==2000000 and s["period_closed"] is False
m,q,a=0,1,math.isqrt(d);a0=a;checkpoints={}
for n in range(1,N+1):
 m=q*a-m
 numerator=d-m*m
 assert numerator>0 and numerator%q==0
 q=numerator//q;a=(a0+m)//q
 assert q>0 and a>0 and a!=2*a0
 if str(n) in s["checkpoints"]:
  checkpoints[str(n)]={"m":str(m),"q":str(q),"a":str(a)}
  assert checkpoints[str(n)]==s["checkpoints"][str(n)]
assert len(checkpoints)==4
def fib(n):
 x,y=0,1
 for b in bin(n)[2:]:
  c=x*(2*y-x);z=x*x+y*y
  x,y=(z,c+z) if b=="1" else (c,z)
 return x
f=fib(N+1)
assert f.bit_length()==1388484 and 10**417975<=f<10**417976
# If L>N is the sqrt(d) CF period, the first +1 Pell solution occurs at
# index L-1 (L even) or 2L-1 (L odd); hence index>=N.
# Its denominator y>=F_(N+1), because CF partial quotients>=1.
out={"rqt":600,"family":28,"squarefree_d":str(d),"replayed_cf_steps":N,"checkpoints":checkpoints,"no_period_closure":True,"fibonacci_index":N+1,"fibonacci_bits":f.bit_length(),"fundamental_y_minimum_digits":417976,"bound":"y >= F_2000001 >= 10^417975","integral_unit":"NOT CONSTRUCTED","seed":"NOT FOUND","excluded_selected":82,"unresolved_selected":53,"wall22d":"NOT REPLAYED","root19":"OPEN","sha256_rqt599":hashlib.sha256(p599.read_bytes()).hexdigest(),"sha256_rqt597":hashlib.sha256(p597.read_bytes()).hexdigest()}
Path(sys.argv[3] if len(sys.argv)>3 else "RQT-600-results.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS: 2M CF steps, all 4 checkpoints, exact 417976-digit lower bound, root19 OPEN")
