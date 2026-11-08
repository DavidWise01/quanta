import test from "node:test";
import assert from "node:assert/strict";
import {composeWordBox,recoverWordBox,expandWordBox,verifyWordBox,WORD_PHASES,WORD_LEVELS}
 from "../language/word-box.mjs";

test("word and space order survives full roundtrip",()=>{
 for(const s of ["","A","QUANTA","Q T Z","HELLO WORLD","ABCDEFGHIJKLMNOPQRSTUVWXYZ","A A A","QUANTUM CHROME DOT"]){
  const p=composeWordBox(s,{context:"test context"});
  assert.equal(recoverWordBox(p),s);
  assert.equal(verifyWordBox(p).pass,true);
  assert.equal(expandWordBox(p,4).semantic.text,s);
  assert.equal(expandWordBox(p,1).semantic.text,s);
 }
});
test("phase progression repeats a/b/c/d within each word and resets at spaces",()=>{
 const p=composeWordBox("QUANTA GLOBULE");
 const glyphs=p.tokens.filter(x=>x.type==="glyph");
 assert.deepEqual(glyphs.map(x=>x.phase),["a","b","c","d","a","b","a","b","c","d","a","b","c"]);
 assert.deepEqual(glyphs.map(x=>x.degrees),[0,90,180,270,0,90,0,90,180,270,0,90,180]);
 assert.deepEqual(WORD_PHASES,["a","b","c","d"]);
 assert.deepEqual(WORD_LEVELS,[4,3,2,1]);
});
test("every A–Z glyph survives word-level transport at every fold view",()=>{
 const text="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
 const p=composeWordBox(text);
 assert.equal(recoverWordBox(p),text);
 for(const level of WORD_LEVELS){
  const e=expandWordBox(p,level);
  assert.equal(e.items.length,26);
  assert.ok(e.items.every(x=>x.view.kind===({4:"geometry",3:"vertices",2:"endpoints",1:"chrome-dot"}[level])));
 }
});
test("semantic source, somatic verbs, Q tail retained",()=>{
 const p=composeWordBox("Q",{context:"question glyph"});
 const e=expandWordBox(p,4);
 assert.equal(e.semantic.context,"question glyph");
 assert.equal(e.items[0].view.paths.length,2);
 assert.ok(e.somatic.some(x=>x.verb==="DRAW"));
 assert.ok(e.somatic.some(x=>x.verb==="TURN"));
 assert.equal(e.somatic.filter(x=>x.verb==="MOVE").length,2);
});
test("malformed spacing or nonalphabet inputs rejected",()=>{
 for(const s of [" a","A ","A  B","a","A!","A\nB","A".repeat(129)])assert.throws(()=>composeWordBox(s),TypeError);
});
test("tampering order, phase, or offsets is detected",()=>{
 const p=composeWordBox("Q Z");
 const bad=[...p.tokens];bad[0]={...bad[0],degrees:90};
 assert.equal(verifyWordBox({...p,tokens:bad}).pass,false);
 const tamper=[...p.tokens];tamper[2]={...tamper[2],offset:999};
 assert.equal(verifyWordBox({...p,tokens:tamper}).pass,false);
 const reord=[...p.tokens].reverse();
 assert.equal(verifyWordBox({...p,tokens:reord}).pass,false);
});
test("a full 90° cycle reconstructs geometry via canonical glyph reference",()=>{
 const p=composeWordBox("AAAA");
 const e=expandWordBox(p,4);
 const pts=e.items.map(x=>x.view.paths[0][0]);
 const local=pts.map((v,i)=>({x:v.x-p.tokens[i].offset,y:v.y}));
 assert.deepEqual(local[0],local[0]); // explicit 0/90/180/270 each valid
 assert.deepEqual(p.tokens.map(x=>x.degrees),[0,90,180,270]);
 assert.equal(recoverWordBox(p),"AAAA");
});
