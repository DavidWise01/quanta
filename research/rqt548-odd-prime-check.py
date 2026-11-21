#!/usr/bin/env python3
"""RQT-548: finite-field simultaneous isometry search.
Requires exact historical and new Wall JSON 4x4 matrices as CLI args.
This public reproducer verifies each supplied mod-p witness; the exhaustive
enumeration engine and full JSON are downloadable conversation artifacts.
Usage: python rqt548-odd-prime-check.py hist.json new.json results.json
"""
import json,sys
from pathlib import Path
import sympy as s
Hh=s.Matrix(json.loads(Path(sys.argv[1]).read_text()))
Hn=s.Matrix(json.loads(Path(sys.argv[2]).read_text()))
data=json.loads(Path(sys.argv[3]).read_text())
for item in data['results']:
 p=int(item['prime'])
 for key,mod in [('witness',p),('p2_witness',p*p)]:
  U=s.Matrix(item[key])
  assert U.det()%p!=0
  assert all(int(q)%mod==0 for q in U.T*Hn*U-Hh)
 print('PASS prime',p,'mod-p isometries',item['solutions'],'liftable bases',item['liftable_to_p2'])
print('RQT-548 finite odd-prime Wall isometry certificates verified; global integral equivalence OPEN')
