// ADA-199N: execute the shipped simulation cores of all eight ADA Phase II HTML labs.
// Run: node ada/ada-199n-eight-lab-core-test.mjs
// This validates deterministic logic, not WebGL or GitHub Pages delivery.
import fs from "node:fs";
import vm from "node:vm";
import assert from "node:assert/strict";

const labs=[
["191N","ada-191n-integrated-living-lab.html","// 3D adapter.",
 "reset();for(let i=0;i<100;i++)step();const v=replay();({pass:v.ok,ticks:tick,events:events.length})"],
["192N","ada-192n-unified-observation-3d.html","// 3D adapter.",
 "reset();for(let i=0;i<100;i++)step();const v=verify();({pass:v.ok,ticks:tick,events:ledger.length})"],
["193N","ada-193n-persistent-3d-memory.html","// Visual adapter:",
 "archive=makeArchive();model=genesis();for(let i=0;i<100;i++)model=applyTick(model,archive.events);updateCheckpoint();const v=verify(archive);({pass:v.verified,ticks:v.ticks,events:v.events})"],
["194N","ada-194n-3d-adaptive-learning.html","// Renderer:",
 "data=make();for(let i=0;i<100;i++)tickOnce(data);const v=replay(data);({pass:v.passed,ticks:v.ticks,events:v.events})"],
["195N","ada-195n-3d-failure-repair.html","// 3D graphics:",
 "state=create();for(let i=0;i<100;i++)tickOnce(state);const v=verify(state);({pass:v.passed,ticks:v.ticks,events:v.events})"],
["196N","ada-196n-unified-three-contact-3d.html","// Visual rendering",
 "data=newModel('cycle');for(let i=0;i<100;i++)stepOnce(data);const v=verify(data);({pass:v.passed,ticks:v.ticks,events:v.records})"],
["197N","ada-197n-best-policy-3d.html","// Graphics independent",
 "model=create('cycle',2,15);for(let i=0;i<100;i++)tickOnce(model);const v=verify(model);({pass:v.passed,ticks:v.ticks,events:v.ledgerRecords})"],
["198N","ada-198n-3d-stress-recovery.html","// Visual layer:",
 "model=create('shock',198000,15,2);for(let i=0;i<100;i++)tickOnce(model);const v=replay(model);({pass:v.passed,ticks:v.ticks,events:v.decisionCount})"]
];
const results=[];
for(const [name,file,splitter,exercise] of labs){
 const html=fs.readFileSync(new URL("./"+file,import.meta.url),"utf8");
 const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
 assert.ok(script,name+": script missing");
 const core=script.split(splitter)[0];
 const elements=new Map();
 const document={
  getElementById(id){
   if(!elements.has(id))elements.set(id,{value:{threshold:"12",window:"18",severeLimit:"15",switchCost:"2",cost:"2",environment:"cycle",regime:"shock",policy:"best"}[id]||"cycle",innerHTML:"",textContent:"",className:"",style:{},onclick:null,onchange:null,addEventListener(){}});
   return elements.get(id);
  },
  createElement(){return {style:{},click(){},addEventListener(){}}}
 };
 const localStorage={getItem(){return null},setItem(){}};
 const context=vm.createContext({document,localStorage,window:{},console,Math,JSON,clearInterval(){},setTimeout(){}});
 const stub=name==="192N"?"function syncScene(){}\n":"";
 const outcome=vm.runInContext(core+"\n"+stub+exercise,context,{timeout:20000});
 assert.equal(outcome.pass,true,name+" replay failed");
 assert.equal(outcome.ticks,100,name+" unexpected tick count");
 if(name==="197N"){
  const causal=vm.runInContext('({first:model.events[0]?.type,second:model.events[1]?.type,causal:model.cycles.every((c,i)=>model.events[2*i]?.type==="single-action"&&model.events[2*i+1]?.type==="observation"&&model.events[2*i]?.source_id===model.events[2*i+1]?.source_id)})',context);
  assert.equal(causal.first,"single-action","ADA-197N must decide before observing");
  assert.equal(causal.second,"observation","ADA-197N must then observe");
  assert.equal(causal.causal,true,"ADA-197N must preserve pre-observation action order");
 }
 results.push({lab:name,...JSON.parse(JSON.stringify(outcome))});
 console.log(name+": PASS ("+outcome.events+" events)");
}
console.log(JSON.stringify({schema:"ADA-199N.eight-core.v1",category:"simulation-core-not-browser",passed:results.length,total:labs.length,results},null,2));
