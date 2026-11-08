import test from "node:test";
import assert from "node:assert/strict";
import {SEMANTIC_ALPHABET} from "../language/semantic-triad.mjs";
import {phaseStation} from "../language/sexagesimal-ring.mjs";
import {bindSemanticLetter,recoverSemanticLetter,bindSemanticText,recoverSemanticText,verifySemanticBinding} from "../language/semantic-ring.mjs";
test("all 78 semantic roles bind to 60 stations at valid quarter-turn phases",()=>{
 let terms=0;
 for(const entry of SEMANTIC_ALPHABET)for(let q=0;q<4;q++){
  const p=bindSemanticLetter(entry.letter,q);
  assert.equal(recoverSemanticLetter(p),entry.letter);
  assert.deepEqual(p.roles.map(r=>r.role),["see","do","learn"]);
  assert.deepEqual(p.roles.map(r=>r.term),entry.terms);
  assert.equal(new Set(p.roles.map(r=>r.station)).size,3);
  for(let i=0;i<3;i++){
   const role=p.roles[i];
   assert.equal(role.phase,(q+i)%4);
   assert.equal(role.station,phaseStation(role.anchorHome,role.phase));
   assert.equal(role.glyph.phase.index,role.phase);
  }
  if(q===0)terms+=p.roles.length;
 }
 assert.equal(terms,78);
});
test("A is Alarm, Action, Achieve with exact phase progression",()=>{
 const p=bindSemanticLetter("A",0);
 assert.deepEqual(p.roles.map(r=>r.term),["Alarm","Action","Achieve"]);
 assert.deepEqual(p.roles.map(r=>r.phase),[0,1,2]);
});
test("DO retains canonical ordered movement verbs while SEE and LEARN remain observations",()=>{
 for(const letter of ["A","Q","Z"]){
  const p=bindSemanticLetter(letter,2);
  assert.equal(p.roles[0].verbs.length,0);
  assert.ok(p.roles[1].verbs.some(v=>v.verb==="DRAW"));
  assert.equal(p.roles[2].verbs.length,0);
  assert.ok(p.roles[1].glyph.geometry.length>=1);
 }
});
test("full phrase recovery preserves spaces and per-letter phase",()=>{
 for(const text of ["","A","QUANTA BOX","ABCDEFGHIJKLMNOPQRSTUVWXYZ","A  Q"]){
  const p=bindSemanticText(text);
  assert.equal(recoverSemanticText(JSON.parse(JSON.stringify(p))),text);
  const report=verifySemanticBinding(p);
  assert.equal(report.pass,true);
  assert.equal(report.roles,report.letters*3);
 }
 assert.deepEqual(bindSemanticText("AB C").items.filter(x=>x.kind==="letter").map(x=>x.binding.entryPhase),[0,1,0]);
});
test("editing terms, positions, verbs or role order invalidates the witness",()=>{
 const p=bindSemanticText("A");
 const clone=JSON.parse(JSON.stringify(p));
 clone.items[0].binding.roles[1].term="Altered";
 assert.equal(verifySemanticBinding(clone).pass,false);
 const alt=JSON.parse(JSON.stringify(p));
 alt.items[0].binding.roles[2].station=59;
 assert.equal(verifySemanticBinding(alt).pass,false);
 const verbs=JSON.parse(JSON.stringify(p));
 verbs.items[0].binding.roles[1].verbs=[];
 assert.equal(verifySemanticBinding(verbs).pass,false);
});
test("invalid glyphs and out of range phases are rejected",()=>{
 assert.throws(()=>bindSemanticLetter("a"),TypeError);
 assert.throws(()=>bindSemanticLetter("A",4),RangeError);
 assert.throws(()=>bindSemanticText("A!"),TypeError);
 assert.throws(()=>bindSemanticText("A".repeat(129)),TypeError);
});
