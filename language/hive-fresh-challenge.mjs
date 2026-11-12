// QG-070 — Freshness Must Be Proven.
// One signed, random challenge per QG-069 rejoin. An external issuer key and agent key
// are independently pinned; consumed challenges must persist outside untrusted clients.
// Synthetic Ed25519 only; no real online freshness/clock/network attestation.
import {verify as verifyRejoin,authorize as authorizeRejoin} from './hive-rejoin.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
import {generateFixtureSigner} from './signed-trust-anchor.mjs';
export const VERSION='QG-070',CHALLENGE_SCHEMA='QUANTA-QG-070-CHALLENGE';
const copy=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>canonical(a)===canonical(b);
const bytes=x=>new TextEncoder().encode(canonical(x));
const b64=x=>btoa(Array.from(new Uint8Array(x),c=>String.fromCharCode(c)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
function unb64(s){
 if(typeof s!=='string'||!/^[A-Za-z0-9_-]+$/.test(s))throw Error('Malformed signature');
 return Uint8Array.from(atob(s.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-s.length%4)%4)),c=>c.charCodeAt(0));
}
async function checkedKey(jwk){
 if(!jwk||jwk.kty!=='OKP'||jwk.crv!=='Ed25519')throw Error('Ed25519 public key required');
 try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}
 catch{throw Error('Invalid Ed25519 public key')}
}
async function sign(privateKey,payload){
 if(privateKey?.algorithm?.name!=='Ed25519'||!privateKey.usages?.includes('sign'))throw Error('Ed25519 private key required');
 return b64(await crypto.subtle.sign('Ed25519',privateKey,bytes(payload)));
}
async function check(publicKey,payload,signature){
 let valid=false;
 try{valid=await crypto.subtle.verify('Ed25519',await checkedKey(publicKey),unb64(signature),bytes(payload))}
 catch{throw Error('Unverifiable Ed25519 signature')}
 if(!valid)throw Error('Ed25519 signature mismatch');
}
function trustValid(trust){
 if(!trust||!trust.pin||typeof trust.checkpointDigest!=='string'||
 !/^[0-9a-f]{64}$/.test(trust.checkpointDigest)||
 typeof trust.agentId!=='string'||!trust.agentId||
 !trust.agentPublicKey||!trust.issuerPublicKey||
 !Number.isSafeInteger(trust.minChallengeSequence)||trust.minChallengeSequence<0)
 throw Error('Independent agent, issuer, checkpoint and challenge floor required');
}
async function baseState(rejoin,trust){
 trustValid(trust);
 await Promise.all([checkedKey(trust.agentPublicKey),checkedKey(trust.issuerPublicKey)]);
 if(rejoin?.source?.agentId!==trust.agentId)throw Error('Agent identity does not match pin');
 const status=await verifyRejoin(rejoin,trust.pin,trust.checkpointDigest);
 if(status.state!=='verified-awaiting-authorization'||status.mayAuthorize)
 throw Error('Verified but unauthorized QG-069 rejoin required');
 return {rejoinDigest:await sha256(canonical(rejoin)),checkpointDigest:status.currentDigest,
  floor:trust.pin.minRevocationSequence};
}
export async function start(rejoin,trust){
 await baseState(rejoin,trust);
 if(trust.minChallengeSequence!==0)throw Error('Independent floor requires consumed challenge evidence');
 return {version:VERSION,rejoin:copy(rejoin),challenge:null,response:null,authorization:null,
  state:'awaiting-challenge',mayAuthorize:false};
}
export async function verify(record,trust){
 trustValid(trust);
 if(!record||record.version!==VERSION)throw Error('Malformed freshness ledger');
 const b=await baseState(record.rejoin,trust);
 let state='awaiting-challenge',mayAuthorize=false,sequence=0,challengeDigest=null;
 if(record.challenge!==null){
  const q=record.challenge,p=q?.payload;
  if(!p||p.schema!==CHALLENGE_SCHEMA||p.sequence!==1||
   p.agentId!==trust.agentId||p.rejoinDigest!==b.rejoinDigest||
   p.checkpointDigest!==b.checkpointDigest||p.revocationFloor!==b.floor||
   typeof p.nonce!=='string'||!/^[0-9a-f]{64}$/.test(p.nonce))
   throw Error('Challenge identity, floor or nonce mismatch');
  await check(trust.issuerPublicKey,p,q.issuerSignature);
  challengeDigest=await sha256(canonical(q));
  state='challenge-issued';sequence=1;
 }
 if(record.response!==null){
  if(state!=='challenge-issued')throw Error('Unsolicited challenge response');
  const rp=record.response?.payload;
  const expected={schema:'QUANTA-QG-070-RESPONSE',agentId:trust.agentId,
   sequence:1,challengeDigest,checkpointDigest:b.checkpointDigest,revocationFloor:b.floor};
  if(!same(rp,expected))throw Error('Response is not bound to issued challenge');
  await check(trust.agentPublicKey,rp,record.response.agentSignature);
  state='challenge-consumed';
 }
 if(record.authorization!==null){
  if(state!=='challenge-consumed'||!record.authorization||record.authorization.challengeDigest!==challengeDigest||
  record.authorization.intent!=='explicit-fresh-rejoin')
   throw Error('Unauthorized rejoin replay');
  const expected=await authorizeRejoin(record.rejoin,trust.pin,trust.checkpointDigest);
  if(!same(record.authorization.rejoined,expected))throw Error('Rejoin certificate mismatch');
  state='rejoined';mayAuthorize=true;
 }
 if(record.state!==state||record.mayAuthorize!==mayAuthorize)throw Error('Freshness state replay mismatch');
 if(sequence<trust.minChallengeSequence)throw Error('Challenge replay below independent floor');
 return {valid:true,state,mayAuthorize,sequence,challengeDigest,
  historyPreserved:true,nonceConsumed:state==='challenge-consumed'||state==='rejoined'};
}
export async function issue(record,issuerPrivateKey,trust){
 const v=await verify(record,trust);
 if(v.state!=='awaiting-challenge')throw Error('Challenge already issued');
 const nonce=Array.from(crypto.getRandomValues(new Uint8Array(32)),x=>x.toString(16).padStart(2,'0')).join('');
 const payload={schema:CHALLENGE_SCHEMA,sequence:1,nonce,agentId:trust.agentId,
  checkpointDigest:trust.checkpointDigest,
  rejoinDigest:await sha256(canonical(record.rejoin)),
  revocationFloor:trust.pin.minRevocationSequence};
 const challenge={payload,issuerSignature:await sign(issuerPrivateKey,payload)};
 const next={...copy(record),challenge,state:'challenge-issued'};
 await verify(next,trust);return next;
}
export async function respond(record,agentPrivateKey,trust){
 const v=await verify(record,trust);
 if(v.state!=='challenge-issued')throw Error('No outstanding challenge');
 const payload={schema:'QUANTA-QG-070-RESPONSE',agentId:trust.agentId,
  sequence:1,challengeDigest:v.challengeDigest,checkpointDigest:trust.checkpointDigest,
  revocationFloor:trust.pin.minRevocationSequence};
 return {payload,agentSignature:await sign(agentPrivateKey,payload)};
}
export async function consume(record,response,trust){
 const v=await verify(record,trust);
 if(v.state!=='challenge-issued')throw Error('Challenge already consumed or not issued');
 const next={...copy(record),response:copy(response),state:'challenge-consumed'};
 await verify(next,trust);return next;
}
export async function authorize(record,trust){
 const v=await verify(record,trust);
 if(v.state!=='challenge-consumed')throw Error('Consumed challenge required for explicit authorization');
 const rejoined=await authorizeRejoin(record.rejoin,trust.pin,trust.checkpointDigest);
 const next={...copy(record),authorization:{challengeDigest:v.challengeDigest,
  intent:'explicit-fresh-rejoin',rejoined},state:'rejoined',mayAuthorize:true};
 await verify(next,trust);return next;
}
export async function fixture(kind='valid'){
 const {fixture:rejoinFixture}=await import('./hive-rejoin.mjs');
 const f=await rejoinFixture('verified');
 const agent=await generateFixtureSigner(),issuer=await generateFixtureSigner();
 const trust={pin:copy(f.pin),checkpointDigest:f.digest,agentId:f.record.source.agentId,
  agentPublicKey:copy(agent.publicJwk),issuerPublicKey:copy(issuer.publicJwk),
  minChallengeSequence:0};
 let record=await start(f.record,trust);
 if(kind==='pending')return {record,trust,agent,issuer,f};
 record=await issue(record,issuer.privateKey,trust);
 if(kind==='issued')return {record,trust,agent,issuer,f};
 let response=await respond(record,agent.privateKey,trust);
 if(kind==='bad-agent'){const other=await generateFixtureSigner();response=await respond(record,other.privateKey,trust)}
 if(kind==='tampered-response')response.payload.agentId='other-agent';
 if(kind==='replay-old-response'){const earlier=record;record=await issue(await start(f.record,trust),issuer.privateKey,trust);return {record,trust,agent,issuer,f,response,earlier}}
 if(kind==='response-only')return {record,trust,agent,issuer,f,response};
 record=await consume(record,response,trust);
 if(kind==='consumed')return {record,trust,agent,issuer,f,response};
 if(kind==='valid')record=await authorize(record,trust);
 return {record,trust,agent,issuer,f,response};
}
