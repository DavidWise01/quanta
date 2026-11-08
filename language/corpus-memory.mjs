/**
 * QUANTA QG-021.1 — Corpus Memory.
 * Append-only, immutable, fully replayable snapshots of the QG-020 corpus tree.
 * No cryptographic authenticity or persistence beyond a serialized ledger.
 */
import {composeCorpusBox,recoverCorpusBox,lookupCorpus} from "./corpus-box.mjs";

export const MEMORY_VERSION="QG-021.1";
export const MEMORY_CARRIER="||||";
const freeze=Object.freeze;
const MAX_REVISIONS=32,MAX_LINEAGE=1024;

function equal(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function validMemoryRoot(ledger){
 if(!ledger||ledger.version!==MEMORY_VERSION||ledger.carrier!==MEMORY_CARRIER||
    !Array.isArray(ledger.revisions)||ledger.revisions.length<1||ledger.revisions.length>MAX_REVISIONS)
   throw new TypeError("Invalid QG-021 memory ledger.");
}
function revisionId(index){return "r"+String(index).padStart(4,"0");}
function canonicalSnapshot(input){
 // QG-020 re-validates all nested paragraphs and reference endpoints.
 const packet=composeCorpusBox(input);
 recoverCorpusBox(packet);
 return packet;
}
function paragraphMap(packet){
 return new Map(packet.items.filter(x=>x.type==="paragraph").map(x=>[x.address,x.text]));
}
function correspondence(previous,next,explicit=[]){
 if(!Array.isArray(explicit)||explicit.length>MAX_LINEAGE)throw new TypeError("Invalid explicit lineage mappings.");
 const before=paragraphMap(previous),after=paragraphMap(next),oldMapped=new Set(),newMapped=new Set(),relations=[];
 for(const item of explicit){
  if(!item||typeof item.from!=="string"||typeof item.to!=="string"||
     !before.has(item.from)||!after.has(item.to)||oldMapped.has(item.from)||newMapped.has(item.to))
   throw new TypeError("Lineage must be one-to-one between existing paragraph addresses.");
  relations.push(freeze({
   from:item.from,to:item.to,
   change:before.get(item.from)===after.get(item.to)?"unchanged":"edited",
   basis:"explicit"
  }));
  oldMapped.add(item.from);newMapped.add(item.to);
 }
 // Match stable addresses first. Avoid guessing whether moved text is the same
 // source merely because the wording happens to be equal.
 for(const [address,text] of before){
  if(after.has(address)&&!oldMapped.has(address)&&!newMapped.has(address)){
   relations.push(freeze({from:address,to:address,
     change:text===after.get(address)?"unchanged":"edited",
     basis:"same-address"}));
   oldMapped.add(address);newMapped.add(address);
  }
 }
 for(const address of before.keys())if(!oldMapped.has(address))
  relations.push(freeze({from:address,to:null,change:"retired",basis:"address"}));
 for(const address of after.keys())if(!newMapped.has(address))
  relations.push(freeze({from:null,to:address,change:"created",basis:"address"}));
 return freeze(relations);
}
function entry(index,snapshot,parent,lineage,comment){
 return freeze({
  id:revisionId(index),index,parent,comment,
  snapshot,
  lineage:freeze(lineage)
 });
}
export function instantiateCorpusMemory(source,comment="Initial corpus"){
 if(typeof comment!=="string"||comment.length>256)throw new TypeError("Comment must be <=256 characters.");
 const packet=canonicalSnapshot(source);
 return freeze({version:MEMORY_VERSION,carrier:MEMORY_CARRIER,
  revisions:freeze([entry(0,packet,null,[],comment)])});
}
function replayCore(ledger){
 validMemoryRoot(ledger);
 for(let i=0;i<ledger.revisions.length;i++){
  const r=ledger.revisions[i];
  if(!r||r.index!==i||r.id!==revisionId(i)||
     r.parent!==(i===0?null:revisionId(i-1))||
     typeof r.comment!=="string"||r.comment.length>256||
     !Array.isArray(r.lineage))throw new Error("Broken revision address, parent or comment.");
  const normalized=canonicalSnapshot(recoverCorpusBox(r.snapshot));
  if(!equal(r.snapshot,normalized))throw new Error("Stored corpus snapshot diverges from canonical source.");
  if(i===0){if(r.lineage.length!==0)throw new Error("Initial revision must not contain lineage.");continue;}
  const prev=ledger.revisions[i-1].snapshot;
  const explicit=r.lineage.filter(x=>x.basis==="explicit").map(x=>({from:x.from,to:x.to}));
  const expected=correspondence(prev,r.snapshot,explicit);
  if(!equal(expected,r.lineage))throw new Error("Revision correspondence changed.");
 }
 return true;
}
export function appendCorpusRevision(ledger,nextSource,options={}){
 replayCore(ledger);
 if(ledger.revisions.length>=MAX_REVISIONS)throw new RangeError("Memory revision limit reached.");
 const comment=options.comment??"Corpus revision";
 if(typeof comment!=="string"||comment.length>256)throw new TypeError("Comment must be <=256 characters.");
 const prior=ledger.revisions.at(-1).snapshot,now=canonicalSnapshot(nextSource);
 const lineage=correspondence(prior,now,options.lineage??[]);
 const nextEntry=entry(ledger.revisions.length,now,ledger.revisions.at(-1).id,lineage,comment);
 return freeze({version:MEMORY_VERSION,carrier:MEMORY_CARRIER,
  revisions:freeze([...ledger.revisions,nextEntry])});
}
export function recoverCorpusRevision(ledger,id){
 replayCore(ledger);
 const revision=ledger.revisions.find(x=>x.id===id);
 if(!revision)throw new RangeError("Unknown revision ID");
 return recoverCorpusBox(revision.snapshot);
}
export function lookupCorpusAtRevision(ledger,id,address){
 replayCore(ledger);
 const revision=ledger.revisions.find(x=>x.id===id);
 if(!revision)throw new RangeError("Unknown revision ID");
 return lookupCorpus(revision.snapshot,address);
}
export function traceCorpusLineage(ledger,id,address){
 replayCore(ledger);
 const index=ledger.revisions.findIndex(r=>r.id===id);
 if(index<0)throw new RangeError("Unknown revision ID");
 if(!paragraphMap(ledger.revisions[index].snapshot).has(address))
  throw new RangeError("Unknown paragraph source address");
 const history=[freeze({revision:id,address})];
 let current=address;
 for(let i=index;i>0;i--){
  const row=ledger.revisions[i].lineage.find(x=>x.to===current);
  if(!row||row.from===null)break;
  current=row.from;history.push(freeze({revision:revisionId(i-1),address:current,change:row.change,basis:row.basis}));
 }
 return freeze(history);
}
export function verifyCorpusMemory(ledger){
 try{
  replayCore(ledger);
  return freeze({pass:true,revisions:ledger.revisions.length,
   paragraphs:ledger.revisions.at(-1).snapshot.totalParagraphs,
   parent:ledger.revisions.at(-1).parent,
   last:ledger.revisions.at(-1).id});
 }catch(e){return freeze({pass:false,error:e.message});}
}
