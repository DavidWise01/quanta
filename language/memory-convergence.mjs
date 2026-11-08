/**
 * QUANTA QG-023.1 — Memory Convergence.
 *
 * Deterministic 3-way paragraph-text convergence for two QG-021 ledgers that
 * share an identical revision-prefix ancestor. Both branch ledgers are retained.
 * Conflicts are explicit, and no arbitrary winner is silently selected.
 *
 * Scope: identical corpus hierarchy, paragraph addresses and explicit reference
 * graph at all three compared snapshots; only paragraph text may differ.
 * This prototype is neither distributed consensus nor cryptographic provenance.
 */
import {
 verifyCorpusMemory,recoverCorpusRevision
} from "./corpus-memory.mjs";
import {composeCorpusBox,recoverCorpusBox} from "./corpus-box.mjs";

export const CONVERGENCE_VERSION="QG-023.1";
export const CONVERGENCE_CARRIER="||||";
const freeze=Object.freeze;
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const clone=x=>JSON.parse(JSON.stringify(x));
function validate(ledger,label) {
 const verdict=verifyCorpusMemory(ledger);
 if(!verdict.pass)throw new Error(label+": "+verdict.error);
}
function sharedOrigin(left,right){
 let common=-1;
 for(let i=0;i<Math.min(left.revisions.length,right.revisions.length);i++){
  const a=left.revisions[i],b=right.revisions[i];
  if(!equal(a,b))break;
  common=i;
 }
 if(common<0)throw new Error("No identical shared ancestor revision");
 return common;
}
function sources(base,left,right) {
 const snapshots=[base,left,right].map(s=>composeCorpusBox(s));
 const paragraphLists=snapshots.map(s=>s.items.filter(x=>x.type==="paragraph"));
 const paths=paragraphLists[0].map(x=>x.address);
 for(let i=1;i<3;i++){
  if(!equal(paragraphLists[i].map(x=>x.address),paths))
   throw new Error("QG-023 requires matching paragraph addresses and topology");
 }
 function skeleton(source){
  const c=clone(source);
  for(const d of c.documents)for(const ch of d.chapters)for(const s of ch.sections)
    s.paragraphs=s.paragraphs.map(()=>null);
  return c;
 }
 if(!equal(skeleton(base),skeleton(left))||!equal(skeleton(base),skeleton(right)))
  throw new Error("QG-023 requires identical document/section metadata and references");
 return {paths,
  maps:paragraphLists.map(list=>new Map(list.map(p=>[p.address,p.text])))};
}
function plan(left,right){
 validate(left,"Left history");validate(right,"Right history");
 const at=sharedOrigin(left,right);
 const ancestor=left.revisions[at],ll=left.revisions.at(-1),rr=right.revisions.at(-1);
 const base=recoverCorpusRevision(left,ancestor.id),
       a=recoverCorpusRevision(left,ll.id),
       b=recoverCorpusRevision(right,rr.id);
 const {paths,maps}=sources(base,a,b);
 const entries=paths.map(address=>{
  const [orig,first,second]=maps.map(m=>m.get(address));
  let status,proposed=null;
  if(first===second){status=first===orig?"unchanged":"agreed";proposed=first}
  else if(first===orig){status="right-only";proposed=second}
  else if(second===orig){status="left-only";proposed=first}
  else status="conflict";
  return freeze({address,base:orig,left:first,right:second,status,proposed});
 });
 return {ancestor:ancestor.id,leftHead:ll.id,rightHead:rr.id,base,entries:freeze(entries),
   conflicts:freeze(entries.filter(e=>e.status==="conflict").map(e=>e.address))};
}
function normalizeResolutions(resolutions){
 if(!resolutions||typeof resolutions!=="object"||Array.isArray(resolutions))throw new TypeError("Resolution map must be an object");
 return resolutions;
}
function mergePlan(plan,resolutions,requireComplete){
 const map=normalizeResolutions(resolutions),known=new Set(plan.conflicts);
 for(const key of Object.keys(map))if(!known.has(key))throw new Error("Unknown conflict resolution address: "+key);
 const selected={},results=[];
 for(const row of plan.entries){
  let text=row.proposed,decision="automatic";
  if(row.status==="conflict"){
   const resolution=map[row.address];
   if(resolution===undefined){
    if(requireComplete)throw new Error("Unresolved conflict at "+row.address);
    decision="unresolved";text=null;
   }else{
    if(!resolution||typeof resolution!=="object"||Array.isArray(resolution)||
       !["left","right","base","custom"].includes(resolution.choice))
       throw new TypeError("Resolution choice must be left/right/base/custom");
    decision=resolution.choice;
    if(decision==="custom"){
     if(typeof resolution.text!=="string")throw new TypeError("Custom resolution requires text");
     text=resolution.text;
    }else text=row[decision];
  }
  selected[row.address]=text;
  results.push(freeze({...row,decision,merged:text}));
 }
 return {selected,results:freeze(results)};
}
function overlay(base,selected){
 const result=clone(base);
 for(const doc of result.documents)for(const ch of doc.chapters)for(const sec of ch.sections)
  for(let i=0;i<sec.paragraphs.length;i++){
   const address="doc/"+doc.id+"/ch/"+ch.id+"/sec/"+sec.id+"/p/"+i;
   if(!Object.hasOwn(selected,address)||typeof selected[address]!=="string")
    throw new Error("Unresolved paragraph at "+address);
   sec.paragraphs[i]=selected[address];
  }
 return recoverCorpusBox(composeCorpusBox(result));
}
export function compareCorpusBranches(left,right){
 const p=plan(left,right);
 return freeze({version:CONVERGENCE_VERSION,carrier:CONVERGENCE_CARRIER,
  ancestor:p.ancestor,leftHead:p.leftHead,rightHead:p.rightHead,
  entries:p.entries,conflicts:p.conflicts,
  ready:p.conflicts.length===0});
}
export function convergeCorpusMemory(left,right,resolutions={}){
 const p=plan(left,right);
 const {selected,results}=mergePlan(p,resolutions,true);
 const mergedSource=overlay(p.base,selected);
 const merged=composeCorpusBox(mergedSource);
 return freeze({version:CONVERGENCE_VERSION,carrier:CONVERGENCE_CARRIER,
  ancestor:p.ancestor,
  parents:freeze({left:p.leftHead,right:p.rightHead}),
  branches:freeze({left,right}), // retain complete, independent histories
  resolutions:freeze(clone(resolutions)),
  records:results,merged});
}
export function recoverCorpusConvergence(record){
 if(!record||record.version!==CONVERGENCE_VERSION||record.carrier!==CONVERGENCE_CARRIER||
    !record.branches||!record.parents)throw new TypeError("Unknown convergence record");
 const expected=convergeCorpusMemory(record.branches.left,record.branches.right,record.resolutions);
 if(!equal(record,expected))throw new Error("Convergence result, parent or witness mismatch");
 return recoverCorpusBox(record.merged);
}
export function verifyCorpusConvergence(record){
 try{
  const source=recoverCorpusConvergence(record);
  return freeze({pass:true,ancestor:record.ancestor,
   parents:record.parents,paragraphs:record.records.length,
   resolvedConflicts:record.records.filter(r=>r.status==="conflict").length,
   documents:source.documents.length});
 }catch(e){return freeze({pass:false,error:e.message});}
}
