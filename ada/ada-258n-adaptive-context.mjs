// ADA-258N .dlw — prospective contextual policy, observation only.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {derivePatterns,verifyPatterns,recognize} from "./ada-256n-pattern-recognition.mjs";
export const INITIAL_POLICY=Object.freeze({window:8,threshold:75});
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
export function adaptContext(previous,history){
 if(history.length<8||history.some(h=>h.edges.length!==36||h.edges.some(e=>e.semantic==="INSUFFICIENT")))return Object.freeze({...previous});
 const signatures=history.map(h=>canonical(h.groups.map(g=>g.mask).sort((a,b)=>a-b)));
 const changes=signatures.slice(1).filter((s,i)=>s!==signatures[i]).length;
 const step=changes>=4?-1:changes===0?1:0;
 return Object.freeze({window:clamp(previous.window+step,3,8),threshold:clamp(previous.threshold-step*5,75,100)});
}
export function deriveAdaptiveContext(chain){
 const source=derivePatterns(chain);if(!verifyPatterns(chain,source).pass)throw Error("Pattern replay failed");
 let prior=null,previousEpoch=null;const result=[];
 for(const e of epochHierarchy(chain)){
 const policy=previousEpoch?.state==="SEALED"&&previousEpoch.holds===0?adaptContext(previousEpoch.policy,previousEpoch.history):previousEpoch?.policy??INITIAL_POLICY;
 for(let i=e.sourceStart;i<=e.sourceEnd;i++){
 const s=source[i],history=Object.freeze(s.history.slice(-policy.window)),patterns=recognize(history);
 const qualified=Object.freeze(patterns.filter(p=>p.present&&p.supported&&!p.incomplete&&history.length>=3&&p.occurrences*100>=policy.threshold*history.length).map(p=>p.mask));
 const body={schema:"ADA-258N.adaptive-context.v1",generation:s.generation,epoch:e.epoch,sourceHash:s.sourceHash,patternHash:s.hash,parent:prior?.hash??null,policyParent:previousEpoch?.hash??null,policy,history,patterns,qualified,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});result.push(prior);
 }
 previousEpoch={state:e.state,holds:e.holds,policy,history:source[e.sourceEnd].history,hash:prior.hash};
 }
 return Object.freeze(result);
}
export function verifyAdaptiveContext(chain,ledger){
 try{const a=deriveAdaptiveContext(chain),s=derivePatterns(chain),epochs=epochHierarchy(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.patternHash===s[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.policy.window>=3&&r.policy.window<=8&&r.policy.threshold>=75&&r.policy.threshold<=100&&canonical(r.history)===canonical(s[i].history.slice(-r.policy.window))&&(!i||r.epoch!==a[i-1].epoch||canonical(r.policy)===canonical(a[i-1].policy))&&r.qualified.every(mask=>r.patterns.some(p=>p.mask===mask&&p.present&&p.supported&&!p.incomplete&&p.occurrences*100>=r.policy.threshold*r.history.length)))&&epochs.every((e,i)=>!i||!epochs[i-1].holds||canonical(a[e.sourceStart].policy)===canonical(a[e.sourceStart-1].policy)),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function adaptiveContextFixtures(){
 const history=(volatile=false,missing=false)=>Array.from({length:8},(_,i)=>({groups:[{mask:volatile&&i%2?3:7}],edges:Array.from({length:36},()=>({semantic:missing?"INSUFFICIENT":"STABLE_AGREEMENT"}))}));
 const base={window:6,threshold:85},stable=adaptContext(base,history()),volatile=adaptContext(base,history(true));
 const checks={stable:stable.window===7&&stable.threshold===80,volatile:volatile.window===5&&volatile.threshold===90,missing:canonical(adaptContext(base,history(false,true)))===canonical(base),warmup:canonical(adaptContext(base,history().slice(0,7)))===canonical(base),upper:canonical(adaptContext(INITIAL_POLICY,history()))===canonical(INITIAL_POLICY),lower:canonical(adaptContext({window:3,threshold:100},history(true)))===canonical({window:3,threshold:100})};
 return {pass:Object.values(checks).every(Boolean),checks};
}
