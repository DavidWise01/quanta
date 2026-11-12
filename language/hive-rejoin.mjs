// QG-069 — Rejoining the Hive. Offline history is retained, never authority.
// All pins and expected checkpoint digests come from an independent trusted caller.
// This is a local deterministic model, not a real remote-attestation or sync service.
import {inspectAgent,requireFloor} from './hive-revocation-floor.mjs';
import {verify as verifyRevocation} from './revocation-outlives-recovery.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-069';
const copy=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>canonical(a)===canonical(b);
const named=x=>typeof x==='string'&&x.length>0&&x.length<=120;
async function inspectSource(source,pin){
 if(!source||!named(source.agentId)||!source.snapshot||source.connection!=='offline')
  throw Error('Initial agent must be offline');
 const r=await inspectAgent(source,pin);
 if(r.state!=='offline'||r.mayAuthorize)throw Error('Initial state must lack authority');
 return r;
}
export async function start(source,pin,checkpointDigest){
 requireFloor(pin);
 if(typeof checkpointDigest!=='string'||!/^[a-f0-9]{64}$/.test(checkpointDigest))
  throw Error('Independently pinned checkpoint digest required');
 await inspectSource(source,pin);
 return {version:VERSION,source:copy(source),pinnedFloor:copy(pin),
  checkpointDigest,offlineLog:[],checkpoint:null,authorization:null,
  eventLog:[{index:0,kind:'offline',agentId:source.agentId}],
  state:'offline',mayAuthorize:false};
}
async function assess(ledger,pin,externalDigest){
 requireFloor(pin);
 if(!ledger||ledger.version!==VERSION||!equal(ledger.pinnedFloor,pin)||
 ledger.checkpointDigest!==externalDigest)throw Error('Independent pin mismatch');
 const origin=await inspectSource(ledger.source,pin);
 if(!Array.isArray(ledger.offlineLog)||!Array.isArray(ledger.eventLog))throw Error('Malformed recovery log');
 const notes=[];
 for(let i=0;i<ledger.offlineLog.length;i++){
  const n=ledger.offlineLog[i];
  if(!n||!named(n.id)||typeof n.message!=='string'||n.message.length>600||
    ledger.offlineLog.slice(0,i).some(v=>v.id===n.id))throw Error('Invalid or duplicated offline note');
  notes.push({index:notes.length+1,kind:'offline-observation',id:n.id});
 }
 let state='offline',mayAuthorize=false,digest=null;
 if(ledger.checkpoint!==null){
  const cp=ledger.checkpoint;
  if(!cp||cp.agentId!==ledger.source.agentId||cp.connection!=='online'||!cp.snapshot)
   throw Error('Invalid reconnect checkpoint');
  digest=await sha256(canonical(cp.snapshot));
  if(digest!==ledger.checkpointDigest)throw Error('Checkpoint does not match independently pinned digest');
  const inspection=await inspectAgent(cp,pin);
  if(inspection.state!=='current'||!inspection.mayAuthorize)throw Error('Checkpoint not current');
  await verifyRevocation(cp.snapshot,pin);
  notes.push({index:notes.length+1,kind:'verified-reconnect',digest});
  state='verified-awaiting-authorization';
 }
 if(ledger.authorization!==null){
  if(state!=='verified-awaiting-authorization'||!ledger.authorization||
    ledger.authorization.agentId!==ledger.source.agentId||
    ledger.authorization.digest!==digest||
    ledger.authorization.floor!==pin.minRevocationSequence||
    ledger.authorization.intent!=='explicit-rejoin')
   throw Error('Unauthorized rejoin certificate');
  notes.push({index:notes.length+1,kind:'explicit-authorization',digest});
  state='rejoined';mayAuthorize=true;
 }
 if(!equal(ledger.eventLog,[{index:0,kind:'offline',agentId:ledger.source.agentId},...notes])||
 ledger.state!==state||ledger.mayAuthorize!==mayAuthorize)throw Error('Rejoin replay mismatch');
 return {valid:true,sourceDigest:origin.digest,currentDigest:digest,state,mayAuthorize,
  offlineNotes:ledger.offlineLog.length,events:ledger.eventLog.length,historyPreserved:true};
}
export async function verify(ledger,pin,externalDigest){return assess(ledger,pin,externalDigest)}
export async function observe(ledger,note,pin,digest){
 await verify(ledger,pin,digest);
 if(ledger.checkpoint!==null)throw Error('Offline history is closed after reconnect');
 const next={...copy(ledger),offlineLog:[...copy(ledger.offlineLog),copy(note)]};
 if(!named(note?.id)||typeof note.message!=='string'||note.message.length>600)throw Error('Invalid offline note');
 next.eventLog.push({index:next.eventLog.length,kind:'offline-observation',id:note.id});
 await verify(next,pin,digest);
 return next;
}
export async function reconnect(ledger,checkpoint,pin,digest){
 await verify(ledger,pin,digest);
 if(ledger.checkpoint!==null)throw Error('Already reconnected');
 const next={...copy(ledger),checkpoint:copy(checkpoint)};
 const currentDigest=await sha256(canonical(checkpoint?.snapshot));
 next.eventLog.push({index:next.eventLog.length,kind:'verified-reconnect',digest:currentDigest});
 next.state='verified-awaiting-authorization';
 await verify(next,pin,digest);return next;
}
export async function authorize(ledger,pin,digest){
 const state=await verify(ledger,pin,digest);
 if(state.state!=='verified-awaiting-authorization')throw Error('Verified reconnect required before authorization');
 const next={...copy(ledger),authorization:{agentId:ledger.source.agentId,digest:state.currentDigest,
  floor:pin.minRevocationSequence,intent:'explicit-rejoin'}};
 next.eventLog.push({index:next.eventLog.length,kind:'explicit-authorization',digest:state.currentDigest});
 next.state='rejoined';next.mayAuthorize=true;
 await verify(next,pin,digest);return next;
}
export async function fixture(kind='valid'){
 const {fixture:baseFixture}=await import('./hive-revocation-floor.mjs');
 const base=await baseFixture('mixed');
 const pin=copy(base.pin),current=copy(base.packets.current.snapshot);
 const digest=await sha256(canonical(current));
 const origin={agentId:'agent-c',connection:'offline',snapshot:copy(base.packets.offline.snapshot)};
 let record=await start(origin,pin,digest);
 record=await observe(record,{id:'note-1',message:'observed while offline'},pin,digest);
 const proposed={agentId:'agent-c',connection:'online',snapshot:copy(current)};
 if(kind==='stale'){proposed.snapshot=copy(base.packets.stale.snapshot)}
 if(kind==='tampered'){proposed.snapshot.revocations[0].payload.retiredFingerprint='forged'}
 if(kind==='wrong-digest'){proposed.snapshot.operations[0].action='unexpected'}
 if(kind==='offline'){proposed.connection='offline'}
 if(kind==='pending')return {record,pin,digest,proposed};
 record=await reconnect(record,proposed,pin,digest);
 if(kind==='verified')return {record,pin,digest,proposed};
 if(kind==='valid')record=await authorize(record,pin,digest);
 return {record,pin,digest,proposed};
}
