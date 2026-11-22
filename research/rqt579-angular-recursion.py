#!/usr/bin/env python3
"""RQT-579 lossless triple-nested angular recursion audit. Run standalone."""
import itertools
from pathlib import Path
import json
R=60
values=[0,1,-1,59,60,61,-59,-60,-61,3599,3600,3601,-3599,-3600,-3601,10**18,-10**18,359343129,-359343129]
def enc(value,n):
 digits=[]
 for _ in range(n):
  value,r=divmod(value,R);digits.append(r)
 return digits,value
def dec(digits,tail):
 for d in reversed(digits):tail=R*tail+d
 return tail
count=0
for container,address,depth,value in itertools.product(['brace','box','torroid'],['y','m','d','h','mi','s','deg','am','as'],range(1,8),values):
 digits,tail=enc(value,depth)
 assert dec(digits,tail)==value
 assert all(0<=x<60 for x in digits)
 assert enc(dec(digits,tail),depth)==(digits,tail)
 count+=1
assert count==3591
print('RQT-579 PASS 3591 reversible address checks; symbolic recursion only; Root19 OPEN')
