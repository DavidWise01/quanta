import test from "node:test";
import assert from "node:assert/strict";
import {
 fold128,unfold128,exportFold128,importFold128,validateFold128,FOLD_WIDTHS,FOLD_CHUNKS
} from "../language/recoverable-fold.mjs";
test("all zero, all one, alternating and patterned 128-bit sources round trip",()=>{
 const source=[
  "0".repeat(128),"1".repeat(128),"01".repeat(64),"10".repeat(64),
  Array.from({length:128},(_,i)=>(i%11===0||i%13===0)?"1":"0").join("")
 ];
 for(const bits of source){
  const f=fold128(bits);
  assert.equal(f.display.length,1);
  assert.equal(unfold128(f),bits);
  assert.equal(validateFold128(f).pass,true);
  assert.deepEqual(f.stages.map(x=>x.outputWidth),FOLD_WIDTHS);
  assert.equal(f.stages.slice(1,8).reduce((n,x)=>n+x.witness.length,0),127);
  assert.equal(f.stages[7].output,f.stages[8].output);
  assert.equal(f.stages[8].operation,"fixed-point");
  assert.ok(Object.isFrozen(f));
  assert.ok(Object.isFrozen(f.stages));
  assert.ok(Object.isFrozen(f.stages[4]));
 }
});
test("two four-number chunks and one stable terminal",()=>{
 assert.deepEqual(FOLD_CHUNKS,[[128,64,32,16],[8,4,2,1],[1]]);
 assert.equal(FOLD_WIDTHS.join(","),"128,64,32,16,8,4,2,1,1");
});
test("compact terminal+witness frame reconstructs full 128-bit source",()=>{
 const source="00110111".repeat(16);
 const framed=exportFold128(fold128(source));
 assert.equal(framed.terminal.length,1);
 assert.deepEqual(framed.witness.map(x=>x.length),[64,32,16,8,4,2,1]);
 assert.equal(framed.witness.join("").length,127);
 const recovered=importFold128(JSON.parse(JSON.stringify(framed)));
 assert.equal(unfold128(recovered),source);
});
test("tampering a stage is detected against recorded source lineage",()=>{
 const s=fold128("11001001".repeat(16));
 const stages=[...s.stages];
 stages[5]={...stages[5],witness:(stages[5].witness[0]==="0"?"1":"0")+stages[5].witness.slice(1)};
 assert.equal(validateFold128({...s,stages}).pass,false);
});
test("incomplete witness is rejected",()=>{
 const frame=exportFold128(fold128("0".repeat(128)));
 assert.throws(()=>importFold128({...frame,witness:frame.witness.slice(1)}));
 assert.throws(()=>importFold128({...frame,terminal:"?"}));
});
test("all 128 single-bit sources are recovered without colliding",()=>{
 for(let i=0;i<128;i++){
  const chars=Array(128).fill("0");chars[i]="1";
  const input=chars.join("");
  const frame=exportFold128(fold128(input));
  assert.equal(unfold128(importFold128(frame)),input);
 }
});
