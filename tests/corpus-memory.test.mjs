import test from "node:test";
import assert from "node:assert/strict";
import {instantiateCorpusMemory,appendCorpusRevision,recoverCorpusRevision,lookupCorpusAtRevision,traceCorpusLineage,verifyCorpusMemory} from "../language/corpus-memory.mjs";
const base="doc/book/ch/zero/sec/opening/p/";
function initial(){return {title:"QUANTA",documents:[{id:"book",title:"Book",chapters:[{id:"zero",title:"Zero",sections:[{id:"opening",title:"Opening",paragraphs:["The first dot.","Fold and return."]}]}]}],references:[]}}
test("append is immutable and all revisions recover",()=>{
 const m0=instantiateCorpusMemory(initial()),next=initial();
 next.documents[0].chapters[0].sections[0].paragraphs[0]="The revised dot.";
 const m1=appendCorpusRevision(m0,next,{comment:"Revise source"});
 assert.equal(verifyCorpusMemory(m1).pass,true);
 assert.equal(m0.revisions.length,1);assert.equal(m1.revisions.length,2);
 assert.equal(m1.revisions[1].parent,"r0000");
 assert.equal(lookupCorpusAtRevision(m1,"r0000",base+"0").text,"The first dot.");
 assert.equal(lookupCorpusAtRevision(m1,"r0001",base+"0").text,"The revised dot.");
 assert.ok(Object.isFrozen(m1));assert.ok(Object.isFrozen(m1.revisions));
});
test("edited, created, unchanged and retired states",()=>{
 const m0=instantiateCorpusMemory(initial()),next=initial();
 next.documents[0].chapters[0].sections[0].paragraphs=["The first dot.","Changed text.","Third created."];
 const m1=appendCorpusRevision(m0,next);
 assert.deepEqual(m1.revisions[1].lineage.map(x=>x.change),["unchanged","edited","created"]);
 const back=initial();back.documents[0].chapters[0].sections[0].paragraphs=["The first dot."];
 const m2=appendCorpusRevision(m1,back);
 assert.equal(m2.revisions[2].lineage.filter(x=>x.change==="retired").length,2);
});
test("explicit moved paragraph lineage can be traced backward",()=>{
 let memory=instantiateCorpusMemory(initial()),next=initial();
 next.documents[0].chapters[0].id="origin";
 const to="doc/book/ch/origin/sec/opening/p/0";
 memory=appendCorpusRevision(memory,next,{lineage:[{from:base+"0",to}]});
 assert.equal(verifyCorpusMemory(memory).pass,true);
 assert.deepEqual(traceCorpusLineage(memory,"r0001",to).map(x=>x.address),[to,base+"0"]);
 assert.equal(recoverCorpusRevision(memory,"r0000").documents[0].chapters[0].id,"zero");
});
test("duplicate or unknown explicit lineage refused",()=>{
 const m=instantiateCorpusMemory(initial());
 assert.throws(()=>appendCorpusRevision(m,initial(),{lineage:[{from:base+"0",to:"missing"}]}));
 assert.throws(()=>appendCorpusRevision(m,initial(),{lineage:[{from:base+"0",to:base+"0"},{from:base+"0",to:base+"1"}]}));
});
test("parent, lineage or nested snapshot tampering fails",()=>{
 let m=instantiateCorpusMemory(initial());m=appendCorpusRevision(m,initial());
 let entries=[...m.revisions];entries[1]={...entries[1],parent:"wrong"};
 assert.equal(verifyCorpusMemory({...m,revisions:entries}).pass,false);
 entries=[...m.revisions];entries[1]={...entries[1],lineage:[]};
 assert.equal(verifyCorpusMemory({...m,revisions:entries}).pass,false);
 entries=[...m.revisions];entries[1]={...entries[1],snapshot:{...entries[1].snapshot,totalParagraphs:999}};
 assert.equal(verifyCorpusMemory({...m,revisions:entries}).pass,false);
});
test("serialize and recover exact version snapshots",()=>{
 let m=instantiateCorpusMemory(initial()),next=initial();
 next.documents[0].chapters[0].sections[0].paragraphs.push("Third source.");
 m=appendCorpusRevision(m,next);
 const cloned=JSON.parse(JSON.stringify(m));
 assert.equal(verifyCorpusMemory(cloned).pass,true);
 assert.deepEqual(recoverCorpusRevision(cloned,"r0001"),next);
 assert.deepEqual(recoverCorpusRevision(cloned,"r0000"),initial());
});
test("empty source evolves into full corpus",()=>{
 let m=instantiateCorpusMemory({title:"Empty",documents:[],references:[]});
 m=appendCorpusRevision(m,initial());
 assert.equal(verifyCorpusMemory(m).pass,true);
 assert.equal(m.revisions[1].snapshot.totalParagraphs,2);
});
