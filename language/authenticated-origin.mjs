/**
 * QG-038.1 — Authenticated Origin (experimental).
 * ECDSA P-256 / SHA-256; keys are externally held, not trusted because embedded.
 * Signature binds the entire QG-036 packet AND the separate QG-037 manifest.
 * Canonical JSON is deterministic over JSON-only records, not an RFC 8785 implementation.
 */
import {verifyIndependentClosure} from "./independent-closure.mjs";
export const VERSION="QG-038.1",CARRIER="||||";
const encoder=new TextEncoder();
const hex=b=>Array.from(new Uint8Array(b),x=>x.toString(16).padStart(2,"0")).join("");
function unhex(h){if(typeof h!=="string"||!/^(?:[0-9a-f]{2})+$/.test(h))throw Error("Malformed hex");return Uint8Array.from(h.match(/../g),h=>parseInt(h,16))}
function canonical(x,depth=0){
 if(depth>30)throw Error("Canonical data nesting bound");
 if(x===null||typeof x==="string"||typeof x==="boolean")return x;
 if(typeof x==="number"&&Number.isFinite(x))return x;
 if(Array.isArray(x))return x.map(v=>canonical(v,depth+1));
 if(x&&Object.getPrototypeOf(x)===Object.prototype){
  const out={};for(const key of Object.keys(x).sort())out[key]=canonical(x[key],depth+1);return out;
 }
 throw Error("Non-JSON payload");
}
const json=x=>JSON.stringify(canonical(x));
async function digest(x){return hex(await crypto.subtle.digest("SHA-256",encoder.encode(json(x))))}
function alg(){return {name:"ECDSA",hash:"SHA-256"}}
function message(packetHash,manifestHash){return encoder.encode("QUANTA|QG-038.1|SHA256|P256|"+packetHash+"|"+manifestHash)}
function validate(packet,manifest){
 const report=verifyIndependentClosure(packet,manifest);
 if(!report.pass)throw Error("Independent closure refused: "+report.error);
}
export async function generateDemoSigningKeys(){
 return crypto.subtle.generateKey({name:"ECDSA",namedCurve:"P-256"},true,["sign","verify"]);
}
export async function attestOrigin(packet,manifest,privateKey,signer){
 validate(packet,manifest);
 if(!privateKey||privateKey.type!=="private"||privateKey.algorithm?.name!=="ECDSA"||privateKey.algorithm.namedCurve!=="P-256"||!privateKey.usages.includes("sign"))throw Error("P-256 private signing key required");
 if(typeof signer!=="string"||! /^[a-z][a-z0-9-]{0,63}$/.test(signer))throw Error("Invalid signer label");
 const packetSha256=await digest(packet),manifestSha256=await digest(manifest);
 const signature=hex(await crypto.subtle.sign(alg(),privateKey,message(packetSha256,manifestSha256)));
 return {version:VERSION,carrier:CARRIER,algorithm:"ECDSA-P256-SHA256",signer,
  packetSha256,manifestSha256,signature,interpretationProven:false};
}
export async function verifyAuthenticatedOrigin(packet,manifest,attestation,trustedPublicKey){
 try{
  validate(packet,manifest);
  if(!attestation||Object.keys(attestation).sort().join("|")!==
   ["algorithm","carrier","interpretationProven","manifestSha256","packetSha256","signature","signer","version"].sort().join("|")||
   attestation.version!==VERSION||attestation.carrier!==CARRIER||attestation.algorithm!=="ECDSA-P256-SHA256"||
   attestation.interpretationProven!==false||typeof attestation.signer!=="string"||
   !/^[a-z][a-z0-9-]{0,63}$/.test(attestation.signer))throw Error("Invalid attestation");
  if(!trustedPublicKey||trustedPublicKey.type!=="public"||trustedPublicKey.algorithm?.name!=="ECDSA"||
   trustedPublicKey.algorithm.namedCurve!=="P-256"||!trustedPublicKey.usages.includes("verify"))throw Error("Externally trusted public key required");
  const p=await digest(packet),m=await digest(manifest);
  if(p!==attestation.packetSha256||m!==attestation.manifestSha256)throw Error("Signed payload digest mismatch");
  const ok=await crypto.subtle.verify(alg(),trustedPublicKey,unhex(attestation.signature),message(p,m));
  if(!ok)throw Error("Signature verification failed");
  return {pass:true,authenticatedToTrustedKey:true,signerLabel:attestation.signer,
   independentClosure:true,interpretationProven:false,algorithm:attestation.algorithm};
 }catch(e){return {pass:false,error:e.message}}
}
