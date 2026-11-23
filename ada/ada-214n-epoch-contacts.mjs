// ADA-214N · Derived Jane / Toph / ADA inheritance across sealed and provisional epochs.
// Each epoch inherits one prior epoch state, references the original source generation
// decisions, and NEVER modifies the write-once source or sealed epoch receipts.
import {PHASE_II_FREEZE,verifyChain,canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveContacts} from "./ada-204n-three-contact-inheritance.mjs";
import {PHASE_III_FREEZE,epochHierarchy,EPOCH_SIZE} from "./ada-211n-epoch-engine.mjs";
export const EPOCH_CONTACT_SCHEMA="ADA-214N.epoch-contacts.v1";
const freeze=x=>Object.freeze(x),round=v=>Number(v.toFixed(6));
function roleId(epoch,name){return "ADA214-"+name+"-E"+String(epoch).padStart(5,"0")}
export function deriveEpochContacts(chain,{size=EPOCH_SIZE}={}){
 const checked=verifyChain(chain);if(!checked.pass)throw Error("Invalid immutable source: "+checked.reason);
 const epochs=epochHierarchy(chain,{size}),contacts=deriveContacts(chain),out=[];
 for(const e of epochs){
  const previous=out.at(-1),last=chain[e.sourceEnd];
  const sourceContacts=contacts.slice(e.sourceStart,e.sourceEnd+1);
  const observations=sourceContacts.map(c=>c.state.jane.observation);
  const mean=round(observations.reduce((a,b)=>a+b,0)/observations.length);
  const jane=freeze({id:roleId(e.epoch,"JANE"),inherited:previous?.state.jane.id||null,
    observationMean:mean,latestObservation:last.contacts[0],
    deltaFromParent:round(mean-(previous?.state.jane.observationMean??mean)),
    sourceContactTip:sourceContacts.at(-1).hash});
  const toph=freeze({id:roleId(e.epoch,"TOPH"),inherited:previous?.state.toph.id||null,
    minimumStability:Math.min(...chain.slice(e.sourceStart,e.sourceEnd+1).map(g=>g.stability)),
    minimumEnergy:Math.min(...chain.slice(e.sourceStart,e.sourceEnd+1).map(g=>g.energy)),
    acceptedAppends:e.appends,heldDecisions:e.holds,
    eligibleToSeal:e.state==="SEALED",rule:"Original generation gate remains authoritative; completed epoch alone may SEALED"});
  const ada=freeze({id:roleId(e.epoch,"ADA"),inherited:previous?.state.ada.id||null,
    action:e.state==="SEALED"?"SEAL":"OPEN_TAIL",authority:"ONE_SOURCE_GATE",
    recordedAppends:e.appends,recordedHolds:e.holds,
    previousDecision:previous?.state.ada.action||null});
  const state=freeze({jane,toph,ada});
  const body={schema:EPOCH_CONTACT_SCHEMA,epoch:e.epoch,phaseIIIFreeze:PHASE_III_FREEZE,
    originalRoot:PHASE_II_FREEZE,epochHash:e.hash,parentContactHash:previous?.hash||null,
    sourceEnd:e.sourceEnd,sourceGenerationHash:last.hash,sourceContactHash:contacts[e.sourceEnd].hash,
    state,decision:ada.action,retention:"Derived epoch state only. Original source decisions and sealed receipts unchanged."};
  out.push(freeze({...body,hash:fnv64(canonical(body))}));
 }
 return freeze(out);
}
export function verifyEpochContacts(chain,ledger,{size=EPOCH_SIZE}={}){
 try{
  if(!Array.isArray(ledger))return {pass:false,reason:"Epoch contacts must be an array"};
  const expected=deriveEpochContacts(chain,{size});
  if(canonical(ledger)!==canonical(expected))return {pass:false,reason:"Epoch contact ancestry or role state mismatch"};
  return {pass:true,epochs:ledger.length,sealed:ledger.filter(x=>x.decision==="SEAL").length,
    open:ledger.filter(x=>x.decision==="OPEN_TAIL").length,
    holds:ledger.reduce((sum,x)=>sum+x.state.ada.recordedHolds,0),
    sourceRoot:PHASE_II_FREEZE,phaseIIIFreeze:PHASE_III_FREEZE,tip:ledger.at(-1).hash};
 }catch(error){return {pass:false,reason:error.message}}
}
export function epochContactProof(chain,epoch,{size=EPOCH_SIZE}={}){
 const ledger=deriveEpochContacts(chain,{size});
 if(!Number.isSafeInteger(epoch)||epoch<0||epoch>=ledger.length)throw Error("Epoch index outside inherited contacts");
 const e=ledger[epoch];
 return freeze({schema:"ADA-214N.epoch-contact-proof.v1",epoch,phaseIIIFreeze:PHASE_III_FREEZE,
  epochHash:e.epochHash,contactHash:e.hash,parentContactHash:e.parentContactHash,
  sourceGenerationHash:e.sourceGenerationHash,roles:e.state,decision:e.decision,
  originalSourceRoots:1});
}
