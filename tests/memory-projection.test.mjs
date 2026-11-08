import test from "node:test";
import assert from "node:assert/strict";
import {instantiateCorpusMemory,appendCorpusRevision} from "../language/corpus-memory.mjs";
import {projectCorpusRevision,unfoldCorpusProjection,walkRevisionHistory,walkParagraphProjection,verifyCorpusProjection,PROJECTION_LEVELS}
 from "../language/memory-projection.mjs";

const source=(text="A dot begins.")=>({title:"QUANTA",documents:[{
 id:"quanta",title:"QUANTA",chapters:[{id:"zero",title:"Zero",sections:[
 {id:"opening",title:"Opening",paragraphs:[text,"The box remembers."]}
 ]}]}]}],references:[]});
const address="doc/quanta/ch/zero/sec/opening/p/0";
function memory(){
 let m=instantiateCorpusMemory(source(),"First dot");
 m=appendCorpusRevision(m,source("The dot now folds."),{comment:"The fold"});
 m=appendCorpusRevision(m,source("The original returns."),{comment:"The return"});
 return m;
}
test("one terminal Chrome Dot selects one specific corpus revision",()=>{
 const m=memory();
 for(const id of ["r0000","r0001","r0002"]){
  const p=projectCorpusRevision(m,id);
  assert.deepEqual(p.terminal,{kind:"chrome-dot",glyph:"•",revision:id});
  assert.equal(p.revision,id);
  assert.equal(p.metrics.paragraphs,2);
  assert.equal(verifyCorpusProjection(m,p).pass,true);
 }
});
test("all versions unfold exactly while retaining earlier source",()=>{
 const m=memory();
 for(const [id,text] of [["r0000","A dot begins."],["r0001","The dot now folds."],["r0002","The original returns."]]){
  const p=projectCorpusRevision(m,id);
  const out=unfoldCorpusProjection(m,p);
  assert.equal(out.source.documents[0].chapters[0].sections[0].paragraphs[0],text);
 }
 assert.equal(m.revisions.length,3);
});
test("backward history walks to initial revision in order",()=>{
 const list=walkRevisionHistory(memory(),"r0002");
 assert.deepEqual(list.map(x=>x.revision),["r0002","r0001","r0000"]);
 assert.deepEqual(list.map(x=>x.parent),["r0001","r0000",null]);
 assert.equal(list[0].changes.some(x=>x.change==="edited"),true);
});
test("a paragraph source address traces backward through revisions",()=>{
 const chain=walkParagraphProjection(memory(),"r0002",address);
 assert.deepEqual(chain.map(x=>x.revision),["r0002","r0001","r0000"]);
 assert.deepEqual(chain.map(x=>x.address),[address,address,address]);
});
test("visual 4→3→2→1 phases do not erase source",()=>{
 const m=memory(),p=projectCorpusRevision(m,"r0001");
 assert.deepEqual(PROJECTION_LEVELS,[4,3,2,1]);
 assert.deepEqual(p.phases.map(x=>x.level),[4,3,2,1]);
 assert.equal(p.phases[3].dots,p.metrics.letters);
 assert.equal(p.phases[0].dots,0);
 assert.equal(unfoldCorpusProjection(m,p).revision,"r0001");
});
test("tampering with projection, witness, phase or revision rejected",()=>{
 const m=memory(),p=projectCorpusRevision(m,"r0001");
 for(const changed of [
  {...p,revision:"r9999"},
  {...p,witness:{...p.witness,parent:"r9999"}},
  {...p,terminal:{...p.terminal,revision:"r0000"}},
  {...p,phases:[...p.phases].reverse()}
 ]) assert.equal(verifyCorpusProjection(m,changed).pass,false);
});
test("empty corpus can be projected and unfolded",()=>{
 const m=instantiateCorpusMemory({title:"Empty",documents:[],references:[]});
 const p=projectCorpusRevision(m,"r0000");
 assert.equal(p.metrics.letters,0);
 assert.equal(verifyCorpusProjection(m,p).pass,true);
 assert.equal(unfoldCorpusProjection(m,p).source.title,"Empty");
});
