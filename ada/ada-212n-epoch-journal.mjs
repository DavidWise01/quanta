// ADA-212N · Persist only SEALED epochs; OPEN_TAIL is always derived, never written.
// Uses the separate ADA-202N write-once generation journal as the only source of truth.
import {PHASE_III_FREEZE,epochHierarchy,verifyEpochs,EPOCH_SIZE} from "./ada-211n-epoch-engine.mjs";
import {restoreJournal,appendJournal} from "./ada-202n-generation-archive.mjs";
export const EPOCH_HEAD_KEY="ADA-212N.epoch.head.v1";
export const EPOCH_ENTRY_KEY=n=>"ADA-212N.epoch.sealed."+String(n).padStart(5,"0");
export const EPOCH_JOURNAL_SCHEMA="ADA-212N.epoch-journal.v1";
function read(storage,key){
 const raw=storage.getItem(key);if(raw===null)return null;
 try{return JSON.parse(raw)}catch{throw Error("Corrupt epoch JSON "+key)}
}
const encoded=v=>JSON.stringify(v);
export function restoreEpochJournal(storage){
 const base=restoreJournal(storage),chain=base.chain,epochs=epochHierarchy(chain,{size:EPOCH_SIZE});
 const expectedSealed=epochs.filter(e=>e.state==="SEALED");
 const head=read(storage,EPOCH_HEAD_KEY);
 if(head===null){
  if(storage.getItem(EPOCH_ENTRY_KEY(0))!==null)throw Error("Orphan sealed epoch without head");
  // A valid source journal can have sealed epochs not yet checkpointed after an interrupted commit.
  return {chain,epochs,persisted:false,sealedCount:0,pending:expectedSealed.length,openTail:epochs.at(-1).state==="OPEN_TAIL"};
 }
 if(head.schema!==EPOCH_JOURNAL_SCHEMA||head.phaseIIIFreeze!==PHASE_III_FREEZE||
    !Number.isSafeInteger(head.count)||head.count<0||head.count>417)throw Error("Invalid Phase IV head/root");
 if(head.count>expectedSealed.length)throw Error("Epoch head claims generations not present in source");
 for(let i=0;i<head.count;i++){
  const saved=read(storage,EPOCH_ENTRY_KEY(i)),e=expectedSealed[i];
  if(saved===null)throw Error("Missing sealed epoch "+i);
  if(encoded(saved)!==encoded(e))throw Error("Sealed epoch divergence at "+i);
 }
 const tip=head.count?expectedSealed[head.count-1].hash:null;
 if(head.tip!==tip)throw Error("Sealed epoch head tip mismatch");
 // A future sealed entry without its head is an interrupted commit, not a silent extension.
 if(storage.getItem(EPOCH_ENTRY_KEY(head.count))!==null)throw Error("Uncommitted sealed epoch exists: manual recovery required");
 const check=verifyEpochs(chain,epochs);
 if(!check.pass)throw Error(check.reason);
 return {chain,epochs,persisted:true,sealedCount:head.count,pending:expectedSealed.length-head.count,openTail:epochs.at(-1).state==="OPEN_TAIL",head};
}
export function commitEpochJournal(storage,chain){
 // Verify and persist original generation ancestry first; never touch prior source receipts.
 appendJournal(storage,chain);
 const state=restoreEpochJournal(storage);
 if(state.chain.length!==chain.length||state.chain.at(-1).hash!==chain.at(-1).hash)throw Error("Concurrent source change");
 const sealed=state.epochs.filter(e=>e.state==="SEALED");
 for(let i=state.sealedCount;i<sealed.length;i++){
  const key=EPOCH_ENTRY_KEY(i),value=encoded(sealed[i]),existing=storage.getItem(key);
  if(existing!==null&&existing!==value)throw Error("Write-once epoch collision at "+i);
  if(existing===null)storage.setItem(key,value);
 }
 const tip=sealed.length?sealed.at(-1).hash:null;
 storage.setItem(EPOCH_HEAD_KEY,encoded({schema:EPOCH_JOURNAL_SCHEMA,phaseIIIFreeze:PHASE_III_FREEZE,count:sealed.length,tip}));
 return {chain:state.chain,epochs:state.epochs,sealedCount:sealed.length,openTail:state.openTail,pending:0,tip};
}
