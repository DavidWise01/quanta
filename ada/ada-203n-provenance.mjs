// ADA-203N · Deterministic, single-origin lineage provenance.
// A traced generation is NOT an independent witness: every descendant has one source root.
import {PHASE_II_FREEZE,verifyChain,fnv64,canonical} from "./ada-201n-generational-engine.mjs";
import {ENTRY_KEY,HEAD_KEY,restoreJournal} from "./ada-202n-generation-archive.mjs";
export const PROVENANCE_SCHEMA="ADA-203N.provenance.v1";
export function traceLineage(chain,generation=chain.length-1,limit=32){
 const result=verifyChain(chain);
 if(!result.pass)throw Error("Provenance requires verified ancestry: "+result.reason);
 if(!Number.isSafeInteger(generation)||generation<0||generation>=chain.length)throw Error("Generation outside verified chain");
 if(!Number.isSafeInteger(limit)||limit<1||limit>256)throw Error("Trace limit must be 1..256");
 const tip=chain[generation],ancestors=[];
 for(let i=generation;i>=0&&ancestors.length<limit;i--){
  const node=chain[i];
  ancestors.push({n:node.n,hash:node.hash,parent:node.parent,decision:node.decision,event:node.event,storageKey:ENTRY_KEY(i)});
 }
 const depth=generation+1;
 const proof={
  schema:PROVENANCE_SCHEMA,parentRoot:PHASE_II_FREEZE,
  originType:"single-owned-phase-II-source",
  independentWitnessRoots:1,
  target:{n:tip.n,hash:tip.hash,decision:tip.decision,signal:tip.signal,stability:tip.stability,energy:tip.energy},
  generationCount:chain.length,ancestryDepth:depth,
  returned:ancestors.length,truncated:ancestors.length<depth,
  ancestors,headKey:HEAD_KEY,chainTip:chain.at(-1).hash,
  verified:true
 };
 return {...proof,fingerprint:fnv64(canonical(proof))};
}
export function inspectJournal(storage,generation,limit=32){
 const {chain,persisted,head}=restoreJournal(storage);
 const proof=traceLineage(chain,generation===undefined?chain.length-1:generation,limit);
 return {...proof,persisted,storedHead:head?.tip??null};
}
export function validateProvenance(proof,chain){
 if(!proof||proof.schema!==PROVENANCE_SCHEMA)return {pass:false,reason:"Unsupported lineage evidence"};
 const {fingerprint,...fields}=proof;
 if(fingerprint!==fnv64(canonical(fields)))return {pass:false,reason:"Evidence fingerprint mismatch"};
 try{
  const expected=traceLineage(chain,proof.target?.n,proof.returned);
  if(canonical(proof)!==canonical(expected))return {pass:false,reason:"Evidence content does not match deterministic lineage"};
  return {pass:true,root:PHASE_II_FREEZE,depth:expected.ancestryDepth,returned:expected.returned,tip:expected.target.hash};
 }catch(e){return {pass:false,reason:e.message}}
}
