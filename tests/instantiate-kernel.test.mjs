import test from "node:test";
import assert from "node:assert/strict";
import {instantiateCanonicalKernel,canonicalStatus} from "../language/instantiate-kernel.mjs";
import {verifyWitnessLineage} from "../language/witness-lineage.mjs";
test("QG-034 boots canonical three-witness shared-origin fixture",()=>{
 const instance=instantiateCanonicalKernel();
 assert.equal(instance.q33.pass,true);
 assert.equal(instance.q34.pass,true);
 assert.equal(instance.ledger.source.trios[0].witnesses.length,3);
 assert.equal(instance.ledger.report.independentLineages,1);
 assert.equal(instance.ledger.report.uniqueOrigins.length,1);
 assert.equal(instance.ledger.report.threeIndependent,false);
 assert.equal(instance.ledger.report.interpretationProven,false);
});
test("bootstrapping produces identical replayable state without mutation",()=>{
 const a=instantiateCanonicalKernel(),b=instantiateCanonicalKernel();
 assert.deepEqual(a.ledger,b.ledger);
 assert.equal(verifyWitnessLineage(JSON.parse(JSON.stringify(a.ledger))).pass,true);
 assert.equal(canonicalStatus().status,"INSTANTIATED");
 assert.equal(a.persisted,false);
});
test("live verified-source provenance is not faked by a demo fixture",()=>{
 const k=instantiateCanonicalKernel();
 assert.equal(k.fixture,true);
 assert.match(k.ledger.source.trios[0].witnesses[0].source.url,/example/);
 assert.equal(k.mode,"observation-only");
});
