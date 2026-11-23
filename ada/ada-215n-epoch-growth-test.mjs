import assert from "node:assert/strict";
import {PHASE_II_FREEZE,genesis,advance,verifyChain} from "./ada-201n-generational-engine.mjs";
import {PHASE_III_FREEZE} from "./ada-211n-epoch-engine.mjs";
import {deriveGrowth} from "./ada-205n-homeostatic-growth.mjs";
import {deriveEpochGrowth,verifyEpochGrowth,epochGrowthProof,EPOCH_GROWTH_FACTOR} from "./ada-215n-epoch-growth.mjs";
const root=[genesis()],chain=advance(root,240),original=JSON.stringify(chain),growth=deriveGrowth(chain),growthBytes=JSON.stringify(growth);
const ledger=deriveEpochGrowth(chain),audit=verifyEpochGrowth(chain,ledger);
assert(audit.pass);
assert.equal(EPOCH_GROWTH_FACTOR,1.025);
assert.equal(ledger.length,11);assert.equal(audit.sealedSteps,10);assert.equal(audit.open,1);
assert.equal(audit.size,Number(Math.pow(1.025,10).toPrecision(14)));
assert.equal(ledger.at(-1).stepFactor,1,"OPEN_TAIL is not a growth event");
assert.equal(ledger.at(-1).sizeMultiplier,ledger.at(-2).sizeMultiplier,"OPEN_TAIL must preserve last size");
assert.equal(ledger.at(-1).generationMultiplier,growth.at(-1).size,"Source generation growth remains linked");
for(let n=0;n<ledger.length;n++){
 const e=ledger[n];assert(Object.isFrozen(e));assert.equal(e.epoch,n);
 assert.equal(e.phaseIIIFreeze,PHASE_III_FREEZE);assert.equal(e.originalRoot,PHASE_II_FREEZE);
 assert.equal(e.stepFactor,n<10?1.025:1);
 assert.equal(e.sealedSteps,Math.min(n+1,10));
 if(n>0)assert.equal(e.parentGrowthHash,ledger[n-1].hash);
 if(e.state==="OPEN_TAIL"&&n>0)assert.equal(e.sizeMultiplier,ledger[n-1].sizeMultiplier);
}
const oneSealed=deriveEpochGrowth(advance(root,23));
assert.equal(oneSealed.length,1);assert.equal(oneSealed[0].stepFactor,1.025);
const oneTail=deriveEpochGrowth(advance(root,24));
assert.equal(oneTail.length,2);assert.equal(oneTail[1].stepFactor,1);
assert.equal(oneTail[1].sizeMultiplier,oneSealed[0].sizeMultiplier);
const noSealed=deriveEpochGrowth(root);assert.equal(noSealed[0].sizeMultiplier,1);
assert.equal(noSealed[0].stepFactor,1);
assert.deepEqual(ledger,deriveEpochGrowth(chain),"Deterministic epoch growth");
assert.equal(JSON.stringify(chain),original,"Source generation history must remain immutable");
assert.equal(JSON.stringify(deriveGrowth(chain)),growthBytes,"Prior generation-growth layer must remain unchanged");
assert(verifyChain(chain).pass);
const tampered=structuredClone(ledger);tampered[3].sizeMultiplier+=.1;
assert.equal(verifyEpochGrowth(chain,tampered).pass,false,"Tamper rejected");
const linked=structuredClone(ledger);linked[4].parentGrowthHash="0".repeat(16);
assert.equal(verifyEpochGrowth(chain,linked).pass,false,"Forged parent rejected");
const proof=epochGrowthProof(chain,10);
assert.equal(proof.state,"OPEN_TAIL");assert.equal(proof.stepFactor,1);
assert.equal(proof.growthHash,ledger.at(-1).hash);
const variant=deriveEpochGrowth(chain,{size:8});assert(verifyEpochGrowth(chain,variant,{size:8}).pass);
assert.throws(()=>deriveEpochGrowth([{...chain[0],signal:999}]),/Invalid inherited source/);
console.log(JSON.stringify({schema:"ADA-215N.test.v1",pass:true,sourceGenerations:chain.length,
 epochs:ledger.length,sealedSteps:audit.sealedSteps,open:audit.open,epochMultiplier:audit.size,
 sourceGenerationMultiplier:growth.at(-1).size,checks:["source freeze","single growth per sealed epoch","no OPEN_TAIL growth",
 "source generation growth untouched","deterministic replay","parent hash continuity","tamper rejection",
 "open-to-sealed transition","alternate epoch capacity","invalid ancestry rejection"]},null,2));
