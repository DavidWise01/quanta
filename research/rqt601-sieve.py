#!/usr/bin/env python3
"""RQT-601 exact family 28 modular seed sieve. Python 3 standard library.
Usage: python rqt601-sieve.py RQT-595-results.json [OUTPUT.json]
"""
import hashlib,json,math,sys
from pathlib import Path
source=Path(sys.argv[1]);raw=source.read_bytes();d=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=="5e68fddb78395b02f5cc4f6cbdd5c4c3cfc341b1ed036d86174175b9e7aee699"
assert d["selected_family_index"]==28
A,B,C,D=[int(d[k]) for k in "ABCD"];assert B*B-4*A*C==D
primes=[31,29,7,17,19,23,5,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
bound=1000000;width=2*bound+1
mask=bytearray(b"\x01")*width;ledger=[]
for p in primes:
 squares={j*j%p for j in range(p)}
 good=[t for t in range(p) if (A*t*t+B*t+C)%p in squares]
 for bad in set(range(p))-set(good):
  start=(bad+bound)%p
  count=(width-1-start)//p+1 if start<width else 0
  if count: mask[start::p]=b"\x00"*count
 ledger.append({"prime":p,"allowed_t_mod_p":sorted(good),"remaining":mask.count(1)})
assert ledger[0]["allowed_t_mod_p"]==[12] and ledger[0]["remaining"]==64516
assert ledger[22]["prime"]==103 and ledger[22]["remaining"]==0
assert mask.count(1)==0
out={"rqt":601,"family_index":28,"source_sha256":hashlib.sha256(raw).hexdigest(),
"window":[-bound,bound],"tested":width,"gates":ledger,
"survivors":0,"square_hits":0,"new_all_scale_exclusions":0,
"selected_excluded":82,"selected_unresolved":53,"wall_22d":"NOT REPLAYED","root19":"OPEN"}
Path(sys.argv[2] if len(sys.argv)>2 else "RQT-601-results.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS RQT-601: 2,000,001 integers, 26 prime gates, zero survivors; finite certificate only.")
