// ADA-261N .dlw — bounded intent address space, no execution.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveAdaptiveContext,verifyAdaptiveContext} from "./ada-258n-adaptive-context.mjs";
export const PHASE_VIII_PARENT="1d5208a8e5012c846c62974cb3b8293fe7e49331";
export function intentContainer(){
 return Object.freeze(["PRESERVE","ADAPT","DEFER"].map((domain,address)=>Object.freeze({address,domain,proposal:null,grounding:null,status:"UNFORMED",execution:false})));
}
export function deriveIntentArchitecture(chain){
 const source=deriveAdaptiveContext(chain);if(!verifyAdaptiveContext(chain,source).pass)throw Error("Context replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const body={schema:"ADA-261N.intent-architecture.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,contextHash:r.hash,phaseVIIIParent:PHASE_VIII_PARENT,parent,qualifiedContext:r.qualified,domains:intentContainer(),selected:null,authority:"OBSERVE_ONLY",execution:false,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyIntentArchitecture(chain,ledger){
 try{const a=deriveIntentArchitecture(chain),s=deriveAdaptiveContext(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.contextHash===s[i].hash&&r.sourceHash===s[i].sourceHash&&canonical(r.qualifiedContext)===canonical(s[i].qualified)&&r.domains.length===3&&r.domains.every((d,j)=>d.address===j&&d.proposal===null&&d.grounding===null&&d.status==="UNFORMED"&&!d.execution)&&r.selected===null&&!r.execution&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
