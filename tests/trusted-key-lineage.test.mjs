import test from "node:test";import assert from "node:assert/strict";
import {demo84211,close84211} from "../language/lossless-closure.mjs";
import {buildClosureManifest} from "../language/independent-closure.mjs";
import {attestOrigin,generateDemoSigningKeys} from "../language/authenticated-origin.mjs";
import {issueKeyCertificate,signKeyRevocation,verifyTrustedKeyLineage} from "../language/trusted-key-lineage.mjs";
const copy=x=>JSON.parse(JSON.stringify(x));
async function sample(){
 const root=await generateDemoSigningKeys(),signer=await generateDemoSigningKeys(),source=demo84211();
 const packet=close84211(source),manifest=buildClosureManifest(source);
 const attestation=await attestOrigin(packet,manifest,signer.privateKey,"witness-key");
 const certificate=await issueKeyCertificate({subject:"witness-key",issuer:"trusted-root",publicKey:signer.publicKey,issuerPrivateKey:root.privateKey,roles:["origin-attest"],notBefore:100,notAfter:300});
 return {packet,manifest,attestation,root,signer,certificates:[certificate],rootId:"trusted-root",rootPublicKey:root.publicKey,revocations:[],asOf:200};
}
test("root-signed delegation validates attestation",async()=>{const f=await sample();const r=await verifyTrustedKeyLineage(f);assert.equal(r.pass,true);assert.equal(r.chain.length,1);assert.equal(r.interpretationProven,false)});
test("wrong root, substituted cert and fabricated authority fail",async()=>{const f=await sample(),other=await generateDemoSigningKeys();assert.equal((await verifyTrustedKeyLineage({...f,rootPublicKey:other.publicKey})).pass,false);let cs=copy(f.certificates);cs[0].roles=["origin-attest","delegate"];assert.equal((await verifyTrustedKeyLineage({...f,certificates:cs})).pass,false)});
test("root signed revocation blocks even valid past signature at later evaluation",async()=>{const f=await sample(),r=await signKeyRevocation({subject:"witness-key",rootId:f.rootId,rootPrivateKey:f.root.privateKey,sequence:201,reason:"Compromised"});assert.equal((await verifyTrustedKeyLineage({...f,revocations:[r],asOf:200})).pass,true);assert.equal((await verifyTrustedKeyLineage({...f,revocations:[r],asOf:202})).pass,false)});
test("unsigned or tampered revocation fails closed",async()=>{const f=await sample(),r=await signKeyRevocation({subject:"witness-key",rootId:f.rootId,rootPrivateKey:f.root.privateKey,sequence:190,reason:"Lost"});r.reason="Forged";assert.equal((await verifyTrustedKeyLineage({...f,revocations:[r]})).pass,false)});
test("expired and not-yet-valid delegation fail",async()=>{const f=await sample();assert.equal((await verifyTrustedKeyLineage({...f,asOf:99})).pass,false);assert.equal((await verifyTrustedKeyLineage({...f,asOf:300})).pass,false)});
test("signer label substitution and wrong signing key fail",async()=>{const f=await sample();let a=copy(f.attestation);a.signer="someone-else";assert.equal((await verifyTrustedKeyLineage({...f,attestation:a})).pass,false)});
test("missing ancestry and cyclic parent fail",async()=>{const f=await sample();assert.equal((await verifyTrustedKeyLineage({...f,certificates:[]})).pass,false);const c=copy(f.certificates);c[0].issuer="witness-key";assert.equal((await verifyTrustedKeyLineage({...f,certificates:c})).pass,false)});
test("delegate chain retains role confinement",async()=>{const f=await sample(),parent=await generateDemoSigningKeys();const upper=await issueKeyCertificate({subject:"middle",issuer:f.rootId,publicKey:parent.publicKey,issuerPrivateKey:f.root.privateKey,roles:["delegate","origin-attest"],notBefore:100,notAfter:300});const lower=await issueKeyCertificate({subject:"witness-key",issuer:"middle",publicKey:f.signer.publicKey,issuerPrivateKey:parent.privateKey,roles:["origin-attest"],notBefore:101,notAfter:290});assert.equal((await verifyTrustedKeyLineage({...f,certificates:[upper,lower]})).pass,true);const noRole=await issueKeyCertificate({subject:"middle",issuer:f.rootId,publicKey:parent.publicKey,issuerPrivateKey:f.root.privateKey,roles:["origin-attest"],notBefore:100,notAfter:300});assert.equal((await verifyTrustedKeyLineage({...f,certificates:[noRole,lower]})).pass,false)});
test("packet tamper is rejected after trust verification",async()=>{const f=await sample(),p=copy(f.packet);p.source.actors[0].statement="changed";assert.equal((await verifyTrustedKeyLineage({...f,packet:p})).pass,false)});
