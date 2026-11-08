import test from "node:test";
import assert from "node:assert/strict";
import {composeCorpusBox,recoverCorpusBox,lookupCorpus,expandCorpusBox,verifyCorpusBox} from "../language/corpus-box.mjs";
function fixture(){
 return {title:"QUANTA Corpus",documents:[
  {id:"quanta",title:"The Wordle of Space",chapters:[
    {id:"zero",title:"Zero",sections:[{id:"opening",title:"Opening",paragraphs:[
      "The dot begins. The box remembers.","Q returns.\nThe tail survives."
    ]}]},
    {id:"gap",title:"The Gap",sections:[{id:"transport",title:"Language Transport",paragraphs:[
      "A letter carries verbs.","A word carries its phase. A sentence can return!"
    ]}]}
  ]},
  {id:"notes",title:"Companion",chapters:[{id:"symbols",title:"Symbols",sections:[
    {id:"primitive",title:"Primitive",paragraphs:["A dot. An edge. One box."]}
  ]}]}],
  references:[
   {from:"doc/quanta/ch/zero/sec/opening/p/0",to:"doc/quanta/ch/gap/sec/transport/p/0",relation:"continues"},
   {from:"doc/notes/ch/symbols/sec/primitive/p/0",to:"doc/quanta/ch/zero/sec/opening/p/0",relation:"explains"}
  ]};
}
test("corpus exact structured roundtrip and address lookup",()=>{
 const src=fixture(),p=composeCorpusBox(src);
 assert.deepEqual(recoverCorpusBox(p),src);
 assert.equal(verifyCorpusBox(p).pass,true);
 assert.equal(p.totalParagraphs,5);
 assert.equal(p.links.length,2);
 assert.equal(lookupCorpus(p,"doc/quanta/ch/zero/sec/opening/p/1").text,"Q returns.\nThe tail survives.");
});
test("document chapter section order and scoped IDs remain deterministic",()=>{
 const p=composeCorpusBox(fixture());
 assert.deepEqual(p.items.map(x=>x.type),["document","chapter","section","paragraph","paragraph","chapter","section","paragraph","paragraph","document","chapter","section","paragraph"]);
 assert.deepEqual(p.items.map(x=>x.order),Array.from({length:13},(_,i)=>i));
 assert.equal(new Set(p.items.map(x=>x.address)).size,p.items.length);
});
test("all 4 projection levels retain exact source and dot count",()=>{
 const p=composeCorpusBox(fixture()),f=expandCorpusBox(p,4),dots=expandCorpusBox(p,1);
 for(let level=1;level<=4;level++)assert.equal(expandCorpusBox(p,level).items.length,p.items.length);
 assert.equal(f.items.reduce((n,x)=>n+(x.glyphCount||0),0),dots.items.reduce((n,x)=>n+(x.dotCount||0),0));
});
test("references are explicit graph edges and missing targets rejected",()=>{
 const src=fixture();src.references[0].to="doc/quanta/ch/not-there";
 assert.throws(()=>composeCorpusBox(src),/endpoint/);
});
test("mutating a paragraph, reference, metadata or index is detected",()=>{
 const p=composeCorpusBox(fixture());
 const corrupted=[...p.items];corrupted[3]={...corrupted[3],text:"Something else."};
 assert.equal(verifyCorpusBox({...p,items:corrupted}).pass,false);
 assert.equal(verifyCorpusBox({...p,links:[...p.links].reverse()}).pass,false);
 assert.equal(verifyCorpusBox({...p,index:{"arbitrary":0}}).pass,false);
});
test("duplicate same-scope IDs and invalid structured data rejected",()=>{
 const source=fixture();
 source.documents[1].id="quanta";
 assert.throws(()=>composeCorpusBox(source),/Duplicate/);
 assert.throws(()=>composeCorpusBox({...fixture(),documents:Array(9).fill(fixture().documents[0])}),TypeError);
 const other=fixture();other.documents[0].chapters[0].sections[0].paragraphs[0]="😃";
 assert.throws(()=>composeCorpusBox(other),TypeError);
});
test("empty corpus and blank paragraphs are reversible",()=>{
 const p=composeCorpusBox({title:"Empty",documents:[],references:[]});
 assert.equal(verifyCorpusBox(p).pass,true);
 const q=composeCorpusBox({title:"Blank",documents:[{id:"one",title:"",chapters:[{id:"a",title:"",sections:[{id:"b",title:"",paragraphs:["","\n"]}]}]}]});
 assert.equal(verifyCorpusBox(q).pass,true);
});
