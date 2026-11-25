// ADA-266N .dlw — bounded hypothetical consequences, never execution.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveIntentPriority,verifyIntentPriority} from "./ada-265n-intent-priority.mjs";
export const SCENARIOS=Object.freeze(["STABLE","CHANGE","UNKNOWN"]);
export function modelConsequences(record){
 const candidate=record.candidates.find(c=>c.address===record.priority.preferred);
 if(!candidate||candidate.groundingStatus!=="GROUNDED"||record.execution!==false)throw Error("Invalid prospective source");
 const domain=candidate.domain;
 const outcomes=SCENARIOS.map(scenario=>{
 const consequence=scenario==="UNKNOWN"?"UNRESOLVED":domain==="DEFER"?"JUDGMENT_RESERVED":domain==="PRESERVE"?(scenario==="STABLE"?"CONTINUITY":"POSSIBLE_MISMATCH"):(scenario==="CHANGE"?"REVIEW_MAY_BE_RELEVANT":"REVIEW_MAY_BE_UNNECESSARY");
 return Object.freeze({scenario,consequence,observed:false,probability:null,execution:false,authority:"HYPOTHETICAL_ONLY"});
 });
 return Object.freeze({preferred:record.priority.preferred,domain,outcomes:Object.freeze(outcomes),recommendation:domain==="DEFER"?"RESERVE_JUDGMENT":"RETAIN_FOR_REVIEW",execution:false});
}
export function deriveConsequences(chain){
 const source=deriveIntentPriority(chain);if(!verifyIntentPriority(chain,source).pass)throw Error("Priority replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const body={schema:"ADA-266N.consequences.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,priorityHash:r.hash,contextHash:r.contextHash,parent,model:modelConsequences(r),selected:null,authority:"OBSERVE_ONLY",execution:false,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyConsequences(chain,ledger){
 try{const a=deriveConsequences(chain),s=deriveIntentPriority(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.priorityHash===s[i].hash&&r.sourceHash===s[i].sourceHash&&r.model.preferred===s[i].priority.preferred&&r.model.outcomes.length===3&&r.model.outcomes.every((o,j)=>o.scenario===SCENARIOS[j]&&!o.observed&&o.probability===null&&!o.execution&&o.authority==="HYPOTHETICAL_ONLY")&&r.selected===null&&!r.execution&&!r.model.execution&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function consequenceFixtures(){
 const f=domain=>modelConsequences({candidates:[{address:0,domain,groundingStatus:"GROUNDED"}],priority:{preferred:0},execution:false});
 const p=f("PRESERVE"),a=f("ADAPT"),d=f("DEFER");
 const checks={continuity:p.outcomes[0].consequence==="CONTINUITY",mismatch:p.outcomes[1].consequence==="POSSIBLE_MISMATCH",review:a.outcomes[1].consequence==="REVIEW_MAY_BE_RELEVANT",unnecessary:a.outcomes[0].consequence==="REVIEW_MAY_BE_UNNECESSARY",unknown:[p,a,d].every(r=>r.outcomes[2].consequence==="UNRESOLVED"),defer:d.recommendation==="RESERVE_JUDGMENT",noExecution:[p,a,d].every(r=>!r.execution&&r.outcomes.every(o=>!o.observed&&!o.execution&&o.probability===null))};
 return {pass:Object.values(checks).every(Boolean),checks};
}
