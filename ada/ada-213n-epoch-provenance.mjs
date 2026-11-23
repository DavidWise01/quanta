// ADA-213N · Deterministic epoch ancestry and source-generation provenance.
// One Phase II root, one frozen Phase III boundary; descendant epochs do NOT
// constitute independent corroboration or cryptographic authentication.
import {PHASE_II_FREEZE,canonical,fnv64,verifyChain} from "./ada-201n-generational-engine.mjs";
import {PHASE_III_FREEZE,epochHierarchy,verifyEpochs} from "./ada-211n-epoch-engine.mjs";
import {restoreEpochJournal,EPOCH_ENTRY_KEY} from "./ada-212n-epoch-journal.mjs";
export const PROVENANCE_SCHEMA="ADA-213N.epoch-provenance.v1";
export function proveEpoch(chain,index,{maxAncestors=24,size=24}={}){
 const original=verifyChain(chain);if(!original.pass)throw Error("Invalid inherited source: "+original.reason);
 const epochs=epochHierarchy(chain,{size}),audit=verifyEpochs(chain,epochs,{size});
 if(!audit.pass)throw Error("Epoch source mismatch: "+audit.reason);
 if(!Number.isSafeInteger(index)||index<0||index>=epochs.length)throw Error("Epoch index outside source lineage");
 if(!Number.isSafeInteger(maxAncestors)||maxAncestors<1||maxAncestors>256)throw Error("Ancestor limit 1..256");
 const target=epochs[index],ancestors=[];
 for(let e=index;e>=0&&ancestors.length<maxAncestors;e--){
  const node=epochs[e];
  ancestors.push(Object.freeze({epoch:node.epoch,hash:node.hash,parentEpochHash:node.parentEpochHash,
   sourceStart:node.sourceStart,sourceEnd:node.sourceEnd,state:node.state,
   sealedStorageKey:node.state==="SEALED"?EPOCH_ENTRY_KEY(e):null}));
 }
 const covered=Object.freeze(chain.slice(target.sourceStart,target.sourceEnd+1).map(g=>Object.freeze({
  n:g.n,hash:g.hash,parent:g.parent,decision:g.decision
 })));
 const body={schema:PROVENANCE_SCHEMA,phaseIIIFreeze:PHASE_III_FREEZE,originalSourceRoot:PHASE_II_FREEZE,
  independentSourceRoots:1,
  selectedEpoch:index,selectedState:target.state,selectedHash:target.hash,
  sealedReceipt:target.state==="SEALED",sourceStart:target.sourceStart,sourceEnd:target.sourceEnd,
  firstInheritedParent:target.firstInheritedParent,sourceGenerationCount:chain.length,
  epochCount:epochs.length,completeAncestryDepth:index+1,returnedAncestors:ancestors.length,
  truncated:ancestors.length<index+1,
  ancestors:Object.freeze(ancestors),generations:covered,
  sourceTip:chain.at(-1).hash,epochTip:epochs.at(-1).hash,
  policy:"Derived single-source trace; OPEN_TAIL is provisional and never a sealed receipt"};
 return Object.freeze({...body,fingerprint:fnv64(canonical(body))});
}
export function verifyEpochProof(chain,proof,{size=24}={}){
 try{
  if(!proof||proof.schema!==PROVENANCE_SCHEMA)return {pass:false,reason:"Unsupported epoch provenance"};
  const {fingerprint,...body}=proof;
  if(fingerprint!==fnv64(canonical(body)))return {pass:false,reason:"Fingerprint mismatch"};
  const expected=proveEpoch(chain,proof.selectedEpoch,{maxAncestors:proof.returnedAncestors,size});
  if(canonical(proof)!==canonical(expected))return {pass:false,reason:"Proof does not match immutable source history"};
  return {pass:true,epoch:proof.selectedEpoch,state:proof.selectedState,sourceStart:proof.sourceStart,
   sourceEnd:proof.sourceEnd,ancestors:proof.returnedAncestors,sourceRoot:PHASE_II_FREEZE};
 }catch(e){return {pass:false,reason:e.message}}
}
export function inspectPersistedEpoch(storage,index,{maxAncestors=24}={}){
 const journal=restoreEpochJournal(storage);
 const proof=proveEpoch(journal.chain,index,{maxAncestors});
 const audit=verifyEpochProof(journal.chain,proof);
 if(!audit.pass)throw Error(audit.reason);
 if(proof.sealedReceipt){
  if(index>=journal.sealedCount)throw Error("Sealed epoch has no committed receipt");
  if(storage.getItem(EPOCH_ENTRY_KEY(index))===null)throw Error("Missing sealed receipt");
 }else if(storage.getItem(EPOCH_ENTRY_KEY(index))!==null){
  throw Error("OPEN_TAIL was incorrectly persisted as sealed");
 }
 return Object.freeze({proof,verified:true,persisted:journal.persisted,
  sealedReceiptPresent:proof.sealedReceipt,pendingSealed:journal.pending,
  journalGenerationCount:journal.chain.length});
}
