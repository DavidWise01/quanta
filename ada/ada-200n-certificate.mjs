// ADA-200N · Evidence-bound release certificate.
// Does not mark a repository phase complete; emits an Actions artifact only after
// both the aggregate gate AND the original reports independently pass.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import assert from "node:assert/strict";

const required=["SOURCE_INTEGRITY","CORE_REPLAY","SEEDED_REPLAY","RENDERER_PROBE","LOCAL","FALLBACK","PUBLIC","PAGES_INTEGRITY"];
const hash=bytes=>crypto.createHash("sha256").update(bytes).digest("hex");
export function validate({gate,manifest,reports,run}){
 assert.equal(gate.schema,"ADA-199N.gate.v2","Gate schema");
 assert.equal(gate.passed,true,"Aggregate gate must pass");
 for(const id of required)assert.equal(gate.outcomes?.[id],"success",id+" must succeed");
 assert.match(run.sha,/^[a-f0-9]{40}$/i,"Workflow commit required");
 assert.match(run.id,/^[0-9]+$/,"Workflow run ID required");
 assert.equal(run.ref,"refs/heads/main","Release must run on main");
 assert.equal(manifest.schema,"ADA-199N.source-integrity.v1");
 assert.equal(Object.keys(manifest.files).length,8,"All eight pinned source roots required");
 const publicBase="https://davidwise01.github.io/quanta";
 const localBase="http://127.0.0.1:8765";
 const sources=Object.entries(manifest.files).sort(([a],[b])=>a.localeCompare(b));
 for(const [file,id] of sources){assert.match(id,/^[a-f0-9]{40}$/);assert.match(file,/^ada\/ada-19[1-8]n-/)}
 for(const key of ["local","fallback","public"]){
   const report=reports[key];
   assert.equal(report.schema,"ADA-199N.smoke.v3",key+" report schema");
   const targetBase=key==="public"?publicBase:localBase;
   assert.equal(report.base,targetBase,key+" report origin");
   assert.equal(report.passed,8,key+" passed count");
   assert.equal(report.failed,0,key+" failure count");
   assert.equal(report.results.length,8,key+" result count");
   assert.equal(report.forceCanvas,key==="fallback",key+" fallback flag");
   assert.equal(report.requireWebGL,key!=="fallback",key+" WebGL requirement");
   assert.equal(new Set(report.results.map(x=>x.version)).size,8,key+" distinct labs");
   for(let i=191;i<=198;i++){
     const lab=report.results.find(x=>x.version===i+"N");
     assert.ok(lab,key+" missing "+i+"N");
     const file=sources.find(([p])=>p.startsWith("ada/ada-"+i+"n-"))?.[0];
     assert.ok(file,key+" source path missing");
     assert.equal(lab.url,targetBase+"/"+file,key+" "+i+"N exact route");
     assert.equal(lab.status,"PASS",key+" "+i+"N status");
     assert.ok(lab.checks?.length>0&&lab.checks.every(x=>x.pass),key+" "+i+"N checks");
   }
 }
 const published=reports.pages;
 assert.equal(published.schema,"ADA-199N.pages-integrity.v1");
 assert.equal(published.base,publicBase,"Published integrity origin");
 assert.equal(published.manifestMatches,true,"Published manifest matches checkout");
 assert.equal(published.success,true,"Published byte-integrity success");
 assert.equal(published.passed,8,"Published source count");
 assert.equal(published.failed,0,"Published source failures");
 assert.equal(published.results.length,8,"Published source records");
 assert.deepEqual(published.results.map(r=>r.path).sort(),sources.map(([file])=>file),"Published paths must be all eight distinct pinned files");
 for(const record of published.results){
   assert.equal(record.pass,true,record.path+" byte integrity");
   assert.equal(record.expected,manifest.files[record.path],record.path+" pinned expectation");
   assert.equal(record.actual,record.expected,record.path+" published hash");
 }
 return {schema:"ADA-200N.release-certificate.v1",state:"EVIDENCE_VALIDATED",scope:"ADA-199N runtime gate and ADA-200N release candidate; NOT an automatic update to public Phase II tracker",phaseCompletionPct:90,run:{id:run.id,attempt:run.attempt,sha:run.sha,ref:run.ref,workflow:run.workflow},checks:required,labCount:8,pinnedSources:sources,reportSummaries:{local:8,fallback:8,public:8,pagesIntegrity:8}};
}
if(process.argv.includes("--self-test")){
 const manifest={schema:"ADA-199N.source-integrity.v1",files:Object.fromEntries(Array.from({length:8},(_,i)=>["ada/ada-"+(i+191)+"n-example.html","a".repeat(40)]))};
 const report=(fallback,base)=>({schema:"ADA-199N.smoke.v3",base,passed:8,failed:0,forceCanvas:fallback,requireWebGL:!fallback,results:Array.from({length:8},(_,i)=>({version:(191+i)+"N",url:base+"/ada/ada-"+(191+i)+"n-example.html",status:"PASS",checks:[{pass:true}]}))});
 const inputs={gate:{schema:"ADA-199N.gate.v2",passed:true,outcomes:Object.fromEntries(required.map(k=>[k,"success"]))},manifest,reports:{local:report(false,"http://127.0.0.1:8765"),fallback:report(true,"http://127.0.0.1:8765"),public:report(false,"https://davidwise01.github.io/quanta"),pages:{schema:"ADA-199N.pages-integrity.v1",base:"https://davidwise01.github.io/quanta",manifestMatches:true,success:true,passed:8,failed:0,results:Object.entries(manifest.files).map(([p,id])=>({path:p,expected:id,actual:id,pass:true}))}},run:{id:"123",attempt:"1",sha:"f".repeat(40),ref:"refs/heads/main",workflow:"ADA-199N"}};
 assert.equal(validate(inputs).state,"EVIDENCE_VALIDATED");
 for(const key of required){const copy=structuredClone(inputs);copy.gate.outcomes[key]="failure";assert.throws(()=>validate(copy),key+" should veto issue")}
 {const copy=structuredClone(inputs);copy.reports.public.results[0].status="FAIL";assert.throws(()=>validate(copy),"Failed browser lab must veto")}
 {const copy=structuredClone(inputs);copy.reports.pages.results[0].actual="b".repeat(40);assert.throws(()=>validate(copy),"Changed public source must veto")}
 {const copy=structuredClone(inputs);copy.run.ref="refs/heads/other";assert.throws(()=>validate(copy),"Non-main branch must veto")}
 {const copy=structuredClone(inputs);copy.reports.pages.results[1]=structuredClone(copy.reports.pages.results[0]);assert.throws(()=>validate(copy),"Duplicate published source must veto")}
 {const copy=structuredClone(inputs);copy.reports.public.base="https://example.invalid";assert.throws(()=>validate(copy),"Wrong public origin must veto")}
 {const copy=structuredClone(inputs);copy.reports.local.results[0].url="http://127.0.0.1:8765/ada/wrong.html";assert.throws(()=>validate(copy),"Wrong browser route must veto")}
 console.log("PASS: valid certificate; eight independent outcome vetoes; browser failure; source drift; non-main branch; duplicate path; wrong origin; wrong route");
}else{
 const base=path.resolve("ada/verification-results");
 const read=p=>JSON.parse(fs.readFileSync(p,"utf8"));
 const run={id:process.env.GITHUB_RUN_ID||"",attempt:process.env.GITHUB_RUN_ATTEMPT||"",sha:process.env.GITHUB_SHA||"",ref:process.env.GITHUB_REF||"",workflow:process.env.GITHUB_WORKFLOW||""};
 const paths={gate:path.join(base,"gate.json"),manifest:"ada/ada-199n-source-integrity.json",local:path.join(base,"local/report.json"),fallback:path.join(base,"fallback/report.json"),public:path.join(base,"public/report.json"),pages:path.join(base,"pages-integrity/report.json")};
 const certificate=validate({gate:read(paths.gate),manifest:read(paths.manifest),reports:{local:read(paths.local),fallback:read(paths.fallback),public:read(paths.public),pages:read(paths.pages)},run});
 certificate.reportSha256=Object.fromEntries(Object.entries(paths).map(([key,file])=>[key,hash(fs.readFileSync(file))]));
 certificate.issuedAt=new Date().toISOString();
 const target=path.join(base,"ada-200n-release-certificate.json");
 fs.writeFileSync(target,JSON.stringify(certificate,null,2)+"\n");
 console.log("ADA-200N VALIDATED certificate:",target);
}
