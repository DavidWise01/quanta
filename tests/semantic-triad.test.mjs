import test from "node:test";
import assert from "node:assert/strict";
import {SEMANTIC_ALPHABET,TRIAD_ROLES,semanticTriad,semanticRole,semanticTriadText,recoverSemanticTriadText} from "../language/semantic-triad.mjs";
test("26 alphabet letters each have exactly three SEE/DO/LEARN roles",()=>{
 assert.equal(SEMANTIC_ALPHABET.length,26);
 assert.deepEqual(TRIAD_ROLES,["see","do","learn"]);
 assert.equal(SEMANTIC_ALPHABET.flatMap(x=>x.terms).length,78);
 for(const x of SEMANTIC_ALPHABET)for(const value of x.terms)assert.equal(value[0].toUpperCase(),x.letter);
});
test("A maps Alarm Action Achieve",()=>{
 assert.deepEqual(semanticTriad("A").terms,["Alarm","Action","Achieve"]);
});
test("all first letters address their immutable semantic triads",()=>{
 for(const x of SEMANTIC_ALPHABET){
  assert.equal(semanticTriad(x.letter),x);
  for(const role of TRIAD_ROLES)assert.equal(semanticRole(x.letter,role),x.roles[role]);
  assert.ok(Object.isFrozen(x));
 }
});
test("source word and spaces are exactly reconstructible",()=>{
 for(const text of ["","A","QUANTA","Q T Z","ALARM ACTION ACHIEVE"]){
  const frame=semanticTriadText(text);
  assert.equal(recoverSemanticTriadText(JSON.parse(JSON.stringify(frame))),text);
 }
});
test("modified terms or order rejected, unsupported source refused",()=>{
 const p=semanticTriadText("ABC");
 assert.throws(()=>recoverSemanticTriadText({...p,items:[...p.items].reverse()}));
 assert.throws(()=>semanticTriad("a"),TypeError);
 assert.throws(()=>semanticRole("A","other"),TypeError);
 assert.throws(()=>semanticTriadText("abc"),TypeError);
});
