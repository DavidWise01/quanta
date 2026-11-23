import assert from "node:assert/strict";
import {PHASE_II_FREEZE,genesis,advance,verifyChain} from "./ada-201n-generational-engine.mjs";
import {deriveGrowth,verifyGrowth,growthProof,GROWTH_FACTOR} from "./ada-205n-homeostatic-growth.mjs";
const chain=advance([genesis()],120),source=JSON.stringify(chain);
const ledger=deriveGrowth(chain),audit=verifyGrowth(chain,ledger);
assert.equal(audit.pass,true);assert.equal(ledger.length,121);
assert.equal(GROWTH_FACTOR,1.025);assert.equal(ledger[0].size,1);
assert.deepEqual(deriveGrowth(chain),ledger,"Deterministic growth");
assert.equal(JSON.stringify(chain),source,"No ancestor mutation");
assert.equal(ledger.at(-1).growthSteps,114);
assert.equal(ledger.filter(x=>x.decision==="HOLD").length,6);
assert.equal(ledger.at(-1).size,Number(Math.pow(1.025,114).toPrecision(14)));
for(let n=1;n<ledger.length;n++){
 const current=ledger[n],before=ledger[n-1];
 assert.equal(current.parent,before.hash,"Parent linkage");
 assert.equal(current.sourceRoot,PHASE_II_FREEZE);
 assert.equal(current.stepFactor,current.decision==="APPEND"?1.025:1);
 assert.equal(current.growthSteps,before.growthSteps+(current.decision==="APPEND"?1:0));
 if(current.decision==="HOLD")assert.equal(current.size,before.size,"HOLD never increases size");
 assert(Object.isFrozen(current),"Every growth state is immutable");
}
const p=growthProof(chain,57);assert.equal(p.decision,"HOLD");assert.equal(p.stepFactor,1);assert.equal(p.sourceRoot,PHASE_II_FREEZE);
const attack=structuredClone(ledger);attack[12].size+=1;assert.equal(verifyGrowth(chain,attack).pass,false);
assert.throws(()=>deriveGrowth([{...chain[0],signal:1}]),/invalid lineage/);
assert(verifyChain(chain).pass);
console.log(JSON.stringify({schema:"ADA-205N.test.v1",pass:true,generations:ledger.length,growthSteps:audit.growthSteps,holds:audit.holds,multiplier:GROWTH_FACTOR,finalSize:audit.size,checks:["frozen source","1.025 multiplier","deterministic replay","HOLD non-growth","growth parent continuity","immutable states","tamper detection","invalid source rejection"]},null,2));
