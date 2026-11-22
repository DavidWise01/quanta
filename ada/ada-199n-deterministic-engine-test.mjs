// ADA-199N deterministic engine regression suite. Run: node ada/ada-199n-deterministic-engine-test.mjs
// Executes the ADA-198N simulation core; not a browser/WebGL/Pages verification.
import fs from "node:fs";
import vm from "node:vm";
import assert from "node:assert/strict";
const html=fs.readFileSync(new URL("./ada-198n-3d-stress-recovery.html",import.meta.url),"utf8");
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script,"ADA-198N script exists");
const core=script.split("// Visual layer:")[0];
assert.ok(core.includes("function replay(m)")&&core.includes("function tickOnce(m)"));
const els=new Map();
const document={getElementById(id){if(!els.has(id))els.set(id,{value:id==="threshold"?"15":id==="cost"?"2":"shock",textContent:"",innerHTML:"",style:{},onclick:null,onchange:null});return els.get(id)}};
const context=vm.createContext({document,console,Math,JSON});
const code=core+String.raw`
const outcomes=[];
for(const regime of ["shock","noise","drift","cost"])for(let i=0;i<4;i++){
 const seed=198000+i*311,engine=create(regime,seed,15,2);
 advance(engine,140);
 const proof=replay(engine);
 if(!proof.passed||proof.sourceCount!==140||proof.decisionCount!==140)throw Error("Replay failed "+regime);
 if(engine.records.some((r,j)=>r.tick!==j+1||r.source_id!==engine.source[j].id))throw Error("Source mismatch");
 if(engine.records.some(r=>!P.includes(r.ada.selected)))throw Error("Invalid policy");
 const independent=create(regime,seed,15,2);advance(independent,140);
 if(JSON.stringify(engine.records)!==JSON.stringify(independent.records))throw Error("Non-deterministic results");
 outcomes.push({...summary(engine),replayPassed:true});
}
outcomes;`;
const rows=vm.runInContext(code,context,{timeout:20000});
assert.equal(rows.length,16);
const result={schema:"ADA-199N.engine-test.v1",engine:"ADA-198N",category:"deterministic-simulation",runs:16,passed:16,groups:{}};
for(const regime of ["shock","noise","drift","cost"]){
 const matches=rows.filter(x=>x.regime===regime);
 result.groups[regime]={runs:matches.length,baselineMAE:matches.reduce((s,x)=>s+x.baselineMAE,0)/matches.length,adaptiveMAE:matches.reduce((s,x)=>s+x.adaptiveMAE,0)/matches.length,baselineSevere:matches.reduce((s,x)=>s+x.baselineSevere,0),adaptiveSevere:matches.reduce((s,x)=>s+x.adaptiveSevere,0),switchingCost:matches.reduce((s,x)=>s+x.switchCost,0)};
}
assert.equal(rows.every(x=>x.replayPassed),true);
assert.equal(result.groups.shock.runs,4);
assert.ok(result.groups.noise.baselineSevere>0);
console.log(JSON.stringify(result,null,2));
