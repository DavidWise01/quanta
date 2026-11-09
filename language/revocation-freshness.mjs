/**
 * QUANTA QG-040.1 — Fresh Revocation Checkpoint.
 * A root-signed status declaration binds an exact revocation collection,
 * a bounded freshness interval and a monotonic sequence floor.
 * Complete/fresh means asserted by the signer, NOT independently observed.
 */
import {verifyTrustedKeyLineage} from "./trusted-key-lineage.mjs";
export const VERSION="QG-040.1",CARRIER="||||";
const te=new TextEncoder();
const encode=v=>te.encode(JSON.stringify(v));
const hex=b=>Array.from(new Uint8Array(b),n=>n.toString(16).padStart(2,"0")).join("");
const fromHex=s=>{if(typeof s!=="string"||!/^(?:[0-9a-f]{2})+$/.test(s))throw Error("Invalid signature hex");return Uint8Array.from(s.match(/../g),s=>parseInt(s,16))};
const int=x=>Number.isSafeInteger(x)&&x>=0;
const id=x=>typeof x==="string"&&/^[a-z][a-z0-9-]{0,63}$/.test(x);
const keys=(o,arr)=>!!o&&typeof o==="object"&&!Array.isArray(o)&&JSON.stringify(Object.keys(o).sort())===JSON.stringify([...arr].sort());
const algorithm={name:"ECDSA",hash:"SHA-256"};
const clone=x=>JSON.parse(JSON.stringify(x));
function canonicalRevocations(revocations){
 if(!Array.isArray(revocations)||revocations.length>64)throw Error("Revocation list bound");
 const list=revocations.map(r=>{
  if(!keys(r,["subject","rootId","sequence","reason","signature"])||!id(r.subject)||!id(r.rootId)||!int(r.sequence)||typeof r.reason!=="string"||!r.reason.trim()||r.reason.length>240||typeof r.signature!=="string")throw Error("Invalid signed revocation");
  return {subject:r.subject,rootId:r.rootId,sequence:r.sequence,reason:r.reason,signature:r.signature};
 }).sort((a,b)=>a.subject.localeCompare(b.subject)||a.sequence-b.sequence||a.signature.localeCompare(b.signature));
 if(new Set(list.map(x=>x.subject+":"+x.sequence)).size!==list.length)throw Error("Duplicate revocation event");
 return list;
}
async function hashRevocations(revocations){return hex(await crypto.subtle.digest("SHA-256",encode(canonicalRevocations(revocations))))}
function body(v){return {version:VERSION,rootId:v.rootId,sequence:v.sequence,issuedAt:v.issuedAt,expiresAt:v.expiresAt,
 revocationsSha256:v.revocationsSha256,complete:v.complete}}
function validCheckpoint(v){
 if(!v||!keys(v,["version","rootId","sequence","issuedAt","expiresAt","revocationsSha256","complete","signature"])||
 v.version!==VERSION||!id(v.rootId)||!int(v.sequence)||!int(v.issuedAt)||!int(v.expiresAt)||
 v.expiresAt<=v.issuedAt||v.complete!==true||
 typeof v.revocationsSha256!=="string"||!/^[0-9a-f]{64}$/.test(v.revocationsSha256))throw Error("Invalid signed checkpoint");
}
const signedMessage=b=>encode(["QUANTA",VERSION,"revocation-checkpoint",b]);
export async function signFreshnessCheckpoint({rootId,sequence,issuedAt,expiresAt,revocations,rootPrivateKey}){
 const checkpoint={version:VERSION,rootId,sequence,issuedAt,expiresAt,
  revocationsSha256:await hashRevocations(revocations),complete:true};
 if(!id(rootId)||!int(sequence)||!int(issuedAt)||!int(expiresAt)||expiresAt<=issuedAt||!rootPrivateKey||
 rootPrivateKey.type!=="private"||rootPrivateKey.algorithm?.name!=="ECDSA"||
 rootPrivateKey.algorithm.namedCurve!=="P-256")throw Error("Invalid checkpoint signing authority");
 return {...checkpoint,signature:hex(await crypto.subtle.sign(algorithm,rootPrivateKey,signedMessage(checkpoint)))};
}
export async function verifyFreshAuthority({packet,manifest,attestation,rootId,rootPublicKey,certificates,revocations,
 checkpoint,asOf,minSequence,maxCheckpointAge}){
 try{
  if(!int(asOf)||!int(minSequence)||!int(maxCheckpointAge)||maxCheckpointAge===0)throw Error("External freshness policy required");
  validCheckpoint(checkpoint);
  if(checkpoint.rootId!==rootId)throw Error("Checkpoint signed for different authority");
  if(checkpoint.sequence<minSequence)throw Error("Checkpoint sequence rollback");
  if(asOf<checkpoint.issuedAt||asOf>=checkpoint.expiresAt)throw Error("Checkpoint expired or not yet issued");
  if(asOf-checkpoint.issuedAt>maxCheckpointAge)throw Error("Checkpoint exceeds maximum age");
  if(!Array.isArray(revocations))throw Error("Complete revocation set required");
  const actual=await hashRevocations(revocations);
  if(actual!==checkpoint.revocationsSha256)throw Error("Revocations missing or substituted");
  if(!rootPublicKey||rootPublicKey.type!=="public"||rootPublicKey.algorithm?.name!=="ECDSA"||
  rootPublicKey.algorithm.namedCurve!=="P-256")throw Error("Pinned P-256 trust root required");
  if(!await crypto.subtle.verify(algorithm,rootPublicKey,fromHex(checkpoint.signature),signedMessage(body(checkpoint))))throw Error("Checkpoint signature invalid");
  // Use the caller's independently obtained asOf and root. A signed checkpoint's
  // completeness bit only asserts what the root claims to have listed.
  const lineage=await verifyTrustedKeyLineage({packet,manifest,attestation,rootId,rootPublicKey,certificates,revocations,asOf});
  if(!lineage.pass)throw Error("Key lineage refused: "+lineage.error);
  return {pass:true,rootId,sequence:checkpoint.sequence,issuedAt:checkpoint.issuedAt,
    expiresAt:checkpoint.expiresAt,revocationsBound:revocations.length,
    lineageValid:true,checkpointSignatureValid:true,interpretationProven:false};
 }catch(e){return {pass:false,error:e.message}}
}
