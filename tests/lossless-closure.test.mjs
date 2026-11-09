import test from "node:test";
import assert from "node:assert/strict";
import {instantiate84211,append84211,FACES} from "../language/byzantine-84211.mjs";
import {close84211,recover84211,verifyLossless84211,demo84211} from "../language/lossless-closure.mjs";
const copy=x=>JSON.parse(JSON.stringify(x));
test("8 to 4 to 2 to 1 to 1 is exactly preserved",()=>{
 const source=demo84211(),p=close84211(source);
 assert.deepEqual(p.stages.map(x=>x.length),[8,4,2,1,1]);
 assert.deepEqual(p.stages[3],p.stages[4]);
 assert.deepEqual(recover84211(p),source);
 assert.equal(verifyLossless84211(p).pass,true);
});
test("all four sealed chambers retain 24 faces, statements and judge verdict",()=>{
 const p=close84211(demo84211()),r=recover84211(p);
 assert.deepEqual(r.actors.map(a=>a.faces.length),[6,6,6,6]);
 assert.deepEqual(r.actors.map(a=>a.id),["AaaA","BbbB","CccC","DddD"]);
 assert.equal(r.ruling.outcome,"insufficient");
 assert.equal(p.stages[0].length,8);
});
test("reject unsealed chamber even when other players sealed",()=>{
 let s=instantiate84211();
 for(const face of FACES)s=append84211(s,{kind:"face",actor:"AaaA",face});
 s=append84211(s,{kind:"seal",actor:"AaaA",statement:"a",source:"source"});
 assert.throws(()=>close84211(s),/four chambers/);
});
test("reject four sealed chambers without a judge verdict",()=>{
 const s=demo84211(),x=copy(s);
 x.events.pop();x.ruling=null;
 assert.throws(()=>close84211(x),/ruling/);
});
test("reject hidden mutation to leaf or folded child",()=>{
 const p=close84211(demo84211());
 for(const edit of [x=>x.stages[0][1].value.statement="changed",x=>x.stages[1][0].children[0].value="fake",x=>x.stages[4][0].children.pop()]){
  const x=copy(p);edit(x);assert.equal(verifyLossless84211(x).pass,false);
 }
});
test("reject changed source ledger, missing witness, and final stage rewrite",()=>{
 const p=close84211(demo84211());
 for(const edit of [x=>x.ledgerEvents[0].face="-z",x=>x.source.actors[0].statement="rewritten",x=>x.stages[4][0].kind="changed",x=>x.widths[0]=7]){
  const x=copy(p);edit(x);assert.equal(verifyLossless84211(x).pass,false);
 }
});
test("folding does not mutate original and independent copies recover deterministically",()=>{
 const a=demo84211(),prior=copy(a),p=close84211(a),again=close84211(a);
 assert.deepEqual(a,prior);assert.deepEqual(p,again);
 assert.notStrictEqual(p.source,a);
});
test("nested reference preserves all eight leaves in order",()=>{
 const p=close84211(demo84211()),flatten=n=>n.kind==="pair"?n.children.flatMap(flatten):[n];
 assert.deepEqual(flatten(p.stages[4][0]),p.stages[0]);
});
