/**
 * QUANTA QG-031.1 — Root Roots: forward evidence propagation.
 *
 * QG-030 chases interpretation -> prerequisite roots.
 * QG-031 appends immutable snapshots after an explicit root evidence update,
 * and traces the reverse dependency DAG from changed roots to dependent claims.
 * It NEVER promotes a dependent claim to true or silently changes its wording.
 *
 * Structural verification catches accidental changes, not deliberate
 * self-consistent rewriting or counterfeit evidence.
 */
import {composeRootChase,recoverRootChase} from "./chasing-roots.mjs";
export const ROOT_PROPAGATION_VERSION="QG-031.1";
export const ROOT_PROPAGATION_CARRIER="||||";
export const MAX_PROPAGATIONS=32;
const freeze=Object.freeze;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const copy=x=>JSON.parse(JSON.stringify(x));
function has(o,k){return Object.prototype.hasOwnProperty.call(o,k)}
function rootIds(packet){
 return packet.nodes.filter(n=>n.requires.length===0).map(n=>n.id);
}
function reverseGraph(packet){
 const reverse=new Map(packet.nodes.map(n=>[n.id,[]]));
 for(const n of packet.nodes)for(const dep of n.requires)reverse.get(dep).push(n.id);
 return reverse;
}
function impacted(packet,ids){
 const links=reverseGraph(packet),queue=[...ids],visited=new Set();
 for(let i=0;i<queue.length;i++){
  const id=queue[i];if(visited.has(id))continue;visited.add(id);
  for(const parent of links.get(id))if(!visited.has(parent))queue.push(parent);
 }
 // Canonical graph order, regardless of changed-root selection ordering.
 return freeze(packet.nodes.filter(n=>visited.has(n.id)).map(n=>n.id));
}
function normalizedChanges(packet,changes){
 if(!Array.isArray(changes)||changes.length<1||changes.length>60)
  throw new TypeError("Provide 1..60 root updates");
 const roots=new Set(rootIds(packet)),seen=new Set();
 return freeze(changes.map(change=>{
  if(!change||typeof change!=="object"||Array.isArray(change)||
     Object.keys(change).some(k=>!["id","status","evidence"].includes(k)))
   throw new TypeError("Root update has invalid keys");
  const id=change.id;
  if(typeof id!=="string"||!roots.has(id))throw new Error("Update must target an existing leaf root");
  if(seen.has(id))throw new Error("Duplicate root update "+id);
  seen.add(id);
  if(!has(change,"status")||!has(change,"evidence"))
   throw new TypeError("Root updates require status and evidence");
  return freeze({id,status:change.status,evidence:copy(change.evidence)});
 }));
}
function updateRootPacket(packet,changes){
 recoverRootChase(packet);
 const updates=normalizedChanges(packet,changes);
 const byId=new Map(updates.map(x=>[x.id,x]));
 const nodes=packet.nodes.map(n=>{
  const u=byId.get(n.id);
  return u?{...n,status:u.status,evidence:u.evidence}:n;
 });
 const next=composeRootChase({society:packet.society,target:packet.target,nodes});
 const altered=updates.filter(u=>{
  const old=packet.nodes.find(n=>n.id===u.id);
  const fresh=next.nodes.find(n=>n.id===u.id);
  return old.status!==fresh.status||!same(old.evidence,fresh.evidence);
 }).map(x=>x.id);
 if(!altered.length)throw new Error("Root update makes no change");
 const roots=freeze(altered),affected=impacted(packet,roots);
 return {next,roots,affected,changes:updates};
}
function changeRecord(index,before,changes,comment){
 if(typeof comment!=="string"||comment.length>256)throw new TypeError("Comment must be <=256 chars");
 const delta=updateRootPacket(before,changes);
 return freeze({
  id:"p"+String(index).padStart(4,"0"),index,parent:index===1?"p0000":"p"+String(index-1).padStart(4,"0"),
  comment,changedRoots:delta.roots,affected:delta.affected,changes:delta.changes,
  snapshot:delta.next
 });
}
export function instantiateRootPropagation(source){
 const root=source?.version==="QG-030.1"?source:composeRootChase(source);
 recoverRootChase(root);
 return freeze({version:ROOT_PROPAGATION_VERSION,carrier:ROOT_PROPAGATION_CARRIER,
  revisions:freeze([freeze({id:"p0000",index:0,parent:null,comment:"Original roots",
   changedRoots:freeze([]),affected:freeze([]),changes:freeze([]),snapshot:root})])});
}
function replay(ledger){
 if(!ledger||ledger.version!==ROOT_PROPAGATION_VERSION||
   ledger.carrier!==ROOT_PROPAGATION_CARRIER||!Array.isArray(ledger.revisions)||
   ledger.revisions.length<1||ledger.revisions.length>MAX_PROPAGATIONS)
  throw new TypeError("Invalid QG-031 ledger");
 for(let i=0;i<ledger.revisions.length;i++){
  const r=ledger.revisions[i];
  if(!r||r.index!==i||r.id!=="p"+String(i).padStart(4,"0")||
     r.parent!==(i?"p"+String(i-1).padStart(4,"0"):null)||
     typeof r.comment!=="string"||r.comment.length>256)
   throw new Error("Broken root revision lineage");
  recoverRootChase(r.snapshot);
  if(i===0){
   if(!same(r.changedRoots,[])||!same(r.affected,[])||!same(r.changes,[]))
    throw new Error("Origin cannot have propagations");
  }else{
   const expected=changeRecord(i,ledger.revisions[i-1].snapshot,r.changes,r.comment);
   if(!same(expected,r))throw new Error("Root propagation, impact or snapshot witness mismatch");
  }
 }
 return true;
}
export function propagateRoots(ledger,changes,comment="New root evidence"){
 replay(ledger);
 if(ledger.revisions.length>=MAX_PROPAGATIONS)throw new RangeError("Propagation history full");
 const row=changeRecord(ledger.revisions.length,ledger.revisions.at(-1).snapshot,changes,comment);
 return freeze({version:ROOT_PROPAGATION_VERSION,carrier:ROOT_PROPAGATION_CARRIER,
  revisions:freeze([...ledger.revisions,row])});
}
export function recoverRootRevision(ledger,id){
 replay(ledger);const row=ledger.revisions.find(r=>r.id===id);
 if(!row)throw new RangeError("Unknown propagation revision");
 return recoverRootChase(row.snapshot);
}
export function inspectRootImpact(ledger,id){
 replay(ledger);const row=ledger.revisions.find(r=>r.id===id);
 if(!row)throw new RangeError("Unknown propagation revision");
 const target=row.snapshot.target;
 return freeze({revision:id,parent:row.parent,changedRoots:row.changedRoots,
  affected:row.affected,interpretationNeedsReview:row.affected.includes(target),
  unresolvedRoots:row.snapshot.trace.gaps,
  claimStatusUnchanged:true});
}
export function verifyRootPropagation(ledger){
 try{
  replay(ledger);const last=ledger.revisions.at(-1);
  return freeze({pass:true,revisions:ledger.revisions.length,
   changedRoots:last.changedRoots.length,affected:last.affected.length,
   unresolvedRoots:last.snapshot.trace.gaps.length,
   target:last.snapshot.target});
 }catch(error){return freeze({pass:false,error:error.message})}
}
