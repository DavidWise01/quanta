// QG-075 — Release Can Be Withdrawn.
// New quorum-signed withdrawal events; QG-074 approval remains immutable.
// Synthetic enforcement only: consumers MUST use authorizePublication here,
// rather than the historical QG-074-only function.
import {audit as auditRelease, fixture as releaseFixture, scopeFixture} from './independent-declassification.mjs';
import {authorizeAction as scopeAuthorize} from './hive-scoped-authority.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-075',SCHEMA='QUANTA-QG-075-WITHDRAWAL';
const clone=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>canonical(a)===canonical(b);
const bytes=x=>new TextEncoder().encode(canonical(x));
const encode=x=>btoa(Array.from(new Uint8Array(x),c=>String.fromCharCode(c)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
function decode(x){if(typeof x!=='string'||!/^[A-Za-z0-9_-]+$/.test(x))throw Error('Bad signature encoding');return Uint8Array.from(atob(x.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-x.length%4)%4)),c=>c.charCodeAt(0))}
async function publicKey(jwk){if(jwk?.kty!=='OKP'||jwk?.crv!=='Ed25519')throw Error('Pinned Ed25519 key required');try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}catch{throw Error('Invalid Ed25519 verification key')}}
async function sign(key,payload){if(key?.algorithm?.name!=='Ed25519'||!key.usages.includes('sign'))throw Error('Reviewer signing key required');return encode(await crypto.subtle.sign('Ed25519',key,bytes(payload)))}
async function verifySignature(pub,payload,sig){let valid=false;try{valid=await crypto.subtle.verify('Ed25519',await publicKey(pub),decode(sig),bytes(payload))}catch{throw Error('Malformed reviewer signature')}if(!valid)throw Error('Withdrawal signature verification failed')}
function validPin(pin){
 if(!pin||!pin.releasePolicy||!Number.isSafeInteger(pin.minWithdrawalSequence)||pin.minWithdrawalSequence<0)
 throw Error('Independent withdrawal policy and rollback floor required');
}
async function verifyBase(releases,pin){validPin(pin);await auditRelease(releases,pin.releasePolicy)}
const hash=x=>sha256(canonical(x));
export async function start(releases,pin){
 await verifyBase(releases,pin);
 if(pin.minWithdrawalSequence!==0)throw Error('Withdrawal floor requires retained event history');
 return {version:VERSION,releases:clone(releases),releaseDigest:await hash(releases),
  events:[],status:releases.releases.map(r=>({id:r.payload.id,withdrawn:false}))};
}
function expectedStatus(releases,events){
 const withdrawn=new Set(events.map(e=>e.payload.releaseId));
 return releases.releases.map(r=>({id:r.payload.id,withdrawn:withdrawn.has(r.payload.id)}));
}
export async function verify(record,pin){
 validPin(pin);
 if(!record||record.version!==VERSION||!Array.isArray(record.events)||!Array.isArray(record.status))
 throw Error('Invalid withdrawal ledger');
 await verifyBase(record.releases,pin);
 if(record.releaseDigest!==await hash(record.releases))throw Error('Approved history was rewritten');
 let previous='GENESIS';
 const used=new Set();
 for(let i=0;i<record.events.length;i++){
  const e=record.events[i],p=e?.payload;
  const release=record.releases.releases.find(r=>r.payload.id===p?.releaseId);
  if(!p||p.schema!==SCHEMA||p.sequence!==i+1||p.previousHash!==previous||
    p.releaseHistoryDigest!==record.releaseDigest||p.reason!=='risk_discovered'||
    !release||used.has(p.releaseId)||p.releaseEntryDigest!==await hash(release)||
    p.exactPublicDigest!==release.payload.releaseDigest||p.destination!==release.payload.destination)
   throw Error('Withdrawal sequence or release binding mismatch');
  if(!Array.isArray(e.votes)||e.votes.length<3||
    e.votes.length>pin.releasePolicy.reviewers.length)throw Error('Three reviewer signatures required');
  const ids=new Set(),roots=new Set();
  for(const vote of e.votes){
   const reviewer=pin.releasePolicy.reviewers.find(r=>r.id===vote?.reviewerId);
   if(!reviewer||ids.has(reviewer.id))throw Error('Duplicate or unpinned reviewer');
   ids.add(reviewer.id);roots.add(reviewer.ancestryRoot);
   await verifySignature(reviewer.publicJwk,p,vote.signature);
  }
  if(roots.size<3)throw Error('Insufficient independent reviewer ancestry');
  used.add(p.releaseId);previous=await hash(e);
 }
 if(record.events.length<pin.minWithdrawalSequence)throw Error('Withdrawal rollback below independent floor');
 const expected=expectedStatus(record.releases,record.events);
 if(!same(expected,record.status))throw Error('Withdrawal status replay mismatch');
 return {valid:true,approved:record.releases.releases.length,withdrawals:record.events.length,
  withdrawn:expected.filter(s=>s.withdrawn).length,active:expected.filter(s=>!s.withdrawn).length,
  originalApprovalsPreserved:true,status:clone(expected)};
}
export async function petition(record,releaseId,pin){
 await verify(record,pin);
 if(record.events.some(e=>e.payload.releaseId===releaseId))throw Error('Already withdrawn');
 const release=record.releases.releases.find(r=>r.payload.id===releaseId);
 if(!release)throw Error('Approved release missing');
 return {schema:SCHEMA,sequence:record.events.length+1,releaseId,
  releaseEntryDigest:await hash(release),exactPublicDigest:release.payload.releaseDigest,
  releaseHistoryDigest:record.releaseDigest,destination:release.payload.destination,
  reason:'risk_discovered',previousHash:record.events.length?await hash(record.events.at(-1)):'GENESIS'};
}
export async function review(payload,reviewerId,privateKey){
 if(payload?.schema!==SCHEMA||typeof reviewerId!=='string'||!reviewerId)
 throw Error('Invalid withdrawal petition');
 return {reviewerId,signature:await sign(privateKey,payload)};
}
export async function withdraw(record,payload,votes,pin){
 await verify(record,pin);
 const expected=await petition(record,payload?.releaseId,pin);
 if(!same(payload,expected))throw Error('Petition not bound to approved exact release');
 const next={...clone(record),events:[...clone(record.events),{payload:clone(payload),votes:clone(votes)}]};
 next.status=expectedStatus(next.releases,next.events);
 await verify(next,pin);return next;
}
export async function authorizePublication(record,releaseId,scope,trust,clock,pin){
 const state=await verify(record,pin);
 const disposition=state.status.find(s=>s.id===releaseId);
 if(!disposition)throw Error('No approved release');
 if(disposition.withdrawn)throw Error('Release withdrawn: future publication denied');
 const approved=record.releases.releases.find(r=>r.payload.id===releaseId);
 const capability=await scopeAuthorize(scope,{action:'publish',surface:approved.payload.destination,
  originSurface:'0root.ai',classification:'public'},trust,clock);
 return {allowed:true,releaseId,releaseDigest:approved.payload.releaseDigest,
  withdrawalSequence:state.withdrawals,originalApprovalPreserved:true,capability};
}
export async function fixture(mode='withdrawn'){
 const base=await releaseFixture('valid');
 const pin={releasePolicy:clone(base.policy),minWithdrawalSequence:0};
 let record=await start(base.record,pin);
 const payload=await petition(record,'release-1',pin);
 const votes=await Promise.all([0,1,2].map(i=>review(payload,'reviewer-'+i,
   mode==='forged'&&i===2?base.reviewers[3].privateKey:base.reviewers[i].privateKey)));
 if(mode==='duplicate')votes[2]=clone(votes[1]);
 if(mode==='shared'){
  pin.releasePolicy.reviewers[2].ancestryRoot=pin.releasePolicy.reviewers[1].ancestryRoot;
  // Policy update is an invalid substitution, not an approved ancestry change.
 }
 if(mode==='approved')return {...base,pin,record,payload,votes};
 record=await withdraw(record,payload,votes,pin);
 return {...base,pin,record,payload,votes};
}
export {scopeFixture};
