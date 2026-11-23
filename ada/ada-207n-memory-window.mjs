// ADA-207N · Bounded working memory over immutable, append-only +n ancestry.
// Compaction affects ONLY the active view. Source/journal entries are never deleted.
import {PHASE_II_FREEZE,verifyChain,fnv64,canonical} from "./ada-201n-generational-engine.mjs";
import {deriveMutations} from "./ada-206n-bounded-mutation.mjs";
export const MEMORY_SCHEMA="ADA-207N.working-memory.v1";
export const DEFAULT_CAPACITY=24;
export const MAX_CAPACITY=256;
export function deriveMemory(chain,capacity=DEFAULT_CAPACITY){
 if(!Number.isSafeInteger(capacity)||capacity<1||capacity>MAX_CAPACITY)throw Error("Capacity must be 1..256");
 const check=verifyChain(chain);if(!check.pass)throw Error("Invalid inherited chain: "+check.reason);
 const mutation=deriveMutations(chain);
 const start=Math.max(0,chain.length-capacity),window=[];
 for(let i=start;i<chain.length;i++){
  const source=chain[i],policy=mutation[i];
  window.push(Object.freeze({n:source.n,hash:source.hash,parent:source.parent,decision:source.decision,signal:source.signal,policy:policy.policy,mutationHash:policy.hash}));
 }
 const archivedBefore=start,tip=chain.at(-1);
 const frame={schema:MEMORY_SCHEMA,root:PHASE_II_FREEZE,capacity,sourceLength:chain.length,archivedBefore,archivedCount:archivedBefore,
  window:Object.freeze(window),firstActiveParent:window[0].parent,sourceTip:tip.hash,mutationTip:mutation.at(-1).hash,
  retention:"ACTIVE_VIEW_ONLY; all prior generation receipts stay in immutable journal"};
 return Object.freeze({...frame,hash:fnv64(canonical(frame))});
}
export function verifyMemory(chain,frame){
 try{
  const expected=deriveMemory(chain,frame?.capacity);
  if(canonical(frame)!==canonical(expected))return {pass:false,reason:"Memory snapshot disagrees with complete archive"};
  return {pass:true,active:frame.window.length,archived:frame.archivedCount,capacity:frame.capacity,tip:frame.sourceTip};
 }catch(error){return {pass:false,reason:error.message}}
}
export function memoryProof(chain,capacity=DEFAULT_CAPACITY){
 const m=deriveMemory(chain,capacity);
 return Object.freeze({schema:"ADA-207N.memory-proof.v1",root:m.root,archived:m.archivedCount,active:m.window.length,
  firstActiveParent:m.firstActiveParent,sourceTip:m.sourceTip,mutationTip:m.mutationTip,memoryHash:m.hash});
}
