// ADA-260N .dlw — Phase VIII source freeze acceptance candidate.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {auditContext} from "./ada-259n-contextual-stability.mjs";
import {deriveContextualInheritance,verifyContextualInheritance} from "./ada-257n-contextual-inheritance.mjs";
import {deriveAdaptiveContext} from "./ada-258n-adaptive-context.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
export function certifyContext(chain){
 const before=canonical(chain),audit=auditContext(chain),receipts=deriveContextualInheritance(chain),epochs=epochHierarchy(chain),a=deriveAdaptiveContext(chain);
 const checks={...audit.checks,fixtures:Object.values(audit.fixtures).every(f=>f.pass),inheritance:verifyContextualInheritance(chain,receipts).pass,epochBinding:receipts.length===epochs.length&&receipts.every((r,i)=>r.epochHash===epochs[i].hash&&r.state===epochs[i].state),receiptAuthority:receipts.every(r=>r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025),noFuture:a.every(r=>r.history.every(h=>h.generation<=r.generation)),sourcePreserved:before===canonical(chain)};
 const pass=audit.pass&&Object.values(checks).every(Boolean);
 return {pass,status:pass?"RUNTIME_GATE_PASS":"REJECTED",checks,audit,epochs:epochs.length,authority:"OBSERVE_ONLY"};
}
export function runContextFreeze(steps=240){
 if(!Number.isSafeInteger(steps)||steps<1||steps>2400)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 return certifyContext(chain);
}
