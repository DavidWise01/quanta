// ADA-322N .dlw — source-addressed public release boundary.
import {strictJSON,requireUnified} from "./strict-release-json.mjs";
import {loadKernel} from "./loader.mjs";
export async function loadRelease(commit){
 if(!/^[a-f0-9]{40}$/.test(commit))throw Error("Expected lowercase source commit required");
 const base=new URL("./releases/"+commit+"/",import.meta.url);
 const get=async name=>{const r=await fetch(new URL(name,base),{cache:"no-store",redirect:"error"});if(!r.ok)throw Error(name+": HTTP "+r.status);return strictJSON(await r.text())};
 const [m,p,s,c,t,a]=await Promise.all(["manifest.json","parity.json","reference-schema.json","chromium.json","ledger-contention.json","ledger-abort.json"].map(get));
 if(m.source_commit!==commit||p.status!=="PASS"||p.checks!==57933||p.tolerance!==1e-12||!Number.isFinite(p.maxError)||p.maxError<0||p.maxError>1e-12||["status","checks","tolerance","maxError","host"].some(k=>p[k]!==m.parity?.[k]))throw Error("Release parity rejected");
 if(s.status!=="PASS"||s.checks!==20||s.valid!==6||s.rejected!==14)throw Error("Release reference schema rejected");
 const groups=["compiled initialization and geometry","24 sequential appends and inheritance","persistent reload and identical ancestry","missing asset rejected","corrupt asset rejected"];
 if(c.status!=="PASS"||c.source!==commit||c.sha256!==m.sha256||JSON.stringify(c.checks)!==JSON.stringify(groups))throw Error("Release Chromium receipt rejected");
 const equal=(actual,expected)=>actual!==null&&typeof actual==="object"&&Object.keys(actual).length===Object.keys(expected).length&&Object.keys(expected).every(k=>JSON.stringify(actual[k])===JSON.stringify(expected[k]));
 if(t.status!=="PASS"||t.scope!=="synthetic kernel; real IndexedDB; two connections"||!equal(t.result,{commits:1,rejections:1,staleRejected:true,recovered:1,generations:[0,1],linked:true}))throw Error("Release contention rejected");
 if(a.status!=="PASS"||a.scope!=="synthetic kernel; real IndexedDB; explicit transaction abort"||!equal(a.result,{inserted:true,aborted:true,rejected:true,invalidated:true,before:[0],genesisPreserved:true,after:[0,1],linked:true,retryPreserved:true}))throw Error("Release recovery rejected");
 const b=m.transaction_sources;
 if(!b||typeof b!=="object"||Object.keys(b).length!==3||!["ledger","contention","abort"].every(k=>typeof b[k]==="string"&&/^[a-f0-9]{64}$/.test(b[k])))throw Error("Transaction source inventory rejected");
 for(const [receipt,kind] of [[t,"contention"],[a,"abort"]]){
  if(!equal(receipt.binding,{source:commit,binary:m.sha256,ledger:b.ledger,harness:b[kind]}))throw Error("Transaction ancestry rejected");
 }
 requireUnified(await get("unified-acceptance.json"),commit,m.sha256);
 const kernel=await loadKernel(base,commit);
 if(kernel.sha256!==m.sha256||kernel.bytes!==m.bytes)throw Error("Release changed during verification");
 return kernel;
}
