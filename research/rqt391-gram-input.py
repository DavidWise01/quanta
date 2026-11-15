#!/usr/bin/env python3
"""Stream original F4 rank-three Gram to RQT391 C++ exact scanner."""
import json,sys
with open(sys.argv[1]) as f:d=json.load(f)
Q=[[int(x) for x in row] for row in d.get('restricted_F4_Gram',d.get('restricted_Gram'))]
assert len(Q)==3 and all(len(row)==3 for row in Q)
assert all(Q[i][j]==Q[j][i] for i in range(3) for j in range(3))
assert all(Q[i][i]%2==0 for i in range(3))
for i,j in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2)):
 print(Q[i][j])
