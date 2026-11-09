/** QG-039.1 — bounded P-256 key ancestry, externally pinned trust root. Experimental. */
import {verifyAuthenticatedOrigin} from "./authenticated-origin.mjs";
export const VERSION="QG-039.1";
const enc=new TextEncoder(),ab=x=>enc.encode(JSON.stringify(x));
const cleanId=x=>typeof x==="string"&&/^[a-z][a-z0-9-]{0,63}$/.test(x);
const hex=a=>Array.from(new Uint8Array(a),x=>x.toString(16).padStart(2,"0")).join("");
const unhex=s=>{if(typeof s!=="string"||!/^([0-9a-f]{2})+$/.test(s))throw Error("Invalid signature encoding");return Uint8Array.from(s.match(/../g),x=>parseInt(x,16))};
const alg={name:"ECDSA",hash:"SHA-256"};
async function publicJwk(key){if(key?.type!=="public"||key.algorithm?.name!=="ECDSA"||key.algorithm?.namedCurve!=="P-256")throw Error("P-256 public key required");const k=await crypto.subtle.exportKey("jwk",key);return {kty:"EC",crv:"P-256",x:k.x,y:k.y}}
async function importJwk(j){if(!j||Object.keys(j).sort().join(",")!=="crv,kty,x,y"||j.kty!=="EC"||j.crv!=="P-256")throw Error("Noncanonical public key");return crypto.subtle.importKey("jwk",j,{name:"ECDSA",namedCurve:"P-256"},true,["verify"])}
async function keyId(j){return hex(await crypto.subtle.digest("SHA-256",ab(j)))}
const message=(kind,record)=>ab(["QUANTA",VERSION,kind,record]);
async function signed(privateKey,kind,record){if(privateKey?.type!=="private"||privateKey.algorithm?.namedCurve!=="P-256")throw Error("Private signing key needed");return hex(await crypto.subtle.sign(alg,privateKey,message(kind,record)))}
async function checked(publicKey,kind,record,sig){return crypto.subtle.verify(alg,publicKey,unhex(sig),message(kind,record))}
function validTime(n){return Number.isSafeInteger(n)&&n>=0}
function validRecord(c){
 if(!c||!cleanId(c.subject)||!cleanId(c.issuer)||!validTime(c.notBefore)||!validTime(c.notAfter)||c.notAfter<=c.notBefore||!Array.isArray(c.roles)||!c.roles.length||new Set(c.roles).size!==c.roles.length||c.roles.some(x=>!["delegate","origin-attest"].includes(x)))throw Error("Invalid certificate");
}
export async function issueKeyCertificate({subject,issuer,publicKey,issuerPrivateKey,roles,notBefore,notAfter}){
 const record={subject,issuer,publicJwk:await publicJwk(publicKey),roles:[...roles].sort(),notBefore,notAfter};
 validRecord(record);return {...record,signature:await signed(issuerPrivateKey,"certificate",record)};
}
export async function signKeyRevocation({subject,rootId,rootPrivateKey,sequence,reason}){
 if(!cleanId(subject)||!cleanId(rootId)||!validTime(sequence)||typeof reason!=="string"||!reason.trim()||reason.length>240)throw Error("Invalid revocation");
 const record={subject,rootId,sequence,reason};return {...record,signature:await signed(rootPrivateKey,"revocation",record)};
}
export async function verifyTrustedKeyLineage({packet,manifest,attestation,rootId,rootPublicKey,certificates,revocations=[],asOf}){
 try{
  if(!cleanId(rootId)||!validTime(asOf))throw Error("Trusted root or verification time missing");
  if(!Array.isArray(certificates)||certificates.length<1||certificates.length>8||!Array.isArray(revocations)||revocations.length>64)throw Error("Lineage bounds");
  const rootJwk=await publicJwk(rootPublicKey),rootFp=await keyId(rootJwk);
  const map=new Map();
  for(const c of certificates){
   validRecord(c);
   if(Object.keys(c).sort().join(",")!=="issuer,notAfter,notBefore,publicJwk,roles,signature,subject")throw Error("Unknown certificate field");
   if(map.has(c.subject)||c.subject===rootId)throw Error("Duplicate or spoofed certificate");
   await importJwk(c.publicJwk);map.set(c.subject,c);
  }
  const revoked=new Set();
  for(const r of revocations){
   if(!r||Object.keys(r).sort().join(",")!=="reason,rootId,sequence,signature,subject"||r.rootId!==rootId||!cleanId(r.subject)||!validTime(r.sequence)||typeof r.reason!=="string"||!r.reason.trim())throw Error("Invalid revocation record");
   const {signature,...record}=r;
   if(!await checked(rootPublicKey,"revocation",record,signature))throw Error("Unauthenticated revocation record");
   if(r.sequence<=asOf)revoked.add(r.subject);
  }
  const signer=attestation?.signer;
  if(!cleanId(signer)||!map.has(signer))throw Error("Signer is not delegated by trusted root");
  const seen=new Set(),walk=[];
  let current=signer,depth=0;
  while(current!==rootId){
   if(++depth>8||seen.has(current))throw Error("Cyclic or excessively deep lineage");
   seen.add(current);
   const c=map.get(current);
   if(!c)throw Error("Missing trust ancestor");
   if(asOf<c.notBefore||asOf>=c.notAfter)throw Error("Certificate expired or not yet valid");
   if(revoked.has(current))throw Error("Key lineage is revoked");
   const parentKey=c.issuer===rootId?rootPublicKey:await importJwk(map.get(c.issuer)?.publicJwk);
   const {signature,...record}=c;
   if(!await checked(parentKey,"certificate",record,signature))throw Error("Certificate signature invalid");
   if(c.issuer!==rootId){
    const parent=map.get(c.issuer);
    if(!parent?.roles.includes("delegate"))throw Error("Parent is not a delegate");
    if(c.roles.some(role=>!parent.roles.includes(role)))throw Error("Parent cannot grant greater authority");
   }
   walk.push({subject:current,issuer:c.issuer,roles:[...c.roles]});
   current=c.issuer;
  }
  if(!map.get(signer).roles.includes("origin-attest"))throw Error("Signer not authorized for origin attestation");
  if(revoked.has(rootId))throw Error("Root revoked");
  const key=await importJwk(map.get(signer).publicJwk);
  const result=await verifyAuthenticatedOrigin(packet,manifest,attestation,key);
  if(!result.pass)throw Error("Origin signature invalid: "+result.error);
  return {pass:true,rootId,rootFingerprint:rootFp,signer,chain:walk,revocationsConsidered:revocations.length,authenticatedToPinnedRoot:true,interpretationProven:false};
 }catch(e){return {pass:false,error:e.message}}
}
