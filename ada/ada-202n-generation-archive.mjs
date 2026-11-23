// ADA-202N · Write-once browser generation journal.
// Browser storage is durability against normal reloads, not malicious same-origin edits.
import {PHASE_II_FREEZE,genesis,verifyChain} from "./ada-201n-generational-engine.mjs";
export const HEAD_KEY="ADA-202N.journal.head.v1";
export const ENTRY_PREFIX="ADA-202N.journal.entry.";
export const ENTRY_KEY=n=>ENTRY_PREFIX+String(n).padStart(5,"0");
const schema="ADA-202N.journal.v1";
const encode=x=>JSON.stringify(x);
function readJson(storage,key){
 const raw=storage.getItem(key);
 if(raw===null)return null;
 try{return JSON.parse(raw)}catch{throw Error("Corrupt stored JSON at "+key)}
}
export function restoreJournal(storage){
 const head=readJson(storage,HEAD_KEY);
 if(head===null){
  if(storage.getItem(ENTRY_KEY(0))!==null)throw Error("Orphan genesis: missing journal head");
  return {chain:[genesis()],persisted:false};
 }
 if(head.schema!==schema||head.parentRoot!==PHASE_II_FREEZE||!Number.isSafeInteger(head.n)||head.n<0||head.n>10000)throw Error("Invalid journal head or Phase II root");
 const chain=[];
 for(let n=0;n<=head.n;n++){
  const node=readJson(storage,ENTRY_KEY(n));
  if(node===null)throw Error("Missing write-once generation "+n);
  chain.push(node);
 }
 const report=verifyChain(chain);
 if(!report.pass)throw Error("Journal rejected: "+report.reason);
 if(chain.at(-1).hash!==head.tip)throw Error("Journal tip mismatch");
 // An extra write-once entry implies interrupted commit, never silently truncate it.
 if(head.n<10000&&storage.getItem(ENTRY_KEY(head.n+1))!==null)throw Error("Uncommitted child exists: manual recovery required");
 return {chain,persisted:true,head};
}
export function appendJournal(storage,chain){
 const report=verifyChain(chain);
 if(!report.pass)throw Error("Archive refused: "+report.reason);
 const existing=restoreJournal(storage);
 const known=existing.persisted?existing.chain.length:0;
 if(chain.length<known)throw Error("Rollback refused: stored generation is newer");
 for(let n=0;n<known;n++)if(encode(existing.chain[n])!==encode(chain[n]))throw Error("History rewrite refused at n="+n);
 // A write-once entry is a deterministic receipt. A conflicting entry is never overwritten.
 for(let n=known;n<chain.length;n++){
  const key=ENTRY_KEY(n),raw=storage.getItem(key),serialized=encode(chain[n]);
  if(raw!==null&&raw!==serialized)throw Error("Write-once slot conflict at n="+n);
  if(raw===null)storage.setItem(key,serialized);
 }
 const tip=chain.at(-1);
 const head={schema,parentRoot:PHASE_II_FREEZE,n:tip.n,tip:tip.hash};
 storage.setItem(HEAD_KEY,encode(head)); // commit marker is written last
 return {count:chain.length,tip:tip.hash,head};
}
