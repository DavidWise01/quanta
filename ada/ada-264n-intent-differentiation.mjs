// ADA-264N .dlw — differentiated intent direction and bounded evidence measures.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveGroundedIntent,verifyGroundedIntent} from "./ada-263n-intent-grounding.mjs";
import {deriveAdaptiveContext} from "./ada-258n-adaptive-context.mjs";
export function differentiateIntent(record,context){
 if(record.contextHash!==context.hash||record.generation!==context.generation)throw Error("Context ancestry mismatch");
 const edges=context.history.at(-1)?.edges??[];
 const coverage=edges.length===36?Math.floor(100*edges.filter(e=>e.semantic!=="INSUFFICIENT").length/36):0;
 return Object.freeze(record.candidates.map(c=>{
 const eligible=c.groundingStatus==="GROUNDED"&&c.proposal!==null&&c.grounding?.contextHash===context.hash;
 const refs=c.grounding?.references??[];
 const supportMasks=new Set(refs.map(r=>r.mask));
 const pairs=new Set(refs.flatMap(r=>r.history.at(-1)?.edges.filter(e=>e.semantic!=="INSUFFICIENT").map(e=>e.from+":"+e.to)??[]));
 const changes=refs.filter(r=>["FORMING","FRAGMENTING","DISSOLVING","RECURRING"].includes(r.status)).length;
 const stability=refs.filter(r=>context.qualified.includes(r.mask)).length;
 return Object.freeze({...c,direction:eligible?({PRESERVE:-1,DEFER:0,ADAPT:1})[c.domain]:null,differentiation:eligible?"DIFFERENTIATED":"UNFORMED",metrics:Object.freeze({coverage,uncertainty:100-coverage,distinctGroups:supportMasks.size,distinctPairs:pairs.size,changes,stability}),execution:false});
 }));
}
export function deriveIntentDifferentiation(chain){
 const source=deriveGroundedIntent(chain),contexts=deriveAdaptiveContext(chain);
 if(!verifyGroundedIntent(chain,source).pass)throw Error("Grounding replay failed");
 let parent=null;
 return Object.freeze(source.map((r,i)=>{
 const body={schema:"ADA-264N.intent-differentiation.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,groundingHash:r.hash,contextHash:r.contextHash,parent,candidates:differentiateIntent(r,contexts[i]),selected:null,authority:"OBSERVE_ONLY",execution:false,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyIntentDifferentiation(chain,ledger){
 try{const a=deriveIntentDifferentiation(chain),s=deriveGroundedIntent(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.groundingHash===s[i].hash&&r.selected===null&&!r.execution&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025&&r.candidates.every((c,j)=>{const {direction,differentiation,metrics,...original}=c;return canonical(original)===canonical(s[i].candidates[j])&&direction===(c.groundingStatus==="GROUNDED"?({PRESERVE:-1,DEFER:0,ADAPT:1})[c.domain]:null)&&metrics.coverage+metrics.uncertainty===100&&metrics.distinctPairs<=36&&metrics.distinctGroups<=502&&!c.execution})),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
