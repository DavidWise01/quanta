// QG-064 — Trust Anchor: signature-gated provenance manifests.
// Public-key trust MUST arrive as an independent parameter, not from the packet.
// This model uses synthetic ephemeral Ed25519 keys, not real publisher identity.
import {start as admissionStart,append as admissionAppend,verify as admissionVerify,sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-064', ALGORITHM='Ed25519';
const copy=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function canonical(value){
 if(value===null||typeof value!=='object')return JSON.stringify(value);
 if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';
 const keys=Object.keys(value).sort();
 if(keys.some(k=>value[k]===undefined))throw Error('Undefined signed field');
 return '{'+keys.map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';
}
function b64encode(bytes){return btoa(Array.from(bytes,x=>String.fromCharCode(x)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'')}
function b64decode(str){
 if(typeof str!=='string'||!/^[A-Za-z0-9_-]+$/.test(str))throw Error('Malformed signature');
 const raw=atob(str.replace(/-/g,'+').replace(/_/g,'/')+'='.repeat((4-str.length%4)%4));
 return Uint8Array.from(raw,c=>c.charCodeAt(0));
}
export async function generateFixtureSigner(){
 const keys=await crypto.subtle.generateKey({name:ALGORITHM},true,['sign','verify']);
 return {privateKey:keys.privateKey,publicJwk:await crypto.subtle.exportKey('jwk',keys.publicKey)};
}
export async function signManifest(registry,revision,privateKey){
 if(!Number.isSafeInteger(revision)||revision<1)throw Error('Revision must be positive');
 if(!privateKey||privateKey.algorithm?.name!==ALGORITHM||!privateKey.usages.includes('sign'))throw Error('Ed25519 signer required');
 await admissionStart(registry); // validate registry before signing
 const payload={schema:'QUANTA-QG-064-MANIFEST',revision,registry:copy(registry)};
 const digest=await sha256(canonical(payload));
 const signature=new Uint8Array(await crypto.subtle.sign(ALGORITHM,privateKey,new TextEncoder().encode(canonical(payload))));
 return {payload,digest,algorithm:ALGORITHM,signature:b64encode(signature)};
}
export async function verifyManifest(envelope,anchor){
 if(!anchor||!anchor.publicJwk||!Number.isSafeInteger(anchor.minRevision)||anchor.minRevision<1)throw Error('Independent trust anchor required');
 if(!envelope||envelope.algorithm!==ALGORITHM||!envelope.payload||
 envelope.payload.schema!=='QUANTA-QG-064-MANIFEST'||
 !Number.isSafeInteger(envelope.payload.revision)||envelope.payload.revision<anchor.minRevision)
 throw Error('Manifest missing, invalid or rolled back');
 await admissionStart(envelope.payload.registry); // rejects malformed pinned registry
 const material=canonical(envelope.payload);
 if(envelope.digest!==await sha256(material))throw Error('Manifest digest mismatch');
 let key;
 try{key=await crypto.subtle.importKey('jwk',anchor.publicJwk,{name:ALGORITHM},false,['verify'])}
 catch{throw Error('Untrusted public-key format')}
 let good=false;
 try{good=await crypto.subtle.verify(ALGORITHM,key,b64decode(envelope.signature),new TextEncoder().encode(material))}
 catch{throw Error('Invalid manifest signature encoding')}
 if(!good)throw Error('Manifest signature verification failed');
 return {valid:true,revision:envelope.payload.revision,digest:envelope.digest,
  anchorFingerprint:await sha256(canonical(anchor.publicJwk)),sources:envelope.payload.registry.length};
}
export async function start(envelope,anchor){
 const signature=await verifyManifest(envelope,anchor);
 const admission=await admissionStart(envelope.payload.registry);
 return {version:VERSION,envelope:copy(envelope),admission,signature};
}
export async function verify(record,anchor){
 if(!record||record.version!==VERSION||!record.envelope||!record.admission)throw Error('Invalid trust-gate ledger');
 const signature=await verifyManifest(record.envelope,anchor);
 await admissionVerify(record.admission);
 if(!equal(record.admission.registry,record.envelope.payload.registry)||!equal(record.signature,signature))
 throw Error('Manifest/admission replay mismatch');
 return {valid:true,signature,accepted:record.admission.accepted,quarantined:record.admission.quarantined,
  roots:record.admission.ancestry.count,decision:record.admission.decision};
}
export async function append(record,packet,anchor){
 await verify(record,anchor); // verify anchor BEFORE any packet may enter the gate
 const admission=await admissionAppend(record.admission,packet);
 const next={...copy(record),admission};
 await verify(next,anchor);
 return next;
}
export async function syntheticFixture(mode='valid'){
 const signer=await generateFixtureSigner();
 const entry=async(surface,source,body,ancestors,policy)=>({
  surface,source,ancestors,digest:await sha256(body),...(policy?{policy}: {})
 });
 const registry=[
  await entry('github','DavidWise01','repo record',['owned-lineage']),
  await entry('0root.ai','0root.ai','public mirror',['owned-lineage']),
  await entry('public-internet','site-a','independent A',['root-a'],{robots:'allow',llms:'listed'}),
  await entry('public-internet','site-b','independent B',['root-b'],{robots:'allow',llms:'unlisted'})
 ];
 const envelope=await signManifest(registry,2,signer.privateKey);
 const anchor={publicJwk:signer.publicJwk,minRevision:2};
 const data=[['github','DavidWise01','repo record'],['0root.ai','0root.ai','public mirror'],
  ['public-internet','site-a','independent A'],['public-internet','site-b','independent B']]
  .map(([surface,source,body],i)=>({id:'packet-'+i,surface,source,body,outcome:0,epoch:'post-withdrawal'}));
 if(mode==='tampered-content')data[2].body='modified A';
 if(mode==='tampered-manifest')envelope.payload.registry[2].ancestors=['fabricated'];
 if(mode==='rollback')anchor.minRevision=3;
 if(mode==='blocked')registry[2].policy.robots='disallow'; // registry after signing can't alter envelope
 return {envelope,anchor,data,signer};
}
