// ADA-211N · Phase IV: a generation of generations (epoch hierarchy).
// Additive deterministic projection over immutable Phase III source generations.
// A new epoch never mutates its parent generation or a previously sealed epoch.
import {PHASE_II_FREEZE,verifyChain,canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveContacts} from "./ada-204n-three-contact-inheritance.mjs";
import {deriveGrowth} from "./ada-205n-homeostatic-growth.mjs";
import {deriveMutations} from "./ada-206n-bounded-mutation.mjs";
export const PHASE_III_FREEZE="59c1419b01ac2c0c592fd650b12a0a11f5b8bb44";
export const EPOCH_SCHEMA="ADA-211N.epoch.v1";
export const EPOCH_SIZE=24;
export function epochHierarchy(chain,{size=EPOCH_SIZE}={}){
 if(!Number.isSafeInteger(size)||size<1||size>256)throw Error("Epoch capacity must be 1..256");
 const check=verifyChain(chain);if(!check.pass)throw Error("Invalid inherited source: "+check.reason);
 const contacts=deriveContacts(chain),growth=deriveGrowth(chain),mutation=deriveMutations(chain);
 const epochs=[];
 for(let start=0;start<chain.length;start+=size){
  const end=Math.min(start+size,chain.length),slice=chain.slice(start,end),n=epochs.length,parent=epochs.at(-1);
  const decisions=Object.freeze(slice.map(x=>x.decision));
  const holds=decisions.filter(x=>x==="HOLD").length,appends=decisions.filter(x=>x==="APPEND").length;
  const isSealed=end-start===size;
  const frame={schema:EPOCH_SCHEMA,epoch:n,sourceRoot:PHASE_II_FREEZE,phaseIIIFreeze:PHASE_III_FREEZE,
   parentEpochHash:parent?.hash||null,sourceStart:start,sourceEnd:end-1,count:end-start,
   firstSourceHash:slice[0].hash,lastSourceHash:slice.at(-1).hash,
   firstInheritedParent:slice[0].parent,contactTip:contacts[end-1].hash,
   growthTip:growth[end-1].hash,mutationTip:mutation[end-1].hash,
   holds,appends,rootDecisions:decisions.filter(x=>x==="ROOT").length,
   state:isSealed?"SEALED":"OPEN_TAIL",decisions,
   policy:"One original frozen source root; epoch children are not independent witnesses"};
  epochs.push(Object.freeze({...frame,hash:fnv64(canonical(frame))}));
 }
 return Object.freeze(epochs);
}
export function verifyEpochs(chain,epochs,{size=EPOCH_SIZE}={}){
 try{
  if(!Array.isArray(epochs))return {pass:false,reason:"Expected epoch array"};
  const expected=epochHierarchy(chain,{size});
  if(canonical(epochs)!==canonical(expected))return {pass:false,reason:"Epoch hierarchy or parent hash mismatch"};
  return {pass:true,epochs:epochs.length,sealed:epochs.filter(x=>x.state==="SEALED").length,
    tail:epochs.at(-1).state,totalGenerations:chain.length,
    holds:epochs.reduce((acc,e)=>acc+e.holds,0),tip:epochs.at(-1).hash,
    phaseIIIFreeze:PHASE_III_FREEZE};
 }catch(e){return {pass:false,reason:e.message}}
}
export function epochProof(chain,n,{size=EPOCH_SIZE}={}){
 const epochs=epochHierarchy(chain,{size});
 if(!Number.isSafeInteger(n)||n<0||n>=epochs.length)throw Error("Epoch index outside derived hierarchy");
 const e=epochs[n];
 return Object.freeze({schema:"ADA-211N.epoch-proof.v1",phaseIIIFreeze:PHASE_III_FREEZE,
   originalSourceRoot:PHASE_II_FREEZE,epoch:n,epochHash:e.hash,
   previousEpochHash:e.parentEpochHash,firstSourceHash:e.firstSourceHash,lastSourceHash:e.lastSourceHash,
   count:e.count,holds:e.holds,appends:e.appends,state:e.state});
}
