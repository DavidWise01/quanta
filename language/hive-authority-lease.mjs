// QG-071 — Authority Has a Lifetime.
// Signed, bounded logical-time leases with independently supplied clock and floor.
// Demo only: NOT a trusted clock, durable consumed-nonce store, or distributed authority.
import {verify as verifyFresh} from './hive-fresh-challenge.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-071',SCHEMA='QUANTA-QG-071-LEASE',MAX_TICKS=300;
const cp=x=>JSON.parse(JSON.stringify(x)),same=(a,b)=>canonical(a)===canonical(b);
const data=x=>new TextEncoder().encode(canonical(x));
const b64=x=>btoa(Array.from(new Uint8Array(x),c=>String.fromCharCode(c)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
function unb64(x){if(typeof x!=='string'||!/^[A-Za-z0-9_-]+$/.test(x))throw Error('Malformed signature');return Uint8Array.from(atob(x.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-x.length%4)%4)),c=>c.charCodeAt(0))}
function validClock(clock){
 if(!clock||!Number.isSafeInteger(clock.tick)||clock.tick<0||
 !Number.isSafeInteger(clock.floor)||clock.floor<0||clock.tick<clock.floor)
 throw Error('Independently trusted monotonic clock required');
}
async function signer(privateKey,payload){
 if(privateKey?.algorithm?.name!=='Ed25519'||!privateKey.usages?.includes('sign'))
 throw Error('Trusted issuer private key required');
 return b64(await crypto.subtle.sign('Ed25519',privateKey,data(payload)));
}
async function signature(key,payload,proof){
 let k;try{k=await crypto.subtle.importKey('jwk',key,{name:'Ed25519'},false,['verify'])}
 catch{throw Error('Invalid pinned issuer key')}
 let ok=false;try{ok=await crypto.subtle.verify('Ed25519',k,unb64(proof),data(payload))}
 catch{throw Error('Malformed issuer signature')}
 if(!ok)throw Error('Issuer lease signature rejected');
}
async function fresh(record,trust){
 const state=await verifyFresh(record,trust);
 if(state.state!=='rejoined'||!state.mayAuthorize)throw Error('Fully authorized QG-070 rejoin required');
 return {challengeDigest:state.challengeDigest,agentId:trust.agentId,
 checkpointDigest:trust.checkpointDigest,revocationFloor:trust.pin.minRevocationSequence,
 freshDigest:await sha256(canonical(record))};
}
function leasePayload(f,sequence,previous,issuedAt,duration){
 if(!Number.isSafeInteger(duration)||duration<1||duration>MAX_TICKS)throw Error('Lease duration outside bound');
 if(!Number.isSafeInteger(issuedAt)||issuedAt<0||issuedAt>Number.MAX_SAFE_INTEGER-duration)throw Error('Invalid lease start');
 return {schema:SCHEMA,sequence,previousHash:previous,agentId:f.agentId,
 challengeDigest:f.challengeDigest,checkpointDigest:f.checkpointDigest,
 revocationFloor:f.revocationFloor,freshDigest:f.freshDigest,
 issuedAt,expiresAt:issuedAt+duration};
}
export async function start(freshRecord,trust){
 await fresh(freshRecord,trust);
 return {version:VERSION,trust:cp(trust),freshSessions:[cp(freshRecord)],leases:[]};
}
export async function verify(record,trust,clock){
 validClock(clock);
 if(!record||record.version!==VERSION||!same(record.trust,trust)||
 !Array.isArray(record.leases)||!Array.isArray(record.freshSessions)||
 record.freshSessions.length!==Math.max(1,record.leases.length))throw Error('Malformed lease lineage or independent pin');
 const sessions=await Promise.all(record.freshSessions.map(r=>fresh(r,trust)));
 let previous='GENESIS',priorExpiration=-1;
 const used=new Set();
 for(let i=0;i<record.leases.length;i++){
  const lease=record.leases[i],p=lease?.payload,f=sessions[i];
  if(!p||p.schema!==SCHEMA||p.sequence!==i+1||p.previousHash!==previous||
  !Number.isSafeInteger(p.issuedAt)||!Number.isSafeInteger(p.expiresAt)||
  p.issuedAt<0||p.expiresAt<=p.issuedAt||p.expiresAt-p.issuedAt>MAX_TICKS||
  p.issuedAt<priorExpiration)throw Error('Lease sequence, timing or linkage mismatch');
  const expected=leasePayload(f,i+1,previous,p.issuedAt,p.expiresAt-p.issuedAt);
  if(!same(expected,p)||used.has(f.challengeDigest))throw Error('Replayed challenge or altered lease identity');
  await signature(trust.issuerPublicKey,p,lease.signature);
  used.add(f.challengeDigest);previous=await sha256(canonical(lease));priorExpiration=p.expiresAt;
 }
 const last=record.leases.at(-1)?.payload;
 // The clock floor is a separately maintained minimum accepted tick; the issuer
 // must obtain both it and clock.tick from trusted monotonic infrastructure.
 const active=!!last&&clock.tick>=last.issuedAt&&clock.tick<last.expiresAt;
 return {valid:true,active,authority:active?'leased':'denied',count:record.leases.length,
  now:clock.tick,expiresAt:last?.expiresAt??null,agentId:trust.agentId,
  historicalLeasesRetained:record.leases.length};
}
export async function issue(record,privateKey,clock,duration,trust){
 await verify(record,trust,clock);
 if(record.leases.length)throw Error('Initial lease already issued; renew with new proof');
 const f=await fresh(record.freshSessions[0],trust);
 const p=leasePayload(f,1,'GENESIS',clock.tick,duration);
 const next=cp(record);next.leases.push({payload:p,signature:await signer(privateKey,p)});
 await verify(next,trust,clock);return next;
}
export async function renew(record,newFreshRecord,privateKey,clock,duration,trust){
 const v=await verify(record,trust,clock);
 if(!v.count)throw Error('Existing lease required for renewal');
 const f=await fresh(newFreshRecord,trust);
 if(record.leases.some(l=>l.payload.challengeDigest===f.challengeDigest))
 throw Error('Renewal requires a fresh unused challenge');
 const last=record.leases.at(-1).payload;
 if(clock.tick<last.expiresAt)throw Error('Renewal requires expiry; no overlap');
 const previous=await sha256(canonical(record.leases.at(-1)));
 const payload=leasePayload(f,record.leases.length+1,previous,clock.tick,duration);
 const next=cp(record);next.freshSessions.push(cp(newFreshRecord));
 next.leases.push({payload,signature:await signer(privateKey,payload)});
 await verify(next,trust,clock);return next;
}
export async function authorizeAction(record,trust,clock,action){
 const state=await verify(record,trust,clock);
 if(!state.active)throw Error('Lease expired or not yet active');
 if(typeof action!=='string'||!action||action.length>120)throw Error('Invalid action');
 return {agentId:trust.agentId,action,leaseSequence:state.count,at:clock.tick,
  leaseDigest:await sha256(canonical(record.leases.at(-1))),allowed:true};
}
export async function fixture(mode='active'){
 const {fixture:freshFixture}=await import('./hive-fresh-challenge.mjs');
 const f=await freshFixture('valid'),trust=cp(f.trust);
 const at={tick:1000,floor:1000};
 let record=await start(f.record,trust);
 if(mode==='unissued')return {record,trust,issuer:f.issuer,clock:at,f};
 record=await issue(record,f.issuer.privateKey,at,60,trust);
 if(mode==='active')return {record,trust,issuer:f.issuer,clock:{tick:1030,floor:1000},f};
 if(mode==='expired')return {record,trust,issuer:f.issuer,clock:{tick:1060,floor:1000},f};
 if(mode==='not-yet')return {record,trust,issuer:f.issuer,clock:{tick:999,floor:999},f};
 if(mode==='renewed'){
  const next=await freshFixture('valid');
  // A new QG-070 challenge session tied to the SAME agent and trust anchor is
  // needed. Build it from the earlier rejoin with original issuer/agent keys.
  const {start:startFresh,issue:issueFresh,respond,consume,authorize}=await import('./hive-fresh-challenge.mjs');
  let fresher=await startFresh(f.record.rejoin,trust);
  fresher=await issueFresh(fresher,f.issuer.privateKey,trust);
  fresher=await consume(fresher,await respond(fresher,f.agent.privateKey,trust),trust);
  fresher=await authorize(fresher,trust);
  record=await renew(record,fresher,f.issuer.privateKey,{tick:1060,floor:1000},30,trust);
  return {record,trust,issuer:f.issuer,clock:{tick:1070,floor:1000},f,fresher};
 }
 throw Error('Unknown fixture');
}
