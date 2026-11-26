# ADA-295N .dlw — validate accepted package before append-only publication.
import hashlib,json,pathlib,sys,re
p=pathlib.Path(sys.argv[1]); m=json.loads((p/"manifest.json").read_text())
r=json.loads((p/"parity.json").read_text()); s=json.loads((p/"reference-schema.json").read_text()); c=json.loads((p/"chromium.json").read_text())
b=(p/"ada_browser.wasm").read_bytes()
def require(ok,msg):
    if not ok: raise SystemExit(msg)
require(m.get("schema")=="ADA-281N.package.v1" and m.get("authority")=="OBSERVE_ONLY","manifest schema")
require(re.fullmatch("[a-f0-9]{40}",m.get("source_commit","")) and m["source_commit"]==sys.argv[2],"source mismatch")
require(m.get("double_build_equal") is True and m.get("sha256")==hashlib.sha256(b).hexdigest() and m.get("bytes")==len(b) and b[:8]==b"\x00asm\x01\x00\x00\x00","binary mismatch")
require(r==m.get("parity") and r.get("status")=="PASS" and r.get("checks")==57933 and r.get("tolerance")==1e-12 and 0<=r.get("maxError",float("inf"))<=1e-12,"parity mismatch")
require(s.get("status")=="PASS" and s.get("checks")==20 and s.get("valid")==6 and s.get("rejected")==14,"schema regression mismatch")
require(c.get("status")=="PASS" and c.get("source")==m["source_commit"] and c.get("sha256")==m["sha256"] and c.get("checks")==["compiled initialization and geometry","24 sequential appends and inheritance","persistent reload and identical ancestry","missing asset rejected","corrupt asset rejected"],"Chromium mismatch")
# ADA-312N .dlw: exact recursive JSON type and value comparison.
def exact(actual,expected):
    if type(actual) is not type(expected): return False
    if isinstance(expected,dict): return actual.keys()==expected.keys() and all(exact(actual[k],v) for k,v in expected.items())
    if isinstance(expected,list): return len(actual)==len(expected) and all(exact(x,y) for x,y in zip(actual,expected))
    return actual==expected
# ADA-309N: require transaction evidence in addition to the original gate.
t=json.loads((p/"ledger-contention.json").read_text())
a=json.loads((p/"ledger-abort.json").read_text())
require(t.get("status")=="PASS" and t.get("scope")=="synthetic kernel; real IndexedDB; two connections" and exact(t.get("result"),{"commits":1,"rejections":1,"staleRejected":True,"recovered":1,"generations":[0,1],"linked":True}),"contention receipt rejected")
require(a.get("status")=="PASS" and a.get("scope")=="synthetic kernel; real IndexedDB; explicit transaction abort" and exact(a.get("result"),{"inserted":True,"aborted":True,"rejected":True,"invalidated":True,"before":[0],"genesisPreserved":True,"after":[0,1],"linked":True,"retryPreserved":True}),"abort receipt rejected")
# ADA-313N: source and binary binding; not independent attestation.
binding=m.get("transaction_sources")
require(type(binding) is dict and set(binding)=={"ledger","contention","abort"} and all(type(v) is str and re.fullmatch("[a-f0-9]{64}",v) for v in binding.values()),"transaction source inventory rejected")
for receipt,kind in [(t,"contention"),(a,"abort")]:
    require(exact(receipt.get("binding"),{"source":m["source_commit"],"binary":m["sha256"],"ledger":binding["ledger"],"harness":binding[kind]}),"transaction ancestry rejected")
print(m["source_commit"])
