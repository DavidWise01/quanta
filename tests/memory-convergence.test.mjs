import test from "node:test";
import assert from "node:assert/strict";
import {instantiateCorpusMemory,appendCorpusRevision,recoverCorpusRevision}
 from "../language/corpus-memory.mjs";
import {compareCorpusBranches,convergeCorpusMemory,recoverCorpusConvergence,verifyCorpusConvergence}
 from "../language/memory-convergence.mjs";
const addr=i=>"doc/quanta/ch/zero/sec/opening/p/"+i;
function source(first="The dot begins.",second="The box remembers."){
 const section={id:"opening",title:"Opening",paragraphs:[first,second]};
 const chapter={id:"zero",title:"Zero",sections:[section]};
 const document={id:"quanta",title:"QUANTA",chapters:[chapter]};
 return {title:"QUANTA",documents:[document],references:[]};
}
function branchPair(leftSource,rightSource){
 const root=instantiateCorpusMemory(source(),"common origin");
 const left=appendCorpusRevision(root,leftSource,{comment:"left branch"});
 const right=appendCorpusRevision(root,rightSource,{comment:"right branch"});
 return {root,left,right};
}
test("independent edits to different paragraphs converge without conflict",()=>{
 const {left,right,root}=branchPair(source("Left changed."),source(undefined,"Right changed."));
 const compared=compareCorpusBranches(left,right);
 assert.equal(compared.ancestor,"r0000");
 assert.deepEqual(compared.conflicts,[]);
 assert.equal(compared.ready,true);
 const out=convergeCorpusMemory(left,right);
 const recovered=recoverCorpusConvergence(out);
 assert.deepEqual(recovered,source("Left changed.","Right changed."));
 assert.equal(verifyCorpusConvergence(out).pass,true);
 assert.equal(recoverCorpusRevision(root,"r0000").documents[0].chapters[0].sections[0].paragraphs[0],"The dot begins.");
 assert.equal(out.branches.left.revisions.length,2);
 assert.equal(out.branches.right.revisions.length,2);
});
test("concurrent edits to same source address remain unresolved until explicit selection",()=>{
 const {left,right}=branchPair(source("Left choice."),source("Right choice."));
 const compared=compareCorpusBranches(left,right);
 assert.deepEqual(compared.conflicts,[addr(0)]);
 assert.equal(compared.ready,false);
 assert.throws(()=>convergeCorpusMemory(left,right),/Unresolved conflict/);
 for(const [choice,expected] of [["left","Left choice."],["right","Right choice."],["base","The dot begins."]]){
  const merged=convergeCorpusMemory(left,right,{[addr(0)]:{choice}});
  assert.equal(recoverCorpusConvergence(merged).documents[0].chapters[0].sections[0].paragraphs[0],expected);
  assert.equal(verifyCorpusConvergence(merged).pass,true);
 }
 const custom=convergeCorpusMemory(left,right,{[addr(0)]:{choice:"custom",text:"Both voices remain."}});
 assert.equal(recoverCorpusConvergence(custom).documents[0].chapters[0].sections[0].paragraphs[0],"Both voices remain.");
});
test("identical concurrent edits agree automatically",()=>{
 const {left,right}=branchPair(source("Shared change."),source("Shared change."));
 const report=compareCorpusBranches(left,right);
 assert.equal(report.entries[0].status,"agreed");
 assert.equal(report.ready,true);
 assert.equal(verifyCorpusConvergence(convergeCorpusMemory(left,right)).pass,true);
});
test("common ancestor is the latest identical revision prefix, not just a label",()=>{
 const root=instantiateCorpusMemory(source(),"first");
 const common=appendCorpusRevision(root,source("Common next."),{comment:"second"});
 const left=appendCorpusRevision(common,source("Left later."));
 const right=appendCorpusRevision(common,source("Common next.","Right later."));
 assert.equal(compareCorpusBranches(left,right).ancestor,"r0001");
 const out=convergeCorpusMemory(left,right);
 assert.deepEqual(recoverCorpusConvergence(out),source("Left later.","Right later."));
});
test("a coincidentally matching revision ID is not proof of shared history",()=>{
 const left=instantiateCorpusMemory(source("A."),"root");
 const right=instantiateCorpusMemory(source("B."),"root");
 assert.throws(()=>compareCorpusBranches(left,right),/No identical shared ancestor/);
});
test("topology differences and invented resolution addresses are rejected",()=>{
 const {left,right}=branchPair(source("L."),source("R."));
 assert.throws(()=>convergeCorpusMemory(left,right,{"bad/address":{choice:"left"}}),/Unknown conflict/);
 const root=branchPair(source("L."),source("R.")).root;
 const changed=source();changed.documents[0].chapters[0].sections[0].paragraphs.push("Extra.");
 const other=appendCorpusRevision(root,changed);
 assert.throws(()=>compareCorpusBranches(left,other),/matching paragraph addresses/);
});
test("corrupted retained branches and changed merge output fail replay",()=>{
 const {left,right}=branchPair(source("L."),source("R."));
 const record=convergeCorpusMemory(left,right,{[addr(0)]:{choice:"left"}});
 assert.equal(verifyCorpusConvergence({...record,parents:{left:"r9999",right:"r0001"}}).pass,false);
 const edited={...record,records:record.records.slice(1)};
 assert.equal(verifyCorpusConvergence(edited).pass,false);
 const fake={...record,merged:{...record.merged,totalParagraphs:300}};
 assert.equal(verifyCorpusConvergence(fake).pass,false);
});
