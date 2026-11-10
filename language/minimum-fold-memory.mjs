// QG-049: recipe-relative lossless regeneration, not a universal minimum-bit proof.
// Successor + selected generator parameter => deterministic original for this family.
import {contractFirstContact} from './post-contact-reconstruction.mjs';
import {freezePinch} from './reversible-pinch.mjs';
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const clone=x=>JSON.parse(JSON.stringify(x));
export const COUNTS=[3,4,5,8,13];
export const RECIPE='QG-047-single-contact-v1';
export function compressPinch(n=8,lobes=1){
 const c=contractFirstContact(n,lobes);
 return {version:'QG-049',recipe:RECIPE,successor:clone(c.successor),witness:{lobes}};
}
export function restorePinch(packet){
 if(!packet||packet.version!=='QG-049'||packet.recipe!==RECIPE||!packet.witness||
    !packet.successor||!Array.isArray(packet.successor.vertices))throw Error('Missing or unsupported reconstruction recipe');
 // n is already present in the successor vertex count; no duplicate size witness.
 const n=packet.successor.vertices.length,lobes=packet.witness.lobes;
 const predicted=contractFirstContact(n,lobes);
 if(!same(packet.successor,predicted.successor))throw Error('Successor does not match reconstruction witness');
 return clone(predicted.original);
}
export function verifyCompressed(packet){
 const original=restorePinch(packet);
 const expanded=freezePinch(original.n,original.lobes);
 if(!same(original,expanded.preimage.original))throw Error('Exact preimage mismatch');
 const fullBytes=JSON.stringify(expanded).length,smallBytes=JSON.stringify(packet).length;
 return {valid:true,roundTrip:true,n:original.n,lobes:original.lobes,fullBytes,smallBytes,bytesSaved:fullBytes-smallBytes};
}
export function strippedWitness(packet){return {version:packet.version,recipe:packet.recipe,successor:clone(packet.successor)}}
export function aliasEvidence(){
 // cos(i*2*pi/8) = cos(7*i*2*pi/8), up to floating precision.
 // Mathematical identity: cos(2pi*i - theta)=cos(theta).
 return {n:8,firstLobes:1,secondLobes:7,meaning:'distinct generator histories can map to numerically near-identical successor geometry; do not infer unique history from graph alone'};
}
export function createLedger(n=8,lobes=1){return {version:'QG-049-ledger',n,lobes,events:[]}}
export function verifyLedger(log){
 if(!log||log.version!=='QG-049-ledger'||!Array.isArray(log.events))throw Error('Invalid ledger');
 const standard=compressPinch(log.n,log.lobes);
 for(let i=0;i<log.events.length;i++){
  const e=log.events[i];if(!e||e.index!==i||!same(e.packet,standard))throw Error('Replay mismatch');
  verifyCompressed(e.packet);
 }
 return {valid:true,events:log.events.length};
}
export function appendCompress(log){
 verifyLedger(log);
 return {version:log.version,n:log.n,lobes:log.lobes,
 events:[...clone(log.events),{index:log.events.length,packet:compressPinch(log.n,log.lobes)}]};
}
