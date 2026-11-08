import test from "node:test";import assert from "node:assert/strict";
import {composeRootChase,recoverRootChase,verifyRootChase} from "../language/chasing-roots.mjs";
const url="https://collection.sciencemuseumgroup.org.uk/people/cp38764/ada-lovelace";
function fixture(){
 const society={id:"ada-1843",letter:"A",subject:"Ada Lovelace",
  is:"Mathematical writer",was:"Studied mathematics and worked with Charles Babbage",
  whichMeans:"Her notes explored the Analytical Engine's wider possibilities",
  wasYear:1833,context:{year:1843,timezone:"Europe/London",place:"London",group:"Computing scholarship"},
  weight:{authority:2,reach:2,legacy:4,confidence:0.7,basis:"Illustrative assigned ordinal"},
  evidence:[{label:"Museum biography",url}],status:"sourced"};
 return {society,target:"interpretation",nodes:[
  {id:"interpretation",statement:society.whichMeans,role:"conclusion",year:1843,status:"annotated",requires:["notes","engine"],evidence:[]},
  {id:"notes",statement:"Notes were published in 1843",role:"prerequisite",year:1843,status:"sourced",requires:["study"],evidence:[{label:"Biography",url}]},
  {id:"engine",statement:"An Analytical Engine was proposed",role:"prerequisite",year:1837,status:"sourced",requires:[],evidence:[{label:"Museum",url}]},
  {id:"study",statement:"She studied mathematics",role:"prerequisite",year:1833,status:"unknown",requires:[],evidence:[]}
 ]};
}
test("chases which-means through exact ordered dependencies to earliest roots",()=>{
 const packet=composeRootChase(fixture());
 assert.equal(verifyRootChase(packet).pass,true);
 assert.deepEqual(packet.trace.order.map(n=>n.id),["interpretation","notes","study","engine"]);
 assert.deepEqual(packet.trace.roots,["study","engine"]);
 assert.deepEqual(packet.trace.gaps.map(n=>n.id),["study"]);
 assert.equal(packet.trace.reachable,4);
});
test("social claim and all 60-ring phase witnesses recover exactly",()=>{
 const f=fixture(),packet=composeRootChase(f);
 assert.deepEqual(packet.phases.map(p=>p.quad),["a","b","c"]);
 assert.equal(new Set(packet.phases.map(p=>p.station)).size,3);
 const source=recoverRootChase(JSON.parse(JSON.stringify(packet)));
 assert.deepEqual(source.claim,f.society);
 assert.equal(verifyRootChase(packet).interpretationProven,false);
});
test("reused prerequisites form a DAG, not an artificial duplicate tree",()=>{
 const f=fixture();f.nodes[2].requires=["study"];f.nodes[2].year=1843;
 const p=composeRootChase(f);
 assert.equal(p.trace.reachable,4);
 assert.deepEqual(p.trace.roots,["study"]);
});
test("cycles, dangling links and later prerequisites refused",()=>{
 for(const change of [
  f=>{f.nodes[3].requires=["interpretation"]},
  f=>{f.nodes[0].requires=["nonexistent"]},
  f=>{f.nodes[1].year=1831}
 ]){const f=fixture();change(f);assert.throws(()=>composeRootChase(f))}
});
test("unlinked facts flagged; no false proof from uncited leaves",()=>{
 const f=fixture();f.nodes.push({id:"unlinked",statement:"Unrelated observation",role:"prerequisite",year:1800,status:"annotated",requires:[],evidence:[]});
 const p=composeRootChase(f);assert.deepEqual(p.trace.unlinked,["unlinked"]);
 assert.deepEqual(p.trace.gaps.map(x=>x.id),["study"]);
});
test("tampered source, claimed evidence or history invalidates the packet",()=>{
 const p=composeRootChase(fixture());
 for(const mutate of [
  c=>{c.trace.roots=[]},
  c=>{c.nodes[2].evidence[0].url="https://example.org"},
  c=>{c.phases[2].station=59},
  c=>{c.society.claim.context.year=1800}
 ]){const c=JSON.parse(JSON.stringify(p));mutate(c);assert.equal(verifyRootChase(c).pass,false)}
});
test("status source requirements, target consistency and bounded inputs checked",()=>{
 for(const change of [
  f=>{f.nodes[2].evidence=[]},
  f=>{f.nodes[0].statement="Wrong interpretation"},
  f=>{f.nodes[0].requires.push("notes")},
  f=>{f.nodes[1].status="inherently-true"}
 ]){const f=fixture();change(f);assert.throws(()=>composeRootChase(f))}
});
