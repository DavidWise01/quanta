import test from "node:test";
import assert from "node:assert/strict";
import {composeParagraphBox,recoverParagraphBox,expandParagraphBox,verifyParagraphBox}
 from "../language/paragraph-box.mjs";
test("exact multiline paragraph roundtrip",()=>{
 for(const text of [
  "", "\n", "\n\n", "QUANTA.","Quanta folds. The dot survives!",
  "Quanta folds.\nThe dot survives.\nThen it unfolds?",
  "One  two... Three!", "A.\n\nB.", "QUANTA\nGLOBULE\nCHROME DOT",
  "Fold (Q), move Z; return!", "Hello, world! One dot? Yes."
 ]){
  const p=composeParagraphBox(text,{context:"QG-019 context"});
  assert.equal(recoverParagraphBox(p),text);
  assert.equal(verifyParagraphBox(p).pass,true);
  for(const level of [1,2,3,4])assert.equal(expandParagraphBox(p,level).source,text);
 }
});
test("distinct sentence transport fragments link across explicit LF",()=>{
 const p=composeParagraphBox("One. Two?\nThree!\nFour.");
 const fragments=p.records.filter(r=>r.type==="sentence");
 assert.deepEqual(fragments.map(r=>r.raw),["One."," Two?","Three!","Four."]);
 assert.deepEqual(fragments.map(r=>r.relation.previous),[null,0,1,2]);
 assert.deepEqual(fragments.map(r=>r.relation.next),[1,2,3,null]);
 assert.equal(p.lineCount,3);
 assert.equal(p.records.filter(r=>r.type==="linebreak").length,2);
});
test("fold level one has a dot per Latin letter and full recovery",()=>{
 const p=composeParagraphBox("Q has a tail.\nA box carries Z.");
 const unfolded=expandParagraphBox(p,4),folded=expandParagraphBox(p,1);
 assert.equal(folded.items.reduce((n,x)=>n+x.dotCount,0),
              unfolded.items.reduce((n,x)=>n+x.glyphCount,0));
 assert.ok(unfolded.somatic.some(v=>v.verb==="DRAW"));
 assert.equal(recoverParagraphBox(p),"Q has a tail.\nA box carries Z.");
});
test("paragraph context preserved without claims of intrinsic semantics",()=>{
 const p=composeParagraphBox("Q. T.",{context:"letters interpreted by reader"});
 assert.equal(p.context,"letters interpreted by reader");
 assert.ok(p.records.filter(r=>r.type==="sentence").every(r=>r.contextRef==="paragraph-context"));
});
test("tampered sentence, line index, or relation rejected",()=>{
 const p=composeParagraphBox("One.\nTwo.");
 for(const change of [
  r=>({...r,raw:"Oops."}),
  r=>({...r,lineIndex:999}),
  r=>({...r,relation:{...r.relation,next:999}})
 ]){
  const records=[...p.records],index=records.findIndex(r=>r.type==="sentence");
  records[index]=change(records[index]);
  assert.equal(verifyParagraphBox({...p,records}).pass,false);
 }
});
test("reject invalid source chars / oversized paragraph",()=>{
 for(const text of ["A😀","é","Hello\r\nWorld","1+1","A".repeat(4097)]){
  assert.throws(()=>composeParagraphBox(text),TypeError);
 }
});
test("long valid line splits into 512-char reversible sentence blocks",()=>{
 const p=composeParagraphBox("A".repeat(1100));
 assert.equal(p.segmentCount,3);
 assert.equal(recoverParagraphBox(p),"A".repeat(1100));
});
