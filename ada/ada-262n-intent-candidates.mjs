// ADA-262N .dlw — bounded proposal formation; no selection or execution.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveIntentArchitecture,verifyIntentArchitecture} from "./ada-261n-bounded-intent.mjs";
import {deriveAdaptiveContext} from "./ada-258n-adaptive-context.mjs";
export function formCandidates(context){
 const qualified=Object.freeze([...context.qualified]);
 const changes=Object.freeze(context.patterns.filter(p=>["FORMING","FRAGMENTING","DISSOLVING","RECURRING"].includes(p.status)&&!p.incomplete).map(p=>p.mask).sort((a,b)=>a-b));
 const incomplete=context.history.at(-1)?.edges.some(e=>e.semantic==="INSUFFICIENT")??true;
 const ready=context.history.length>=3&&!incomplete;
 return Object.freeze([
 Object.freeze({address:0,domain:"PRESERVE",proposal:ready&&qualified.length?"RETAIN_CONTEXT_POLICY":null,support:qualified,status:ready&&qualified.length?"CANDIDATE":"UNFORMED",execution:false}),
 Object.freeze({address:1,domain:"ADAPT",proposal:ready&&changes.length?"REVIEW_CONTEXT_POLICY":null,support:changes,status:ready&&changes.length?"CANDIDATE":"UNFORMED",execution:false}),
 Object.freeze({address:2,domain:"DEFER",proposal:"RESERVE_JUDGMENT",support:Object.freeze([]),status:"CANDIDATE",reason:ready?"SAFE_BASELINE":"INSUFFICIENT_CONTEXT",execution:false})
 ]);
}
export function deriveCandidates(chain){
 const source=deriveIntentArchitecture(chain),contexts=deriveAdaptiveContext(chain);
 if(!verifyIntentArchitecture(chain,source).pass)throw Error("Intent architecture replay failed");
 let parent=null;
 return Object.freeze(source.map((r,i)=>{
 const c=contexts[i];if(r.contextHash!==c.hash)throw Error("Context ancestry mismatch");
 const body={schema:"ADA-262N.candidates.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,intentHash:r.hash,contextHash:c.hash,parent,candidates:formCandidates(c),selected:null,authority:"OBSERVE_ONLY",execution:false,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyCandidates(chain,ledger){
 try{const a=deriveCandidates(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.candidates.length===3&&r.candidates.every((c,j)=>c.address===j&&!c.execution&&(c.status==="CANDIDATE")===(c.proposal!==null))&&r.candidates[2].proposal==="RESERVE_JUDGMENT"&&r.selected===null&&!r.execution&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function candidateFixtures(){
 const context=(qualified,patterns,missing=false,n=3)=>({qualified,patterns,history:Array.from({length:n},()=>({edges:[{semantic:missing?"INSUFFICIENT":"STABLE_AGREEMENT"}]}))});
 const stable=formCandidates(context([7],[])),change=formCandidates(context([],[{mask:7,status:"FRAGMENTING",incomplete:false}])),missing=formCandidates(context([7],[],true)),warmup=formCandidates(context([7],[],false,2));
 const checks={preserve:stable[0].status==="CANDIDATE",adapt:change[1].status==="CANDIDATE",missing:missing.slice(0,2).every(c=>c.proposal===null),warmup:warmup.slice(0,2).every(c=>c.proposal===null),defer:[stable,change,missing,warmup].every(c=>c[2].status==="CANDIDATE"),noExecution:[stable,change,missing,warmup].flat().every(c=>!c.execution)};
 return {pass:Object.values(checks).every(Boolean),checks};
}
