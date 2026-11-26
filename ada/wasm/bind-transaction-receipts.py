# ADA-313N .dlw — attach checked-out source identity after successful test execution.
import hashlib,json,os,pathlib,sys
p=pathlib.Path(sys.argv[1])
m=json.loads((p/"manifest.json").read_text())
assert m["source_commit"]==os.environ["GITHUB_SHA"]
assert m["sha256"]==hashlib.sha256((p/"ada_browser.wasm").read_bytes()).hexdigest()
sources={"ledger":"ledger-incremental.mjs","contention":"ledger-contention.test.mjs","abort":"ledger-abort.test.mjs"}
actual={k:hashlib.sha256((pathlib.Path(__file__).parent/v).read_bytes()).hexdigest() for k,v in sources.items()}
assert actual==m["transaction_sources"]
for kind in ("contention","abort"):
    f=p/("ledger-"+kind+".json")
    r=json.loads(f.read_text())
    assert r["status"]=="PASS" and "binding" not in r
    r["binding"]={"source":m["source_commit"],"binary":m["sha256"],"ledger":actual["ledger"],"harness":actual[kind]}
    f.write_text(json.dumps(r,indent=2)+"\n")
