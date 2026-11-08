import test from "node:test";
import assert from "node:assert/strict";
import {
 composeSentenceBox,recoverSentenceBox,expandSentenceBox,verifySentenceBox
} from "../language/sentence-box.mjs";

test("exact sentence case punctuation whitespace and order roundtrips",()=>{
 for(const input of [
  "", "QUANTA.", "Quanta travels.", "Hello, world!",
  "Why? Because it can.", "A  B", "Q, T, Z.",
  "Fold (Q) to Z; observe: one dot.", "Wait... Go!", "A-B", "'Q' is a letter.",
  "The Chrome Dot: fold, move, return!"
 ]){
  const packet=composeSentenceBox(input,{context:"geometric transport"});
  assert.equal(recoverSentenceBox(packet),input);
  assert.equal(verifySentenceBox(packet).pass,true);
  for(const level of [1,2,3,4])assert.equal(expandSentenceBox(packet,level).source,input);
 }
});
test("sentence phrase phases accumulate across words and reset on end marks",()=>{
 const p=composeSentenceBox("Q A BC. T Z!");
 const w=p.tokens.filter(t=>t.kind==="word");
 assert.deepEqual(w.map(t=>[t.raw,t.phase,t.entryPhase,t.exitPhase]),[
  ["Q","a",0,1],["A","b",1,2],["BC","c",2,0],
  ["T","a",0,1],["Z","b",1,2]
 ]);
 const glyphs=expandSentenceBox(p,4).items.filter(x=>x.kind==="glyph");
 assert.deepEqual(glyphs.map(g=>g.degrees),[0,90,180,270,0,90]);
});
test("relational addresses linked between words inside sentences only",()=>{
 const p=composeSentenceBox("ONE TWO. THREE FOUR?");
 const w=p.tokens.filter(t=>t.kind==="word");
 assert.deepEqual(w.map(t=>[t.relation.follows,t.relation.precedes]),[
 [null,1],[0,null],[null,3],[2,null]]);
});
test("semantic identity and somatic actions survive level-one dots",()=>{
 const p=composeSentenceBox("Q tail.");
 const full=expandSentenceBox(p,4),min=expandSentenceBox(p,1);
 assert.equal(min.items.filter(t=>t.kind==="glyph").length,5);
 assert.equal(min.items[0].view.kind,"chrome-dot");
 assert.ok(full.somatic.some(v=>v.verb==="DRAW"));
 assert.equal(recoverSentenceBox(p),"Q tail.");
});
test("tampered phases punctuation and case are rejected",()=>{
 const p=composeSentenceBox("Quanta? Yes.");
 const t=[...p.tokens];t[0]={...t[0],entryPhase:1};
 assert.equal(verifySentenceBox({...p,tokens:t}).pass,false);
 const q=[...p.tokens];const boundary=q.findIndex(x=>x.kind==="punctuation");
 q[boundary]={...q[boundary],action:"MARK"};
 assert.equal(verifySentenceBox({...p,tokens:q}).pass,false);
 const f=[...p.tokens];f[0]={...f[0],caseMask:"111111"};
 assert.equal(verifySentenceBox({...p,tokens:f}).pass,false);
});
test("unsupported glyphs and oversized sentences fail closed",()=>{
 for(const v of ["😃","a\nb","ok_why","A".repeat(513),"3D"]){
  assert.throws(()=>composeSentenceBox(v),TypeError);
 }
});
