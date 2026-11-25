// ADA-263N .dlw — exact contextual grounding; no authorization.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveCandidates,verifyCandidates,formCandidates} from "./ada-262n-intent-candidates.mjs";
import {deriveAdaptiveContext} from "./ada-258n-adaptive-context.mjs";
export function groundCandidates(record,context){
 if(record.contextHash!==context.hash||record.generation!==context.generation||record.sourceHash!==context.sourceHash)throw Error("Context ancestry mismatch");
 if(canonical(record.candidates)!==canonical(formCandidates(context)))throw Error("Candidate mismatch");
 const latest=context.history.at(-1);
 return Object.freeze(record.candidates.map(c=>{
 const references=Object.freeze(c.support.map(mask=>{
 const p=context.patterns.find(p=>p.mask===mask);
 if(!p)throw Error("Missing pattern");
 const members=Object.freeze([...p.members]);
 const history=Object.freeze(context.history.map(h=>Object.freeze({generation:h.generation,associationHash:h.associationHash,edges:Object.freeze(h.edges.filter(e=>members.includes(e.from)&&members.includes(e.to)))})));
 return Object.freeze({mask,members,status:p.status,present:p.present,history});
 }));
 const grounded=c.proposal!==null&&(c.domain==="DEFER"||references.length>0);
 return Object.freeze({...c,grounding:grounded?Object.freeze({contextHash:context.hash,patternHash:context.patternHash,sourceHash:context.sourceHash,generation:context.generation,latestAssociationHash:latest?.associationHash??null,references,basis:c.domain==="DEFER"?c.reason:"CONTEXTUAL_SUPPORT"}):null,groundingStatus:grounded?"GROUNDED":"UNFORMED",execution:false});
 }));
}
export function deriveGroundedIntent(chain){
 const source=deriveCandidates(chain),contexts=deriveAdaptiveContext(chain);
 if(!verifyCandidates(chain,source).pass)throw Error("Candidate replay failed");
 let parent=null;
 return Object.freeze(source.map((r,i)=>{
 const body={schema:"ADA-263N.grounded-intent.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,candidateHash:r.hash,contextHash:r.contextHash,parent,candidates:groundCandidates(r,contexts[i]),selected:null,authority:"OBSERVE_ONLY",execution:false,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyGroundedIntent(chain,ledger){
 try{const a=deriveGroundedIntent(chain),s=deriveCandidates(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.candidateHash===s[i].hash&&r.selected===null&&!r.execution&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025&&r.candidates.every(c=>!c.execution&&(c.groundingStatus==="GROUNDED")===(c.grounding!==null)&&(!c.grounding||c.grounding.contextHash===r.contextHash&&c.grounding.generation===r.generation&&c.grounding.references.every(p=>p.history.every(h=>h.generation<=r.generation))))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
