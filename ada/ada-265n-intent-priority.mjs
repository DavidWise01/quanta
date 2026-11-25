// ADA-265N .dlw — deterministic preference, not authorization.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveIntentDifferentiation,verifyIntentDifferentiation} from "./ada-264n-intent-differentiation.mjs";
export function prioritizeIntent(candidates){
 const eligible=candidates.filter(c=>c.differentiation==="DIFFERENTIATED"&&c.groundingStatus==="GROUNDED"&&c.proposal!==null);
 const defer=eligible.find(c=>c.domain==="DEFER");
 if(!defer)throw Error("Missing grounded deferral");
 const complete=defer.metrics.coverage===100;
 const ranked=eligible.map(c=>{
 const m=c.metrics;
 const score=c.domain==="DEFER"?0:c.domain==="PRESERVE"?m.distinctPairs*2+Math.min(m.stability,36):m.distinctPairs*2+Math.min(m.changes,36);
 return {address:c.address,domain:c.domain,score,eligible:c.domain==="DEFER"||complete&&score>0};
 }).filter(c=>c.eligible).sort((a,b)=>b.score-a.score||({DEFER:0,PRESERVE:1,ADAPT:2})[a.domain]-({DEFER:0,PRESERVE:1,ADAPT:2})[b.domain]||a.address-b.address);
 return Object.freeze({ranking:Object.freeze(ranked.map((c,i)=>Object.freeze({...c,rank:i+1}))),preferred:ranked[0].address,reason:!complete?"INSUFFICIENT_COVERAGE":ranked[0].domain==="DEFER"?"NO_SUPPORTED_ALTERNATIVE":"MAXIMUM_BOUNDED_SUPPORT",execution:false});
}
export function deriveIntentPriority(chain){
 const source=deriveIntentDifferentiation(chain);if(!verifyIntentDifferentiation(chain,source).pass)throw Error("Differentiation replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const priority=prioritizeIntent(r.candidates);
 const body={schema:"ADA-265N.intent-priority.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,contextHash:r.contextHash,differentiationHash:r.hash,parent,candidates:r.candidates,priority,selected:null,authority:"OBSERVE_ONLY",execution:false,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyIntentPriority(chain,ledger){
 try{const a=deriveIntentPriority(chain),s=deriveIntentDifferentiation(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.differentiationHash===s[i].hash&&canonical(r.candidates)===canonical(s[i].candidates)&&canonical(r.priority)===canonical(prioritizeIntent(r.candidates))&&r.priority.ranking.length>=1&&r.priority.preferred===r.priority.ranking[0].address&&r.selected===null&&!r.priority.execution&&!r.execution&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function priorityFixtures(){
 const c=(address,domain,coverage,pairs,stability,changes,formed=true)=>({address,domain,proposal:formed?"PROPOSAL":null,groundingStatus:formed?"GROUNDED":"UNFORMED",differentiation:formed?"DIFFERENTIATED":"UNFORMED",metrics:{coverage,distinctPairs:pairs,stability,changes}});
 const f=(coverage,p,a)=>prioritizeIntent([c(0,"PRESERVE",coverage,p,p,0),c(1,"ADAPT",coverage,a,0,a),c(2,"DEFER",coverage,0,0,0)]);
 const checks={preserve:f(100,4,2).preferred===0,adapt:f(100,2,4).preferred===1,tie:f(100,3,3).preferred===0,missing:f(99,4,5).preferred===2,zero:f(100,0,0).preferred===2,noExecution:!f(100,4,5).execution,unformed:prioritizeIntent([c(0,"PRESERVE",100,36,36,0,false),c(1,"ADAPT",100,0,0,0,false),c(2,"DEFER",100,0,0,0)]).preferred===2};
 return {pass:Object.values(checks).every(Boolean),checks};
}
