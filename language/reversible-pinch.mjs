// QG-048: exact reversible contraction requires retained preimage evidence.
import {contractFirstContact,verifyContraction} from './post-contact-reconstruction.mjs';
const copy=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export const COUNTS=Object.freeze([3,4,5,8,13]);
function certify(packet) {
 const proof=verifyContraction(packet);
 if(!proof.valid)throw Error('Invalid contraction proof');
 if(!packet.original||!packet.vertexMap||!packet.edgeLineage)throw Error('Missing preimage evidence');
 return proof;
}
export function freezePinch(n=8,lobes=1) {
 const contracted=contractFirstContact(n,lobes);
 certify(contracted);
 return {version:'QG-048',contracted:copy(contracted),preimage:{
   original:copy(contracted.original),
   vertexMap:copy(contracted.vertexMap),
   edgeLineage:copy(contracted.edgeLineage)
 }};
}
export function unfoldPinch(frozen) {
 if(!frozen||frozen.version!=='QG-048'||!frozen.preimage)throw Error('Missing reversible packet');
 const packet=frozen.contracted;
 certify(packet);
 if(!eq(frozen.preimage.original,packet.original)||!eq(frozen.preimage.vertexMap,packet.vertexMap)||
    !eq(frozen.preimage.edgeLineage,packet.edgeLineage))
   throw Error('Preimage mismatch');
 // Independent regeneration from the exact initial condition verifies lineage.
 const expected=contractFirstContact(packet.original.n,packet.original.lobes);
 if(!eq(packet,expected))throw Error('Contracted source mismatch');
 return copy(frozen.preimage.original);
}
export function examineLoss(frozen) {
 const original=unfoldPinch(frozen);
 const next=frozen.contracted.successor;
 const lostVertices=original.vertices.filter(v=>v.id==='C'||v.id==='R0').map(v=>v.id);
 const lostEdges=frozen.contracted.edgeLineage.filter(e=>e.reason!=='edge retained');
 return {originalVertices:original.vertices.length,successorVertices:next.verticesCount,
 originalEdges:original.edges.length,successorEdges:next.edgesCount,
 mergedVertexIdentities:lostVertices,
 edgeEvents:lostEdges.map(e=>({source:e.source,reason:e.reason,destination:e.destination})),
 canRecoverWithoutPreimage:false};
}
export function verifyFrozen(frozen) {
 const original=unfoldPinch(frozen),expected=contractFirstContact(original.n,original.lobes);
 if(!eq(expected.successor,frozen.contracted.successor))throw Error('Successor mismatch');
 return {valid:true,originalVertices:original.vertices.length,originalEdges:original.edges.length,
 successorVertices:frozen.contracted.successor.verticesCount,successorEdges:frozen.contracted.successor.edgesCount,
 roundTrip:true};
}
export function stripPreimage(frozen) {
 verifyFrozen(frozen);
 return {version:'QG-048-stripped',successor:copy(frozen.contracted.successor)};
}
export function startLedger(n=8,lobes=1){return {version:'QG-048-ledger',n,lobes,events:[]}}
export function verifyLedger(log){
 if(!log||log.version!=='QG-048-ledger'||!Array.isArray(log.events))throw Error('Malformed ledger');
 // Fail fast if original configuration itself cannot be contracted.
 freezePinch(log.n,log.lobes);
 for(let i=0;i<log.events.length;i++){
  const evt=log.events[i];
  if(!evt||evt.index!==i||!eq(evt.frozen,freezePinch(log.n,log.lobes)))throw Error('Ledger mismatch at '+i);
  verifyFrozen(evt.frozen);
 }
 return {valid:true,count:log.events.length};
}
export function appendFold(log){
 verifyLedger(log);
 return {version:'QG-048-ledger',n:log.n,lobes:log.lobes,
 events:[...copy(log.events),{index:log.events.length,frozen:freezePinch(log.n,log.lobes)}]};
}
