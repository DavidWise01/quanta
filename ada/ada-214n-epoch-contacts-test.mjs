import assert from "node:assert/strict";
import {genesis,advance,verifyChain,PHASE_II_FREEZE} from "./ada-201n-generational-engine.mjs";
import {PHASE_III_FREEZE,epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveEpochContacts,verifyEpochContacts,epochContactProof} from "./ada-214n-epoch-contacts.mjs";
const chain=advance([genesis()],240),original=JSON.stringify(chain),epochs=epochHierarchy(chain);
const contacts=deriveEpochContacts(chain),audit=verifyEpochContacts(chain,contacts);
assert(audit.pass);assert.equal(contacts.length,11);assert.equal(audit.sealed,10);assert.equal(audit.open,1);assert.equal(audit.holds,17);
assert.equal(audit.sourceRoot,PHASE_II_FREEZE);assert.equal(audit.phaseIIIFreeze,PHASE_III_FREEZE);
assert.deepEqual(contacts,deriveEpochContacts(chain),"Deterministic replay");
assert.equal(JSON.stringify(chain),original,"No source mutation");
assert(verifyChain(chain).pass);
for(let i=0;i<contacts.length;i++){
 const c=contacts[i],e=epochs[i];
 assert(Object.isFrozen(c)&&Object.isFrozen(c.state)&&Object.isFrozen(c.state.jane)&&Object.isFrozen(c.state.toph)&&Object.isFrozen(c.state.ada));
 assert.equal(c.epochHash,e.hash);
 assert.equal(c.sourceGenerationHash,chain[e.sourceEnd].hash);
 assert.equal(c.state.toph.heldDecisions,e.holds);
 assert.equal(c.state.ada.recordedAppends,e.appends);
 assert.equal(c.state.ada.recordedHolds,e.holds);
 assert.equal(c.decision,e.state==="SEALED"?"SEAL":"OPEN_TAIL");
 assert.equal(c.state.toph.eligibleToSeal,e.state==="SEALED");
 if(i>0){
  assert.equal(c.parentContactHash,contacts[i-1].hash);
  assert.equal(c.state.jane.inherited,contacts[i-1].state.jane.id);
  assert.equal(c.state.toph.inherited,contacts[i-1].state.toph.id);
  assert.equal(c.state.ada.inherited,contacts[i-1].state.ada.id);
 }
}
const last=contacts.at(-1);
assert.equal(last.decision,"OPEN_TAIL");
assert.equal(last.state.toph.heldDecisions,1);
assert.equal(last.state.ada.action,"OPEN_TAIL");
const proof=epochContactProof(chain,10);
assert.equal(proof.originalSourceRoots,1);assert.equal(proof.contactHash,last.hash);
assert.equal(proof.parentContactHash,contacts[9].hash);
const changed=structuredClone(contacts);changed[5].state.toph.heldDecisions++;
assert.equal(verifyEpochContacts(chain,changed).pass,false);
const forged=structuredClone(contacts);forged[2].parentContactHash="0".repeat(16);
assert.equal(verifyEpochContacts(chain,forged).pass,false);
const alternate=deriveEpochContacts(chain,{size:8});
assert(verifyEpochContacts(chain,alternate,{size:8}).pass);
assert.throws(()=>deriveEpochContacts([{...chain[0],energy:0}]),/Invalid immutable source/);
console.log(JSON.stringify({schema:"ADA-214N.test.v1",pass:true,generations:chain.length,epochs:contacts.length,sealed:audit.sealed,open:audit.open,holds:audit.holds,checks:["three inherited identities","sealed/open epoch gate","single original root","source HOLD preservation","parent contact hashes","immutable ancestry","deterministic replay","tamper rejection","alternate epoch capacity"]},null,2));
