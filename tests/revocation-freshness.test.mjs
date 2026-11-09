import test from "node:test";import assert from "node:assert/strict";
import {demo84211,close84211} from "../language/lossless-closure.mjs";
import {buildClosureManifest} from "../language/independent-closure.mjs";
import {attestOrigin,generateDemoSigningKeys} from "../language/authenticated-origin.mjs";
import {issueKeyCertificate,signKeyRevocation} from "../language/trusted-key-lineage.mjs";
import {signFreshnessCheckpoint,verifyFreshAuthority} from "../language/revocation-freshness.mjs";
const c=x=>JSON.parse(JSON.stringify(x));
async function fixture(){
 const root=await generateDemoSigningKeys(),signer=await generateDemoSigningKeys(),source=demo84211(),packet=close84211(source),manifest=buildClosureManifest(source);
 const attestation=await attestOrigin(packet,manifest,signer.privateKey,"witness-key");
 const certificates=[await issueKeyCertificate({subject:"witness-key",issuer:"trusted-root",publicKey:signer.publicKey,issuerPrivateKey:root.privateKey,roles:["origin-attest"],notBefore:100,notAfter:400})];
 const revocations=[],checkpoint=await signFreshnessCheckpoint({rootId:"trusted-root",sequence:7,issuedAt:190,expiresAt:240,revocations,rootPrivateKey:root.privateKey});
 return {root,packet,manifest,attestation,certificates,rootId:"trusted-root",rootPublicKey:root.publicKey,revocations,checkpoint,asOf:200,minSequence:7,maxCheckpointAge:30};
}
test("fresh signed complete checkpoint permits already authorized signer",async()=>{const f=await fixture(),r=await verifyFreshAuthority(f);assert.equal(r.pass,true);assert.equal(r.sequence,7);assert.equal(r.interpretationProven,false)});
test("expired and future checkpoints fail closed",async()=>{const f=await fixture();assert.equal((await verifyFreshAuthority({...f,asOf:240})).pass,false);assert.equal((await verifyFreshAuthority({...f,asOf:189})).pass,false)});
test("checkpoint too old by local policy is rejected",async()=>{const f=await fixture();assert.equal((await verifyFreshAuthority({...f,asOf:225,maxCheckpointAge:30})).pass,false)});
test("sequence rollback below independent high water mark fails",async()=>{const f=await fixture();assert.equal((await verifyFreshAuthority({...f,minSequence:8})).pass,false)});
test("signed checkpoint rejects substituted revocation set",async()=>{const f=await fixture();const rev=await signKeyRevocation({subject:"witness-key",rootId:f.rootId,rootPrivateKey:f.root.privateKey,sequence:195,reason:"Compromised"});assert.equal((await verifyFreshAuthority({...f,revocations:[rev]})).pass,false)});
test("matching signed revoked key fails despite valid prior signature",async()=>{const f=await fixture();const rev=await signKeyRevocation({subject:"witness-key",rootId:f.rootId,rootPrivateKey:f.root.privateKey,sequence:195,reason:"Compromised"});const checkpoint=await signFreshnessCheckpoint({rootId:f.rootId,sequence:8,issuedAt:197,expiresAt:240,revocations:[rev],rootPrivateKey:f.root.privateKey});assert.equal((await verifyFreshAuthority({...f,revocations:[rev],checkpoint,minSequence:8})).pass,false)});
test("forged checkpoint contents or signature cannot be trusted",async()=>{const f=await fixture();for(const fn of [x=>x.checkpoint.sequence=9,x=>x.checkpoint.complete=false,x=>x.checkpoint.signature="00".repeat(64),x=>x.checkpoint.expiresAt=250]){const x={...f,checkpoint:c(f.checkpoint)};fn(x);assert.equal((await verifyFreshAuthority(x)).pass,false)}});
test("wrong trust root and missing policy fail",async()=>{const f=await fixture(),other=await generateDemoSigningKeys();assert.equal((await verifyFreshAuthority({...f,rootPublicKey:other.publicKey})).pass,false);assert.equal((await verifyFreshAuthority({...f,minSequence:undefined})).pass,false);assert.equal((await verifyFreshAuthority({...f,maxCheckpointAge:undefined})).pass,false)});
test("checkpoint signed for other root fails",async()=>{const f=await fixture();assert.equal((await verifyFreshAuthority({...f,rootId:"another-root"})).pass,false)});
test("packet alteration still fails downstream full chain",async()=>{const f=await fixture(),packet=c(f.packet);packet.source.actors[0].statement="forged";assert.equal((await verifyFreshAuthority({...f,packet})).pass,false)});
test("invalid revocation duplication rejected when signing checkpoint",async()=>{const f=await fixture(),r=await signKeyRevocation({subject:"witness-key",rootId:f.rootId,rootPrivateKey:f.root.privateKey,sequence:195,reason:"Lost"});await assert.rejects(()=>signFreshnessCheckpoint({rootId:f.rootId,sequence:8,issuedAt:197,expiresAt:240,revocations:[r,r],rootPrivateKey:f.root.privateKey}))});
