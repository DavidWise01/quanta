// QG-065 Trust Anchor Rotation — dual-signed, append-only-by-value key transitions.
// Uses a separately pinned genesis public key AND minimum accepted sequence.
// Synthetic Ed25519 keys; no real publisher identity is established.
import {generateFixtureSigner,signManifest,verifyManifest} from './signed-trust-anchor.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-065';
const clone=v=>JSON.parse(JSON.stringify(v));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function canonical(value) {
 if(value===null||typeof value!=='object')return JSON.stringify(value);
 if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';
 const keys=Object.keys(value).sort();
 if(keys.some(k=>value[k]===undefined))throw Error('Undefined canonical member');
 return '{'+keys.map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';
}
const bytes=v=>new TextEncoder().encode(canonical(v));
function encode(buf){return btoa(Array.from(new Uint8Array(buf),c=>String.fromCharCode(c)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'')}
function decode(s){
 if(typeof s!=='string'||!/^[A-Za-z0-9_-]+$/.test(s))throw Error('Invalid signature encoding');
 return Uint8Array.from(atob(s.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-s.length%4)%4)),c=>c.charCodeAt(0));
}
async function keyFingerprint(jwk){return sha256(canonical(jwk))}
async function checkedKey(jwk){
 if(!jwk||jwk.kty!=='OKP'||jwk.crv!=='Ed25519')throw Error('Invalid Ed25519 public key');
 try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}
 catch{throw Error('Unusable Ed25519 public key')}
}
async function sign(privateKey,payload){
 if(!privateKey||privateKey.algorithm?.name!=='Ed25519'||!privateKey.usages.includes('sign'))throw Error('Signing key required');
 return encode(await crypto.subtle.sign('Ed25519',privateKey,bytes(payload)));
}
async function verifySignature(jwk,payload,signature){
 const key=await checkedKey(jwk);
 let valid=false;
 try{valid=await crypto.subtle.verify('Ed25519',key,decode(signature),bytes(payload))}
 catch{throw Error('Signature verification error')}
 if(!valid)throw Error('Signature verification failed');
}
export function validatePin(pin){
 if(!pin||!pin.publicJwk||!Number.isSafeInteger(pin.minSequence)||pin.minSequence<0||
 !Number.isSafeInteger(pin.minManifestRevision)||pin.minManifestRevision<1)throw Error('External genesis pin and revision floor required');
}
export async function start(genesisKey){
 await checkedKey(genesisKey);
 return {version:VERSION,genesisKey:clone(genesisKey),transitions:[],manifests:[]};
}
export async function makeTransition(record,oldPrivateKey,newPrivateKey,newPublicJwk){
 if(!record||record.version!==VERSION)throw Error('Invalid rotation ledger');
 const sequence=record.transitions.length+1;
 const current=sequence===1?record.genesisKey:record.transitions.at(-1).payload.toKey;
 const previousHash=sequence===1?'GENESIS':await sha256(canonical(record.transitions.at(-1)));
 const payload={schema:'QUANTA-QG-065-ROTATION',sequence,fromFingerprint:await keyFingerprint(current),
  toKey:clone(newPublicJwk),toFingerprint:await keyFingerprint(newPublicJwk),previousHash};
 await checkedKey(newPublicJwk);
 if(payload.fromFingerprint===payload.toFingerprint)throw Error('Rotation must change the key');
 return {payload,oldSignature:await sign(oldPrivateKey,payload),newSignature:await sign(newPrivateKey,payload)};
}
export async function verifyChain(record,pin){
 validatePin(pin);
 if(!record||record.version!==VERSION||!Array.isArray(record.transitions)||!Array.isArray(record.manifests))throw Error('Invalid rotation ledger');
 if(!equal(record.genesisKey,pin.publicJwk))throw Error('Genesis key disagrees with independent pin');
 let current=clone(pin.publicJwk),previousHash='GENESIS';
 const keys=[clone(current)];
 for(let i=0;i<record.transitions.length;i++){
  const transition=record.transitions[i],p=transition?.payload;
  if(!p||p.schema!=='QUANTA-QG-065-ROTATION'||p.sequence!==i+1||
   p.previousHash!==previousHash||p.fromFingerprint!==await keyFingerprint(current)||
   p.toFingerprint!==await keyFingerprint(p.toKey)||p.fromFingerprint===p.toFingerprint)throw Error('Rotation sequence or linkage mismatch');
  await verifySignature(current,p,transition.oldSignature);
  await verifySignature(p.toKey,p,transition.newSignature);
  previousHash=await sha256(canonical(transition));
  current=clone(p.toKey);keys.push(current);
 }
 if(record.transitions.length<pin.minSequence)throw Error('Rotation state rolled back below independent floor');
 let lastRevision=pin.minManifestRevision-1;
 for(const m of record.manifests){
  if(!Number.isSafeInteger(m.keyEpoch)||m.keyEpoch<0||m.keyEpoch>=keys.length||
  m.keyEpoch>record.transitions.length||!Number.isSafeInteger(m.envelope?.payload?.revision)||
  m.envelope.payload.revision<=lastRevision)throw Error('Manifest revision or historical epoch mismatch');
  // Historical manifest must be signed by the key active at that epoch.
  // Once rotated, the prior epoch may not issue a higher revision.
  const idx=record.manifests.indexOf(m);
  if(idx>0&&m.keyEpoch<record.manifests[idx-1].keyEpoch)throw Error('Manifest key epoch regressed');
  await verifyManifest(m.envelope,{publicJwk:keys[m.keyEpoch],minRevision:pin.minManifestRevision});
  lastRevision=m.envelope.payload.revision;
 }
 return {valid:true,activeEpoch:record.transitions.length,activeFingerprint:await keyFingerprint(current),
  transitions:record.transitions.length,historicalManifests:record.manifests.length,
  retainedKeys:keys.length,keys};
}
export async function appendRotation(record,transition,pin){
 const before=await verifyChain(record,pin);
 if(!transition||transition.payload?.sequence!==before.activeEpoch+1)throw Error('Unexpected rotation step');
 const next={...clone(record),transitions:[...clone(record.transitions),clone(transition)]};
 await verifyChain(next,{...pin,minSequence:Math.min(pin.minSequence,next.transitions.length)});
 return next;
}
export async function appendManifest(record,envelope,pin){
 const chain=await verifyChain(record,pin),revision=envelope?.payload?.revision;
 const last=record.manifests.at(-1)?.envelope.payload.revision??(pin.minManifestRevision-1);
 if(!Number.isSafeInteger(revision)||revision<=last)throw Error('Manifest revision must increase');
 await verifyManifest(envelope,{publicJwk:chain.keys[chain.activeEpoch],minRevision:Math.max(pin.minManifestRevision,last+1)});
 const next={...clone(record),manifests:[...clone(record.manifests),{keyEpoch:chain.activeEpoch,envelope:clone(envelope)}]};
 await verifyChain(next,pin);
 return next;
}
export async function fixture(mode='valid'){
 const a=await generateFixtureSigner(),b=await generateFixtureSigner();
 const pin={publicJwk:clone(a.publicJwk),minSequence:0,minManifestRevision:1};
 let record=await start(a.publicJwk);
 record=await appendManifest(record,await signManifest([],1,a.privateKey),pin);
 const transition=await makeTransition(record,a.privateKey,b.privateKey,b.publicJwk);
 if(mode==='bad-old')transition.oldSignature=transition.newSignature;
 if(mode==='bad-new')transition.newSignature=transition.oldSignature;
 if(mode==='wrong-link')transition.payload.previousHash='forged';
 record=await appendRotation(record,transition,pin);
 record=await appendManifest(record,await signManifest([],2,b.privateKey),pin);
 return {record,pin,old:a,newSigner:b};
}
