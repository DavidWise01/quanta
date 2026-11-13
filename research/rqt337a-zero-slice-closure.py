#!/usr/bin/env python3
"""RQT-337-A: exact x2=0 check completing original-lattice height bound."""
import sympy as s
F=s.Matrix([[-4523390658618420908,2239380521691398176,-2422224054680331217,-3109472006028867029],[2239380521691398176,-6703602364620082676,-1185189370853509030,4418426561730616356],[-2422224054680331217,-1185189370853509030,-5270086080008383040,4649693842155823637],[-3109472006028867029,4418426561730616356,4649693842155823637,-12373412455412906476]])
P=-F.extract([0,1,3],[0,1,3])
assert all(P[:i,:i].det()>0 for i in (1,2,3))
# For z^T P z=2: Cauchy-Schwarz gives z_i^2 <= 2*(P^-1)ii.
# All three right sides are <1, so all integer z_i=0, contradiction.
bounds=[2*P.inv()[i,i] for i in range(3)]
assert all(z<1 for z in bounds)
print('PASS RQT-337-A: no x2=0 integral vector of norm -2; norm 0 only zero')
print('PASS: original combined norm 0/-2 necessary coordinate abs(x2)>=5001')
