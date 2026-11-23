import assert from "node:assert/strict";
import {PHASE_II_FREEZE,genesis,advance,verifyChain} from "./ada-201n-generational-engine.mjs";
import {deriveGrowth} from "./ada-205n-homeostatic-growth.mjs";
import {STEP_LIMIT,TOTAL_LIMIT,deriveMutations,verifyMutations,mutationProof} from "./ada-206n-bounded-mutation.mjs";
const chain=advance([genesis()],120),unchanged=JSON.stringify(chain),growth=deriveGrowth(chain);
const ledger=deriveMutations(chain),audit=verifyMutations(chain,ledger);
assert.equal(STEP_LIMIT,.025);assert.equal(TOTAL_LIMIT,.25);
assert(audit.pass);assert.equal(ledger.length,121);
assert.equal(audit.held,6);
assert.equal(audit.mutated,114);
assert.deepEqual(ledger,deriveMutations(chain),"Bit-for-bit replay");
assert.equal(JSON.stringify(chain),unchanged,"Ancestors must not mutate");
assert(verifyChain(chain).pass);
for(let n=0;n<ledger.length;n++){
 const item=ledger[n];assert(Object.isFrozen(item));
 assert.equal(item.sourceRoot,PHASE_II_FREEZE);
 assert.equal(item.growthHash,growth[n].hash);
 assert(Math.abs(item.applied)<=STEP_LIMIT+1e-7,"Step limit");
 assert(Math.abs(item.policy)<=TOTAL_LIMIT+1e-7,"Total policy bound");
 if(n){assert.equal(item.parent,ledger[n-1].hash);assert.equal(item.inheritedPolicy,ledger[n-1].policy)}
 if(item.decision==="HOLD"){assert.equal(item.applied,0);assert.equal(item.policy,item.inheritedPolicy)}
}
const hold=ledger.find(x=>x.decision==="HOLD"),proof=mutationProof(chain,hold.n);
assert.equal(proof.decision,"HOLD");assert.equal(proof.applied,0);assert.equal(proof.mutationHash,hold.hash);
const tampered=structuredClone(ledger);tampered[7].policy=.25;
assert.equal(verifyMutations(chain,tampered).pass,false);
assert.throws(()=>deriveMutations([{...chain[0],energy:0}]),/Invalid ancestor chain/);
console.log(JSON.stringify({schema:"ADA-206N.test.v1",pass:true,generations:ledger.length,mutated:audit.mutated,held:audit.held,finalPolicy:audit.policy,stepLimit:STEP_LIMIT,totalLimit:TOTAL_LIMIT,checks:["replay","immutable inherited state","single source root","growth hash reference","step and global bounds","HOLD zero mutation","parent continuity","tamper rejection","invalid ancestry rejection"]},null,2));
