// QG-066 — Recovery Without the Old Key.
// Separate emergency recovery branch; NEVER misrepresents a recovery vote as QG-065 old-key signature.
// Synthetic pinned guardians, 3 distinct ancestral roots, Ed25519 PoP and history retention.
import {verifyChain,canonical} from './trust-anchor-rotation.mjs';
import {verifyManifest,generateFixtureSigner,signManifest} from './signed-trust-anchor.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-066', RECOVERY_SCHEMA='QUANTA-QG-066-RECOVERY';
const copy=x=>JSON.parse(JSON.stringify(x)), same=(a,b)=>canonical(a)===canonical(b);
const data=x=>new TextEncoder().encode(canonical(x));
const b64=x=>btoa(Array.from(new Uint8Array(x),v=>String.fromCharCode(v)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
function unb64(s){if(typeof s!=='string'||!/^[A-Za-z0-9_-]+$/.test(s))throw Error('Malformed signature');return Uint8Array.from(atob(s.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-s.length%4)%4)),v=>v.charCodeAt(0))}
async function getKey(jwk){
 if(!jwk||jwk.kty!=='OKP'||jwk.crv!=='Ed25519')throw Error('Ed25519 key required');
 try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}
 catch{throw Error('Unusable public key')}
}
async function sign(privateKey,payload){
 if(privateKey?.algorithm?.name!=='Ed25519'||!privateKey.usages.includes('sign'))throw Error('Signing key required');
 return b64(await crypto.subtle.sign('Ed25519',privateKey,data(payload)));
}
async function check(jwk,payload,signature){
 const key=await getKey(jwk);
 let result=false;
 try{result=await crypto.subtle.verify('Ed25519',key,unb64(signature),data(payload))}
 catch{throw Error('Malformed recovery signature')}
 if(!result)throw Error('Recovery signature failed');
}
async function fingerprint(jwk){return sha256(canonical(jwk))}
function validPin(pin){
 if(!pin||!pin.chainPin||!Array.isArray(pin.guardians)||pin.guardians.length<3||
 !Number.isSafeInteger(pin.minRecoverySequence)||pin.minRecoverySequence<0||
 !Number.isSafeInteger(pin.minRecoveredRevision)||pin.minRecoveredRevision<1)
 throw Error('Independent recovery policy pin required');
 const ids=new Set(),roots=new Set();
 for(const g of pin.guardians){
  if(!g||typeof g.id!=='string'||!g.id||typeof g.ancestryRoot!=='string'||!g.ancestryRoot||
    !g.publicJwk||ids.has(g.id))throw Error('Invalid pinned recovery guardian');
  ids.add(g.id);roots.add(g.ancestryRoot);
 }
 if(roots.size<3)throw Error('Pinned guardians share too few independent ancestry roots');
}
async function verifyPolicy(pin){
 validPin(pin);
 for(const g of pin.guardians)await getKey(g.publicJwk);
 return true;
}
async function baseProof(chain,chainPin){
 await verifyChain(chain,chainPin);
 return sha256(canonical(chain));
}
export async function start(chain,policyPin){
 await verifyPolicy(policyPin);
 const v=await verifyChain(chain,policyPin.chainPin);
 return {version:VERSION,history:copy(chain),historyDigest:await baseProof(chain,policyPin.chainPin),
  recovery:null,newManifests:[],historicalActiveEpoch:v.activeEpoch};
}
export async function request(record,newPublicJwk,policyPin){
 await verify(record,policyPin);
 if(record.recovery)throw Error('Recovery already sealed');
 await getKey(newPublicJwk);
 const prior=await verifyChain(record.history,policyPin.chainPin);
 const oldKey=prior.keys[prior.activeEpoch];
 if(await fingerprint(newPublicJwk)===await fingerprint(oldKey))throw Error('Successor must be a distinct key');
 return {schema:RECOVERY_SCHEMA,recoverySequence:1,priorChainDigest:record.historyDigest,
  retiredKeyFingerprint:await fingerprint(oldKey),successorKey:copy(newPublicJwk),
  successorFingerprint:await fingerprint(newPublicJwk),reason:'lost_or_compromised_key',
  minimumGuardianRoots:3};
}
export async function witness(payload,guardianId,guardianPrivateKey){
 if(!payload||payload.schema!==RECOVERY_SCHEMA)throw Error('Invalid recovery request');
 if(typeof guardianId!=='string'||!guardianId)throw Error('Guardian ID required');
 return {guardianId,signature:await sign(guardianPrivateKey,payload)};
}
export async function successorProof(payload,newPrivateKey){return sign(newPrivateKey,payload)}
async function auditRecovery(record,pin){
 if(!record.recovery)return {status:'not_requested',acceptedRoots:0,acceptedGuardians:0};
 const {payload,votes,successorSignature}=record.recovery;
 if(!payload||payload.schema!==RECOVERY_SCHEMA||payload.recoverySequence!==1||
 payload.priorChainDigest!==record.historyDigest||
 payload.reason!=='lost_or_compromised_key'||payload.minimumGuardianRoots!==3||
 payload.successorFingerprint!==await fingerprint(payload.successorKey))throw Error('Recovery payload lineage mismatch');
 const before=await verifyChain(record.history,pin.chainPin);
 if(payload.retiredKeyFingerprint!==await fingerprint(before.keys[before.activeEpoch])||
 payload.successorFingerprint===payload.retiredKeyFingerprint)throw Error('Retired key mismatch');
 await check(payload.successorKey,payload,successorSignature);
 if(!Array.isArray(votes)||votes.length<3||votes.length>pin.guardians.length)throw Error('Insufficient pinned guardian signatures');
 const ids=new Set(),roots=new Set();
 for(const vote of votes){
  const guardian=pin.guardians.find(g=>g.id===vote.guardianId);
  if(!guardian||ids.has(vote.guardianId))throw Error('Unpinned or repeated guardian');
  ids.add(vote.guardianId);
  await check(guardian.publicJwk,payload,vote.signature);
  roots.add(guardian.ancestryRoot);
 }
 if(roots.size<3)throw Error('Insufficient independent guardian ancestry');
 return {status:'recovered',acceptedRoots:roots.size,acceptedGuardians:ids.size,
  successorFingerprint:payload.successorFingerprint};
}
export async function verify(record,pin){
 await verifyPolicy(pin);
 if(!record||record.version!==VERSION||!Array.isArray(record.newManifests))throw Error('Malformed recovery record');
 const prior=await verifyChain(record.history,pin.chainPin);
 if(record.historicalActiveEpoch!==prior.activeEpoch||record.historyDigest!==await baseProof(record.history,pin.chainPin))throw Error('Historical chain changed');
 if(pin.minRecoverySequence> (record.recovery?1:0))throw Error('Recovery rollback below independently pinned floor');
 const recovery=await auditRecovery(record,pin);
 if(record.newManifests.length&&recovery.status!=='recovered')throw Error('Manifest requires recovered key');
 let revision=record.history.manifests.at(-1)?.envelope.payload.revision??(pin.chainPin.minManifestRevision-1);
 for(const m of record.newManifests){
  if(!Number.isSafeInteger(m.revision)||m.revision<=revision||
  m.revision!==m.envelope?.payload?.revision)throw Error('Nonmonotonic recovered manifest revision');
  await verifyManifest(m.envelope,{publicJwk:record.recovery.payload.successorKey,
   minRevision:Math.max(pin.minRecoveredRevision,revision+1)});
  revision=m.revision;
 }
 return {valid:true,...recovery,priorManifests:record.history.manifests.length,
  recoveredManifests:record.newManifests.length,historyDigest:record.historyDigest,
  originalAuthorityRetained:true};
}
export async function recover(record,payload,votes,successorSignature,pin){
 await verify(record,pin);
 if(record.recovery)throw Error('Recovery already sealed');
 const next={...copy(record),recovery:{payload:copy(payload),votes:copy(votes),successorSignature}};
 await verify(next,pin);
 return next;
}
export async function appendManifest(record,envelope,pin){
 const result=await verify(record,pin);
 if(result.status!=='recovered')throw Error('Recovery approval required');
 const last=record.newManifests.at(-1)?.revision??
 (record.history.manifests.at(-1)?.envelope.payload.revision??0);
 if(envelope?.payload?.revision<=last)throw Error('Recovered manifest revision must increase');
 await verifyManifest(envelope,{publicJwk:record.recovery.payload.successorKey,
  minRevision:Math.max(pin.minRecoveredRevision,last+1)});
 const next={...copy(record),newManifests:[...copy(record.newManifests),
  {revision:envelope.payload.revision,envelope:copy(envelope)}]};
 await verify(next,pin);return next;
}
export async function fixture(kind='valid'){
 const old=await generateFixtureSigner(),successor=await generateFixtureSigner();
 const guardians=await Promise.all(Array.from({length:4},()=>generateFixtureSigner()));
 const chainPin={publicJwk:copy(old.publicJwk),minSequence:0,minManifestRevision:1};
 const {start:begin,appendManifest:historicalManifest}=await import('./trust-anchor-rotation.mjs');
 let history=await begin(old.publicJwk);
 history=await historicalManifest(history,await signManifest([],1,old.privateKey),chainPin);
 const pin={chainPin,guardians:guardians.map((g,i)=>({id:'guardian-'+i,
  ancestryRoot:kind==='shared-root'&&i===3?'guardian-root-1':'guardian-root-'+i,
  publicJwk:copy(g.publicJwk)})),minRecoverySequence:0,minRecoveredRevision:2};
 let record=await start(history,pin);
 const payload=await request(record,successor.publicJwk,pin);
 const selected=kind==='shared-root'?[0,1,3]:[0,1,2];
 const votes=[];
 for(const i of selected)votes.push(await witness(payload,'guardian-'+i,
  kind==='forged-vote'&&i===2?old.privateKey:guardians[i].privateKey));
 if(kind==='duplicate-vote')votes[2]=copy(votes[1]);
 const pop=await successorProof(payload,kind==='bad-successor'?old.privateKey:successor.privateKey);
 return {record,pin,payload,votes,pop,old,successor,guardians};
}
