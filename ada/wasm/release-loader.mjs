// ADA-296N .dlw — source-addressed public release boundary.
import {loadKernel} from "./loader.mjs";
export async function loadRelease(commit){
 if(!/^[a-f0-9]{40}$/.test(commit))throw Error("Expected lowercase source commit required");
 const base=new URL("./releases/"+commit+"/",import.meta.url);
 const get=async name=>{const r=await fetch(new URL(name,base),{cache:"no-store",redirect:"error"});if(!r.ok)throw Error(name+": HTTP "+r.status);return r.json()};
 const [m,p,s,c]=await Promise.all(["manifest.json","parity.json","reference-schema.json","chromium.json"].map(get));
 if(m.source_commit!==commit||p.status!=="PASS"||p.checks!==57933||p.tolerance!==1e-12||!Number.isFinite(p.maxError)||p.maxError<0||p.maxError>1e-12||["status","checks","tolerance","maxError","host"].some(k=>p[k]!==m.parity?.[k]))throw Error("Release parity rejected");
 if(s.status!=="PASS"||s.checks!==20||s.valid!==6||s.rejected!==14)throw Error("Release reference schema rejected");
 const groups=["compiled initialization and geometry","24 sequential appends and inheritance","persistent reload and identical ancestry","missing asset rejected","corrupt asset rejected"];
 if(c.status!=="PASS"||c.source!==commit||c.sha256!==m.sha256||JSON.stringify(c.checks)!==JSON.stringify(groups))throw Error("Release Chromium receipt rejected");
 const kernel=await loadKernel(base,commit);
 if(kernel.sha256!==m.sha256||kernel.bytes!==m.bytes)throw Error("Release changed during verification");
 return kernel;
}
