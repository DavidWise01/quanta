// ADA-259N .dlw — contextual stability audit.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveAdaptiveContext,verifyAdaptiveContext,adaptiveContextFixtures} from "./ada-258n-adaptive-context.mjs";
import {derivePatterns,patternFixtures} from "./ada-256n-pattern-recognition.mjs";
import {associationFixtures} from "./ada-255n-contextual-association.mjs";
import {semanticFixtures} from "./ada-254n-semantic-differentiation.mjs";
import {temporalFixtures} from "./ada-253n-temporal-relationships.mjs";
export function auditContext(chain){
 const before=canonical(chain),a=deriveAdaptiveContext(chain),s=derivePatterns(chain),epochs=epochHierarchy(chain);
 const prefix=deriveAdaptiveContext(chain.slice(0,Math.min(48,chain.length)));
 const checks={
 replay:verifyAdaptiveContext(chain,a).pass,
 unchanged:before===canonical(chain),
 prefix:prefix.every((r,i)=>canonical(r)===canonical(a[i])),
 lineage:a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.patternHash===s[i].hash&&r.sourceHash===chain[i].hash),
 policyAncestry:epochs.every(e=>a.slice(e.sourceStart,e.sourceEnd+1).every(r=>r.policyParent===(e.sourceStart?a[e.sourceStart-1].hash:null))),
 policyHold:epochs.every((e,i)=>!i||!epochs[i-1].holds||canonical(a[e.sourceStart].policy)===canonical(a[e.sourceStart-1].policy)),
 bounds:a.every(r=>r.policy.window>=3&&r.policy.window<=8&&r.policy.threshold>=75&&r.policy.threshold<=100),
 history:a.every(r=>r.history.length<=r.policy.window&&new Set(r.history.map(h=>h.generation)).size===r.history.length&&r.history.every(h=>h.generation<=r.generation)),
 qualification:a.every(r=>canonical(r.qualified)===canonical(r.patterns.filter(p=>p.present&&p.supported&&!p.incomplete&&r.history.length>=3&&p.occurrences*100>=r.policy.threshold*r.history.length).map(p=>p.mask))),
 directSupport:a.every(r=>r.qualified.every(mask=>{const members=Array.from({length:9},(_,i)=>i).filter(i=>mask&(1<<i));return members.length>=2&&members.every((x,i)=>members.slice(i+1).every(y=>r.history.at(-1).edges.some(e=>e.from===x&&e.to===y&&e.semantic==="STABLE_AGREEMENT")))})),
 authority:a.every(r=>r.authority==="OBSERVE_ONLY"),growth:a.every(r=>r.growthFactor===1.025)};
 const fixtures={temporal:temporalFixtures(),semantic:semanticFixtures(),association:associationFixtures(),pattern:patternFixtures(),adaptive:adaptiveContextFixtures()};
 return {pass:Object.values(checks).every(Boolean)&&Object.values(fixtures).every(f=>f.pass),checks,fixtures,generations:a.length,epochs:epochs.length,tip:a.at(-1)?.hash};
}
export function stressContext(steps=240){
 if(!Number.isSafeInteger(steps)||steps<1||steps>2400)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 return auditContext(chain);
}
