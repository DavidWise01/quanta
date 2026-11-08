import test from "node:test";
import assert from "node:assert/strict";
import {
 instantiateGrowth,growCorpusBranch,convergeGrowthBranches,recoverGrowthNode,
 traceGrowthAncestors,inspectGrowthGraph,verifyGrowthGraph
} from "../language/memory-growth.mjs";
const addr="doc/quanta/ch/zero/sec/opening/p/0";
function source(a="The dot begins.",b="The box remembers."){
 const section={id:"opening",title:"Opening",paragraphs:[a,b]};
 const chapter={id:"zero",title:"Zero",sections:[section]};
 const doc={id:"quanta",title:"QUANTA",chapters:[chapter]};
 return {title:"QUANTA",documents:[doc],references:[]};
}
function forks(){
 let graph=instantiateGrowth(source(),"Origin");
 graph=growCorpusBranch(graph,"n0000",source("Left branch."),"Left");
 graph=growCorpusBranch(graph,"n0000",source(undefined,"Right branch."),"Right");
 return graph;
}
test("two independent child nodes converge, then grow again",()=>{
 let graph=forks();
 graph=convergeGrowthBranches(graph,"n0001","n0002");
 assert.equal(verifyGrowthGraph(graph).pass,true);
 assert.equal(graph.nodes[3].kind,"convergence");
 assert.deepEqual(graph.nodes[3].parents,["n0001","n0002"]);
 assert.equal(graph.nodes[3].base,"n0000");
 assert.deepEqual(recoverGrowthNode(graph,"n0003"),source("Left branch.","Right branch."));
 graph=growCorpusBranch(graph,"n0003",source("New generation.","Right branch."));
 assert.deepEqual(recoverGrowthNode(graph,"n0004"),source("New generation.","Right branch."));
 assert.equal(recoverGrowthNode(graph,"n0000").documents[0].chapters[0].sections[0].paragraphs[0],"The dot begins.");
});
test("repeated divergence after a convergence reaches a second two-parent node",()=>{
 let g=convergeGrowthBranches(forks(),"n0001","n0002");
 g=growCorpusBranch(g,"n0003",source("Second left.","Right branch."));
 g=growCorpusBranch(g,"n0003",source("Left branch.","Second right."));
 g=convergeGrowthBranches(g,"n0004","n0005");
 assert.equal(g.nodes[6].base,"n0003");
 assert.deepEqual(recoverGrowthNode(g,"n0006"),source("Second left.","Second right."));
 assert.deepEqual(traceGrowthAncestors(g,"n0006").map(n=>n.id),
 ["n0006","n0005","n0004","n0003","n0002","n0001","n0000"]);
 assert.equal(inspectGrowthGraph(g).convergences,2);
});
test("same-address divergent edits refuse convergence until explicitly resolved",()=>{
 let g=instantiateGrowth(source());
 g=growCorpusBranch(g,"n0000",source("Left!"));
 g=growCorpusBranch(g,"n0000",source("Right!"));
 assert.throws(()=>convergeGrowthBranches(g,"n0001","n0002"),/Unresolved conflict/);
 const next=convergeGrowthBranches(g,"n0001","n0002",{[addr]:{choice:"custom",text:"A resolved path."}});
 assert.equal(recoverGrowthNode(next,"n0003").documents[0].chapters[0].sections[0].paragraphs[0],"A resolved path.");
});
test("dangling, repeated and forward parents cannot enter graph",()=>{
 const g=forks();
 assert.throws(()=>growCorpusBranch(g,"n9999",source()),/Unknown parent/);
 assert.throws(()=>convergeGrowthBranches(g,"n0001","n0001"),/distinct parents/);
 assert.equal(verifyGrowthGraph({...g,nodes:[...g.nodes,{...g.nodes[2],parents:["n9999"]}]}).pass,false);
 assert.equal(verifyGrowthGraph({...g,nodes:[...g.nodes,{...g.nodes[2],id:"n0007"}]}).pass,false);
});
test("modification of convergence parent, base or merged snapshot is detected",()=>{
 const g=convergeGrowthBranches(forks(),"n0001","n0002");
 for(const patch of [{base:"n0001"},{parents:["n0000","n0002"]},
   {snapshot:{...g.nodes[3].snapshot,totalParagraphs:999}}]){
  const nodes=[...g.nodes];nodes[3]={...nodes[3],...patch};
  assert.equal(verifyGrowthGraph({...g,nodes}).pass,false);
 }
});
test("JSON serialization retains exact graph and sources",()=>{
 const g=convergeGrowthBranches(forks(),"n0001","n0002");
 const replay=JSON.parse(JSON.stringify(g));
 assert.equal(verifyGrowthGraph(replay).pass,true);
 assert.deepEqual(recoverGrowthNode(replay,"n0001"),source("Left branch."));
 assert.deepEqual(recoverGrowthNode(replay,"n0002"),source(undefined,"Right branch."));
});
test("empty corpus and graph heads remain addressable",()=>{
 let g=instantiateGrowth({title:"Empty",documents:[],references:[]});
 assert.equal(verifyGrowthGraph(g).pass,true);
 g=growCorpusBranch(g,"n0000",source());
 assert.deepEqual(inspectGrowthGraph(g).heads,["n0001"]);
 assert.equal(inspectGrowthGraph(g).edges,1);
 assert.equal(recoverGrowthNode(g,"n0000").title,"Empty");
});
