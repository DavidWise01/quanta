// QG-068 — Revocation across the Hive.
// No agent can authorize a NEW operation from an offline, stale, or invalid snapshot.
// The independent monotonic floor must be distributed out-of-band; this does not
// implement a real network, clock, key vault, or durable consensus protocol.
import {fixture as revocationFixture,verify as verifyRevocation} from './revocation-outlives-recovery.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-068', REQUIRED_SEQUENCE=1;
const copy=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>canonical(a)===canonical(b);
const named=s=>typeof s==='string'&&s.length>0&&s.length<=120;
export async function inspectAgent(packet,pin){
 if(!packet||!named(packet.agentId)||!['online','offline'].includes(packet.connection)||!packet.snapshot)
  throw Error('Malformed agent report');
 const digest=await sha256(canonical(packet.snapshot));
 if(packet.connection==='offline')return {agentId:packet.agentId,state:'offline',mayAuthorize:false,digest,reason:'cannot attest current trust floor'};
 try{
  const v=await verifyRevocation(packet.snapshot,pin);
  if(!v.revoked||v.revocationSequence<REQUIRED_SEQUENCE)
   return {agentId:packet.agentId,state:'stale',mayAuthorize:false,digest,reason:'revocation missing'};
  return {agentId:packet.agentId,state:'current',mayAuthorize:true,digest,
   reason:'verified recovery and required revocation'};
 }catch(error){
  // Distinguish an otherwise intact pre-revocation snapshot from a malformed one.
  try{
   const old=await verifyRevocation(packet.snapshot,{...pin,minRevocationSequence:0});
   if(!old.revoked)return {agentId:packet.agentId,state:'stale',mayAuthorize:false,digest,
     reason:'independent revocation floor not met'};
  }catch{}
  return {agentId:packet.agentId,state:'invalid',mayAuthorize:false,digest,
   reason:'snapshot failed cryptographic or provenance replay'};
 }
}
export function requireFloor(pin){
 if(!pin||!pin.recoveryPin||!Number.isSafeInteger(pin.minRevocationSequence)||
 pin.minRevocationSequence<REQUIRED_SEQUENCE)
 throw Error('Hive requires independently pinned revocation floor >= 1');
}
export async function start(pin){
 requireFloor(pin);
 return {version:VERSION,pin:copy(pin),reports:[],receipts:[],eligibleAgents:0};
}
export async function verify(ledger,independentPin){
 requireFloor(independentPin);
 if(!ledger||ledger.version!==VERSION||!Array.isArray(ledger.reports)||!Array.isArray(ledger.receipts)||
 !equal(ledger.pin,independentPin))throw Error('Hive pin or ledger mismatch');
 const seen=new Set(),receipts=[];
 for(const packet of ledger.reports){
  if(seen.has(packet?.agentId))throw Error('Duplicate agent identity');
  seen.add(packet.agentId);
  receipts.push(await inspectAgent(packet,independentPin));
 }
 const eligibleAgents=receipts.filter(r=>r.mayAuthorize).length;
 if(!equal(ledger.receipts,receipts)||ledger.eligibleAgents!==eligibleAgents)
  throw Error('Hive receipt replay mismatch');
 return {valid:true,receipts,eligibleAgents,total:receipts.length,
  stale:receipts.filter(r=>r.state==='stale').length,
  offline:receipts.filter(r=>r.state==='offline').length,
  invalid:receipts.filter(r=>r.state==='invalid').length};
}
export async function append(ledger,packet,independentPin){
 await verify(ledger,independentPin);
 if(ledger.reports.some(p=>p.agentId===packet?.agentId))throw Error('Duplicate agent identity');
 const next={...copy(ledger),reports:[...copy(ledger.reports),copy(packet)]};
 next.receipts=await Promise.all(next.reports.map(p=>inspectAgent(p,independentPin)));
 next.eligibleAgents=next.receipts.filter(r=>r.mayAuthorize).length;
 await verify(next,independentPin);
 return next;
}
export async function authorizeAgent(ledger,agentId,independentPin){
 await verify(ledger,independentPin);
 const receipt=ledger.receipts.find(r=>r.agentId===agentId);
 if(!receipt||!receipt.mayAuthorize)throw Error('Agent authorization denied: missing current revocation');
 return {agentId,allowed:true,revocationSequence:1,digest:receipt.digest};
}
export async function fixture(mode='mixed'){
 const f=await revocationFixture('valid');
 const pin={...copy(f.pin),minRevocationSequence:1};
 const stale=copy(f.record);
 stale.revocations=[];stale.operations=[];
 const invalid=copy(f.record);
 invalid.revocations[0].payload.retiredFingerprint='forged';
 const packets={
  current:{agentId:'agent-a',connection:'online',snapshot:copy(f.record)},
  stale:{agentId:'agent-b',connection:'online',snapshot:stale},
  offline:{agentId:'agent-c',connection:'offline',snapshot:copy(f.record)},
  invalid:{agentId:'agent-d',connection:'online',snapshot:invalid}
 };
 const names=mode==='mixed'?['current','stale','offline','invalid']:
  mode==='current'?['current']:mode==='stale'?['stale']:
  mode==='offline'?['offline']:mode==='invalid'?['invalid']:null;
 if(!names)throw Error('Unknown fixture');
 let ledger=await start(pin);
 for(const name of names)ledger=await append(ledger,packets[name],pin);
 return {ledger,pin,packets,source:f};
}
