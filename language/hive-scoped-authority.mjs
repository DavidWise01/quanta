// QG-072 — Authority Must Have Scope.
// Explicit issuer-signed capability matrix bound to QG-071 signed lease.
// Synthetic only: authorization decisions, never network/API or filesystem writes.
import {verify as verifyLease,fixture as leaseFixture} from './hive-authority-lease.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-072',SCHEMA='QUANTA-QG-072-SCOPE';
export const SURFACES=Object.freeze(['github','0root.ai','public-internet']);
export const ACTIONS=Object.freeze(['observe','learn','publish','modify']);
const copy=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>canonical(a)===canonical(b);
const bytes=x=>new TextEncoder().encode(canonical(x));
const b64=x=>btoa(Array.from(new Uint8Array(x),c=>String.fromCharCode(c)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
function unb64(x){if(typeof x!=='string'||!/^[A-Za-z0-9_-]+$/.test(x))throw Error('Malformed signature');return Uint8Array.from(atob(x.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-x.length%4)%4)),c=>c.charCodeAt(0))}
function validScope(scope){
 if(!Array.isArray(scope)||scope.length<1||scope.length>16)throw Error('Nonempty finite scope required');
 const unique=new Set();
 for(const item of scope){
  if(!item||!ACTIONS.includes(item.action)||!SURFACES.includes(item.surface)||
    Object.keys(item).sort().join(',')!=='action,surface')throw Error('Invalid scope rule');
  const k=item.action+'|'+item.surface;
  if(unique.has(k))throw Error('Duplicate scope rule');
  unique.add(k);
  // Public-facing internet is a discovery surface, not an unrestricted publishing sink.
  if(item.surface==='public-internet'&&['publish','modify'].includes(item.action))
   throw Error('Public internet is discovery-only in this model');
 }
}
async function key(jwk){
 if(jwk?.kty!=='OKP'||jwk?.crv!=='Ed25519')throw Error('Ed25519 issuer key required');
 try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}
 catch{throw Error('Unusable Ed25519 issuer key')}
}
async function sign(priv,payload){
 if(priv?.algorithm?.name!=='Ed25519'||!priv.usages.includes('sign'))throw Error('Issuer signing key required');
 return b64(await crypto.subtle.sign('Ed25519',priv,bytes(payload)));
}
async function check(pub,payload,proof){
 let good=false;
 try{good=await crypto.subtle.verify('Ed25519',await key(pub),unb64(proof),bytes(payload))}
 catch{throw Error('Malformed signed scope')}
 if(!good)throw Error('Scope signature mismatch');
}
async function leaseEvidence(record,trust,clock){
 const v=await verifyLease(record,trust,clock);
 const last=record.leases.at(-1);
 if(!last)throw Error('Signed QG-071 lease required');
 return {leaseDigest:await sha256(canonical(last)),leaseSequence:v.count,
  agentId:trust.agentId,revocationFloor:trust.pin.minRevocationSequence,
  checkpointDigest:trust.checkpointDigest,active:v.active};
}
export async function start(lease,trust,clock){
 const info=await leaseEvidence(lease,trust,clock);
 return {version:VERSION,lease:copy(lease),trust:copy(trust),grant:null,decisions:[],
  state:'awaiting-scope'};
}
export async function verify(record,trust,clock){
 if(!record||record.version!==VERSION||!equal(record.trust,trust)||
 !Array.isArray(record.decisions))throw Error('Malformed scope ledger or trust pin');
 const info=await leaseEvidence(record.lease,trust,clock);
 let scope=[],state='awaiting-scope';
 if(record.grant!==null){
  const payload=record.grant?.payload;
  if(!payload||payload.schema!==SCHEMA||payload.agentId!==info.agentId||
    payload.leaseDigest!==info.leaseDigest||payload.leaseSequence!==info.leaseSequence||
    payload.revocationFloor!==info.revocationFloor||
    payload.checkpointDigest!==info.checkpointDigest)
   throw Error('Grant not bound to signed lease and current identity');
  validScope(payload.rules);
  await check(trust.issuerPublicKey,payload,record.grant.signature);
  scope=payload.rules;
  state='scoped';
 }
 for(let i=0;i<record.decisions.length;i++){
  const d=record.decisions[i];
  if(!d||d.index!==i||d.grantDigest!==await sha256(canonical(record.grant))||
    d.leaseDigest!==info.leaseDigest||!d.request)throw Error('Decision replay mismatch');
  const expected=decisionFor(d.request,scope,true);
  if(!equal(d.result,expected))throw Error('Forged scope decision');
 }
 if(record.state!==state)throw Error('Scope state replay mismatch');
 return {valid:true,state,active:info.active,scope:copy(scope),decisions:record.decisions.length,
  leaseDigest:info.leaseDigest,agentId:info.agentId};
}
export async function grant(record,issuerPrivateKey,rules,trust,clock){
 const v=await verify(record,trust,clock);
 if(record.grant!==null)throw Error('Grant already sealed');
 if(!v.active)throw Error('Expired lease cannot receive scope');
 validScope(rules);
 const payload={schema:SCHEMA,agentId:trust.agentId,
  leaseDigest:v.leaseDigest,leaseSequence:record.lease.leases.length,
  revocationFloor:trust.pin.minRevocationSequence,
  checkpointDigest:trust.checkpointDigest,rules:copy(rules)};
 const next={...copy(record),grant:{payload,signature:await sign(issuerPrivateKey,payload)},state:'scoped'};
 await verify(next,trust,clock);
 return next;
}
function decisionFor(request,rules,grantPresent){
 if(!request||!ACTIONS.includes(request.action)||!SURFACES.includes(request.surface)||
 !SURFACES.includes(request.originSurface)||!['public','gated'].includes(request.classification))
 throw Error('Invalid action or surface request');
 // Origin/gated classification is model metadata, not verified information-flow taint.
 if(request.classification==='gated'&&request.originSurface!=='github')
 return {allowed:false,reason:'invalid-gated-origin'};
 if(request.classification==='gated'&&request.surface!=='github')
 return {allowed:false,reason:'gated-export-denied'};
 if(request.originSurface==='github'&&request.surface!=='github'&&request.classification==='gated')
 return {allowed:false,reason:'gated-export-denied'};
 if(request.surface==='public-internet'&&['publish','modify'].includes(request.action))
 return {allowed:false,reason:'external-discovery-only'};
 if(!grantPresent||!rules.some(r=>r.action===request.action&&r.surface===request.surface))
 return {allowed:false,reason:'outside-signed-scope'};
 return {allowed:true,reason:'within-signed-scope'};
}
export async function authorizeAction(record,request,trust,clock){
 const state=await verify(record,trust,clock);
 if(!state.active)throw Error('Lease expired or not yet active');
 if(!record.grant)throw Error('No signed scope grant');
 const result=decisionFor(request,state.scope,true);
 if(!result.allowed)throw Error('Scope denied: '+result.reason);
 return {agentId:trust.agentId,request:copy(request),allowed:true,
  leaseDigest:state.leaseDigest,grantDigest:await sha256(canonical(record.grant)),
  at:clock.tick};
}
export async function appendDecision(record,request,trust,clock){
 const state=await verify(record,trust,clock);
 if(!state.active||!record.grant)throw Error('Active lease and signed grant required');
 const result=decisionFor(request,state.scope,true);
 const d={index:record.decisions.length,request:copy(request),result,
  leaseDigest:state.leaseDigest,grantDigest:await sha256(canonical(record.grant))};
 const next={...copy(record),decisions:[...copy(record.decisions),d]};
 await verify(next,trust,clock);
 return next;
}
export async function fixture(kind='valid'){
 const f=await leaseFixture(kind==='expired'?'expired':'active');
 const rules=[{action:'observe',surface:'public-internet'},
  {action:'learn',surface:'0root.ai'},{action:'observe',surface:'github'}];
 let record=await start(f.record,f.trust,f.clock);
 if(kind==='unsigned')return {...f,record,rules};
 if(kind==='expired')return {...f,record,rules};
 record=await grant(record,f.issuer.privateKey,rules,f.trust,f.clock);
 if(kind==='valid')record=await appendDecision(record,{action:'observe',surface:'public-internet',
  originSurface:'public-internet',classification:'public'},f.trust,f.clock);
 return {...f,record,rules};
}
