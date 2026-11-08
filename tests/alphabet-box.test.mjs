import test from "node:test";
import assert from "node:assert/strict";
import {
 alphabet,pathsFor,tokenFor,parseToken,rotatePoint,transportLetter,recoverLetter,transportText,recoverText,
 QUADS,LEVELS,BOX_CARRIER
} from "../language/alphabet-box.mjs";

test("entire A–Z alphabet is instantiated and each token is in a |||| carrier",()=>{
 assert.equal(alphabet().join(""),"ABCDEFGHIJKLMNOPQRSTUVWXYZ");
 assert.equal(BOX_CARRIER,"||||");
 for(const ch of alphabet()){
   assert.equal(parseToken(tokenFor(ch)),ch);
   assert.ok(pathsFor(ch).length>=1);
   const p=transportLetter(ch);
   assert.equal(p.token,"||"+ch+"||");
   assert.equal(recoverLetter(p).letter,ch);
 }
});
test("four quads advance by 90° and each contains levels 4→3→2→1",()=>{
 for(const ch of alphabet()){
  const p=transportLetter(ch);
  assert.deepEqual(p.quads.map(x=>[x.name,x.degrees]),[["a",0],["b",90],["c",180],["d",270]]);
  for(const q of p.quads){
   assert.deepEqual(q.levels.map(x=>x.level),LEVELS);
   assert.ok(q.somatic.some(x=>x.verb==="DRAW"));
   assert.equal(q.levels[3].view.kind,"chrome-dot");
  }
 }
 assert.deepEqual(QUADS.map(x=>x.name),["a","b","c","d"]);
});
test("four 90° rotations return each source vertex exactly",()=>{
 for(const ch of alphabet()) for(const stroke of pathsFor(ch)) for(const point of stroke){
   let p=point;
   for(let i=0;i<4;i++)p=rotatePoint(p,90);
   assert.deepEqual(p,point);
 }
});
test("phase and verb tampering is detected against canonical glyph geometry",()=>{
 const q=transportLetter("Q",{meaning:"question"});
 assert.equal(q.semantic.meaning,"question");
 assert.ok(q.quads[0].geometry.length>1); // includes the Q tail
 assert.ok(q.quads[0].somatic.some(x=>x.verb==="TURN"));
 assert.throws(()=>recoverLetter({...q,quads:q.quads.slice(1)}));
 const altered=[...q.quads];
 altered[1]={...altered[1],degrees:180};
 assert.throws(()=>recoverLetter({...q,quads:altered}));
 const p=transportLetter("T");
 const tamper=[...p.quads];tamper[2]={...tamper[2],somatic:[]};
 assert.throws(()=>recoverLetter({...p,quads:tamper}));
});
test("text transport reconstructs alphabet and arbitrary uppercase strings",()=>{
 for(const text of ["","Q","TZ","ABCDEFGHIJKLMNOPQRSTUVWXYZ","AZAZAZ","QUANTA"]){
  const stream=transportText(text);
  assert.equal(recoverText(stream),text);
  assert.equal(stream.packets.length,text.length);
 }
});
test("lowercase, unsupported code points and malformed tokens are rejected",()=>{
 assert.throws(()=>transportText("abc"),TypeError);
 assert.throws(()=>transportText("HI!"),TypeError);
 assert.throws(()=>transportText("A".repeat(1025)),TypeError);
 assert.throws(()=>parseToken("||a||"),TypeError);
 assert.throws(()=>transportLetter("a"),TypeError);
});
