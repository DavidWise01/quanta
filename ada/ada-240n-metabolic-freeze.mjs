// ADA-240N .dlw — final Phase VI acceptance candidate.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {auditMetabolism,disturbanceSuite} from "./ada-239n-metabolic-stability.mjs";
import {deriveEquilibrium} from "./ada-238n-adaptive-equilibrium.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
export function certifyMetabolism(chain){
 const audit=auditMetabolism(chain),fixtures=disturbanceSuite(),a=deriveEquilibrium(chain),epochs=epochHierarchy(chain);
 const checks={...audit.checks,disturbances:fixtures.pass,epochBalance:epochs.every(e=>a[e.sourceStart].levels.every((l,d)=>{const rows=a.slice(e.sourceStart,e.sourceEnd+1).map(r=>r.levels[d]);return l.inputOpening+l.activeOpening+rows.reduce((n,r)=>n+r.accepted-r.spent,0)===rows.at(-1).totalClosing})),sealedPrefix:epochs.filter(e=>e.state==="SEALED").every(e=>a[e.sourceEnd].epoch===e.epoch),compartmentBounds:a.every(r=>r.levels.every(l=>l.activeClosing<=Math.floor(l.capacity/2)&&l.totalClosing<=l.capacity&&l.accepted<=l.offered&&l.spent<=l.requested)),holdPolicy:epochs.every((e,i)=>!i||!epochs[i-1].holds||a[e.sourceStart].levels.every((l,d)=>canonical(l.policy)===canonical(a[e.sourceStart-1].levels[d].policy)))};
 return {pass:Object.values(checks).every(Boolean),checks,audit,fixtures,epochs:epochs.length,status:Object.values(checks).every(Boolean)?"RUNTIME_GATE_PASS":"REJECTED"};
}
export function runMetabolicFreeze(steps=2400){
 if(!Number.isSafeInteger(steps)||steps<1||steps>9600)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 return certifyMetabolism(chain);
}
