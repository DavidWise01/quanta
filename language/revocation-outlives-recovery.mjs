// QG-067: revocation outlives recovery, valid historical signature != current authorization.
// Ed25519 test model, no live credentials or durable external monotonic store.
import {verify as verifyRecovery,fixture as recoveryFixture,recover} from './recovery-without-old-key.mjs';
import {verifyChain,canonical} from './trust-anchor-rotation.mjs';
import {verifyManifest,signManifest} from './signed-trust-anchor.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-067',SCHEMA='QUANTA-QG-067-REVOCATION';
const clone=x=>JSON.parse(JSON.stringify(x)),equal=(a,b)=>canonical(a)===canonical(b);
const bytes=x=>new TextEncoder().encode(canonical(x));
const encode=x=>btoa(Array.from(new Uint8Array(x),v=>String.fromCharCode(v)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
function decode(s){if(typeof s!=='string'||!/^[a-zA-Z0-9_-]+$/.test(s))throw Error('Malformed signature');return Uint8Array.from(atob(s.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-s.length%4)%4)),x=>x.charCodeAt(0))}
async function key(jwk){
 if(jwk?.kty!=='OKP'||jwk?.crv!=='Ed25519')throw Error('Expected Ed25519 key');
 try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}
 catch{throw Error('Unusable Ed25519 key')}
}
async function sign(priv,payload){
 if(priv?.algorithm?.name!=='Ed25519'||!priv.usages.includes('sign'))throw Error('Ed25519 signer required');
 return encode(await crypto.subtle.sign('Ed25519',priv,bytes(payload)));
}
async function check(pub,payload,sig){
 let ok=false;
 try{ok=await crypto.subtle.verify('Ed25519',await key(pub),decode(sig),bytes(payload))}
 catch{throw Error('Signature parsing failed')}
 if(!ok)throw Error('Signature verification failed');
}
async function fp(pub){return sha256(canonical(pub))}
function floor(pin){
 if(!pin||!pin.recoveryPin||!Number.isSafeInteger(pin.minRevocationSequence)||
 pin.minRevocationSequence<0)throw Error('Independent revocation floor required');
}
export async function start(recovered,pin){
 floor(pin);
 const state=await verifyRecovery(recovered,pin.recoveryPin);
 if(state.status!=='recovered')throw Error('Completed QG-066 recovery required');
 return {version:VERSION,recovered:clone(recovered),revocations:[],operations:[]};
}
async function expected(record,pin){
 floor(pin);
 if(!record||record.version!==VERSION||!Array.isArray(record.revocations)||!Array.isArray(record.operations))throw Error('Malformed revocation ledger');
 const recovery=await verifyRecovery(record.recovered,pin.recoveryPin);
 if(recovery.status!=='recovered')throw Error('Completed recovery required');
 const p=record.recovered.recovery.payload;
 const historical=await verifyChain(record.recovered.history,pin.recoveryPin.chainPin);
 const retired=historical.keys[historical.activeEpoch];
 const retiredFingerprint=await fp(retired);
 const successorFingerprint=await fp(p.successorKey);
 const recoveryDigest=await sha256(canonical(record.recovered.recovery));
 if(record.revocations.length>1)throw Error('Only one revocation in this finite recovery epoch');
 let revocation=null;
 if(record.revocations.length){
  revocation=record.revocations[0];
  const payload=revocation.payload;
  if(!payload||payload.schema!==SCHEMA||payload.sequence!==1||
  payload.recoveryDigest!==recoveryDigest||
  payload.historyDigest!==record.recovered.historyDigest||
  payload.retiredFingerprint!==retiredFingerprint||
  payload.successorFingerprint!==successorFingerprint||
  payload.disposition!=='deny_new_operations_preserve_history')throw Error('Revocation lineage mismatch');
  await check(p.successorKey,payload,revocation.successorSignature);
 }
 if(record.revocations.length<pin.minRevocationSequence)throw Error('Revocation rollback below independent floor');
 const used=new Set();
 for(let i=0;i<record.operations.length;i++){
  const op=record.operations[i];
  if(!op||!Number.isSafeInteger(op.sequence)||op.sequence!==i+1||
   typeof op.action!=='string'||!op.action||op.action.length>120||
   used.has(op.id)||typeof op.id!=='string'||!op.id)throw Error('Invalid operation sequence');
  used.add(op.id);
  if(!revocation)throw Error('New operations require revocation gate');
  if(op.keyFingerprint!==successorFingerprint)throw Error('Revoked or unknown key cannot perform new operations');
  const payload={schema:'QUANTA-QG-067-OPERATION',id:op.id,sequence:op.sequence,
   action:op.action,keyFingerprint:successorFingerprint,revocationDigest:await sha256(canonical(revocation))};
  if(!equal(op.payload,payload))throw Error('Operation replay mismatch');
  await check(p.successorKey,payload,op.signature);
 }
 return {valid:true,revoked:!!revocation,retiredFingerprint,successorFingerprint,
  historicalManifests:record.recovered.history.manifests.length,
  recoveredManifests:record.recovered.newManifests.length,
  operations:record.operations.length,revocationSequence:record.revocations.length,
  historyStillVerified:true};
}
export async function verify(record,pin){return expected(record,pin)}
export async function makeRevocation(record,successorPrivate,pin){
 const state=await verify(record,pin);
 if(state.revoked)throw Error('Already revoked');
 const payload={schema:SCHEMA,sequence:1,recoveryDigest:await sha256(canonical(record.recovered.recovery)),
  historyDigest:record.recovered.historyDigest,retiredFingerprint:state.retiredFingerprint,
  successorFingerprint:state.successorFingerprint,disposition:'deny_new_operations_preserve_history'};
 return {payload,successorSignature:await sign(successorPrivate,payload)};
}
export async function appendRevocation(record,certificate,pin){
 await verify(record,pin);
 if(record.revocations.length)throw Error('Revocation already recorded');
 const next={...clone(record),revocations:[...clone(record.revocations),clone(certificate)]};
 await verify(next,{...pin,minRevocationSequence:Math.min(1,pin.minRevocationSequence)});
 return next;
}
export async function signOperation(record,id,action,privateKey,pin){
 const state=await verify(record,pin);
 if(!state.revoked)throw Error('Revocation first');
 const payload={schema:'QUANTA-QG-067-OPERATION',id,sequence:record.operations.length+1,
  action,keyFingerprint:state.successorFingerprint,
  revocationDigest:await sha256(canonical(record.revocations[0]))};
 return {id,action,sequence:payload.sequence,keyFingerprint:state.successorFingerprint,
  payload,signature:await sign(privateKey,payload)};
}
export async function appendOperation(record,operation,pin){
 await verify(record,pin);
 const next={...clone(record),operations:[...clone(record.operations),clone(operation)]};
 await verify(next,pin);
 return next;
}
export async function historicalProof(record,pin){
 const state=await verify(record,pin);
 return {valid:true,oldSignaturesStillValid:state.historyStillVerified,oldKeyCanAuthorizeNew:false,
  historicalManifestCount:state.historicalManifests};
}
export async function fixture(kind='valid'){
 const f=await recoveryFixture();
 const recovered=await recover(f.record,f.payload,f.votes,f.pop,f.pin);
 const pin={recoveryPin:f.pin,minRevocationSequence:0};
 let record=await start(recovered,pin);
 let certificate=await makeRevocation(record,kind==='forged-revocation'?f.old.privateKey:f.successor.privateKey,pin);
 if(kind==='tampered-certificate')certificate.payload.retiredFingerprint='forged';
 if(kind==='no-revocation')return {...f,record,pin,certificate};
 record=await appendRevocation(record,certificate,pin);
 if(kind==='valid'){
  const operation=await signOperation(record,'op-1','review-evidence',f.successor.privateKey,pin);
  record=await appendOperation(record,operation,pin);
 }
 return {...f,record,pin,certificate};
}
