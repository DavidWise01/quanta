// ADA-206N · Source-bound adaptive mutation in a separate immutable derived ledger.
// No changes to frozen Phase II root, 201N generation, 202N journal, 204N contacts, or 205N growth.
import {PHASE_II_FREEZE,canonical,fnv64,bound,verifyChain} from "./ada-201n-generational-engine.mjs";
import {deriveContacts} from "./ada-204n-three-contact-inheritance.mjs";
import {deriveGrowth} from "./ada-205n-homeostatic-growth.mjs";
export const MUTATION_SCHEMA="ADA-206N.mutation.v1";
export const STEP_LIMIT=0.025;
export const TOTAL_LIMIT=0.25;
const round=x=>Number(x.toFixed(6));
export function deriveMutations(chain){
 const check=verifyChain(chain);if(!check.pass)throw Error("Invalid ancestor chain: "+check.reason);
 const contacts=deriveContacts(chain),growth=deriveGrowth(chain),ledger=[];
 let policy=0;
 for(let n=0;n<chain.length;n++){
  const gen=chain[n],contact=contacts[n],g=growth[n],parent=ledger.at(-1);
  // Jane proposes a measured, signed adjustment from observed error. Clamp before Toph's gate.
  const observed=round((gen.contacts[0]-gen.contacts[1])/100);
  const proposed=round(bound(observed,-STEP_LIMIT,STEP_LIMIT));
  const eligible=n>0&&contact.state.toph.eligible&&contact.decision==="APPEND"&&g.stepFactor===1.025;
  const applied=eligible?round(bound(proposed,-STEP_LIMIT,STEP_LIMIT)):0;
  const nextPolicy=eligible?round(bound(policy+applied,-TOTAL_LIMIT,TOTAL_LIMIT)):policy;
  const effective=round(nextPolicy-policy);
  const decision=n===0?"ROOT":!eligible?"HOLD":effective===0?"NO_CHANGE":"MUTATE";
  const body={schema:MUTATION_SCHEMA,n,sourceRoot:PHASE_II_FREEZE,
   generationHash:gen.hash,contactHash:contact.hash,growthHash:g.hash,
   parent:parent?.hash||null,proposed,applied:effective,
   policy:nextPolicy,eligible,decision,
   stepLimit:STEP_LIMIT,totalLimit:TOTAL_LIMIT,
   inheritedPolicy:policy};
  ledger.push(Object.freeze({...body,hash:fnv64(canonical(body))}));
  policy=nextPolicy;
 }
 return Object.freeze(ledger);
}
export function verifyMutations(chain,ledger){
 try{
  if(!Array.isArray(ledger)||ledger.length!==chain.length)return {pass:false,reason:"Mutation ledger length mismatch"};
  const expected=deriveMutations(chain);
  for(let i=0;i<expected.length;i++)if(canonical(expected[i])!==canonical(ledger[i]))return {pass:false,reason:"Mutation mismatch at generation "+i};
  return {pass:true,generations:ledger.length,tip:ledger.at(-1).hash,policy:ledger.at(-1).policy,mutated:ledger.filter(x=>x.decision==="MUTATE").length,held:ledger.filter(x=>x.decision==="HOLD").length,sourceRoot:PHASE_II_FREEZE};
 }catch(e){return {pass:false,reason:String(e.message||e)}}
}
export function mutationProof(chain,n=chain.length-1){
 if(!Number.isSafeInteger(n)||n<0||n>=chain.length)throw Error("Invalid mutation generation");
 const item=deriveMutations(chain)[n];
 return Object.freeze({schema:"ADA-206N.proof.v1",n,parentRoot:item.sourceRoot,generationHash:item.generationHash,contactHash:item.contactHash,growthHash:item.growthHash,priorMutationHash:item.parent,policy:item.policy,proposed:item.proposed,applied:item.applied,decision:item.decision,mutationHash:item.hash});
}
