// ADA-250N .dlw — Phase VII acceptance candidate.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {auditPerception,perceptualFixtures} from "./ada-249n-perceptual-stability.mjs";
import {deriveAdaptivePerception} from "./ada-248n-adaptive-perception.mjs";
import {derivePerceptualInheritance,verifyPerceptualInheritance} from "./ada-247n-perceptual-inheritance.mjs";
import {deriveAcquisition} from "./ada-242n-signal-acquisition.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
export function certifyPerception(chain){
 const audit=auditPerception(chain),fixtures=perceptualFixtures(),a=deriveAdaptivePerception(chain),raw=deriveAcquisition(chain),epochs=epochHierarchy(chain),receipts=derivePerceptualInheritance(chain);
 const checks={...audit.checks,fixtures:fixtures.pass,inheritance:verifyPerceptualInheritance(chain,receipts).pass,rawAddresses:raw.every((r,i)=>r.sourceHash===chain[i].hash&&r.levels.length===3&&r.levels.every(l=>l.axes.length===3&&l.axes.every(x=>x.faces.length===2&&x.faces.every(f=>f.observed===(f.raw!==null))))),effectiveBounds:a.every(r=>r.channels.every(c=>c.current===null?c.effective===null&&c.state===null:Math.abs(c.effective)<=Math.abs(c.current))),sealedReceipts:epochs.every((e,i)=>receipts[i].epochHash===e.hash&&receipts[i].state===e.state),noAuthority:a.every(r=>r.authority==="OBSERVE_ONLY")};
 return {pass:Object.values(checks).every(Boolean),checks,audit,fixtures,epochs:epochs.length,status:Object.values(checks).every(Boolean)?"RUNTIME_GATE_PASS":"REJECTED"};
}
export function runPerceptualFreeze(steps=2400){
 if(!Number.isSafeInteger(steps)||steps<1||steps>9600)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 return certifyPerception(chain);
}
