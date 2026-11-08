/**
 * QUANTA QG-032.1 — Root Reconciliation.
 * Preserve competing root observations and their evidence, flag conflicts,
 * and record explicit human decisions without overwriting any witness.
 *
 * Root graph: verified QG-030 / QG-031 latest snapshot.
 * Both observations address the same existing leaf root.
 * Different positions (supports / challenges) create an open conflict.
 * Decisions are review annotations, never automatically established facts.
 */
import {composeRootChase,recoverRootChase} from "./chasing-roots.mjs";
import {verifyRootPropagation} from "./root-propagation.mjs";

export const RECONCILIATION_VERSION="QG-032.1";
export const RECONCILIATION_CARRIER="||||";
export const RECONCILIATION_LIMIT=32;
const freeze=Object.freeze;
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const clone=x=>JSON.parse(JSON.stringify(x));
function text(v,name,max=900) {
 if(typeof v!=="string"||!v.trim()||v.length>max||/[\u0000-\u001f]/.test(v))
  throw new TypeError(name+" must be nonempty text up to "+max);
 return v;
}
function checkId(id){if(typeof id!=="string"||!/^[a-z][a-z0-9-]{0,63}$/.test(id))throw new TypeError("Invalid ID");return id}
function ownFields(o,fields,label){
 if(!o||typeof o!=="object"||Array.isArray(o)||Object.keys(o).some(k=>!fields.includes(k)))
  throw new TypeError("Invalid "+label);
}
function sources(list) {
 if(!Array.isArray(list)||list.length<1||list.length>12)throw new TypeError("Observation requires 1–12 cited URLs");
 return freeze(list.map(e=>{
  ownFields(e,["label","url"],"evidence");
  if(!/^https:\/\/[^\s]+$/.test(e.url))throw new TypeError("Evidence URL must be HTTPS");
  return freeze({label:text(e.label,"evidence label",160),url:text(e.url,"evidence URL",1000)});
 }));
}
function rootSource(source){
 let p=source;
 if(p?.version==="QG-031.1") {
  const audit=verifyRootPropagation(p);
  if(!audit.pass)throw new Error("Invalid root propagation: "+audit.error);
  p=p.revisions.at(-1).snapshot;
 }else if(p?.version!=="QG-030.1")p=composeRootChase(p);
 recoverRootChase(p);
 return p;
}
function root(packet,id){
 const n=packet.nodes.find(n=>n.id===id);
 if(!n||n.requires.length)throw new Error("Conflict must address an existing leaf root");
 return n;
}
function normalObservation(packet,input){
 ownFields(input,["id","root","position","statement","year","evidence","question"],"observation");
 const id=checkId(input.id),rootId=checkId(input.root),r=root(packet,rootId);
 if(!["supports","challenges"].includes(input.position))throw new TypeError("Position must support or challenge");
 if(!Number.isInteger(input.year)||input.year<1||input.year>packet.society.claim.context.year||
    input.year<r.year)throw new RangeError("Observation year outside root-to-context interval");
 return freeze({id,root:rootId,position:input.position,
  statement:text(input.statement,"observation statement"),year:input.year,
  evidence:sources(input.evidence),question:text(input.question,"resolution question",600)});
}
function normalDecision(input,conflict){
 ownFields(input,["id","choice","rationale","evidence"],"decision");
 if(checkId(input.id)!==conflict.id)throw new Error("Decision must reference conflict ID");
 if(!["support","challenge","insufficient"].includes(input.choice))
  throw new TypeError("Decision must select support/challenge/insufficient");
 return freeze({id:input.id,choice:input.choice,
  rationale:text(input.rationale,"rationale",1000),
  evidence:sources(input.evidence)});
}
function reverseAffected(packet,rootId){
 const reverse=new Map(packet.nodes.map(n=>[n.id,[]]));
 for(const n of packet.nodes)for(const dep of n.requires)reverse.get(dep).push(n.id);
 const found=new Set(),queue=[rootId];
 for(let i=0;i<queue.length;i++){
  const id=queue[i];if(found.has(id))continue;found.add(id);
  for(const d of reverse.get(id))if(!found.has(d))queue.push(d);
 }
 return freeze(packet.nodes.filter(n=>found.has(n.id)).map(n=>n.id));
}
function conflictId(index){return "c"+String(index).padStart(4,"0")}
function encounter(packet,left,right,index) {
 const a=normalObservation(packet,left),b=normalObservation(packet,right);
 if(a.id===b.id||a.root!==b.root)throw new Error("Two distinct observations must concern one root");
 if(a.position===b.position)throw new Error("Both positions agree; no opposing-root conflict");
 return freeze({id:conflictId(index),root:a.root,
  observations:freeze([a,b]),affected:reverseAffected(packet,a.root),
  state:"open",decision:null});
}
export function instantiateReconciliation(source){
 const packet=rootSource(source);
 return freeze({version:RECONCILIATION_VERSION,carrier:RECONCILIATION_CARRIER,
  rootPacket:packet,conflicts:freeze([]),events:freeze([])});
}
function replay(ledger){
 if(!ledger||ledger.version!==RECONCILIATION_VERSION||ledger.carrier!==RECONCILIATION_CARRIER||
  !Array.isArray(ledger.conflicts)||!Array.isArray(ledger.events)||
  ledger.conflicts.length>RECONCILIATION_LIMIT||ledger.events.length>RECONCILIATION_LIMIT*2)
  throw new TypeError("Invalid reconciliation ledger");
 recoverRootChase(ledger.rootPacket);
 const ordered=[];let prior=null;
 for(let i=0;i<ledger.events.length;i++){
  const e=ledger.events[i];
  if(!e||e.index!==i||e.previous!==prior||!["encounter","decision"].includes(e.kind))
   throw new Error("Broken append-only reconciliation event order");
  if(e.kind==="encounter"){
   if(ordered.length>=RECONCILIATION_LIMIT)throw new Error("Conflict limit");
   const c=encounter(ledger.rootPacket,e.observations[0],e.observations[1],ordered.length);
   if(!equal(e.conflict,c))throw new Error("Encounter witness mismatch");
   ordered.push(c);
  }else{
   const which=ordered.findIndex(c=>c.id===e.id);
   if(which<0||ordered[which].state!=="open")throw new Error("Decision target missing or already decided");
   const d=normalDecision(e.decision,ordered[which]);
   if(!equal(d,e.decision))throw new Error("Decision witness mismatch");
   ordered[which]=freeze({...ordered[which],state:"reviewed",decision:d});
  }
  prior="e"+String(i).padStart(4,"0");
 }
 if(!equal(ordered,ledger.conflicts))throw new Error("Reconciled conflicts differ from event replay");
 return true;
}
function append(ledger,event,conflicts){
 return freeze({version:RECONCILIATION_VERSION,carrier:RECONCILIATION_CARRIER,
  rootPacket:ledger.rootPacket,events:freeze([...ledger.events,freeze(event)]),
  conflicts:freeze(conflicts)});
}
export function encounterRootConflict(ledger,left,right){
 replay(ledger);
 if(ledger.conflicts.length>=RECONCILIATION_LIMIT)throw new RangeError("Conflict capacity reached");
 const c=encounter(ledger.rootPacket,left,right,ledger.conflicts.length),i=ledger.events.length;
 return append(ledger,{index:i,previous:i?"e"+String(i-1).padStart(4,"0"):null,
  kind:"encounter",observations:freeze([c.observations[0],c.observations[1]]),conflict:c},
  [...ledger.conflicts,c]);
}
export function decideRootConflict(ledger,id,choice,rationale,evidence){
 replay(ledger);
 const at=ledger.conflicts.findIndex(c=>c.id===id);
 if(at<0||ledger.conflicts[at].state!=="open")throw new Error("No open conflict at "+id);
 const decision=normalDecision({id,choice,rationale,evidence},ledger.conflicts[at]);
 const updated=[...ledger.conflicts];updated[at]=freeze({...updated[at],state:"reviewed",decision});
 const i=ledger.events.length;
 return append(ledger,{index:i,previous:i?"e"+String(i-1).padStart(4,"0"):null,
  kind:"decision",id,decision},updated);
}
export function inspectRootReconciliation(ledger){
 replay(ledger);
 return freeze({conflicts:ledger.conflicts.length,open:ledger.conflicts.filter(c=>c.state==="open").length,
  reviewed:ledger.conflicts.filter(c=>c.state==="reviewed").length,
  events:ledger.events.length,
  affected:freeze([...new Set(ledger.conflicts.flatMap(c=>c.affected))]),
  interpretationProven:false});
}
export function verifyRootReconciliation(ledger){
 try{return freeze({pass:true,...inspectRootReconciliation(ledger)})}
 catch(e){return freeze({pass:false,error:e.message})}
}
