// ADA-205N · Homeostatic generational growth.
// Dimensionless growth factor: 1 * 1.025 per eligible APPEND;
// HOLD is recorded as a generation, but does not increase the growth state.
// This is a deterministic model, not a claim of physical Planck-scale expansion.
import {PHASE_II_FREEZE,verifyChain,fnv64,canonical} from "./ada-201n-generational-engine.mjs";
import {deriveContacts,verifyContacts} from "./ada-204n-three-contact-inheritance.mjs";
export const GROWTH_SCHEMA="ADA-205N.homeostasis.v1";
export const GROWTH_FACTOR=1.025;
const freeze=x=>Object.freeze(x);
export function deriveGrowth(chain){
 const result=verifyChain(chain);
 if(!result.pass)throw Error("Cannot grow invalid lineage: "+result.reason);
 const contacts=deriveContacts(chain),audit=verifyContacts(chain,contacts);
 if(!audit.pass)throw Error("Cannot grow invalid contact lineage: "+audit.reason);
 const out=[];
 let growthSteps=0;
 for(let n=0;n<chain.length;n++){
  const source=chain[n],contact=contacts[n];
  if(n!==0&&contact.decision==="APPEND")growthSteps++;
  const size=Number(Math.pow(GROWTH_FACTOR,growthSteps).toPrecision(14));
  const body={schema:GROWTH_SCHEMA,n,sourceRoot:PHASE_II_FREEZE,generationHash:source.hash,contactHash:contact.hash,parent:out.at(-1)?.hash||null,
   decision:contact.decision,eligible:n===0?false:contact.state.toph.eligible,
   growthSteps,stepFactor:n===0?1:contact.decision==="APPEND"?GROWTH_FACTOR:1,
   size,rule:"1 × 1.025 per eligible APPEND; HOLD does not grow"};
  out.push(freeze({...body,hash:fnv64(canonical(body))}));
 }
 return freeze(out);
}
export function verifyGrowth(chain,ledger){
 try{
  if(!Array.isArray(ledger)||ledger.length!==chain.length)return {pass:false,reason:"Growth ledger length mismatch"};
  const expected=deriveGrowth(chain);
  for(let n=0;n<expected.length;n++)if(canonical(expected[n])!==canonical(ledger[n]))return {pass:false,reason:"Growth mismatch at generation "+n};
  return {pass:true,generations:ledger.length,tip:ledger.at(-1).hash,size:ledger.at(-1).size,growthSteps:ledger.at(-1).growthSteps,holds:ledger.filter(x=>x.decision==="HOLD").length,sourceRoot:PHASE_II_FREEZE};
 }catch(e){return {pass:false,reason:e.message}}
}
export function growthProof(chain,n=chain.length-1){
 if(!Number.isSafeInteger(n)||n<0||n>=chain.length)throw Error("Invalid growth generation");
 const ledger=deriveGrowth(chain),entry=ledger[n];
 return freeze({schema:"ADA-205N.growth-proof.v1",sourceRoot:PHASE_II_FREEZE,sourceGenerationHash:entry.generationHash,sourceContactHash:entry.contactHash,
  n,previousGrowthHash:entry.parent,decision:entry.decision,stepFactor:entry.stepFactor,eligibleSteps:entry.growthSteps,size:entry.size,hash:entry.hash});
}
