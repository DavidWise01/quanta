// ADA-215N · Homeostatic growth at epoch scale, derived from sealed epoch state.
// Multiplies by 1.025 exactly once per SEALED epoch; OPEN_TAIL contributes x1.
// The original generation growth history is referenced, never recomputed as epoch growth.
import {PHASE_II_FREEZE,verifyChain,fnv64,canonical} from "./ada-201n-generational-engine.mjs";
import {PHASE_III_FREEZE,epochHierarchy,EPOCH_SIZE} from "./ada-211n-epoch-engine.mjs";
import {deriveGrowth,GROWTH_FACTOR} from "./ada-205n-homeostatic-growth.mjs";
import {deriveEpochContacts,verifyEpochContacts} from "./ada-214n-epoch-contacts.mjs";
export const EPOCH_GROWTH_SCHEMA="ADA-215N.epoch-homeostasis.v1";
export const EPOCH_GROWTH_FACTOR=GROWTH_FACTOR;
export function deriveEpochGrowth(chain,{size=EPOCH_SIZE}={}){
 const audit=verifyChain(chain);if(!audit.pass)throw Error("Invalid inherited source: "+audit.reason);
 const epochs=epochHierarchy(chain,{size}),contacts=deriveEpochContacts(chain,{size}),check=verifyEpochContacts(chain,contacts,{size});
 if(!check.pass)throw Error("Epoch contacts inconsistent: "+check.reason);
 const generationGrowth=deriveGrowth(chain),ledger=[];
 let sealedSteps=0;
 for(const epoch of epochs){
  const contact=contacts[epoch.epoch],lastGen=generationGrowth[epoch.sourceEnd];
  const eligible=epoch.state==="SEALED"&&contact.decision==="SEAL"&&contact.state.toph.eligibleToSeal;
  if(eligible)sealedSteps++;
  const multiplier=Math.pow(EPOCH_GROWTH_FACTOR,sealedSteps);
  if(!Number.isFinite(multiplier))throw Error("Epoch growth exceeds finite numeric range");
  const sizeMultiplier=Number(multiplier.toPrecision(14));
  const parent=ledger.at(-1);
  const body={schema:EPOCH_GROWTH_SCHEMA,epoch:epoch.epoch,phaseIIIFreeze:PHASE_III_FREEZE,
   originalRoot:PHASE_II_FREEZE,epochHash:epoch.hash,epochContactHash:contact.hash,
   sourceGenerationGrowthHash:lastGen.hash,parentGrowthHash:parent?.hash||null,
   state:epoch.state,eligible,stepFactor:eligible?EPOCH_GROWTH_FACTOR:1,
   sealedSteps,sizeMultiplier,generationMultiplier:lastGen.size,
   rule:"Epoch multiplier is separately derived: ×1.025 per SEALED epoch; OPEN_TAIL ×1; generation growth history unchanged"};
  ledger.push(Object.freeze({...body,hash:fnv64(canonical(body))}));
 }
 return Object.freeze(ledger);
}
export function verifyEpochGrowth(chain,ledger,{size=EPOCH_SIZE}={}){
 try{
  if(!Array.isArray(ledger))return {pass:false,reason:"Growth ledger must be an array"};
  const expected=deriveEpochGrowth(chain,{size});
  if(canonical(ledger)!==canonical(expected))return {pass:false,reason:"Epoch growth derivation or ancestry mismatch"};
  return {pass:true,epochs:ledger.length,sealedSteps:ledger.at(-1).sealedSteps,
   open:ledger.filter(e=>e.state==="OPEN_TAIL").length,size:ledger.at(-1).sizeMultiplier,
   tip:ledger.at(-1).hash,phaseIIIFreeze:PHASE_III_FREEZE};
 }catch(error){return {pass:false,reason:error.message}}
}
export function epochGrowthProof(chain,index,{size=EPOCH_SIZE}={}){
 const ledger=deriveEpochGrowth(chain,{size});
 if(!Number.isSafeInteger(index)||index<0||index>=ledger.length)throw Error("Epoch growth index outside ancestry");
 const item=ledger[index];
 return Object.freeze({schema:"ADA-215N.epoch-growth-proof.v1",epoch:index,phaseIIIFreeze:PHASE_III_FREEZE,
  epochHash:item.epochHash,epochContactHash:item.epochContactHash,
  generationGrowthHash:item.sourceGenerationGrowthHash,priorEpochGrowthHash:item.parentGrowthHash,
  state:item.state,stepFactor:item.stepFactor,sealedSteps:item.sealedSteps,sizeMultiplier:item.sizeMultiplier,
  growthHash:item.hash});
}
