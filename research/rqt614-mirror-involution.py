#!/usr/bin/env python3
"""RQT-614 exact sign involution of archived Pell corridors.
Usage: python rqt614-mirror-involution.py RQT583.json RQT613.json [OUT.json]
"""
import json,hashlib,sys
from pathlib import Path
p,q=map(Path,sys.argv[1:3]);raw=p.read_bytes();wraw=q.read_bytes()
assert hashlib.sha256(raw).hexdigest()=="5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92"
d=json.loads(raw);w=json.loads(wraw)
assert len(d["equations"])==80 and w["rqt"]==613
bykey={(tuple(e["ray"]),tuple(e["offset"])):e for e in d["equations"]}
assert len(bykey)==80
paired=[];fixed=[];processed=set()
for e in d["equations"]:
 i=e["index"]
 if i in processed:continue
 other=bykey[(tuple(e["ray"]),tuple(-v for v in e["offset"]))]
 j=other["index"]
 assert int(e["A"])==int(other["A"])
 assert int(e["B"])==-int(other["B"])
 assert int(e["C"])==int(other["C"]) and int(e["D"])==int(other["D"])
 for t in (-137,-31,-1,0,1,31,137):
  def delta(s,z):return int(s["A"])*z*z+int(s["B"])*z+int(s["C"])
  assert delta(e,t)==delta(other,-t)
 processed.update([i,j])
 if i==j:fixed.append(i)
 else:paired.append(sorted((i,j)))
assert len(paired)==39 and fixed==[13,67] and len(processed)==80
rw={r["index"]:r for r in w["family_results"]}
for i,j in paired:
 if i in rw and j in rw:
  left,right=rw[i],rw[j]
  assert left["wheel_modulus"]==right["wheel_modulus"]==44051
  assert set(right["wheel_residues"])=={(-t)%44051 for t in left["wheel_residues"]}
  assert right["allowed_t_mod49"]==sorted({(-a)%49 for a in left["allowed_t_mod49"]})
  assert left["final_survivors"]==right["final_survivors"]==[]
assert (2,24) in [tuple(x) for x in paired]
out={"rqt":614,"source_rqt583_sha256":hashlib.sha256(raw).hexdigest(),
"source_rqt613_sha256":hashlib.sha256(wraw).hexdigest(),"archived_equations":80,
"sign_involution_orbits":41,"two_element_orbits":39,"self_mirror_families":fixed,
"pairs":sorted(paired),"mirror_wheel_family_pair":[2,24],
"family_2_and_24_relation":"Q_24(-u,-t)=Q_2(u,t); Delta_24(-t)=Delta_2(t)",
"new_global_exclusions":0,"selected_excluded":82,"selected_unresolved":53,
"wall_22d":"NOT REPLAYED","root19":"OPEN"}
Path(sys.argv[3] if len(sys.argv)>3 else "RQT-614-results.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS: 39 paired mirror orbits and 2 fixed points; no new exclusions")
